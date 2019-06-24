# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
from pineboolib import decorators


class QPushButton(QtWidgets.QPushButton):
    def __init__(self, *args, **kwargs):
        super(QPushButton, self).__init__(*args, **kwargs)
        self.setTextLabel = self.setText

    @decorators.NotImplementedWarn
    def setTextPosition(self, pos):
        pass

    @decorators.NotImplementedWarn
    def setUsesBigPixmap(self, b):
        pass

    @decorators.NotImplementedWarn
    def setUsesTextLabel(self, b):
        pass

    @property
    def pixmap(self):
        return self.icon()

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
        return super().text()

    def setText(self, val):
        if self.maximumWidth() < 33 and len(val) > 4:
            val = ""
        super().setText(val)

    def setMaximumSize(self, *args):
        w = 30
        h = 30

        if len(args) == 1:
            w = args[0].width()
            h = args[0].height()
            super().setMaximumSize(w, h)

        else:
            super().setMaximumSize(args[0], args[1])

    toggleButton = property(getToggleButton, setToggleButton)
    on = property(getOn, setOn)
    text = property(getText, setText)

    @decorators.NotImplementedWarn
    def __getattr__(self, name):
        pass
