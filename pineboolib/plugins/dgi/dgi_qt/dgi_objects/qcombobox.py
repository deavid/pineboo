# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets  # type: ignore


from pineboolib.plugins.dgi.dgi_qt.dgi_objects.qframe import QFrame
from pineboolib.plugins.dgi.dgi_qt.dgi_objects.qgroupbox import QGroupBox
from typing import Optional, Union
from typing import Any, Sized


class QComboBox(QtWidgets.QComboBox):
    def __init__(self, parent: Optional[Union[QFrame, QGroupBox]] = None) -> None:
        super().__init__(parent)

    def insertStringList(self, strl: Sized) -> None:
        self.insertItems(len(strl), strl)

    def setReadOnly(self, b: bool) -> None:
        super().setEditable(not b)

    def getCurrentItem(self) -> Any:
        return super().currentIndex

    def setCurrentItem(self, i) -> Any:
        pos = None
        if isinstance(i, str):
            pos = 0
            size_ = self.model().rowCount()
            for n in range(size_):
                item = self.model().index(n, 0)
                if item.data() == i:
                    pos = n
                    break

        else:
            pos = i

        return super().setCurrentIndex(pos)

    currentItem = property(getCurrentItem, setCurrentItem, None, "get/set current item index")
