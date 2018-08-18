# -*- coding: utf-8 -*-
import logging
import datetime
from xml import etree


class parsertools(object):
    _fix_altura = None

    def __init__(self):
        self.logger = logging.getLogger("ParseTools")
        self.pagina = 0
        self._fix_altura = 0.927

    def loadKut(self, data):
        data = data.encode("ISO-8859-15")
        return etree.ElementTree.fromstring(data)

    def heightCorrection(self, value):
        return value * self._fix_altura

    def convertToNode(self, data):

        node = self._parser_tools.Node()
        for k in data.keys():
            node.setAttribute(k, data.get(k))

        return node

    def getHeight(self, xml):
        h = int(xml.get("Height"))
        if h:
            return h
        else:
            return 0

    def getSpecial(self, name, page_num):
        self.logger.debug("%s:getSpecial %s" % (__name__, name))
        ret = "None"
        if name == "Fecha":
            ret = str(datetime.date.__format__(
                datetime.date.today(), "%d.%m.%Y"))
        if name == "NúmPágina":
            ret = str(page_num)

        return ret

    def calculated(self, field, dataType, Precision, data=None):

        ret_ = field
        if dataType == 5:  # Imagen
            from pineboolib.plugings.kugar.pnkugarplugins import refkey2cache
            ret_ = parseKey(field)
        elif data:
            ret_ = data.get(field)

        return ret_

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
            self.logger.warn(
                "porcessXML:No se encuentra pagesize para %s. Usando A4" % size)
            r = [595, 842]

        if orientation != 0:
            r = [r[1], r[0]]

        return r


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
                self.logger.warn(
                    "rml:refkey2cache No se ha podido guardar la imagen %s" % imgFile)
                ret = None

        ret = imgFile

    return ret
