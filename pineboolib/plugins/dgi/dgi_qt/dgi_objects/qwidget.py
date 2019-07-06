# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets  # type: ignore
from typing import Any


class QWidget(QtWidgets.QWidget):
    def child(self, name) -> Any:
        return self.findChild(QtWidgets.QWidget, name)
