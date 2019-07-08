# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets  # type: ignore


class QVBoxLayout(QtWidgets.QVBoxLayout):
    def __init__(self, parent=None) -> None:
        if isinstance(parent, QtWidgets.QWidget):
            super().__init__(parent)
        else:
            super().__init__()
            if parent:
                parent.addLayout(self)

        self.setContentsMargins(1, 1, 1, 1)
        self.setSpacing(1)
        self.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
