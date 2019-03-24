# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtCore

class QComboBox(QtWidgets.QComboBox):

    _parent = None

    def __init__(self, parent=None):
        self._parent = parent
        super(QComboBox, self).__init__(parent)

    @property
    def currentItem(self):
        return self.currentIndex()

    @currentItem.setter
    def currentItem(self, i):
        if i is not None:
            self.setCurrentIndex(i)

    def insertStringList(self, strl):
        self.insertItems(len(strl), strl)