# # -*- coding: utf-8 -*-
from PyQt5 import QtCore
from pineboolib.core import decorators


class FLNetwork(QtCore.QObject):

    url = None
    request = None
    manager = None

    reply = None

    finished = QtCore.pyqtSignal()
    start = QtCore.pyqtSignal()
    data = QtCore.pyqtSignal(str)
    dataTransferProgress = QtCore.pyqtSignal(int, int)

    def __init__(self, url):
        super(FLNetwork, self).__init__()
        self.url = url
        from PyQt5.QtNetwork import QNetworkRequest, QNetworkAccessManager

        self.request = QNetworkRequest()

        self.manager = QNetworkAccessManager()
        # self.manager.readyRead.connect(self._slotNetworkStart)
        self.manager.finished["QNetworkReply*"].connect(self._slotNetworkFinished)
        # self.data.connect(self._slotNetWorkData)
        # self.dataTransferProgress.connect(self._slotNetworkProgress)

    @decorators.BetaImplementation
    def get(self, location):
        self.request.setUrl(QtCore.QUrl("%s%s" % (self.url, location)))
        self.reply = self.manager.get(self.request)
        try:
            self.reply.uploadProgress.disconnect(self._slotNetworkProgress)
            self.reply.downloadProgress.disconnect(self._slotNetworkProgress)
        except Exception:
            pass

        self.reply.downloadProgress.connect(self._slotNetworkProgress)

    @decorators.BetaImplementation
    def put(self, data, location):
        self.request.setUrl(QtCore.QUrl("%s%s" % (self.url, location)))
        self.reply = self.manager.put(data, self.request)
        try:
            self.reply.uploadProgress.disconnect(self._slotNetworkProgress)
            self.reply.downloadProgress.disconnect(self._slotNetworkProgress)
        except Exception:
            pass
        self.uploadProgress.connect(self.slotNetworkProgress)

    @decorators.BetaImplementation
    def copy(self, fromLocation, toLocation):
        self.request.setUrl("%s%s" % (self.url, fromLocation))
        data = self.manager.get(self.request)
        self.put(data.readAll(), toLocation)

    @QtCore.pyqtSlot()
    def _slotNetworkStart(self):
        self.start.emit()

    @QtCore.pyqtSlot()
    def _slotNetworkFinished(self, reply=None):
        self.finished.emit()

    # @QtCore.pyqtSlot(QtCore.QByteArray)
    # def _slotNetWorkData(self, b):
    #    buffer = b
    #    self.data.emit(b)

    def _slotNetworkProgress(self, bDone, bTotal):
        self.dataTransferProgress.emit(bDone, bTotal)
        data_ = None
        reply_ = self.reply.readAll().data()
        try:
            data_ = str(reply_, encoding="iso-8859-15")
        except Exception:
            data_ = str(reply_, encoding="utf-8")

        self.data.emit(data_)
