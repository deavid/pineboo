# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore

class QDialog(QtWidgets.QDialog):
    
    def __init__(self, parent=None, name=None, b=None):
        if isinstance(parent, int):
            parent = None
        
        super().__init__(parent)
        if name:
            self.setTitle(name)
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
    
    @QtCore.pyqtSlot()
    def close(self):
        super().close()
    

    caption = property(getTitle, setTitle)
    enable = property(getEnabled, setEnable_)