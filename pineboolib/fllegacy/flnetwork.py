# # -*- coding: utf-8 -*-
from typing import Optional, cast
from PyQt5 import QtCore  # type: ignore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtNetwork import QNetworkRequest, QNetworkAccessManager, QNetworkReply  # type: ignore
from pineboolib.core import decorators


class FLNetwork(QtCore.QObject):

    url = None
    request = None
    manager = None

    reply: Optional[QNetworkReply] = None

    finished = QtCore.pyqtSignal()
    start = QtCore.pyqtSignal()
    data = QtCore.pyqtSignal(str)
    dataTransferProgress = QtCore.pyqtSignal(int, int)

    def __init__(self, url) -> None:
        super(FLNetwork, self).__init__()
        self.url = url

        self.request = QNetworkRequest()

        self.manager = QNetworkAccessManager()
        # self.manager.readyRead.connect(self._slotNetworkStart)
        finished_signal = cast(pyqtSignal, self.manager.finished)
        finished_signal.connect(self._slotNetworkFinished)
        # finished_signal["QNetworkReply*"].connect(self._slotNetworkFinished) # FIXME: What does this code?
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

    @decorators.pyqtSlot()
    def _slotNetworkStart(self):
        self.start.emit()

    @decorators.pyqtSlot()
    def _slotNetworkFinished(self, reply=None):
        self.finished.emit()

    # @decorators.pyqtSlot(QtCore.QByteArray)
    # def _slotNetWorkData(self, b):
    #    buffer = b
    #    self.data.emit(b)

    def _slotNetworkProgress(self, bDone, bTotal) -> None:
        if self.reply is None:
            raise Exception("No reply in progress")
        self.dataTransferProgress.emit(bDone, bTotal)
        data_ = None
        reply_ = self.reply.readAll().data()
        try:
            data_ = str(reply_, encoding="iso-8859-15")
        except Exception:
            data_ = str(reply_, encoding="utf-8")

        self.data.emit(data_)
