# encoding: UTF-8
import os
from PyQt4 import QtCore,QtGui
import qsaglobals 
from flcontrols import FLTable, FLTableDB, FLSqlCursor, FLUtil

def Object(): return {}

def Array(): return []


        

class FormDBWidget(QtGui.QWidget):
    def __init__(self,action, project):
        super(FormDBWidget, self).__init__()
        self._action = action
        self._cursor = FLSqlCursor(action.name)
        self._prj = project
        self._class_init()
        
    def _class_init(self):
        pass

    def child(self, childName):
        return self.findChild(QtGui.QWidget, childName)
    
    def cursor(self):
        return self._cursor
