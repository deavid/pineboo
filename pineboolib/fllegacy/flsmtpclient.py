from PyQt5 import QtCore


class FLSmtpClient(QtCore.QObject):

    status = QtCore.pyqtSignal()

    def __init__(self, parent):
        super(FLSmtpClient, self).__init__(parent)
