# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
from pineboolib import decorators

class QGroupBox(QtWidgets.QGroupBox):

    def __init__(self, *args, **kwargs):
        super(QGroupBox, self).__init__(*args, **kwargs)
        self.setStyleSheet("QGroupBox { font-weight: bold; } ")
        self.setContentsMargins(0, 0, 0, 0)
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

    @decorators.NotImplementedWarn
    def setShown(self, b):
        pass

    def __setattr__(self, name, value):
        if name == "title":
            self.setTitle(str(value))
        else:
            super(QGroupBox, self).__setattr__(name, value)