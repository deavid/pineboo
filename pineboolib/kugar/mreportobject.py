from enum import Enum

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.Qt import QObject

from pineboolib import decorators
from pineboolib.flcontrols import ProjectClass

from pineboolib.fllegacy.FLStylePainter import FLStylePainter


class MReportObject(ProjectClass, QObject):

    class BorderStyle(Enum):
        NoPen = 0
        SolidLine = 1
        DashLine = 2
        DotLine = 3
        DashDotLine = 4
        DashDotDotLine = 5

    class ReportObjectType(Enum):
        Invalid = 0
        Label = 1
        Field = 2
        Calc = 3
        Special = 4

    @decorators.BetaImplementation
    def __init__(self, *args):
        if len(args) and isinstance(args[0], MReportObject):
            self.copy(args[0])
        else:
            super(MReportObject, self).__init__()

            self.xpos_ = 0
            self.ypos_ = 0
            self.width_ = 40
            self.height_ = 23

            self.backgroundColor_.setRgb(255, 255, 255)
            self.foregroundColor_.setRgb(0, 0, 0)
            self.borderColor_.setRgb(0, 0, 0)
            self.borderWidth_ = 1
            self.borderStyle_ = self.BorderStyle.SolidLine

            self.sectionIndex_ = -1
            self.transparent = False
            self.objectId = 0

    @decorators.NotImplementedWarn
    # def operator=(self, mro): #FIXME
    def operator(self, mro):
        return self

    @decorators.BetaImplementation
    def draw(self, p):
        self.drawBase(p)
        return 0

    @decorators.BetaImplementation
    def drawBase(self, p):
        if p.drawRect(self):
            return

        restore = False
        if p.errCode() == FLStylePainter.IdNotFound:
            p.painter().save(self.name())
            p.applyTransforms()
            p.painter().translate(self.xpos_, self.ypos_)
            restore = True

        if self.borderStyle_ != self.BorderStyle.NoPen or self.transparent_:
            if self.transparent_:
                p.painter().setBrush(Qt.NoBrush)
            else:
                p.painter().setBrush(self.backgroundColor_)

            if self.borderStyle_ != 0:
                p.painter().setPen(QtGui.QPen(self.borderColor_, self.borderWidth_, self.borderStyle_))
            else:
                p.painter().setPen(Qt.NoPen)

            p.painter().drawRect(0, 0, self.width_, self.height_)
        else:
            p.painter().fillRect(0, 0, self.width_, self.height_, self.backgroundColor_)

        if restore:
            p.painter().restore()

    @decorators.BetaImplementation
    def setGeometry(self, x, y, w, h):
        self.xpos_ = x
        self.ypos_ = y
        self.width_ = w
        self.height_ = h

    @decorators.BetaImplementation
    def move(self, x, y):
        self.xpos_ = x
        self.ypos_ = y

    @decorators.BetaImplementation
    def setBackgroundColor(self, r, g, b):
        self.backgroundColor_.setRgb(r, g, b)

    @decorators.BetaImplementation
    def setForegroundColor(self, r, g, b):
        self.foregroundColor_.setRgb(r, g, b)

    @decorators.BetaImplementation
    def setBorderColor(self, r, g, b):
        self.borderColor_.setRgb(r, g, b)

    @decorators.BetaImplementation
    def copy(self, mro):
        self.xpos_ = mro.xpos_
        self.ypos_ = mro.ypos_
        self.width_ = mro.width_
        self.height_ = mro.height_

        self.backgroundColor_ = mro.backgroundColor_
        self.foregroundColor_ = mro.foregroundColor_

        self.borderColor_ = mro.borderColor_
        self.borderWidth_ = mro.borderWidth_
        self.borderStyle_ = mro.borderStyle_

        self.sectionIndex_ = mro.sectionIndex_
        self.transparent_ = mro.transparent_
        self.objectId_ = mro.objectId_

    @decorators.BetaImplementation
    def RTTI(self):
        return self.ReportObjectType.Invalid

    @decorators.BetaImplementation
    def getX(self):
        return self.xpos_

    @decorators.BetaImplementation
    def getY(self):
        return self.ypos_

    @decorators.BetaImplementation
    def getHeight(self):
        return self.height_

    @decorators.BetaImplementation
    def getWidth(self):
        return self.width_

    @decorators.BetaImplementation
    def getDrawAtBottom(self):
        return self.drawAtBottom_

    @decorators.BetaImplementation
    def getSectionIndex(self):
        return self.sectionIndex_

    @decorators.BetaImplementation
    def getObjectId(self):
        return self.objectId_

    @decorators.BetaImplementation
    def setBorderWidth(self, width):
        self.borderWidth_ = width

    @decorators.BetaImplementation
    def setBorderStyle(self, style):
        self.borderStyle_ = style

    @decorators.BetaImplementation
    def setTransparent(self, t):
        self.transparent_ = t

    @decorators.BetaImplementation
    def setDrawAtBottom(self, b):
        self.drawAtBottom_ = b

    @decorators.BetaImplementation
    def setSectionIndex(self, idx):
        self.sectionIndex_ = idx

    @decorators.BetaImplementation
    def setObjectId(self, id):
        self.objectId_ = id
