# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets


class QMainWindow(QtWidgets.QMainWindow):
    def child(self, n, c=None):
        ret = None

        if c is None:
            c = QtCore.QObject
        ret = self.findChild(c, n)
        return ret
