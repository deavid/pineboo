# -*- coding: utf-8 -*-
from PyQt5 import QtCore

import time
import os
import logging
import zlib
import sys
import traceback

import pineboolib
from pineboolib.utils import filedir, one, Struct, XMLStruct, cacheXPM, parseTable, _path, coalesce_path, _dir
from pineboolib.fllegacy.flutil import FLUtil
from pineboolib.fllegacy.flsettings import FLSettings
from pineboolib.mtdparser.pnmtdparser import mtd_parse

"""
Almacena los datos del serividor de la BD principal
"""


class DBServer(XMLStruct):
    host = None
    port = None


"""
Almacena los datos de autenticación de la BD principal
"""


class DBAuth(XMLStruct):
    username = None
    password = None


"""
Esta es la clase principal del projecto. Se puede acceder a esta con pineboolib.project desde cualquier parte del projecto
"""


class Project(object):
    logger = logging.getLogger("main.Project")
    conn = None  # Almacena la conexión principal a la base de datos
    debugLevel = 100

    #_initModules = None
    main_window = None
    acl_ = None
    _DGI = None
    deleteCache = None
    path = None
    kugarPluging = None
    _splash = None
    sql_drivers_manager = None
    timer_ = None
    """
    Constructor
    """

    def __init__(self, DGI):

        from pineboolib.plugins.kugar.pnkugarplugins import PNKugarPlugins
        self._DGI = DGI
        self.tree = None
        self.root = None
        self.dbserver = None
        self.dbauth = None
        self.dbname = None
        self.apppath = None
        self.tmpdir = None
        self.parser = None
        self.version = 0.7
        self.main_form_name = "eneboo" if not self._DGI.mobilePlatform() else "mobile"
        pineboolib.project = self
        self.deleteCache = False
        self.parseProject = False
        self.translator_ = []
        self.actions = {}
        self.tables = {}
        self.files = {}
        self.apppath = filedir("..")
        self.tmpdir = FLSettings().readEntry("ebcomportamiento/kugar_temp_dir", filedir("../tempdata"))
        if not os.path.exists(self.tmpdir):
            os.mkdir(self.tmpdir)
        self.kugarPlugin = PNKugarPlugins()

        if not self._DGI.localDesktop():
            self._DGI.extraProjectInit()
        
        self.init_time()

    """
    Destructor
    """

    """
    Especifica el nivel de debug de la aplicación
    @param q Número con el nimvel espeficicado
    """

    def setDebugLevel(self, q):
        Project.debugLevel = q
        #self._DGI.pnqt3ui.Options.DEBUG_LEVEL = q
    
    def init_time(self):
        self.time_ = time.time()
        
    def show_time(self, text = "", stack = False):
        now_ = time.time()
        self.logger.warning("%s Tiempo : %s", text, round(now_ - self.time_, 5), stack_info = stack)

    """
    Retorna si hay o no acls cargados
    @return Objeto acl_
    """

    def acl(self):
        return self.acl_

    """
    Especifica los datos para luego conectarse a la BD.
    @param dbname. Nombre de la BD.
    @param host. Nombre del equipo anfitrión de la BD.
    @param port. Puerto a usar para conectarse a la BD.
    @param passwd. Contraseña de la BD.
    @param driveralias. Alias del pluging a usar en la conexión
    """

    def load_db(self, dbname, host, port, user, passwd, driveralias):
        self.dbserver = DBServer()
        self.dbserver.host = host
        self.dbserver.port = port
        self.dbserver.type = driveralias
        self.dbauth = DBAuth()
        self.dbauth.username = user
        self.dbauth.password = passwd
        self.dbname = dbname

        self.actions = {}
        self.tables = {}
    
    def load(self, file_name):
        from xml.etree import ElementTree as ET
        tree = ET.parse(file_name)
        root = tree.getroot()
        
        

        for profile in root.findall("profile-data"):
            if getattr(profile.find("password"), "text", None) is not None:
                self.logger.warning("No se puede cargar un profile con contraseña por consola")

        self.dbname = root.find("database-name").text
        for db in root.findall("database-server"):
            self.dbserver = DBServer()
            self.dbserver.host = db.find("host").text
            self.dbserver.port = db.find("port").text
            self.dbserver.type = db.find("type").text
            if self.dbserver.type not in self.sql_drivers_manager.aliasList():
                self.logger.warning("Esta versión de pineboo no soporta el driver '%s'" % self.dbserver.type)
                self.database = None
                return
        for credentials in root.findall("database-credentials"):
            self.dbauth = DBAuth()
            self.dbauth.username = credentials.find("username").text
            ps = credentials.find("password").text
            if ps:
                import base64
                self.dbauth.password = base64.b64decode(ps).decode()
            else:
                self.dbauth.password = ""

    """
    Arranca el projecto. Conecta a la BD y carga los datos
    """

    def run(self):

        if not self.conn:
            from pineboolib.pnconnection import PNConnection
            self.conn = PNConnection(self.dbname, self.dbserver.host, self.dbserver.port,
                                     self.dbauth.username, self.dbauth.password, self.dbserver.type)

        if self.conn.conn is False:
            return False

        # TODO: Refactorizar esta función en otras más sencillas
        # Preparar temporal

        if self.deleteCache and os.path.exists(_dir("cache/%s" % self.conn.DBName())):
            if self._splash:
                self._splash.showMessage("Borrando caché ...", QtCore.Qt.AlignLeft, QtCore.Qt.white)
            self.logger.debug("DEVELOP: DeleteCache Activado\nBorrando %s", _dir(
                "cache/%s" % self.conn.DBName()))
            for root, dirs, files in os.walk(_dir("cache/%s" % self.conn.DBName()), topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))

        if not os.path.exists(_dir("cache")):
            os.makedirs(_dir("cache"))

        if not os.path.exists(_dir("cache/%s" % self.conn.DBName())):
            os.makedirs(_dir("cache/%s" % self.conn.DBName()))

        if not self.deleteCache:
            keep_images = FLSettings().readBoolEntry("ebcomportamiento/keep_general_cache", False)
            if keep_images is False:
                for f in os.listdir(self.tmpdir):
                    if f.find(".") > -1:
                        pt_ = os.path.join(self.tmpdir, f)
                        os.remove(pt_)
                    
                
        # Conectar:

        # Se verifica que existen estas tablas
        for table in ("flareas", "flmodules", "flfiles", "flgroups", "fllarge", "flserial", "flusers", "flvar", "flmetadata"):
            self.conn.manager().createSystemTable(table)

        util = FLUtil()
        util.writeSettingEntry(u"DBA/lastDB", self.conn.DBName())
        cursor_ = self.conn.cursor()
        self.areas = {}
        cursor_.execute(
            """ SELECT idarea, descripcion FROM flareas WHERE 1 = 1""")
        for idarea, descripcion in cursor_:
            self.areas[idarea] = Struct(idarea=idarea, descripcion=descripcion)

        self.areas["sys"] = Struct(idarea="sys", descripcion="Area de Sistema")

        # Obtener módulos activos
        cursor_.execute(""" SELECT idarea, idmodulo, descripcion, icono FROM flmodules WHERE bloqueo = %s """ %
                         self.conn.driver().formatValue("bool", "True", False))
        self.modules = {}
        for idarea, idmodulo, descripcion, icono in cursor_:
            icono = cacheXPM(icono)
            self.modules[idmodulo] = Module(idarea, idmodulo, descripcion, icono)

        file_object = open(filedir("..", "share", "pineboo", "sys.xpm"), "r")
        icono = file_object.read()
        file_object.close()
        #icono = clearXPM(icono)

        self.modules["sys"] = Module("sys", "sys", "Administración", icono)

        # Descargar proyecto . . .

        cursor_.execute(""" SELECT COUNT(idmodulo) FROM flfiles WHERE NOT sha = ''""")
        for count in cursor_:
            size_ = count[0]
        
        cursor_.execute(
            """ SELECT idmodulo, nombre, sha FROM flfiles WHERE NOT sha = '' ORDER BY idmodulo, nombre """)
        
        f1 = open(_dir("project.txt"), "w")
        self.files = {}
        if self._DGI.useDesktop() and self._DGI.localDesktop():
            tiempo_ini = time.time()
        if not os.path.exists(_dir("cache")):
            raise AssertionError
        p = 0
        pos_qs = 1
        for idmodulo, nombre, sha in cursor_:
            if not self._DGI.accept_file(nombre):
                continue
            
            p = p + 1
            if idmodulo not in self.modules:
                continue  # I
            fileobj = File(idmodulo, nombre, sha)
            if nombre in self.files:
                self.logger.warning("run: file %s already loaded, overwritting..." % nombre)
            self.files[nombre] = fileobj
            self.modules[idmodulo].add_project_file(fileobj)
            f1.write(fileobj.filekey + "\n")

            fileobjdir = os.path.dirname(_dir("cache", fileobj.filekey))
            if not os.path.exists(fileobjdir):
                os.makedirs(fileobjdir)
            
            if os.path.exists(_dir("cache", fileobj.filekey)):
                if _dir("cache", fileobj.filekey).endswith(".qs"):
                    if os.path.exists("%s.py" % _dir("cache", fileobj.filekey)):
                        continue
                    
                elif _dir("cache", fileobj.filekey).endswith(".mtd"):
                    if os.path.exists("%s_model.py" % _dir("cache", fileobj.filekey[:-4])):
                        continue
                else:
                    continue

            cur2 = self.conn.cursor()
            sql = "SELECT contenido FROM flfiles WHERE idmodulo = %s AND nombre = %s AND sha = %s" % (self.conn.driver().formatValue(
                "string", idmodulo, False), self.conn.driver().formatValue("string", nombre, False), self.conn.driver().formatValue("string", sha, False))
            cur2.execute(sql)
            qs_count = 0
            for (contenido,) in cur2:

                encode_ = "ISO-8859-15"
                if str(nombre).endswith(".kut") or str(nombre).endswith(".ts"):
                    encode_ = "utf-8"

                settings = FLSettings()
                
                
                    
                
                
                
                
                    
                folder = _dir("cache", "/".join(fileobj.filekey.split("/")[:len(fileobj.filekey.split("/")) -1]))
                if os.path.exists(folder):
                    for root, dirs, files in os.walk(folder):
                        for f in files:
                            os.remove(os.path.join(root, f))
                    

                if settings.readBoolEntry("application/isDebuggerMode", False):
                    if self._splash:
                        self._splash.showMessage("Volcando a caché %s..." %
                                                     nombre, QtCore.Qt.AlignLeft, QtCore.Qt.white)

                    
                    
                if contenido:
                    f2 = open(_dir("cache", fileobj.filekey), "wb")
                    txt = contenido.encode(encode_, "replace")
                    f2.write(txt)
                    f2.close()
            
            if nombre.endswith(".mtd"):
                mtd_parse(fileobj)
            
            

            if self.parseProject and nombre.endswith(".qs") and settings.readBoolEntry("application/isDebuggerMode", False):
                # if self._splash:
                #    self._splash.showMessage("Convirtiendo %s ( %d/ ??) ..." %
                #                             (nombre, pos_qs), QtCore.Qt.AlignLeft, QtCore.Qt.white)
                self.parseScript(_dir("cache", fileobj.filekey), "(%d de %d)" % (p, size_))

                pos_qs += 1

        if self._DGI.useDesktop() and self._DGI.localDesktop():
            tiempo_fin = time.time()
            self.logger.info("Descarga del proyecto completo a disco duro: %.3fs", (tiempo_fin - tiempo_ini))

        # Cargar el núcleo común del proyecto
        idmodulo = 'sys'
        for root, dirs, files in os.walk(filedir("..", "share", "pineboo")):
            for nombre in files:
                if root.find("modulos") == -1:
                    fileobj = File(idmodulo, nombre, basedir=root)
                    self.files[nombre] = fileobj
                    self.modules[idmodulo].add_project_file(fileobj)
                    if self.parseProject and nombre.endswith(".qs"):
                        self.parseScript(_dir(root, nombre))
        
        
        
        
        if self._splash:
            self._splash.showMessage("Cargando objetos ...", QtCore.Qt.AlignLeft, QtCore.Qt.white)
            self._DGI.processEvents()
        
        from pineboolib.pncontrolsfactory import load_models
        load_models()
        
        
        if self._splash:
            self._splash.showMessage("Cargando traducciones ...", QtCore.Qt.AlignLeft, QtCore.Qt.white)
            self._DGI.processEvents()

       
        from pineboolib.pncontrolsfactory import aqApp
        
        aqApp.loadTranslations()
        from pineboolib.fllegacy.flaccesscontrollists import FLAccessControlLists
        self.acl_ = FLAccessControlLists()
        self.acl_.init_()
        
        return True

    """
    LLama a una función del projecto.
    @param function. Nombre de la función a llamar.
    @param aList. Array con los argumentos.
    @param objectContext. Contexto en el que se ejecuta la función.
    @param showException. Boolean que especifica si se muestra los errores.
    @return Boolean con el resultado.
    """

    def call(self, function, aList, object_context=None, showException=True):
        # FIXME: No deberíamos usar este método. En Python hay formas mejores
        # de hacer esto.
        self.logger.trace("JS.CALL: fn:%s args:%s ctx:%s",
                          function, aList, object_context, stack_info=True)
        
        if function is not None:
        # Tipicamente flfactalma.iface.beforeCommit_articulos()
            if function[-2:] == "()":
                function = function[:-2]

            aFunction = function.split(".")
        else:
            aFunction = []

        if not object_context:
            if not aFunction[0] in self.actions:
                if len(aFunction) > 1:
                    if showException:
                        self.logger.error("No existe la acción %s en el módulo %s", aFunction[1], aFunction[0])
                else:
                    if showException:
                        self.logger.error("No existe la acción %s", aFunction[0])
                return False

            funAction = self.actions[aFunction[0]]
            if aFunction[1] == "iface" or len(aFunction) == 2:
                mW = funAction.load()
                if len(aFunction) == 2:
                    object_context = None
                    if hasattr(mW.widget, aFunction[1]):
                        object_context = mW.widget
                    if hasattr(mW.iface, aFunction[1]):
                        object_context = mW.iface

                    if not object_context:
                        object_context = mW

                else:
                    object_context = mW.iface

            elif aFunction[1] == "widget":
                fR = None
                funAction.load_script(aFunction[0], fR)
                object_context = fR.iface
            else:
                return False

            if not object_context:
                if showException:
                    self.logger.error(
                        "No existe el script para la acción %s en el módulo %s", aFunction[0], aFunction[0])
                return False

        fn = None
        if len(aFunction) == 1:  # Si no hay puntos en la llamada a functión
            function_name = aFunction[0]

        elif len(aFunction) > 2:  # si existe self.iface por ejemplo
            function_name = aFunction[2]
        elif len(aFunction) == 2:
            function_name = aFunction[1]  # si no exite self.iiface
        else:
            if len(aFunction) == 0:
                fn = object_context

        if not fn:
            fn = getattr(object_context, function_name, None)

        if fn is None:
            if showException:
                self.logger.error(
                    "No existe la función %s en %s", function_name, aFunction[0])
            return True  # FIXME: Esto devuelve true? debería ser false, pero igual se usa por el motor para detectar propiedades

        
        try:
            return fn(*aList)
        except Exception:
            from pineboolib.pncontrolsfactory import wiki_error
            msg_w = wiki_error(traceback.format_exc())
            if pineboolib.project._DGI.localDesktop():
                from pineboolib.pncontrolsfactory import aqApp
                aqApp.msgBoxWarning(msg_w ,pineboolib.project._DGI)
            else:
                self.logger.warning(msg_w)
                
        #try:
        #    if aList:
        #        return fn(*aList)
        #    else:
        #        return fn()
        #except Exception:
        #    if showException:
        #        self.logger.exception("js.call: error al llamar %s de %s", function, object_context)

        return None
    
        
    
    
    """
    Convierte un script .qs a .py lo deja al lado
    @param scriptname, Nombre del script a convertir
    """

    def parseScript(self, scriptname, txt_=""):

        # Intentar convertirlo a Python primero con flscriptparser2
        if not os.path.isfile(scriptname):
            raise IOError
        python_script_path = (
            scriptname + ".xml.py").replace(".qs.xml.py", ".qs.py")
        if not os.path.isfile(python_script_path) or pineboolib.no_python_cache:
            settings = FLSettings()
            debug_postparse = False
            if settings.readBoolEntry("application/isDebuggerMode", False):
                util = FLUtil()
                file_name = scriptname.split("\\") if util.getOS() == "WIN32" else scriptname.split("/")

                file_name = file_name[len(file_name) - 2]

                msg = "Convirtiendo a Python . . . %s.qs %s" % (file_name, txt_)
                if settings.readBoolEntry("ebcomportamiento/SLConsola", False):
                    debug_postparse = True
                    self.logger.warning(msg)

                if self._splash:
                    self._splash.showMessage(msg, QtCore.Qt.AlignLeft, QtCore.Qt.white)

                else:
                    if settings.readBoolEntry("ebcomportamiento/SLInterface", False):
                        from pineboolib.pncontrolsfactory import aqApp
                        aqApp.popupWarn(msg)
            
            clean_no_python = self._DGI.clean_no_python()
            
            from pineboolib.flparser import postparse
            try:
                postparse.pythonify(scriptname, debug_postparse, clean_no_python)
            except Exception as e:
                self.logger.warning("El fichero %s no se ha podido convertir: %s", scriptname, e)

    """
    Lanza los test
    @param name, Nombre del test específico. Si no se especifica se lanzan todos los tests disponibles
    @return Texto con la valoración de los test aplicados
    """

    def test(self, name=None):
        from importlib import import_module
        dirlist = os.listdir(filedir("../pineboolib/plugins/test"))
        testDict = {}
        for f in dirlist:
            if not f[0:2] == "__":
                f = f[:f.find(".py")]
                mod_ = import_module(
                    "pineboolib.plugins.test.%s" % f)
                test_ = getattr(mod_, f)
                testDict[f] = test_

        maxValue = 0
        value = 0
        result = None
        resultValue = 0
        if name:
            try:
                t = testDict[name]()
                maxValue = t.maxValue()
                value = t.run()
            except Exception:
                result = False
        else:

            for test in testDict.keys():
                print("test", test)
                t = testDict[test]()
                maxValue = maxValue + t.maxValue
                v = t.run()
                print("result", test, v, "/", t.maxValue)
                value = value + v

        if result is None and maxValue > 0:
            resultValue = value

        result = "%s/%s" % (resultValue, maxValue)

        return result

    """
    Retorna la carpeta temporal predefinida de pineboo
    @return ruta a la carpeta temporal
    """

    def get_temp_dir(self):
        return self.tmpdir


