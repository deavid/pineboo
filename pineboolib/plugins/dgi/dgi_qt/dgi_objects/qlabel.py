# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore, QtGui

class QLabel(QtWidgets.QLabel):

    @QtCore.pyqtProperty(str)
    def text(self):
        return self.text()

    @text.setter
    def text(self, v):
        if not isinstance(v, str):
            v = str(v)
        self.setText(v)

    def setText(self, text):
        if not isinstance(text, str):
            text = str(text)
        super(QLabel, self).setText(text)

    def setPixmap(self, pix):

        if isinstance(pix, QtGui.QIcon):
            pix = pix.pixmap(32, 32)
        super(QLabel, self).setPixmap(pix)

    @QtCore.pyqtSlot(bool)
    def setShown(self, b):
        self.setVisible(b)
    
    def getAlign(self):
        return self.alignment()
    
    def setAlign(self, alignment_):
        self.setAlignment(alignment_)
        
    alignment = property(getAlign, setAlign)