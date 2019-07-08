# -*- coding: utf-8 -*-

from pineboolib import pncontrolsfactory
from pineboolib.core import decorators


class FLTable(pncontrolsfactory.QTable):
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
