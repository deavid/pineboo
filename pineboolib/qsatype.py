# encoding: UTF-8
import os
from PyQt4 import QtCore,QtGui

def Object(): return {}

def Array(): return []

class FLSqlCursor(object):
    def __init__(self, actionname):
        print "New Cursor:", actionname
    


class FormDBWidget(QtGui.QWidget):
    def __init__(self):
        super(FormDBWidget, self).__init__()
        self.cursor = None
        self._class_init()
        
    def _class_init(self):
        pass

    def child(self, childName):
        return self.findChild(QtGui.QWidget, childName)
    
    def cursor(self):
        return self.cursor
