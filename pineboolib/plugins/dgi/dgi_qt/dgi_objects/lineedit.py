# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets  # type: ignore
from pineboolib.plugins.dgi.dgi_qt.dgi_objects.qwidget import QWidget
from typing import Any


class LineEdit(QWidget):
    _label: QtWidgets.QLabel
    _line: QtWidgets.QLineEdit

    def __init__(self) -> None:
        super(LineEdit, self).__init__()

        self._label = QtWidgets.QLabel(self)
        self._line = QtWidgets.QLineEdit(self)
        _lay = QtWidgets.QHBoxLayout()
        _lay.addWidget(self._label)
        _lay.addWidget(self._line)
        self.setLayout(_lay)

    def __setattr__(self, name, value) -> None:
        if name == "label":
            self._label.setText(str(value))
        elif name == "text":
            self._line.setText(str(value))
        else:
            super(LineEdit, self).__setattr__(name, value)

    def __getattr__(self, name) -> Any:
        if name == "text":
            return self._line.text()
        else:
            return super(LineEdit, self).__getattr__(name)
