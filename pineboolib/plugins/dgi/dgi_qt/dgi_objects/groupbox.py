# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
from pineboolib.plugins.dgi.dgi_qt.dgi_objects.qgroupbox import QGroupBox

class GroupBox(QGroupBox):
    def __init__(self, *args):
        super(GroupBox, self).__init__(*args)
        self._layout = QtWidgets.QVBoxLayout()
        self.setLayout(self._layout)

    def add(self, _object):
        self._layout.addWidget(_object)