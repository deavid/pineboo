# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets

class QPushButton(QtWidgets.QPushButton):

    def __init__(self, *args, **kwargs):
        super(QPushButton, self).__init__(*args, **kwargs)
        

    @property
    def pixmap(self):
        return self.icon()

    @property
    def enabled(self):
        return self.getEnabled()

    @enabled.setter
    def enabled(self, s):
        return self.setEnabled(s)

    @pixmap.setter
    def pixmap(self, value):
        return self.setIcon(value)

    def setPixmap(self, value):
        return self.setIcon(value)

    def getToggleButton(self):
        return self.isCheckable()

    def setToggleButton(self, v):
        return self.setCheckable(v)

    def getOn(self):
        return self.isChecked()

    def setOn(self, value):
        self.setChecked(value)
    
    def getText(self):
        return self.text()
    
    def setText(self, val):
        super(QPushButton, self).setText(val)
    
    def setMaximumSize(self, w, h=None):
        if not isinstance(w, int):
            if w.height() == 32767:
                w.setHeight(22)
            
            super().setMaximumSize(w)
        else:
            if h == 32767:
                h = w
            super().setMaximumSize(w, h) 

    toggleButton = property(getToggleButton, setToggleButton)
    on = property(getOn, setOn)
    text = property(getText, setText)