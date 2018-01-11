from enum import Enum

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from pineboolib import decorators
from pineboolib.flcontrols import ProjectClass

from pineboolib.fllegacy.FLUtil import FLUtil
from pineboolib.fllegacy.FLCodBar import FLCodBar

from pineboolib.kugar.mreportobject import MReportObject
from pineboolib.kugar.mlabelobject import MLabelObject
from pineboolib.kugar.mutil import MUtil


class MFieldObject(ProjectClass, MLabelObject):

    class DataType(Enum):
        String = 0
        Integer = 1
        Float = 2
        Date = 3
        Currency = 4
        Pixmap = 5
        Codbar = 6
        Bool = 7

    @decorators.BetaImplementation
    def __init__(self, *args):
        super(MFieldObject, self).__init__()

        if isinstance(args[0], MFieldObject):
            self.copy(args[0])
        else:
            self.fieldName_ = ""
            self.dataType_ = self.DataType.String
            self.format_ = MUtil.DateFormatType.MDY_SLASH
            self.precision_ = 0
            self.currency_ = Qt.QChar(8364)
            self.negativeValueColor_ = Qt.QColor().setRgb(255, 0, 0)
            self.comma_ = 0
            self.blankZero_ = 0
            self.codbarType_ = FLCodBar.nameToType("code128")
            self.codbarRes_ = 72
            self.saveColor_ = Qt.QColor().setRgb(0, 0, 0)

    @decorators.BetaImplementation
    def setText(self, txt):
        d = Qt.QDate()
        ret = None
        month = None
        day = None
        year = None
        val = None
        regexp = Qt.QRegExp("[0-9][0-9](-|//)[0-9][0-9](-|//)[0-9][0-9][0-9][0-9]")

        if self.dataType_ == self.DataType.String:
            if QtWidgets.QApplication.multiLangEnabled() and txt:
                self.text_ = txt.decode("utf8")
                if self.text_ == txt:
                    self.text_ = FLUtil.translate(self, "app", txt)
            else:
                self.text_ = txt
        elif self.dataType_ == self.DataType.Integer:
            val = float(txt)
            if val < 0.5 and val > -0.5 and self.blankZero_:
                self.text_ = Qt.QString("")
            else:
                self.text_ = round(val, 0)
                self.formatNegValue()
                if (self.comma_):
                    self.formatCommas()
        elif self.dataType_ == self.DataType.Float:
            val = float(txt)
            if val < 0.0000001 and val > -0.0000001 and self.blankZero_:
                self.text_ = Qt.QString("")
            else:
                self.text_ = round(val, self.precision_)
                self.formatNegValue()
                if (self.comma_):
                    self.formatCommas()
        elif self.dataType_ == self.DataType.Date:
            if not txt:
                self.text_ = Qt.QString("")
            else:
                regexp.search(txt[0:])
                ret = regexp.matchedLength()

                if ret == -1:
                    year = txt[:4]
                    day = txt[-2:]
                    month = txt[5:7]

                    if int(year) != 0 and int(month) != 0 and int(day) != 0:
                        d.setYMD(int(year), int(month), int(day))
                        self.text_ = MUtil.formatDate(d, self.format_)
                    else:
                        self.text_ = Qt.QString("")
                else:
                    self.text_ = txt
        elif self.dataType_ == self.DataType.Currency:
            val = float(txt)
            if val < 0.01 and val > -0.01 and self.blankZero_:
                self.text_ = Qt.QString("")
            else:
                self.text_ = round(val, 2)
                self.formatNegValue()
                if self.comma_:
                    self.formatCommas()
                self.text_ = self.text_ + str(self.currency_)
        elif self.dataType_ == self.DataType.Pixmap:
            if txt and not self.paintFunction_:
                if not self.pixmap_:
                    self.pixmap_ = Qt.QPixmap()
                if Qt.QPixmapCache.find(txt[:100], self.pixmap_):
                    if Qt.QFile.exists(txt):
                        self.pixmap_.load(txt)
                    else:
                        self.pixmap_.loadFromData(txt)
                    if not self.pixmap_.isNull():
                        Qt.QPixmapCache.insert(txt[:100], self.pixmap_)
                if self.pixmap_.isNull():
                    self.pixmap_ = False
            else:
                if self.pixmap_:
                    self.pixmap_ = False
        elif self.dataType_ == self.DataType.Codbar:
            if txt and not self.paintFunction_:
                cb = FLCodBar(txt, self.codbarType_, 10, 1, 0, 0, True, Qt.black, Qt.white, self.codbarRes_)
                if not self.pixmap_:
                    self.pixmap_ = Qt.QPixmap()
                if not cb.pixmap().isNull():
                    self.pixmap_ = cb.pixmap()
                else:
                    self.pixmap_ = False
            else:
                if self.pixmap_:
                    self.pixmap_ = False
        elif self.dataType_ == self.DataType.Bool:
            if txt.toUpper() == "FALSE" or txt.toUpper() == "F":
                self.text_ = FLUtil.translate(self, "app", "No")
            else:
                self.text_ = FLUtil.translate(self, "app", "Sí")

    @decorators.BetaImplementation
    def setCodBarType(self, t):
        self.codbarType_ = FLCodBar.nameToType(t)

    @decorators.BetaImplementation
    def draw(self, p):
        if self.dataType_ != self.DataType.Codbar:
            return super(MFieldObject, self).draw(p)

        if self.pixmap_ and self.pixmap_.isNull():
            self.pixmap_ = False
            self.drawBase(p)
            return 0
        elif self.pixmap_:
            if self.changeHeight_:
                sy = self.pixmap_.height() - self.height_
                if sy < 0:
                    sy = 0
                if not p.drawPixmap(self.pixmap_, 0, sy, self.width_, self.height_, self):
                    p.painter().drawPixmap(0, 0, self.pixmap_, 0, sy, self.width_, self.height_)
                return 0
            else:
                originalHeight = self.height_
                pixH = self.pixmap_.height()
                self.height_ = pixH
                if not p.drawPixmap(self.pixmap_, 0, 0, self.width_, self.height_, self):
                    p.painter().drawPixmap(0, 0, self.pixmap_, 0, 0, self.width_, self.height_)
                self.height_ = originalHeight
                return pixH

    @decorators.BetaImplementation
    def formatNegValue(self):
        if float(self.text_) < 0:
            self.foregroundColor_ = self.negativeValueColor_
        else:
            self.foregroundColor_ = self.saveColor_

    @decorators.BetaImplementation
    def formatCommas(self):
        tmp = None
        offset = None

        if float(self.text_) < 0:
            offset = 1
        else:
            offset = 0

        pos = self.text_.rfind(".")
        if pos == -1:
            pos = len(self.text_)
        else:
            tmp = "," + self.text_[(pos + 1):len(self.text_)]

        i = pos - 1
        j = 0
        while i >= offset:
            tmp = self.text_[i:(i + 1)] + tmp
            j = j + 1
            if j == 3 and (i - 1) >= offset:
                tmp = "." + tmp
                j = 0
            i = i - 1

        if offset:
            tmp = "-" + tmp

        self.text_ = tmp

    @decorators.BetaImplementation
    def copy(self, mfo):
        self.fieldName_ = mfo.fieldName_
        self.dataType_ = mfo.dataType_
        self.format_ = mfo.format_
        self.precision_ = mfo.precision_
        self.currency_ = mfo.currency_
        self.negativeValueColor_ = mfo.negativeValueColor_
        self.saveColor_ = mfo.saveColor_
        self.comma_ = mfo.comma_
        self.blankZero_ = mfo.blankZero_
        self.codbarType_ = mfo.codbarType_
        self.codbarRes_ = mfo.codbarRes_

    @decorators.BetaImplementation
    def RTTI(self):
        return MReportObject.ReportObjectType.Field

    @decorators.BetaImplementation
    def getDataType(self):
        return self.dataType_

    @decorators.BetaImplementation
    def getFieldName(self):
        return self.fieldName_

    @decorators.BetaImplementation
    def getBlankZero(self):
        return self.blankZero_

    @decorators.BetaImplementation
    def setFieldName(self, f):
        self.fieldName_ = f

    @decorators.BetaImplementation
    def setDataType(self, t):
        self.dataType_ = t
        if self.dataType_ == self.DataType.Integer or self.dataType_ == self.DataType.Float or self.dataType_ == self.DataType.Currency:
            self.saveColor_ = self.foregroundColor_

    @decorators.BetaImplementation
    def setCodBarRes(self, r):
        self.codbarRes_ = r

    @decorators.BetaImplementation
    def setDateFormat(self, f):
        self.format_ = f

    @decorators.BetaImplementation
    def setPrecision(self, p):
        self.precision_ = p

    @decorators.BetaImplementation
    def setCurrency(self, c):
        if c is None or not c:
            self.currency_ = Qt.QChar(8364)
        else:
            self.currency_ = c

    @decorators.BetaImplementation
    def setNegValueColor(self, r, g, b):
        self.negativeValueColor_.setRgb(r, g, b)

    @decorators.BetaImplementation
    def setCommaSeparator(self, c):
        self.comma_ = c

    @decorators.BetaImplementation
    def setBlankZero(self, z):
        self.blankZero_ = z
