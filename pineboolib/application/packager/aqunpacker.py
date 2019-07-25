# -*- coding: utf-8 -*-
from PyQt5 import QtCore  # type: ignore
from typing import Any

err_msgs_ = []


def AQ_STRERROR(val) -> None:
    err_msgs_.append(val)


class AQUnpacker(QtCore.QObject):
    def __init__(self, in_) -> None:
        self.file_ = QtCore.QFile(QtCore.QDir.cleanPath(in_))
        if not self.file_.open(QtCore.QIODevice.ReadOnly):
            raise Exception("Error opening file %r" % in_)
        self.stream_ = QtCore.QDataStream(self.file_)
        self.package_version_ = self.stream_.readBytes().decode("utf-8")

    def errorMessages(self) -> list:
        return err_msgs_

    def getText(self) -> Any:
        ba = QtCore.QByteArray(self.stream_.readBytes())
        uncompress_ = QtCore.qUncompress(ba)
        data_bytes = uncompress_.data()
        try:
            data_ = data_bytes.decode("utf-8")
        except UnicodeDecodeError:
            data_ = data_bytes.decode("iso-8859-15")

        return data_

    def getBinary(self) -> Any:
        ba = QtCore.QByteArray(self.stream_.readBytes())
        return QtCore.qUncompress(ba)

    def getVersion(self) -> Any:
        return self.package_version_

    def jump(self) -> None:
        self.stream_.readBytes()
