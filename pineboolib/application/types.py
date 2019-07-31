"""
Data Types for QSA.
"""

import os
import os.path
import collections
from typing import Any, Optional, Dict, Union, Generator

from PyQt5 import QtCore  # type: ignore

from pineboolib.core.utils import logging
from pineboolib.core.utils.utils_base import StructMyDict
from pineboolib.application.utils.date_conversion import date_dma_to_amd

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


class Date(object):
    """
    Case que gestiona un objeto tipo Date.
    """

    date_: QtCore.QDate
    time_: QtCore.QTime

    def __init__(self, *args: Union["Date", QtCore.QDate, str, QtCore.QTime, int]) -> None:
        """Create new Date object."""
        super(Date, self).__init__()
        if not args:
            self.date_ = QtCore.QDate.currentDate()
            self.time_ = QtCore.QTime.currentTime()
        elif len(args) <= 2:
            date_ = args[0]
            format_ = args[1] if len(args) == 2 else "yyyy-MM-dd"
            if not isinstance(format_, str):
                raise ValueError("format must be string")
            self.time_ = QtCore.QTime(0, 0)
            if isinstance(date_, str):
                if len(date_) == 10:
                    tmp = date_.split("-")
                    if len(tmp[2]) == 4:
                        date_amd = date_dma_to_amd(date_)
                        if date_amd is None:
                            raise ValueError("Date %s is invalid" % date_)
                        date_ = date_amd

                    self.date_ = QtCore.QDate.fromString(date_, format_)
                else:
                    self.date_ = QtCore.QDate.fromString(date_[0:10], format_)
                    self.time_ = QtCore.QTime.fromString(date_[11:], "hh:mm:ss")

            elif isinstance(date_, Date):
                self.date_ = date_.date_
                self.time_ = date_.time_

            elif isinstance(date_, QtCore.QDate):
                self.date_ = date_
            if not self.time_:
                self.time_ = QtCore.QTime(0, 0)
        else:
            y, m, d = args[0], args[1], args[2]
            if not isinstance(y, int) or not isinstance(m, int) or not isinstance(d, int):
                raise ValueError("Expected year, month, day as integers")
            self.date_ = QtCore.QDate(y, m, d)
            self.time_ = QtCore.QTime(0, 0)

    def toString(self, pattern: Optional[str] = None) -> str:
        """
        Return string with date & time data.

        @return cadena de texto con los datos de fecha y hora
        """
        if pattern:
            texto = self.date_.toString(pattern)
        else:
            texto = "%s-%s-%sT%s:%s:%s" % (
                self.date_.toString("yyyy"),
                self.date_.toString("MM"),
                self.date_.toString("dd"),
                self.time_.toString("hh"),
                self.time_.toString("mm"),
                self.time_.toString("ss"),
            )

        return texto

    def getTime(self) -> int:
        """Get integer representing date & time."""
        pattern = "%s%s%s%s%s%s" % (
            self.date_.toString("yyyy"),
            self.date_.toString("MM"),
            self.date_.toString("dd"),
            self.time_.toString("hh"),
            self.time_.toString("mm"),
            self.time_.toString("ss"),
        )
        return int(pattern)

    def getYear(self) -> int:
        """
        Return year from date.

        @return año
        """
        return self.date_.year()

    def setYear(self, year: Union[str, int]) -> "Date":
        """
        Set year into current date.

        @param yyyy. Año a setear
        """
        self.date_ = QtCore.QDate.fromString("%s-%s-%s" % (year, self.date_.toString("MM"), self.date_.toString("dd")), "yyyy-MM-dd")

        return self

    def getMonth(self) -> int:
        """
        Get month as a number from current date.

        @return mes
        """
        return self.date_.month()

    def setMonth(self, mm: Union[str, int]) -> "Date":
        """
        Set month into current date.

        @param mm. Mes a setear
        """
        if isinstance(mm, int):
            mm = str(mm)

        if len(mm) == 1:
            mm = "0%s" % mm

        self.date_ = QtCore.QDate.fromString("%s-%s-%s" % (self.date_.toString("yyyy"), mm, self.date_.toString("dd")), "yyyy-MM-dd")

        return self

    def getDay(self) -> int:
        """
        Get day from current date.

        @return día
        """
        return self.date_.day()

    def setDay(self, dd: Union[str, int]) -> "Date":
        """
        Set given day.

        @param dd. Dia a setear
        """
        if isinstance(dd, int):
            dd = str(dd)

        if len(str(dd)) == 1:
            dd = "0%s" % dd

        self.date_ = QtCore.QDate.fromString("%s-%s-%s" % (self.date_.toString("yyyy"), self.date_.toString("mm"), dd), "yyyy-MM-dd")

        return self

    def getHours(self) -> int:
        """
        Get Hour from Date.

        @return horas
        """
        return self.time_.hour()

    def getMinutes(self) -> int:
        """
        Get Minutes from Date.

        @return minutos
        """
        return self.time_.minute()

    def getSeconds(self) -> int:
        """
        Get Seconds from Date.

        @return segundos
        """
        return self.time_.second()

    def getMilliseconds(self) -> int:
        """
        Get Milliseconds from Date.

        @return milisegundos
        """
        return self.time_.msec()

    getDate = getDay
    # setDate = setDay

    def setDate(self, date: Any) -> "Date":
        """
        Set Date from any format.

        @param date. Fecha a setear
        """
        year_ = self.date_.toString("yyyy")
        month_ = self.date_.toString("MM")
        day_ = str(date)
        if len(day_) == 1:
            day_ = "0" + day_

        str_ = "%s-%s-%s" % (year_, month_, day_)
        self.date_ = QtCore.QDate.fromString(str_, "yyyy-MM-dd")

        return self

    def addDays(self, d: int) -> "Date":
        """
        Return result of adding a particular amount of days to current date.

        @param d. Dias a sumar (o restar) a la fecha dada
        @return nueva fecha calculada
        """
        return Date(self.date_.addDays(d).toString("yyyy-MM-dd"))

    def addMonths(self, m: int) -> "Date":
        """
        Return result of adding given number of months to this date.

        @param m. Meses a sumar (o restar) a la fecha dada
        @return nueva fecha calculada
        """
        return Date(self.date_.addMonths(m).toString("yyyy-MM-dd"))

    def addYears(self, y: int) -> "Date":
        """
        Return result of adding given number of years to this date.

        @param y. Años a sumar (o restar) a la fecha dada
        @return nueva fecha calculada
        """
        return Date(self.date_.addYears(y).toString("yyyy-MM-dd"))

    @classmethod
    def parse(cls, value: str) -> "Date":
        """Parse a ISO string into a date."""
        return Date(value, "yyyy-MM-dd")

    def __str__(self) -> str:
        """Support for str()."""
        return self.toString()

    def __lt__(self, other: Union[str, "Date"]) -> bool:
        """Support for comparisons."""
        return str(self) < str(other)

    def __le__(self, other: Union[str, "Date"]) -> bool:
        """Support for comparisons."""
        return str(self) <= str(other)

    def __ge__(self, other: Union[str, "Date"]) -> bool:
        """Support for comparisons."""
        return str(self) >= str(other)

    def __gt__(self, other: Union[str, "Date"]) -> bool:
        """Support for comparisons."""
        return str(self) > str(other)

    def __eq__(self, other: Any) -> bool:
        """Support for comparisons."""
        return str(other) == str(self)

    def __ne__(self, other: Any) -> bool:
        """Support for comparisons."""
        return not self.__eq__(other)


AttributeDict = StructMyDict
