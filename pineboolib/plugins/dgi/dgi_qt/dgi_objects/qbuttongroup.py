# -*- coding: utf-8 -*-

from pineboolib.plugins.dgi.dgi_qt.dgi_objects.qgroupbox import QGroupBox
from pineboolib import decorators

class QButtonGroup(QGroupBox):

    def __init__(self, *args):
        super(QButtonGroup, self).__init__(*args)

    @decorators.NotImplementedWarn
    def setLineWidth(self, w):
        pass