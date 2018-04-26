# -*- coding: utf-8 -*-
import re
import os.path
import weakref
import logging
import traceback
import math
from PyQt5.Qt import qApp
from PyQt5 import QtCore, QtWidgets
from PyQt5.Qt import QDateEdit


import pineboolib
from pineboolib import decorators
from pineboolib.utils import filedir
from pineboolib.fllegacy.FLUtil import FLUtil
from pineboolib.fllegacy.AQObjects import AQSql as AQSql_Legacy
from pineboolib.fllegacy.FLSqlCursor import FLSqlCursor


logger = logging.getLogger(__name__)

AQSql = AQSql_Legacy
AQUtil = FLUtil()  # A falta de crear AQUtil, usamos la versión anterior
util = FLUtil()  # <- para cuando QS erróneo usa util sin definirla

Insert = 0
Edit = 1
Del = 2
Browse = 3


class File:

    @classmethod
    def exists(cls, name):
        return os.path.isfile(name)


class FileDialog(QtWidgets.QFileDialog):

    # def __init__(self):
    #    super(FileDialog, self).__init__()

    def getOpenFileName(*args):
        obj = None
        parent = QtWidgets.QApplication.activeModalWidget()
        if len(args) == 1:
            obj = QtWidgets.QFileDialog.getOpenFileName(parent, str(args[0]))
        elif len(args) == 2:
            obj = QtWidgets.QFileDialog.getOpenFileName(parent, str(args[0]), str(args[1]))
        elif len(args) == 3:
            obj = QtWidgets.QFileDialog.getOpenFileName(parent, str(args[0]), str(args[1]), str(args[2]))
        elif len(args) == 4:
            obj = QtWidgets.QFileDialog.getOpenFileName(parent, str(args[0]), str(args[1]), str(args[2]), str(args[3]))

        if obj is None:
            return None

        return obj[0]

    def getExistingDirectory(basedir, caption=None):
        if basedir == False:
            basedir = filedir("..")
        return "%s/" % QtWidgets.QFileDialog.getExistingDirectory(None, caption, basedir)


class Math(object):

    def abs(x):
        return math.fabs(x)

    def ceil(x):
        return math.ceil(x)

    def floor(x):
        return math.floor(x)

    def pow(x, y):
        return math.pow(x, y)


def parseFloat(x):
    if x is None:
        return 0
    return float(x)


"""
class parseString(object):

    obj_ = None
    length = None

    def __init__(self, objeto):
        try:
            self.obj_ = objeto.toString()
        except Exception:
            self.obj_ = str(objeto)

        self.length = len(self.obj_)

    def __str__(self):
        return self.obj_

    def __getitem__(self, key):
        return self.obj_.__getitem__(key)



    def charAt(self, pos):
        try:
            return self.obj_[pos]
        except Exception:
            return False

    def substring(self, ini, fin):
        return self.obj_[ini: fin]

 """


def parseString(objeto):
    try:
        return objeto.toString()
    except Exception:
        return str(objeto)


def parseInt(x):
    if x is None:
        return 0
    return int(x)


def isNaN(x):
    if not x:
        return True

    try:
        float(x)
        return False
    except ValueError:
        return True


# TODO: separar en otro fichero de utilidades
def ustr(*t1):

    return "".join([ustr1(t) for t in t1])


def ustr1(t):
    if isinstance(t, str):
        return t

    if isinstance(t, float):
        try:
            t = int(t)
        except Exception:
            pass

    # if isinstance(t, QtCore.QString): return str(t)
    if isinstance(t, str):
        return str(t, "UTF-8")
    try:
        return str(t)
    except Exception as e:
        logger.exception("ERROR Coercing to string: %s", repr(t))
        return None


def debug(txt):
    logger.message("---> " + ustr(txt))


class aqApp(object):

    def db():
        return pineboolib.project.conn


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

    def nameBD(self):
        return pineboolib.project.conn.DBName()

    def setCaptionMainWidget(self, value):
        self.mainWidget().setWindowTitle("Pineboo - %s" % value)
        pass

    def toUnicode(self, text, format):
        return u"%s" % text

    def mainWidget(self):
        if pineboolib.project._DGI.localDesktop():
            return pineboolib.project.main_window.ui
        else:
            return None

    def Mr_Proper(self):
        pineboolib.project.conn.Mr_Proper()

    def installPrefix(self):
        return filedir("..")

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

    @decorators.NotImplementedWarn
    def reinit(self):
        pass

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


