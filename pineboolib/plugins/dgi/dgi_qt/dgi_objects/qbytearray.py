# -*- coding: utf-8 -*-

from PyQt5 import QtCore


class QByteArray(QtCore.QByteArray):
    def sha1(self):
        hash = QtCore.QCryptographicHash(QtCore.QCryptographicHash.Sha1)
        hash.addData(self.data())
        return hash.result().toHex().data().decode("utf-8").upper()

    def setString(self, val):
        self.append(val)

    def getString(self):
        return self.data().decode("utf-8").upper()

    string = property(getString, setString)
