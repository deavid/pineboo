from PyQt5.QtCore import Qt
from PyQt5.Qt import QWidget

from pineboolib import decorators
from pineboolib.flcontrols import ProjectClass


class MPageDisplayObject(ProjectClass, QWidget):

    @decorators.BetaImplementation
    def __init__(self, *args):
        super(MPageDisplayObject, self).__init__(*args)

        self.buffer_ = Qt.QPixmap()
        self.buffer_.resize(1, 1)

        self.bufferCopy_ = Qt.QPixmap()
        self.bufferCopy_.resize(1, 1)

    @decorators.BetaImplementation
    def setPage(self, image):
        # self.buffer_.fill(Qt.white) #FIXME
        self.buffer_.fill(self.white_)
        p = Qt.QPainter(self.buffer_)
        p.setClipRect(0, 0, self.buffer_.width(), self.buffer_.height())
        image.play(p)
        self.bufferCopy_ = self.buffer_

    @decorators.BetaImplementation
    def paintEvent(self, event):
        # bitBlt(this, 0, 0, buffer); #FIXME
        self.bitBlt(self, 0, 0, self.buffer_)

    @decorators.BetaImplementation
    def setPageDimensions(self, size):
        self.buffer_.resize(size)
        self.resize(size)

    @decorators.BetaImplementation
    def sizeHint(self):
        return self.buffer_.size()

    @decorators.BetaImplementation
    def sizePolicy(self):
        return Qt.QSizePolicy(Qt.QSizePolicy.Fixed, Qt.QSizePolicy.Fixed)

    @decorators.BetaImplementation
    def zoomUp(self):
        img = self.bufferCopy_
        width = self.buffer_.width() * 1.25
        height = self.buffer_.height() * 1.25

        if img and not img.isNull():
            self.buffer_.resize(width, height)
            self.resize(width, height)
            self.buffer_ = img.smoothScale(width, height)

    @decorators.BetaImplementation
    def zoomDown(self):
        img = self.bufferCopy_
        width = self.buffer_.width() / 1.25
        height = self.buffer_.height() / 1.25

        if img and not img.isNull():
            self.buffer_.resize(width, height)
            self.resize(width, height)
            self.buffer_ = img.smoothScale(width, height)
