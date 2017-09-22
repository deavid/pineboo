# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals

from PyQt5 import QtCore, QtWidgets #, QtGui, QtWidgets, uic

import pineboolib
#from pineboolib.qsaglobals import ustr
from pineboolib.utils import DefFun
from pineboolib import decorators

Qt = QtCore.Qt
# TODO: separar en otro fichero de utilidades

def ustr1(t):
    if isinstance(t, str): return t
    #if isinstance(t, QtCore.QString): return str(t)
    #if isinstance(t, str): return str(t,"UTF-8")
    try:
        return str(t)
    except Exception as e:
        print("ERROR Coercing to string:", repr(t))
        print("ERROR", e.__class__.__name__, str(e))
        return None

def ustr(*t1):
    return "".join([ ustr1(t) for t in t1 ])

class QLayoutWidget(QtWidgets.QWidget):
    pass

class ProjectClass(QtCore.QObject):
    def __init__(self):
        super(ProjectClass, self).__init__()
        self._prj = pineboolib.project
    def __iter__(self):
        # Para soportar el modo Javascript de "attribute" in object
        # agregamos soporte de iteración
        return iter(self.__dict__.keys())        

class QCheckBox(QtWidgets.QCheckBox):
    def __getattr__(self, name): return DefFun(self, name)

    @QtCore.pyqtProperty(int)
    def checked(self):
        return self.isChecked()

    @checked.setter
    def checked(self, v):
        if not v:
            v = False
        self.setCheckState(v)

class QLabel(QtWidgets.QLabel):
    
    def __getattr__(self, name): 
        return DefFun(self, name)
    
    @QtCore.pyqtProperty(str)
    def text(self):
        return self.text()
    
    @text.setter
    def text(self, v):
        if not isinstance(v, str): 
            v = str(v)
        self.setText(v)
    
    def setText(self, text):
        if not isinstance(text, str): 
            text = str(text)
        super(QLabel, self).setText(text)


class QComboBox(QtWidgets.QComboBox):
    def __getattr__(self, name): return DefFun(self, name)
    
    @QtCore.pyqtProperty(str)
    def currentItem(self): return self.currentIndex

    @currentItem.setter
    def currentItem(self, i):
        if i:
            self.setCurrentIndex(i)

class QButtonGroup(QtWidgets.QGroupBox):
    def __getattr__(self, name): return DefFun(self, name)
    @property
    def selectedId(self): return 0


class ProgressDialog(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(ProgressDialog,self).__init__(*args, **kwargs)
        self.title = "Untitled"
        self.step = 0
        self.steps = 100
    def __getattr__(self, name): return DefFun(self, name)

    def setup(self, title, steps):
        self.title = title
        self.step = 0
        self.steps = steps
        self.setWindowTitle("%s - %d/%d" % (self.title,self.step,self.steps))
        self.setWindowModality(QtCore.Qt.ApplicationModal)

    def setProgress(self, step):
        self.step = step
        self.setWindowTitle("%s - %d/%d" % (self.title,self.step,self.steps))
        if step > 0: self.show()
        self.update()
        QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.ExcludeUserInputEvents)


class FLTable(QtWidgets.QTableWidget):
    def __getattr__(self, name): return DefFun(self, name)


class QTabWidget(QtWidgets.QTabWidget):
    def setTabEnabled(self, tab, enabled):
        #print("QTabWidget::setTabEnabled %r : %r" % (tab, enabled))
        if isinstance(tab, int): return QtWidgets.QTabWidget.setTabEnabled(self, tab, enabled)
        if isinstance(tab, str): 
            tabs = [ str(QtWidgets.QTabWidget.tabText(self, i)).lower().replace("&","") for i in range(self.count()) ]
            try:
                idx = tabs.index(tab.lower())              
                return QtWidgets.QTabWidget.setTabEnabled(self, idx, enabled)
            except ValueError:
                print("ERROR: Tab not found:: QTabWidget::setTabEnabled %r : %r" % (tab, enabled), tabs)
                return False
        print("ERROR: Unknown type for 1st arg:: QTabWidget::setTabEnabled %r : %r" % (tab, enabled))


class QLineEdit(QtWidgets.QLineEdit):
    
    
    @QtCore.pyqtProperty(str)
    def text(self):
        return super(QLineEdit, self).text()
    
    @text.setter
    def text(self, v):
        if not isinstance(v, str): 
            v = str(v)
        super(QLineEdit, self).setText(v)
    
    #def __getattr__(self, name): 
        #return DefFun(self, name)
        

class QListView(QtWidgets.QListView):
    def __init__(self, *args, **kwargs):
        super(QListView, self).__init__(*args, **kwargs)

    def __getattr__(self, name):
        print("flcontrols.QListView: Emulando método %r" % name)
        return self.defaultFunction

    def defaultFunction(self, *args, **kwargs):
        print("flcontrols.QListView: llamada a método no implementado", args,kwargs)

class QPushButton(QtWidgets.QPushButton):
    @property
    def pixmap(self):
        return self.icon()
    
    @property
    def enabled(self):
        return self.getEnabled()
    @enabled.setter
    def enabled(self, s):
        return self.setEnabled(s)
    
    @pixmap.setter
    def pixmap(self, value):
        return self.setIcon(value)

    def setPixmap(self, value):
        return self.setIcon(value)

    def getToggleButton(self):
        return self.isCheckable()
    def setToggleButton(self, v):
        return self.setCheckable(v)

    toggleButton = property(getToggleButton,setToggleButton)
