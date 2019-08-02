"""
SysBaseType for QSA.

Will be inherited at fllegacy.
"""

import platform
import traceback
import codecs
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
    time_user_ = QtCore.QDateTime.currentDateTime()

    @classmethod
    def nameUser(self) -> str:
        ret_ = None
        if project.conn is None:
            raise Exception("Project is not connected yet")

        if project.DGI.use_alternative_credentials():
            ret_ = project.DGI.get_nameuser()
        else:
            ret_ = project.conn.user()

        return ret_

    @classmethod
    def interactiveGUI(self) -> str:
        return project.DGI.self.interactiveGUI()

    @classmethod
    def isUserBuild(self) -> bool:
        return self.version().upper().find("USER") > -1

    @classmethod
    def isDeveloperBuild(self) -> bool:
        return self.version().upper().find("DEVELOPER") > -1

    @classmethod
    def isNebulaBuild(self) -> bool:
        return self.version().upper().find("NEBULA") > -1

    @classmethod
    def isDebuggerMode(self) -> bool:
        return bool(config.value("application/isDebuggerMode", False))

    @classmethod
    @decorators.NotImplementedWarn
    def isCloudMode(self) -> bool:
        return False

    @classmethod
    def isDebuggerEnabled(self) -> bool:
        return bool(config.value("application/dbadmin_enabled", False))

    @classmethod
    def isQuickBuild(self) -> bool:
        return not self.isDebuggerEnabled()

    @classmethod
    def isLoadedModule(self, modulename: str) -> bool:
        if project.conn is None:
            raise Exception("Project is not connected yet")
        return modulename in project.conn.managerModules().listAllIdModules()

    @classmethod
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

    @classmethod
    def nameBD(self) -> Any:
        if project.conn is None:
            raise Exception("Project is not connected yet")
        return project.conn.DBName()

    @classmethod
    def toUnicode(self, val: str, format: str) -> str:
        return val.encode(format).decode("utf-8", "replace")

    @classmethod
    def fromUnicode(self, val, format) -> Any:
        return val.encode("utf-8").decode(format, "replace")

    @classmethod
    def Mr_Proper(self) -> None:
        if project.conn is None:
            raise Exception("Project is not connected yet")
        project.conn.Mr_Proper()

    @classmethod
    def installPrefix(self) -> str:

        return filedir("..")

    @classmethod
    def version(self) -> str:
        return str(project.version)

    @classmethod
    def processEvents(self) -> None:
        if not project._DGI:
            raise Exception("project._DGI is empty!")

        return project.DGI.processEvents()

    @classmethod
    def write(self, encode_: str, dir_: str, contenido: str) -> None:

        b_ = contenido.encode()
        f = codecs.open(dir_, encoding=encode_, mode="wb+")
        f.write(b_.decode(encode_))
        f.seek(0)
        f.close()

    @classmethod
    def cleanupMetaData(self, connName="default") -> None:
        if project.conn is None:
            raise Exception("Project is not connected yet")
        project.conn.useConn(connName).manager().cleanupMetaData()

    @classmethod
    def nameDriver(self, connName="default") -> Any:
        if project.conn is None:
            raise Exception("Project is not connected yet")
        return project.conn.useConn(connName).driverName()

    @classmethod
    def nameHost(self, connName="default") -> Any:
        if project.conn is None:
            raise Exception("Project is not connected yet")
        return project.conn.useConn(connName).host()

    @classmethod
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

    @classmethod
    def removeDatabase(self, connName="default") -> Any:
        if project.conn is None:
            raise Exception("Project is not connected yet")
        return project.conn.useConn(connName).removeConn(connName)

    @classmethod
    def idSession(self) -> str:
        # FIXME: Code copied from flapplication.aqApp
        return self.time_user_.toString(QtCore.Qt.ISODate)

    @classmethod
    def reportChanges(self, changes=None):
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
                if arrNew[key]["shatext"] != arrOld[key]["shatext"] or arrNew[key]["shabinary"] != arrOld[key]["shabinary"]:
                    info = [key, "mod", arrOld[key]["shatext"], arrOld[key]["shabinary"], arrNew[key]["shatext"], arrNew[key]["shabinary"]]
                    ret[key] = "@".join(info)
                    size += 1

        ret["size"] = size
        return ret

    @classmethod
    def filesDefToArray(self, xml=None):
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
        return (
            ext.endswith(u".ui")
            or ext.endswith(u".qry")
            or ext.endswith(u".kut")
            or ext.endswith(u".jrxml")
            or ext.endswith(u".ar")
            or ext.endswith(u".mtd")
            or ext.endswith(u".ts")
            or ext.endswith(u".qs")
            or ext.endswith(".qs.py")
            or ext.endswith(u".xml")
            or ext.endswith(u".xpm")
            or ext.endswith(u".svg")
        )

    @classmethod
    def binaryPacking(self, ext=None):
        return ext.endswith(u".qs")

    @classmethod
    def infoMsgBox(self, msg=None):
        msg = ustr(msg)
        msg += u"\n"
        if self.interactiveGUI():
            QMessageBox.information(QApplication.focusWidget(), "Eneboo", msg, QMessageBox.Ok)
        else:
            logger.warning(ustr(u"INFO: ", msg))

    @classmethod
    def warnMsgBox(self, msg=None):
        msg = ustr(msg)
        msg += u"\n"
        if self.interactiveGUI():
            QMessageBox.warning(QApplication.focusWidget(), "Eneboo", msg, QMessageBox.Ok)
        else:
            logger.warning(ustr(u"WARN: ", msg))

    @classmethod
    def errorMsgBox(self, msg=None):
        msg = ustr(msg)
        msg += u"\n"
        if self.interactiveGUI():
            QMessageBox.critical(QApplication.focusWidget(), "Eneboo", msg, QMessageBox.Ok)
        else:
            logger.warning(ustr(u"ERROR: ", msg))

    @classmethod
    def translate(self, text: str) -> str:
        return text

    @classmethod
    def _warnHtmlPopup(self, html: str, options: List) -> None:
        raise Exception("not implemented.")

    @classmethod
    def infoPopup(self, msg: Optional[str] = None):
        msg = ustr(msg)
        caption = self.translate(u"AbanQ Información")
        msg = msg.replace("\n", "<br>")
        msgHtml = ustr(u'<img source="about.png" align="right">', u"<b><u>", caption, u"</u></b><br><br>", msg, u"<br>")
        self._warnHtmlPopup(msgHtml, [])

    @classmethod
    def warnPopup(self, msg=None):
        msg = ustr(msg)
        msg = msg.replace("\n", "<br>")
        caption = self.translate(u"AbanQ Aviso")
        msgHtml = ustr(u'<img source="bug.png" align="right">', u"<b><u>", caption, u"</u></b><br><br>", msg, u"<br>")
        self._warnHtmlPopup(msgHtml, [])

    @classmethod
    def errorPopup(self, msg=None):
        msg = ustr(msg)
        msg = msg.replace("\n", "<br>")
        caption = self.translate(u"AbanQ Error")
        msgHtml = ustr(u'<img source="remove.png" align="right">', u"<b><u>", caption, u"</u></b><br><br>", msg, u"<br>")
        self._warnHtmlPopup(msgHtml, [])

    @classmethod
    def trTagText(self, tagText=None):
        if not tagText.startswith(u"QT_TRANSLATE_NOOP"):
            return tagText
        txt = tagText[len("QT_TRANSLATE_NOOP") + 1 :]
        txt = "[%s]" % txt[0 : len(txt) - 1]
        arr = ast.literal_eval(txt)  # FIXME: Don't use "ast.literal_eval"
        return self.translate(arr[0], arr[1])

    @classmethod
    def updatePineboo(self):
        QMessageBox.warning(
            QApplication.focusWidget(), "Pineboo", self.translate(u"Funcionalidad no soportada aún en Pineboo."), QMessageBox.Ok
        )
        return

    @classmethod
    def setObjText(self, container=None, component=None, value=None):
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
        c = self.testObj(container, component)
        if not c:
            return False
        clase = (
            "FLFieldDB" if isinstance(c, project.DGI.FLFieldDB) else "FLTableDB" if isinstance(c, project.DGI.FLTableDB) else c.className()
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
        c = self.testObj(container, component)
        if not c:
            return False
        clase = u"FLFieldDB" if (u"editor" in c) else ((u"FLTableDB" if (u"tableName" in c) else c.className()))
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
        c = self.testObj(container, component)
        if not c:
            return False
        clase = u"FLFieldDB" if (u"editor" in c) else ((u"FLTableDB" if (u"tableName" in c) else c.className()))
        if clase == u"FLTableDB":
            pass
        elif clase == u"FLFieldDB":
            self.runObjMethod(container, component, u"setFilter", filter)
        else:
            return False
        return True

    @classmethod
    def testObj(self, container=None, component=None):
        if not container or container is None:
            return False
        c = container.child(component)
        if not c:
            logger.warning(ustr(component, u" no existe"))
            return False
        return c

    @classmethod
    def testAndRun(self, container=None, component=None, method=None, param=None):
        c = self.testObj(container, component)
        if not c:
            return False
        if not self.runObjMethod(container, component, method, param):
            return False
        return True

    @classmethod
    def runObjMethod(self, container=None, component=None, method=None, param=None):
        c = container.child(component)
        m = getattr(c, method, None)
        if m is not None:
            m(param)
        else:
            logger.warning(ustr(method, u" no existe"))

        return True

    @classmethod
    def connectSS(self, ssSender=None, ssSignal=None, ssReceiver=None, ssSlot=None):
        if not ssSender:
            return False
        connections.connect(ssSender, ssSignal, ssReceiver, ssSlot)
        return True

    @classmethod
    def openUrl(self, url=None):
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
        try:
            Process.execute(comando)
            return True
        except Exception:
            e = traceback.format_exc()
            logger.error(e)
            return False
