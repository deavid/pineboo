# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets

class FLCheckBox(QtWidgets.QCheckBox):

    def __init__(self, parent=None, num_rows=None):
        super(FLCheckBox, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)