# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore, QtGui

class QLabel(QtWidgets.QLabel):
        

    @QtCore.pyqtProperty(str)
    def text(self):
        return super().text()

    @text.setter
    def text(self, v):
        if not isinstance(v, str):
            v = str(v)
        self.setText(v)

    def setText(self, text):
        if not isinstance(text, str):
            text = str(text)
        super().setText(text)

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
    
    def get_palette_fore_ground(self):
        return self.palette().text().color()
    
    def set_palette_fore_ground(self, color):
        pal = self.palette()
        pal.setColor(pal.WindowText, color)
        self.setPalette(pal)
        
    alignment = property(getAlign, setAlign)
    paletteForegroundColor = property(get_palette_fore_ground, set_palette_fore_ground)