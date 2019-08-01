# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets  # type: ignore
from pineboolib.core import decorators


from .qframe import QFrame
from .qgroupbox import QGroupBox
from .qwidget import QWidget
from typing import Union, Any


class QToolButton(QtWidgets.QToolButton):

    groupId = None

    def __init__(self, parent: Union[QWidget, QGroupBox, QFrame]) -> None:
        super(QToolButton, self).__init__(parent)
        self.groupId = None

    def setToggleButton(self, value) -> None:
        self.setDown(value)

    @decorators.Deprecated
    def setUsesBigPixmap(self, value):
        pass

    def toggleButton(self) -> Any:
        return self.isDown()

    def getOn(self) -> Any:
        return self.isChecked()

    def setOn(self, value) -> None:
        self.setChecked(value)

    on = property(getOn, setOn)

    @decorators.Deprecated
    def setUsesTextLabel(self, value):
        pass

    def buttonGroupId(self) -> Any:
        return self.groupId

    def setButtonGroupId(self, id) -> None:
        self.groupId = id
