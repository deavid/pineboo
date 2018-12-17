# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets

class QAction(QtWidgets.QAction):

    activated = QtCore.pyqtSignal()
    _menuText = None
    _objectName = None

    def __init__(self, parent=None):
        super(QAction, self).__init__(parent)
        self.triggered.connect(self.send_activated)
        self._name = None
        self._menuText = None

    def send_activated(self, b=None):
        self.activated.emit()

    def getName(self):
        return self.objectName()

    def setName(self, n):
        self.setObjectName(n)

    def getMenuText(self):
        return self._menuText

    def setMenuText(self, t):
        self._menuText = t

    name = property(getName, setName)
    menuText = property(getMenuText, setMenuText)