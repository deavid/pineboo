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
    resize_policy = None
    
    Default = 0
    Manual = 1
    AutoOne = 2
    AutoOneFit = 3
    sort_column_ = None
    

    def __init__(self, parent=None, name = None):
        super(QTable, self).__init__(parent)
        if not parent:
            self.setParent(self.parentWidget())
        
        if name:
            self.setObjectName(name)

        self.cols_list = []
        self.lineaActual = -1
        self.currentCellChanged.connect(self.currentChanged_)
        self.cellDoubleClicked.connect(self.doubleClicked_)
        self.itemChanged.connect(self.valueChanged_)
        self.read_only_cols = []
        self.read_only_rows = []
        self.resize_policy = 0 #Default
        self.sort_column_ = None
    
    def currentChanged_(self, current_row, current_column, previous_row, previous_column):
        # FIXME: esto produce un TypeError: native Qt signal is not callable, porque existe una función virtual llamada currentChanged
        if (current_row > -1 and current_column > -1):
            self.currentChanged.emit(current_row, current_column)
            pass

    def doubleClicked_(self, f, c):
        self.doubleClicked.emit(f, c)
    
    
    @decorators.NotImplementedWarn
    def setResizePolicy(self, pol):
        self.resize_policy = pol
    
    
    def __getattr__(self, name):
        if name == "Multi":
            return self.MultiSelection
        elif name == "SpreadSheet":
            return 999
        
        print("FIXME:QTable:", name)
        return getattr(QtCore.Qt, name, None)
    
    def valueChanged_(self, item = None):
        
        if item and self.text(item.row(), item.column()) != "":
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
        if isinstance(m, int):
            return
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
    
    def setSelectionMode(self, mode):
        if mode == 999:
            self.setAlternatingRowColors(True)
        else:
            super().setSelectionMode(mode)
        

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
        from pineboolib.utils import format_double
        prev_item = self.item(row, col)
        if prev_item:
            bg_color = prev_item.background()
        
        right = True if isinstance(value, (int, float)) else False
        
        if right:
            value = value if isinstance(value, int) else format_double(value, len("%s" % value), 2)
        
        item =  QtWidgets.QTableWidgetItem(str(value))
        
        if right:
            item.setTextAlignment(QtCore.Qt.AlignVCenter + QtCore.Qt.AlignRight)
            
        self.setItem(row, col, item)
        
        if prev_item:
            self.setCellBackgroundColor(row, col, bg_color)
        
        new_item = self.item(row, col)
        
        if new_item is not None:
            if row in self.read_only_rows or col in self.read_only_cols:
                new_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            else:
                new_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable)


    def adjustColumn(self, k):
        self.horizontalHeader().setSectionResizeMode(k, QtWidgets.QHeaderView.ResizeToContents)

    def setRowReadOnly(self, row, b):      
        if b:
            if row in self.read_only_rows:
                pass
            else:            
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
                pass
            else:
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
    
    def getSorting(self):
        return self.sort_column_
    
    def setSorting(self, col):
        if not super().isSortingEnabled():
            super().setSortingEnabled(True)
        super().sortByColumn(col, QtCore.Qt.AscendingOrder)
        self.sort_column_ = col
        
    
    sorting = property(getSorting, setSorting)
    
    def editCell(self, row, col):
        self.editItem(self.item(row,col))
        