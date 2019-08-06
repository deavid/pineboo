"""
SysBaseType for QSA.

Will be inherited at fllegacy.
"""

import platform
import traceback
import ast

from typing import Any, Dict, Optional, List

from PyQt5 import QtCore

from PyQt5.QtWidgets import QMessageBox, QApplication

from pineboolib.core.settings import config
from pineboolib.core import decorators
from pineboolib.core.utils.utils_base import ustr, filedir
from pineboolib.core.utils import logging

from pineboolib.application import project
from pineboolib.application import connections

from pineboolib.qt3_widgets.process import Process

logger = logging.getLogger("fllegacy.systype")


class SysBaseType(object):
    """
    Obtain useful data from the application.
    """

    time_user_ = QtCore.QDateTime.currentDateTime()

    @classmethod
    def nameUser(self) -> str:
        """Get current database user."""
        ret_ = None
        if project.conn is None:
            raise Exception("Project is not connected yet")

        if project.DGI.use_alternative_credentials():
            ret_ = project.DGI.get_nameuser()
        else:
            ret_ = project.conn.user()

        return ret_ or ""

    @classmethod
    def interactiveGUI(self) -> str:
        """Check if running in GUI mode."""
        return project.DGI.interactiveGUI()

    @classmethod
    def isUserBuild(self) -> bool:
        """Check if this build is an user build."""
        return self.version().upper().find("USER") > -1

    @classmethod
    def isDeveloperBuild(self) -> bool:
        """Check if this build is a developer build."""
        return self.version().upper().find("DEVELOPER") > -1

    @classmethod
    def isNebulaBuild(self) -> bool:
        """Check if this build is a nebula build."""
        return self.version().upper().find("NEBULA") > -1

    @classmethod
    def isDebuggerMode(self) -> bool:
        """Check if running in debugger mode."""
        return bool(config.value("application/isDebuggerMode", False))

    @classmethod
    @decorators.NotImplementedWarn
    def isCloudMode(self) -> bool:
        """Check if running on cloud mode."""
        return False

    @classmethod
    def isDebuggerEnabled(self) -> bool:
        """Check if this debugger is on."""
        return bool(config.value("application/dbadmin_enabled", False))

    @classmethod
    def isQuickBuild(self) -> bool:
        """Check if this build is a Quick build."""
        return not self.isDebuggerEnabled()

    @classmethod
    def isLoadedModule(self, modulename: str) -> bool:
        """Check if a module has been loaded."""
        if project.conn is None:
            raise Exception("Project is not connected yet")
        return modulename in project.conn.managerModules().listAllIdModules()

    @classmethod
    def osName(self) -> str:
        """
        Get operating system name.

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

    @classmethod
    def nameBD(self) -> Any:
        """Get database name."""
        if project.conn is None:
            raise Exception("Project is not connected yet")
        return project.conn.DBName()

    @classmethod
    def toUnicode(self, val: str, format: str) -> str:
        """Convert string to unicode."""
        return val.encode(format).decode("utf-8", "replace")

    @classmethod
    def fromUnicode(self, val, format) -> Any:
        """Convert from unicode to string."""
        return val.encode("utf-8").decode(format, "replace")

    @classmethod
    def Mr_Proper(self) -> None:
        """Cleanup database like Mr. Proper."""
        if project.conn is None:
            raise Exception("Project is not connected yet")
        project.conn.Mr_Proper()

    @classmethod
    def installPrefix(self) -> str:
        """Get folder where app is installed."""
        return filedir("..")

    @classmethod
    def version(self) -> str:
        """Get version number as string."""
        return str(project.version)

    @classmethod
    def processEvents(self) -> None:
        """Process event loop."""
        if not project._DGI:
            raise Exception("project._DGI is empty!")

        return project.DGI.processEvents()

    @classmethod
    def write(self, encode_: str, dir_: str, contenido: str) -> None:
        """Write to file."""
        from pineboolib.application.types import File

        fileISO = File(dir_, encode_)
        fileISO.write(contenido)
        fileISO.close()

    @classmethod
    def cleanupMetaData(self, connName="default") -> None:
        """Clean up metadata."""
        if project.conn is None:
            raise Exception("Project is not connected yet")
        project.conn.useConn(connName).manager().cleanupMetaData()

    @classmethod
    def nameDriver(self, connName="default") -> Any:
        """Get driver name."""
        if project.conn is None:
            raise Exception("Project is not connected yet")
        return project.conn.useConn(connName).driverName()

    @classmethod
    def nameHost(self, connName="default") -> Any:
        """Get database host name."""
        if project.conn is None:
            raise Exception("Project is not connected yet")
        return project.conn.useConn(connName).host()

    @classmethod
    def addDatabase(self, *args) -> bool:
        """Add a new database."""
        # def addDatabase(self, driver_name = None, db_name = None, db_user_name = None,
        #                 db_password = None, db_host = None, db_port = None, connName="default"):
        if project.conn is None:
            raise Exception("Project is not connected yet")
        if len(args) == 1:
            conn_db = project.conn.useConn(args[0])
            if not conn_db.isOpen():
                if (
                    conn_db.driverName_
                    and conn_db.driverSql
                    and conn_db.driverSql.loadDriver(conn_db.driverName_)
                ):
                    conn_db.driver_ = conn_db.driverSql.driver()
                    conn_db.conn = conn_db.conectar(
                        project.conn.db_name,
                        project.conn.db_host,
                        project.conn.db_port,
                        project.conn.db_userName,
                        project.conn.db_password,
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

    @classmethod
    def removeDatabase(self, connName="default") -> Any:
        """Remove a database."""
        if project.conn is None:
            raise Exception("Project is not connected yet")
        project.conn.useConn(connName)._isOpen = False
        return project.conn.useConn(connName).removeConn(connName)

    @classmethod
    def idSession(self) -> str:
        """Get Session ID."""
        # FIXME: Code copied from flapplication.aqApp
        return self.time_user_.toString(QtCore.Qt.ISODate)

    @classmethod
    def reportChanges(self, changes=None):
        """Create a report for project changes."""
        ret = u""
        # DEBUG:: FOR-IN: ['key', 'changes']
        for key in changes:
            if key == u"size":
                continue
            chg = changes[key].split("@")
            ret += "Nombre: %s \n" % chg[0]
            ret += "Estado: %s \n" % chg[1]
            ret += "ShaOldTxt: %s \n" % chg[2]
            ret += "ShaNewTxt: %s \n" % chg[4]
            ret += u"###########################################\n"

        return ret

    @classmethod
    def diffXmlFilesDef(self, xmlOld=None, xmlNew=None):
        """Create a Diff for XML."""
        arrOld = self.filesDefToArray(xmlOld)
        arrNew = self.filesDefToArray(xmlNew)
        ret: Dict[str, Any] = {}
        size = 0
        # DEBUG:: FOR-IN: ['key', 'arrOld']
        for key in arrOld:
            if key not in arrNew:
                info = [key, "del", arrOld[key]["shatext"], arrOld[key]["shabinary"], "", ""]
                ret[key] = "@".join(info)
                size += 1
        # DEBUG:: FOR-IN: ['key', 'arrNew']

        for key in arrNew:
            if key not in arrOld:
                info = [key, "new", "", "", arrNew[key]["shatext"], arrNew[key]["shabinary"]]
                ret[key] = "@".join(info)
                size += 1
            else:
                if (
                    arrNew[key]["shatext"] != arrOld[key]["shatext"]
                    or arrNew[key]["shabinary"] != arrOld[key]["shabinary"]
                ):
                    info = [
                        key,
                        "mod",
                        arrOld[key]["shatext"],
                        arrOld[key]["shabinary"],
                        arrNew[key]["shatext"],
                        arrNew[key]["shabinary"],
                    ]
                    ret[key] = "@".join(info)
                    size += 1

        ret["size"] = size
        return ret

    @classmethod
    def filesDefToArray(self, xml=None):
        """Convert Module MOD xml to array."""
        root = xml.firstChild()
        files = root.childNodes()
        ret = {}
        i = 0
        while_pass = True
        while i < len(files):
            if not while_pass:
                i += 1
                while_pass = True
                continue
            while_pass = False
            it = files.item(i)
            fil = {
                "id": it.namedItem(u"name").toElement().text(),
                "module": it.namedItem(u"module").toElement().text(),
                "text": it.namedItem(u"text").toElement().text(),
                "shatext": it.namedItem(u"shatext").toElement().text(),
                "binary": it.namedItem(u"binary").toElement().text(),
                "shabinary": it.namedItem(u"shabinary").toElement().text(),
            }
            if len(fil["id"]) == 0:
                continue
            ret[fil["id"]] = fil
            i += 1
            while_pass = True
            try:
                i < len(files)
            except Exception:
                break

        return ret

    @classmethod
    def textPacking(self, ext=None):
        """Determine if file is text."""
        return (
            ext.endswith(".ui")
            or ext.endswith(".qry")
            or ext.endswith(".kut")
            or ext.endswith(".jrxml")
            or ext.endswith(".ar")
            or ext.endswith(".mtd")
            or ext.endswith(".ts")
            or ext.endswith(".qs")
            or ext.endswith(".qs.py")
            or ext.endswith(".xml")
            or ext.endswith(".xpm")
            or ext.endswith(".svg")
        )

    @classmethod
    def binaryPacking(self, ext=None):
        """Determine if file is binary."""
        return ext.endswith(u".qs")

    @classmethod
    def infoMsgBox(self, msg=None):
        """Show information message box."""
        msg = ustr(msg)
        msg += u"\n"
        if self.interactiveGUI():
            QMessageBox.information(QApplication.focusWidget(), "Eneboo", msg, QMessageBox.Ok)
        else:
            logger.warning(ustr(u"INFO: ", msg))

    @classmethod
    def warnMsgBox(self, msg=None):
        """Show Warning message box."""
        msg = ustr(msg)
        msg += u"\n"
        if self.interactiveGUI():
            QMessageBox.warning(QApplication.focusWidget(), "Eneboo", msg, QMessageBox.Ok)
        else:
            logger.warning(ustr(u"WARN: ", msg))

    @classmethod
    def errorMsgBox(self, msg=None):
        """Show error message box."""
        msg = ustr(msg)
        msg += u"\n"
        if self.interactiveGUI():
            QMessageBox.critical(QApplication.focusWidget(), "Eneboo", msg, QMessageBox.Ok)
        else:
            logger.warning(ustr(u"ERROR: ", msg))

    @classmethod
    def translate(self, text: str) -> str:
        """Translate text."""
        return text

    @classmethod
    def _warnHtmlPopup(self, html: str, options: List) -> None:
        """Show a fancy html popup."""
        raise Exception("not implemented.")

    @classmethod
    def infoPopup(self, msg: Optional[str] = None):
        """Show information popup."""
        msg = ustr(msg)
        caption = self.translate(u"AbanQ Información")
        msg = msg.replace("\n", "<br>")
        msgHtml = ustr(
            u'<img source="about.png" align="right">',
            u"<b><u>",
            caption,
            u"</u></b><br><br>",
            msg,
            u"<br>",
        )
        self._warnHtmlPopup(msgHtml, [])

    @classmethod
    def warnPopup(self, msg=None):
        """Show warning popup."""
        msg = ustr(msg)
        msg = msg.replace("\n", "<br>")
        caption = self.translate(u"AbanQ Aviso")
        msgHtml = ustr(
            u'<img source="bug.png" align="right">',
            u"<b><u>",
            caption,
            u"</u></b><br><br>",
            msg,
            u"<br>",
        )
        self._warnHtmlPopup(msgHtml, [])

    @classmethod
    def errorPopup(self, msg=None):
        """Show error popup."""
        msg = ustr(msg)
        msg = msg.replace("\n", "<br>")
        caption = self.translate(u"AbanQ Error")
        msgHtml = ustr(
            u'<img source="remove.png" align="right">',
            u"<b><u>",
            caption,
            u"</u></b><br><br>",
            msg,
            u"<br>",
        )
        self._warnHtmlPopup(msgHtml, [])

    @classmethod
    def trTagText(self, tagText=None):
        """Process QT_TRANSLATE_NOOP tags."""
        if not tagText.startswith(u"QT_TRANSLATE_NOOP"):
            return tagText
        txt = tagText[len("QT_TRANSLATE_NOOP") + 1 :]
        txt = "[%s]" % txt[0 : len(txt) - 1]
        arr = ast.literal_eval(txt)  # FIXME: Don't use "ast.literal_eval"
        return self.translate(arr[0], arr[1])

    @classmethod
    def updatePineboo(self):
        """Execute auto-updater."""
        QMessageBox.warning(
            QApplication.focusWidget(),
            "Pineboo",
            self.translate(u"Funcionalidad no soportada aún en Pineboo."),
            QMessageBox.Ok,
        )
        return

    @classmethod
    def setObjText(self, container=None, component=None, value=None):
        """Set text to random widget."""
        c = self.testObj(container, component)
        if c is None:
            return False
        clase = u"FLFieldDB" if hasattr(c, "editor_") else c.__class__.__name__

        if clase == u"QPushButton":
            pass
        elif clase == u"QToolButton":
            pass
        elif clase == u"QLabel":
            self.runObjMethod(container, component, u"text", value)
        elif clase == u"FLFieldDB":
            self.runObjMethod(container, component, u"setValue", value)
        else:
            return False
        return True

    @classmethod
    def disableObj(self, container=None, component=None):
        """Disable random widget."""
        c = self.testObj(container, component)
        if not c:
            return False
        clase = (
            "FLFieldDB"
            if isinstance(c, project.DGI.FLFieldDB)
            else "FLTableDB"
            if isinstance(c, project.DGI.FLTableDB)
            else c.className()
        )
        if clase in ["QToolButton", "QPushButton"]:
            self.runObjMethod(container, component, u"setEnabled", False)
        elif clase == u"FLFieldDB":
            self.runObjMethod(container, component, u"setDisabled", True)
        else:
            return False

        return True

    @classmethod
    def enableObj(self, container=None, component=None):
        """Enable random widget."""
        c = self.testObj(container, component)
        if not c:
            return False
        clase = (
            u"FLFieldDB"
            if (u"editor" in c)
            else ((u"FLTableDB" if (u"tableName" in c) else c.className()))
        )
        if clase == u"QPushButton":
            pass
        elif clase == u"QToolButton":
            self.runObjMethod(container, component, u"setEnabled", True)
        elif clase == u"FLFieldDB":
            self.runObjMethod(container, component, u"setDisabled", False)
        else:
            return False
        return True

    @classmethod
    def filterObj(self, container=None, component=None, filter=None):
        """Apply filter to random widget."""
        c = self.testObj(container, component)
        if not c:
            return False
        clase = (
            u"FLFieldDB"
            if (u"editor" in c)
            else ((u"FLTableDB" if (u"tableName" in c) else c.className()))
        )
        if clase == u"FLTableDB":
            pass
        elif clase == u"FLFieldDB":
            self.runObjMethod(container, component, u"setFilter", filter)
        else:
            return False
        return True

    @classmethod
    def testObj(self, container=None, component=None):
        """Test if object does exist."""
        if not container or container is None:
            return False
        c = container.child(component)
        if not c:
            logger.warning(ustr(component, u" no existe"))
            return False
        return c

    @classmethod
    def testAndRun(self, container=None, component=None, method=None, param=None):
        """Test and execute object."""
        c = self.testObj(container, component)
        if not c:
            return False
        if not self.runObjMethod(container, component, method, param):
            return False
        return True

    @classmethod
    def runObjMethod(self, container=None, component=None, method=None, param=None):
        """Execute method from object."""
        c = container.child(component)
        m = getattr(c, method, None)
        if m is not None:
            m(param)
        else:
            logger.warning(ustr(method, u" no existe"))

        return True

    @classmethod
    def connectSS(self, ssSender=None, ssSignal=None, ssReceiver=None, ssSlot=None):
        """Connect signal to slot."""
        if not ssSender:
            return False
        connections.connect(ssSender, ssSignal, ssReceiver, ssSlot)
        return True

    @classmethod
    def openUrl(self, url=None):
        """Open given URL in a browser."""
        if not url:
            return False
        os_name = self.osName()
        if os_name == "LINUX":
            if self.launchCommand([u"xdg-open", url]):
                return True
            if self.launchCommand([u"gnome-open", url]):
                return True
            if self.launchCommand([u"kfmclient openURL", url]):
                return True
            if self.launchCommand([u"kfmclient exec", url]):
                return True
            if self.launchCommand([u"firefox", url]):
                return True
            if self.launchCommand([u"mozilla", url]):
                return True
            if self.launchCommand([u"opera", url]):
                return True
            if self.launchCommand([u"google-chrome", url]):
                return True
            return False

        if os_name == u"WIN32":
            if url.startswith(u"mailto"):
                url = url.replace("&", "^&")
            return self.launchCommand([u"cmd.exe", u"/C", u"start", u"", url])

        if os_name == u"MACX":
            return self.launchCommand([u"open", url])

        return False

    @classmethod
    def launchCommand(self, comando):
        """Execute a program."""
        try:
            Process.execute(comando)
            return True
        except Exception:
            e = traceback.format_exc()
            logger.error(e)
            return False
