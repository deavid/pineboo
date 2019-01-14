# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtGui

class QListView(QtWidgets.QListView):

    _model = None
    _resizeable = True
    _clickable = True
    
    def __init__(self, *args, **kwargs):
        super(QListView, self).__init__(*args, **kwargs)

        self._model = QtGui.QStandardItemModel(self)
        self._resizeable = True
        self._clickable = True

    def addItem(self, item):
        it = QtGui.QStandardItem(item)
        self._model.appendRow(it)
        self.setModel(self._model)

    def setItemMargin(self, m):
        self.setContentsMargins(m, m, m, m)
    
    def setHeaderLabel(self, l):
        if isinstance(l, str):
            l = [l]
            
        if self._model and isinstance(l, list):
            self._model.setHorizontalHeaderLabels(l)

    def setClickable(self, c):
        self._clickable = True if c else False

    def setResizable(self, r):
        self._resizeable = True if r else False
    
    def resizeEvent(self, e):
        return super().resizeEvent(self, e) if self._resizeable else False
            
    def clear(self):
        self._model = None
        self._model = QtGui.QStandardItemModel(self)