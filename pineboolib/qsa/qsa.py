# -*- coding: utf-8 -*-
import traceback
import os
import re
import math
from os.path import expanduser
from pineboolib.core.utils import logging

from PyQt5 import QtCore  # type: ignore
from PyQt5.Qt import QIODevice  # type: ignore

# FLObjects
from pineboolib.core import decorators
from pineboolib.core.utils.utils_base import ustr, filedir


# from pineboolib.pnobjectsfactory import load_model, Calculated
from pineboolib.fllegacy.flutil import FLUtil
from pineboolib.pncontrolsfactory import qsa_sys
from typing import Any, Optional, Union, Match, List, Pattern, Generator


logger: logging.Logger = logging.getLogger(__name__)  # type: ignore

util = FLUtil()  # <- para cuando QS erróneo usa util sin definirla
sys = qsa_sys
print_ = print

undefined = None
LogText = 0
RichText = 1


# from: http://code.activestate.com/recipes/410692/
# This class provides the functionality we want. You only need to look at
# this if you want to know how this works. It only needs to be defined
# once, no need to muck around with its internals.
class switch(object):
    def __init__(self, value: Any):
        self.value = value
        self.fall = False

    def __iter__(self) -> Generator:
        """Return the match method once, then stop"""
        yield self.match

    def match(self, *args: List[Any]) -> bool:
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args:
            self.fall = True
            return True
        else:
            return False


def parseFloat(x: Any) -> Any:
    """
    Convierte a float un valor dado
    @param x. valor a convertir
    @return Valor tipo float, o parametro x , si no es convertible
    """
    orig_ = x
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
                try:
                    ret = float(x)
                except Exception:
                    return orig_

        else:
            ret = 0 if x in (None, "") else float(x)

        if ret == int(ret):
            ret = int(ret)

        return ret
    except Exception:
        logger.exception("parseFloat: Error converting %s to float", x)
        return x


def parseString(obj: Any) -> str:
    """
    Convierte a str un objeto dado
    @param obj. valor a convertir
    @return str del objeto dado
    """
    return obj.toString() if hasattr(obj, "toString") else str(obj)


def parseInt(x: Union[float, int, str]) -> int:
    """
    Convierte en int un valor dado
    @param x. Valor a convertir
    @return Valor convertido
    """
    ret_ = 0
    if isinstance(x, str) and x.find(",") > -1:
        x = x.replace(",", ".")

    if x is not None:
        x = float(x)
        ret_ = int(x)

    return ret_


def isNaN(x: Any) -> bool:
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


def length(obj: Any) -> int:
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


def text(obj: Any) -> str:
    """
    Parser para recoger valor text de un objeto dado
    @param obj. Objeto a procesar
    @return Valor de text o text()
    """
    try:
        return obj.text()
    except Exception:
        return obj.text


class qsaRegExp(object):
    logger = logging.getLogger("qsaRegExp")
    result_: Optional[Match[str]]

    def __init__(self, strRE: str, is_global: bool = False):
        self.strRE_ = strRE
        self.pattern = re.compile(self.strRE_)
        self.is_global = is_global
        self.result_ = None

    def search(self, text: str) -> Optional[Match[str]]:
        self.result_ = None
        if self.pattern is not None:
            self.result_ = self.pattern.search(text)
        return self.result_

    def replace(self, target: str, new_value: str) -> str:
        count = 1 if not self.is_global else 0
        return self.pattern.sub(new_value, target, count)

    def cap(self, i: int) -> Optional[str]:
        if self.result_ is None:
            return None

        try:
            return self.result_.group(i)
        except Exception:
            self.logger.exception("Error calling cap(%s)" % i)
            return None

    def get_global(self) -> bool:
        return self.is_global

    def set_global(self, b: bool) -> None:
        self.is_global = b

    global_ = property(get_global, set_global)


def RegExp(strRE: str) -> qsaRegExp:
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


class Math(object):
    @staticmethod
    def abs(x: Union[int, float]) -> Union[int, float]:
        return math.fabs(x)

    @staticmethod
    def ceil(x: float) -> int:
        return math.ceil(x)

    @staticmethod
    def floor(x: float) -> int:
        return math.floor(x)

    @staticmethod
    def pow(x: Union[int, float], y: Union[int, float]) -> Union[int, float]:
        return math.pow(x, y)

    @staticmethod
    def round(x: Union[int, float]) -> float:
        return round(float(x), 2)


