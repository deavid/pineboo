# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import os
import datetime

from PyQt4 import QtCore, QtGui

from pineboolib import qsaglobals
from pineboolib import flcontrols
from pineboolib.fllegacy import FLFormSearchDB as FLFormSearchDB_legacy
from pineboolib.flcontrols import FLTable, FLReportViewer, QLineEdit
from pineboolib.fllegacy import FLSqlQuery as FLSqlQuery_Legacy
from pineboolib.fllegacy import FLSqlCursor as FLSqlCursor_Legacy
from pineboolib.fllegacy import FLTableDB as FLTableDB_Legacy
from pineboolib.fllegacy import FLUtil as FLUtil_Legacy

from pineboolib import decorators

def Object(x=None):
    if x is None: x = {}
    return dict(x)

def Array(x=None):
    try:
        if x is None: return {}
        else: return list(x)
    except TypeError:
        return [x]

def Boolean(x=False): return bool(x)

def FLSqlQuery(*args):
    #if not args: return None
    return FLSqlQuery_Legacy.FLSqlQuery(*args)

def FLUtil(*args):
    return FLUtil_Legacy.FLUtil(*args)

def FLSqlCursor(action=None):
    if action is None: return None
    return FLSqlCursor_Legacy.FLSqlCursor(action)

def FLTableDB(*args):
    if not args: return None
    return FLTableDB_Legacy.FLTableDB(*args)

@decorators.NotImplementedWarn
def FLCodBar(*args, **kwargs):
    class flcodbar:
        def nameToType(self, name):
            return name
        def pixmap(self):
            return None
        def validBarcode(self):
            return None
    return flcodbar()

class FormDBWidget(QtGui.QWidget):

    def __init__(self, action, project, parent = None):
        super(FormDBWidget, self).__init__(parent)
        self._action = action
        self.cursor_ = FLSqlCursor(action.name)
        self._prj = project
        self._class_init()

    def _class_init(self):
        pass

    def child(self, childName):
        try:
            ret = self.findChild(QtGui.QWidget, childName)
        except RuntimeError as rte:
            # FIXME: A veces intentan buscar un control que ya está siendo eliminado.
            # ... por lo que parece, al hacer el close del formulario no se desconectan sus señales.
            print("ERROR: Al buscar el control %r encontramos el error %r" % (childName,rte))
            ret = None
        else:
            if ret is None:
                print("WARN: No se encontró el control %r" % childName)
        #else:
        #    print("DEBUG: Encontrado el control %r: %r" % (childName, ret))
        return ret

    def cursor(self):
        cursor = getattr(self.parentWidget(),"cursor_", None)
        if cursor:
            del self.cursor_
            self.cursor_ = cursor
        return self.cursor_

def FLFormSearchDB(name):
    widget = FLFormSearchDB_legacy.FLFormSearchDB(name)
    widget.setWindowModality(QtCore.Qt.ApplicationModal)
    return widget

class Date(QtCore.QDate):
    pass

class Dialog(QtGui.QDialog):
    _layout = None

    def __init__(self, title, f):
        #FIXME: f no lo uso , es qt.windowsflg
        super(Dialog, self).__init__()
        self.setWindowTitle(title)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self._layout = QtGui.QVBoxLayout()
        self.setLayout(self._layout)


    def add(self, _object):
        self._layout.addWidget(_object)



class GroupBox(QtGui.QGroupBox):
    pass

class CheckBox(QtGui.QCheckBox):
    pass