class ProxySlot:
    PROXY_FUNCTIONS = {}

    def __init__(self, remote_fn, receiver, slot):
        self.key = "%r.%r->%r" % (remote_fn, receiver, slot)
        if self.key not in self.PROXY_FUNCTIONS:
            weak_fn = weakref.WeakMethod(remote_fn)
            weak_receiver = weakref.ref(receiver)
            self.PROXY_FUNCTIONS[self.key] = proxy_fn(weak_fn, weak_receiver, slot)
        self.proxy_function = self.PROXY_FUNCTIONS[self.key]

    def getProxyFn(self):
        return self.proxy_function


def proxy_fn(wf, wr, slot):
    def fn(*args, **kwargs):
        f = wf()
        if not f:
            return None
        r = wr()
        if not r:
            return None

        # Apaño para conectar los clicked()
        if args == (False,):
            return f()

        return f(*args, **kwargs)
    return fn


def connect(sender, signal, receiver, slot, caller=None):
    if caller is not None:
        logger.debug("* * * Connect::", caller, sender, signal, receiver, slot)
    else:
        logger.debug("? ? ? Connect::", sender, signal, receiver, slot)
    signal_slot = solve_connection(sender, signal, receiver, slot)
    if not signal_slot:
        return False
    # http://pyqt.sourceforge.net/Docs/PyQt4/qt.html#ConnectionType-enum
    conntype = QtCore.Qt.QueuedConnection | QtCore.Qt.UniqueConnection
    signal, slot = signal_slot

    try:
        signal.connect(slot, type=conntype)
    except Exception:
        logger.exception("ERROR Connecting: %s %s %s %s", sender, signal, receiver, slot)
        return False

    return signal_slot


def disconnect(sender, signal, receiver, slot, caller=None):
    signal_slot = solve_connection(sender, signal, receiver, slot)
    if not signal_slot:
        return False
    signal, slot = signal_slot
    try:
        signal.disconnect(slot)
    except Exception:
        pass

    return signal_slot


def solve_connection(sender, signal, receiver, slot):
    if sender is None:
        logger.error("Connect Error:: %s %s %s %s", sender, signal, receiver, slot)
        return False

    m = re.search(r"^(\w+)\.(\w+)(\(.*\))?", slot)
    if slot.endswith("()"):
        slot = slot[:-2]

    if isinstance(sender, QDateEdit):
        if "valueChanged" in signal:
            signal = signal.replace("valueChanged", "dateChanged")

    if receiver.__class__.__name__ == "FormInternalObj" and slot == "accept":
        receiver = receiver.parent()

    remote_fn = getattr(receiver, slot, None)

    sg_name = re.sub(' *\(.*\)', '', signal)
    oSignal = getattr(sender, sg_name, None)
    if not oSignal and sender.__class__.__name__ == "FormInternalObj":
        oSignal = getattr(sender.parent(), sg_name, None)
    if not oSignal:
        logger.error("ERROR: No existe la señal %s para la clase %s", signal, sender.__class__.__name__)
        return

    if remote_fn:
        if receiver.__class__.__name__ == "FLFormSearchDB" and slot == "accept":
            return oSignal, remote_fn

        pS = ProxySlot(remote_fn, receiver, slot)
        proxyfn = pS.getProxyFn()
        return oSignal, proxyfn
    elif m:
        remote_obj = getattr(receiver, m.group(1), None)
        if remote_obj is None:
            raise AttributeError("Object %s not found on %s" %
                                 (remote_obj, str(receiver)))
        remote_fn = getattr(remote_obj, m.group(2), None)
        if remote_fn is None:
            raise AttributeError("Object %s not found on %s" %
                                 (remote_fn, remote_obj))
        return oSignal, remote_fn

    elif isinstance(receiver, QtCore.QObject):
        if isinstance(slot, str):
            oSlot = getattr(receiver, slot, None)
            if not oSlot:
                return False
        return oSignal, oSlot
    else:
        logger.error(
            "Al realizar connect %s:%s -> %s:%s ; "
            "el slot no se reconoce y el receptor no es QObject.",
            sender, signal, receiver, slot)
    return False


