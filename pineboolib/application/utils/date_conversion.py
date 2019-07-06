from typing import List
from PyQt5.QtCore import QDate
from PyQt5 import QtCore


def date_dma_to_amd(f):
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


def date_amd_to_dma(f):
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


def convert_to_qdate(date: str) -> QDate:
    """Convierte diferentes formatos de fecha a QDate
    @param date: Fecha a convertir
    @return QDate con el valor de la fecha dada
    """
    from pineboolib.application.types import Date
    import datetime

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
