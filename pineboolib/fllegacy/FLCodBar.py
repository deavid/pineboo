# # -*- coding: utf-8 -*-
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmapCache, QPixmap
from PyQt5.QtWidgets import qApp
from pineboolib import decorators
from pineboolib import qsatype

BARCODE_ANY = 0
BARCODE_EAN = 1
BARCODE_UPC = 2
BARCODE_ISBN = 3
BARCODE_39 = 4
BARCODE_128 = 5
BARCODE_128B = 6
BARCODE_128C = 7
BARCODE_128RAW = 7
BARCODE_I25 = 8
BARCODE_CBR = 9
BARCODE_MSI = 10
BARCODE_PLS = 11
BARCODE_93 = 12


class FLCodBar(object):

    barcode = {}
    p = None
    pError = None
    proc = None
    readingStdout = None
    writingStdout = None

    @decorators.BetaImplementation
    def __init__(self, value=None, type_=None, margin=None, scale=None, cut=None, rotation=None, text_flag=False, fg=QtCore.Qt.black, bg=QtCore.Qt.white, res=72):
        if value in [None, 0]:
            self.proc = qsatype.Process()
            self.p = None
            self.pError = QPixmap()
            self.readingStdout = False
            self.writingStdout = False
            self.fillDefault(self.barcode)
        else:
            if isinstance(value, str):
                self.proc = qsatype.Process()
                self.p = None
                self.pError = QPixmap()
                self.readingStdout = False
                self.writingStdout = False
                self.barcode["value"] = value
                self.barcode["type"] = type_
                self.barcode["margin"] = margin
                self.barcode["scale"] = scale
                self.barcode["cut"] = cut
                self.barcode["rotation"] = rotation
                self.barcode["text"] = text_flag
                self.barcode["fg"] = fg
                self.barcode["bg"] = bg
                self.barcode["valid"] = False
                self.barcode["res"] = res

            else:
                self._copyBarCode(value, self.barcode)

    def __del__(self):
        if self.proc:
            del self.proc

    @decorators.BetaImplementation
    def pixmap(self):

        if not self.p:
            key = "%s%s%s" % (self.barcode["value"], self.barcode["type"], self.barcode["res"])

            if not QPixmapCache.find(key):
                self._createBarcode()
                if self.barcode["valid"]:
                    key = "%s%s%s" % (self.barcode["value"], self.barcode["type"], self.barcode["res"])
                    QPixmapCache.insert(key, self.p)
            else:
                self.barcode["valid"] = True

        return self.p

    def pixmapError(self):
        return self.pError

    def value(self):
        return self.barcode["value"]

    def type_(self):
        return self.barcode["type"]

    def margin(self):
        return self.barcode["margin"]

    def scale(self):
        return self.barcode["scale"]

    def cut(self):
        return self.barcode["cut"]

    def text(self):
        return self.barcode["text"]

    def rotation(self):
        return self.barcode["rotation"]

    def fg(self):
        return self.barcode["fg"]

    def bg(self):
        return self.barcode["bg"]

    def setData(self, d):
        self.barcode = d

    def validBarcode(self):
        return self.barcode["valid"]

    def setCaption(self, caption):
        self.barcode["caption"] = caption

    def caption(self):
        return self.barcode["caption"]

    def setValue(self, value):
        self.barcode["value"] = value

    def setType(self, type_):
        self.barcode["type"] = type_

    def setMargin(self, margin):
        self.barcode["margin"] = margin

    def setScale(self, scale):
        self.barcode["scale"] = scale

    def setCut(self, cut):
        self.barcode["cut"] = cut

    def setText(self, text):
        self.barcode["text"] = text

    def setRotation(self, rotation):
        self.barcode["rotation"] = rotation

    def setFg(self, fg):
        self.barcode["fg"] = fg

    def setBg(self, bg):
        self.barcode["bg"] = bg

    def setRes(self, res):
        self.barcode["res"] = res

    def data(self):
        return self.barcode

    def fillDefault(self, data):
        data["bg"] = QtCore.Qt.white
        data["fg"] = QtCore.Qt.black
        data["margin"] = 10
        data["text"] = True
        data["value"] = "1234567890"
        data["type"] = BARCODE_39
        data["scale"] = 1.0
        data["cut"] = 1.0
        data["rotation"] = 0
        data["caption"] = "Static"
        data["valid"] = False
        data["res"] = 72

    def cleanUp(self):
        self.p.resize(0, 0)
        self.pError.resize(0, 0)

    def nameToType(self, name):
        n = name.lower()
        if n == "any":
            return BARCODE_ANY
        elif n == "ean":
            return BARCODE_EAN
        elif n == "upc":
            return BARCODE_UPC
        elif n == "isbn":
            return BARCODE_ISBN
        elif n == "code39":
            return BARCODE_39
        elif n == "code128":
            return BARCODE_128
        elif n == "code128c":
            return BARCODE_128C
        elif n == "code128b":
            return BARCODE_128B
        elif n == "codei25":
            return BARCODE_I25
        elif n == "code128r":
            return BARCODE_128RAW
        elif n == "cbr":
            return BARCODE_CBR
        elif n == "msi":
            return BARCODE_MSI
        elif n == "pls":
            return BARCODE_PLS
        elif n == "code93":
            return BARCODE_93
        else:
            return BARCODE_ANY

    def typeToName(self, type_):
        if type_ == BARCODE_ANY:
            return "ANY"
        elif type_ == BARCODE_EAN:
            return "EAN"
        elif type_ == BARCODE_UPC:
            return "UPC"
        elif type_ == BARCODE_ISBN:
            return "ISBN"
        elif type_ == BARCODE_39:
            return "Code39"
        elif type_ == BARCODE_128:
            return "Code128"
        elif type_ == BARCODE_128C:
            return "Code128C"
        elif type_ == BARCODE_128B:
            return "Code128B"
        elif type_ == BARCODE_I25:
            return "CodeI25"
        elif type_ == BARCODE_128RAW:
            return "Code128RAW"
        elif type_ == BARCODE_CBR:
            return "CBR"
        elif type_ == BARCODE_MSI:
            return "MSI"
        elif type_ == BARCODE_PLS:
            return "PLS"
        elif type_ == BARCODE_93:
            return "Code93"
        else:
            return "ANY"

    @decorators.BetaImplementation
    @QtCore.pyqtSlot()
    def readPixmapStdout(self):
        if self.writingStdout:
            qApp.processEvents()
            return

        self.p.loadFormData(self.proc.readStdout(), "PNG")
        if self.p:
            m = QWMatrix
            m.rotate(self.barcode["rotation"])
            self.p.xForm(m)
            self.barcode["valid"] = True

        self.readingStdout = False

    @QtCore.pyqtSlot()
    def writingStdoutFinished(self):
        self.writingStdout = False
        self.readPixmapStdout()

    @decorators.NotImplementedWarn
    def _createBarcode(self):
        pass

    def _copyBarCode(self, source, dest):
        dest["value"] = source["value"]
        dest["type"] = source["type"]
        dest["margin"] = source["margin"]
        dest["scale"] = source["scale"]
        dest["cut"] = source["cut"]
        dest["rotation"] = source["rotation"]
        dest["text"] = source["text"]
        dest["caption"] = source["caption"]
        dest["valid"] = source["valid"]
        dest["fg"] = source["fg"]
        dest["bg"] = source["bg"]
        dest["x"] = source["x"]
        dest["y"] = source["y"]
        dest["res"] = source["res"]
