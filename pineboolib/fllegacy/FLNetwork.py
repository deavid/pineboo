# # -*- coding: utf-8 -*-
from PyQt5 import QtCore
from pineboolib import decorators
from PyQt5.QtCore import QByteArray, QUrl
from PyQt5.QtNetwork import QNetworkRequest, QNetworkAccessManager


class FLNetwork(object):

    url = None
    request = None
    manager = None

    reply = None

    finished = QtCore.pyqtSignal()
    start = QtCore.pyqtSignal()
    data = QtCore.pyqtSignal(str)
    dataTransferProgress = QtCore.pyqtSignal(int, int)

    def __init__(self, url):
        self.url = QUrl(url)
        self.request = QNetworkRequest()

        self.manager = QNetworkAccessManager()
        self.manager.readyRead.connect(self._slotNetworkStart)
        self.manager.finished.connect(self._slotNetworkFinished)
        # self.data.connect(self._slotNetWorkData)
        # self.dataTransferProgress.connect(self._slotNetworkProgress)

    @decorators.BetaImplementation
    def get(self, location):
        self.request.setUrl("%s%s" % (self.url, localtion))
        self.reply = self.manager.get(self.request)
        try:
            self.reply.uploadProgress.disconnect(self._slotNetworkProgress)
            self.reply.downloadProgress.disconnect(self._slotNetworkProgress)
        except:
            pass

        self.reply.downloadProgress.connect(self.slotNetworkProgress)

    @decorators.BetaImplementation
    def put(self, data, location):
        self.request.setUrl("%s%s" % (self.url, localtion))
        self.reply = self.manager.put(data, self.request)
        try:
            self.reply.uploadProgress.disconnect(self._slotNetworkProgress)
            self.reply.downloadProgress.disconnect(self._slotNetworkProgress)
        except:
            pass
        self.uploadProgress.connect(self.slotNetworkProgress)

    @decorators.BetaImplementation
    def copy(self, fromLocation, toLocation):
        self.request.setUrl("%s%s" % (self.url, fromLocaltion))
        data = self.manager.get(self.request)
        self.put(data.readAll(), toLocation)

    @QtCore.pyqtSlot()
    def _slotNetworkStart(self):
        self.start.emit()

    @QtCore.pyqtSlot()
    def _slotNetworkFinished(self):
        self.finished.emit()

    @QtCore.pyqtSlot(QByteArray)
    def _slotNetWorkData(self, b):
        buffer = b
        self.data.emit(b)

    @QtCore.pyqtSlot(int, int)
    def _slotNetworkProgress(self, bDone, bTotal):
        self.dataTransferProgress(bDone, bTotal).emit()
        self.data.emit(self.reply.read())
