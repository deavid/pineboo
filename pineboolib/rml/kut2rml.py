# -*- coding: utf-8 -*-
from xml import etree
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from PyQt5.QtGui import QColor
from pineboolib.utils import filedir
import logging
import os
from datetime import date
from reportlab.pdfbase import pdfmetrics

canvas_ = None
header_ = []
name_ = None
pageFormat_ = []


class kut2rml(object):
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
    actualVSize = {}
    maxVSize = {}
    docInitSubElemet_ = None
    registeredFonts = []

    def __init__(self):
        self.rml_ = Element(None)
        self.pagina = 0
        self.logger = logging.getLogger("kut2rml")
        self.correcionAltura_ = 0.927

    def parse(self, name, kut, dataString):
        self.xmlK_ = etree.ElementTree.fromstring(kut)
        documment = SubElement(self.rml_, "document")
        # Para definir tipos de letra
        self.docInitSubElemet_ = SubElement(documment, "docinit")
        for f in pdfmetrics.standardFonts:
            self.registeredFonts.append(f)

        # FIXME Añadir todas las fuentes de share/fonts/

        self.templateName_ = name
        documment.set("filename", "%s.pdf" % self.templateName_)
        documment.set("invariant", "1")
        #template = SubElement(documment, "template")

        data = etree.ElementTree.fromstring(dataString).findall("Row")
        self.processKutDetails(self.xmlK_, data, documment)

        #st = SubElement(documment, "stylesheet")
        #story = SubElement(documment, "story")

        #self.pageTemplate_ = self.pageFormat(self.xmlK_)
        #self.header_ = self.pageHeader(self.xmlK_.find("PageHeader"))
        # print(etree.ElementTree.tostring(self.rml_))
        res_ = etree.ElementTree.tostring(self.rml_)
        res_ = '<!DOCTYPE document SYSTEM \"rml_1_0.dtd\">%s' % res_.decode("utf-8")
        return res_

    def processKutDetails(self, xml, xmlData, parent):
        pageG = self.newPage(parent)
        prevLevel = 0
        for data in xmlData:
            level = int(data.get("level"))
            if prevLevel > level:
                pageG = self.processData("DetailFooter", xml, data, pageG, prevLevel)

            pageG = self.processData("Detail", xml, data, pageG, level, parent)

            prevLevel = level

        print("final!!")
        pageG = self.processData("DetailFooter", xml, data, pageG, level)

        pageG = self.pageFooter(xml.find("PageFooter"), pageG)

    def processData(self, name, xml, data, parent, level, docParent=None):
        listDF = xml.findall(name)
        for dF in listDF:
            if dF.get("Level") == str(level):
                if name is "Detail":
                    heightCalculated = self.getHeight(dF) + self.actualVSize[str(self.pagina)]
                    # Buscamos si existe DetailFooter y PageFooter y miramos si no excede tamaño
                    for dFooter in xml.findall("DetailFooter"):
                        if dFooter.get("Level") == str(level):
                            heightCalculated += self.getHeight(dFooter)
                    pageFooter = xml.get("PageFooter")
                    if pageFooter is not None:
                        if self.pagina == 1 or pageFooter.get("PrintFrecuency") == "1":
                            heightCalculated += self.getHeight(pageFooter)

                    heightCalculated += self.pageSize_["BM"]

                    if heightCalculated > self.maxVSize[str(self.pagina)]:  # Si nos pasamos
                        self.pageFooter(xml.find("PageFooter"), parent)  # Pie de página
                        parent = self.newPage(docParent)  # Nueva página

                self.processXML(dF, parent, data)
                self.logger.debug("%s_BOTTON = %s" % (name.upper(), self.actualVSize[str(self.pagina)]))
        return parent

    def newPage(self, parent):
        self.pagina = self.pagina + 1
        #el = SubElement(parent, "pageTemplate")
        #el.set("id", "main")
        #el.set("id", "main" if self.pagina == 1 else "Pagina_%s" % self.pagina)
        #pG = SubElement(el, "pageDrawing")
        pG = SubElement(parent, "pageDrawing")
        self.pageFormat(self.xmlK_, parent)
        self.actualVSize[str(self.pagina)] = self.pageSize_["TM"]
        #el.set("pagesize", parent.get("pagesize"))
        self.pageHeader(self.xmlK_.find("PageHeader"), pG)
        return pG

    def getHeight(self, xml):
        h = int(xml.get("Height"))
        if h:
            return h
        else:
            return 0

    def pageFormat(self, xml, parent):
        Custom = None
        BM = xml.get("BottomMargin")
        LM = xml.get("LeftMargin")
        PO = int(xml.get("PageOrientation"))
        PS = int(xml.get("PageSize"))
        RM = xml.get("RightMargin")
        TM = xml.get("TopMargin")
        if PS in [30, 31]:
            Custom = [int(xml.get("CustomHeightMM")), int(xml.get("CustomWidthMM"))]
        self.pageSize_["W"], self.pageSize_["H"] = self.converPageSize(int(PS), int(PO))
        #self.pageSize_["H"] = self.pageSize_["H"] - int(TM)
        self.pageSize_["LM"] = int(LM)
        self.pageSize_["TM"] = int(TM)
        self.pageSize_["RM"] = int(RM)
        self.pageSize_["BM"] = int(BM)
        pS = self.converPageSize(PS, PO, Custom)
        parent.set("pagesize", "(%s,%s)" % (pS[0], pS[1]))
        parent.set("leftMargin", str(LM))
        parent.set("showBoundary", "1")
        self.maxVSize[str(self.pagina)] = self.pageSize_["H"]  # Fix!!??
        #parent.set("id", "main")
        #parent.set("title", self.templateName_)
        #parent.set("author", "pineboo.parse2reportlab")

    def pageHeader(self, xml, parent):
        frecuencia = int(xml.get("PrintFrequency"))
        if frecuencia == 1 or self.pagina_ == 1:  # Siempre o si es primera pagina
            self.processXML(xml, parent)

        #self.actualVSize[str(self.pagina)] += self.getHeight(xml)
        self.logger.warn("PAGE_HEADER BOTTON", self.actualVSize[str(self.pagina)])

    def pageFooter(self, xml, parent):
        frecuencia = int(xml.get("PrintFrequency"))
        if frecuencia == 1 or self.pagina_ == 1:  # Siempre o si es primera pagina
            #self.actualVSize[str(self.pagina)] = self.maxVSize[str(self.pagina)] + (self.getHeight(xml) - self.pageSize_["BM"]) * self.correcionAltura_
            self.actualVSize[str(self.pagina)] = self.maxVSize[str(self.pagina)] + self.getHeight(xml) * self.correcionAltura_
            self.logger.warn("PAGE_FOOTER BOTTON", self.actualVSize[str(self.pagina)])
            self.processXML(xml, parent)

    def processXML(self, xml, parent, data=None):

        for child in xml.iter():
            if child.tag == "Label":
                self.processText(child, parent)
            elif child.tag == "Line":
                self.processLine(child, parent)
            elif child.tag == "Field":
                self.processText(child, parent, data)
            elif child.tag == "Special":
                # print(etree.ElementTree.tostring(child))
                self.processText(child, parent)
            else:
                if child.tag not in ("PageFooter", "PageHeader", "DetailFooter", "Detail"):
                    self.logger.warn("porcessXML: Unknown tag %s." % child.tag)

        self.actualVSize[str(self.pagina)] += self.getHeight(xml)

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
        lineE.text = "%s %s %s %s" % (self.getCord("X", X1), self.getCord("Y", Y1 * self.correcionAltura_), X2, self.getCord("Y", Y2 * self.correcionAltura_))

    def processText(self, xml, parent, data=None):
        isImage = False
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
        if xml.tag == "Field" and data is not None:
            text = data.get(xml.get("Field"))
            if text == "None":
                return
        if xml.tag == "Special":
            text = self.getSpecial(text[1:len(text) - 1])

        if text.startswith(filedir("../tempdata")):
            isImage = True

        precision = xml.get("Precision")
        negValueColor = xml.get("NegValueColor")
        Currency = xml.get("Currency")
        dataType = xml.get("Datatype")
        commaSeparator = xml.get("CommaSeparator")
        dateFormat = xml.get("DateFormat")
        """
            if precision:
                print("Fix Field.precision", precision)
            if negValueColor:
                print("Fix Field.negValueColor", negValueColor)
            if Currency:
                print("Fix Field.Currency", Currency)
            if dataType:
                print("Fix Field.dataType", dataType)
            if commaSeparator:
                print("Fix Field.commaSeparator", commaSeparator)
            if dateFormat:
                print("Fix Field.dateFormat", dateFormat)
        """
        if font not in self.registeredFonts:
            font = "Helvetica"
        fontName = font

        if fontW > 60 and fontSize > 10:
            fontB = "%s-Bold" % font
            if fontB in self.registeredFonts:
                font = fontB

        if fontI == 1:
            fontIt = None
            if font.find("Bold") == -1:
                fontIt = "%s-" % font
            else:
                fontIt = "%s"

            if "%sOblique" % fontIt in self.registeredFonts:
                font = "%sOblique" % fontIt
            elif "%sItalic" % fontIt in self.registeredFonts:
                font = "%sItalic" % fontIt

        if font not in self.registeredFonts:
            self.logger.warn("porcessXML: Registering %s font" % font)
            self.registeredFonts.append(fontName)

            rF = SubElement(self.docInitSubElemet_, "registerTTFont")
            rF.set("faceName", font)
            rF.set("fileName", fileF)

        # if W > self.pageSize_["W"]:
        #    W = self.pageSize_["W"] - self.pageSize_["RM"]

        if borderStyle == 1:
            # Rectangulo
            sE = SubElement(parent, "stroke")
            sE.set("color", fgColor)
            rectE = SubElement(parent, "rect")
            rectE.set("x", str(self.getCord("X", x)))
            # if (self.pageSize_["H"] - self.pageSize_["TM"]) < self.getCord("Y", y):  # Controla si se sobrepasa el margen superior
            #    self.logger.debug("Alto max %s , actual %s" % ((self.pageSize_["H"] - self.pageSize_["TM"]), self.getCord("Y", y)))
            #    rectE.set("y", str(self.pageSize_["H"] - self.pageSize_["TM"]))
            # else:
            rectE.set("y", str(self.getCord("Y", y * self.correcionAltura_)))
            if self.pageSize_["W"] - self.pageSize_["RM"] < W + self.getCord("X", x):  # Controla si se sobrepasa el margen derecho
                self.logger.debug("Limite Ancho pasado %s de %s" % (self.pageSize_["W"] - self.pageSize_["RM"], W))
                W = self.pageSize_["W"] - self.pageSize_["RM"] - self.getCord("X", x)

            rectE.set("width", str(W))
            rectE.set("height", str(H * -1))
            rectE.set("fill", "no")
            rectE.set("stroke", "yes")
            #print("Creando rectangulo", W, H)

        # Calculamos la posicion real contando con el tamaño
        if HAlig == 1:  # Centrado
            x = x + (W / 2) - (fontW / 1.75)
        elif HAlig == 2:
            x = x + (fontW / 1.75)

        if VAlig == 1:  # Centrado
            y = y + (H / 2) + (H / 4)

        if not isImage:
            fontE = SubElement(parent, "setFont")
            fontE.set("name", font)
            fontE.set("size", str(fontSize))
            strE = SubElement(parent, "drawString")
            #strE.set("fontName", font)
            #strE.set("fontSize", str(fontSize))

            strE.text = text
        else:
            strE = SubElement(parent, "image")
            strE.set("file", text)

        strE.set("x", str(self.getCord("X", x)))
        strE.set("y", str(self.getCord("Y", y * self.correcionAltura_)))

    def getColor(self, rgb):
        rgb = rgb.split(",")
        return QColor(int(rgb[0]), int(rgb[1]), int(rgb[2]))

    def getCord(self, t, val):
        ret = None
        if t is "X":  # Horizontal
            ret = int(self.pageSize_["LM"]) + int(val)
        elif t is "Y":  # Vertical
            #ret = int(self.pageSize_["H"]) - int(val) - int(self.pageSize_["TM"] - self.pageSize_["BM"] + self.actualVSize[str(self.pagina)])
            ret = int(self.pageSize_["H"]) - int(val) - int(self.actualVSize[str(self.pagina)] * self.correcionAltura_)

        return ret

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
            self.logger.warn("porcessXML:No se encuentra pagesize para %s. Usando A4" % size)
            r = [595, 842]

        if orientation != 0:
            r = [r[1], r[0]]

        return r

    def getSpecial(self, name):
        self.logger.debug("porcessXML:getSpecial %s" % name)
        ret = "None"
        if name == "Fecha":
            ret = str(date.__format__(date.today(), "%d.%m.%Y"))
        if name == "NúmPágina":
            ret = str(self.pagina)

        return ret
