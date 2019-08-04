# -*- coding: utf-8 -*-
import datetime
from typing import Union

from PyQt5 import QtCore  # type: ignore
from pineboolib.qt3_widgets.qdateedit import QDateEdit
from pineboolib.application.utils.date_conversion import convert_to_qdate
from pineboolib.application.types import Date


class FLDateEdit(QDateEdit):

    valueChanged = QtCore.pyqtSignal()
    DMY = "dd-MM-yyyy"
    _parent = None

    def __init__(self, parent, name) -> None:
        super().__init__(parent, name)
        self.setMinimumWidth(90)
        self.setMaximumWidth(90)
        self._parent = parent

    def setOrder(self, order: str) -> None:
        self.setDisplayFormat(order)

    def getDate(self) -> str:
        return super().getDate()

    def setDate(self, d: Union[str, datetime.date, Date] = None) -> None:  # type: ignore
        if d in (None, "NAN", ""):
            date = QtCore.QDate.fromString(str("01-01-2000"), "dd-MM-yyyy")
        else:
            date = convert_to_qdate(d)

        super().setDate(date)
        self.setStyleSheet("color: black")

    date = property(getDate, setDate)  # type: ignore
