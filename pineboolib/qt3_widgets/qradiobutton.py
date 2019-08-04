# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets  # type: ignore
from pineboolib import logging
from PyQt5.QtCore import pyqtProperty  # type: ignore

from .qbuttongroup import QButtonGroup
from typing import Optional
from typing import Any

logger = logging.getLogger(__name__)


class QRadioButton(QtWidgets.QRadioButton):

    dg_id = None

    def __init__(self, parent: Optional[QButtonGroup] = None) -> None:
        super().__init__(parent)
        self.setChecked(False)
        self.dg_id = None

        self.clicked.connect(self.send_clicked)

    def setButtonGroupId(self, id) -> None:
        self.dg_id = id
        if self.parent() and hasattr(self.parent(), "selectedId"):
            if self.dg_id == self.parent().selectedId:
                self.setChecked(True)

    def send_clicked(self) -> None:
        if self.parent() and hasattr(self.parent(), "selectedId"):
            self.parent().presset.emit(self.dg_id)

    def isChecked(self) -> Any:
        return super().isChecked()

    def setChecked(self, b: bool) -> None:
        super().setChecked(b)

    def getText(self) -> Any:
        return super().getText()

    def setText(self, t: str) -> None:
        super().setText(t)

    checked = pyqtProperty(bool, isChecked, setChecked)
    text = pyqtProperty(str, getText, setText)
