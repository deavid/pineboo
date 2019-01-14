# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
from pineboolib import decorators
from PyQt5.QtWidgets import QFrame
from PyQt5 import Qt

class QGroupBox(QtWidgets.QGroupBox):
    
    style_str = None
    _line_width = None
    
    def __init__(self, *args, **kwargs):
        super(QGroupBox, self).__init__(*args, **kwargs)
        self._do_style()
        from pineboolib.fllegacy.flsettings import FLSettings
        settings = FLSettings()
        if not settings.readBoolEntry("ebcomportamiento/spacerLegacy", False):
            self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

    def setLineWidth(self, width):
        self._line_width = width
        self._do_style()
    
    
    def _do_style(self):
        self.style_str = "QGroupBox { font-weight: bold; background-color: transparent;"
        if self._line_width is not None:
            self.style_str += " border: %spx transparent;" % self._line_width
        self.style_str += " }"
        self.setStyleSheet(self.style_str)
        

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
    
    @decorators.NotImplementedWarn
    def setFrameShadow(self, fs):
        pass
    
    @decorators.NotImplementedWarn
    def setFrameShape(self, fs):
        pass
    
    
    enabled = property(get_enabled, set_enabled)
    
        
        