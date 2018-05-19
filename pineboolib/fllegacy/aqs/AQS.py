# -*- coding: utf-8 -*-
from PyQt5.QtGui import QColor, QCloseEvent
from pineboolib.fllegacy.aqs.AQObjects import AQSql as AQSql_legacy

AQSql = AQSql_legacy


class AQS(object):

    Close = None

    def __init__(self):
        print("Eoo")
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
