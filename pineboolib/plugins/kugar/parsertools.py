# -*- coding: utf-8 -*-
from PyQt5.QtGui import QPixmap
from pineboolib.utils import filedir, cacheXPM, load2xml
from pineboolib.fllegacy.flsqlquery import FLSqlQuery
from pineboolib.fllegacy.flsettings import FLSettings
import pineboolib
import os
import sys
import logging
import datetime
import fnmatch
from xml import etree


"""
Esta clase ofrece algunas funciones comunes de los diferentes parser de kut.
"""


class parsertools(object):
    _fix_altura = None

    def __init__(self):
        self.logger = logging.getLogger("ParseTools")
        self.pagina = 0
        self._fix_altura = 0.947  # Corrector de altura 0.927

    """
    Retorna un objecto xml desde una cadena de texto.
    @param data. Cadena de texto.
    @return xml.
    """

    def loadKut(self, data):
        return load2xml(data)

    """
    Corrige la altura para ajustarse a un kut original.
    @param value. Número a corregir.
    @return Número corregido.
    """

    def heightCorrection(self, value):
        return value * self._fix_altura

    """
    Cuando es un calculatedField , se envia un dato al qsa de tipo node.
    @param data. xml con información de la linea de datos afectada.
    @return Node con la información facilitada.
    """

    def convertToNode(self, data):

        node = Node()
        for k in data.keys():
            node.setAttribute(k, data.get(k))

        return node

    """
    Coge la altura especificada en un elemento xml.
    @param xml. Elemento del que hay que extraer la altura.
    @return Valor de la altura o 0 si no existe tal dato.
    """

    def getHeight(self, xml):
        ret_ = 0
        if xml is None:
            pass
        else:
            h = int(xml.get("Height"))
            if h:
                ret_ =  h

        return ret_

    """
    Devuelve un valor de tipo especial.
    @param name. Nombre del tipo especial a cargar.
    @param page_num. Número de página por si es un tipo "NúmPágina".
    @return Valor requerido según tipo especial especificado.
    """

    def getSpecial(self, name, page_num=None):
        self.logger.debug("%s:getSpecial %s" % (__name__, name))
        ret = "None"
        if name[0] == "[":
            name = name[1: len(name) -1]
        if name in ("Fecha", "Date"):
            ret = str(datetime.date.__format__(
                datetime.date.today(), "%d.%m.%Y"))
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

    def calculated(self, value, data_type, p, data):
        from pineboolib.pncontrolsfactory import aqApp
        ret_ = value
        if data_type == 2: # Double
            ret_ = aqApp.localeSystem().toString(float(value),'f', p)
        
        elif data_type == 5:  # Imagen
            pass
        elif data_type == 0:
            pass
        
        elif data_type == 6: # Barcode
            pass
        elif data:
            ret_ = data.get(value)

        return ret_

    """
    Retorna el nombre de un fichero .png que está cacheado en tempdata. Si no existe lo crea.
    @param. Nombre de la cadena que especifica la tupla afectada en fllarge.
    @return. Ruta completa del fichero en tempdata.
    """

    def parseKey(self, ref_key=None):
        print(ref_key)
        ret = None
        table_name = "fllarge"
        if ref_key is not None:
            value = None
            from pineboolib.pncontrolsfactory import aqApp
            
            tmp_dir = FLSettings().readEntry("ebcomportamiento/kugar_temp_dir",pineboolib.project.getTempDir())
            img_file = filedir("%s/%s.png" % (tmp_dir, ref_key))
            
            if not os.path.exists(img_file):
                if not pineboolib.project.singleFLLarge():  # Si no es FLLarge modo único añadimos sufijo "_nombre" a fllarge
                    table_name += "_%s" % ref_key.split("@")[1]

                q = FLSqlQuery()
                # q.setForwardOnly(True)
                q.exec_("SELECT contenido FROM %s WHERE refkey='%s'" % (table_name, ref_key))
                if q.next():
                    value = cacheXPM(q.value(0))

                if value:
                    pix = QPixmap(value)
                    if not pix.save(img_file):
                        self.logger.warn("%s:refkey2cache No se ha podido guardar la imagen %s" % (__name__, img_file))
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
        elif size in (30, 31):
            r = Custom  # "CUSTOM"
        if r is None:
            self.logger.warn(
                "porcessXML:No se encuentra pagesize para %s. Usando A4" % size)
            r = [595, 842]

        if orientation != 0:
            r = [r[1], r[0]]

        return r

    """
    Busca y retorna el path de un tipo de letra dado
    @param font_name. Nombre del tipo de letra
    @return Path del fichero ".ttf" o None 
    """

    def find_font(self, font_name):
        fonts_folders = []
        if sys.platform.find("win") > -1:
            windir = os.environ.get("WINDIR")
            fonts_folders = [os.path.join(windir, "fonts")]
        elif sys.platform.find("linux") > -1:
            lindirs = os.environ.get("XDG_DATA_DIRS", "")
            if not lindirs:
                lindirs = "usr/share"

            for lin_dir in lindirs.split(":"):
                fonts_folders.append(os.path.join(lin_dir, "fonts"))
        elif sys.platform.find("darwin") > -1:
            fonts_folders = ["/Library/Fonts", "/System/Library/Fonts", "~/Library/Fonts"]
        else:
            self.logger.warn("KUTPARSERTOOLS: Plataforma desconocida %s", sys.platform)
            return False

        for folder in fonts_folders:
            for root, dirnames, filenames in os.walk(folder):
                for filename in fnmatch.filter(filenames, '%s.ttf' % font_name):
                    ret_ = os.path.join(root, filename)
                    return ret_
        return None
    
    def calculate_sum(self, field_name, line, xml_list, level):
        val = 0
        i = 0
        for l in xml_list:
            if int(l.get("level")) != int(level):
                continue
            i += 1
            val += float(l.get(field_name))
            if l is line:
                break
        
        return val


"""
Clase del tipo node para los calculatedField.
"""


class Node(object):
    list_ = None

    def __init__(self):
        self.list_ = {}

    def setAttribute(self, name, value):
        self.list_[name] = value

    def attributeValue(self, name):
        return self.list_[name]
