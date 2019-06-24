# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets


class QWidget(QtWidgets.QWidget):
    def child(self, name):
        return self.findChild(QtWidgets.QWidget, name)
