"""
Project Module.
"""
import os
import time
from typing import List, Optional, Any, Dict, TYPE_CHECKING
from optparse import Values

# from pineboolib.fllegacy.flaccesscontrollists import FLAccessControlLists # FIXME: Not allowed yet
from PyQt5 import QtCore  # type: ignore

from pineboolib.core.utils import logging
from pineboolib.core.utils.utils_base import filedir
from pineboolib.core.utils.struct import AreaStruct
from pineboolib.core.exceptions import CodeDoesNotBelongHereException, NotConnectedError
from pineboolib.core.settings import config

from pineboolib.application.module import Module
from pineboolib.application.utils.path import _dir

if TYPE_CHECKING:
    from pineboolib.interfaces.dgi_schema import dgi_schema
    from pineboolib.application.database.pnconnection import PNConnection
    from pineboolib.core.utils.struct import ActionStruct  # noqa: F401


class Project(object):
    """
    Singleton for the whole application.

    Can be accessed with pineboolib.project from anywhere.
    """

    logger = logging.getLogger("main.Project")
    _app: Optional[QtCore.QCoreApplication] = None
    _conn: Optional["PNConnection"] = None  # Almacena la conexión principal a la base de datos
    debugLevel = 100
    options: Values
    modules: Dict[str, "Module"]

    # _initModules = None
    main_form: Any = None  # FIXME: How is this used? Which type?
    main_window: Any = None
    acl_ = None
    _DGI: Optional["dgi_schema"] = None
    deleteCache = None
    path = None
    _splash = None
    sql_drivers_manager = None
    timer_ = None
    no_python_cache = False  # TODO: Fill this one instead
    _msg_mng = None

    def __init__(self) -> None:
        """Constructor."""
        self._conn = None
        self._DGI = None
        self.tree = None
        self.root = None
        self.apppath = ""
        self.tmpdir = filedir("../tempdata")
        self.parser = None
        self.main_form_name: Optional[str] = None
        self.deleteCache = False
        self.parseProject = False
        self.translator_: List[Any] = []  # FIXME: Add proper type
        self.actions: Dict[Any, "ActionStruct"] = {}  # FIXME: Add proper type
        self.tables: Dict[Any, Any] = {}  # FIXME: Add proper type
        self.files: Dict[Any, Any] = {}  # FIXME: Add proper type
        self.options = Values()

    @property
    def app(self) -> QtCore.QCoreApplication:
        """Retrieve current Qt Application or throw error."""
        if self._app is None:
            raise Exception("No application set")
        return self._app

    def set_app(self, app: QtCore.QCoreApplication):
        """Set Qt Application."""
        self._app = app

    @property
    def conn(self) -> "PNConnection":
        """Retrieve current connection or throw."""
        if self._conn is None:
            raise Exception("Project is not initialized")
        return self._conn

    @property
    def DGI(self) -> "dgi_schema":
        """Retrieve current DGI or throw."""
        if self._DGI is None:
            raise Exception("Project is not initialized")
        return self._DGI

    def init_conn(self, connection: "PNConnection") -> None:
        """Initialize project with a connection."""
        self._conn = connection
        self.apppath = filedir("..")
        self.tmpdir = config.value("ebcomportamiento/kugar_temp_dir", filedir("../tempdata"))
        if not os.path.exists(self.tmpdir):
            os.mkdir(self.tmpdir)

        self.deleteCache = config.value("ebcomportamiento/deleteCache", False)
        self.parseProject = config.value("ebcomportamiento/parseProject", False)

    def init_dgi(self, DGI: "dgi_schema") -> None:
        """Load and associate the defined DGI onto this project."""
        # FIXME: Actually, DGI should be loaded here, or kind of.
        from pineboolib.core.message_manager import Manager

        self._DGI = DGI

        self._msg_mng = Manager(DGI)

        self.main_form_name = "eneboo"  # FIXME: Belongs to loader.main .. or dgi-qt5
        if config.value("ebcomportamiento/mdi_mode"):
            self.main_form_name = "eneboo_mdi"  # FIXME: Belongs to loader.main .. or dgi-qt5

        self._DGI.extraProjectInit()

    def load_modules(self) -> None:
        """Load all modules."""
        for module_name, mod_obj in self.modules.items():
            mod_obj.load()
            self.tables.update(mod_obj.tables)

    def setDebugLevel(self, q: int) -> None:
        """
        Set debug level for application.

        @param q Número con el nivel espeficicado
        ***DEPRECATED***
        """
        Project.debugLevel = q
        # self._DGI.pnqt3ui.Options.DEBUG_LEVEL = q

    # def acl(self) -> Optional[FLAccessControlLists]:
    #     """
    #     Retorna si hay o no acls cargados
    #     @return Objeto acl_
    #     """
    #     return self.acl_
    def acl(self):
        """Return loaded ACL."""
        raise CodeDoesNotBelongHereException("ACL Does not belong to PROJECT. Go away.")

    def run(self) -> bool:
        """Run project. Connects to DB and loads data."""

        if self.actions:
            del self.actions

        if self.tables:
            del self.tables

        self.actions = {}
        self.tables = {}

        if self._DGI is None:
            raise Exception("DGI not loaded")

        if not self.conn or not self.conn.conn:
            raise NotConnectedError("Cannot execute Pineboo Project without a connection in place")

        # TODO: Refactorizar esta función en otras más sencillas
        # Preparar temporal

        if self.deleteCache and os.path.exists(_dir("cache/%s" % self.conn.DBName())):

            self.message_manager().send("splash", "showMessage", ["Borrando caché ..."])
            self.logger.debug(
                "DEVELOP: DeleteCache Activado\nBorrando %s", _dir("cache/%s" % self.conn.DBName())
            )
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
            keep_images = config.value("ebcomportamiento/keep_general_cache", False)
            if keep_images is False:
                for f in os.listdir(self.tmpdir):
                    if f.find(".") > -1:
                        pt_ = os.path.join(self.tmpdir, f)
                        os.remove(pt_)

        # Conectar:

        # Se verifica que existen estas tablas
        for table in (
            "flareas",
            "flmodules",
            "flfiles",
            "flgroups",
            "fllarge",
            "flserial",
            "flusers",
            "flvar",
            "flmetadata",
        ):
            self.conn.manager().createSystemTable(table)

        cursor_ = self.conn.dbAux().cursor()
        self.areas: Dict[str, AreaStruct] = {}
        cursor_.execute(""" SELECT idarea, descripcion FROM flareas WHERE 1 = 1""")
        for idarea, descripcion in cursor_:
            self.areas[idarea] = AreaStruct(idarea=idarea, descripcion=descripcion)

        self.areas["sys"] = AreaStruct(idarea="sys", descripcion="Area de Sistema")

        # Obtener módulos activos
        cursor_.execute(
            """ SELECT idarea, idmodulo, descripcion, icono FROM flmodules WHERE bloqueo = %s """
            % self.conn.driver().formatValue("bool", "True", False)
        )

        self.modules: Dict[str, "Module"] = {}
        from pineboolib.application.utils.xpm import cacheXPM

        for idarea, idmodulo, descripcion, icono in cursor_:
            icono = cacheXPM(icono)
            self.modules[idmodulo] = Module(idarea, idmodulo, descripcion, icono)

        file_object = open(filedir("..", "share", "pineboo", "sys.xpm"), "r")
        icono = file_object.read()
        file_object.close()
        # icono = clearXPM(icono)

        self.modules["sys"] = Module("sys", "sys", "Administración", icono)

        cursor_.execute(
            """ SELECT idmodulo, nombre, sha FROM flfiles WHERE NOT sha = '' ORDER BY idmodulo, nombre """
        )

        size_ = cursor_.rowcount

        f1 = open(_dir("project.txt"), "w")
        self.files = {}
        if self._DGI.useDesktop() and self._DGI.localDesktop():
            tiempo_ini = time.time()
        if not os.path.exists(_dir("cache")):
            raise AssertionError
        p = 0
        from pineboolib.application.file import File

        for idmodulo, nombre, sha in cursor_:
            if not self._DGI.accept_file(nombre):
                continue

            p = p + 1
            if idmodulo not in self.modules:
                continue  # I
            fileobj = File(idmodulo, nombre, sha, db_name=self.conn.DBName())
            if nombre in self.files:
                self.logger.warning("run: file %s already loaded, overwritting..." % nombre)
            self.files[nombre] = fileobj
            self.modules[idmodulo].add_project_file(fileobj)
            f1.write(fileobj.filekey + "\n")

            fileobjdir = os.path.dirname(_dir("cache", fileobj.filekey))
            file_name = _dir("cache", fileobj.filekey)
            if not os.path.exists(fileobjdir):
                os.makedirs(fileobjdir)

            if os.path.exists(file_name):
                if file_name.endswith(".qs"):
                    if os.path.exists("%s.py" % file_name):
                        continue

                elif file_name.endswith(".mtd"):
                    if not config.value("ebcomportamiento/orm_parser_disabled", False):
                        if os.path.exists("%s_model.py" % _dir("cache", fileobj.filekey[:-4])):
                            continue
                else:
                    continue

            cur2 = self.conn.dbAux().cursor()
            sql = (
                "SELECT contenido FROM flfiles WHERE idmodulo = %s AND nombre = %s AND sha = %s"
                % (
                    self.conn.driver().formatValue("string", idmodulo, False),
                    self.conn.driver().formatValue("string", nombre, False),
                    self.conn.driver().formatValue("string", sha, False),
                )
            )
            cur2.execute(sql)
            for (contenido,) in cur2:

                encode_ = "ISO-8859-15"
                if str(nombre).endswith(".kut") or str(nombre).endswith(".ts"):
                    encode_ = "utf-8"

                folder = _dir(
                    "cache",
                    "/".join(fileobj.filekey.split("/")[: len(fileobj.filekey.split("/")) - 1]),
                )
                if (
                    os.path.exists(folder) and not file_name
                ):  # Borra la carpeta si no existe el fichero destino
                    for root, dirs, files in os.walk(folder):
                        for f in files:
                            os.remove(os.path.join(root, f))

                self.message_manager().send(
                    "splash", "showMessage", ["Volcando a caché %s..." % nombre]
                )

                if contenido and not os.path.exists(file_name):
                    f2 = open(file_name, "wb")
                    txt = contenido.encode(encode_, "replace")
                    f2.write(txt)
                    f2.close()

            if (
                self.parseProject
                and nombre.endswith(".qs")
                and config.value("application/isDebuggerMode", False)
            ):
                self.message_manager().send(
                    "splash", "showMessage", ["Convirtiendo %s ( %d/ %d) ..." % (nombre, p, size_)]
                )
                if os.path.exists(file_name):

                    self.parseScript(file_name, "(%d de %d)" % (p, size_))

        tiempo_fin = time.time()
        self.logger.info(
            "Descarga del proyecto completo a disco duro: %.3fs", (tiempo_fin - tiempo_ini)
        )

        # Cargar el núcleo común del proyecto
        idmodulo = "sys"
        for root, dirs, files in os.walk(filedir("..", "share", "pineboo")):
            for nombre in files:
                if root.find("modulos") == -1:
                    fileobj = File(idmodulo, nombre, basedir=root, db_name=self.conn.DBName())
                    self.files[nombre] = fileobj
                    self.modules[idmodulo].add_project_file(fileobj)
                    if self.parseProject and nombre.endswith(".qs"):
                        self.parseScript(_dir(root, nombre))

        if not config.value("ebcomportamiento/orm_load_disabled", False):
            self.message_manager().send("splash", "showMessage", ["Cargando objetos ..."])
            # from pineboolib.application.parsers.mtdparser.pnormmodelsfactory import load_models
            # load_models()

        self.message_manager().send("splash", "showMessage", ["Cargando traducciones ..."])

        # FIXME: ACLs needed at this level?
        # self.acl_ = FLAccessControlLists()
        # self.acl_.init()

        return True

    def call(
        self,
        function: str,
        aList: List[Any],
        object_context: Any = None,
        showException: bool = True,
    ) -> Optional[Any]:
        """
        Call to a QS project function.

        @param function. Nombre de la función a llamar.
        @param aList. Array con los argumentos.
        @param objectContext. Contexto en el que se ejecuta la función.
        @param showException. Boolean que especifica si se muestra los errores.
        @return Boolean con el resultado.
        """
        # FIXME: No deberíamos usar este método. En Python hay formas mejores
        # de hacer esto.
        self.logger.trace(
            "JS.CALL: fn:%s args:%s ctx:%s", function, aList, object_context, stack_info=True
        )

        # Tipicamente flfactalma.iface.beforeCommit_articulos()
        if function[-2:] == "()":
            function = function[:-2]

        aFunction = function.split(".")

        if not object_context:
            if not aFunction[0] in self.actions:
                if len(aFunction) > 1:
                    if showException:
                        self.logger.error(
                            "No existe la acción %s en el módulo %s", aFunction[1], aFunction[0]
                        )
                else:
                    if showException:
                        self.logger.error("No existe la acción %s", aFunction[0])
                return None

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
                fR = funAction.load_script(aFunction[0], None)
                object_context = fR.iface
            else:
                return False

            if not object_context:
                if showException:
                    self.logger.error(
                        "No existe el script para la acción %s en el módulo %s",
                        aFunction[0],
                        aFunction[0],
                    )
                return None

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
                self.logger.error("No existe la función %s en %s", function_name, aFunction[0])
            return (
                True
            )  # FIXME: Esto devuelve true? debería ser false, pero igual se usa por el motor para detectar propiedades

        try:
            return fn(*aList)
        except Exception:
            self.logger.exception("JSCALL: Error executing function %s", stack_info=True)

        return None

    def parseScript(self, scriptname: str, txt_: str = "") -> None:
        """
        Convert QS script into Python and stores it in the same folder.

        @param scriptname, Nombre del script a convertir
        """

        # Intentar convertirlo a Python primero con flscriptparser2
        if not os.path.isfile(scriptname):
            raise IOError
        python_script_path = (scriptname + ".xml.py").replace(".qs.xml.py", ".qs.py")
        if not os.path.isfile(python_script_path) or self.no_python_cache:
            file_name_l = scriptname.split(os.sep)  # FIXME: is a bad idea to split by os.sep
            file_name = file_name_l[len(file_name_l) - 2]

            msg = "Convirtiendo a Python . . . %s.qs %s" % (file_name, txt_)
            self.logger.info(msg)

            # clean_no_python = self._DGI.clean_no_python() # FIXME: No longer needed. Applied on the go.

            from pineboolib.application.parsers.qsaparser import postparse

            try:
                postparse.pythonify([scriptname])
            except Exception:
                self.logger.exception("El fichero %s no se ha podido convertir", scriptname)

    def test(self, name=None):
        """
        Start GUI tests.

        @param name, Nombre del test específico. Si no se especifica se lanzan todos los tests disponibles
        @return Texto con la valoración de los test aplicados
        """
        from importlib import import_module

        dirlist = os.listdir(filedir("../pineboolib/plugins/test"))
        testDict = {}
        for f in dirlist:
            if not f[0:2] == "__":
                f = f[: f.find(".py")]
                mod_ = import_module("pineboolib.plugins.test.%s" % f)
                test_ = getattr(mod_, f)
                testDict[f] = test_

        maxValue = 0
        value = 0
        resultValue = 0
        if name:
            try:
                t = testDict[name]()
                maxValue = t.maxValue()
                value = t.run()
            except Exception:
                self.logger.exception("While running tests")
        else:

            for test in testDict.keys():
                print("test", test)
                t = testDict[test]()
                maxValue = maxValue + t.maxValue
                v = t.run()
                print("result", test, v, "/", t.maxValue)
                value = value + v

        resultValue = value

        self.logger.warning("%s/%s", resultValue, maxValue)

        return True

    def get_temp_dir(self) -> str:
        """
        Return temporary folder defined for pineboo.

        @return ruta a la carpeta temporal
        ***DEPRECATED***
        """
        # FIXME: anti-pattern in Python. Getters for plain variables are wrong.
        raise CodeDoesNotBelongHereException("Use project.tmpdir instead, please.")
        # return self.tmpdir

    def load_version(self):
        """Initialize current version numbers."""
        self.version = "0.14"
        if config.value("application/dbadmin_enabled", False):
            self.version = "DBAdmin v%s" % self.version
        else:
            self.version = "Quick v%s" % self.version

    def message_manager(self):
        """Return message manager for splash and progress."""
        return self._msg_mng
