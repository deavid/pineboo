# -*- coding: utf-8 -*-
import logging

from PyQt5.QtGui import QColor


class pnkugarparsetools(object):

    def __init__(self):
        self.logger = logging.getLogger("PNKugarParseTools")
        self.pagina = 0

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

    def pageFooter(self, xml, parent):
        frecuencia = int(self.getOption(xml, "PrintFrequency"))
        if frecuencia == 1 or self.pagina == 1:  # Siempre o si es primera pagina
            #self.actualVSize[str(self.pagina)] = self.maxVSize[str(self.pagina)] + (self.getHeight(xml) - self.pageSize_["BM"]) * self.correcionAltura_
            self.actualVSize[str(self.pagina)] = self.maxVSize[str(self.pagina)] + self.getHeight(xml) * self.correcionAltura_
            #self.logger.warn("PAGE_FOOTER BOTTON %s" % self.actualVSize[str(self.pagina)])
            self.processXML(xml, parent)

    def getSpecial(self, name):
        self.logger.debug("porcessXML:getSpecial %s" % name)
        ret = "None"
        if name == "Fecha":
            from datetime import date
            ret = str(date.__format__(date.today(), "%d.%m.%Y"))
        if name == "NúmPágina":
            ret = str(self.pagina)

    def getOption(self, xml, name):
        ret = xml.get(name)
        if ret is None:
            ret = 0

        return ret

    def calculated(self, field, dataType, Precision, data=None):

        ret = field
        if int(dataType) == 5:  # Imagen
            from pineboolib.plugings.kugar.pnkugarplugins import refkey2cache
            ret = parseKey(field)
        elif data:
            ret = data.get(field)

        return ret

    def convertToNode(self, data):
        node = Node()
        for k in data.keys():
            node.setAttribute(k, data.get(k))

        return node

    def getHeight(self, xml):
        h = int(xml.get("Height"))
        if h:
            return h
        else:
            return 0

    def pageHeader(self, xml, parent):
        frecuencia = int(self.getOption(xml, "PrintFrequency"))
        if frecuencia == 1 or self.pagina == 1:  # Siempre o si es primera pagina
            self.processXML(xml, parent)

    def processKutDetails(self, xml, xmlData, parent):
        pageG = self.newPage(parent)
        prevLevel = 0
        for data in xmlData.findall("Row"):
            level = int(data.get("level"))
            if prevLevel > level:
                pageG = self.processData("DetailFooter", xml, data, pageG, prevLevel)
            elif prevLevel < level:
                pageG = self.processData("DetailHeader", xml, data, pageG, level)

            pageG = self.processData("Detail", xml, data, pageG, level, parent)

            prevLevel = level

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
                if name is "Detail" and (dF.get("DrawIf") is None or data.get(dF.get("DrawIf")) is not None):
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

                if dF.get("DrawIf") is None or data.get(dF.get("DrawIf")) is not None:
                    self.processXML(dF, parent, data)
                    #self.logger.debug("%s_BOTTON = %s" % (name.upper(), self.actualVSize[str(self.pagina)]))
        return parent

    def processXML(self, xml, parent, data=None):

        if xml.tag == "DetailFooter":
            if xml.get("PlaceAtBottom") == "true":
                self.actualVSize[str(self.pagina)] = self.pageSize_["H"] - self.getHeight(xml)

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
                    self.logger.warn("porcessXML: Unknown tag %s." % child.tag)

        self.actualVSize[str(self.pagina)] += self.getHeight(xml)


class Node(object):
    list_ = None

    def __init__(self):
        self.list_ = {}


def parseKey(name=None):
    ret = None
    value = None
    if name is None:
        ret = None
    else:
        q = FLSqlQuery()
        # q.setForwardOnly(True)
        q.exec_("SELECT contenido FROM fllarge WHERE refkey='%s'" % name)
        if q.next():
            value = clearXPM(q.value(0))

        imgFile = filedir("../tempdata")
        imgFile += "/%s.png" % name
        if not os.path.exists(imgFile) and value:
            pix = QPixmap(value)
            if not pix.save(imgFile):
                self.logger.warn("rml:refkey2cache No se ha podido guardar la imagen %s" % imgFile)
                ret = None

        ret = imgFile

    return ret
