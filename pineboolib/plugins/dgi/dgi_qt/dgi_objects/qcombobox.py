# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
from pineboolib import decorators


class QComboBox(QtWidgets.QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setCurrentItem = self.setCurrentIndex

    def insertStringList(self, strl):
        self.insertItems(len(strl), strl)

    def setReadOnly(self, b):
        super().setEditable(not b)
