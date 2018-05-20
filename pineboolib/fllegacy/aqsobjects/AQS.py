# -*- coding: utf-8 -*-
from PyQt5.QtGui import QColor, QCloseEvent

class AQS(object):

    Close = None

    def __init__(self):
        self.Close = QCloseEvent

    def ColorDialog_getColor(self, color=None, parent=None, name=None):
        from PyQt5.QtWidgets import QColorDialog
        from PyQt5.QtGui import QColor

        if color is None:
            color = QColor.black()

        if isinstance(color, str):
            color = QColor()

        cL = QColorDialog(color, parent)
        return cL.getColor()
