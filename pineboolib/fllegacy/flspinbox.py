# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets  # type: ignore
from typing import Any


class FLSpinBox(QtWidgets.QSpinBox):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        # editor()setAlignment(Qt::AlignRight);

    def setMaxValue(self, v) -> None:
        self.setMaximum(v)

    def getValue(self) -> Any:
        return super().value()

    def setValue(self, val) -> None:
        super().setValue(val)

    value: Any = property(getValue, setValue)  # type: ignore
    text: Any = value