class Dir(object):
    """
    Gestiona un directorio
    """

    # Filters :
    Files = QtCore.QDir.Files
    Dirs = QtCore.QDir.Dirs
    NoFilter = QtCore.QDir.NoFilter

    # Sort Flags:
    Name = QtCore.QDir.Name
    NoSort = QtCore.QDir.NoSort

    # other:
    home = expanduser("~")

    def __init__(self, path: Optional[str] = None):
        self.path_: Optional[str] = path

    def entryList(self, patron: str, type_: int = NoFilter, sort: int = NoSort) -> list:
        """
        Lista de ficheros que coinciden con un patron dado
        @param patron. Patron a usa para identificar los ficheros
        @return lista con los ficheros que coinciden con el patrón
        """
        # p = os.walk(self.path_)
        retorno: List[str] = []
        try:
            import fnmatch

            if self.path_ is None:
                raise ValueError("self.path_ is not defined!")

            if os.path.exists(self.path_):
                for file in os.listdir(self.path_):
                    if fnmatch.fnmatch(file, patron):
                        retorno.append(file)
        except Exception as e:
            print("Dir_Class.entryList:", e)

        return retorno

    def fileExists(self, file_name: str) -> bool:
        """
        Retorna si existe el fichero dado o no
        @param file_name. Nombre del fichero
        @return Boolean. Si existe el ficehro o no.
        """
        return os.path.exists(file_name)

    @staticmethod
    def cleanDirPath(name: str) -> str:
        """
        Devuelve la ruta del ficehro limpia
        @param name. Rtua del ficehro a limpiar
        @return ruta limpia
        """
        return str(name)

    @staticmethod
    @decorators.Deprecated
    def convertSeparators(filename: str) -> str:
        """
        Retona el mismo valor
        """
        return filename

    def setCurrent(self, val: Optional[str] = None) -> None:
        """
        Especifica la ruta como path actual
        @param val. Ruta especificada
        """
        os.chdir(val or filedir("."))

    def mkdir(self, name: Optional[str] = None) -> None:
        """
        Crea un directorio
        @param name. Nombre de la ruta a crear
        """
        if name is None:
            if self.path_ is None:
                raise ValueError("self.path_ is not defined!")

            name = self.path_
        try:
            os.stat(name)
        except Exception:
            os.mkdir(name)


class File(object):  # FIXME : Rehacer!!
    """
    Para gestionar un fichero
    """

    ReadOnly = QIODevice.ReadOnly
    WriteOnly = QIODevice.WriteOnly
    ReadWrite = QIODevice.ReadWrite
    Append = QIODevice.Append

    fichero: str
    mode_: QIODevice
    path = None

    encode_: str
    last_seek = None
    qfile: QtCore.QFile
    eof = False

    def __init__(self, rutaFichero: Optional[str] = None, encode: Optional[str] = None):
        self.encode_ = "iso-8859-15"
        if rutaFichero:
            # if isinstance(rutaFichero, tuple):
            #     rutaFichero = rutaFichero[0]
            self.fichero = str(rutaFichero)
            self.qfile = QtCore.QFile(rutaFichero)

            self.path = os.path.dirname(os.path.abspath(self.fichero))
        else:
            self.qfile = QtCore.QFile()

        if encode is not None:
            self.encode_ = encode

        self.mode_ = self.ReadWrite

    def open(self, m: QIODevice) -> None:
        self.mode_ = m
        self.eof = False

    def close(self) -> None:
        pass

    def read(self: Union["File", str], bytes: bool = False) -> Union[str, bytes]:
        """
        Lee el fichero al completo
        @param bytes. Especifica si se lee en modo texto o en bytess
        @retunr contenido del fichero
        """
        file_: str
        encode: str

        if isinstance(self, str):
            file_ = self
            encode = "iso-8859-15"
        else:
            if self.fichero is None:
                raise ValueError("self.fichero is not defined!")

            file_ = self.fichero
            encode = self.encode_
        import codecs

        if file_ is None:
            raise ValueError("file is empty!")

        f = codecs.open(file_, "r" if not bytes else "rb", encoding=encode)
        ret = ""
        for l in f:
            ret = ret + l

        f.close()
        if isinstance(self, File):
            self.eof = True
        return ret

    def write(self: Union["File", str], data: Union[str, bytes], length: int = -1) -> None:
        """
        Escribe datos en el fichero
        @param data. Valores a guardar en el fichero
        @param length. Tamaño de data. (No se usa)
        """
        encode: str
        file_: str

        if isinstance(self, str):
            file_ = self
            encode = "utf-8"
        else:
            if self.fichero is None:
                raise ValueError("self.fichero is empty!")
            file_ = self.fichero
            encode = self.encode_

        if encode is None:
            raise ValueError("encode is empty!")

        if isinstance(data, str):
            bytes_ = data.encode(encode)
        else:
            bytes_ = data
        mode = "wb"
        if isinstance(self, File):
            if self.mode_ == self.Append:
                mode = "ab"
        with open(file_, mode) as file:
            file.write(bytes_)

        file.close()

    def writeBlock(self, bytes_array: bytes) -> None:
        if self.fichero is None:
            raise ValueError("self.fichero is empty!")

        with open(self.fichero, "wb") as file:
            file.write(bytes_array)

        file.close()

    @staticmethod
    def exists(name: str) -> bool:
        """
        Comprueba si un fichero exite
        @param name. Nombre del fichero.
        @return boolean informando si existe o no el fichero.
        """
        return os.path.exists(name)

    @staticmethod
    def isDir(dir_name: str) -> bool:
        """
        Indica si la ruta data es un directorio
        @param. Nombre del directorio
        @return. boolean informando si la ruta dada es un directorio o no.
        """
        return os.path.isdir(dir_name)

    @staticmethod
    def isFile(file_name: str) -> bool:
        """
        Indica si la ruta data es un fichero
        @param. Nombre del fichero
        @return. boolean informando si la ruta dada es un fichero o no.
        """
        return os.path.isfile(file_name)

    def getName(self) -> str:
        """
        Retorna el nombre del fichero
        @return Nombre del fichero
        """
        if self.fichero is None:
            raise ValueError("self.fichero is empty!")

        path_, file_name = os.path.split(self.fichero)
        return file_name

    def writeLine(self, data: str) -> None:
        """
        Escribe un nueva linea en un fichero
        @param data. Datos a añadir en el fichero
        """
        import codecs

        if self.fichero is None:
            raise ValueError("self.fichero is empty!")

        f = codecs.open(self.fichero, encoding=self.encode_, mode="a")
        f.write("%s\n" % data)
        f.close()

    def readLine(self) -> str:
        """
        Lee una linea de un fichero dado
        @return cadena de texto con los datos de la linea actual
        """
        if self.last_seek is None:
            self.last_seek = 0

        import codecs

        if self.fichero is None:
            raise ValueError("self.fichero is empty!")

        f = codecs.open(self.fichero, "r", encoding=self.encode_)
        ret = f.readline(self.last_seek)
        self.last_seek += 1
        f.close()
        return ret

    def readLines(self) -> List[str]:
        """
        Lee todas las lineas de un fichero y devuelve un array
        @return array con las lineas del fichero.
        """
        ret: List[str]
        import codecs

        f = codecs.open(self.fichero, encoding=self.encode_, mode="a")
        if self.last_seek is not None:
            f.seek(self.last_seek)
        ret = f.readlines()
        f.close()
        return ret

    def readbytes(self) -> bytes:
        """
        Lee una linea (bytess) de un fichero dado
        @return bytess con los datos de la linea actual
        """
        ret_ = self.read(True)
        if isinstance(ret_, str):
            raise ValueError("expected bytes")

        return ret_

    def writebytes(self, data_b: str) -> None:
        """
        Escribe un nueva linea en un fichero
        @param data_b. Datos a añadir en el fichero
        """

        import codecs

        f = codecs.open(self.fichero, encoding=self.encode_, mode="wb+")
        f.write(data_b)
        f.close()

    def remove(self: Union["File", str]) -> bool:
        """
        Borra el fichero dado
        @return Boolean . True si se ha borrado el fichero, si no False.
        """
        if isinstance(self, str):
            file = File(self)
            return file.remove()
        else:
            return self.qfile.remove()

    name = property(getName)


