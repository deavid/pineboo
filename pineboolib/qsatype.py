# encoding: UTF-8
import os
from PyQt4 import QtCore,QtGui
import qsaglobals 
import flcontrols
from flcontrols import FLTable, FLUtil, FLReportViewer

def Object(x={}): return dict(x)

def Array(x=None): 
    if x is None: return {}
    else: return list(x)

def Boolean(x=False): return bool(x)

def FLSqlQuery(*args):
    #if not args: return None
    return flcontrols.FLSqlQuery(*args)

def FLSqlCursor(action=None):
    if action is None: return None
    return flcontrols.FLSqlCursor(action)       
     
def FLTableDB(*args):     
    if not args: return None
    return flcontrols.FLTableDB(*args)

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

def FLFormSearchDB(name):
    return flcontrols.FLFormSearchDB(name)