"""
Module for Date type.
"""
from typing import Union, Optional, Any
from PyQt5 import QtCore
from pineboolib.application.utils.date_conversion import date_dma_to_amd


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
        self.date_ = QtCore.QDate.fromString(
            "%s-%s-%s" % (year, self.date_.toString("MM"), self.date_.toString("dd")), "yyyy-MM-dd"
        )

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

        self.date_ = QtCore.QDate.fromString(
            "%s-%s-%s" % (self.date_.toString("yyyy"), mm, self.date_.toString("dd")), "yyyy-MM-dd"
        )

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

        self.date_ = QtCore.QDate.fromString(
            "%s-%s-%s" % (self.date_.toString("yyyy"), self.date_.toString("mm"), dd), "yyyy-MM-dd"
        )

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
