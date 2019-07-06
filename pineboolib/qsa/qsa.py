# -*- coding: utf-8 -*-

import os
import re
import math
from pineboolib import logging

from PyQt5 import QtCore

# FLObjects
from pineboolib.core import decorators
from pineboolib.core.utils.utils_base import ustr, filedir

from pineboolib.application import types


# from pineboolib.pnobjectsfactory import load_model, Calculated
from pineboolib.pncontrolsfactory import FLUtil, qsa_sys, QInputDialog, QLineEdit


Boolean = types.Boolean
QString = types.QString
String = types.String
Function = types.Function
Object = types.Object
Array = types.Array
Date = types.Date

logger = logging.getLogger(__name__)

util = FLUtil()  # <- para cuando QS erróneo usa util sin definirla
sys = qsa_sys
print_ = print

undefined = None
LogText = 0
RichText = 1


def parseFloat(x):
    """
    Convierte a float un valor dado
    @param x. valor a convertir
    @return Valor tipo float, o parametro x , si no es convertible
    """
    ret = 0.00
    try:
        if isinstance(x, str) and x.find(":") > -1:
            # Convertimos a horas
            list_ = x.split(":")
            x = float(list_[0])  # Horas
            x += float(list_[1]) / 60  # Minutos a hora
            x += float(list_[2]) / 3600  # Segundos a hora

        if isinstance(x, str):
            try:
                ret = float(x)
            except Exception:
                x = x.replace(".", "")
                x = x.replace(",", ".")
        else:
            ret = 0 if x in (None, "") else float(x)

        if ret == int(ret):
            ret = int(ret)

        return ret
    except Exception:
        logger.exception("parseFloat: Error converting %s to float", x)
        return x


def parseString(obj):
    """
    Convierte a str un objeto dado
    @param obj. valor a convertir
    @return str del objeto dado
    """
    return obj.toString() if hasattr(obj, "toString") else str(obj)


def parseInt(x):
    """
    Convierte en int un valor dado
    @param x. Valor a convertir
    @return Valor convertido
    """
    return int(x) if x is not None else 0


def isNaN(x):
    """
    Comprueba si un valor dado en numerico
    @param x. Valor numérico
    @return True o False
    """

    if x is None:
        return True

    if isinstance(x, str) and x.find(":"):
        x = x.replace(":", "")
    try:
        float(x)
        return False
    except ValueError:
        return True


class Input(object):
    """
    Dialogo de entrada de datos
    """

    @classmethod
    def getText(cls, question, prevtxt="", title="Pineboo"):
        """
        Recoge texto
        @param question. Label del diálogo.
        @param prevtxt. Valor inicial a especificar en el campo
        @param title. Título del diálogo
        @return cadena de texto recogida
        """
        text, ok = QInputDialog.getText(None, title, question, QLineEdit.Normal, prevtxt)
        if not ok:
            return None
        return text

    @classmethod
    def getNumber(cls, question, value, part_decimal, title="Pineboo"):
        text, ok = QInputDialog.getText(None, title, question, QLineEdit.Normal, str(round(float(value), part_decimal)))
        if not ok:
            return None
        return float(text)

    @classmethod
    def getItem(cls, question, items_list=[], title="Pineboo", editable=True):
        """
        Recoge Item
        @param question. Label del diálogo.
        @param item_list. Lista de items.
        @param title. Título del diálogo.
        @return item, Item seleccionado.
        """

        text, ok = QInputDialog.getItem(None, title, question, items_list, 0, editable)
        if not ok:
            return None
        return text


def qsa_length(obj):
    """
    Parser para recoger el length de un campo
    @param obj, objeto a obtener longitud
    @return longitud del objeto
    """
    if hasattr(obj, "length"):
        if isinstance(obj.length, int):
            return obj.length
        else:
            return obj.length()

    else:
        if isinstance(obj, dict) and "result" in obj.keys():
            return len(obj) - 1
        else:
            return len(obj)


def qsa_text(obj):
    """
    Parser para recoger valor text de un objeto dado
    @param obj. Objeto a procesar
    @return Valor de text o text()
    """
    try:
        return obj.text()
    except Exception:
        return obj.text


