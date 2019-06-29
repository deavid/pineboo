# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
import logging
from PyQt5.QtCore import pyqtProperty

from pineboolib.plugins.dgi.dgi_qt.dgi_objects.qbuttongroup import QButtonGroup
from typing import Optional

logger = logging.getLogger(__name__)


class QRadioButton(QtWidgets.QRadioButton):

    dg_id = None

    def __init__(self, parent: Optional[QButtonGroup] = None) -> None:
        super().__init__(parent)
        self.setChecked(False)
        self.dg_id = None

        self.clicked.connect(self.send_clicked)

    def setButtonGroupId(self, id):
        self.dg_id = id
        if self.parent() and hasattr(self.parent(), "selectedId"):
            if self.dg_id == self.parent().selectedId:
                self.setChecked(True)

    def send_clicked(self):
        if self.parent() and hasattr(self.parent(), "selectedId"):
            self.parent().presset.emit(self.dg_id)

    def isChecked(self):
        return super().isChecked()

    def setChecked(self, b: bool) -> None:
        super().setChecked(b)

    def getText(self):
        return super().getText()

    def setText(self, t: str) -> None:
        super().setText(t)

    checked = pyqtProperty(bool, isChecked, setChecked)
    text = pyqtProperty(str, getText, setText)
