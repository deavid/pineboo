# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets  # type: ignore
from pineboolib.plugins.dgi.dgi_qt.dgi_objects.qwidget import QWidget
from typing import Any


class CheckBox(QWidget):
    _label: QtWidgets.QLabel
    _cb: QtWidgets.QCheckBox

    def __init__(self) -> None:
        super(CheckBox, self).__init__()

        self._label = QtWidgets.QLabel(self)
        self._cb = QtWidgets.QCheckBox(self)
        spacer = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        _lay = QtWidgets.QHBoxLayout()
        _lay.addWidget(self._cb)
        _lay.addWidget(self._label)
        _lay.addSpacerItem(spacer)
        self.setLayout(_lay)

    def __setattr__(self, name, value) -> None:
        if name == "text":
            self._label.setText(str(value))
        elif name == "checked":
            self._cb.setChecked(value)
        else:
            super(CheckBox, self).__setattr__(name, value)

    def __getattr__(self, name) -> Any:
        if name == "checked":
            return self._cb.isChecked()
        else:
            return super(CheckBox, self).__getattr__(name)
