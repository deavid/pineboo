from enum import Enum

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.Qt import QDomDocument as FLDomDocument

from pineboolib import decorators
from pineboolib.flcontrols import ProjectClass

from pineboolib.kugar.mreportobject import MReportObject

from pineboolib.fllegacy.FLUtil import FLUtil
from pineboolib.fllegacy.FLStylePainter import FLStylePainter


class MLabelObject(ProjectClass, MReportObject):

    class FontWeight(Enum):
        Light = 25
        Normal = 50
        DemiBold = 63
        Bold = 75
        Black = 87

    class HAlignment(Enum):
        Left = 0
        Center = 1
        Right = 2

    class VAlignment(Enum):
        Top = 0
        Middle = 1
        Bottom = 2

    @decorators.BetaImplementation
    def __init__(self, *args):
        super(MLabelObject, self).__init__()

        if isinstance(args[0], MLabelObject):
            self.copy(args[0])
        else:
            self.text_ = ""

            self.fontFamily_ = "times"
            self.fontSize_ = 10
            self.fontWeight_ = self.FontWeight.Normal
            self.fontItalic_ = False
            self.adjustFontSize_ = False

            self.hAlignment_ = self.hAlignment.Left
            self.vAlignment_ = self.vAlignment.Top
            self.wordWrap_ = False
            self.labelFunction_ = None
            self.changeHeight_ = False
            self.paintFunction_ = None

            self.pixmap_ = None
            self.domNodeData_ = None

            self.height_ = 0
            self.width_ = 0

    @decorators.BetaImplementation
    def setText(self, txt):
        if not self.labelFunction_:
            if QtWidgets.QApplication.multiLangEnabled() and txt:
                self.text_ = txt.decode("utf8")
                if self.text_ == txt:
                    self.text_ = FLUtil.translate(self, "app", txt)
            else:
                self.text_ = txt
        else:
            dni = 0
            argList = [txt]

            if self.domNodeData_ and not self.domNodeData_.isNull():
                dni = FLDomDocument(self.domNodeData_)
                argList.append(dni)

            v = self.labelFunction_(*argList)
            if v:
                txtFun = str(v)

                if QtWidgets.QApplication.multiLangEnabled() and txtFun:
                    self.text_ = txtFun.decode("utf8")
                    if self.text_ == txtFun:
                        self.text_ = FLUtil.translate(self, "app", txtFun)
                else:
                    self.text_ = txtFun

            if dni:
                del dni

    @decorators.BetaImplementation
    def getText(self):
        return self.text_

    @decorators.BetaImplementation
    def getChangeHeight(self):
        return self.changeHeight_

    @decorators.BetaImplementation
    def setAdjustFontSize(self, a):
        self.adjustFontSize_ = a

    @decorators.BetaImplementation
    def setHorizontalAlignment(self, a):
        self.hAlignment_ = a

    @decorators.BetaImplementation
    def setVerticalAlignment(self, a):
        self.vAlignment_ = a

    @decorators.BetaImplementation
    def setWordWrap(self, wr):
        self.wordWrap_ = wr

    @decorators.BetaImplementation
    def setPaintFunction(self, pf):
        self.paintFunction_ = pf

    @decorators.BetaImplementation
    def setLabelFunction(self, lf):
        self.labelFunction_ = lf

    @decorators.BetaImplementation
    def setChangeHeight(self, ch):
        self.changeHeight_ = ch

    @decorators.BetaImplementation
    def setDomNodeData(self, dnd):
        self.domNodeData_ = dnd

    @decorators.BetaImplementation
    def setPixmap(self, pix):
        if not self.paintFunction_:
            if self.pixmap_:
                self.pixmap_ = None
            if not self.pixmap_.isNull():
                self.pixmap_ = Qt.QPixmap(pix)
        else:
            if self.pixmap_:
                self.pixmap_ = None

    @decorators.BetaImplementation
    def setFont(self, family, size, weight, italic):
        self.fontFamily_ = family
        self.fontSize_ = size
        self.fontWeight_ = weight
        self.fontItalic_ = italic

    @decorators.BetaImplementation
    def draw(self, p):
        if not self.paintFunction_:
            dni = 0
            argList = [self.text_]

            if self.domNodeData_ and not self.domNodeData_.isNull():
                dni = FLDomDocument(self.domNodeData_)
                argList.append(dni)

        v = self.paintFunction_(*argList)
        tp = type(v)

        # if (tp != QSArgument::Invalid) { #FIXME
        if tp:
            pix = Qt.QPixmap()
            if tp == Qt.QSArgument.VoidPointer:
                vPix = Qt.QPixmap(v.ptr())
                if vPix:
                    pix = vPix
            else:
                pix = v.toPixmap()

            if not pix.isNull() and self.drawPixmap(p, pix):
                return self.height_ if self.changeHeight_ else 0

        if self.pixmap_ and self.pixmap_.isNull():
            self.pixmap_ = None
        elif self.pixmap_ and self.drawPixmap(p, self.pixmap_):
            return self.height_ if self.changeHeight_ else 0

        if False:
            # MAC #FIXME
            pass
        else:
            # LINUX/WIN32
            originalHeight = self.height_

            tf = 0
            if self.hAlignment_ == self.HAlignment.Left:
                tf = Qt.QPainter.AlignLeft
            elif self.hAlignment_ == self.HAlignment.Center:
                tf = Qt.QPainter.AlignHCenter
            elif self.hAlignment_ == self.HAlignment.Right:
                tf = Qt.QPainter.AlignRight

            if self.vAlignment_ == self.VAlignment.Top:
                tf = tf | Qt.QPainter.AlignTop
            elif self.vAlignment_ == self.VAlignment.Bottom:
                tf = tf | Qt.QPainter.AlignBottom
            elif self.vAlignment_ == self.VAlignment.Middle:
                tf = tf | Qt.QPainter.AlignVCenter

            if self.wordWrap_:
                tf = tf | Qt.QPainter.WordBreak

            fnt = Qt.QFont()
            fnt.setFamily(self.fontFamily_)
            fnt.setPointSizeFloat(self.fontSize_)
            fnt.setWeight(self.fontWeight_)
            fnt.setItalic(self.fontItalic_)
            p.painter().setFont(fnt)

            retVal = 0
            if self.changeHeight_:
                maxRect = p.painter().boundingRect(0, 0, self.width_, self.height_, tf, self.text_)
                if maxRect.height() > self.height_:
                    self.height_ = maxRect.height()
                    retVal = self.height_

            self.drawBase(p)

            p.painter().setPen(self.foregroundColor_)

            restoreBg = False
            oldBgMode = Qt.BGMode()
            oldBgColor = Qt.QColor()
            if not self.transparent_:
                restoreBg = True
                oldBgMode = p.painter().backgroundMode()
                oldBgColor = p.painter().backgroundColor()
                p.painter().setBackgroundColor(self.backgroundColor_)
                p.painter().setBackgroundMode(Qt.OpaqueMode)

            if not p.drawText(self.text_, tf, self):
                restore = False
                if p.errCode() == FLStylePainter.IdNotFound:
                    # p.painter().save(Qt.QObject.name())
                    p.painter().save(self.name())
                    p.applyTransforms()
                    p.painter().translate(self.xpos_, self.ypos_)
                    restore = True

                if self.adjustFontSize_ and not self.wordWrap_ and not self.changeHeight_:
                    factor = float(self.width_) / float(p.painter().fontMetrics().width(self.text_))
                    if factor < 1.0:
                        f = p.painter().font()
                        f.setPointSizeFloat(f.pointSizeFloat() * factor)
                        p.painter().setFont(f)

                if restore:
                    p.painter().restore()

            if restoreBg:
                p.painter().setBackgroundMode(oldBgMode)
                p.painter().setBackgroundColor(oldBgColor)

        self.height_ = originalHeight
        return retVal

    @decorators.BetaImplementation
    def calcHeight(self, p):
        if not self.changeHeight_:
            return 0

        if self.pixmap_ and not self.pixmap_.isNull():
            return self.height_

        fnt = Qt.QFont()
        fnt.setFamily(self.fontFamily_)
        fnt.setPointSizeFloat(self.fontSize_)
        fnt.setWeight(self.fontWeight_)
        fnt.setItalic(self.fontItalic_)
        p.painter().setFont(fnt)

        tf = 0
        if self.hAlignment_ == self.HAlignment.Left:
            tf = Qt.QPainter.AlignLeft
        elif self.hAlignment_ == self.HAlignment.Center:
            tf = Qt.QPainter.AlignHCenter
        elif self.hAlignment_ == self.HAlignment.Right:
            tf = Qt.QPainter.AlignRight

        if self.vAlignment_ == self.VAlignment.Top:
            tf = tf | Qt.QPainter.AlignTop
        elif self.vAlignment_ == self.VAlignment.Bottom:
            tf = tf | Qt.QPainter.AlignBottom
        elif self.vAlignment_ == self.VAlignment.Middle:
            tf = tf | Qt.QPainter.AlignVCenter

        if self.wordWrap_:
            tf = tf | Qt.QPainter.WordBreak

        maxRect = p.painter().boundingRect(0, 0, self.width_, self.height_, tf, self.text_)
        return maxRect.height() if maxRect.height() > self.height_ else self.height_

    @decorators.BetaImplementation
    def drawPixmap(self, p, pixmap):
        if not p.drawPixmap(pixmap, 0, 0, -1, -1, self):
            if self.width_ > 0 and self.height_ > 0:
                # p.painter().save(Qt.QObject.name())
                p.painter().save(self.name())
                p.painter().scale(float(self.width_) / float(self.pixmap_.width()), float(self.height_) / float(self.pixmap_.height()))
            else:
                Qt.qWarning("MLabelObject::drawPixmap : width and/or height are not valid")
                return False

            p.painter().drawPixmap(0, 0, pixmap)
            p.painter().restore()

        return True

    @decorators.BetaImplementation
    def copy(self, mlo):
        self.text_ = mlo.text_

        self.fontFamily_ = mlo.fontFamily_
        self.fontSize_ = mlo.fontSize_
        self.fontWeight_ = mlo.fontWeight_
        self.fontItalic_ = mlo.fontItalic_

        self.vAlignment_ = mlo.vAlignment_
        self.hAlignment_ = mlo.hAlignment_
        self.wordWrap_ = mlo.wordWrap_
        self.labelFunction_ = mlo.labelFunction_
        self.changeHeight_ = mlo.changeHeight_
        self.paintFunction_ = mlo.paintFunction_

        if mlo.pixmap_ and not mlo.pixmap_.isNull():
            if not self.pixmap_:
                self.pixmap_ = Qt.QPixmap()
            self.pixmap_ = mlo.pixmap_

        self.domNodeData_ = mlo.domNodeData_

    @decorators.BetaImplementation
    def RTTI(self):
        return MReportObject.ReportObjectType.Label