"""
Esta clase almacena la información de los módulos cargados
"""


class Module(object):
    """
    Constructor
    @param areaid. Identificador de area.
    @param name. Nombre del módulo
    @param description. Descripción del módulo
    @param icon. Icono del módulo
    """

    def __init__(self, areaid, name, description, icon):
        self.areaid = areaid
        self.name = name
        self.description = description  # En python2 era .decode(UTF-8)
        self.icon = icon
        self.files = {}
        self.tables = {}
        self.loaded = False
        self.path = pineboolib.project.path
        self.logger = logging.getLogger("main.Module")

    """
    Añade ficheros al array que controla que ficehros tengo.
    @param fileobj. Objeto File con información del fichero
    """

    def add_project_file(self, fileobj):
        self.files[fileobj.filename] = fileobj

    """
    Carga las acciones pertenecientes a este módulo
    @return Boolean. True si ok, False si hay problemas
    """

    def load(self):
        pathxml = _path("%s.xml" % self.name)
        #pathui = _path("%s.ui" % self.name)
        if pathxml is None:
            self.logger.error("módulo %s: fichero XML no existe", self.name)
            return False
        #if pathui is None:
        #    self.logger.error("módulo %s: fichero UI no existe", self.name)
        #    return False
        if pineboolib.project._DGI.useDesktop() and pineboolib.project._DGI.localDesktop():
            tiempo_1 = time.time()
        try:
            self.actions = ModuleActions(self, pathxml, self.name)
            self.actions.load()
        except Exception as e:
            self.logger.exception("Al cargar módulo %s:", self.name)
            return False

        # TODO: Load Main Script:
        self.mainscript = None
        # /-----------------------
        if pineboolib.project._DGI.useDesktop() and pineboolib.project._DGI.localDesktop():
            tiempo_2 = time.time()

        for tablefile in self.files:
            if not tablefile.endswith(".mtd"):
                continue
            name, ext = os.path.splitext(tablefile)
            try:
                contenido = str(open(_path(tablefile),
                                     "rb").read(), "ISO-8859-15")
            except UnicodeDecodeError as e:
                self.logger.error(
                    "Error al leer el fichero %s %s", tablefile, e)
                continue
            tableObj = parseTable(name, contenido)
            if tableObj is None:
                self.logger.warning(
                    "No se pudo procesar. Se ignora tabla %s/%s ", self.name, name)
                continue
            self.tables[name] = tableObj
            pineboolib.project.tables[name] = tableObj

        if pineboolib.project._DGI.useDesktop() and pineboolib.project._DGI.localDesktop():
            tiempo_3 = time.time()
            if tiempo_3 - tiempo_1 > 0.2:
                self.logger.debug("Carga del módulo %s : %.3fs ,  %.3fs",
                                  self.name, tiempo_2 - tiempo_1, tiempo_3 - tiempo_2)

        self.loaded = True
        return True


