# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
from pineboolib import decorators
from PyQt5.QtWidgets import QFrame
from PyQt5 import Qt

class QGroupBox(QtWidgets.QGroupBox):

    def __init__(self, *args, **kwargs):
        super(QGroupBox, self).__init__(*args, **kwargs)
        self.setStyleSheet("QGroupBox { font-weight: bold; } ")
        from pineboolib.fllegacy.flsettings import FLSettings
        settings = FLSettings()
        if not settings.readBoolEntry("ebcomportamiento/spacerLegacy", False):
            self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

    @decorators.NotImplementedWarn
    def setLineWidth(self, width):
        pass

    @property
    def selectedId(self):
        return 0
    
    def get_enabled(self):
        return self.isEnabled()
    
    def set_enabled(self, b):
        self.setDisabled(not b)

    @decorators.NotImplementedWarn
    def setShown(self, b):
        pass

    def __setattr__(self, name, value):
        if name == "title":
            self.setTitle(str(value))
        else:
            super(QGroupBox, self).__setattr__(name, value)
    
    
    
    enabled = property(get_enabled, set_enabled)
    
        
        