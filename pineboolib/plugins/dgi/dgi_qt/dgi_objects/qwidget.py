# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
from typing import Any


class QWidget(QtWidgets.QWidget):
    def child(self, name) -> Any:
        return self.findChild(QtWidgets.QWidget, name)