"""
Clase que gestiona cada uno de los ficheros de un módulo
"""


class File(object):
    """
    Constructor
    @param module. Identificador del módulo propietario
    @param filename. Nombre del fichero
    @param sha. Código sha1 del contenido del fichero
    @param basedir. Ruta al fichero en cache
    """

    def __init__(self, module, filename, sha=None, basedir=None):
        self.module = module
        self.filename = filename
        self.sha = sha
        if filename.endswith(".qs.py"):
            self.ext = ".qs.py"
            self.name = os.path.splitext(os.path.splitext(filename)[0])[0]
        else:
            self.name, self.ext = os.path.splitext(filename)

        db_name = pineboolib.project.conn.DBName()

        if self.sha:
            self.filekey = "%s/%s/file%s/%s/%s%s" % (
                db_name, module, self.ext, self.name, sha, self.ext)
        else:
            self.filekey = filename
        self.basedir = basedir

    """
    Devuelve la ruta absoluta del fichero
    @return Ruta absoluta del fichero
    """

    def path(self):
        if self.basedir:
            # Probablemente porque es local . . .
            return _dir(self.basedir, self.filename)
        else:
            # Probablemente es remoto (DB) y es una caché . . .
            return _dir("cache", *(self.filekey.split("/")))


"""
Clase encargada de gestionar los diferentes módulos de inteligencia lógica del projecto
"""


