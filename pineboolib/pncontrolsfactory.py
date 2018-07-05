# -*- coding: utf-8 -*-
import pineboolib
import logging
from pineboolib import decorators

logger = logging.getLogger("PNControlsFactory")

"""
Conjunto de controles usados en Pineboo. Estos son cargados desde el DGI seleccionado en el proyecto
"""

"""
Devuelve un objecto a partir de su nombre
@param name, Nombre del objecto a buscar
@return objecto o None si no existe el objeto buscado
"""


def resolveObject(name):
    ret_ = pineboolib.project.resolveDGIObject(name)
    return ret_


QComboBox = resolveObject("QComboBox")
QTable = resolveObject("QTable")
QLayoutWidget = resolveObject("QLayoutWidget")
QTabWidget = resolveObject("QTabWidget")
QGroupBox = resolveObject("QGroupBox")
QListView = resolveObject("QListView")
QPushButton = resolveObject("QPushButton")
QTextEdit = resolveObject("QTextEdit")
QLineEdit = resolveObject("QLineEdit")
QCheckBox = resolveObject("QCheckBox")
FLLineEdit = resolveObject("FLLineEdit")
FLTimeEdit = resolveObject("FLTimeEdit")
FLDateEdit = resolveObject("FLDateEdit")
FLPixmapView = resolveObject("FLPixmapView")


class SysType(object):
    def __init__(self):
        self._name_user = None

    def nameUser(self):
        return pineboolib.project.conn.user()

    def interactiveGUI(self):
        return "Pineboo"

    def isLoadedModule(self, modulename):
        return modulename in pineboolib.project.conn.managerModules().listAllIdModules()

    def translate(self, text):
        return text

    def osName(self):
        util = FLUtil()
        return util.getOS()

    def nameDB(self):
        return pineboolib.project.conn.DBName()

    def setCaptionMainWidget(self, value):
        self.mainWidget().setWindowTitle("Pineboo - %s" % value)
        pass

    def toUnicode(self, text, format):
        return u"%s" % text

    def mainWidget(self):
        if pineboolib.project._DGI.localDesktop():
            return pineboolib.project.main_window.ui_
        else:
            return None

    def Mr_Proper(self):
        pineboolib.project.conn.Mr_Proper()

    def installPrefix(self):
        return filedir("..")

    def installACL(self, idacl):
        acl_ = pineboolib.project.acl()
        if acl_:
            acl_.installACL(idacl)

    def __getattr__(self, name):
        obj = eval("sys.widget.%s" % name, pineboolib.qsaglobals.__dict__)
        if obj:
            return obj
        else:
            logger.warn("No se encuentra sys.%s", name)

    def version(self):
        return pineboolib.project.version

    def processEvents(self):
        qApp.processEvents()

    @decorators.BetaImplementation
    def reinit(self):
        self.processEvents()
        pineboolib.project.main_window.saveState()
        pineboolib.project.run()
        pineboolib.project.main_window.areas = []
        # FIXME: Limpiar el ui para no duplicar controles
        pineboolib.project.main_window.load()
        pineboolib.project.main_window.show()
        pineboolib.project.call("sys.iface._class_init()", [], None, True)

    def write(self, encode_, dir_, contenido):
        f = codecs.open(dir_, encoding=encode_, mode="w+")
        f.write(contenido)
        f.seek(0)
        f.close()

    def cleanupMetaData(self, connName="default"):
        pineboolib.project.conn.database(connName).manager().cleanupMetaData()

    def updateAreas(self):
        pineboolib.project.initToolBox()

    @decorators.NotImplementedWarn
    def isDebuggerMode(self):
        return False

    def nameDriver(self, connName="default"):
        return pineboolib.project.conn.database(connName).driverName()

    def addDatabase(self, connName="default"):
        return pineboolib.project.conn.useConn(connName)()

    def removeDatabase(self, connName="default"):
        return pineboolib.project.conn.removeConn(connName)

    def runTransaction(self, f, oParam):

        curT = FLSqlCursor("flfiles")
        curT.transaction(False)
        # gui = self.interactiveGUI()
        # if gui:
        #   AQS.Application_setOverrideCursor(AQS.WaitCursor);

        errorMsg = None
        try:
            valor = f(oParam)
            errorMsg = getattr(oParam, "errorMsg", None)
            if valor:
                curT.commit()
            else:
                curT.rollback()
                # if gui:
                #   AQS.Application_restoreOverrideCursor();
                if errorMsg is None:
                    self.warnMsgBox(self.translate(u"Error al ejecutar la función"))
                else:
                    self.warnMsgBox(errorMsg)
                return False

        except Exception:
            curT.rollback()
            # if gui:
            #   AQS.Application_restoreOverrideCursor();
            if errorMsg is None:
                self.warnMsgBox(self.translate(u"Error al ejecutar la función"))
            else:
                self.warnMsgBox(errorMsg)
            return False

        # if gui:
        #   AQS.Application_restoreOverrideCursor();
        return valor

    def infoMsgBox(self, msg):

        if not isinstance(msg, str):
            return
        msg += "\n"
        if self.interactiveGUI():
            MessageBox.information(msg, MessageBox.Ok, MessageBox.NoButton, MessageBox.NoButton, "Pineboo")
        else:
            print("INFO ", msg)

    def warnMsgBox(self, msg):

        if not isinstance(msg, str):
            return
        msg += "\n"
        if self.interactiveGUI():
            MessageBox.warning(msg, MessageBox.Ok, MessageBox.NoButton, MessageBox.NoButton, "Pineboo")
        else:
            print("WARN ", msg)

    def errorMsgBox(self, msg):

        if not isinstance(msg, str):
            return
        msg += "\n"
        if self.interactiveGUI():
            MessageBox.critical(msg, MessageBox.Ok, MessageBox.NoButton, MessageBox.NoButton, "Pineboo")
        else:
            print("ERROR ", msg)
