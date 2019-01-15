# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore

class QDialog(QtWidgets.QDialog):
    
    def __init__(self):
        super().__init__()
        self.setModal(True)
        
    
    def getTitle(self):
        return self.windowTitle()
    
    def setTitle(self, title):
        self.setWindowTitle(title)
    
    def getEnabled(self):
        return self.isEnabled()
    
    def setEnable_(self, enable_):
        self.setEnabled(enable_)
    
    @QtCore.pyqtSlot()
    def accept(self):
        super().accept()
    
    @QtCore.pyqtSlot()
    def reject(self):
        super().reject()

    caption = property(getTitle, setTitle)
    enable = property(getEnabled, setEnable_)