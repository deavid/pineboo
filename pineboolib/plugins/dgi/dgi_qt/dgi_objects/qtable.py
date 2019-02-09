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
    
    def currentChanged_(self, current_row, current_column, previous_row, previous_column):
        # FIXME: esto produce un TypeError: native Qt signal is not callable, porque existe una función virtual llamada currentChanged
        if (current_row > -1 and current_column > -1):
            self.currentChanged.emit(current_row, current_column)
            pass

    def doubleClicked_(self, f, c):
        self.doubleClicked.emit(f, c)
    
    def __getattr__(self, name):
        return getattr(QtCore.Qt, name) if hasattr(QtCore.Qt, name) else None
    
    def valueChanged_(self, item = None):
        
        if item:
            self.valueChanged.emit(item.row(), item.column())

    def numRows(self):
        return self.rowCount()

    def numCols(self):
        return self.columnCount()
    
    def setCellAlignment(self, row, col, alig_):
        self.item(row, col).setTextAlignment(alig_)

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
    
    def setRowLabels(self, separator, lista):
        array_ = lista.split(separator)
        self.setVerticalHeaderLabels(array_)
    
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
            if row in self.read_only_rows:
                return #Ya esta en True la row
            
            self.read_only_rows.append(row)
        else:
            if row in self.read_only_rows:
                self.read_only_rows.remove(row)
            else:
                return #Ya esta en False la row

        for col in range(self.columnCount()):
            item = self.item(row, col)
            if item:
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled) if b else item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable)

    def setColumnReadOnly(self, col, b):
        if b:
            if col in self.read_only_cols:
                return
            
            self.read_only_cols.append(col)
        else:
            if col in self.read_only_cols:
                self.read_only_cols.remove(col)
            else:
                return

        for row in range(self.rowCount()):
            item = self.item(row, col)
            if item:
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled) if b else item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable)

    @decorators.NotImplementedWarn
    def setLeftMargin(self, n):
        pass

    
    def setCellBackgroundColor(self, row, col, color):
        item = self.item(row, col)
        
        if item is not None and color:
            item.setBackground(color)
    
    @decorators.NotImplementedWarn
    def getSort(self):
        pass
    
    def setSort(self, col):
        super().setSortingEnabled()
        super().sortByColumn(col)
        
    
    sorting = property(getSort, setSort)
    
    def editCell(self, row, col):
        self.editItem(self.item(row,col))
        