from enum import Enum

from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import QObject
from PyQt5.QtCore import Qt

from pineboolib import decorators


class FLPicture(QObject):
    class FLPenStyle(Enum):
        NoPen = 0
        SolidLine = 1
        DashLine = 2
        DotLine = 3
        DashDotLine = 4
        DashDotDotLine = 5
        MPenStyle = 0x0F

    class FLBrushStyle(Enum):
        NoBrush = 0
        SolidPattern = 1
        Dense1Pattern = 2
        Dense2Pattern = 3
        Dense3Pattern = 4
        Dense4Pattern = 5
        Dense5Pattern = 6
        Dense6Pattern = 7
        Dense7Pattern = 8
        HorPattern = 9
        VerPattern = 10
        CrossPattern = 11
        BDiagPattern = 12
        FDiagPattern = 13
        DiagCrossPattern = 14
        CustomPattern = 24

    class FLBGMode(Enum):
        TransparentMode = 0
        OpaqueMode = 1

    class FLRasterOP(Enum):
        CopyROP = 0
        OrROP = 1
        XorROP = 2
        NotAndROP = 3
        EraseROP = NotAndROP
        NotCopyROP = 4
        NotOrROP = 5
        NotXorROP = 6
        AndROP = 7
        NotEraseROP = AndROP
        NotROP = 8
        ClearROP = 9
        SetROP = 10
        NopROP = 11
        AndNotROP = 12
        OrNotROP = 13
        NandROP = 14
        NorROP = 15
        LastROP = NorROP

    class FLCoordinateMode(Enum):
        CoordDevice = 0
        CoordPainter = 1

    class FLTextDirection(Enum):
        Auto = 0
        RTL = 1
        LTR = 2

    class FLAlignment(Enum):
        AlignAuto = 0  # FIXME
        AlignLeft = Qt.AlignLeft
        AlignRight = Qt.AlignRight
        AlignHCenter = Qt.AlignHCenter
        AlignJustify = Qt.AlignJustify
        AlignTop = Qt.AlignTop
        AlignBottom = Qt.AlignBottom
        AlignVCenter = Qt.AlignVCenter
        AlignCenter = Qt.AlignCenter
        AlignHorizontal_Mask = Qt.AlignHorizontal_Mask
        AlignVertical_Mask = Qt.AlignVertical_Mask

    class FLPicturePrivate(QtCore.QObject):
        @decorators.BetaImplementation
        def __init__(self, *args):
            super(FLPicture.FLPicturePrivate, self).__init__()

            self.pic_ = QtGui.QPicture()
            self.pte_ = QtGui.QPainter()
            self.ownerPic_ = True
            self.ownerPte_ = True
            self.endPte_ = True

        @decorators.BetaImplementation
        def begin(self):
            if not self.pte_.isActive():
                return self.pte_.begin(self.pic_)
            return False

        @decorators.BetaImplementation
        def play(self, painter):
            if self.pic_:
                return self.pic_.play(painter)
            return False

        @decorators.BetaImplementation
        def end(self):
            if self.ownerPte_ and self.pte_.isActive():
                return self.pte_.end()
            elif not self.ownerPte_ and self.pte_.isActive() and self.endPte_:
                return self.pte_.end()
            return False

        @decorators.BetaImplementation
        def setPainter(self, pt):
            if self.pic_ and pt:
                if self.pte_:
                    self.end()
                    if self.ownerPte_:
                        del self.pte_
                self.pte_ = pt
                self.ownerPte_ = False
                self.endPte_ = not self.pte_.isActive()

    @decorators.BetaImplementation
    def __init__(self, *args):
        self.d_ = 0

        if len(args) and isinstance(args[0], FLPicture):
            super(FLPicture, self).__init__()
            otherPic = args[0]
            if otherPic and otherPic != self and otherPic.d_ and otherPic.d_.pic_:
                self.d_ = self.FLPicturePrivate()
                self.d_.pic_ = otherPic.d_.pic_

        elif len(args) and isinstance(args[0], QtGui.QPicture):
            if len(args) >= 3:
                super(FLPicture, self).__init__(args[1], args[2])
            else:
                super(FLPicture, self).__init__()
            self.setPicture(args[0])

        elif len(args) > 1 and isinstance(args[1], QtGui.QPainter):
            self.d_.setPainter(args[1])
            super(FLPicture, self).__init__(args[2], args[3])

        else:
            super(FLPicture, self).__init__(args[0], args[1])

    @decorators.BetaImplementation
    def PIC_NEW_D(self):
        if not self.d_:
            self.d_ = self.FLPicturePrivate()

    @decorators.BetaImplementation
    def PIC_CHK_D(self):
        if not self.d_ or (self.d_ and not self.d_.pte_.isActive()):
            # print("FLPicture. Picture no está activado, para activarlo llama a la función begin()")
            return False
        return True

    @decorators.BetaImplementation
    def picture(self):
        if not self.d_:
            return 0
        return self.d_.pic_

    @decorators.BetaImplementation
    def setPicture(self, pic):
        if pic:
            self.cleanup()
            self.PIC_NEW_D()
            del self.d_.pic_
            self.d_.pic_ = pic
            self.d_.ownerPic_ = False

    @decorators.BetaImplementation
    def isNull(self):
        return self.d_ and self.d_.pic_.isNull()

    @decorators.BetaImplementation
    def load(self, fileName, fformat=0):
        self.PIC_NEW_D()
        self.d_.pic_.load(fileName, fformat)

    @decorators.BetaImplementation
    def save(self, fileName, fformat=0):
        if not self.d_:
            return False
        return self.d_.pic_.save(fileName, fformat)

    @decorators.BetaImplementation
    def boundingRect(self, *args):
        if not self.PIC_CHK_D():
            return QtCore.QRect()
        self.d_.pte_.boundingRect(args)

    @decorators.BetaImplementation
    def setBoundingRect(self, r):
        self.PIC_NEW_D()
        return self.d_.pic_.setBoundingRect(r)

    @decorators.BetaImplementation
    def begin(self):
        self.PIC_NEW_D()
        return self.d_.begin()

    @decorators.BetaImplementation
    def end(self):
        if not self.PIC_CHK_D():
            return False
        return self.d_.end()

    @decorators.BetaImplementation
    def cleanup(self):
        if hasattr(self, "d_") and self.d_:
            del self.d_
        self.d_ = 0

    @decorators.BetaImplementation
    def isActive(self):
        if not self.PIC_CHK_D():
            return False
        return self.d_.pte_.isActive()

    @decorators.BetaImplementation
    def play(self, painter):
        if self.d_:
            return self.d_.play(painter)
        return False

    @decorators.BetaImplementation
    def flush(self):
        if not self.PIC_CHK_D():
            return None
        return self.d_.pte_.flush()

    @decorators.BetaImplementation
    def savePainter(self):
        if not self.PIC_CHK_D():
            return None
        return self.d_.pte_.save()

    @decorators.BetaImplementation
    def restorePainter(self):
        if not self.PIC_CHK_D():
            return None
        return self.d_.pte_.restore()

    @decorators.BetaImplementation
    def font(self):
        if not self.PIC_CHK_D():
            return QtGui.QFont()
        return self.d_.pte_.font()

    @decorators.BetaImplementation
    def setFont(self, font):
        if not self.PIC_CHK_D():
            return None
        self.d_.pte_.setFont(font)

    @decorators.BetaImplementation
    def setPen(self, color, width=0, style=FLPenStyle.SolidLine):
        if not self.PIC_CHK_D():
            return None
        self.d_.pte_.setPen(QtGui.QPen(color, width, style))

    @decorators.BetaImplementation
    def setBrush(self, color, style=FLBrushStyle.SolidPattern):
        if not self.PIC_CHK_D():
            return None
        self.d_.pte_.setBrush(QtGui.QBrush(color, style))

    @decorators.BetaImplementation
    def backgroundColor(self):
        if not self.PIC_CHK_D():
            return QtGui.QColor()
        return self.d_.pte_.backgroundColor()

    @decorators.BetaImplementation
    def setBackgroundColor(self, color):
        if not self.PIC_CHK_D():
            return None
        self.d_.pte_.setBackgroundColor(color)

    @decorators.BetaImplementation
    def backgroundMode(self):
        if not self.PIC_CHK_D():
            return self.FLBGMode.OpaqueMode
        return self.d_.pte_.backgroundMode()

    @decorators.BetaImplementation
    def setBackgroundMode(self, bgm):
        if not self.PIC_CHK_D():
            return None
        self.d_.pte_.setBackgroundMode(bgm)

    @decorators.BetaImplementation
    def rasterOp(self):
        if not self.PIC_CHK_D():
            return self.FLRasterOp.NotROP
        return self.d_.pte_.rasterOp()

    @decorators.BetaImplementation
    def setRasterOp(self, rop):
        if not self.PIC_CHK_D():
            return None
        self.d_.pte_.setRasterOp(rop)

    @decorators.BetaImplementation
    def brushOrigin(self):
        if not self.PIC_CHK_D():
            return QtCore.QPoint()
        return self.d_.pte_.brushOrigin()

    @decorators.BetaImplementation
    def setBrushOrigin(self, *args):
        if not self.PIC_CHK_D():
            return None
        self.d_.pte_.setBrushOrigin(args)

    @decorators.BetaImplementation
    def window(self):
        if not self.PIC_CHK_D():
            return QtCore.QRect()
        return self.d_.pte_.window()

    @decorators.BetaImplementation
    def setWindow(self, x, y, w, h):
        if not self.PIC_CHK_D():
            return None
        self.d_.pte_.setWindow(x, y, w, h)

    @decorators.BetaImplementation
    def viewport(self):
        if not self.PIC_CHK_D():
            return QtCore.QRect()
        return self.d_.pte_.viewport()

    @decorators.BetaImplementation
    def setViewport(self, *args):
        if not self.PIC_CHK_D():
            return None
        self.d_.pte_.setViewport(args)

    @decorators.BetaImplementation
    def scale(self, sx, sy):
        if not self.PIC_CHK_D():
            return None
        self.d_.pte_.scale(sx, sy)

    @decorators.BetaImplementation
    def shear(self, sh, sv):
        if not self.PIC_CHK_D():
            return None
        self.d_.pte_.shear(sh, sv)

    @decorators.BetaImplementation
    def rotate(self, a):
        if not self.PIC_CHK_D():
            return None
        self.d_.pte_.rotate(a)

    @decorators.BetaImplementation
    def translate(self, dx, dy):
        if not self.PIC_CHK_D():
            return None
        self.d_.pte_.translate(dx, dy)

    @decorators.BetaImplementation
    def translationX(self):
        if not self.PIC_CHK_D():
            return None
        return self.d_.pte_.translationX()

    @decorators.BetaImplementation
    def translationY(self):
        if not self.PIC_CHK_D():
            return None
        return self.d_.pte_.translationY()

    @decorators.BetaImplementation
    def setClipping(self, c):
        if not self.PIC_CHK_D():
            return None
        self.d_.pte_.setClipping(c)

    @decorators.BetaImplementation
    def hasClipping(self):
        if not self.PIC_CHK_D():
            return False
        return self.d_.pte_.hasClipping()

    @decorators.BetaImplementation
    def setClipRect(self, *args):
        if not self.PIC_CHK_D():
            return None
        self.d_.pte_.setClipRect(args)

    @decorators.BetaImplementation
    def drawLine(self, *args):
        if not self.PIC_CHK_D():
            return None
        self.d_.pte_.drawLine(args)

    @decorators.BetaImplementation
    def drawPoint(self, *args):
        if not self.PIC_CHK_D():
            return None
        self.d_.pte_.drawPoint(args)

    @decorators.BetaImplementation
    def moveTo(self, *args):
        if not self.PIC_CHK_D():
            return None
        self.d_.pte_.moveTo(args)

    @decorators.BetaImplementation
    def lineTo(self, *args):
        if not self.PIC_CHK_D():
            return None
        self.d_.pte_.lineTo(args)

    @decorators.BetaImplementation
    def drawRect(self, *args):
        if not self.PIC_CHK_D():
            return None
        self.d_.pte_.drawRect(args)

    @decorators.BetaImplementation
    def drawWinFocusRect(self, *args):
        if not self.PIC_CHK_D():
            return None
        self.d_.pte_.drawWinFocusRect(args)

    @decorators.BetaImplementation
    def drawRoundRect(self, *args):
        if not self.PIC_CHK_D():
            return None
        self.d_.pte_.drawRoundRect(args)

    @decorators.BetaImplementation
    def drawEllipse(self, *args):
        if not self.PIC_CHK_D():
            return None
        self.d_.pte_.drawEllipse(args)

    @decorators.BetaImplementation
    def drawArc(self, *args):
        if not self.PIC_CHK_D():
            return None
        self.d_.pte_.drawArc(args)

    @decorators.BetaImplementation
    def drawPie(self, *args):
        if not self.PIC_CHK_D():
            return None
        self.d_.pte_.drawPie(args)

    @decorators.BetaImplementation
    def drawChord(self, *args):
        if not self.PIC_CHK_D():
            return None
        self.d_.pte_.drawChord(args)

    @decorators.BetaImplementation
    def drawPixmap(self, *args):
        if not self.PIC_CHK_D():
            return None
        self.d_.pte_.drawPixmap(args)

    @decorators.BetaImplementation
    def drawTiledPixmap(self, *args):
        if not self.PIC_CHK_D():
            return None
        self.d_.pte_.drawTiledPixmap(args)

    @decorators.BetaImplementation
    def drawPicture(self, *args):
        if not self.PIC_CHK_D():
            return None
        nArgs = []
        hasPic = False
        for a in args:
            if isinstance(a, FLPicture):
                if a and a.picture():
                    hasPic = True
                    nArgs.append(a.picture())
            else:
                nArgs.append(a)
        if hasPic:
            self.d_.pte_.drawPicture(nArgs)

    @decorators.BetaImplementation
    def fillRect(self, *args):
        if not self.PIC_CHK_D():
            return None
        self.d_.pte_.fillRect(args)

    @decorators.BetaImplementation
    def eraseRect(self, *args):
        if not self.PIC_CHK_D():
            return None
        self.d_.pte_.eraseRect(args)

    @decorators.BetaImplementation
    def drawText(self, *args):
        if not self.PIC_CHK_D():
            return None
        self.d_.pte_.drawText(args)

    @decorators.BetaImplementation
    def playOnPixmap(self, pix):
        if not self.PIC_CHK_D():
            return 0
        if not pix:
            return 0
        self.end()
        cpyPic = QtGui.QPicture()
        cpyPic.setData(self.d_.pic_.data(), self.d_.pic_.size())
        pa = QtGui.QPainter(pix)
        pa.setClipRect(0, 0, pix.width(), pix.height())
        cpyPic.play(pa)
        pa.end()
        self.begin()
        self.d_.pte_.drawPicture(0, 0, cpyPic)
        return pix

    @decorators.BetaImplementation
    def playOnPicture(self, pic):
        if not self.PIC_CHK_D():
            return 0
        if pic and pic.picture():
            self.end()
            cpyPic = QtGui.QPicture()
            cpyPic.setData(self.d_.pic_.data(), self.d_.pic_.size())
            pa = QtGui.QPainter(pic.picture())
            cpyPic.play(pa)
            pa.end()
            self.begin()
            self.d_.pte_.drawPicture(0, 0, cpyPic)
            return pic
        return 0
