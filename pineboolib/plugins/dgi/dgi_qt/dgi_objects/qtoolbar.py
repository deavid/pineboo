# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets


class QToolBar(QtWidgets.QToolBar):
    _label = None

    def setLabel(self, l):
        self._label = l

    def getLabel(self):
        return self._label

    label = property(getLabel, setLabel)
