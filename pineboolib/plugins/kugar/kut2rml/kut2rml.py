# -*- coding: utf-8 -*-
from xml import etree
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from PyQt5.QtGui import QColor
from pineboolib.utils import filedir
import pineboolib
import logging
import traceback
import os
import sys
import datetime
from pineboolib.plugins.kugar.pnkugarparsetools import pnkugarparsetools

canvas_ = None
header_ = []
name_ = None
pageFormat_ = []


class kut2rml(pnkugarparsetools):
    rml_ = None
    header_ = None
    repeatHeader_ = False
    xmlK_ = None
    xmlData_ = None
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
    parseTools_ = None

    def __init__(self):
        self.rml_ = Element(None)
        self.logger = logging.getLogger("kut2rml")
        self.correcionAltura_ = 0.927
        self.correccionAncho_ = 0.927

    def parse(self, name, kut, dataString):
        if not pineboolib.project._DGI.isDeployed():
            from reportlab.pdfbase import pdfmetrics
        else:
            return None

        try:
            self.xmlK_ = etree.ElementTree.fromstring(kut)
        except Exception:
            self.logger.exception("KUT2RML: Problema al procesar %s.kut\n" % name)
            return False
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

        self.xmlData_ = etree.ElementTree.fromstring(dataString)
        self.processKutDetails(self.xmlK_, self.xmlData_, documment)

        #st = SubElement(documment, "stylesheet")
        #story = SubElement(documment, "story")

        #self.pageTemplate_ = self.pageFormat(self.xmlK_)
        #self.header_ = self.pageHeader(self.xmlK_.find("PageHeader"))
        # print(etree.ElementTree.tostring(self.rml_))
        res_ = etree.ElementTree.tostring(self.rml_)
        res_ = '<!DOCTYPE document SYSTEM \"rml_1_0.dtd\">%s' % res_.decode("utf-8")
        pdfname = pineboolib.project.getTempDir()
        pdfname += "/%s.pdf" % datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        pPDF = parsePDF()
        pPDF.parse(res_, pdfname)

        return pdfname

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
        if self.xmlK_.find("PageHeader"):
            self.pageHeader(self.xmlK_.find("PageHeader"), pG)
        # elif self.xmlK_.find("AddOnHeader"):
        #    self.pageHeader(self.xmlK_.find("AddOnHeader"), pG)
        return pG

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

    def drawLine(self, xml, parent):

        color = self.getColor(xml.get("Color")).name()
        style = int(xml.get("Style"))
        width = int(xml.get("Width"))
        X1 = int(xml.get("X1"))
        X2 = int(xml.get("X2"))
        Y1 = int(xml.get("Y1")) * self.correcionAltura_
        Y2 = int(xml.get("Y2")) * self.correcionAltura_

        X2 = self.fixRMarging(X2)

        lineME = SubElement(parent, "lineMode")
        lineME.set("width", str(width))
        lineE = SubElement(parent, "lines")
        lineE.text = "%s %s %s %s" % (self.getCord("X", X1), self.getCord("Y", Y1), X2, self.getCord("Y", Y2))

    def processText(self, xml, parent, data=None):
        isImage = False
        text = xml.get("Text")
        BorderWidth = int(self.getOption(xml, "BorderWidth"))
        borderColor = self.getColor(xml.get("BorderColor")).name()
        font = xml.get("FontFamily")
        fontSize = int(xml.get("FontSize"))
        fontW = int(self.getOption(xml, "FontWeight"))
        fontI = int(self.getOption(xml, "FontItalic"))

        if xml.tag == "Field" and data is not None:
            text = data.get(xml.get("Field"))
            if text == "None":
                return
        if xml.tag == "Special":
            text = self.getSpecial(text[1:len(text) - 1])

        if xml.tag == "CalculatedField":
            if xml.get("FunctionName"):
                fN = xml.get("FunctionName")
                try:
                    nodo = self.convertToNode(data)
                    text = str(pineboolib.project.call(fN, [nodo]))
                except Exception:
                    print(traceback.format_exc())
                    return
            else:
                if not data:
                    data = self.xmlData_[0]
                if xml.get("Field"):
                    v = data.get(xml.get("Field"))
                    if v == "None":
                        v = ""
                    text = v

            if text and xml.get("DataType") is not None:
                text = self.calculated(text, xml.get("DataType"), xml.get("Precision"), data)

            # else:
            #    text = self.calculated(xml.get("Field"), xml.get("DataType"), xml.get("Precision"), data)

            if int(xml.get("DataType")) == 5:
                print("Añadida imagen", text)
                isImage = True

        if text:
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

        if self.getOption(xml, "BorderStyle") == "1":
            self.drawRec(xml, parent)

        if not isImage:
            self.setFont(parent, font, fontSize)
            self.drawText(xml, parent, text)
        # else:
        #    self.drawImage(xml, parent, text)

    def drawRec(self, xml, parent):
        # Rectangulo
        bgColor = self.getColor(xml.get("BackgroundColor")).name()
        fgColor = self.getColor(xml.get("ForegroundColor")).name()

        sE = SubElement(parent, "stroke")
        sE.set("color", fgColor)
        rectE = SubElement(parent, "rect")
        self.setPos(rectE, xml)
        self.setSize(xml, rectE, True)

        rectE.set("fill", "no")
        rectE.set("stroke", "yes")
        #print("Creando rectangulo", W, H)

    def drawImage(self, xml, parent, filename):
        strE = SubElement(parent, "image")
        strE.set("file", filename)
        self.setSize(xml, strE)
        self.setPos(strE, xml)

    def drawText(self, xml, parent, text):
        strE = SubElement(parent, "drawString")
        strE.text = text
        self.setPos(strE, xml)

    def setSize(self, xml, obj, reverseH=False):
        rev = 1
        if reverseH is True:
            rev = -1
        W = int(xml.get("Width"))
        H = int(xml.get("Height"))
        x = xml.get("X")
        y = xml.get("Y")

        # if W > self.pageSize_["W"]:
        #    W = self.pageSize_["W"] - self.pageSize_["RM"]
        W = self.fixRMarging(W, x)
        #H = self.fixTMargin(H, y)
        # if self.pageSize_["H"] - self.pageSize_["TM"] < H + self.getCord("Y", y):  # Controla si se sobrepasa el margen derecho
        #    self.logger.debug("Limite Alto pasado %s de %s" % (self.pageSize_["H"] - self.pageSize_["TM"], H))
        #    H = self.pageSize_["H"] - self.pageSize_["TM"] - self.getCord("Y", y)

        obj.set("width", str(W))
        obj.set("height", str(H * rev))

    def setPos(self, obj, xml):

        x = int(xml.get("X"))
        y = int(xml.get("Y"))
        HAlig = int(self.getOption(xml, "HAlignment"))
        VAlig = int(self.getOption(xml, "VAlignment"))
        W = int(xml.get("Width"))
        H = int(xml.get("Height"))

        # Calculamos la posicion real contando con el tamaño
        if xml.tag in ("Label", "Field", "Special", "CalculatedField"):
            if (xml.get("Text") and obj.tag == "drawString"):
                Ancho_ = int(xml.get("FontSize")) * len(xml.get("Text"))
                Alto_ = int(xml.get("FontSize"))
                #x = x + (W / 2) - Ancho_
                y = y - Alto_

                W = self.fixRMarging(W, x)

                if HAlig == 0:  # Izquierda
                    x = x

                if HAlig == 1:  # Centrado
                    x = x + (W / 2)  # Falla un poco revisar

                if HAlig == 2:  # Derecha
                    x = x + W

                if VAlig == 1:  # Centrado
                    y = y + H + (Alto_ / 2) + (Alto_ / 4) - (H / 8)

            if obj.tag == "image":
                x = x
                y = self.fixTMargin(H, y)

            if obj.tag == "rect":
                x = x
                y = y
                if HAlig == 1:  # Centrado
                    x = x

                if VAlig == 1:  # Centrado
                    y = y - (H / 8)

        obj.set("x", str(self.getCord("X", x)))
        obj.set("y", str(self.getCord("Y", y * self.correcionAltura_)))

    def fixRMarging(self, W, x=None):
        ret = W

        if x:
            if self.pageSize_["W"] - self.pageSize_["RM"] < W + self.getCord("X", x):  # Controla si se sobrepasa el margen derecho
                ret = self.pageSize_["W"] - self.pageSize_["RM"] - self.getCord("X", x)
        else:

            if self.pageSize_["W"] - self.pageSize_["RM"] < (W + self.pageSize_["LM"]):
                ret = self.pageSize_["W"] - (self.pageSize_["RM"])

        return ret

    def fixTMargin(self, H, y=None):
        ret = H + int(y)
        if H + self.pageSize_["TM"] > int(y):
            ret = H
        return ret

    def setFont(self, parent, font, size):
        fontE = SubElement(parent, "setFont")
        fontE.set("name", font)
        fontE.set("size", str(size))

    """
    Calcula la coordenada en el nuevo report , segun los tramos ya añadidos 
    """

    def getCord(self, t, val):
        ret = None
        if t is "X":  # Horizontal
            ret = int(self.pageSize_["LM"]) + int(val) * self.correccionAncho_
            #ret = val
        elif t is "Y":  # Vertical
            #ret = int(self.pageSize_["H"]) - int(val) - int(self.pageSize_["TM"] - self.pageSize_["BM"] + self.actualVSize[str(self.pagina)])
            #ret = int(self.pageSize_["H"]) - int(val) - int(self.actualVSize[str(self.pagina)] * self.correcionAltura_)
            ret = int(self.pageSize_["H"]) - int(val) - int(self.actualVSize[str(self.pagina)] * self.correcionAltura_)
        return ret

        return ret


class parsePDF(object):

    def parse(self, xml, filename):
        print(pineboolib.project._DGI.isDeployed())
        if not pineboolib.project._DGI.isDeployed():
            from z3c.rml import document, rml2pdf
        else:
            return

        res_ = rml2pdf.parseString(xml).read()
        with open(filename, 'wb') as w:
            w.write(res_)

        w.close()

    def setAttribute(self, name, value):
        self.list_[name] = value

    def attributeValue(self, name):
        return self.list_[name]
