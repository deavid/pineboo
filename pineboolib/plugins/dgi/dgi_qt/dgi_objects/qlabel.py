# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore, QtGui  # type: ignore
from typing import Any


class QLabel(QtWidgets.QLabel):
    def get_text(self):
        return super().text()

    def setText(self, text: str) -> None:
        if not isinstance(text, str):
            text = str(text)
        super().setText(text)

    def setPixmap(self, pix) -> None:

        if isinstance(pix, QtGui.QIcon):
            pix = pix.pixmap(32, 32)
        super(QLabel, self).setPixmap(pix)

    @QtCore.pyqtSlot(bool)
    def setShown(self, b):
        self.setVisible(b)

    def getAlign(self) -> Any:
        return super().alignment()

    def setAlign(self, alignment_) -> None:
        self.setAlignment(alignment_)

    def get_palette_fore_ground(self) -> Any:
        return self.palette().text().color()

    def set_palette_fore_ground(self, color) -> None:
        pal = self.palette()
        pal.setColor(pal.WindowText, color)
        self.setPalette(pal)

    alignment = property(getAlign, setAlign)
    text = property(get_text, setText)
    paletteForegroundColor = property(get_palette_fore_ground, set_palette_fore_ground)
