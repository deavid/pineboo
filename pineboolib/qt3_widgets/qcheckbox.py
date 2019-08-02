# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets  # type: ignore


class QCheckBox(QtWidgets.QCheckBox):

    _parent = None

    def __init__(self, *args) -> None:
        if len(args) == 1:
            parent = args[0]
        else:
            self.setObjectName(args[0])
            parent = args[1]

        super().__init__(parent)

    def get_checked(self):
        return self.isChecked()

    def set_checked(self, b):
        if isinstance(b, str):
            b = b == "true"

        super().setChecked(b)

    checked = property(get_checked, set_checked)
