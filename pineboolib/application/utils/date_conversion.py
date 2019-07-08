from typing import List, Union
from PyQt5.QtCore import QDate  # type: ignore
from PyQt5 import QtCore  # type: ignore
import datetime
from typing import Any, Mapping, Optional, Sized, TypeVar

_T0 = TypeVar("_T0")
_TDate = TypeVar("_TDate", bound=Date)

_T0 = TypeVar("_T0")
_TDate = TypeVar("_TDate", bound=Date)


def date_dma_to_amd(f) -> Optional[str]:
    if not f:
        return None

    f = str(f)
    if f.find("T") > -1:
        f = f[: f.find("T")]

    array_: List[str] = []
    dia_ = None
    mes_ = None
    ano_ = None

    if f.find("-") > -1:
        array_ = f.split("-")
    elif f.find("/") > -1:
        array_ = f.split("/")

    if array_:
        if len(array_) == 3:
            dia_ = array_[0]
            mes_ = array_[1]
            ano_ = array_[2]
        else:
            dia_ = f[0:2]
            mes_ = f[2:2]
            ano_ = f[4:4]

    return "%s-%s-%s" % (ano_, mes_, dia_)


def date_amd_to_dma(f) -> Optional[str]:
    if not f:
        return None

    f = str(f)
    if f.find("T") > -1:
        f = f[: f.find("T")]

    array_: List[str] = []
    dia_ = None
    mes_ = None
    ano_ = None
    if f.find("-") > -1:
        array_ = f.split("-")
    elif f.find("/") > -1:
        array_ = f.split("/")

    if array_:
        if len(array_) == 3:
            ano_ = array_[0]
            mes_ = array_[1]
            dia_ = array_[2]
        else:
            ano_ = f[0:4]
            mes_ = f[4:2]
            dia_ = f[6:2]

    return "%s-%s-%s" % (dia_, mes_, ano_)


class Date(object):
    """
    Case que gestiona un objeto tipo Date
    """

    date_ = None
    time_ = None

    def __init__(self, *args) -> None:
        super(Date, self).__init__()
        if not args:
            self.date_ = QtCore.QDate.currentDate()
            self.time_ = QtCore.QTime.currentTime()
        elif len(args) <= 2:
            date_ = args[0]
            format_ = args[1] if len(args) == 2 else "yyyy-MM-dd"
            self.time_ = None
            if isinstance(date_, str):
                if len(date_) == 10:
                    tmp = date_.split("-")
                    if len(tmp[2]) == 4:
                        date_ = date_dma_to_amd(date_)

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
            self.date_ = QtCore.QDate(args[0], args[1], args[2])
            self.time_ = QtCore.QTime(0, 0)

    def toString(self, pattern=None) -> str:
        """
        Retorna una cadena de texto con los datos de fecha y hora.
        @return cadena de texto con los datos de fecha y hora
        """
        if pattern:
            texto = self.date_.toString(pattern)

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
        pattern = "%s%s%s%s%s%s" % (
            self.date_.toString("yyyy"),
            self.date_.toString("MM"),
            self.date_.toString("dd"),
            self.time_.toString("hh"),
            self.time_.toString("mm"),
            self.time_.toString("ss"),
        )
        return int(pattern)

    def getYear(self) -> Any:
        """
        Retorna el año
        @return año
        """
        return self.date_.year()

    def setYear(self: _TDate, yyyy) -> _TDate:
        """
        Setea un año dado
        @param yyyy. Año a setear
        """
        if yyyy is not None:
            self.date_ = QtCore.QDate.fromString("%s-%s-%s" % (yyyy, self.date_.toString("MM"), self.date_.toString("dd")), "yyyy-MM-dd")

        return self

    def getMonth(self) -> Any:
        """
        Retorna el mes
        @return mes
        """
        return self.date_.month()

    def setMonth(self: _TDate, mm) -> _TDate:
        """
        Setea un mes dado
        @param mm. Mes a setear
        """

        if mm is not None:
            if len(str(mm)) == 1:
                mm = "0%s" % mm
            self.date_ = QtCore.QDate.fromString("%s-%s-%s" % (self.date_.toString("yyyy"), mm, self.date_.toString("dd")), "yyyy-MM-dd")

        return self

    def getDay(self) -> Any:
        """
        Retorna el día
        @return día
        """
        return self.date_.day()

    def setDay(self: _TDate, dd) -> _TDate:
        """
        Setea un dia dado
        @param dd. Dia a setear
        """
        if dd is not None:
            if len(str(dd)) == 1:
                dd = "0%s" % dd

            self.date_ = QtCore.QDate.fromString("%s-%s-%s" % (self.date_.toString("yyyy"), self.date_.toString("mm"), dd), "yyyy-MM-dd")

        return self

    def getHours(self) -> Any:
        """
        Retorna horas
        @return horas
        """
        return self.time_.hour()

    def getMinutes(self) -> Any:
        """
        Retorna minutos
        @return minutos
        """
        return self.time_.minute()

    def getSeconds(self) -> Any:
        """
        Retorna segundos
        @return segundos
        """
        return self.time_.second()

    def getMilliseconds(self) -> Any:
        """
        Retorna milisegundos
        @return milisegundos
        """
        return self.time_.msec()

    getDate = getDay
    # setDate = setDay

    def setDate(self: _TDate, date) -> _TDate:
        """
        Se especifica fecha
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

    def addDays(self: _TDate, d) -> _TDate:
        """
        Se añaden dias a una fecha dada
        @param d. Dias a sumar (o restar) a la fecha dada
        @return nueva fecha calculada
        """
        return Date(self.date_.addDays(d).toString("yyyy-MM-dd"))

    def addMonths(self: _TDate, m) -> _TDate:
        """
        Se añaden meses a una fecha dada
        @param m. Meses a sumar (o restar) a la fecha dada
        @return nueva fecha calculada
        """
        return Date(self.date_.addMonths(m).toString("yyyy-MM-dd"))

    def addYears(self: _TDate, y) -> _TDate:
        """
        Se añaden años a una fecha dada
        @param y. Años a sumar (o restar) a la fecha dada
        @return nueva fecha calculada
        """
        return Date(self.date_.addYears(y).toString("yyyy-MM-dd"))

    @classmethod
    def parse(cls, value: Union[Sized, Mapping[slice, Any]]) -> Date:
        return Date(value, "yyyy-MM-dd")

    def __str__(self):
        return self.toString()

    def __lt__(self, other: _T0) -> Union[bool, _T0]:
        return self.toString() < other.toString() if not isinstance(other, str) else other

    def __le__(self, other: _T0) -> Union[bool, _T0]:
        return self.toString() <= other.toString() if not isinstance(other, str) else other

    def __ge__(self, other: _T0) -> Union[bool, _T0]:
        return self.toString() >= other.toString() if not isinstance(other, str) else other

    def __gt__(self, other: _T0) -> Union[bool, _T0]:
        return self.toString() > other.toString() if not isinstance(other, str) else other

    def __eq__(self, other):
        if str(other) == self.toString():
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)


def convert_to_qdate(date: Union[Date, datetime.date, str]) -> QDate:
    """Convierte diferentes formatos de fecha a QDate
    @param date: Fecha a convertir
    @return QDate con el valor de la fecha dada
    """

    if isinstance(date, Date):
        date = date.date_  # str
    elif isinstance(date, datetime.date):
        date = str(date)

    if isinstance(date, str):
        if "T" in date:
            date = date[: date.find("T")]

        date = date_amd_to_dma(date) if len(date.split("-")[0]) == 4 else date
        date = QtCore.QDate.fromString(date, "dd-MM-yyyy")

    return date
