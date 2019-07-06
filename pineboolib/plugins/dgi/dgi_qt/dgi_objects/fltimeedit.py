# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtCore  # type: ignore


class FLTimeEdit(QtWidgets.QTimeEdit):
    def __init__(self, parent) -> None:
        super(FLTimeEdit, self).__init__(parent)
        self.setDisplayFormat("hh:mm:ss")
        self.setMinimumWidth(90)
        self.setMaximumWidth(90)

    def setTime(self, v) -> None:
        if isinstance(v, str):
            v = v.split(":")
            time = QtCore.QTime(int(v[0]), int(v[1]), int(v[2]))
        else:
            time = v

        super(FLTimeEdit, self).setTime(time)
