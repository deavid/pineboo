# -*- coding: utf-8 -*-
from pineboolib.core import decorators

P76MM = 76
P57_5MM = 57
P69_5MM = 69


class FLPosPrinter:

    PaperWidth = []
    paperWidth_ = None
    printerName_ = None
    strBuffer = []
    escBuffer = []
    idxBuffer = []
    server_ = None
    queueName_ = None

    def __init__(self):

        self.PaperWidth = [P57_5MM, P69_5MM, P76MM]
        self.paperWidth_ = P76MM

    def __del__(self):
        self.cleanup()

    def paperWidths(self):
        return self.PaperWidth

    def PaperWidth(self):
        return self.paperWidth_

    def setPaperWidth(self, pW):
        self.paperWidth_ = pW

    def printerName(self):
        return self.printerName_

    @decorators.NotImplementedWarn
    def metric(self, m):
        pass

    @decorators.NotImplementedWarn
    def setPrinterName(self, name):
        pass

    @decorators.BetaImplementation
    def cleanup(self):
        if self.strBuffer:
            self.strBuffer = []

        if self.idxBuffer:
            self.idxBuffer = []

        self.idxBuffer = []

    @decorators.NotImplementedWarn
    def flush(self):
        pass

    @decorators.NotImplementedWarn
    def send(self, str_, col=-1, row=-1):
        pass

    @decorators.NotImplementedWarn
    def sendStr(self, c, col, row):
        pass

    @decorators.NotImplementedWarn
    def sendEsc(self, e, col, row):
        pass

    @decorators.NotImplementedWarn
    def cmd(self, c, paint, p):
        pass

    @decorators.BetaImplementation
    def paperWidthToCols(self):
        ret = None
        if self.paperWidth_ is P76MM:
            ret = 80
        elif self.paperWidth_ is P69_5MM:
            ret = 65
        elif self.paperWidth_ is P57_5MM:
            ret = 55
        return ret

    @decorators.NotImplementedWarn
    def initFile(self):
        pass

    @decorators.BetaImplementation
    def initStrBuffer(self):
        if not self.strBuffer:
            self.strBuffer = []
        else:
            self.strBuffer.clear()

    @decorators.BetaImplementation
    def initEscBuffer(self):
        if not self.escBuffer:
            self.escBuffer = []
        else:
            self.escBuffer.clear()

    @decorators.BetaImplementation
    def parsePrinterName(self):
        posdots = self.printerName_.find(":")
        self.server_ = self.printerName_[:posdots]
        self.queueName_ = self.printerName_[posdots:]
        print("FLPosPrinter:parsePinterName", self.server_, self.queueName_)
