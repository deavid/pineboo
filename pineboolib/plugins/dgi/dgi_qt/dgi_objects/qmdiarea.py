# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QMdiArea  # type: ignore
from PyQt5 import QtCore  # type: ignore


class QMdiArea(QMdiArea):

    logo = None

    def __init__(self, *args):
        super().__init__(*args)
        from pineboolib import pncontrolsfactory

        self.setBackground(pncontrolsfactory.QBrush(pncontrolsfactory.QColor(255, 255, 255)))
        self.logo = pncontrolsfactory.AQS.Pixmap_fromMineSource("pineboo-logo.png")
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.logo = self.logo.scaled(self.size(), QtCore.Qt.IgnoreAspectRatio)

    def paintEvent(self, e):
        super().paintEvent(e)

        # painter = super().viewport()

        # x = self.width() - self.logo.width()
        # y = self.height() - self.logo.height()
        # painter.drawPixmap(x, y, self.logo)
