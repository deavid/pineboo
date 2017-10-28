from enum import Enum

from PyQt4.QtCore import Qt

from pineboolib import decorators
from pineboolib.flcontrols import ProjectClass


class FLPicture(ProjectClass):

    class FLPenStyle(Enum):
        NoPen = 0
        SolidLine = 1
        DashLine = 2
        DotLine = 3
        DashDotLine = 4
        DashDotDotLine = 5
        MPenStyle = 0x0f

    class FLBrushStyle(Enum):
        NoBrush = Enum.auto()
        SolidPattern = Enum.auto()
        Dense1Pattern = Enum.auto()
        Dense2Pattern = Enum.auto()
        Dense3Pattern = Enum.auto()
        Dense4Pattern = Enum.auto()
        Dense5Pattern = Enum.auto()
        Dense6Pattern = Enum.auto()
        Dense7Pattern = Enum.auto()
        HorPattern = Enum.auto()
        VerPattern = Enum.auto()
        CrossPattern = Enum.auto()
        BDiagPattern = Enum.auto()
        FDiagPattern = Enum.auto()
        DiagCrossPattern = Enum.auto()
        CustomPattern = 24

    class FLBGMode(Enum):
        TransparentMode = Enum.auto()
        OpaqueMode = Enum.auto()

    class FLRasterOP(Enum):
        CopyROP = Enum.auto()
        OrROP = Enum.auto()
        XorROP = Enum.auto()
        NotAndROP = Enum.auto()
        EraseROP = NotAndROP
        NotCopyROP = Enum.auto()
        NotOrROP = Enum.auto()
        NotXorROP = Enum.auto()
        AndROP = Enum.auto()
        NotEraseROP = AndROP
        NotROP = Enum.auto()
        ClearROP = Enum.auto()
        SetROP = Enum.auto()
        NopROP = Enum.auto()
        AndNotROP = Enum.auto()
        OrNotROP = Enum.auto()
        NandROP = Enum.auto()
        NorROP = Enum.auto()
        LastROP = NorROP

    class FLCoordinateMode(Enum):
        CoordDevice = Enum.auto()
        CoordPainter = Enum.auto()

    class FLTextDirection(Enum):
        Auto = Enum.auto()
        RTL = Enum.auto()
        LTR = Enum.auto()

    class FLAlignment(Enum):
        AlignAuto = Qt.AlignAuto,
        AlignLeft = Qt.AlignLeft,
        AlignRight = Qt.AlignRight,
        AlignHCenter = Qt.AlignHCenter,
        AlignJustify = Qt.AlignJustify,
        AlignTop = Qt.AlignTop,
        AlignBottom = Qt.AlignBottom,
        AlignVCenter = Qt.AlignVCenter,
        AlignCenter = Qt.AlignCenter,
        AlignHorizontal_Mask = Qt.AlignHorizontal_Mask,
        AlignVertical_Mask = Qt.AlignVertical_Mask

    class FLPicturePrivate(ProjectClass):

        pic_ = None
        pte_ = None
        ownerPic_ = None
        ownerPte_ = None
        endPte_ = None

        @decorators.BetaImplementation
        def __init__(self, *args):
            self.pic_ = Qt.QPicture()
            self.pte_ = Qt.QPainter()
            self.ownerPic_ = True
            self.ownerPte_ = True
            self.endPte_ = True

        @decorators.BetaImplementation
        def begin(self):
            if not self.pte_.isActive():
                return self.pte_.begin(self.pic_)
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
                        self.pte_ = None
                self.pte_ = pt
                self.ownerPte_ = False
                self.endPte_ = not self.pte_.isActive()

    @decorators.BetaImplementation
    def __init__(self, *args):
        super(FLPicture, self).__init__()
        self.d = None

        if isinstance(args[0], FLPicture):
            otherPic = args[0]
            if otherPic and otherPic != self and otherPic.d and otherPic.d.pic_:
                self.d = self.FLPicturePrivate()
                self.d.pic_ = otherPic.d.pic_

        if isinstance(args[0], Qt.QPicture):
            self.setPicture(args[0])

        if isinstance(args[1], Qt.QPainter):
            self.d.setPainter(args[1])

    @decorators.BetaImplementation
    def PIC_NEW_D(self):
        if not self.d:
            self.d = self.FLPicturePrivate()

    @decorators.BetaImplementation
    def PIC_CHK_D(self):
        if not self.d or (self.d and not self.d.pte_.isActive()):
            print("FLPicture. Picture no está activado, para activarlo llama a la función begin()")
            return False
        return True

    @decorators.BetaImplementation
    def picture(self):
        if not self.d:
            return False
        return self.d.pic_

    @decorators.BetaImplementation
    def setPicture(self, pic):
        if pic:
            self.cleanup()
            self.PIC_NEW_D()
            self.d.pic_ = pic
            self.d.ownerPic_ = False

    @decorators.BetaImplementation
    def isNull(self):
        return self.d and self.d.pic_.isNull()

    @decorators.BetaImplementation
    def load(self, fileName, format):
        self.PIC_NEW_D()
        self.d.pic_.load(fileName, format)

    @decorators.BetaImplementation
    def save(self, fileName, format):
        if not self.d:
            return False
        return self.d.pic_.save(fileName, format)

    @decorators.BetaImplementation
    def boundingRect(self, *args):
        if not self.PIC_CHK_D():
            return Qt.QRect()
        self.d.pte_.boundingRect(args)

    @decorators.BetaImplementation
    def setBoundingRect(self, r):
        self.PIC_NEW_D()
        return self.d.pic_.setBoundingRect(r)

    @decorators.BetaImplementation
    def begin(self):
        self.PIC_NEW_D()
        return self.d.begin()

    @decorators.BetaImplementation
    def end(self):
        if not self.PIC_CHK_D():
            return False
        return self.d.end()

    @decorators.BetaImplementation
    def cleanup(self):
        if self.d:
            self.d = None

    @decorators.BetaImplementation
    def isActive(self):
        if not self.PIC_CHK_D():
            return False
        return self.d.pte_.isActive()

    @decorators.BetaImplementation
    def flush(self):
        if not self.PIC_CHK_D():
            return None
        return self.d.pte_.flush()

    @decorators.BetaImplementation
    def savePainter(self):
        if not self.PIC_CHK_D():
            return None
        return self.d.pte_.save()

    @decorators.BetaImplementation
    def restorePainter(self):
        if not self.PIC_CHK_D():
            return None
        return self.d.pte_.restore()

    @decorators.BetaImplementation
    def font(self):
        if not self.PIC_CHK_D():
            return Qt.QFont()
        return self.d.pte_.font()

    @decorators.BetaImplementation
    def setFont(self, font):
        if not self.PIC_CHK_D():
            return None
        self.d.pte_.setFont(font)

    @decorators.BetaImplementation
    def setPen(self, color, width, style):
        if not self.PIC_CHK_D():
            return None
        self.d.pte_.setPen(Qt.QPen(color, width, style))

    @decorators.BetaImplementation
    def setBrush(self, color, style):
        if not self.PIC_CHK_D():
            return None
        self.d.pte_.setBrush(Qt.QBrush(color, style))

    @decorators.BetaImplementation
    def backgroundColor(self):
        if not self.PIC_CHK_D():
            return Qt.QColor()
        return self.d.pte_.backgroundColor()

    @decorators.BetaImplementation
    def setBackgroundColor(self, color):
        if not self.PIC_CHK_D():
            return None
        self.d.pte_.setBackgroundColor(color)

    @decorators.BetaImplementation
    def backgroundMode(self):
        if not self.PIC_CHK_D():
            return self.FLBGMode.OpaqueMode
        return self.d.pte_.backgroundMode()

    @decorators.BetaImplementation
    def setBackgroundMode(self, bgm):
        if not self.PIC_CHK_D():
            return None
        self.d.pte_.setBackgroundMode(bgm)

    @decorators.BetaImplementation
    def rasterOp(self):
        if not self.PIC_CHK_D():
            return self.FLRasterOp.NotROP
        return self.d.pte_.rasterOp()

    @decorators.BetaImplementation
    def setRasterOp(self, rop):
        if not self.PIC_CHK_D():
            return None
        self.d.pte_.setRasterOp(rop)

    @decorators.BetaImplementation
    def brushOrigin(self):
        if not self.PIC_CHK_D():
            return Qt.QPoint()
        return self.d.pte_.brushOrigin()

    @decorators.BetaImplementation
    def setBrushOrigin(self, *args):
        if not self.PIC_CHK_D():
            return None
        self.d.pte_.setBrushOrigin(args)

    @decorators.BetaImplementation
    def window(self):
        if not self.PIC_CHK_D():
            return Qt.QRect()
        return self.d.pte_.window()

    @decorators.BetaImplementation
    def setWindow(self, x, y, w, h):
        if not self.PIC_CHK_D():
            return None
        self.d.pte_.setWindow(x, y, w, h)

    @decorators.BetaImplementation
    def viewport(self):
        if not self.PIC_CHK_D():
            return Qt.QRect()
        return self.d.pte_.viewport()

    @decorators.BetaImplementation
    def setViewport(self, *args):
        if not self.PIC_CHK_D():
            return None
        self.d.pte_.setViewport(args)

    @decorators.BetaImplementation
    def scale(self, sx, sy):
        if not self.PIC_CHK_D():
            return None
        self.d.pte_.scale(sx, sy)

    @decorators.BetaImplementation
    def shear(self, sh, sv):
        if not self.PIC_CHK_D():
            return None
        self.d.pte_.shear(sh, sv)

    @decorators.BetaImplementation
    def rotate(self, a):
        if not self.PIC_CHK_D():
            return None
        self.d.pte_.rotate(a)

    @decorators.BetaImplementation
    def translate(self, dx, dy):
        if not self.PIC_CHK_D():
            return None
        self.d.pte_.translate(dx, dy)

    @decorators.BetaImplementation
    def translationX(self):
        if not self.PIC_CHK_D():
            return False
        return self.d.pte_.translationX()

    @decorators.BetaImplementation
    def translationY(self):
        if not self.PIC_CHK_D():
            return False
        return self.d.pte_.translationY()

    @decorators.BetaImplementation
    def setClipping(self, c):
        if not self.PIC_CHK_D():
            return None
        self.d.pte_.setClipping(c)

    @decorators.BetaImplementation
    def hasClipping(self):
        if not self.PIC_CHK_D():
            return False
        return self.d.pte_.hasClipping()

    @decorators.BetaImplementation
    def setClipRect(self, *args):
        if not self.PIC_CHK_D():
            return None
        self.d.pte_.setClipRect(args)

    @decorators.BetaImplementation
    def drawLine(self, *args):
        if not self.PIC_CHK_D():
            return None
        self.d.pte_.drawLine(args)

    @decorators.BetaImplementation
    def drawPoint(self, *args):
        if not self.PIC_CHK_D():
            return None
        self.d.pte_.drawPoint(args)

    @decorators.BetaImplementation
    def moveTo(self, *args):
        if not self.PIC_CHK_D():
            return None
        self.d.pte_.moveTo(args)

    @decorators.BetaImplementation
    def lineTo(self, *args):
        if not self.PIC_CHK_D():
            return None
        self.d.pte_.lineTo(args)

    @decorators.BetaImplementation
    def drawRect(self, *args):
        if not self.PIC_CHK_D():
            return None
        self.d.pte_.drawRect(args)

    @decorators.BetaImplementation
    def drawWinFocusRect(self, *args):
        if not self.PIC_CHK_D():
            return None
        self.d.pte_.drawWinFocusRect(args)

    @decorators.BetaImplementation
    def drawRoundRect(self, *args):
        if not self.PIC_CHK_D():
            return None
        self.d.pte_.drawRoundRect(args)

    @decorators.BetaImplementation
    def drawEllipse(self, *args):
        if not self.PIC_CHK_D():
            return None
        self.d.pte_.drawEllipse(args)

    @decorators.BetaImplementation
    def drawArc(self, *args):
        if not self.PIC_CHK_D():
            return None
        self.d.pte_.drawArc(args)

    @decorators.BetaImplementation
    def drawPie(self, *args):
        if not self.PIC_CHK_D():
            return None
        self.d.pte_.drawPie(args)

    @decorators.BetaImplementation
    def drawChord(self, *args):
        if not self.PIC_CHK_D():
            return None
        self.d.pte_.drawChord(args)

    @decorators.BetaImplementation
    def drawPixmap(self, *args):
        if not self.PIC_CHK_D():
            return None
        self.d.pte_.drawPixmap(args)

    @decorators.BetaImplementation
    def drawTiledPixmap(self, *args):
        if not self.PIC_CHK_D():
            return None
        self.d.pte_.drawTiledPixmap(args)

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
            self.d.pte_.drawPicture(nArgs)

    @decorators.BetaImplementation
    def fillRect(self, *args):
        if not self.PIC_CHK_D():
            return None
        self.d.pte_.fillRect(args)

    @decorators.BetaImplementation
    def eraseRect(self, *args):
        if not self.PIC_CHK_D():
            return None
        self.d.pte_.eraseRect(args)

    @decorators.BetaImplementation
    def drawText(self, *args):
        if not self.PIC_CHK_D():
            return None
        self.d.pte_.drawText(args)

    @decorators.BetaImplementation
    def playOnPixmap(self, pix):
        if not self.PIC_CHK_D():
            return None
        if not pix:
            return False
        self.end()
        cpyPic = Qt.QPicture()
        cpyPic.setData(self.d.pic_.data(), self.d.pic_.size())
        pa = Qt.QPainter(pix)
        pa.setClipRect(0, 0, pix.width(), pix.height())
        cpyPic.play(pa)
        pa.end()
        self.begin()
        self.d.pte_.drawPicture(0, 0, cpyPic)
        return pix

    @decorators.BetaImplementation
    def playOnPicture(self, pic):
        if not self.PIC_CHK_D():
            return None
        if pic and pic.picture():
            self.end()
            cpyPic = Qt.QPicture()
            cpyPic.setData(self.d.pic_.data(), self.d.pic_.size())
            pa = Qt.QPainter(pic.picture())
            cpyPic.play(pa)
            pa.end()
            self.begin()
            self.d.pte_.drawPicture(0, 0, cpyPic)
            return pic
        return False
