# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets


class FLWidget(QtWidgets.QWidget):

    logo = None
    f_color = None
    p_color = None

    def __init__(self, parent, name):
        super(FLWidget, self).__init__(parent)
        self.setObjectName(name)
