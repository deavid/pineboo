# -*- coding: utf-8 -*-

from PyQt5 import Qt  # type: ignore
from pineboolib.core import decorators
from pineboolib import logging
from pineboolib.qt3_widgets import qlistview
from typing import Any

logger = logging.getLogger("FLListViewItem")


class FLListViewItem(Qt.QStandardItem):

    _expandable: bool = False
    _key = None
    _open = None
    _root = None
    _index_child: int = 0

    def __init__(self, parent=None) -> None:
        super().__init__()
        self._root = False
        self.setExpandable(False)
        self._parent = None
        self.setKey("")
        self.setEditable(False)
        self._index_child = 0
        if parent:
            # Comprueba que tipo de parent es
            if isinstance(parent, qlistview.QListView):
                # self._root = True
                parent.model().setItem(0, 0, self)
            else:
                if isinstance(parent, self):
                    # print("Añadiendo nueva linea a", parent.text(0))
                    parent.appendRow(self)

        # if parent:
        #    self._parent = parent
        #    self._row = self._parent.model().rowCount()
        #    if self._parent.model().item(0,0) is not None:
        #        self._parent.model().item(0,0).setChild(self._row,0, self)
        #        self._parent.model().item(0,0)._rowcount += 1
        #    else:
        #        self._parent.model().setItem(self._row,0,self)

        #    self._rows = self._parent.model().item(0,0)._rowcount - 1

    def firstChild(self) -> Any:
        self._index_child = 0
        item = self.child(self._index_child)
        return item

    def nextSibling(self) -> Any:
        self._index_child += 1
        item = self.child(self._index_child)
        return item

    def isExpandable(self) -> bool:
        return self._expandable
        # return True if self.child(0) is not None or not self.parent() else False

    def setText(self, *args) -> None:
        # print("Seteando", args, self.parent())
        # logger.warning("Seteo texto %s" , args, stack_info = True )
        col = 0
        if len(args) == 1:
            value = args[0]
        else:
            col = args[0]
            value = str(args[1])

        if col == 0:
            # if self._root:
            # print("Inicializando con %s a %s" % ( value, self.parent()))
            super().setText(value)
        else:
            item = self.parent().child(self.row(), col)
            if item is None:
                item = FLListViewItem()
                self.parent().setChild(self.row(), col, item)

            item.setText(value)

    def text(self, col) -> str:
        ret = ""
        if col == 0:
            ret = super().text()

        return str(ret)

    @decorators.NotImplementedWarn
    def setPixmap(self, *args):
        pass

    def setExpandable(self, b) -> None:
        self._expandable = b

    def setKey(self, k) -> None:
        self._key = str(k)

    def key(self) -> Any:
        if self.parent() and self.column() > 0:
            return self.parent().child(self.row(), 0).key()
        return self._key

    def setOpen(self, o) -> None:
        self._open = o

    def del_(self) -> None:
        del self
