# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets  # type: ignore


from typing import Optional, Union, Any, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .qframe import QFrame  # noqa: F401
    from .qgroupbox import QGroupBox  # noqa: F401


class QComboBox(QtWidgets.QComboBox):
    def __init__(self, parent: Optional[Union["QFrame", "QGroupBox"]] = None) -> None:
        super().__init__(parent)

    def insertStringList(self, strl: List[str]) -> None:
        self.insertItems(len(strl), strl)

    def setReadOnly(self, b: bool) -> None:
        super().setEditable(not b)

    def getCurrentItem(self) -> Any:
        return super().currentIndex

    def setCurrentItem(self, i: Union[str, int]) -> Any:
        pos = -1
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

    def getCurrentText(self) -> str:
        return super().currentText()

    def setCurrentText(self, value: str) -> None:
        super().setCurrentText(value)

    currentItem = property(getCurrentItem, setCurrentItem, None, "get/set current item index")
    currentText = property(
        getCurrentText, setCurrentText, None, "get/set current text"
    )  # type: ignore