class Date(object):

    @classmethod
    def parse(cls, value):
        return QtCore.QDate.fromString(value)


QMessageBox = QtWidgets.QMessageBox


class MessageBox(QMessageBox):
    @classmethod
    def msgbox(cls, typename, text, button0, button1=None, button2=None, title=None, form=None):
        if title or form:
            logger.warn("MessageBox: Se intentó usar título y/o form, y no está implementado.")
        icon = QMessageBox.NoIcon
        title = "Message"
        if typename == "question":
            icon = QMessageBox.Question
            title = "Question"
        elif typename == "information":
            icon = QMessageBox.Information
            title = "Information"
        elif typename == "warning":
            icon = QMessageBox.Warning
            title = "Warning"
        elif typename == "critical":
            icon = QMessageBox.Critical
            title = "Critical"
        # title = unicode(title,"UTF-8")
        # text = unicode(text,"UTF-8")
        msg = QMessageBox(icon, str(title), str(text))
        msg.addButton(button0)
        if button1:
            msg.addButton(button1)
        if button2:
            msg.addButton(button2)
        return msg.exec_()

    @classmethod
    def question(cls, *args):
        return cls.msgbox("question", *args)

    @classmethod
    def information(cls, *args):
        return cls.msgbox("question", *args)

    @classmethod
    def warning(cls, *args):
        return cls.msgbox("warning", *args)

    @classmethod
    def critical(cls, *args):
        return cls.msgbox("critical", *args)


class Input(object):
    @classmethod
    def getText(cls, question, prevtxt, title):
        text, ok = QtWidgets.QInputDialog.getText(None, title,
                                                  question, QtWidgets.QLineEdit.Normal, prevtxt)
        if not ok:
            return None
        return text


def qsa_length(obj):
    lfn = getattr(obj, "length", None)
    if lfn:
        return lfn()
    return len(lfn)


def qsa_text(obj):
    try:
        return obj.text()
    except Exception:
        return obj.text


class qsa:
    parent = None
    loaded = False

    def __init__(self, parent):
        if isinstance(parent, str):
            parent = parent
        self.parent = parent
        self.loaded = True

    def __getattr__(self, k):
        if not self.loaded:
            return super(qsa, self).__getattr__(k)
        try:
            f = getattr(self.parent, k)
            if callable(f):
                return f()
            else:
                return f
        except Exception:
            if k == 'length':
                if self.parent:
                    return len(self.parent)
                else:
                    return 0
            logger.exception("qsa: error al intentar emular getattr de %s.%s", self.parent, k)

    def __setattr__(self, k, v):
        if not self.loaded:
            return super(qsa, self).__setattr__(k, v)
        try:
            if not self.parent:
                return
            f = getattr(self.parent, k)
            if callable(f):
                return f(v)
            else:
                return setattr(self.parent, k, v)
        except Exception:
            try:
                k = 'set' + k[0].upper() + k[1:]
                f = getattr(self.parent, k)
                if callable(f):
                    return f(v)
                else:
                    return setattr(self.parent, k, v)
            except Exception:
                logger.exception("qsa: error al intentar emular setattr de %s.%s = %s", self.parent, k, v)


# -------------------------- FORBIDDEN FRUIT ----------------------------------
# Esto de aquí es debido a que en Python3 decidieron que era mejor abandonar
# QString en favor de los strings de python3. Por lo tanto ahora el código QS
# llama a funciones de str en lugar de QString, y obviamente algunas no existen

# forbidden fruit tiene otra licencia (gplv3) y lo he incluído dentro del código
# por simplicidad de la instalación; pero sigue siendo gplv3, por lo que si
# alguien quiere hacer algo que en MIT se puede y en GPLv3 no, tendría que sacar
# ese código de allí. (como mínimo; no sé hasta donde llegaría legalmente)

# Para terminar, esto es una guarrada, pero es lo que hay. Si lo ves aquí, te
# gusta y lo quieres usar en tu proyecto, no, no es una bunea idea. Yo no tuve
# más opción. (Es más, si consigo parchear el python para que no imprima "left"
# quitaré esta librería demoníaca)

# from forbiddenfruit import curse
# curse(str, "left", lambda self, n: self[:n])