QFile = File


def startTimer(time: int, fun: Any) -> "QtCore.QTimer":
    timer = QtCore.QTimer()
    timer.timeout.connect(fun)
    timer.start(time)
    return timer


def killTimer(t: Optional["QtCore.QTimer"] = None) -> None:
    if t is not None:
        t.stop()
        t = None


def debug(txt: str) -> None:
    """
    Mensajes debug en qsa
    @param txt. Mensaje.
    """
    from pineboolib.application import project

    project.message_manager().send("debug", None, [ustr(txt)])


def from_project(scriptname: str) -> Any:
    """
    Devuelve el objeto de proyecto que coincide con el nombre dado
    """
    from pineboolib import qsa as qsa_dict_modules

    # FIXME: Esto debería estar guardado en Project.
    return getattr(qsa_dict_modules, scriptname, None)


class Application:
    """El modulo "Datos" usa Application.formRecorddat_procesos para leer el módulo"""

    def __getattr__(self, name: str) -> Any:
        return from_project(name)


def format_exc(exc: Optional[int] = None) -> str:
    return traceback.format_exc(exc)


def isnan(n: Any) -> bool:
    return math.isnan(n)


def replace(source: str, search: Any, replace: str) -> Union[str, Pattern]:
    """Replace for QSA where detects if "search" is a Regexp"""
    if hasattr(search, "match"):
        return search.replace(source, replace)
    else:
        return source.replace(search, str(replace))


# Usadas solo por import *
from pineboolib.fllegacy.flposprinter import FLPosPrinter  # noqa: F401
from pineboolib.fllegacy.flsqlquery import FLSqlQuery  # noqa: F401
from pineboolib.fllegacy.flsqlcursor import FLSqlCursor  # noqa: F401
from pineboolib.fllegacy.flnetwork import FLNetwork  # noqa: F401
from pineboolib.fllegacy.flreportviewer import FLReportViewer  # noqa: F401
from pineboolib.fllegacy.flapplication import FLApplication  # noqa: F401
from pineboolib.fllegacy.flvar import FLVar  # noqa: F401

# from pineboolib.core.utils.utils_base import ustr, filedir  # noqa: F401
from pineboolib.application.types import Boolean, QString, String, Function, Object, Array, Date, AttributeDict  # noqa: F401
from .input import Input  # noqa: F401
from pineboolib.pncontrolsfactory import *  # noqa: F401
from pineboolib.fllegacy.aqsobjects.aqsobjectfactory import AQS  # noqa: F401
