# -*- coding: utf-8 -*-

from PyQt5 import QtCore
from pineboolib import decorators

class QLine(QtCore.QLine):
    object_name = None
    
    def __init__(self, parent):
        super().__init__()
    
    def __getattr__(self, name):
        print("Buscando", name)
    
    @decorators.NotImplementedWarn
    def setPalette(self, *args):
        pass
    
    
    def getObjectName(self):
        return self.object_name
    
    def setObjectName(self, name):
        self.object_name = name
    
    @decorators.NotImplementedWarn
    def show(self):
        pass
    
    @decorators.NotImplementedWarn
    def setFrameShadow(self, frame_shadow):
        pass
    
    @decorators.NotImplementedWarn
    def setFrameShape(self, frame_shape):
        pass
    
    @decorators.NotImplementedWarn
    def setOrientation(self, ori_):
        pass
    
    def getOrientation(self):
        return super().orientation()
    
    orientation = property(getOrientation, setOrientation)
    objectName = property(getObjectName, setObjectName)