def RegExp(strRE):
    """
    Regexp
    @param strRE. Cadena de texto
    @return valor procesado
    """
    is_global = False
    if strRE[-2:] == "/g":
        strRE = strRE[:-2]
        is_global = True
    elif strRE[-1:] == "/":
        strRE = strRE[:-1]

    if strRE[:1] == "/":
        strRE = strRE[1:]

    return qsaRegExp(strRE, is_global)


class qsaRegExp(object):
    logger = logging.getLogger("qsaRegExp")

    def __init__(self, strRE, is_global=False):
        self.strRE_ = strRE
        self.pattern = re.compile(self.strRE_)
        self.is_global = is_global
        self.result_ = None

    def search(self, text):
        self.result_ = self.pattern.search(text)
        return self.result_

    def replace(self, target, new_value):
        count = 1 if not self.is_global else 0
        return self.pattern.sub(new_value, target, count)

    def cap(self, i):
        if self.result_ is None:
            return None

        try:
            return self.result_.group(i)
        except Exception:
            self.logger.exception("Error calling cap(%s)" % i)
            return None

    def get_global(self):
        return self.is_global

    def set_global(self, b):
        self.is_global = b

    global_ = property(get_global, set_global)


class Math(object):
    def abs(x):
        return math.fabs(x)

    def ceil(x):
        return math.ceil(x)

    def floor(x):
        return math.floor(x)

    def pow(x, y):
        return math.pow(x, y)

    def round(x):
        return round(float(x), 2)


class Dir(object):
    """
    Gestiona un directorio
    """

    path_ = None
    Files = "*.*"

    from os.path import expanduser

    home = expanduser("~")

    def __init__(self, path=None):
        self.path_ = path

    def entryList(self, patron, type_=None):
        """
        Lista de ficheros que coinciden con un patron dado
        @param patron. Patron a usa para identificar los ficheros
        @return lista con los ficheros que coinciden con el patrón
        """
        # p = os.walk(self.path_)
        retorno = []
        try:
            import fnmatch

            if os.path.exists(self.path_):
                for file in os.listdir(self.path_):
                    if fnmatch.fnmatch(file, patron):
                        retorno.append(file)
        except Exception as e:
            print("Dir_Class.entryList:", e)

        return retorno

    def fileExists(self, file_name):
        """
        Retorna si existe el fichero dado o no
        @param file_name. Nombre del fichero
        @return Boolean. Si existe el ficehro o no.
        """
        return os.path.exists(file_name)

    def cleanDirPath(name):
        """
        Devuelve la ruta del ficehro limpia
        @param name. Rtua del ficehro a limpiar
        @return ruta limpia
        """
        return str(name)

    @decorators.Deprecated
    def convertSeparators(filename):
        """
        Retona el mismo valor
        """
        return filename

    def setCurrent(self, val=None):
        """
        Especifica la ruta como path actual
        @param val. Ruta especificada
        """
        os.chdir(val or filedir("."))

    def mkdir(self, name=None):
        """
        Crea un directorio
        @param name. Nombre de la ruta a crear
        """
        if name is None:
            name = self.path_
        try:
            os.stat(name)
        except Exception:
            os.mkdir(name)


