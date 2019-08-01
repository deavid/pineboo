# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets  # type: ignore
from typing import Any


class QToolBar(QtWidgets.QToolBar):
    _label = None

    def setLabel(self, l: str) -> None:
        self._label = l

    def getLabel(self) -> Any:
        return self._label

    label = property(getLabel, setLabel)
