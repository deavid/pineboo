# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore, Qt
from pineboolib import decorators

class QTable(QtWidgets.QTableWidget):

    lineaActual = None
    currentChanged = QtCore.pyqtSignal(int, int)
    doubleClicked = QtCore.pyqtSignal(int, int)
    valueChanged = QtCore.pyqtSignal(int , int)
    read_only_cols = None
    read_only_rows = None
    cols_list = None

    def __init__(self, parent=None):
        super(QTable, self).__init__(parent)
        if not parent:
            self.setParent(self.parentWidget())

        self.cols_list = []
        self.lineaActual = -1
        self.currentCellChanged.connect(self.currentChanged_)
        self.cellDoubleClicked.connect(self.doubleClicked_)
        self.itemChanged.connect(self.valueChanged_)
        self.read_only_cols = []
        self.read_only_rows = []

    @decorators.needRevision
    def currentChanged_(self, currentRow, currentColumn, previousRow, previousColumn):
        # FIXME: esto produce un TypeError: native Qt signal is not callable
        self.currentChanged.emit(currentRow, currentColumn)

    def doubleClicked_(self, f, c):
        self.doubleClicked.emit(f, c)
    
    def valueChanged_(self, item = None):
        if item:
            self.valueChanged.emit(item.row(), item.col())

    def numRows(self):
        return self.rowCount()

    def numCols(self):
        return self.columnCount()

    def setNumCols(self, n):
        self.setColumnCount(n)
        self.setColumnLabels(",", ",".join(self.cols_list))

    def setNumRows(self, n):
        self.setRowCount(n)

    def setReadOnly(self, b):
        if b:
            self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        else:
            self.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)

    def selectionMode(self):
        return super(QTable, self).selectionMode()

    def setFocusStyle(self, m):
        self.setStyleSheet(m)

    def setColumnLabels(self, separador, lista):
        array_ = lista.split(separador)
        self.cols_list = []
        for i in range(self.columnCount()):
            if len(array_) > i:
                self.cols_list.append(array_[i])
        self.setHorizontalHeaderLabels(self.cols_list)
    
    def clear(self):
        super().clear()
        for i in range(self.rowCount()):
            self.removeRow(i)
        self.setHorizontalHeaderLabels(self.cols_list)
        self.setRowCount(0)
        

    def setColumnStrechable(self, col, b):
        if b:
            self.horizontalHeader().setSectionResizeMode(col, Qt.QHeaderView.Stretch)
        else:
            self.horizontalHeader().setSectionResizeMode(col, Qt.QHeaderView.AdjustToContents)

    def setHeaderLabel(self, l):
        self.cols_list.append(l)
        self.setColumnLabels(",", ",".join(self.cols_list))

    def insertRows(self, numero, n = 1):
        for r in range(n):
            self.insertRow(numero)

    def text(self, row, col):
        if row is None:
            return
        
        return self.item(row, col).text() if self.item(row, col) else None

    def setText(self, row, col, value):
        prev_item = self.item(row, col)
        if prev_item:
            bg_color = prev_item.background()
            
        self.setItem(row, col, QtWidgets.QTableWidgetItem(str(value)))
        
        if prev_item:
            self.setCellBackgroundColor(row, col, bg_color)
            
        if row in self.read_only_rows:
            self.setRowReadOnly(row, True)

        if col in self.read_only_cols:
            self.setColumnReadOnly(col, True)

    def adjustColumn(self, k):
        self.horizontalHeader().setSectionResizeMode(k, QtWidgets.QHeaderView.ResizeToContents)

    def setRowReadOnly(self, row, b):
        if b:
            self.read_only_rows.append(row)
        else:
            for r in self.read_only_rows:
                if r == row:
                    del r
                    break

        for col in range(self.columnCount()):
            item = self.item(row, col)
            if item:
                if b:
                    item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                else:
                    item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable)

    def setColumnReadOnly(self, col, b):
        if b:
            self.read_only_cols.append(col)
        else:
            for c in self.read_only_cols:
                if c == col:
                    del c
                    break

        for row in range(self.rowCount()):
            item = self.item(row, col)
            if item:
                if b:
                    item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                else:
                    item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable)

    @decorators.NotImplementedWarn
    def setLeftMargin(self, n):
        pass

    
    def setCellBackgroundColor(self, row, col, color):
        item = self.item(row, col)
        
        if item is not None and color:
            item.setBackground(color)