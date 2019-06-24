# -*- coding: utf-8 -*-
from PyQt5 import QtCore

err_msgs_ = []


def AQ_STRERROR(val):
    err_msgs_.append(val)


class AQUnpacker(QtCore.QObject):
    file_ = None
    stream_ = None
    package_version_ = None

    def __init__(self, in_):
        self.file_ = QtCore.QFile(QtCore.QDir.cleanPath(in_))
        if self.file_.open(QtCore.QIODevice.ReadOnly):
            self.stream_ = QtCore.QDataStream(self.file_)
            self.package_version_ = self.stream_.readBytes().decode("utf-8")

        else:
            AQ_STRERROR("Error opening file %s" % input)

    def errorMessages(self):
        return err_msgs_

    def getText(self):
        from pineboolib.pncontrolsfactory import QByteArray

        ba = QByteArray(self.stream_.readBytes())
        uncompress_ = QtCore.qUncompress(ba)
        data_ = uncompress_.data()
        try:
            data_ = data_.decode("utf-8")
        except UnicodeDecodeError:
            data_ = data_.decode("iso-8859-15")

        return data_

    def getBinary(self):
        from pineboolib.pncontrolsfactory import QByteArray

        ba = QByteArray(self.stream_.readBytes())
        return QtCore.qUncompress(ba)

    def getVersion(self):
        return self.package_version_

    def jump(self):
        self.stream_.readBytes()
