# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
from builtins import object
import re
from PyQt4 import QtCore, QtGui

import traceback
import pineboolib
from pineboolib import flcontrols


from pineboolib.utils import aqtt, auto_qt_translate_text

def parseFloat(x): return float(x)


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



class SysType(object):
    def __init__(self):
        self._name_user = "database_user"

    def nameUser(self): return self._name_user
    def isLoadedModule(self, modulename):
        prj = pineboolib.project
        return modulename in prj.modules
sys = SysType()


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


def qsa_length(obj):
    lfn = getattr(obj, "length", None)
    if lfn: return lfn()
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
        if isinstance(parent,str): parent = QtCore.QString(parent)
        self.parent = parent
        self.loaded = True


    def __getattr__(self, k):
        if not self.loaded: return super(qsa, self).__getattr__(k)
        try:
            f = getattr(self.parent,k)
            if callable(f): return f()
            else: return f
        except Exception:
            if k == 'length': return len(self.parent)
            print("FATAL: qsa: error al intentar emular getattr de %r.%r" % (self.parent, k))
            print(traceback.format_exc(4))

    def __setattr__(self, k,v):
        if not self.loaded: return super(qsa, self).__setattr__(k,v)
        try:
            if not self.parent:
                return
            f = getattr(self.parent,k)
            if callable(f): return f(v)
            else: return setattr(self.parent,k,v)
        except Exception:
            try:
                k = 'set' + k[0].upper() + k[1:]
                f = getattr(self.parent,k)
                if callable(f): return f(v)
                else: return setattr(self.parent,k,v)
            except Exception:
                print("FATAL: qsa: error al intentar emular setattr de %r.%r = %r" % (self.parent, k , v))
                print(traceback.format_exc(4))


from pineboolib.fllegacy import FLUtil
util = FLUtil.FLUtil() # <- para cuando QS erróneo usa util sin definirla

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

#from forbiddenfruit import curse
#curse(str, "left", lambda self, n: self[:n])
