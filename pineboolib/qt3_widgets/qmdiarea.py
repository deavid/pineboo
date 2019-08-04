# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QMdiArea as QMA  # type: ignore
from PyQt5 import QtCore  # type: ignore
from PyQt5.QtGui import QBrush, QColor
from pineboolib.fllegacy.aqsobjects.aqs import AQS


class QMdiArea(QMA):

    logo = None

    def __init__(self, *args) -> None:
        super().__init__(*args)

        self.setBackground(QBrush(QColor(255, 255, 255)))
        self.logo = AQS.pixmap_fromMimeSource("pineboo-logo.png")
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.logo = self.logo.scaled(self.size(), QtCore.Qt.IgnoreAspectRatio)

    def paintEvent(self, e) -> None:
        super().paintEvent(e)

        # painter = super().viewport()

        # x = self.width() - self.logo.width()
        # y = self.height() - self.logo.height()
        # painter.drawPixmap(x, y, self.logo)
