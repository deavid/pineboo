# -*- coding: utf-8 -*-
from xml import etree
from xml.etree.ElementTree import Element, SubElement
from PyQt5.QtGui import QColor
from pineboolib.utils import filedir
import pineboolib
import logging
import traceback
import datetime

canvas_ = None
header_ = []
name_ = None
pageFormat_ = []


class kut2rml(object):
    logger = logging.getLogger("kut2rml")
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
    _parser_tools = None

    def __init__(self):
        from pineboolib.utils import checkDependencies

        dict_ = {"z3c.rml": "z3c.rml"}
        checkDependencies(dict_)
        self.rml_ = Element(None)
        self.correccionAncho_ = 0.927

    def parse(self, name, kut, dataString):
        if pineboolib.is_deployed():
            self.logger.error("Reportlab not available for Bundles")
            return None

        from reportlab.pdfbase import pdfmetrics
        from pineboolib.plugins.kugar.parsertools import parsertools

        self._parser_tools = parsertools()

        try:
            self.xmlK_ = self._parser_tools.loadKut(kut)
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
        # template = SubElement(documment, "template")

        self.xmlData_ = etree.ElementTree.fromstring(dataString)
        self.processKutDetails(self.xmlK_, self.xmlData_, documment)

        # st = SubElement(documment, "stylesheet")
        # story = SubElement(documment, "story")

        # self.pageTemplate_ = self.pageFormat(self.xmlK_)
        # self.header_ = self.pageHeader(self.xmlK_.find("PageHeader"))
        # print(etree.ElementTree.tostring(self.rml_))
        res_ = etree.ElementTree.tostring(self.rml_)
        res_ = '<!DOCTYPE document SYSTEM "rml_1_0.dtd">%s' % res_.decode("utf-8")
        pdfname = pineboolib.project.get_temp_dir()
        pdfname += "/%s.pdf" % datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        pPDF = parsePDF()
        pPDF.parse(res_, pdfname)

        return pdfname

    def newPage(self, parent):
        self.pagina = self.pagina + 1
        # el = SubElement(parent, "pageTemplate")
        # el.set("id", "main")
        # el.set("id", "main" if self.pagina == 1 else "Pagina_%s" % self.pagina)
        # pG = SubElement(el, "pageDrawing")
        pG = SubElement(parent, "pageDrawing")
        self.pageFormat(self.xmlK_, parent)
        self.actualVSize[str(self.pagina)] = self.pageSize_["TM"]
        # el.set("pagesize", parent.get("pagesize"))
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
        self.pageSize_["W"], self.pageSize_["H"] = self._parser_tools.converPageSize(int(PS), int(PO))
        # self.pageSize_["H"] = self.pageSize_["H"] - int(TM)
        self.pageSize_["LM"] = int(LM)
        self.pageSize_["TM"] = int(TM)
        self.pageSize_["RM"] = int(RM)
        self.pageSize_["BM"] = int(BM)
        pS = self._parser_tools.converPageSize(PS, PO, Custom)
        parent.set("pagesize", "(%s,%s)" % (pS[0], pS[1]))
        parent.set("leftMargin", str(LM))
        parent.set("showBoundary", "1")
        self.maxVSize[str(self.pagina)] = self.pageSize_["H"]  # Fix!!??
        # parent.set("id", "main")
        # parent.set("title", self.templateName_)
        # parent.set("author", "pineboo.parse2reportlab")

    def drawLine(self, xml, parent):

        # color = self.getColor(xml.get("Color")).name()
        # style = int(xml.get("Style"))
        width = int(xml.get("Width"))
        X1 = int(xml.get("X1"))
        X2 = int(xml.get("X2"))
        Y1 = self._parser_tools.heightCorrection(int(xml.get("Y1")))
        Y2 = self._parser_tools.heightCorrection(int(xml.get("Y2")))

        X2 = self.fixRMarging(X2)

        lineME = SubElement(parent, "lineMode")
        lineME.set("width", str(width))
        lineE = SubElement(parent, "lines")
        lineE.text = "%s %s %s %s" % (self.getCord("X", X1), self.getCord("Y", Y1), X2, self.getCord("Y", Y2))

    def processText(self, xml, parent, data=None):
        isImage = False
        text = xml.get("Text")
        # BorderWidth = int(self.getOption(xml, "BorderWidth"))
        # borderColor = self.getColor(xml.get("BorderColor")).name()
        font = xml.get("FontFamily")
        fontSize = int(xml.get("FontSize"))
        fontW = int(self.getOption(xml, "FontWeight"))
        fontI = int(self.getOption(xml, "FontItalic"))

        if xml.tag == "Field" and data is not None:
            text = data.get(xml.get("Field"))
            if text == "None":
                return
        if xml.tag == "Special":
            text = self._parser_tools.getSpecial(text[1 : len(text) - 1], self.pagina)

        if xml.tag == "CalculatedField":
            if xml.get("FunctionName"):
                fN = xml.get("FunctionName")
                try:
                    nodo = self._parser_tools.convertToNode(data)
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
                text = self._parser_tools.calculated(text, xml.get("DataType"), xml.get("Precision"), data)

            # else:
            #    text = self.calculated(xml.get("Field"), xml.get("DataType"), xml.get("Precision"), data)

            if int(xml.get("DataType")) == 5:
                print("Añadida imagen", text)
                isImage = True

        if text:
            if text.startswith(filedir("../tempdata")):
                isImage = True

        # precision = xml.get("Precision")
        # negValueColor = xml.get("NegValueColor")
        # Currency = xml.get("Currency")
        # dataType = xml.get("Datatype")
        # commaSeparator = xml.get("CommaSeparator")
        # dateFormat = xml.get("DateFormat")
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
            self.logger.warning("porcessXML: Registering %s font" % font)
            self.registeredFonts.append(fontName)

            rF = SubElement(self.docInitSubElemet_, "registerTTFont")
            rF.set("faceName", font)
            # rF.set("fileName", fileF)

        if self.getOption(xml, "BorderStyle") == "1":
            self.drawRec(xml, parent)

        if not isImage:
            self.setFont(parent, font, fontSize)
            self.drawText(xml, parent, text)
        # else:
        #    self.drawImage(xml, parent, text)

    def drawRec(self, xml, parent):
        # Rectangulo
        # bgColor = self.getColor(xml.get("BackgroundColor")).name()
        fgColor = self.getColor(xml.get("ForegroundColor")).name()

        sE = SubElement(parent, "stroke")
        sE.set("color", fgColor)
        rectE = SubElement(parent, "rect")
        self.setPos(rectE, xml)
        self.setSize(xml, rectE, True)

        rectE.set("fill", "no")
        rectE.set("stroke", "yes")
        # print("Creando rectangulo", W, H)

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
        # y = xml.get("Y")

        # if W > self.pageSize_["W"]:
        #    W = self.pageSize_["W"] - self.pageSize_["RM"]
        W = self.fixRMarging(W, x)
        # H = self.fixTMargin(H, y)
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
            if xml.get("Text") and obj.tag == "drawString":
                # Ancho_ = int(xml.get("FontSize")) * len(xml.get("Text"))
                Alto_ = int(xml.get("FontSize"))
                # x = x + (W / 2) - Ancho_
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
        obj.set("y", str(self.getCord("Y", self._parser_tools.heightCorrection(y))))

    def fixRMarging(self, W, x=None):
        ret = W

        if x:
            # Controla si se sobrepasa el margen derecho
            if self.pageSize_["W"] - self.pageSize_["RM"] < W + self.getCord("X", x):
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
        if t == "X":  # Horizontal
            ret = int(self.pageSize_["LM"]) + int(val) * self.correccionAncho_
            # ret = val
        elif t == "Y":  # Vertical
            # ret = int(self.pageSize_["H"]) - int(val) - int(self.pageSize_["TM"] - self.pageSize_["BM"] + self.actualVSize[str(self.pagina)])
            # ret = int(self.pageSize_["H"]) - int(val) - int(self.actualVSize[str(self.pagina)] * self.correcionAltura_)
            ret = int(self.pageSize_["H"]) - int(val) - self._parser_tools.heightCorrection(self.actualVSize[str(self.pagina)])
        return ret

        return ret

    def getColor(self, rgb):
        ret = None
        if rgb is None:
            ret = QColor(0, 0, 0)
        else:
            if rgb.find(",") > -1:
                rgb_ = rgb.split(",")
                ret = QColor(int(rgb_[0]), int(rgb_[1]), int(rgb_[2]))
            elif len(rgb) == 3:
                ret = QColor(int(rgb[0]), int(rgb[1]), int(rgb[2]))
            else:
                ret = QColor(int(rgb[0:2]), int(rgb[3:5]), int(rgb[6:8]))

        return ret

    def pageFooter(self, xml, parent):
        frecuencia = int(self.getOption(xml, "PrintFrequency"))
        if frecuencia == 1 or self.pagina == 1:  # Siempre o si es primera pagina
            # self.actualVSize[str(self.pagina)] = self.maxVSize[str(self.pagina)] + (self.getHeight(xml) - self.pageSize_["BM"]) * self.correcionAltura_
            self.actualVSize[str(self.pagina)] = self.maxVSize[str(self.pagina)] + self._parser_tools.heightCorrection(self._parser_tools.getHeight(xml))
            # self.logger.warning("PAGE_FOOTER BOTTON %s" % self.actualVSize[str(self.pagina)])
            self.processXML(xml, parent)

    def getOption(self, xml, name):
        ret = xml.get(name)
        if ret is None:
            ret = 0

        return ret

    def pageHeader(self, xml, parent):
        frecuencia = int(self.getOption(xml, "PrintFrequency"))
        if frecuencia == 1 or self.pagina == 1:  # Siempre o si es primera pagina
            self.processXML(xml, parent)

    def processKutDetails(self, xml, xmlData, parent):
        pageG = self.newPage(parent)
        prevLevel = 0
        level = None
        for data in xmlData.findall("Row"):
            level = int(data.get("level"))
            if prevLevel > level:
                pageG = self.processData("DetailFooter", xml, data, pageG, prevLevel)
            elif prevLevel < level:
                pageG = self.processData("DetailHeader", xml, data, pageG, level)

            pageG = self.processData("Detail", xml, data, pageG, level, parent)

            prevLevel = level

        if level:
            for l in reversed(range(level + 1)):
                pageG = self.processData("DetailFooter", xml, data, pageG, l)

        if xml.find("PageFooter"):
            pageG = self.pageFooter(xml.find("PageFooter"), pageG)
        elif xml.find("AddOnFooter"):
            pageG = self.pageFooter(xml.find("AddOnFooter"), pageG)

    def processData(self, name, xml, data, parent, level, docParent=None):
        listDF = xml.findall(name)
        for dF in listDF:
            if dF.get("Level") == str(level):
                if name == "Detail" and (dF.get("DrawIf") is None or data.get(dF.get("DrawIf")) is not None):
                    heightCalculated = self._parser_tools.getHeight(dF) + self.actualVSize[str(self.pagina)]
                    # Buscamos si existe DetailFooter y PageFooter y miramos si
                    # no excede tamaño
                    for dFooter in xml.findall("DetailFooter"):
                        if dFooter.get("Level") == str(level):
                            heightCalculated += self._parser_tools.getHeight(dFooter)
                    pageFooter = xml.get("PageFooter")
                    if pageFooter is not None:
                        if self.pagina == 1 or pageFooter.get("PrintFrecuency") == "1":
                            heightCalculated += self._parser_tools.getHeight(pageFooter)

                    heightCalculated += self.pageSize_["BM"]

                    # Si nos pasamos
                    if heightCalculated > self.maxVSize[str(self.pagina)]:
                        self.pageFooter(xml.find("PageFooter"), parent)  # Pie de página
                        parent = self.newPage(docParent)  # Nueva página

                if dF.get("DrawIf") is None or data.get(dF.get("DrawIf")) is not None:
                    self.processXML(dF, parent, data)
                    # self.logger.debug("%s_BOTTON = %s" % (name.upper(), self.actualVSize[str(self.pagina)]))
        return parent

    def processXML(self, xml, parent, data=None):

        if xml.tag == "DetailFooter":
            if xml.get("PlaceAtBottom") == "true":
                self.actualVSize[str(self.pagina)] = self.pageSize_["H"] - self._parser_tools.getHeight(xml)

        for child in xml.iter():
            if child.tag == "Label":
                self.processText(child, parent, data)
            elif child.tag == "Line":
                self.drawLine(child, parent)
            elif child.tag == "Field":
                self.processText(child, parent, data)
            elif child.tag == "Special":
                # print(etree.ElementTree.tostring(child))
                self.processText(child, parent)
            elif child.tag == "CalculatedField":
                self.processText(child, parent, data)
            else:
                if child.tag not in ("PageFooter", "PageHeader", "DetailFooter", "Detail", "AddOnHeader", "AddOnFooter", "DetailHeader"):
                    self.logger.warning("porcessXML: Unknown tag %s." % child.tag)

        self.actualVSize[str(self.pagina)] += self._parser_tools.getHeight(xml)


class parsePDF(object):
    logger = logging.getLogger("parsePDF")

    def parse(self, xml, filename):
        if pineboolib.is_deployed():
            self.logger.error("RML2PDF not available on Bundles")
            return

        from z3c.rml import rml2pdf

        res_ = rml2pdf.parseString(xml).read()
        with open(filename, "wb") as w:
            w.write(res_)

        w.close()
