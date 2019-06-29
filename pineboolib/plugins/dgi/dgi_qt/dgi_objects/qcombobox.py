# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets


from pineboolib.plugins.dgi.dgi_qt.dgi_objects.qframe import QFrame
from pineboolib.plugins.dgi.dgi_qt.dgi_objects.qgroupbox import QGroupBox
from typing import Optional, Union
class QComboBox(QtWidgets.QComboBox):
    def __init__(self, parent: Optional[Union[QFrame, QGroupBox]] = None) -> None:
        super().__init__(parent)

        self.setCurrentItem = self.setCurrentIndex

    def insertStringList(self, strl):
        self.insertItems(len(strl), strl)

    def setReadOnly(self, b: bool) -> None:
        super().setEditable(not b)
