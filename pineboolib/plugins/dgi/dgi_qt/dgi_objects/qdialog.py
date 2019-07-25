# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets  # type: ignore
from typing import Any
from pineboolib.core import decorators


class QDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, name=None, b=None) -> None:
        if isinstance(parent, int):
            parent = None

        super().__init__(parent)
        if name:
            self.setTitle(name)
        self.setModal(True)

    def child(self, name) -> Any:
        return self.findChild(QtWidgets.QWidget, name)

    def getTitle(self) -> Any:
        return self.windowTitle()

    def setTitle(self, title) -> None:
        self.setWindowTitle(title)

    def getEnabled(self) -> Any:
        return self.isEnabled()

    def setEnable_(self, enable_) -> None:
        self.setEnabled(enable_)

    @decorators.pyqtSlot()
    def accept(self):
        super().accept()

    @decorators.pyqtSlot()
    def reject(self):
        super().reject()

    @decorators.pyqtSlot()
    def close(self):
        super().close()

    caption = property(getTitle, setTitle)
    enable = property(getEnabled, setEnable_)