class DelayedObjectProxyLoader(object):

    """
    Constructor
    """

    def __init__(self, obj, *args, **kwargs):
        self._name = "unnamed-loader"
        if "name" in kwargs:
            self._name = kwargs["name"]
            del kwargs["name"]
        self._obj = obj
        self._args = args
        self._kwargs = kwargs
        self.loaded_obj = None
        self.logger = logging.getLogger("main.DelayedObjectProxyLoader")

    """
    Carga un objeto nuevo
    @return objeto nuevo o si ya existe , cacheado
    """

    def __load(self):
        self.logger.debug(
            "DelayedObjectProxyLoader: loading %s %s( *%s **%s)",
            self._name, self._obj, self._args, self._kwargs)
        
        self.loaded_obj = self._obj(*self._args, **self._kwargs)
        return self.loaded_obj

    """
    Retorna una función buscada
    @param name. Nombre del la función buscada
    @return el objecto del XMLAction afectado
    """

    def __getattr__(self, name):  # Solo se lanza si no existe la propiedad.
        obj_ = self.__load()
        return getattr(obj_, name, getattr(obj_.widget, name, None)) if obj_ else None


"""
Genera un arbol con las acciones de los diferentes módulos
@param name. Nombre del la función buscada
@return el objecto del XMLAction afectado
"""


