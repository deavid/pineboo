# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui  # type: ignore
from pineboolib.core import decorators
from PyQt5.QtCore import pyqtSignal  # type: ignore
from typing import Any, List


class QListView(QtWidgets.QWidget):

    _resizeable = True
    _clickable = True
    _root_is_decorated = None
    _default_rename_action = None
    _tree = None
    _cols_labels: List[str]
    _key = None
    _root_item = None
    _current_row: int

    doubleClicked = pyqtSignal(object)
    selectionChanged = pyqtSignal(object)
    expanded = pyqtSignal(object)
    collapsed = pyqtSignal(object)

    def __init__(self, parent=None) -> None:
        super().__init__(parent=None)
        lay = QtWidgets.QVBoxLayout(self)
        self._tree = QtWidgets.QTreeView(self)
        lay.addWidget(self._tree)
        self._tree.setModel(QtGui.QStandardItemModel())
        self._cols_labels = []
        self._root_is_decorated = False
        self._key = ""
        self._root_item = None
        self._current_row = -1
        self._tree.doubleClicked.connect(self.doubleClickedEmit)
        self._tree.clicked.connect(self.singleClickedEmit)
        self._tree.activated.connect(self.singleClickedEmit)

    def singleClickedEmit(self, index) -> None:
        if index.column() != 0:
            index = index.sibling(index.row(), 0)
        else:
            index = index.sibling(index.row(), index.column())
        item = index.model().itemFromIndex(index)

        self.selectionChanged.emit(item)

    def doubleClickedEmit(self, index) -> None:
        item = index.model().itemFromIndex(index)
        self.doubleClicked.emit(item)

    def addItem(self, t) -> None:
        from pineboolib import pncontrolsfactory

        self._current_row = self._current_row + 1
        item = pncontrolsfactory.FLListViewItem()
        item.setEditable(False)
        item.setText(t)
        if self._tree is not None:
            self._tree.model().setItem(self._current_row, 0, item)

    @decorators.NotImplementedWarn
    def setItemMargin(self, m):
        self.setContentsMargins(m, m, m, m)

    def setHeaderLabel(self, labels) -> None:
        if isinstance(labels, str):
            labels = [labels]

        if self._tree is not None:
            self._tree.model().setHorizontalHeaderLabels(labels)
        self._cols_labels = labels

    def setColumnText(self, col, new_value) -> None:
        i = 0
        new_list = []
        for old_value in self._cols_labels:
            value = new_value if i == col else old_value
            new_list.append(value)

        self._cols_labels = new_list

    def addColumn(self, text) -> None:
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

    def clear(self) -> None:
        self._cols_labels = []

    @decorators.NotImplementedWarn
    def defaultRenameAction(self):
        return self._default_rename_action

    @decorators.NotImplementedWarn
    def setDefaultRenameAction(self, b):
        self._default_rename_action = b

    def model(self) -> Any:
        if self._tree is not None:
            return self._tree.model()
        else:
            raise Exception("No hay _tree")
