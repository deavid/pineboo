from enum import Enum

from PyQt5 import QtGui

from pineboolib import decorators
from pineboolib.flcontrols import ProjectClass

from pineboolib.fllegacy.FLStylePainter import FLStylePainter


class MLineObject(ProjectClass):

    class Style(Enum):
        NoPen = 0
        SolidLine = 1
        DashLine = 2
        DotLine = 3
        DashDotLine = 4
        DashDotDotLine = 5

    @decorators.BetaImplementation
    def __init__(self, *args):
        if len(args) and isinstance(args[0], MLineObject):
            self.copy(args[0])
        else:
            super(MLineObject, self).__init__()

            self.xpos1_ = 0
            self.ypos1_ = 0
            self.xpos2_ = 0
            self.ypos2_ = 0

            self.penWidth_ = 0
            self.penColor_ = QtGui.QColor().setRgb(0, 0, 0)
            self.penStyle_ = self.Style.SolidLine

            self.objectId = 0

    @decorators.BetaImplementation
    def setLine(self, xStart, yStart, xEnd, yEnd):
        self.xpos1_ = xStart
        self.ypos1_ = yStart
        self.xpos2_ = xEnd
        self.ypos2_ = yEnd

    @decorators.BetaImplementation
    def draw(self, p):
        self.drawBase(p)

    @decorators.BetaImplementation
    def drawBase(self, p):
        if p.drawLine(self):
            return None

        restore = False
        if p.errCode() == FLStylePainter.ErrCode.IdNotFound:
            # p.painter().save(Qt.QObject.name())
            p.painter().save(self.name())
            p.applyTransforms()
            p.painter().translate(self.xpos1_, self.ypos1_)
            restore = True

        linePen = QtGui.QPen(self.penColor_, self.penWidth_, self.penStyle_)
        p.painter().setPen(linePen)
        p.painter().drawLine(
            0, 0,
            self.xpos2_ - self.xpos1_,
            self.ypos2_ - self.ypos1_
        )

        if restore:
            p.painter().restore()

    @decorators.BetaImplementation
    def copy(self, mlo):
        self.xpos1_ = mlo.xpos1_
        self.ypos1_ = mlo.ypos1_
        self.xpos2_ = mlo.xpos2_
        self.ypos2_ = mlo.ypos2_

        self.penWidth_ = mlo.penWidth_
        self.penColor_ = mlo.penColor_
        self.penStyle_ = mlo.penStyle_

    @decorators.BetaImplementation
    def getObjectId(self):
        return self.objectId_

    @decorators.BetaImplementation
    def setObjectId(self, oid):
        self.objectId_ = oid

    @decorators.BetaImplementation
    def setColor(self, r, g, b):
        self.penColor_.setRgb(r, g, b)

    @decorators.BetaImplementation
    def setStyle(self, style):
        self.penStyle_ = style

    @decorators.BetaImplementation
    def setWidth(self, width):
        self.penWidth_ = width
