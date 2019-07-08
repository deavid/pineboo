# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets  # type: ignore
from typing import Optional
from typing import Any


class QAction(QtWidgets.QAction):

    activated = QtCore.pyqtSignal()
    _menuText = None
    _objectName = None

    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.triggered.connect(self.send_activated)
        self._name = None
        self._menuText = None

    def send_activated(self, b: Optional[bool] = None) -> None:
        self.activated.emit()

    def getName(self) -> str:
        return self.objectName()

    def setName(self, n) -> None:
        self.setObjectName(n)

    def getMenuText(self) -> Any:
        return self._menuText

    def setMenuText(self, t) -> None:
        self._menuText = t

    name = property(getName, setName)
    menuText = property(getMenuText, setMenuText)
