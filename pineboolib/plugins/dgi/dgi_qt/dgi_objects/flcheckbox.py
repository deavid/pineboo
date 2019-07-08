# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets  # type: ignore


class FLCheckBox(QtWidgets.QCheckBox):
    def __init__(self, parent=None, num_rows=None) -> None:
        super(FLCheckBox, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
