# encoding: UTF-8
from __future__ import print_function
from __future__ import unicode_literals
from builtins import str
from builtins import object
import re
from PyQt4 import QtCore, QtGui

import pineboolib
from pineboolib import flcontrols


def parseFloat(x): return float(x)

util = flcontrols.FLUtil() # <- para cuando QS erróneo usa util sin definirla

# TODO: separar en otro fichero de utilidades
def ustr(*t1):
    return "".join([ ustr1(t) for t in t1 ])

def ustr1(t):
    if isinstance(t, str): return t
    #if isinstance(t, QtCore.QString): return str(t)
    if isinstance(t, str): return str(t,"UTF-8")
    try:
        return str(t)
    except Exception as e:
        print("ERROR Coercing to string:", repr(t))
        print("ERROR", e.__class__.__name__, str(e))
        return None

def debug(txt):
    print("DEBUG:", ustr(txt))


def auto_qt_translate_text(text):
    if not isinstance(text,str): text=str(text)

    if isinstance(text,str):
        if text.find("QT_TRANSLATE") != -1:
            match = re.search(r"""QT_TRANSLATE\w*\(.+,["'](.+)["']\)""", text)
            if match: text = match.group(1)
    return text

class SysType(object):
    def __init__(self):
        self._name_user = "database_user"

    def nameUser(self): return self._name_user
    def isLoadedModule(self, modulename):
        prj = pineboolib.project
        return modulename in prj.modules
sys = SysType()

aqtt = auto_qt_translate_text

def connect(sender, signal, receiver, slot):
    # print "Connect::", sender, signal, receiver, slot
    if sender is None:
        print("Connect Error::", sender, signal, receiver, slot)
        return False
    m = re.search(r"^(\w+)\.(\w+)(\(.*\))?", slot)
    remote_fn = getattr(receiver, slot, None)
    if remote_fn:
        try:
            QtCore.QObject.connect(sender, QtCore.SIGNAL(signal), remote_fn)
        except RuntimeError as e:
            print("ERROR Connecting:", sender, QtCore.SIGNAL(signal), remote_fn)
            print("ERROR %s : %s" % (e.__class__.__name__, str(e)))
            return False
    elif m:
        remote_obj = getattr(receiver, m.group(1), None)
        if remote_obj is None: raise AttributeError("Object %s not found on %s" % (remote_obj, str(receiver)))
        remote_fn = getattr(remote_obj, m.group(2), None)
        if remote_fn is None: raise AttributeError("Object %s not found on %s" % (remote_fn, remote_obj))
        try:
            QtCore.QObject.connect(sender, QtCore.SIGNAL(signal), remote_fn)
        except RuntimeError as e:
            print("ERROR Connecting:", sender, QtCore.SIGNAL(signal), remote_fn)
            print("ERROR %s : %s" % (e.__class__.__name__, str(e)))
            return False

    else:
        QtCore.QObject.connect(sender, QtCore.SIGNAL(signal), receiver, QtCore.SLOT(slot))
    return True

QMessageBox = QtGui.QMessageBox

class MessageBox(QMessageBox):
    @classmethod
    def msgbox(cls, typename, text, button0, button1 = None, button2 = None):
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
        #title = unicode(title,"UTF-8")
        #text = unicode(text,"UTF-8")
        msg = QMessageBox(icon, title, text)
        msg.addButton(button0)
        if button1: msg.addButton(button1)
        if button2: msg.addButton(button2)
        return msg.exec_()

    @classmethod
    def question(cls, *args): return cls.msgbox("question",*args)

    @classmethod
    def information(cls, *args): return cls.msgbox("question",*args)

    @classmethod
    def warning(cls, *args): return cls.msgbox("warning",*args)

    @classmethod
    def critical(cls, *args): return cls.msgbox("critical",*args)


class Input(object):
    @classmethod
    def getText(cls, question, prevtxt, title):
        text, ok = QtGui.QInputDialog.getText(None, title,
                question, QtGui.QLineEdit.Normal, prevtxt)
        if not ok: return None
        return text


