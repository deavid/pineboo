# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets

class QDialog(QtWidgets.QDialog):
    
    def getTitle(self):
        return self.windowTitle()
    
    def setTitle(self, title):
        self.setWindowTitle(title)
    
    def getEnabled(self):
        return self.isEnabled()
    
    def setEnable_(self, enable_):
        self.setEnabled(enable_)

    caption = property(getTitle, setTitle)
    enable = property(getEnabled, setEnable_)