from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.Qt import QWidget

from pineboolib import decorators


class MPageDisplay(QWidget):

    buffer_ = None
    bufferCopy_ = None

    @decorators.BetaImplementation
    def __init__(self, parent=0, name=0):
        super(MPageDisplay, self).__init__(parent)

        self.buffer_ = QtGui.QPixmap(1, 1)
        self.bufferCopy_ = QtGui.QPixmap(1, 1)

    @decorators.BetaImplementation
    def setPage(self, image):
        self.buffer_.fill(Qt.white)
        p = QtGui.QPainter(self.buffer_)
        p.setClipRect(0, 0, self.buffer_.width(), self.buffer_.height())
        image.play(p)
        self.bufferCopy_ = self.buffer_

    @decorators.BetaImplementation
    def paintEvent(self, event):
        # bitBlt(this, 0, 0, buffer); #FIXME
        self.bitBlt(self, 0, 0, self.buffer_)

    @decorators.BetaImplementation
    def setPageDimensions(self, size):
        self.buffer_ = self.buffer_.scaled(size)
        self.resize(size)

    @decorators.BetaImplementation
    def sizeHint(self):
        return self.buffer_.size()

    @decorators.BetaImplementation
    def sizePolicy(self):
        return QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )

    @decorators.BetaImplementation
    def zoomUp(self):
        img = self.bufferCopy_
        width = self.buffer_.width() * 1.25
        height = self.buffer_.height() * 1.25

        if img and not img.isNull():
            self.buffer_ = self.buffer_.scaled(QtCore.QSize(width, height))
            self.resize(width, height)
            #self.buffer_ = img.smoothScale(width, height)
            self.buffer_ = img.scaled(width, height)

    @decorators.BetaImplementation
    def zoomDown(self):
        img = self.bufferCopy_
        width = self.buffer_.width() / 1.25
        height = self.buffer_.height() / 1.25

        if img and not img.isNull():
            self.buffer_ = self.buffer_.scaled(QtCore.QSize(width, height))
            self.resize(width, height)
            #self.buffer_ = img.smoothScale(width, height)
            self.buffer_ = img.scaled(width, height)
