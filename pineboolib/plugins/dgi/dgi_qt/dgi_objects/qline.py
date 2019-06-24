# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
from pineboolib import decorators


class QLine(QtWidgets.QFrame):
    object_name = None
    orientation_ = 0

    def __init__(self, parent):
        super().__init__()

    def getObjectName(self):
        return self.object_name

    def setObjectName(self, name):
        self.object_name = name

    def setOrientation(self, ori_=0):
        self.orientation_ = ori_
        self.setFrameShape(self.HLine if ori_ == 1 else self.VLine)

    def getOrientation(self):
        return self.orientation_

    orientation = property(getOrientation, setOrientation)
    objectName = property(getObjectName, setObjectName)
