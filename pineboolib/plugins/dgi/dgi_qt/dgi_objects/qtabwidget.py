# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
import logging

logger = logging.getLogger(__name__)


class QTabWidget(QtWidgets.QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.Top = self.North
        self.Bottom = self.South
        self.Left = self.West
        self.Right = self.East

    def setTabEnabled(self, tab, enabled):

        idx = self.indexByName(tab)
        if idx is None:
            return

        return QtWidgets.QTabWidget.setTabEnabled(self, idx, enabled)

    def showPage(self, tab):

        idx = self.indexByName(tab)
        if idx is None:
            return

        return QtWidgets.QTabWidget.setCurrentIndex(self, idx)

    def indexByName(self, tab):

        idx = None
        if isinstance(tab, int):
            return tab
        elif not isinstance(tab, str):
            logger.error("ERROR: Unknown type tab name or index:: QTabWidget %r", tab)
            return None

        try:
            for idx in range(self.count()):
                if self.widget(idx).objectName() == tab.lower():
                    return idx
        except ValueError:
            logger.error("ERROR: Tab not found:: QTabWidget, tab name = %r", tab)
        return None

    def removePage(self, idx):
        if isinstance(idx, int):
            self.removeTab(idx)
