from pineboolib.flcontrols import ProjectClass
from pineboolib import decorators, qt3ui
from pineboolib.utils import filedir
from pineboolib.fllegacy.FLSqlQuery import FLSqlQuery
import os
import traceback

"""
Gestor de módulos.

Esta clase permite realizar las funciones básicas de manejo de ficheros
de texto que forman parte de los módulos de aplicación, utilizando como
soporte de almacenamiento la base de datos y el sistema de cachés de texto
para optimizar las lecturas.
Gestiona la carga y descarga de módulos. Mantiene cual es el módulo activo.
El módulo activo se puede establecer en cualquier momento con
FLManagerModules::setActiveIdModule().

Los módulos se engloban en áreas (FACTURACION, FINANCIERA, PRODUCCION, etc..) y
cada módulo tiene varios ficheros de texto XML y scripts. Toda la estructura de
módulos se almacena en las tablas flareas, flmodulos, flserial y flfiles, sirviendo esta
clase como interfaz para el manejo de dicha estructura en el entorno de trabajo
de AbanQ.

@author InfoSiAL S.L.
"""


class FLInfoMod(object):
    idModulo = None
    idArea = None
    descripcion = None
    version = None
    icono = None
    areaDescripcion = None


class FLManagerModules(ProjectClass):

    """
    Mantiene el identificador del area a la que pertenece el módulo activo.
    """
    activeIdArea_ = None

    """
    Mantiene el identificador del módulo activo.
    """
    activeIdModule_ = None

    """
    Mantiene la clave sha correspondiente a la version de los módulos cargados localmente
    """
    shaLocal_ = None

    """
    Diccionario de claves de ficheros, para optimizar lecturas
    """
    dictKeyFiles = {}

    """
    Lista de todos los identificadores de módulos cargados, para optimizar lecturas
    """
    listAllIdModules_ = {}

    """
    Lista de todas los identificadores de areas cargadas, para optimizar lecturas
    """
    listIdAreas_ = {}

    """
    Diccionario con información de los módulos
    """
    dictInfoMods = {}

    """
    Diccionario de identificadores de modulo de ficheros, para optimizar lecturas
    """
    dictModFiles = {}

    """
    Base de datos a utilizar por el manejador
    """
    db_ = None

    """
    Uso interno.
    Informacion para la carga estatica desde el disco local
    """
    staticBdInfo_ = None

    rootDir_ = None
    scriptsDir_ = None
    tablesDir_ = None
    formsDir_ = None
    reportsDir_ = None
    queriesDir_ = None
    transDir_ = None

    """
    constructor
    """

    def __init__(self, db=None):
        super(FLManagerModules, self).__init__()
        if db:
            self.db_ = db

    """
    destructor
    """

    def __del__(self):
        self.finish()

    """
    Acciones de inicialización del sistema de módulos.
    """
    @decorators.NotImplementedWarn
    def init(self):
        pass

    """
    Acciones de finalización del sistema de módulos.
    """
    @decorators.NotImplementedWarn
    def finish(self):
        pass

    """
    Obtiene el contenido de un fichero almacenado la base de datos.

    Este método busca el contenido del fichero solicitado en la
    base de datos, exactamente en la tabla flfiles, si no lo encuentra
    intenta obtenerlo del sistema de ficheros.

    @param n Nombre del fichero.
    @return QString con el contenido del fichero o vacía en caso de error.
    """

    def content(self, n):
        query = "SELECT contenido FROM flfiles WHERE nombre='%s'" % n
        cursor = self.db_.cursor()
        try:
            cursor.execute(query)
        except Exception:
            print("ERROR: FLManagerModules.content", traceback.format_exc())
            # cursor.execute("ROLLBACK")
            cursor.close()
            return None

        for contenido in cursor:
            return contenido[0]

    """
    Obtiene el contenido de un fichero de script, procesándolo para cambiar las conexiones que contenga,
    de forma que al acabar la ejecución de la función conectada se reanude el guión de pruebas.
    Tambien realiza procesos de formateo del código para optimizarlo.

    @param n Nombre del fichero.
    @return QString con el contenido del fichero o vacía en caso de error.
    """
    @decorators.NotImplementedWarn
    def byteCodeToStr(self, n):
        return None

    @decorators.NotImplementedWarn
    def contentCode(self, n):
        return None

    """
    Obtiene el contenido de un fichero almacenado en el sistema de ficheros.

    @param pN Ruta y nombre del fichero en el sistema de ficheros
    @return QString con el contenido del fichero o vacía en caso de error.
    """

    def contentFS(self, pN, utf8=False):
        ret = None
        try:
            if utf8:
                ret = str(open(pN, "rb").read(), "utf-8")
            else:
                ret = str(open(pN, "rb").read(), "ISO-8859-15")
        except Exception:
            pass

        return ret

    """
    Obtiene el contenido de un fichero, utilizando la caché de memoria y disco.

    Este método primero busca el contenido del fichero solicitado en la
    caché interna, si no está lo obtiene con el método FLManagerModules::content().

    @param n Nombre del fichero.
    @return QString con el contenido del fichero o vacía en caso de error.
    """

    def contentCached(self, n, shaKey=None):

        data = None
        modId = None
        name_ = n[:n.index(".")]
        ext_ = n[n.index(".") + 1:]

        if not shaKey and not self._prj.conn.manager().isSystemTable(name_):
            query = "SELECT sha FROM flfiles WHERE nombre='%s'" % n
            try:
                cursor = self.db_.cursor()
            except Exception:
                cursor = self._prj.conn.cursor()
            try:
                cursor.execute(query)
            except Exception:
                print("ERROR: FLManagerModules.contentCached",
                      traceback.format_exc())
                # cursor.execute("ROLLBACK")
                cursor.close()
                return None

            for contenido in cursor:
                shaKey = contenido[0]

        if self._prj.conn.manager().isSystemTable(name_):
            modId = "sys"
        else:
            modId = self._prj.conn.managerModules().idModuleOfFile(n)
        if os.path.exists(filedir("../tempdata/cache/%s/%s/file.%s/%s" % (self._prj.dbname, modId, ext_, name_))):
            utf8_ = False
            if ext_ == "kut":
                utf8_ = True
            data = self.contentFS(filedir("../tempdata/cache/%s/%s/file.%s/%s/%s.%s" %
                                          (self._prj.dbname, modId, ext_, name_, shaKey, ext_)), utf8_)
        elif os.path.exists(filedir("../share/pineboo/tables/%s.%s" % (name_, ext_))):
            data = self.contentFS(
                filedir("../share/pineboo/tables/%s.%s" % (name_, ext_)))
        else:
            data = self.content(n)

        return data

    """
    Almacena el contenido de un fichero en un módulo dado.

    @param n Nombre del fichero.
    @param idM Identificador del módulo al que se asociará el fichero
    @param content Contenido del fichero.
    """
    @decorators.NotImplementedWarn
    def setContent(self, n, idM, content):
        pass

    """
    Crea un formulario a partir de su fichero de descripción.

    Utiliza el método FLManagerModules::contentCached() para obtener el texto XML que describe
    el formulario.

    @param n Nombre del fichero que contiene la descricpción del formulario.
    @return QWidget correspondiente al formulario construido.
    """

    def createUI(self, n, connector=None, parent=None, name=None):
        if ".ui" not in n:
            n += ".ui"
        form_path = parent.prj.path(n)
        if form_path is None:
            raise AttributeError("File %r not found in project" % n)
        qt3ui.loadUi(form_path, parent.widget)

    """
    Llama al método load de los FLTableDB de un widget
    @param w Widget que contiene los FLTableDB
    """

    def loadFLTableDBs(self, w):
        qt3ui.loadFLTableDBs(w)

    """
    Crea el formulario maestro de una acción a partir de su fichero de descripción.

    Utiliza el método FLManagerModules::createUI() para obtener el formulario construido.

    @param a Objeto FLAction.
    @return QWidget correspondiente al formulario construido.
    """
    @decorators.NotImplementedWarn
    def createForm(self, a, connector=None, parent=None, name=None):
        return None

    """
    Esta función es igual a la anterior, sólo se diferencia en que carga
    la descripción de interfaz del formulario de edición de registros.
    """
    @decorators.NotImplementedWarn
    def createFormRecord(self, a, connector=None, parent=None, name=None):
        return None

    """
    Para establecer el módulo activo.

    Automáticamente también establece cual es el área correspondiente al módulo,
    ya que un módulo sólo puede pertenecer a una sola área.

    @param id Identificador del módulo
    """
    @decorators.NotImplementedWarn
    def setActiveIdModule(self, _id):
        pass

    """
    Para obtener el area del módulo activo.

    @return Identificador del area
    """

    def activeIdArea(self):
        return self.activeIdArea_

    """
    Para obtener el módulo activo.

    @return Identificador del módulo
    """

    def activeIdModule(self):
        return self.activeIdModule_

    """
    Obtiene la lista de identificadores de area cargadas en el sistema.

    @return Lista de identificadores de areas
    """
    @decorators.NotImplementedWarn
    def listIdAreas(self):
        return None

    """
    Obtiene la lista de identificadores de módulos cargados en el sistema de una area dada.

    @param idA Identificador del área de la que se quiere obtener la lista módulos
    @return Lista de identificadores de módulos
    """

    def listIdModules(self, idA):
        list_ = []
        for name, mod in self.dictInfoMods:
            if self.dictInfoMods[name].idArea == idA:
                list_.append(name)

        return list_

    """
    Obtiene la lista de identificadores de todos los módulos cargados en el sistema.

    @return Lista de identificadores de módulos
    """

    def listAllIdModules(self):
        return self.listAllIdModules_

    """
    Obtiene la descripción de un área a partir de su identificador.

    @param idA Identificador del área.
    @return Texto de descripción del área, si lo encuentra o idA si no lo encuentra.
    """
    @decorators.NotImplementedWarn
    def idAreaToDescription(self, idA):
        return None

    """
    Obtiene la descripción de un módulo a partir de su identificador.

    @param idM Identificador del módulo.
    @return Texto de descripción del módulo, si lo encuentra o idM si no lo encuentra.
    """
    @decorators.NotImplementedWarn
    def idModuleToDescription(self, idM):
        return None

    """
    Para obtener el icono asociado a un módulo.

    @param idM Identificador del módulo del que obtener el icono
    @return QPixmap con el icono
    """
    @decorators.NotImplementedWarn
    def iconModule(self, idM):
        return None

    """
    Para obtener la versión de un módulo.

    @param idM Identificador del módulo del que se quiere saber su versión
    @return Cadena con la versión
    """
    @decorators.NotImplementedWarn
    def versionModule(self, idM):
        return None

    """
    Para obtener la clave sha local.

    @return Clave sha de la versión de los módulos cargados localmente
    """
    @decorators.NotImplementedWarn
    def shaLocal(self):
        return None

    """
    Para obtener la clave sha global.

    @return Clave sha de la versión de los módulos cargados globalmente
    """
    @decorators.NotImplementedWarn
    def shaGlobal(self):
        return None

    """
    Establece el valor de la clave sha local con el del global.
    """
    @decorators.NotImplementedWarn
    def setShaLocalFromGlobal(self):
        pass

    """
    Obtiene la clave sha asociada a un fichero almacenado.

    @param n Nombre del fichero
    @return Clave sh asociada al ficheros
    """

    def shaOfFile(self, n):
        if self._prj.conn.dbAux() and not n[:3] == "sys" and not self._prj.conn.manager().isSystemTable(n):
            formatVal = self._prj.conn.manager().formatAssignValue("nombre", "string", n, True)
            q = FLSqlQuery(None, self._prj.conn.dbAux())
            # q.setForwardOnly(True)
            q.exec_("SELECT sha FROM flfiles WHERE %s" % formatVal)
            if q.next():
                return str(q.value(0))
            return None

        else:
            return None

    """
    Carga en el diccionario de claves las claves sha1 de los ficheros
    """

    def loadKeyFiles(self):

        self.dictKeyFiles = {}
        self.dictModFiles = {}
        q = FLSqlQuery(None, self._prj.conn.dbAux())
        # q.setForwardOnly(True)
        q.exec_("SELECT nombre, sha, idmodulo FROM flfiles")
        name = None
        while q.next():
            name = str(q.value(0))
            self.dictKeyFiles[name] = str(q.value(1))
            self.dictModFiles[name.upper()] = str(q.value(2))

    """
    Carga la lista de todos los identificadores de módulos
    """

    def loadAllIdModules(self):
        if not self._prj.conn.dbAux():
            return

        self.listAllIdModules_ = []
        self.listAllIdModules_.append("sys")
        self.dictInfoMods = {}

        q = FLSqlQuery(None, self._prj.conn.dbAux())
        # q.setForwardOnly(True)
        q.exec_("SELECT idmodulo,flmodules.idarea,flmodules.descripcion,version,icono,flareas.descripcion "
                "FROM flmodules left join flareas on flmodules.idarea = flareas.idarea")

        sysModuleFound = False
        while q.next():
            infoMod = FLInfoMod()
            infoMod.idModulo = str(q.value(0))
            infoMod.idArea = str(q.value(1))
            infoMod.descripcion = str(q.value(2))
            infoMod.version = str(q.value(3))
            infoMod.icono = str(q.value(4))
            infoMod.areaDescripcion = str(q.value(5))
            self.dictInfoMods[infoMod.idModulo.upper()] = infoMod

            if not infoMod.idModulo == "sys":
                self.listAllIdModules_.append(infoMod.idModulo)
            else:
                sysModuleFound = True

        if not sysModuleFound:
            infoMod = FLInfoMod()
            infoMod.idModulo = "sys"
            infoMod.idArea = "sys"
            infoMod.descripcion = "Administracion"
            infoMod.version = "0.0"
            infoMod.icono = self.contentFS(
                "%s/%s" % (filedir("../share/pineboo"), "/sys.xpm"))
            infoMod.areaDescripcion = "Sistema"
            self.dictInfoMods[infoMod.idModulo.upper()] = infoMod

    """
    Carga la lista de todos los identificadores de areas
    """

    def loadIdAreas(self):
        if not self._prj.conn.dbAux():
            return

        self.listIdAreas_ = []
        q = FLSqlQuery(None, self._prj.conn.dbAux())
        # q.setForwardOnly(True)
        q.exec_("SELECT idarea from flareas WHERE idarea <> 'sys'")
        while q.next():
            self.listIdAreas_.append(str(q.value(0)))

        self.listIdAreas_.append("sys")

    """
    Comprueba las firmas para un modulo dado
    """
    @decorators.NotImplementedWarn
    def checkSignatures(self):
        pass

    """
    Para obtener el identificador del módulo al que pertenece un fichero dado.

    @param n Nombre del fichero incluida la extensión
    @return Identificador del módulo al que pertenece el fichero
    """

    def idModuleOfFile(self, n):
        if not isinstance(n, str):
            n = n.toString()

        query = "SELECT idmodulo FROM flfiles WHERE nombre='%s'" % n
        cursor = self.db_.cursor()
        try:
            cursor.execute(query)
        except Exception:
            print("ERROR: FLManagerModules.idModuleOfFile",
                  traceback.format_exc())
            # cursor.execute("ROLLBACK")
            cursor.close()
            return None

        for idmodulo in cursor:
            return idmodulo[0]
    """
    Guarda el estado del sistema de módulos
    """
    @decorators.NotImplementedWarn
    def writeState(self):
        pass

    """
    Lee el estado del sistema de módulos
    """

    def readState(self):
        pass

    """
    Uso interno.
    Obtiene el contenido de un fichero mediante la carga estatica desde el disco local

    @param n Nombre del fichero.
    @return QString con el contenido del fichero o vacía en caso de error.
    """
    @decorators.NotImplementedWarn
    def contentStatic(self, n):
        return None

    """
    Uso interno.
    Muestra cuadro de dialogo para configurar la carga estatica desde el disco local
    """
    @decorators.NotImplementedWarn
    def staticLoaderSetup(self):
        pass
