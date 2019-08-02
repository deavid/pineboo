# -*- coding: utf-8 -*-
"""
Variety of tools for KUT.
"""
import os
import sys
import datetime
import fnmatch
from xml.etree.ElementTree import Element, ElementTree
from typing import Any, Iterable, Optional, SupportsInt, Union, List

from pineboolib import logging
from pineboolib.core.utils.utils_base import load2xml
from pineboolib.application.utils.xpm import cacheXPM
from pineboolib.application import project


class KParserTools(object):
    """
    Common functions for different KUT parsers.
    """

    _fix_altura = None

    def __init__(self) -> None:
        """Create base class for tools."""
        self.logger = logging.getLogger("ParseTools")
        self.pagina = 0
        self._fix_ratio_h = 0.927  # Corrector de altura 0.927
        self._fix_ratio_w = 0.92

    def loadKut(self, data: str) -> ElementTree:
        """
        Parse KUT xml from text.

        @param data. Input text (kut sources)
        @return xml.
        """
        return load2xml(data)

    def ratio_correction_h(self, value: float) -> int:
        """
        Revise height to become similar to the original kut.

        @param value. Input number to revise.
        @return Revised number.
        """
        return int(value * self._fix_ratio_h)

    def ratio_correction_w(self, value: float) -> int:
        """
        Revise width to become similar to the original kut.

        @param value. Input number to revise.
        @return Revised number.
        """
        return int(value * self._fix_ratio_w)

    def convertToNode(self, data: Element) -> Element:
        """
        Convert XML line to Node XML.

        When it's a calculatedField sends data to QSA of Node type.
        @param data. xml with related line info.
        @return Node with original data contents.
        """

        # node = Node()
        from PyQt5.QtXml import QDomDocument

        doc = QDomDocument()
        ele = doc.createElement("element")
        for k in data.keys():
            attr_node = doc.createAttribute(k)
            attr_node.setValue(data.get(k) or "")
            ele.setAttributeNode(attr_node)

        return ele

    def getHeight(self, xml: Element) -> int:
        """
        Retrieve height specified in xaml.

        @param xml. Element to extract the height from.
        @return Height or zero if does not exist.
        """
        return int(xml.get("Height") or "0")

    def getSpecial(self, name: str, page_num: Optional[int] = None) -> str:
        """
        Retrieve value of special type.

        @param name. Name of special type to load.
        @param page_num. PAge number if it is "PageNo" type.
        @return Required value.
        """
        self.logger.debug("%s:getSpecial %s" % (__name__, name))
        ret = "None"
        if name[0] == "[":
            name = name[1:-1]
        if name in ("Fecha", "Date"):
            ret = str(datetime.date.__format__(datetime.date.today(), "%d.%m.%Y"))
        if name in ("NúmPágina", "PageNo", "NÃºmPÃ¡gina"):
            ret = str(page_num)

        return ret

    def calculated(self, value: Any, data_type: int, p: Union[bytes, str, SupportsInt] = None, data: Element = None) -> Any:
        """
        Get value of type "calculated".

        @param field. Field name
        @param dataType. Data type. Changes how value is returned.
        @param precision. Number of decimal places.
        @param data. XML data line related.
        @return calculated value.
        """

        p = 0 if p is None else int(p)

        from pineboolib.application.utils.date_conversion import date_amd_to_dma

        ret_ = value
        if data_type == 2:  # Double
            if value in (None, "None"):
                return
            from PyQt5 import QtCore  # type: ignore

            ret_ = QtCore.QLocale.system().toString(float(value), "f", p)
        elif data_type == 0:
            pass
        elif data_type == 3:
            if value.find("T") > -1:
                value = value[: value.find("T")]
            ret_ = date_amd_to_dma(value)

        elif data_type == 5:  # Imagen
            pass

        elif data_type == 6:  # Barcode
            pass
        elif data:
            ret_ = data.get(value)

        return ret_

    def parseKey(self, ref_key: str = None) -> Optional[str]:
        """
        Get filename of .png file cached on tempdata. If it does not exist it is created.

        @param. String of related tuple in fllarge.
        @return. Path to the file in tempdata.
        """

        ret = None
        table_name = "fllarge"
        if ref_key is not None:
            from PyQt5.QtGui import QPixmap

            value = None
            tmp_dir = project.tmpdir
            img_file = "%s/%s.png" % (tmp_dir, ref_key)

            if not os.path.exists(img_file) and ref_key[0:3] == "RK@":
                from pineboolib.application.database.pnsqlquery import PNSqlQuery

                single_query = PNSqlQuery()
                single_query.exec_("SELECT valor FROM flsettings WHERE flkey='FLLargeMode'")
                single_fllarge = True

                if single_query.next():
                    if single_query.value(0) == "True":
                        single_fllarge = False

                if not single_fllarge:  # Si no es FLLarge modo único añadimos sufijo "_nombre" a fllarge
                    table_name += "_%s" % ref_key.split("@")[1]

                q = PNSqlQuery()
                q.exec_("SELECT contenido FROM %s WHERE refkey='%s'" % (table_name, ref_key))
                if q.next():
                    value = cacheXPM(q.value(0))

                if value:
                    ret = img_file
                    pix = QPixmap(value)
                    if not pix.save(img_file):
                        self.logger.warning("%s:refkey2cache No se ha podido guardar la imagen %s" % (__name__, img_file))
                        ret = None
                    else:
                        ret = img_file
            elif ref_key.endswith(".xpm"):
                pix = QPixmap(ref_key)
                img_file = ref_key.replace(".xpm", ".png")
                if not pix.save(img_file):
                    self.logger.warning("%s:refkey2cache No se ha podido guardar la imagen %s" % (__name__, img_file))
                    ret = None
                else:
                    ret = img_file

            else:

                ret = img_file

        return ret

    def converPageSize(self, size: int, orientation: int, custom: Optional[List[int]] = None) -> List[int]:
        """
        Get page size for the page code specified on .kut file.

        @param size. Size code specified on doc (0..31).
        @param orientation. 0 portrait, 1 landscape.
        @param custom. Where size is (30 or 31), custom is returned.
        @return Array with the size values.
        """
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
        elif size in (30, 31):
            r = custom  # "CUSTOM"
        if r is None:
            self.logger.warning("porcessXML:No se encuentra pagesize para %s. Usando A4" % size)
            r = [595, 842]

        # if orientation != 0:
        #    r = [r[1], r[0]]

        return r

    def find_font(self, font_name: str, font_style: str) -> Optional[str]:
        """
        Find and retrieve path for a specified font.

        @param font_name. Font name required
        @return Path to ".ttf" or None
        """
        fonts_folders: List[str] = []
        if sys.platform.find("win") > -1:
            windir = os.environ.get("WINDIR")
            if windir is None:
                raise Exception("WINDIR environ not found!")

            folders_ = os.path.join(windir, "fonts")
            if folders_:
                fonts_folders = fonts_folders
        elif sys.platform.find("linux") > -1:
            lindirs = os.environ.get("XDG_DATA_DIRS", "")
            if not lindirs:
                lindirs = "usr/share"

            for lin_dir in lindirs.split(":"):
                fonts_folders.append(os.path.join(lin_dir, "fonts"))
        elif sys.platform.find("darwin") > -1:
            fonts_folders = ["/Library/Fonts", "/System/Library/Fonts", "~/Library/Fonts"]
        else:
            self.logger.warning("KUTPARSERTOOLS: Plataforma desconocida %s", sys.platform)
            return None

        font_name = font_name.replace(" ", "_")

        font_name = font_name
        font_name2 = font_name
        font_name3 = font_name

        if font_name.endswith("BI"):
            font_name2 = font_name.replace("BI", "_Bold_Italic")
            font_name3 = font_name.replace("BI", "bi")

        if font_name.endswith("B"):
            font_name2 = font_name.replace("B", "_Bold")
            font_name3 = font_name.replace("B", "b")

        if font_name.endswith("I"):
            font_name2 = font_name.replace("I", "_Italic")
            font_name3 = font_name.replace("I", "i")

        for folder in fonts_folders:
            for root, dirnames, filenames in os.walk(folder):

                for filename in fnmatch.filter(filenames, "%s.ttf" % font_name):
                    ret_ = os.path.join(root, filename)
                    return ret_

                for filename in fnmatch.filter(filenames, "%s%s.ttf" % (font_name[0].upper(), font_name[1:])):
                    ret_ = os.path.join(root, filename)
                    return ret_

                for filename in fnmatch.filter(filenames, "%s.ttf" % font_name2):
                    ret_ = os.path.join(root, filename)
                    return ret_

                for filename in fnmatch.filter(filenames, "%s%s.ttf" % (font_name2[0].upper(), font_name2[1:])):
                    ret_ = os.path.join(root, filename)
                    return ret_

                for filename in fnmatch.filter(filenames, "%s.ttf" % font_name3):
                    ret_ = os.path.join(root, filename)
                    return ret_

                for filename in fnmatch.filter(filenames, "%s%s.ttf" % (font_name3[0].upper(), font_name3[1:])):
                    ret_ = os.path.join(root, filename)
                    return ret_

        return None

    def calculate_sum(self, field_name: str, line: Element, xml_list: Iterable, level: int) -> str:
        """
        Calculate sum for specified element line.
        """
        val = 0.0
        for l in xml_list:
            lev_ = int(l.get("level"))
            if lev_ == 0:
                val = 0.0
            if lev_ > level:
                val += float(l.get(field_name))
            if l is line:
                break

        return str(val)

    def restore_text(self, t: str) -> str:
        """Un-replace text for special characters."""
        ret_ = t
        ret_ = ret_.replace("__RPAREN__", ")")
        ret_ = ret_.replace("__LPAREN__", "(")
        ret_ = ret_.replace("__ASTERISK__", "*")
        ret_ = ret_.replace("__PLUS__", "+")

        return ret_
