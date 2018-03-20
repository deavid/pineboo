# -*- coding: utf-8 -*-
from xml import etree
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from PyQt5.QtGui import QColor
from lxml.etree import ElementTree

canvas_ = None
header_ = []
name_ = None
pageFormat_ = []


class parse2reportlab(object):

    rml_ = None
    header_ = None
    repeatHeader_ = False
    xmlK_ = None
    pageTemplate_ = None
    pageSize_ = {}
    documment_ = ""
    repeatHeader_ = None
    pagina = 0
    templateName_ = None

    def __init__(self):
        #self.rml_.append('<!DOCTYPE document SYSTEM "rml.dtd">')
        self.rml_ = Element(None)
        self.pagina = 0

    def parseKut(self, name, kut, data):
        self.xmlK_ = etree.ElementTree.fromstring(kut)
        documment = SubElement(self.rml_, "documment")
        self.templateName_ = name
        documment.set("filename", "%s.pdf" % self.templateName_)
        template = SubElement(documment, "template")

        pTemplate = self.newPage(template)

        st = SubElement(documment, "stylesheet")
        story = SubElement(documment, "story")

        #self.pageTemplate_ = self.pageFormat(self.xmlK_)
        #self.header_ = self.pageHeader(self.xmlK_.find("PageHeader"))
        # print(etree.ElementTree.tostring(self.rml_))
        return etree.ElementTree.tostring(self.rml_)

    def newPage(self, parent):
        self.pagina = self.pagina + 1
        el = SubElement(parent, "pageTemplate")
        el.set("id", "Pagina_%s" % self.pagina)
        pG = SubElement(el, "pageGraphics")
        self.pageFormat(self.xmlK_, el)
        self.pageHeader(self.xmlK_.find("PageHeader"), pG)

    def pageFormat(self, xml, parent):
        Custom = None
        BottomMargin = xml.get("BottomMargin")
        LM = xml.get("LeftMargin")
        PO = int(xml.get("PageOrientation"))
        PS = int(xml.get("PageSize"))
        RM = xml.get("RightMargin")
        TM = xml.get("TopMargin")
        if PS in [30, 31]:
            Custom = [int(xml.get("CustomHeightMM")), int(xml.get("CustomWidthMM"))]
        self.pageSize_["W"], self.pageSize_["H"] = self.converPageSize(int(PS), int(PO))
        self.pageSize_["H"] = self.pageSize_["H"] - int(TM)
        self.pageSize_["LM"] = int(LM)
        self.pageSize_["TM"] = int(TM)
        self.pageSize_["RM"] = int(RM)
        parent.set("pageSize", self.converPageSize(PS, PO, Custom))

        parent.set("id", "main")
        parent.set("title", self.templateName_)
        parent.set("author", "pineboo.parse2reportlab")

    def pageHeader(self, xml, parent):
        frecuencia = int(xml.get("PrintFrequency"))
        if frecuencia == 1 or self.pagina_ == 1:  # Siempre o si es primera pagina
            self.processXML(xml, parent)

    def processXML(self, xml, parent):

        for label in xml.findall("Label"):
            self.processLabel(label, parent)

        for line in xml.findall("Line"):
            self.processLine(line, parent)

        for field in xml.findall("Field"):
            self.processField(field, parent)

        for Special in xml.findall("Special"):
            self.processSpecial(Special, parent)

    def processLine(self, xml, parent):

        color = self.getColor(xml.get("Color")).name()
        style = int(xml.get("Style"))
        width = int(xml.get("Width"))
        X1 = int(xml.get("X1"))
        X2 = int(xml.get("X2"))
        Y1 = int(xml.get("Y1"))
        Y2 = int(xml.get("Y2"))

        if X2 > self.pageSize_["W"]:
            X2 = self.pageSize_["W"] - self.pageSize_["RM"]

        lineME = SubElement(parent, "lineMode")
        lineME.set("width", str(width))
        lineE = SubElement(parent, "lines")
        lineE.text = "%s %s %s %s" % (self.getCord("X", X1), self.getCord("Y", Y1), X2, self.getCord("Y", Y2))

    def processLabel(self, xml, parent):
        x = int(xml.get("X"))
        y = int(xml.get("Y"))
        text = xml.get("Text")
        borderStyle = int(xml.get("BorderStyle"))
        BorderWidth = int(xml.get("BorderWidth"))
        borderColor = self.getColor(xml.get("BorderColor")).name()
        bgColor = self.getColor(xml.get("BackgroundColor")).name()
        fgColor = self.getColor(xml.get("ForegroundColor")).name()
        HAlig = int(xml.get("HAlignment"))
        VAlig = int(xml.get("VAlignment"))
        W = int(xml.get("Width"))
        H = int(xml.get("Height"))
        font = xml.get("FontFamily")
        fontSize = int(xml.get("FontSize"))
        fontW = int(xml.get("FontWeight"))
        fontI = int(xml.get("FontItalic"))
        text = xml.get("Text")

        # if font not in canvas_.getAvailableFonts():
        #    font = "Helvetica"

        if fontW > 60:
            text = "<b>%s</b>" % text

        if fontI == 1:
            text = "<i>%s</i>" % text

        if W > self.pageSize_["W"]:
            W = self.pageSize_["W"] - self.pageSize_["RM"]

        if borderStyle == 1:
            # Rectangulo
            sE = SubElement(parent, "stroke")
            sE.set("color", fgColor)
            rectE = SubElement(parent, "rect")
            rectE.set("x", str(self.getCord("X", x)))
            rectE.set("y", str(self.getCord("Y", y)))
            rectE.set("width", str(W - self.getCord("X", x)))
            rectE.set("height", str(H * -1))
            rectE.set("fill", "no")
            rectE.set("stroke", "yes")

        # Calculamos la posicion real contando con el tamaño
        if HAlig == 1:  # Centrado
            x = x + (W / 2)

        if VAlig == 1:  # Centrado
            y = y + (H / 2)

            fontE = SubElement(parent, "setFont")
            fontE.set("name", str(font))
            fontE.set("size", str(fontSize))
            strE = SubElement(parent, "drawString")
            strE.set("x", str(self.getCord("X", x)))
            strE.set("y", str(self.getCord("Y", y)))
            strE.text = xml.get("Text")

    def getColor(self, rgb):
        rgb = rgb.split(",")
        return QColor(int(rgb[0]), int(rgb[1]), int(rgb[2]))

    def getCord(self, t, val):
        ret = None
        if t is "X":
            ret = int(self.pageSize_["LM"]) + int(val)
        elif t is "Y":
            ret = int(self.pageSize_["H"]) - int(val) - int(self.pageSize_["TM"])

        return ret

    def processField(self, xml):
        pass

    def processSpecial(self, xml):
        pass

    def converPageSize(self, size, orientation, Custom=None):
        result_ = None
        r = None
        if size == 0:
            r = [595, 842]  # "A4"
        elif size == 1:
            r = [709, 499]  # "B5"
        elif size == 2:
            r = [612, 791]  # "LETTER"
        elif size == 3:
            r = [612, 1009]  # "legal"
        elif size == 5:
            r = [2384, 3370]  # "A0"
        elif size == 6:
            r = [1684, 2384]  # "A1"
        elif size == 7:
            r = [1191, 1684]  # "A2"
        elif size == 8:
            r = [842, 1191]  # "A3"
        elif size == 9:
            r = [420, 595]  # "A5"
        elif size == 10:
            r = [298, 420]  # "A6"
        elif size == 11:
            r = [210, 298]  # "A7"
        elif size == 12:
            r = [147, 210]  # "A8"
        elif size == 13:
            r = [105, 147]  # "A9"
        elif size == 14:
            r = [4008, 2835]  # "B0"
        elif size == 15:
            r = [2835, 2004]  # "B1"
        elif size == 16:
            r = [125, 88]  # "B10"
        elif size == 17:
            r = [2004, 1417]  # "B2"
        elif size == 18:
            r = [1417, 1001]  # "B3"
        elif size == 19:
            r = [1001, 709]  # "B4"
        elif size == 20:
            r = [499, 354]  # "B6"
        elif size == 21:
            r = [324, 249]  # "B7"
        elif size == 22:
            r = [249, 176]  # "B8"
        elif size == 23:
            r = [176, 125]  # "B9"
        elif size == 24:
            r = [649, 459]  # "C5"
        elif size == 25:
            r = [113, 79]  # "C10"
        elif size == 28:
            r = [1255, 791]  # "LEDGER"
        elif size == 29:
            r = [791, 1255]  # "TABLOID"
        elif size in [30, 31]:
            r = Custom  # "CUSTOM"
        if r is None:
            print("No se encuentra pagesize para %s. Usando A4" % size)
            r = [595, 842]

        if orientation != 0:
            r = [r[1], r[0]]

        return r