class ModuleActions(object):
    """
    Constructor
    @param module. Identificador del módulo
    @param path. Ruta del módulo
    @param modulename. Nombre del módulo
    """

    def __init__(self, module, path, modulename):
        self.mod = module
        self.path = path
        self.module_name = modulename
        self.logger = logging.getLogger("main.ModuleActions")
        if not self.path:
            self.logger.error(
                "El módulo no tiene un path válido %s", self.module_name)

    """
    Carga las actions del módulo en el projecto
    """

    def load(self):
        # Ojo: Almacena un arbol con los módulos cargados
        from pineboolib import qsa as qsa_dict_modules
        
        self.tree = pineboolib.utils.load2xml(self.path)
        self.root = self.tree.getroot()

        action = XMLAction()
        action.mod = self
        action.name = self.mod.name
        action.alias = self.mod.name
        # action.form = self.mod.name
        action.form = None
        action.table = None
        action.scriptform = self.mod.name
        pineboolib.project.actions[action.name] = action
        if hasattr(qsa_dict_modules, action.name):
            if action.name is not "sys":
                self.logger.warning("No se sobreescribe variable de entorno %s", action.name)
        else:  # Se crea la action del módulo
            setattr(qsa_dict_modules, action.name, DelayedObjectProxyLoader(
                action.load, name="QSA.Module.%s" % action.name))

        for xmlaction in self.root:
            action_xml = XMLAction(xmlaction)
            action_xml.mod = self
            name = action_xml.name
            if name != "unnamed":
                if hasattr(qsa_dict_modules, "form%s" % name):
                    self.logger.warning("No se sobreescribe variable de entorno %s. Hay una definición previa en %s", "%s.form%s" %(self.module_name, name), pineboolib.project.actions[name].mod.module_name)
                else:  # Se crea la action del form
                    pineboolib.project.actions[name] = action_xml
                    delayed_action = DelayedObjectProxyLoader(
                        action_xml.load,
                        name="QSA.Module.%s.Action.form%s" % (self.mod.name, name))
                    setattr(qsa_dict_modules, "form" + name, delayed_action)

                if hasattr(qsa_dict_modules, "formRecord" + name):
                    self.logger.debug(
                        "No se sobreescribe variable de entorno %s", "formRecord" + name)
                else:  # Se crea la action del formRecord
                    delayed_action = DelayedObjectProxyLoader(
                        action_xml.formRecordWidget,
                        name="QSA.Module.%s.Action.formRecord%s" % (self.mod.name, name))

                    setattr(qsa_dict_modules, "formRecord" + name, delayed_action)

    """
    Busca si es propietario de una action
    """

    def __contains__(self, k):
        return k in pineboolib.project.actions

    """
    Recoge una action determinada
    @param name. Nombre de la action
    @return Retorna el XMLAction de la action dada
    """

    def __getitem__(self, name):
        return pineboolib.project.actions[name]

    """
    Añade una action a propiedad del módulo
    @param name. Nombre de la action
    @param action_. Action a añadir a la propiedad del módulo
    """

    def __setitem__(self, name, action_):
        raise NotImplementedError("Actions are not writable!")
        #pineboolib.project.actions[name] = action_


