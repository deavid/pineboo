# # -*- coding: utf-8 -*-
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmapCache, QPixmap, QColor
from PyQt5.QtWidgets import qApp
from pineboolib import decorators

import barcode
import traceback
import logging


logger = logging.getLogger(__name__)

BARCODE_ANY = 0
BARCODE_EAN = 1
BARCODE_EAN_8 = 2
BARCODE_EAN_13 = 3
BARCODE_EAN_14 = 4
BARCODE_UPC = 5
BARCODE_UPC_A = 6
BARCODE_JAN = 7
BARCODE_ISBN = 8
BARCODE_ISBN_10 = 9
BARCODE_ISBN_13 = 10
BARCODE_ISSN = 11
BARCODE_39 = 12
BARCODE_128 = 13
BARCODE_PZN = 14
BARCODE_ITF = 15
BARCODE_GS1 = 16
BARCODE_GTIN = 17


class FLCodBar(object):

    barcode = {}
    p = None
    pError = None

    @decorators.BetaImplementation
    def __init__(self, value=None, type_=None, margin=None, scale=None, cut=None, rotation=None, text_flag=False, fg=QtCore.Qt.black, bg=QtCore.Qt.white, res=72):

        self.barcode["value"] = ""

        if value in [None, 0]:
            self.p = None
            self.pError = QPixmap()
            self.readingStdout = False
            self.writingStdout = False
            self.fillDefault(self.barcode)
        else:
            if isinstance(value, str):
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

    @decorators.BetaImplementation
    def pixmap(self):
        if not self.p:
            key = "%s%s%s" % (self.barcode["value"], self.barcode["type"], self.barcode["res"])

            if not QPixmapCache.find(key):
                self._createBarcode()
                if self.barcode["valid"]:
                    key = "%s%s%s" % (self.barcode["value"], self.barcode["type"], self.barcode["res"])
                    if key:
                        QPixmapCache.insert(key, self.p)
            else:
                self.p = QPixmapCache.find(key)
                self.barcode["valid"] = True

        if not self.p:
            self.barcode["valid"] = False

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
        data["bg"] = "white"
        data["fg"] = "black"
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
        elif n == "ean-8":
            return BARCODE_EAN_8
        elif n == "ean-13":
            return BARCODE_EAN_13
        elif n == "ean-14":
            return BARCODE_EAN_14
        elif n == "upc":
            return BARCODE_UPC
        elif n == "upc-a":
            return BARCODE_UPC_A
        elif n == "jan":
            return BARCODE_JAN
        elif n == "isbn":
            return BARCODE_ISBN
        elif n == "isbn-10":
            return BARCODE_ISBN_10
        elif n == "isbn-13":
            return BARCODE_ISBN_13
        elif n == "issn":
            return BARCODE_ISSN
        elif n == "code39":
            return BARCODE_39
        elif n == "code128":
            return BARCODE_128
        elif n == "pzn":
            return BARCODE_PZN
        elif n == "itf":
            return BARCODE_ITF
        elif n == "gs1":
            return BARCODE_GS1
        elif n == "gtin":
            return BARCODE_GTIN
        else:
            logger.warning("Formato no soportado (%s)\nSoportados: %s." % (n, barcode.PROVIDED_BARCODES))
            return BARCODE_ANY

    def typeToName(self, type_):
        if type_ == BARCODE_ANY:
            return "ANY"
        elif type_ == BARCODE_EAN:
            return "EAN"
        elif type_ == BARCODE_EAN_8:
            return "EAN-8"
        elif type_ == BARCODE_EAN_13:
            return "EAN-13"
        elif type_ == BARCODE_EAN_14:
            return "EAN-14"
        elif type_ == BARCODE_UPC:
            return "UPC"
        elif type_ == BARCODE_UPC_A:
            return "UPC-A"
        elif type_ == BARCODE_JAN:
            return "JAN"
        elif type_ == BARCODE_ISBN:
            return "ISBN"
        elif type_ == BARCODE_ISBN_10:
            return "ISBN-10"
        elif type_ == BARCODE_ISBN_13:
            return "ISBN-13"
        elif type_ == BARCODE_ISSN:
            return "ISSN"
        elif type_ == BARCODE_39:
            return "Code39"
        elif type_ == BARCODE_128:
            return "Code128"
        elif type_ == BARCODE_PZN:
            return "PZN"
        elif type_ == BARCODE_ITF:
            return "ITF"
        elif type_ == BARCODE_GS1:
            return "GS1"
        elif type_ == BARCODE_GTIN:
            return "GTIN"
        else:
            return "ANY"

    @decorators.BetaImplementation
    def _createBarcode(self):
        if self.barcode["value"] == "":
            return
        if self.barcode["type"] == BARCODE_ANY:
            logger.warning("Usando %s por defecto" % self.typeToName(BARCODE_128))
            self.barcode["type"] = BARCODE_128

        type_ = self.typeToName(self.barcode["type"])
        value_ = self.barcode["value"]
        bg_ = self.barcode["bg"]
        fg_ = self.barcode["fg"]
        if not isinstance(self.barcode["bg"], str):
            bg_ = QColor(self.barcode["bg"]).name()

        if not isinstance(self.barcode["fg"], str):
            fg_ = QColor(self.barcode["fg"]).name()

        margin_ = self.barcode["margin"] / 10
        bar_ = None
        render_options = {
            'module_width': 0.2,
            'module_height': 5,  # 15
            'text_distance': 1.0,  # 5.0
            'background': bg_.lower(),
            'foreground': fg_.lower(),
            'write_text': self.barcode["text"],
            'font_size': 10,
            'text': value_,
            'quiet_zone': margin_,  # 6.5
        }

        try:
            from barcode.writer import ImageWriter
            from PIL.ImageQt import ImageQt
            barC = barcode.get_barcode_class(type_.lower())
            bar_ = barC(u'%s' % value_, writer=ImageWriter())
            b = bar_.render(render_options)
            qim = ImageQt(b)
            self.p = QPixmap.fromImage(qim)
        except Exception:
            print(traceback.format_exc())
            self.barcode["valid"] = False
            self.p = None

        if self.p:
            # Escalar
            if self.barcode["scale"] != 1.0:
                wS_ = self.barcode["x"] * self.barcode["scale"]
                hS_ = self.barcode["y"] * self.barcode["scale"]
                self.p = self.p.scaled(wS_, hS_)

            self.barcode["x"] = self.p.width()
            self.barcode["y"] = self.p.height()

            # FALTA: res , cut y rotation

            self.barcode["valid"] = True
        else:
            self.barcode["valid"] = False

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
