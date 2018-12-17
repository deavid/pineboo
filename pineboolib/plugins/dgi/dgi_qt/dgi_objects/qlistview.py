# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtGui
from pineboolib import decorators

class QListView(QtWidgets.QListView):

    _model = None

    def __init__(self, *args, **kwargs):
        super(QListView, self).__init__(*args, **kwargs)

        self._model = QtGui.QStandardItemModel(self)

    def addItem(self, item):
        it = QtGui.QStandardItem(item)
        self._model.appendRow(it)
        self.setModel(self._model)

    @decorators.Deprecated
    def setItemMargin(self, margin):
        pass

    @decorators.NotImplementedWarn
    def setClickable(self, c):
        pass

    @decorators.NotImplementedWarn
    def setResizable(self, r):
        pass

    @decorators.NotImplementedWarn
    def setHeaderLabel(self, l):
        pass

    def clear(self):
        self._model = None
        self._model = QtGui.QStandardItemModel(self)