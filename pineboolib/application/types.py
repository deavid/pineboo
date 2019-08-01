"""
Data Types for QSA.
"""

import os
import os.path
import collections
from typing import Any, Optional, Dict, Union, Generator, List

from os.path import expanduser
from PyQt5 import QtCore  # type: ignore
from PyQt5.Qt import QIODevice  # type: ignore

from pineboolib.core import decorators

from pineboolib.core.utils import logging
from pineboolib.core.utils.utils_base import StructMyDict, filedir

from pineboolib.application.qsatypes.date import Date  # noqa: F401

logger = logging.getLogger(__name__)


def Boolean(x: Union[bool, str, float] = False) -> bool:
    """
    Return boolean from string.
    """
    if isinstance(x, bool):
        return x
    if isinstance(x, str):
        x = x.lower().strip()[0]
        if x in ["y", "t"]:
            return True
        if x in ["n", "f"]:
            return False
        raise ValueError("Cannot convert %r to Boolean" % x)
    if isinstance(x, int):
        return x != 0
    if isinstance(x, float):
        if abs(x) < 0.01:
            return False
        else:
            return True
    raise ValueError("Cannot convert %r to Boolean" % x)


class QString(str):
    """
    Emulate original QString as was removed from PyQt5.
    """

    def mid(self, start: int, length: Optional[int] = None) -> str:
        """
        Cut sub-string.

        @param start. Posición inicial
        @param length. Longitud de la cadena. Si no se especifica , es hasta el final
        @return sub cadena de texto.
        """
        if length is None:
            return self[start:]
        else:
            return self[start : start + length]


def Function(*args: str) -> Any:
    """
    Load QS string code and create a function from it.

    Parses it to Python and return the pointer to the function.
    """

    import importlib
    import sys as python_sys

    # Leer código QS embebido en Source
    # asumir que es una funcion anónima, tal que:
    #  -> function($args) { source }
    # compilar la funcion y devolver el puntero
    arguments = args[: len(args) - 1]
    source = args[len(args) - 1]
    qs_source = """

function anon(%s) {
    %s
} """ % (
        ", ".join(arguments),
        source,
    )

    # print("Compilando QS en línea: ", qs_source)
    from .parsers.qsaparser import flscriptparse
    from .parsers.qsaparser import postparse
    from .parsers.qsaparser.pytnyzer import write_python_file

    from . import project

    prog = flscriptparse.parse(qs_source)
    if prog is None:
        raise ValueError("Failed to convert to Python")
    tree_data = flscriptparse.calctree(prog, alias_mode=0)
    ast = postparse.post_parse(tree_data)

    dest_filename = "%s/anon.py" % project.tmpdir
    # f1 = io.StringIO()
    if os.path.exists(dest_filename):
        os.remove(dest_filename)

    f1 = open(dest_filename, "w", encoding="UTF-8")

    write_python_file(f1, ast)
    f1.close()
    mod = None
    module_path = "tempdata.anon"

    if module_path in python_sys.modules:
        mod = importlib.reload(python_sys.modules[module_path])
    else:
        mod = importlib.import_module(module_path)
    forminternalobj = getattr(mod, "FormInternalObj", None)
    os.remove(dest_filename)
    return getattr(forminternalobj(), "anon", None)


def Object(x: Optional[Dict[str, Any]] = None) -> StructMyDict:
    """
    Object type "object".
    """
    if x is None:
        x = {}

    return StructMyDict(x)


def String(value: str) -> str:
    """
    Convert something into string.

    @param value. Valor a convertir
    @return cadena de texto.
    """
    return str(value)


class Array(object):
    """
    Array type object.
    """

    # NOTE: To avoid infinite recursion on getattr/setattr, all attributes MUST be defined at class-level.
    _dict: Dict[Any, Any] = {}
    _pos_iter = 0

    def __init__(self, *args: Any) -> None:
        """Create new array."""
        self._pos_iter = 0
        self._dict = collections.OrderedDict()

        if not len(args):
            return
        elif len(args) == 1:
            if isinstance(args[0], list):
                for n, f in enumerate(args[0]):
                    self._dict[n] = f

            elif isinstance(args[0], dict):
                dict_ = args[0]
                for k, v in dict_.items():
                    self._dict[k] = v

            elif isinstance(args[0], int):
                return

        elif isinstance(args[0], str):
            for f in args:
                self.__setitem__(f, f)

    def __iter__(self) -> Generator[Any, None, None]:
        """
        Iterate through values.
        """
        for v in self._dict.values():
            yield v

    def __setitem__(self, key: Union[str, int], value: Any) -> None:
        """
        Set item.

        @param key. Nombre del registro
        @param value. Valor del registro
        """
        # field_key = key
        # while field_key in self.dict_.keys():
        #    field_key = "%s_bis" % field_key
        self._dict[key] = value

    def __getitem__(self, key: Union[str, int, slice]) -> Any:
        """
        Get item.

        @param key. Valor que idenfica el registro a recoger
        @return Valor del registro especificado
        """
        if isinstance(key, int):
            i = 0
            for k in self._dict.keys():
                if key == i:
                    return self._dict[k]
                i += 1

        elif isinstance(key, slice):
            logger.warning("FIXME: Array __getitem__%s con slice" % key)
        else:
            return self._dict[key] if key in self._dict.keys() else None

        return None

    def length(self) -> int:
        """Return array size."""
        return len(self._dict)

    def __getattr__(self, k: str) -> Any:
        """Support for attribute style access."""
        return self._dict[k]

    def __setattr__(self, k: str, val: Any) -> None:
        """Support for attribute style writes."""
        if k[0] == "_":
            return super().__setattr__(k, val)
        self._dict[k] = val

    def __eq__(self, other: Any) -> bool:
        """Support for equality comparisons."""
        if isinstance(other, Array):
            return other._dict == self._dict
        if isinstance(other, list):
            return other == list(self._dict.values())
        if isinstance(other, dict):
            return other == self._dict
        return False

    def __repr__(self) -> str:
        """Support for repr."""
        return "<%s %r>" % (self.__class__.__name__, list(self._dict.values()))

    def splice(self, *args: Any) -> None:
        """Cut or replace array."""
        if len(args) == 2:  # Delete
            pos_ini = args[0]
            length_ = args[1]
            i = 0
            x = 0
            new = {}
            for m in self._dict.keys():
                if i >= pos_ini and x <= length_:
                    new[m] = self._dict[m]
                    x += 1

                i += 1

            self._dict = new

        elif len(args) > 2 and args[1] == 0:  # Insertion
            for i in range(2, len(args)):
                self.append(args[i])
        elif len(args) > 2 and args[1] > 0:  # Replacement
            pos_ini = args[0]
            replacement_size = args[1]
            new_values = args[2:]

            i = 0
            x = 0
            new = {}
            for m in self._dict.keys():
                if i < pos_ini:
                    new[m] = self._dict[m]
                else:
                    if x < replacement_size:
                        if x == 0:
                            for n in new_values:
                                new[n] = n

                        x += 1
                    else:
                        new[m] = self._dict[m]

                i += 1

            self._dict = new

    def __len__(self) -> int:
        """Return size of array."""
        return len(self._dict)

    def __str__(self) -> str:
        """Support for str."""
        return repr(list(self._dict.values()))

    def append(self, val: Any) -> None:
        """Append new value."""
        k = len(self._dict)
        while k in self._dict:
            k += 1

        self._dict[k] = val


AttributeDict = StructMyDict


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
