# -*- coding: utf-8 -*-
import time
import os
import logging
import traceback
from lxml import etree
from binascii import unhexlify

import zlib
import importlib


from PyQt5 import QtCore, QtGui
from pineboolib.fllegacy.FLSettings import FLSettings
from pineboolib.fllegacy.FLTranslator import FLTranslator
from pineboolib.fllegacy.FLAccessControlLists import FLAccessControlLists
from pineboolib.fllegacy.FLFormDB import FLFormDB
from pineboolib import qt3ui
from pineboolib.PNConnection import PNConnection
from pineboolib.dbschema.schemaupdater import parseTable
from pineboolib.fllegacy.FLUtil import FLUtil
from pineboolib.fllegacy.FLFormRecordDB import FLFormRecordDB
from PyQt5.Qt import qWarning, qApp

import pineboolib.emptyscript
from pineboolib import decorators


from pineboolib.utils import filedir, one, Struct, XMLStruct
Qt = QtCore.Qt


class DBServer(XMLStruct):
    host = "127.0.0.1"
    port = "5432"


class DBAuth(XMLStruct):
    username = "postgres"
    password = "passwd"


class Project(object):
    logger = logging.getLogger("main.Project")
    conn = None  # Almacena la conexión principal a la base de datos
    debugLevel = 100
    mainFormName = "Pineboo"
    version = "0.3"
    _initModules = None
    main_window = None
    translators = None
    multiLangEnabled_ = False
    multiLangId_ = QtCore.QLocale().name()[:2].upper()
    translator_ = None
    acl_ = None
    _DGI = None

    def __init__(self, DGI):
        self._DGI = DGI
        self.tree = None
        self.root = None
        self.dbserver = None
        self.dbauth = None
        self.dbname = None
        self.apppath = None
        self.tmpdir = None
        self.parser = None
        self._initModules = []
        if self._DGI.useDesktop():
            if self._DGI.localDesktop():
                self.main_window = importlib.import_module("pineboolib.plugins.mainForm.%s.%s" % (
                    self.mainFormName, self.mainFormName)).mainWindow
            else:
                self.main_window = self._DGI.mainForm().mainWindow
        self.deleteCache = False
        self.parseProject = False

        self.translator_ = []
        self.actions = {}
        self.tables = {}
        self.files = {}
        self.cur = None
        if not self._DGI.localDesktop():
            self._DGI.extraProjectInit()

    def __del__(self):
        self.writeState()

    def setDebugLevel(self, q):
        Project.debugLevel = q
        decorators.Options.DEBUG_LEVEL = q
        qt3ui.Options.DEBUG_LEVEL = q

    """
    Para especificar si usa fllarge unificado o multiple (Eneboo/Abanq)
    """

    def singleFLLarge(self):
        return True

    """
    Retorna si hay o no acls cargados
    """

    def acl(self):
        return self.acl_

    def consoleShown(self):
        return True

    def load_db(self, dbname, host, port, user, passwd, driveralias):
        self.dbserver = DBServer()
        self.dbserver.host = host
        self.dbserver.port = port
        self.dbserver.type = driveralias
        self.dbauth = DBAuth()
        self.dbauth.username = user
        self.dbauth.password = passwd
        self.dbname = dbname
        self.apppath = filedir("..")
        self.tmpdir = filedir("../tempdata")

        self.actions = {}
        self.tables = {}
        pineboolib.project = self

    def load(self, filename):
        self.parser = etree.XMLParser(
            ns_clean=True,
            encoding="UTF-8",
            remove_blank_text=True,
        )
        self.tree = etree.parse(filename, self.parser)
        self.root = self.tree.getroot()
        self.dbserver = DBServer(one(self.root.xpath("database-server")))
        self.dbauth = DBAuth(one(self.root.xpath("database-credentials")))
        self.dbname = one(self.root.xpath("database-name/text()"))
        self.apppath = one(self.root.xpath("application-path/text()"))
        self.tmpdir = filedir("../tempdata")
        if not getattr(self.dbserver, "host", None):
            self.dbserver.host = None

        if not getattr(self.dbserver, "port", None):
            self.dbserver.port = None

        if not getattr(self.dbserver, "type", None):
            self.dbserver.type = None

        if not self.dbauth:
            self.dbauth.username = None
            self.dbauth.password = None

        self.actions = {}
        self.tables = {}
        pineboolib.project = self

    def path(self, filename):
        if filename not in self.files:
            print("WARN: Fichero %r no encontrado en el proyecto." % filename)
            return None
        return self.files[filename].path()

    def dir(self, *x):
        return os.path.join(self.tmpdir, *x)

    def run(self):
        # TODO: Refactorizar esta función en otras más sencillas
        # Preparar temporal
        if self.deleteCache and not not os.path.exists(self.dir("cache/%s" % self.dbname)):
            print("DEVELOP: DeleteCache Activado\nBorrando %s" %
                  self.dir("cache/%s" % self.dbname))
            for root, dirs, files in os.walk(self.dir("cache/%s" % self.dbname), topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            # borrando de share
            for root, dirs, files in os.walk(self.dir("../share/pineboo"), topdown=False):
                for name in files:
                    if name.endswith("qs.py") or name.endswith("qs.py.debug") or name.endswith("qs.xml"):
                        os.remove(os.path.join(root, name))

        if not os.path.exists(self.dir("cache")):
            os.makedirs(self.dir("cache"))

        # Conectar:

        self.conn = PNConnection(self.dbname, self.dbserver.host, self.dbserver.port,
                                 self.dbauth.username, self.dbauth.password, self.dbserver.type)
        if self.conn.conn is False:
            return False

        # Se verifica que existen estas tablas
        for table in ("flareas", "flmodules", "flfiles", "flgroups", "fllarge", "flserial", "flusers", "flvar"):
            self.conn.manager().createSystemTable(table)

        util = FLUtil()
        util.writeSettingEntry(u"DBA/lastDB", self.dbname)
        self.cur = self.conn.cursor()
        self.areas = {}
        self.cur.execute(
            """ SELECT idarea, descripcion FROM flareas WHERE 1 = 1""")
        for idarea, descripcion in self.cur:
            self.areas[idarea] = Struct(idarea=idarea, descripcion=descripcion)

        # Obtener modulos activos
        self.cur.execute(""" SELECT idarea, idmodulo, descripcion, icono FROM flmodules WHERE bloqueo = %s """ %
                         self.conn.driver().formatValue("bool", "True", False))
        self.modules = {}
        for idarea, idmodulo, descripcion, icono in self.cur:
            self.modules[idmodulo] = Module(
                self, idarea, idmodulo, descripcion, icono)
        # Añadimos módulo sistema(falta icono)
        self.modules["sys"] = Module(
            self, "sys", "sys", "Administración", None)

        # Descargar proyecto . . .

        self.cur.execute(
            """ SELECT idmodulo, nombre, sha FROM flfiles ORDER BY idmodulo, nombre """)
        size_ = len(self.cur.fetchall())
        self.cur.execute(
            """ SELECT idmodulo, nombre, sha FROM flfiles ORDER BY idmodulo, nombre """)
        f1 = open(self.dir("project.txt"), "w")
        self.files = {}
        if self._DGI.useDesktop() and self._DGI.localDesktop():
            tiempo_ini = time.time()
        if not os.path.exists(self.dir("cache")):
            raise AssertionError
        # if self.parseProject:
        if self._DGI.useDesktop() and self._DGI.localDesktop():
            util.createProgressDialog("Pineboo", size_)
        p = 0
        for idmodulo, nombre, sha in self.cur:
            if self._DGI.useDesktop() and self._DGI.localDesktop():
                util.setProgress((p * 100) / size_)
                util.setLabelText("Convirtiendo %s." % nombre)
            if idmodulo not in self.modules:
                continue  # I
            fileobj = File(self, idmodulo, nombre, sha)
            if nombre in self.files:
                print("WARN: file %s already loaded, overwritting..." % nombre)
            self.files[nombre] = fileobj
            self.modules[idmodulo].add_project_file(fileobj)
            f1.write(fileobj.filekey + "\n")
            if os.path.exists(self.dir("cache", fileobj.filekey)):
                continue
            fileobjdir = os.path.dirname(self.dir("cache", fileobj.filekey))
            if not os.path.exists(fileobjdir):
                os.makedirs(fileobjdir)

            cur2 = self.conn.cursor()
            sql = "SELECT contenido FROM flfiles WHERE idmodulo = %s AND nombre = %s AND sha = %s" % (self.conn.driver().formatValue(
                "string", idmodulo, False), self.conn.driver().formatValue("string", nombre, False), self.conn.driver().formatValue("string", sha, False))
            cur2.execute(sql)
            for (contenido,) in cur2:
                f2 = open(self.dir("cache", fileobj.filekey), "wb")
                # La cadena decode->encode corrige el bug de guardado de AbanQ/Eneboo
                txt = ""
                try:
                    # txt = contenido.decode("UTF-8").encode("ISO-8859-15")
                    txt = contenido.encode("ISO-8859-15")
                except Exception:
                    print("Error al decodificar", idmodulo, nombre)
                    # txt = contenido.decode("UTF-8","replace").encode("ISO-8859-15","replace")
                    txt = contenido.encode("ISO-8859-15", "replace")

                f2.write(txt)

            if self.parseProject and nombre.endswith(".qs"):
                self.parseScript(self.dir("cache", fileobj.filekey))

            p = p + 1
        if self._DGI.useDesktop() and self._DGI.localDesktop():
            tiempo_fin = time.time()

            if Project.debugLevel > 50:
                print("Descarga del proyecto completo a disco duro: %.3fs" %
                      (tiempo_fin - tiempo_ini))

        # Cargar el núcleo común del proyecto
        idmodulo = 'sys'
        for root, dirs, files in os.walk(filedir("..", "share", "pineboo")):
            for nombre in files:
                if root.find("modulos") == -1:
                    fileobj = File(self, idmodulo, nombre, basedir=root)
                    self.files[nombre] = fileobj
                    self.modules[idmodulo].add_project_file(fileobj)
                    if self.parseProject and nombre.endswith(".qs"):
                        self.parseScript(self.dir(root, nombre))

        if self._DGI.useDesktop() and self._DGI.localDesktop():
            try:
                util.destroyProgressDialog()
            except Exception as e:
                self.logger.error(e)

            self.loadTranslations()
            self.readState()
        self.acl_ = FLAccessControlLists()
        self.acl_.init_()

    def saveGeometryForm(self, name, geo):
        name = "geo/%s" % name
        FLSettings().writeEntry(name, geo)

    def loadGeometryForm(self, name):
        name = "geo/%s" % name
        return FLSettings().readEntry(name, None)

    @decorators.NotImplementedWarn
    def readState(self):
        pass

    @decorators.NotImplementedWarn
    def writeState(self):
        pass

    def call(self, function, aList, objectContext, showException=True):
        # FIXME: No deberíamos usar este método. En Python hay formas mejores de hacer esto.
        if Project.debugLevel > 50:
            print("*** JS.CALL :: function:%r   argument.list:%r    context:%r ***" %
                  (function, aList, objectContext))

        # Tipicamente flfactalma.iface.beforeCommit_articulos()
        if function[-2:] == "()":
            function = function[:-2]

        aFunction = function.split(".")
        if not aFunction[0] in self.modules:
            if Project.debugLevel > 50:
                print("No existe el módulo %s" % (aFunction[0]))
            return False

        funModule = self.modules[aFunction[0]]

        if not aFunction[0] in funModule.actions:
            if Project.debugLevel > 50:
                print("No existe la acción %s en el módulo %s" %
                      (aFunction[0], aFunction[0]))
            return False

        funAction = funModule.actions[aFunction[0]]

        if aFunction[1] == "iface":
            mW = funAction.load()
            funScript = mW.iface
        elif aFunction[1] == "widget":
            funScript = funAction.formrecord_widget
        else:
            return False

        if not funScript:
            if Project.debugLevel > 50:
                print("No existe el script para la acción %s en el módulo %s" %
                      (aFunction[0], aFunction[0]))
            return False

        fn = getattr(funScript, aFunction[2], None)
        if fn is None:
            if Project.debugLevel > 50:
                print("No existe la función %s en %s" %
                      (aFunction[2], function))
            return True

        # fn = None
        try:
            # fn = eval(function, pineboolib.qsaglobals.__dict__)
            if aList:
                return fn(*aList)
            else:
                return fn()

        except Exception:
            # print("** JS.CALL :: ERROR:", traceback.format_exc())
            if showException:
                print("** JS.CALL :: ERROR:", traceback.format_exc())

        return None

    def loadTranslations(self):
        translatorsCopy = None
        # if self.translators:
        #     translatorsCopy = copy.copy(self.translators)
        #     for it in translatorsCopy:
        #         self.removeTranslator(it)

        lang = QtCore.QLocale().name()[:2]
        for module in self.modules.keys():
            self.loadTranslationFromModule(module, lang)

        if translatorsCopy:
            for it in translatorsCopy:
                item = it
                if item.sysTrans_:
                    self.installTranslator(item)
                else:
                    item.deletelater()

    @decorators.BetaImplementation
    def trMulti(self, s, l):
        backMultiEnabled = self.multiLangEnabled_
        ret = self.translate("%s_MULTILANG" % l.upper(). s)
        self.multiLangEnabled_ = backMultiEnabled
        return ret

    @decorators.BetaImplementation
    def setMultiLang(self, enable, langid):
        self.multiLangEnabled_ = enable
        if enable and langid:
            self.multiLangId_ = langid.upper()

    def loadTranslationFromModule(self, idM, lang):
        self.installTranslator(self.createModTranslator(idM, lang, True))
        # self.installTranslator(self.createModTranslator(idM, "mutliLang"))

    def installTranslator(self, tor):
        if not tor:
            return
        else:
            qApp.installTranslator(tor)
            self.translator_.append(tor)

    @decorators.NotImplementedWarn
    def createSysTranslator(self, lang, loadDefault):
        pass

    def createModTranslator(self, idM, lang, loadDefault=False):
        fileTs = "%s.%s.ts" % (idM, lang)
        key = self.conn.managerModules().shaOfFile(fileTs)

        if key is not None or idM == "sys":
            tor = FLTranslator(self, "%s_%s" %
                               (idM, lang), lang == "multilang")

            if tor.loadTsContent(key):
                return tor

        return self.createModTranslator(idM, "es") if loadDefault else None

    @decorators.NotImplementedWarn
    def initToolBox(self):
        pass

    def parseScript(self, scriptname):
        # Intentar convertirlo a Python primero con flscriptparser2
        if not os.path.isfile(scriptname):
            raise IOError
        python_script_path = (
            scriptname + ".xml.py").replace(".qs.xml.py", ".qs.py")
        if not os.path.isfile(python_script_path) or pineboolib.no_python_cache:
            print("Convirtiendo a Python . . .", scriptname)
            # ret = subprocess.call(["flscriptparser2", "--full",script_path])
            from pineboolib.flparser import postparse
            try:
                postparse.pythonify(scriptname)
            except Exception as e:
                qWarning("WARN: El fichero %s no se ha podido convertir: %s" %
                         (scriptname, e))

        # if not os.path.isfile(python_script_path):
        #    raise AssertionError(u"No se encontró el módulo de Python, falló flscriptparser?")

    def reinitP(self):
        if self.acl_:
            self.acl_.init_()

        self.call("sys.widget.init()", [], None, True)

    def resolveDGIObject(self, name):
        obj_ = getattr(self._DGI, name)
        if obj_:
            return obj_

        print("WARN: Project.resolveSDIObject no puede encontra el objeto %s en %s" % (
            name, self._DGI.alias()))


class Module(object):
    def __init__(self, project, areaid, name, description, icon):
        self.prj = project
        self.areaid = areaid
        self.name = name
        self.description = description  # En python2 era .decode(UTF-8)
        self.icon = icon
        self.files = {}
        self.tables = {}
        self.loaded = False
        self.path = self.prj.path

    def add_project_file(self, fileobj):
        self.files[fileobj.filename] = fileobj

    def load(self):
        pathxml = self.path("%s.xml" % self.name)
        pathui = self.path("%s.ui" % self.name)
        if pathxml is None:
            print("ERROR: modulo %r: fichero XML no existe" % (self.name))
            return False
        if pathui is None:
            print("ERROR: modulo %r: fichero UI no existe" % (self.name))
            return False
        if self.prj._DGI.useDesktop() and self.prj._DGI.localDesktop():
            tiempo_1 = time.time()
        try:
            self.actions = ModuleActions(self, pathxml, self.name)
            self.actions.load()
            if self.prj._DGI.useDesktop():
                self.mainform = MainForm(self, pathui)
                self.mainform.load()
        except Exception as e:
            print("ERROR al cargar modulo %r:" % self.name, e)
            print(traceback.format_exc(), "---")
            return False

        # TODO: Load Main Script:
        self.mainscript = None
        # /-----------------------
        if self.prj._DGI.useDesktop() and self.prj._DGI.localDesktop():
            tiempo_2 = time.time()

        for tablefile in self.files:
            if not tablefile.endswith(".mtd"):
                continue
            name, ext = os.path.splitext(tablefile)
            try:
                contenido = str(open(self.path(tablefile),
                                     "rb").read(), "ISO-8859-15")
            except UnicodeDecodeError as e:
                print("Error al leer el fichero", tablefile, e)
                continue
            tableObj = parseTable(name, contenido)
            if tableObj is None:
                print("No se pudo procesar. Se ignora tabla %s/%s " %
                      (self.name, name))
                continue
            self.tables[name] = tableObj
            self.prj.tables[name] = tableObj

        if self.prj._DGI.useDesktop() and self.prj._DGI.localDesktop():
            tiempo_3 = time.time()
            if tiempo_3 - tiempo_1 > 0.2:
                if Project.debugLevel > 50:
                    print("Carga del modulo %s : %.3fs ,  %.3fs" %
                          (self.name, tiempo_2 - tiempo_1, tiempo_3 - tiempo_2))

        self.loaded = True
        return True


class File(object):
    def __init__(self, project, module, filename, sha=None, basedir=None):
        self.prj = project
        self.module = module
        self.filename = filename
        self.sha = sha
        if filename.endswith(".qs.py"):
            self.ext = ".qs.py"
            self.name = os.path.splitext(os.path.splitext(filename)[0])[0]
        else:
            self.name, self.ext = os.path.splitext(filename)

        db_name = self.prj.conn.DBName()

        if self.sha:
            self.filekey = "%s/%s/file%s/%s/%s%s" % (
                db_name, module, self.ext, self.name, sha, self.ext)
        else:
            self.filekey = filename
        self.basedir = basedir

    def path(self):
        if self.basedir:
            # Probablemente porque es local . . .
            return self.prj.dir(self.basedir, self.filename)
        else:
            # Probablemente es remoto (DB) y es una caché . . .
            return self.prj.dir("cache", *(self.filekey.split("/")))


class DelayedObjectProxyLoader(object):
    def __init__(self, obj, *args, **kwargs):
        self._name = "unnamed-loader"
        if "name" in kwargs:
            self._name = kwargs["name"]
            del kwargs["name"]
        self._obj = obj
        self._args = args
        self._kwargs = kwargs
        self.loaded_obj = None

    def __load(self):
        if not self.loaded_obj:
            if Project.debugLevel > 50:
                print("DelayedObjectProxyLoader: loading %s %r( *%r **%r)" %
                      (self._name, self._obj, self._args, self._kwargs))
            self.loaded_obj = self._obj(*self._args, **self._kwargs)
        return self.loaded_obj

    def __getattr__(self, name):  # Solo se lanza si no existe la propiedad.
        obj = self.__load()
        return getattr(obj, name)


class ModuleActions(object):
    def __init__(self, module, path, modulename):
        self.mod = module
        self.prj = module.prj
        self.path = path
        self.moduleName = modulename
        assert path

    def load(self):
        from pineboolib import qsaglobals

        self.parser = etree.XMLParser(
            ns_clean=True,
            encoding="ISO-8859-15",
            remove_blank_text=True,
        )

        self.tree = etree.parse(self.path, self.parser)
        self.root = self.tree.getroot()
        action = XMLAction(self.prj, None)
        action.mod = self
        action.prj = self.prj
        action.name = self.mod.name
        action.alias = self.mod.name
        # action.form = self.mod.name
        action.form = None
        action.table = None
        action.scriptform = self.mod.name
        self.prj.actions[action.name] = action
        if hasattr(qsaglobals, action.name):
            # print("INFO: No se sobreescribe variable de entorno", action.name)
            pass
        else:
            setattr(qsaglobals, action.name, DelayedObjectProxyLoader(
                action.load, name="QSA.Module.%s" % action.name))

        for xmlaction in self.root:
            action = XMLAction(self.prj, xmlaction)
            action.mod = self
            action.prj = self.prj
            try:
                name = action.name
            except AttributeError:
                name = "unnamed"
            self.prj.actions[name] = action
            # print(":::" , self.mod.name, name)
            if name != "unnamed":
                if hasattr(qsaglobals, "form" + name):
                    if Project.debugLevel > 150:
                        print(
                            "INFO: No se sobreescribe variable de entorno", "form" + name)
                    pass
                else:
                    setattr(qsaglobals, "form" + name, DelayedObjectProxyLoader(action.load,
                                                                                name="QSA.Module.%s.Action.form%s" % (self.mod.name, name)))

                if hasattr(qsaglobals, "formRecord" + name):
                    if Project.debugLevel > 150:
                        print("INFO: No se sobreescribe variable de entorno",
                              "formRecord" + name)
                    pass
                else:
                    setattr(qsaglobals, "formRecord" + name, DelayedObjectProxyLoader(
                        action.loadRecord, name="QSA.Module.%s.Action.formRecord%s" % (self.mod.name, name)))

    def __contains__(self, k):
        return k in self.prj.actions

    def __getitem__(self, k):
        return self.prj.actions[k]

    def __setitem__(self, k, v):
        raise NotImplementedError("Actions are not writable!")
        self.prj.actions[k] = v


class MainForm(object):
    logger = logging.getLogger("main.MainForm")
    
    def __init__(self, module, path):
        self.mod = module
        self.prj = module.prj
        self.path = path
        assert path

    def load(self):
        try:
            self.parser = etree.XMLParser(
                ns_clean=True,
                encoding="UTF8",
                remove_blank_text=True,
            )
            self.tree = etree.parse(self.path, self.parser)
        except etree.XMLSyntaxError:
            try:
                self.parser = etree.XMLParser(
                    ns_clean=True,
                    encoding="ISO-8859-15",
                    recover=True,
                    remove_blank_text=True,
                )
                self.tree = etree.parse(self.path, self.parser)
                self.logger.exception("Formulario %r se cargó con codificación ISO (UTF8 falló)", self.path)
            except etree.XMLSyntaxError:
                self.logger.exception("Error cargando UI después de intentar con UTF8 y ISO", self.path)

        self.root = self.tree.getroot()
        self.actions = {}
        self.pixmaps = {}
        if self.prj._DGI.useDesktop():
            for image in self.root.xpath("images/image[@name]"):
                name = image.get("name")
                xmldata = image.xpath("data")[0]
                img_format = xmldata.get("format")
                data = unhexlify(xmldata.text.strip())
                if img_format == "XPM.GZ":
                    data = zlib.decompress(data, 15)
                    img_format = "XPM"
                
                if self.prj._DGI.localDesktop():
                    pixmap = QtGui.QPixmap()
                    pixmap.loadFromData(data, img_format)
                    icon = QtGui.QIcon(pixmap)
                    self.pixmaps[name] = icon
                else:
                    self.pixmaps[name] = data

        for xmlaction in self.root.xpath("actions//action"):
            action = XMLMainFormAction(xmlaction)
            action.mainform = self
            action.mod = self.mod
            action.prj = self.prj
            iconSet = getattr(action, "iconSet", None)
            action.icon = None
            if iconSet:
                try:
                    action.icon = self.pixmaps[iconSet]
                except Exception as e:
                    if self.prj._DGI.useDesktop():
                        print(
                            "main.Mainform: Error al intentar decodificar icono de accion. No existe.")
                        print(e)
            else:
                action.iconSet = None
            # if iconSet:
            #    for images in self.root.xpath("images/image[@name='%s']" % iconSet):
            #        print("*****", iconSet, images)
            self.actions[action.name] = action
            if not self.prj._DGI.localDesktop():
                self.prj._DGI.mainForm().mainWindow.loadAction(action)

            # Asignamos slot a action
            for slots in self.root.xpath("connections//connection"):
                slot = XMLStruct(slots)
                if slot._v("sender") == action.name:
                    action.slot = slot._v("slot")
                    action.slot = action.slot.replace('(', '')
                    action.slot = action.slot.replace(')', '')
                if not self.prj._DGI.localDesktop():
                    self.prj._DGI.mainForm().mainWindow.loadConnection(action)

        self.toolbar = []
        for toolbar_action in self.root.xpath("toolbars//action"):
            self.toolbar.append(toolbar_action.get("name"))
            if not self.prj._DGI.localDesktop():
                self.prj._DGI.mainForm().mainWindow.loadToolBarsAction(toolbar_action.get("name"))
        # self.ui = WMainForm()
        # self.ui.load(self.path)
        # self.ui.show()


class XMLMainFormAction(XMLStruct):
    name = "unnamed"
    text = ""
    mainform = None
    mod = None
    prj = None
    slot = None

    def run(self):
        if Project.debugLevel > 50:
            print("Running MainFormAction:", self.name, self.text, self.slot)
        try:
            action = self.mod.actions[self.name]
            getattr(action, self.slot, "unknownSlot")()
        finally:
            if Project.debugLevel > 50:
                print("END of Running MainFormAction:",
                      self.name, self.text, self.slot)


class XMLAction(XMLStruct):

    def __init__(self, _project, *args, **kwargs):
        super(XMLAction, self).__init__(*args, **kwargs)
        self.prj = _project
        self.form = self._v("form")
        self.script = self._v("script")
        self.mainform = self._v("mainform")
        self.mainscript = self._v("mainscript")
        self.mainform_widget = None
        self.formrecord_widget = None
        self._loaded = False
        self._record_loaded = False

    def loadRecord(self, cursor=None):
        # if self.formrecord_widget is None:
        if not getattr(self, "formrecord", None):
            if Project.debugLevel > 50:
                print("Record action %s is not defined. Canceled !" %
                      (self.name))
            return None
        if Project.debugLevel > 50:
            print("Loading record action %s . . . " % (self.name))
        parent_or_cursor = cursor  # Sin padre, ya que es ventana propia
        self.formrecord_widget = FLFormRecordDB(
            parent_or_cursor, self, load=True)
        self.formrecord_widget.setWindowModality(Qt.ApplicationModal)
        # self._record_loaded = True
        if self.mainform_widget:
            if Project.debugLevel > 50:
                print("End of record action load %s (iface:%s ; widget:%s)"
                      % (self.name,
                         repr(self.mainform_widget.iface),
                          repr(self.mainform_widget.widget)
                         )
                      )

        self.initModule(self.name)
        return self.formrecord_widget

    def load(self):
        try:
            return self._load()
        except Exception as e:
            print("ERROR: Loading action %s: %s" % (self.name, e))
            print(traceback.format_exc())
            return None

    def _load(self):
        if self._loaded:
            return self.mainform_widget
        if Project.debugLevel > 50:
            print("Loading action %s . . . " % (self.name))
        w = self.prj.main_window
        if not self.mainform_widget:
            if self.prj._DGI.useDesktop():
                self.mainform_widget = FLMainForm(w, self, load=True)
            else:
                from pineboolib.utils import Struct
                self.mainform_widget = Struct()
                self.mainform_widget.action = self
                self.mainform_widget.prj = self.prj
                try:
                    self.load_script(
                        getattr(self, "scriptform", None), self.mainform_widget)
                except Exception:
                    print(traceback.format_exc(), "---")

        self._loaded = True
        if Project.debugLevel > 50:
            print("End of action load %s (iface:%s ; widget:%s)"
                  % (self.name,
                     repr(self.mainform_widget.iface),
                     repr(self.mainform_widget.widget)
                     )
                  )
        return self.mainform_widget

    def openDefaultForm(self):
        if Project.debugLevel > 50:
            print("Opening default form for Action", self.name)
        self.load()
        # Es necesario importarlo a esta altura, QApplication tiene que ser
        # ... construido antes que cualquier widget)
        w = self.prj.main_window
        # self.mainform_widget.init()
        self.initModule(self.name)
        self.mainform_widget = FLMainForm(w, self, load=True)
        w.addFormTab(self)
        # self.mainform_widget.show()

    def formRecord(self):
        return self.form

    def openDefaultFormRecord(self, cursor=None):
        if Project.debugLevel > -50:
            print("Opening default formRecord for Action", self.name)
        w = self.loadRecord(cursor)
        # w.init()
        if w:
            w.show()

    def execDefaultScript(self):
        if Project.debugLevel > 50:
            print("Executing default script for Action", self.name)

        self.load_script(self.scriptform, None)
        self.initModule(self.name)
        if getattr(self.script.form, "iface", None):
            self.script.form.iface.main()
        else:
            self.script.form.main()

    def load_script(self, scriptname, parent=None):
        print("Cargando script " + str(scriptname) + " de " +
              str(parent) + " accion " + str(self.name))

        parent_ = parent
        if parent is None:
            parent = self
            action_ = self
            prj_ = self.prj
        else:
            action_ = parent.action
            prj_ = parent.prj

        # Si ya esta cargado se reusa...
        if getattr(self, "script", None) and parent_:
            parent.script = self.script
            # self.script.form = self.script.FormInternalObj(action = self.action, project = self.prj, parent = self)
            parent.widget = parent.script.form
            if getattr(parent.widget, "iface", None):
                parent.iface = parent.widget.iface
            return

            # import aqui para evitar dependencia ciclica
        import pineboolib.emptyscript
        python_script_path = None
        # primero default, luego sobreescribimos
        parent.script = pineboolib.emptyscript

        if scriptname is None:
            parent.script.form = parent.script.FormInternalObj(
                action=action_, project=prj_, parent=parent)
            parent.widget = parent.script.form
            parent.iface = parent.widget.iface
            return

        script_path_qs = prj_.path(scriptname + ".qs")
        script_path_py = prj_.path(
            scriptname + ".py") or prj_.path(scriptname + ".qs.py")

        overload_pyfile = os.path.join(
            parent.prj.tmpdir, "overloadpy", scriptname + ".py")
        if os.path.isfile(overload_pyfile):
            print(
                "WARN: ** cargando %r de overload en lugar de la base de datos!!" % scriptname)
            try:
                parent.script = importlib.machinery.SourceFileLoader(
                    scriptname, overload_pyfile).load_module()
            except Exception as e:
                print("ERROR al cargar script OVERLOADPY para la accion %r:" %
                      action_.name, e)
                print(traceback.format_exc(), "---")

        elif script_path_py:
            script_path = script_path_py
            print("Loading script PY %s . . . " % scriptname)
            if not os.path.isfile(script_path):
                raise IOError
            try:
                print("Cargando %s : %s " % (scriptname,
                                             script_path.replace(parent.prj.tmpdir, "tempdata")))
                parent.script = importlib.machinery.SourceFileLoader(
                    scriptname, script_path).load_module()
            except Exception as e:
                print("ERROR al cargar script PY para la accion %r:" %
                      action_.name, e)
                print(traceback.format_exc(), "---")

        elif script_path_qs:
            script_path = script_path_qs
            print("Loading script QS %s . . . " % scriptname)
            # Intentar convertirlo a Python primero con flscriptparser2
            if not os.path.isfile(script_path):
                raise IOError
            python_script_path = (
                script_path + ".xml.py").replace(".qs.xml.py", ".qs.py")
            if not os.path.isfile(python_script_path) or pineboolib.no_python_cache:
                print("Convirtiendo a Python . . .")
                # ret = subprocess.call(["flscriptparser2", "--full",script_path])
                from pineboolib.flparser import postparse
                postparse.pythonify(script_path)

            if not os.path.isfile(python_script_path):
                raise AssertionError(
                    u"No se encontró el módulo de Python, falló flscriptparser?")
            try:
                print("Cargando %s : %s " % (scriptname,
                                             python_script_path.replace(self.prj.tmpdir, "tempdata")))
                parent.script = importlib.machinery.SourceFileLoader(
                    scriptname, python_script_path).load_module()
                # self.script = imp.load_source(scriptname,python_script_path)
                # self.script = imp.load_source(scriptname,filedir(scriptname+".py"), open(python_script_path,"U"))
            except Exception as e:
                print("ERROR al cargar script QS para la accion %r:" %
                      action_.name, e)
                print(traceback.format_exc(), "---")

        parent.script.form = parent.script.FormInternalObj(
            action_, prj_, parent_)
        if parent_:
            parent.widget = parent.script.form
            if getattr(parent.widget, "iface", None):
                parent.iface = parent.widget.iface

    def unknownSlot(self):
        print("Executing unknown script for Action", self.name)
        # Aquí debería arramcar el script

    """
    Inicializa el modulo del form en caso de que no se inicializara ya
    """

    def initModule(self, name):

        moduleName = self.prj.actions[name].mod.moduleName
        if moduleName in (None, "sys"):
            return
        if moduleName not in self.prj._initModules:
            self.prj._initModules.append(moduleName)
            self.prj.call("%s.iface.init()" % moduleName, [], None, False)
            return


class FLMainForm(FLFormDB):
    """ Controlador dedicado a las ventanas maestras de búsqueda (en pestaña) """
    pass
