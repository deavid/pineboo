# -*- coding: utf-8 -*-
from xml import etree
from reportlab.platypus import SimpleDocTemplate, Image
from reportlab.lib.units import inch
from reportlab.lib import pagesizes

canvas_ = None
header_ = []
name_ = None


def parseKut(t, kut):
    global canvas_, name_

    tree = etree.ElementTree.fromstring(kut)
    name_ = t
    canvas_ = pageFormat(tree)
    header_ = pageHeader(tree.find("PageHeader"))

    # DetailLevel
    # DetailFooter
    # PageFooter
    print("CANVAS", canvas_)
    return canvas_


def pageFormat(xml):
    global name_
    BottomMargin = xml.get("BottomMargin")
    LM = xml.get("LeftMargin")
    PO = xml.get("PageOrientation")
    PS = xml.get("PageSize")
    RM = xml.get("RightMargin")
    TM = xml.get("TopMargin")

    return SimpleDocTemplate("%s.pdf" % name_, pagesize=converPageSize(int(PS), int(PO)), rightMargin=int(RM), leftMargin=int(LM), topMargin=int(TM))


def pageHeader(xml):
    global header_
    frecuencia = xml.get("PrintFrequency")
    altura = xml.get("Height")
    processXML(xml, header_)


def processXML(xml, parent):

    for label in xml.findall("Label"):
        processLabel(label, parent)

    for line in xml.findall("Line"):
        processLine(line, parent)

    for field in xml.findall("Field"):
        processLine(field, parent)

    for Special in xml.findall("Special"):
        processLine(Special, parent)


def processLabel(xml, parent):
    pass


def processLine(xml, parent):
    pass


def processField(xml, parent):
    pass


def processSpecial(xml, parent):
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

    result_ = getattr(pagesizes, r, None)

    if result_ is None:
        print("No se encuentra pagesize para", size)

    if orientation != 0:
        result_ = landscape(result_)

    return result_
