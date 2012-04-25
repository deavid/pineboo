# encoding: UTF-8
from PyQt4 import QtCore,QtGui
import re
import flcontrols
import pineboolib

def parseFloat(x): return float(x)

util = flcontrols.FLUtil() # <- para cuando QS erróneo usa util sin definirla

def ustr(t):
    if isinstance(t, unicode): return t
    if isinstance(t, QtCore.QString): return unicode(t)
    if isinstance(t, str): return unicode(t,"UTF-8")
    try:
        return str(t)
    except Exception, e:
        print "ERROR Coercing to string:", repr(t)
        print "ERROR", e.__class__.__name__, str(e)
        return None
    
    

def auto_qt_translate_text(text):
    if isinstance(text,basestring):
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
    print "Connect::", sender, signal, receiver, slot
    if sender is None:
        return False
    m = re.search("^(\w+).(\w+)(\(.*\))?", slot)
    if m:
        remote_obj = getattr(receiver, m.group(1))
        if remote_obj is None: raise AttribueError, "Object %s not found on %s" % (remote_obj, str(receiver))
        remote_fn = getattr(remote_obj, m.group(2))
        if remote_fn is None: raise AttribueError, "Object %s not found on %s" % (remote_fn, remote_obj)
        sender.connect(sender, QtCore.SIGNAL(signal), remote_fn)
    else:
        sender.connect(sender, QtCore.SIGNAL(signal), receiver, QtCore.SLOT(slot))
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
                                              

