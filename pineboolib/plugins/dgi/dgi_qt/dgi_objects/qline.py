# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets  # type: ignore
from typing import Any


class QLine(QtWidgets.QFrame):
    object_name = None
    orientation_ = 0

    def __init__(self, parent) -> None:
        super().__init__()

    def getObjectName(self) -> Any:
        return self.object_name

    def setObjectName(self, name) -> None:
        self.object_name = name

    def setOrientation(self, ori_=0) -> None:
        self.orientation_ = ori_
        self.setFrameShape(self.HLine if ori_ == 1 else self.VLine)

    def getOrientation(self) -> int:
        return self.orientation_

    orientation = property(getOrientation, setOrientation)
    objectName = property(getObjectName, setObjectName)  # type: ignore
