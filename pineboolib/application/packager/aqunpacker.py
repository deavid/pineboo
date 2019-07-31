# -*- coding: utf-8 -*-
"""
AQUnpacker package.

Extract the files from the .abanq and .eneboopkg packages and save them in the flfiles table
"""

from PyQt5 import QtCore  # type: ignore
from typing import Any, List

err_msgs_: List[str] = []


def AQ_STRERROR(val: str) -> None:
    """
    Store the errors that occur in the extraction and insertion process in the table.
    """

    err_msgs_.append(val)


class AQUnpacker(QtCore.QObject):
    """AQUnpacker Class."""

    def __init__(self, in_: str) -> None:
        """
        Initialize the class.

        @param in_. package file name.
        """

        self.file_ = QtCore.QFile(QtCore.QDir.cleanPath(in_))
        if not self.file_.open(QtCore.QIODevice.ReadOnly):
            raise Exception("Error opening file %r" % in_)
        self.stream_ = QtCore.QDataStream(self.file_)
        self.package_version_ = self.stream_.readBytes().decode("utf-8")

    def errorMessages(self) -> list:
        """
        Return a list of messages with errors that have occurred.

        @return error list.
        """

        return err_msgs_

    def getText(self) -> str:
        """
        Return a record.

        @return record string.
        """

        ba = QtCore.QByteArray(self.stream_.readBytes())
        uncompress_ = QtCore.qUncompress(ba)
        data_bytes = uncompress_.data()
        try:
            data_ = data_bytes.decode("utf-8")
        except UnicodeDecodeError:
            data_ = data_bytes.decode("iso-8859-15")

        return data_

    def getBinary(self) -> Any:
        """
        Return a record in byte format.

        @return record bytes.
        """

        ba = QtCore.QByteArray(self.stream_.readBytes())
        return QtCore.qUncompress(ba)

    def getVersion(self) -> str:
        """
        Return the package version.

        @return package version string.
        """

        return self.package_version_

    def jump(self) -> None:
        """
        Skip a field in the package structure.
        """
        self.stream_.readBytes()
