# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtCore  # type: ignore
from .qgroupbox import QGroupBox
from pineboolib.core import decorators


from typing import Callable


class QButtonGroup(QGroupBox):

    selectedId = None
    pressed = QtCore.pyqtSignal(int)

    def __init__(self, *args) -> None:
        super(QButtonGroup, self).__init__(*args)
        self.bg_ = QtWidgets.QButtonGroup(self)
        self.selectedId = None

    @decorators.NotImplementedWarn
    def setLineWidth(self, w):
        pass

    def setSelectedId(self, id) -> None:
        self.selectedId = id

    def __getattr__(self, name: str) -> Callable:

        ret_ = getattr(self.bg_, name, None)
        return ret_
