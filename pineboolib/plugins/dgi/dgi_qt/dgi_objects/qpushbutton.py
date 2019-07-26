# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets  # type: ignore
from pineboolib.core import decorators


from PyQt5.QtGui import QIcon  # type: ignore
from typing import Any


class QPushButton(QtWidgets.QPushButton):
    def __init__(self, *args, **kwargs) -> None:
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

    def setPixmap(self, value: QIcon) -> None:
        return self.setIcon(value)

    def getToggleButton(self) -> Any:
        return self.isCheckable()

    def setToggleButton(self, v: bool) -> None:
        return self.setCheckable(v)

    def getOn(self) -> Any:
        return self.isChecked()

    def setOn(self, value) -> None:
        self.setChecked(value)

    def getText(self) -> Any:
        return super().text()

    def setText(self, val: str) -> None:
        if self.maximumWidth() < 33 and len(val) > 4:
            val = ""
        super().setText(val)

    def setMaximumSize(self, *args) -> None:
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
    text = property(getText, setText)  # type: ignore

    @decorators.NotImplementedWarn
    def __getattr__(self, name):
        pass
