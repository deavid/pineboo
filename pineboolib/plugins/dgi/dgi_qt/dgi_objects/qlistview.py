# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtGui
from pineboolib import decorators

class QListView(QtWidgets.QWidget):

    _resizeable = True
    _clickable = True
    _tree = None
    _cols_labels = None
    
    def __init__(self, parent = None):
        super().__init__(parent = None)
        lay = QtWidgets.QVBoxLayout(self)
        self._tree = QtWidgets.QTreeView(self)
        lay.addWidget(self._tree)
        self._tree.setModel(QtGui.QStandardItemModel())
        self._cols_labels = []
    
    @decorators.NotImplementedWarn
    def addItem(self, item):
        pass


    @decorators.NotImplementedWarn
    def setItemMargin(self, m):
        self.setContentsMargins(m, m, m, m)
    
    def setHeaderLabel(self, labels):
        if isinstance(labels, str):
            labels = [labels]
        
        self._tree.model().setHorizontalHeaderLabels(labels)  
        self._cols_labels = labels
        
            
    
    def setColumnText(self, col, new_value):
        i = 0
        new_list = []
        for old_value in self._cols_labels:
            value = new_value if i == col else old_value
            new_list.append(value)
        
        self._cols_labels = new_list
    
    def addColumn(self, text):
        self._cols_labels.append(text)
        
        self.setHeaderLabel(self._cols_labels)
    
    @decorators.NotImplementedWarn
    def setExpandable(self, e):
        pass
    
    @decorators.NotImplementedWarn
    def setText(self, *args):
        pass
    
    @decorators.NotImplementedWarn
    def text(self, pos):
        pass
    
    @decorators.NotImplementedWarn
    def setOpen(self, b):
        pass
    
    
    @decorators.NotImplementedWarn
    def setPixmap(self, *args):
        pass

    @decorators.NotImplementedWarn
    def setClickable(self, c):
        self._clickable = True if c else False

    @decorators.NotImplementedWarn
    def setResizable(self, r):
        self._resizeable = True if r else False
    
    @decorators.NotImplementedWarn
    def resizeEvent(self, e):
        return super().resizeEvent(e) if self._resizeable else False
    
    @decorators.NotImplementedWarn
    def clear(self):
        self._cols_labels = []