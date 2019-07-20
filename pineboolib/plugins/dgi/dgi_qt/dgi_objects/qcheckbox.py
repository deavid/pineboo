# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets  # type: ignore


class QCheckBox(QtWidgets.QCheckBox):

    _parent = None

    def __init__(self, parent) -> None:
        self._parent = parent
        super().__init__(parent)

    def get_checked(self):
        return self.isChecked()

    def set_checked(self, b):
        if isinstance(b, str):
            b = b == "true"

        super().setChecked(b)

    checked = property(get_checked, set_checked)
