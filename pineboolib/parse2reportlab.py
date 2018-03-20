# -*- coding: utf-8 -*-
from xml import etree
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Image, Paragraph
from reportlab.lib.units import inch, mm
from reportlab.lib import pagesizes
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
from PyQt5.QtGui import QColor

canvas_ = None
header_ = []
name_ = None
styles = getSampleStyleSheet()
page_ = {}


def parseKut(t, kut):
    global canvas_, name_

    tree = etree.ElementTree.fromstring(kut)
    name_ = t
    canvas_ = pageFormat(tree)

    pageHeader(tree.find("PageHeader"))

    # DetailLevel
    # DetailFooter
    # PageFooter
    print("CANVAS", canvas_)
    canvas_.save()
    return canvas_


def pageFormat(xml):
    global page_
    BottomMargin = xml.get("BottomMargin")
    LM = xml.get("LeftMargin")
    PO = xml.get("PageOrientation")
    PS = xml.get("PageSize")
    RM = xml.get("RightMargin")
    TM = xml.get("TopMargin")
    # return SimpleDocTemplate("%s.pdf" % name_, pagesize=converPageSize(int(PS), int(PO)), rightMargin=int(RM), leftMargin=int(LM), topMargin=int(TM))
    page_["W"], page_["H"] = pagesize = converPageSize(int(PS), int(PO))
    page_["H"] = page_["H"] - int(TM)
    page_["LM"] = int(LM)
    page_["TM"] = int(TM)
    page_["RM"] = int(RM)
    return canvas.Canvas("/home/jose/%s.pdf" % name_, pagesize=converPageSize(int(PS), int(PO)))


def pageHeader(xml):
    global header_, page_
    frecuencia = xml.get("PrintFrequency")
    page_["headerH"] = xml.get("Height")
    processXML(xml, header_)
    # frecuencia si se repite en otras paginas


def processXML(xml, parent):

    for label in xml.findall("Label"):
        processLabel(label)

    for line in xml.findall("Line"):
        processLine(line)

    for field in xml.findall("Field"):
        processLine(field)

    for Special in xml.findall("Special"):
        processLine(Special)


def processLine(xml):
    global page_

    color = getColor(xml.get("Color")).name()
    style = int(xml.get("Style"))
    width = int(xml.get("Width"))
    X1 = int(xml.get("X1"))
    X2 = int(xml.get("X2"))
    Y1 = int(xml.get("Y1"))
    Y2 = int(xml.get("Y2"))

    if X2 > page_["W"]:
        X2 = page_["W"] - page_["RM"]

    canvas_.line(getCord("X", X1), getCord("Y", Y1), X2, getCord("Y", Y2))


def processLabel(xml):
    global page_
    x = int(xml.get("X"))
    y = int(xml.get("Y"))
    text = xml.get("Text")
    borderStyle = int(xml.get("BorderStyle"))
    BorderWidth = int(xml.get("BorderWidth"))
    borderColor = getColor(xml.get("BorderColor")).name()
    bgColor = getColor(xml.get("BackgroundColor")).name()
    fgColor = getColor(xml.get("ForegroundColor")).name()
    HAlig = int(xml.get("HAlignment"))
    VAlig = int(xml.get("VAlignment"))
    W = int(xml.get("Width"))
    H = int(xml.get("Height"))
    font = xml.get("FontFamily")
    fontSize = int(xml.get("FontSize"))
    fontW = int(xml.get("FontWeight"))

    if font not in canvas_.getAvailableFonts():
        font = "Helvetica"

    if fontW > 60:
        font = "%s-Bold" % font

    if W > page_["W"]:
        W = page_["W"] - page_["RM"]

    if borderStyle == 1:
        # Rectangulo
        canvas_.setStrokeColor(fgColor)
        #canvas_.setFillColor(bgColor, True)
        #print("Longitud", W)
        #print("Altitud", H)
        #print("AltoD", page_["H"])
        #print("AnchoD", page_["W"])
        # print(canvas_.getAvailableFonts())
        canvas_.rect(getCord("X", x), getCord("Y", y),  W - getCord("X", x), H * -1, stroke=True, fill=False)

    # Calculamos la posicion real contando con el tamaño
    if HAlig == 1:  # Centrado
        x = x + (W / 2)

    if VAlig == 1:  # Centrado
        y = y + (H / 2)

    canvas_.setFont(font, fontSize)
    canvas_.drawString(getCord("X", x), getCord("Y", y), xml.get("Text"))


def getColor(rgb):
    rgb = rgb.split(",")
    return QColor(int(rgb[0]), int(rgb[1]), int(rgb[2]))


def getCord(t, val):
    global page_
    ret = None
    if t is "X":
        ret = int(page_["LM"]) + int(val)
    elif t is "Y":
        ret = int(page_["H"]) - int(val) - int(page_["TM"])

    return ret


def processField(xml):
    pass


def processSpecial(xml):
    pass


def converPageSize(size, orientation):
    result_ = None
    r = None
    if size == 0:
        r = "A4"
    elif size == 1:
        r = "B5"
    elif size == 2:
        r = "LETTER"
    elif size == 3:
        r = "legal"
    elif size == 5:
        r = "A0"
    elif size == 6:
        r = "A1"
    elif size == 7:
        r = "A2"
    elif size == 8:
        r = "A3"
    elif size == 9:
        r = "A5"
    elif size == 10:
        r = "A6"
    elif size == 11:
        r = "A7"
    elif size == 12:
        r = "A8"
    elif size == 13:
        r = "A9"
    elif size == 14:
        r = "B0"
    elif size == 15:
        r = "B1"
    elif size == 17:
        r = "B2"
    elif size == 18:
        r = "B3"
    elif size == 19:
        r = "B4"
    elif size == 20:
        r = "B6"

    print("---->", r)
    result_ = getattr(pagesizes, r, None)

    if result_ is None:
        print("No se encuentra pagesize para", size)

    if orientation != 0:
        result_ = landscape(result_)

    return result_
