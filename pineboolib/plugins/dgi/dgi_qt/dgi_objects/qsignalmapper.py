# -*- coding: utf-8 -*-
from PyQt5 import QtCore

class QSignalMapper(QtCore.QSignalMapper):

    def __init__(self, parent, name):
        super(QSignalMapper, self).__init__(parent)
        self.setObjectName(name)