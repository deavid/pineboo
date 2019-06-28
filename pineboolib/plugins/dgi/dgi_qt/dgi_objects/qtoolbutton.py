# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
from pineboolib.core import decorators


class QToolButton(QtWidgets.QToolButton):

    groupId = None

    def __init__(self, parent):
        super(QToolButton, self).__init__(parent)
        self.groupId = None

    def setToggleButton(self, value):
        self.setDown(value)

    @decorators.Deprecated
    def setUsesBigPixmap(self, value):
        pass

    def toggleButton(self):
        return self.isDown()

    def getOn(self):
        return self.isChecked()

    def setOn(self, value):
        self.setChecked(value)

    on = property(getOn, setOn)

    @decorators.Deprecated
    def setUsesTextLabel(self, value):
        pass

    def buttonGroupId(self):
        return self.groupId

    def setButtonGroupId(self, id):
        self.groupId = id
