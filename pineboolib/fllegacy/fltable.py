# -*- coding: utf-8 -*-

from pineboolib.qt3_widgets.qtable import QTable
from pineboolib.core import decorators


class FLTable(QTable):
    AlwaysOff = None

    @decorators.NotImplementedWarn
    def setColumnMovingEnabled(self, b):
        pass

    @decorators.NotImplementedWarn
    def setVScrollBarMode(self, mode):
        pass

    @decorators.NotImplementedWarn
    def setHScrollBarMode(self, mode):
        pass
