# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
from pineboolib import decorators

class QListView(QtWidgets.QWidget):

    _resizeable = True
    _clickable = True
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pass
    
    @decorators.NotImplementedWarn
    def addItem(self, item):
        pass

    @decorators.NotImplementedWarn
    def setItemMargin(self, m):
        self.setContentsMargins(m, m, m, m)
    
    @decorators.NotImplementedWarn
    def setHeaderLabel(self, l):
        pass
    
    @decorators.NotImplementedWarn
    def setColumnText(self, col, text):
        pass
    
    @decorators.NotImplementedWarn
    def addColumn(self, text):
        pass
    
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
        pass