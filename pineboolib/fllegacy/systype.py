from typing import Callable
import platform

from PyQt5 import QtCore  # type: ignore

from pineboolib.core.utils.singleton import Singleton
from pineboolib.core.settings import config
from pineboolib.core import decorators
from pineboolib.application import project

from pineboolib.core.utils import logging
from typing import Any

logger = logging.getLogger("fllegacy.systype")


class SysType(object, metaclass=Singleton):
    def __init__(self) -> None:
        self._name_user = None
        self.sys_widget = None
        self.time_user_ = QtCore.QDateTime.currentDateTime()

    def nameUser(self) -> str:
        ret_ = None
        if project.conn is None:
            raise Exception("Project is not connected yet")

        if not project._DGI:
            raise Exception("project._DGI is empty!")

        if project.DGI.use_alternative_credentials():
            ret_ = project.DGI.get_nameuser()
        else:
            ret_ = project.conn.user()

        return ret_

    def interactiveGUI(self) -> str:
        if not project._DGI:
            raise Exception("project._DGI is empty!")
        return project.DGI.interactiveGUI()

    def isUserBuild(self) -> bool:
        return self.version().upper().find("USER") > -1

    def isDeveloperBuild(self) -> bool:
        return self.version().upper().find("DEVELOPER") > -1

    def isNebulaBuild(self) -> bool:
        return self.version().upper().find("NEBULA") > -1

    def isDebuggerMode(self) -> bool:
        return bool(config.value("application/isDebuggerMode", False))

    @decorators.NotImplementedWarn
    def isCloudMode(self) -> bool:
        return False

    def isDebuggerEnabled(self) -> bool:
        return bool(config.value("application/dbadmin_enabled", False))

    def isQuickBuild(self) -> bool:
        return not self.isDebuggerEnabled()

    def isLoadedModule(self, modulename: str) -> bool:
        if project.conn is None:
            raise Exception("Project is not connected yet")
        return modulename in project.conn.managerModules().listAllIdModules()

    def translate(self, *args) -> str:
        from pineboolib.fllegacy.fltranslations import FLTranslate

        group = args[0] if len(args) == 2 else "scripts"
        text = args[1] if len(args) == 2 else args[0]

        if text == "MetaData":
            group, text = text, group

        text = text.replace(" % ", " %% ")

        return str(FLTranslate(group, text))

    def osName(self) -> str:
        """
        Devuelve el sistema operativo sobre el que se ejecuta el programa

        @return Código del sistema operativo (WIN32, LINUX, MACX)
        """
        if platform.system() == "Windows":
            return "WIN32"
        elif platform.system() == "Linux" or platform.system() == "Linux2":
            return "LINUX"
        elif platform.system() == "Darwin":
            return "MACX"
        else:
            return platform.system()

    def nameBD(self) -> Any:
        if project.conn is None:
            raise Exception("Project is not connected yet")
        return project.conn.DBName()

    def toUnicode(self, val: str, format: str) -> str:
        return val.encode(format).decode("utf-8", "replace")

    def fromUnicode(self, val, format) -> Any:
        return val.encode("utf-8").decode(format, "replace")

    def Mr_Proper(self) -> None:
        if project.conn is None:
            raise Exception("Project is not connected yet")
        project.conn.Mr_Proper()

    def installPrefix(self) -> str:
        from pineboolib.core.utils.utils_base import filedir

        return filedir("..")

    def __getattr__(self, fun_: str) -> Callable:
        if self.sys_widget is None:
            if "sys" in project.actions:
                self.sys_widget = project.actions["sys"].load().widget
            else:
                logger.warn("No action found for 'sys'")
        return getattr(self.sys_widget, fun_, None)

    def installACL(self, idacl) -> None:
        # FIXME: Add ACL later
        # acl_ = project.acl()
        # acl_ = None
        # if acl_:
        #     acl_.installACL(idacl)
        pass

    def version(self) -> str:
        return str(project.version)

    def processEvents(self) -> None:
        if not project._DGI:
            raise Exception("project._DGI is empty!")

        return project.DGI.processEvents()

    def write(self, encode_: str, dir_: str, contenido: str) -> None:
        import codecs

        b_ = contenido.encode()
        f = codecs.open(dir_, encoding=encode_, mode="wb+")
        f.write(b_.decode(encode_))
        f.seek(0)
        f.close()

    def cleanupMetaData(self, connName="default") -> None:
        if project.conn is None:
            raise Exception("Project is not connected yet")
        project.conn.useConn(connName).manager().cleanupMetaData()

    def updateAreas(self) -> None:
        from pineboolib.fllegacy.flapplication import aqApp

        aqApp.initToolBox()

    def reinit(self) -> None:
        from pineboolib.fllegacy.flapplication import aqApp

        aqApp.reinit()

    def setCaptionMainWidget(self, t) -> None:
        from pineboolib.fllegacy.flapplication import aqApp

        aqApp.setCaptionMainWidget(t)

    def nameDriver(self, connName="default") -> Any:
        if project.conn is None:
            raise Exception("Project is not connected yet")
        return project.conn.useConn(connName).driverName()

    def nameHost(self, connName="default") -> Any:
        if project.conn is None:
            raise Exception("Project is not connected yet")
        return project.conn.useConn(connName).host()

    def addDatabase(self, *args) -> bool:
        # def addDatabase(self, driver_name = None, db_name = None, db_user_name = None,
        #                 db_password = None, db_host = None, db_port = None, connName="default"):
        if project.conn is None:
            raise Exception("Project is not connected yet")
        if len(args) == 1:
            conn_db = project.conn.useConn(args[0])
            if not conn_db.isOpen():
                if conn_db.driverName_ and conn_db.driverSql and conn_db.driverSql.loadDriver(conn_db.driverName_):
                    conn_db.driver_ = conn_db.driverSql.driver()
                    conn_db.conn = conn_db.conectar(
                        project.conn.db_name, project.conn.db_host, project.conn.db_port, project.conn.db_userName, project.conn.db_password
                    )
                    if conn_db.conn is False:
                        return False

                    conn_db._isOpen = True

        else:
            conn_db = project.conn.useConn(args[6])
            if not conn_db.isOpen():
                if conn_db.driverSql is None:
                    raise Exception("driverSql not loaded!")
                conn_db.driverName_ = conn_db.driverSql.aliasToName(args[0])
                if conn_db.driverName_ and conn_db.driverSql.loadDriver(conn_db.driverName_):
                    conn_db.conn = conn_db.conectar(args[1], args[4], args[5], args[2], args[3])

                    if conn_db.conn is False:
                        return False

                    # conn_db.driver().db_ = conn_db
                    conn_db._isOpen = True
                    # conn_db._dbAux = conn_db

        return True

    def removeDatabase(self, connName="default") -> Any:
        if project.conn is None:
            raise Exception("Project is not connected yet")
        return project.conn.useConn(connName).removeConn(connName)

    def idSession(self) -> Any:
        # FIXME: Code copied from flapplication.aqApp
        return self.time_user_.toString(QtCore.Qt.ISODate)