class File(QtCore.QFile):
    """
    Para gestionar un fichero
    """

    fichero = None
    mode = None
    path = None

    from PyQt5.Qt import QIODevice

    ReadOnly = QIODevice.ReadOnly
    WriteOnly = QIODevice.WriteOnly
    ReadWrite = QIODevice.ReadWrite
    encode_ = None
    last_seek = None

    def __init__(self, rutaFichero=None, encode=None):
        self.encode_ = "iso-8859-15"
        if rutaFichero:
            if isinstance(rutaFichero, tuple):
                rutaFichero = rutaFichero[0]
            self.fichero = str(rutaFichero)
            super().__init__(rutaFichero)
            self.path = os.path.dirname(os.path.abspath(self.fichero))
        else:
            super().__init__()

        if encode is not None:
            self.encode_ = encode

    def read(self, byte=False):
        """
        Lee el fichero al completo
        @param byte. Especifica si se lee en modo texto o en bytes
        @retunr contenido del fichero
        """
        if isinstance(self, str):
            file_ = self
            encode = "iso-8859-15"
        else:
            file_ = self.fichero
            encode = self.encode_
        import codecs

        f = codecs.open(file_, "r" if not byte else "rb", encoding=encode)
        ret = ""
        for l in f:
            ret = ret + l

        f.close()
        return ret

    def write(self, data, length=-1):
        """
        Escribe datos en el fichero
        @param data. Valores a guardar en el fichero
        @param length. Tamaño de data. (No se usa)
        """
        if isinstance(self, str):
            file_ = self
            encode = "utf-8"
        else:
            file_ = self.fichero
            encode = self.encode_

        byte_ = data.encode(encode)

        with open(file_, "wb") as file:
            file.write(byte_)

        file.close()

    def writeBlock(self, byte_array):
        with open(self.fichero, "wb") as file:
            file.write(byte_array)

        file.close()

    def exists(name):
        """
        Comprueba si un fichero exite
        @param name. Nombre del fichero.
        @return boolean informando si existe o no el fichero.
        """
        return QtCore.QFile.exists(name)

    def isDir(dir_name):
        """
        Indica si la ruta data es un directorio
        @param. Nombre del directorio
        @return. boolean informando si la ruta dada es un directorio o no.
        """
        return os.path.isdir(dir_name)

    def isFile(file_name):
        """
        Indica si la ruta data es un fichero
        @param. Nombre del fichero
        @return. boolean informando si la ruta dada es un fichero o no.
        """
        return os.path.isfile(file_name)

    def getName(self):
        """
        Retorna el nombre del fichero
        @return Nombre del fichero
        """
        path_, file_name = os.path.split(self.fichero)
        return file_name

    def writeLine(self, data):
        """
        Escribe un nueva linea en un fichero
        @param data. Datos a añadir en el fichero
        """
        import codecs

        f = codecs.open(self.fichero, encoding=self.encode_, mode="a")
        f.write("%s\n" % data)
        f.close()

    def readLine(self):
        """
        Lee una linea de un fichero dado
        @return cadena de texto con los datos de la linea actual
        """
        if self.last_seek is None:
            self.last_seek = 0

        import codecs

        f = codecs.open(self.fichero, "r", encoding=self.encode_)
        ret = f.readline(self.last_seek)
        self.last_seek += 1
        f.close()
        return ret

    def readLines(self):
        """
        Lee todas las lineas de un fichero y devuelve un array
        @return array con las lineas del fichero.
        """
        ret = None
        import codecs

        f = codecs.open(self.fichero, encoding=self.encode_, mode="a")
        if self.last_seek is not None:
            f.seek(self.last_seek)
        ret = f.readlines()
        f.close()
        return ret

    def readByte(self):
        """
        Lee una linea (bytes) de un fichero dado
        @return Bytes con los datos de la linea actual
        """
        return self.read(True)

    def writeByte(self, data_b):
        """
        Escribe un nueva linea en un fichero
        @param data_b. Datos a añadir en el fichero
        """

        import codecs

        f = codecs.open(self.fichero, encoding=self.encode_, mode="wb+")
        f.write(data_b)
        f.close()

    def remove(self):
        """
        Borra el fichero dado
        @return Boolean . True si se ha borrado el fichero, si no False.
        """
        if isinstance(self, str):
            file = File(self)
            file.remove()
        else:
            return super().remove()

    name = property(getName)


QFile = File


def startTimer(time, fun):
    timer = QtCore.QTimer()
    timer.timeout.connect(fun)
    timer.start(time)
    return timer


def killTimer(t):
    t.stop()
    t = None


def debug(txt):
    """
    Mensajes debug en qsa
    @param txt. Mensaje.
    """
    from pineboolib import project

    project.message_manager().send("debug", None, [ustr(txt)])


# Usadas solo por import *
from pineboolib.fllegacy.flposprinter import FLPosPrinter  # noqa
from pineboolib.fllegacy.flsqlquery import FLSqlQuery  # noqa
from pineboolib.fllegacy.flsqlcursor import FLSqlCursor  # noqa
from pineboolib.fllegacy.flnetwork import FLNetwork  # noqa
from pineboolib.fllegacy.flreportviewer import FLReportViewer  # noqa
from pineboolib.fllegacy.flvar import FLVar  # noqa
from pineboolib.core.utils.utils_base import ustr, ustr1, filedir  # noqa
from pineboolib.pncontrolsfactory import *  # noqa
