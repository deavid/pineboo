# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets


from pineboolib.plugins.dgi.dgi_qt.dgi_objects.qgroupbox import QGroupBox
from pineboolib.plugins.dgi.dgi_qt.dgi_objects.qwidget import QWidget
from typing import Union


class QFrame(QtWidgets.QFrame):
    _line_width = None

    def __init__(self, parent: Union[QGroupBox, QWidget]) -> None:
        super().__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self._line_width = 1
        self._do_style()

    def _do_style(self) -> None:
        self.style_str = "QFrame{ background-color: transparent;"
        self.style_str += " border-width: %spx;" % self._line_width
        self.style_str += " }"
        self.setStyleSheet(self.style_str)
