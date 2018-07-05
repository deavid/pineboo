# -*- coding: utf-8 -*-
import re
import os.path
import weakref
import logging
import traceback
import math
import codecs
from PyQt5.Qt import qApp
from PyQt5 import QtCore, QtWidgets
from PyQt5.Qt import QDateEdit


import pineboolib
from pineboolib import decorators
from pineboolib.utils import filedir
from pineboolib.fllegacy.FLUtil import FLUtil
from pineboolib.fllegacy.FLSqlCursor import FLSqlCursor
from pineboolib.fllegacy.aqsobjects.AQS import AQS as AQS_Legacy

logger = logging.getLogger(__name__)

util = FLUtil()  # <- para cuando QS erróneo usa util sin definirla

Insert = 0
Edit = 1
Del = 2
Browse = 3

AQS = AQS_Legacy()


class File:

    @classmethod
    def exists(cls, name):
        return os.path.isfile(name)


class FileDialog(QtWidgets.QFileDialog):

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

    def getExistingDirectory(basedir=None, caption=None):
        if not basedir:
            basedir = filedir("..")

        if pineboolib.project._DGI.localDesktop():
            parent = pineboolib.project.main_window.ui_
            ret = QtWidgets.QFileDialog.getExistingDirectory(parent, caption, basedir, QtWidgets.QFileDialog.ShowDirsOnly)
            if ret:
                ret = ret + "/"

            return ret


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


"""
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

"""
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
