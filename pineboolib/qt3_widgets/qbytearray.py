# -*- coding: utf-8 -*-

from PyQt5 import QtCore  # type: ignore
from typing import Any


class QByteArray(QtCore.QByteArray):
    def sha1(self) -> Any:
        hash = QtCore.QCryptographicHash(QtCore.QCryptographicHash.Sha1)
        hash.addData(self.data())
        return hash.result().toHex().data().decode("utf-8").upper()

    def setString(self, val) -> None:
        self.append(val)

    def getString(self) -> Any:
        return self.data().decode("utf-8").upper()

    string = property(getString, setString)
