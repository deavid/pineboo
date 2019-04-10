# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtCore
from pineboolib.plugins.dgi.dgi_qt.dgi_objects.qgroupbox import QGroupBox
from pineboolib import decorators

class QButtonGroup(QGroupBox):

    selectedId = None
    pressed = QtCore.pyqtSignal(int)
    def __init__(self, *args):
        super(QButtonGroup, self).__init__(*args)
        self.bg_ = QtWidgets.QButtonGroup(self)
        self.selectedId = None
        
    @decorators.NotImplementedWarn
    def setLineWidth(self, w):
        pass
    
    def setSelectedId(self, id):
        self.selectedId = id
    
    
    def __getattr__(self, name):
        
        ret_ = getattr(self.bg_, name, None)        
        return ret_
        