"""
Contiene Información de cada action del mainForm
"""


class XMLMainFormAction(XMLStruct):
    name = "unnamed"
    text = ""
    mainform = None
    mod = None
    prj = None
    slot = None
    logger = logging.getLogger("main.XMLMainFormAction")

    """
    Lanza la action
    """

    def run(self):
        self.logger.debug("Running: %s %s %s", self.name, self.text, self.slot)
        try:
            action = self.mod.actions[self.name]
            getattr(action, self.slot, "unknownSlot")()
        finally:
            self.logger.debug(
                "END of Running: %s %s %s",
                self.name, self.text, self.slot)


"""
Contiene información de las actions especificadas en el .xml del módulo
"""


class XMLAction(XMLStruct):
    logger = logging.getLogger("main.XMLAction")

    """
    Constructor
    """

    def __init__(self, *args, **kwargs):
        super(XMLAction, self).__init__(*args, **kwargs)
        self.form = self._v("form")
        self.name = self._v("name")
        self.script = self._v("script")  # script_form_record
        self.table = self._v("table")
        self.mainform = self._v("mainform")
        self.mainscript = self._v("mainscript")  # script_form
        self.formrecord = self._v("formrecord")  # form_record
        self.mainform_widget = None
        self.formrecord_widget = None
        self._loaded = False

    """
    Carga FLFormRecordDB por defecto
    @param cursor. Asigna un cursor al FLFormRecord
    @return widget con form inicializado
    """

    def loadRecord(self, cursor):
        self._loaded = getattr(self.formrecord_widget, "_loaded", False)
        if not self._loaded:
            if getattr(self.formrecord_widget, "widget", None):
                self.formrecord_widget.widget.doCleanUp()
                #self.formrecord_widget.widget = None
                
                
            self.logger.debug("Loading record action %s . . . ", self.name)
            if pineboolib.project._DGI.useDesktop():
                self.formrecord_widget = pineboolib.project.conn.managerModules().createFormRecord(self, None, cursor, None)
            else:
                #self.script = getattr(self, "script", None)
                #if isinstance(self.script, str) or self.script is None:
                self.load_script(self.scriptformrecord, None)
                self.formrecord_widget = self.script.form
                self.formrecord_widget.widget = self.formrecord_widget
                self.formrecord_widget.iface = self.formrecord_widget.widget.iface
                self.formrecord_widget._loaded = True
            # self.formrecord_widget.setWindowModality(Qt.ApplicationModal)
            if self.formrecord_widget:
                self.logger.debug("End of record action load %s (iface:%s ; widget:%s)", self.name, getattr(
                    self.formrecord_widget, "iface", None), getattr(self.formrecord_widget, "widget", None))
        
        if cursor and self.formrecord_widget:
            self.formrecord_widget.setCursor(cursor)
        

        return self.formrecord_widget

    def load(self):
        self._loaded = getattr(self.mainform_widget, "_loaded", False)
        if not self._loaded:
            if getattr(self.mainform_widget, "widget", None):
                self.mainform_widget.widget.doCleanUp()
            self.logger.debug("Loading action %s . . . ", self.name)
            if pineboolib.project._DGI.useDesktop():
                self.mainform_widget = pineboolib.project.conn.managerModules().createForm(
                    self, None, pineboolib.project.main_window.w_, None)
            else:
                self.scriptform = getattr(self, "scriptform", None)
                self.load_script(self.scriptform, None)
                self.mainform_widget = self.script.form
                self.mainform_widget.widget = self.mainform_widget
                self.mainform_widget.iface = self.mainform_widget.widget.iface
                self.mainform_widget._loaded = True

            self.logger.debug("End of action load %s (iface:%s ; widget:%s)", self.name, getattr(
                self.mainform_widget, "iface", None), getattr(self.mainform_widget, "widget", None))

        return self.mainform_widget

    """
    Llama a la función main de una action
    """

    def execMainScript(self, name):
        a = pineboolib.project.conn.manager().action(name)
        if not a:
            self.logger.warning("No existe la acción %s", name)
            return True
        pineboolib.project.call("%s.main" % a.name(), [], None, False)

    """
    Retorna el widget del formRecord. Esto es necesario porque a veces no hay un FLformRecordDB inicialidado todavía
    @return wigdet del formRecord.
    """

    def formRecordWidget(self):
        if not getattr(self.formrecord_widget, "_loaded", None):
            self.loadRecord(None)

        return self.formrecord_widget

    """
    Abre el FLFormRecordDB por defecto
    @param cursor. Cursor a usar por el FLFormRecordDB
    """

    def openDefaultFormRecord(self, cursor):
        self.logger.info("Opening default formRecord for Action %s", self.name)
        w = self.loadRecord(cursor)
        # w.init()
        if w:
            if pineboolib.project._DGI.localDesktop():
                w.show()
    
    def openDefaultForm(self):
        self.logger.info("Opening default form for Action %s", self.name)
        w = self.load()
        
        if w:
            if pineboolib.project._DGI.localDesktop():
                w.show()

    """
    Ejecuta el script por defecto
    """

    def execDefaultScript(self):
        self.logger.info("Executing default script for Action %s", self.name)
        self.scriptform = getattr(self, "scriptform", None)
        self.load_script(self.scriptform, None)

        self.mainform_widget = self.script.form
        if self.mainform_widget.iface:
            self.mainform_widget.iface.main()
        else:
            self.mainform_widget.main()

    """
    Convierte un script qsa en .py y lo carga
    @param scriptname. Nombre del script a convertir
    @param parent. Objecto al que carga el script, si no se especifica es a self.script
    """

    def load_script(self, scriptname, parent=None):
        from importlib import machinery
        if scriptname:
            scriptname = scriptname.replace(".qs", "")
        #if scriptname:
        #    self.logger.info("Cargando script %s de %s accion %s", scriptname, parent, self.name)

        parent_ = parent
        if parent is None:
            parent = self
            action_ = self
        else:
            action_ = parent._action if hasattr(parent, "_action") else self

            # import aqui para evitar dependencia ciclica
        from pineboolib.utils import convertFLAction
        if not isinstance(action_, XMLAction):
            action_ = convertFLAction(action_)

        python_script_path = None
        # primero default, luego sobreescribimos
        from pineboolib import emptyscript
        parent.script = emptyscript

        if scriptname is None:
            parent.script.form = parent.script.FormInternalObj(action=action_, project=pineboolib.project, parent=parent)
            parent.widget = parent.script.form
            parent.iface = parent.widget.iface
            return
        
        script_path_py = pineboolib.project._DGI.alternative_script_path("%s.py" % scriptname)
        
        if script_path_py is None:
            script_path_qs = _path("%s.qs" % scriptname, False)        
            script_path_py = coalesce_path("%s.py" % scriptname, "%s.qs.py" % scriptname, None)
        
        mng_modules = pineboolib.project.conn.managerModules()
        if mng_modules.staticBdInfo_ and mng_modules.staticBdInfo_.enabled_:
            from pineboolib.fllegacy.flmodulesstaticloader import FLStaticLoader
            ret_py = FLStaticLoader.content("%s.qs.py" % scriptname, mng_modules.staticBdInfo_, True)  # Con True solo devuelve el path
            if ret_py:
                script_path_py = ret_py
            else:
                ret_qs = FLStaticLoader.content("%s.qs" % scriptname, mng_modules.staticBdInfo_, True)  # Con True solo devuelve el path
                if ret_qs:
                    script_path_qs = ret_qs
        
        if script_path_py is not None:
            script_path = script_path_py
            self.logger.info("Loading script PY %s . . . ", scriptname)
            if not os.path.isfile(script_path):
                raise IOError
            try:
                self.logger.info(
                    "Cargando %s : %s ", scriptname,
                    script_path.replace(pineboolib.project.tmpdir, "tempdata"))
                parent.script = machinery.SourceFileLoader(
                    scriptname, script_path).load_module()
            except Exception as e:
                self.logger.exception(
                    "ERROR al cargar script PY para la accion %s:", action_.name)

        elif script_path_qs:
            script_path = script_path_qs
            pineboolib.project.parseScript(script_path)
            self.logger.info("Loading script QS %s . . . ", scriptname)
            python_script_path = (
                script_path + ".xml.py").replace(".qs.xml.py", ".qs.py")
            try:
                self.logger.info(
                    "Cargando %s : %s ", scriptname,
                    python_script_path.replace(pineboolib.project.tmpdir, "tempdata"))
                parent.script = machinery.SourceFileLoader(
                    scriptname, python_script_path).load_module()
            except Exception as e:
                self.logger.exception(
                    "ERROR al cargar script QS para la accion %s:", action_.name)
        
        parent.script.form = parent.script.FormInternalObj(action_, pineboolib.project, parent_)
        if parent_:
            parent.widget = parent.script.form
            if getattr(parent.widget, "iface", None):
                parent.iface = parent.widget.iface

        return

    def unknownSlot(self):
        self.logger.error("Executing unknown script for Action %s", self.name)
