# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtGui
from pineboolib import decorators
import pineboolib

class QListView(QtWidgets.QWidget):

    _resizeable = True
    _clickable = True
    _root_is_decorated = None
    _default_rename_action = None
    _tree = None
    _cols_labels = None
    _key = None
    _root_item = None
    _current_row = None
    
    def __init__(self, parent = None):
        super().__init__(parent = None)
        lay = QtWidgets.QVBoxLayout(self)
        self._tree = QtWidgets.QTreeView(self)
        lay.addWidget(self._tree)
        self._tree.setModel(QtGui.QStandardItemModel())
        self._cols_labels = []
        self._root_is_decorated = False
        self._key = ""
        self._root_item = None
        self._current_row = -1
    
    @decorators.NotImplementedWarn
    def addItem(self, t):
    #    from pineboolib.pncontrolsfactory import FLListViewItem
    #    self._current_row = self._current_row + 1
    #    item = FLListViewItem(self)
    #    item.setText(t)
    #    print("PADRE", item)
    #    self._tree.model().setItem(self._current_row, 0, item)
        pass

    @decorators.NotImplementedWarn
    def setItemMargin(self, m):
        self.setContentsMargins(m, m, m, m)
    
    def setHeaderLabel(self, labels):
        if isinstance(labels, str):
            labels = [labels]
        
        self._tree.model().setHorizontalHeaderLabels(labels)  
        self._cols_labels = labels
        
            
    @decorators.NotImplementedWarn
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
    
    @decorators.NotImplementedWarn
    def defaultRenameAction(self):
        return self._default_rename_action
    
    @decorators.NotImplementedWarn
    def setDefaultRenameAction(self, b):
        self._default_rename_action = b
    
    
    def model(self):
        return self._tree.model()
    
    #def __getattr__(self, name):
    #    att = getattr(self._tree, name, None)
    #    return att
    
    #def key(self):
    #    return self._key
    
    #def setKey(self, k):
    #    self._key = str(k)

            