# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets


class FLSpinBox(QtWidgets.QSpinBox):

    def __init__(self, parent=None):
        super().__init__(parent)
        # editor()setAlignment(Qt::AlignRight);

    def setMaxValue(self, v):
        self.setMaximum(v)
    
    def getValue(self):
        return super().value()
    
    def setValue(self, val):
        super().setValue(val)
    
    value = property(getValue, setValue)