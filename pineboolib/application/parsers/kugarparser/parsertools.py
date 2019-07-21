# -*- coding: utf-8 -*-
import os
import sys
from pineboolib import logging
import datetime
import fnmatch
import xml.etree.ElementTree

from pineboolib.core.utils.utils_base import load2xml
from pineboolib.application.utils.xpm import cacheXPM
from pineboolib.application import project


from typing import Any, Iterable, Optional, SupportsInt, TypeVar, Union, List, TYPE_CHECKING

_T2 = TypeVar("_T2")

if TYPE_CHECKING:
    import xml


"""
Esta clase ofrece algunas funciones comunes de los diferentes parser de kut.
"""


class KParserTools(object):
    _fix_altura = None

    def __init__(self):
        self.logger = logging.getLogger("ParseTools")
        self.pagina = 0
        self._fix_ratio_h = 0.927  # Corrector de altura 0.927
        self._fix_ratio_w = 0.92

    """
    Retorna un objecto xml desde una cadena de texto.
    @param data. Cadena de texto.
    @return xml.
    """

    def loadKut(self, data: str) -> "xml.etree.ElementTree.ElementTree":
        return load2xml(data)

    """
    Corrige la altura para ajustarse a un kut original.
    @param value. Número a corregir.
    @return Número corregido.
    """

    def ratio_correction_h(self, value) -> int:
        return value * self._fix_ratio_h

    def ratio_correction_w(self, value) -> int:
        return value * self._fix_ratio_w

    """
    Cuando es un calculatedField , se envia un dato al qsa de tipo node.
    @param data. xml con información de la linea de datos afectada.
    @return Node con la información facilitada.
    """

    def convertToNode(self, data) -> Any:

        # node = Node()
        from pineboolib import pncontrolsfactory

        doc = pncontrolsfactory.FLDomDocument()
        ele = doc.createElement("element")
        for k in data.keys():
            attr_node = doc.createAttribute(k)
            attr_node.setValue(data.get(k))
            ele.setAttributeNode(attr_node)

        return ele

    """
    Coge la altura especificada en un elemento xml.
    @param xml. Elemento del que hay que extraer la altura.
    @return Valor de la altura o 0 si no existe tal dato.
    """

    def getHeight(self, xml) -> int:
        ret_ = 0
        if xml is None:
            pass
        else:
            h = int(xml.get("Height"))
            if h:
                ret_ = h

        return ret_

    """
    Devuelve un valor de tipo especial.
    @param name. Nombre del tipo especial a cargar.
    @param page_num. Número de página por si es un tipo "NúmPágina".
    @return Valor requerido según tipo especial especificado.
    """

    def getSpecial(self, name: str, page_num=None) -> str:
        self.logger.debug("%s:getSpecial %s" % (__name__, name))
        ret = "None"
        if name[0] == "[":
            name = name[1 : len(name) - 1]
        if name in ("Fecha", "Date"):
            ret = str(datetime.date.__format__(datetime.date.today(), "%d.%m.%Y"))
        if name in ("NúmPágina", "PageNo", "NÃºmPÃ¡gina"):
            ret = str(page_num)

        return ret

    """
    Devuelve un valor de tipo de dato calculado.
    @param field. Nombre del campo.
    @param dataType. Tipo de dato. Dependiendo de este se devolvera el valor de una manera u otra.
    @param precision. Numero de decimales
    @param data. Linea del xml de datos afectada
    @return Valor calculado.
    """

    def calculated(self, value: Any, data_type, p: Union[bytes, str, SupportsInt] = None, data=None) -> Any:

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

    """
    Retorna el nombre de un fichero .png que está cacheado en tempdata. Si no existe lo crea.
    @param. Nombre de la cadena que especifica la tupla afectada en fllarge.
    @return. Ruta completa del fichero en tempdata.
    """

    def parseKey(self, ref_key: str = None) -> Any:
        ret = None
        table_name = "fllarge"
        if ref_key is not None:
            from pineboolib import pncontrolsfactory

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
                    pix = pncontrolsfactory.QPixmap(value)
                    if not pix.save(img_file):
                        self.logger.warning("%s:refkey2cache No se ha podido guardar la imagen %s" % (__name__, img_file))
                        ret = None
                    else:
                        ret = img_file
            elif ref_key.endswith(".xpm"):
                pix = pncontrolsfactory.QPixmap(ref_key)
                img_file = ref_key.replace(".xpm", ".png")
                if not pix.save(img_file):
                    self.logger.warning("%s:refkey2cache No se ha podido guardar la imagen %s" % (__name__, img_file))
                    ret = None
                else:
                    ret = img_file

            else:

                ret = img_file

        return ret

    """
    Retorna el tamaño adecuado el código de página especificado en el .kut.
    @param size. Código de tamaño del documento(0..31).
    @param orientation. 0 vertical, 1 apaisado.
    @param custom. Cuando se especifican size (30 o 31), recogemos el valor de custom.
    @return Array con los valores del tamaño de la página.
    """

    def converPageSize(self, size, orientation, Custom: Optional[List[int]] = None) -> List[int]:
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
            r = Custom  # "CUSTOM"
        if r is None:
            self.logger.warning("porcessXML:No se encuentra pagesize para %s. Usando A4" % size)
            r = [595, 842]

        # if orientation != 0:
        #    r = [r[1], r[0]]

        return r

    """
    Busca y retorna el path de un tipo de letra dado
    @param font_name. Nombre del tipo de letra
    @return Path del fichero ".ttf" o None
    """

    def find_font(self, font_name: str, font_style) -> Union[bool, str]:
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
            return False

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

        return False

    def calculate_sum(self, field_name, line, xml_list: Iterable, level: int) -> str:
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

    def restore_text(self, t: str) -> Any:
        ret_ = t
        ret_ = ret_.replace("__RPAREN__", ")")
        ret_ = ret_.replace("__LPAREN__", "(")
        ret_ = ret_.replace("__ASTERISK__", "*")
        ret_ = ret_.replace("__PLUS__", "+")

        return ret_
