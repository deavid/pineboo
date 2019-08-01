# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets  # type: ignore
from .qgroupbox import QGroupBox


class GroupBox(QGroupBox):
    def __init__(self, *args) -> None:
        super(GroupBox, self).__init__(*args)
        self._layout = QtWidgets.QVBoxLayout()
        self.setLayout(self._layout)

    def add(self, _object) -> None:
        self._layout.addWidget(_object)
