import math
from enum import Enum
from datetime import datetime
import sys
import math

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtPrintSupport
from PyQt5 import QtXml
from PyQt5.QtCore import Qt
from PyQt5.Qt import QObject
from PyQt5.Qt import QPaintDevice

from pineboolib import decorators
from pineboolib.flcontrols import ProjectClass

from pineboolib.kugar.mreportsection import MReportSection
from pineboolib.kugar.mpagecollection import MPageCollection
from pineboolib.kugar.mlabelobject import MLabelObject
from pineboolib.kugar.mfieldobject import MFieldObject
from pineboolib.kugar.mlineobject import MLineObject
from pineboolib.kugar.mcalcobject import MCalcObject
from pineboolib.kugar.mspecialobject import MSpecialObject

from pineboolib.fllegacy.FLUtil import FLUtil
from pineboolib.fllegacy.FLStylePainter import FLStylePainter
from pineboolib.fllegacy.FLPosPrinter import FLPosPrinter
from pineboolib.fllegacy.FLDiskCache import FLDiskCache

# from pineboolib.fllegacy.AQOdsGenerator import AQOdsGenerator
# from pineboolib.fllegacy.AQOdsSpreadSheet import AQOdsSpreadSheet
# from pineboolib.fllegacy.AQOdsSheet import AQOdsSheet
# from pineboolib.fllegacy.AQOdsRow import AQOdsRow
# from pineboolib.fllegacy.AQOdsColor import AQOdsColor
# from pineboolib.fllegacy.AQOdsStyle import AQOdsStyle
# from pineboolib.fllegacy.AQOdsImage import AQOdsImage
# from pineboolib.fllegacy.AQOdsCentimeters import AQOdsCentimeters
AQOdsGenerator = AQOdsSpreadSheet = AQOdsSheet = None  # FIXME
AQOdsRow = AQOdsColor = AQOdsStyle = None  # FIXME
AQOdsImage = AQOdsCentimeters = QPrinter = None  # FIXME


class MReportEngine(QObject):

    AQ_ODSCELL_WIDTH = 80.0
    AQ_ODSCELL_HEIGHT = 15.0
    AQ_ODS_ROWS_LIMIT = 64000

    signalRenderStatus = QtCore.pyqtSignal(int)
    preferedTemplate = QtCore.pyqtSignal()

    class PageOrientation(Enum):
        Portrait = 0
        Landscape = 1

    class PageSize(Enum):
        A4 = 0
        B5 = 1
        Letter = 2
        Legal = 3
        Executive = 4
        A0 = 5
        A1 = 6
        A2 = 7
        A3 = 8
        A5 = 9
        A6 = 10
        A7 = 11
        A8 = 12
        A9 = 13
        B0 = 14
        B1 = 15
        B10 = 16
        B2 = 17
        B3 = 18
        B4 = 19
        B6 = 20
        B7 = 21
        B8 = 22
        B9 = 23
        C5E = 24
        Comm10E = 25
        DLE = 26
        Folio = 27
        Ledger = 28
        Tabloid = 29
        Custom = 30
        NPageSize = Custom
        CustomOld = 31

    class RenderReportFlags(Enum):
        Append = 0x00000001
        Display = 0x00000002
        PageBreak = 0x00000004
        FillRecords = 0x00000008

    class AQNullPaintDevice(QPaintDevice):

        @decorators.BetaImplementation
        def __init__(self, *args):
            # AQNullPaintDevice() : QPaintDevice(QInternal::ExternalDevice) {} #FIXME
            super(MReportEngine.AQNullPaintDevice, self).__init__(
                QtCore.QInternal.PaintDevice.Flags.ExternalDevice)

        @decorators.BetaImplementation
        def cmd(self, *args):
            return True

    class AQPointKey(ProjectClass):

        @decorators.BetaImplementation
        def __init__(self, *args):
            if len(args) and isinstance(args[0], QtCore.QPoint):
                self.p_ = args[0]
            elif len(args) and isinstance(args[0], MReportEngine.AQPointKey):
                self.p_ = args[0].p_

        @decorators.NotImplementedWarn
        # def operator=(self, aqpk): #FIXME
        def operator(self, aqpk):
            return self

        @decorators.NotImplementedWarn
        # def operator<(self, aqpk): #FIXME
        def operator2(self, aqpk):
            return True

        @decorators.BetaImplementation
        def p(self):
            return self.p_

    class AQPaintItem(ProjectClass):

        @decorators.BetaImplementation
        def __init__(self, *args):
            self.r_ = QtCore.QRect()
            self.rr_ = QtCore.QRect()
            self.str_ = ""
            self.pix_ = QtGui.QPixmap()
            self.fnt_ = QtGui.QFont()
            self.pen_ = QtGui.QPen()
            self.brush_ = QtGui.QBrush()
            self.bgColor_ = QtGui.QColor()
            self.tf_ = Qt.Q_INT16

    # class AQPaintItemMap(ProjectClass, QMap):
    class AQPaintItemMap(ProjectClass):
        pass

    @decorators.BetaImplementation
    def __init__(self, *args):
        if len(args) > 1 and isinstance(args[0], MReportEngine):
            super(MReportEngine, self).__init__(args[1] or 0)

            self.copy(args[0])
        else:
            super(MReportEngine, self).__init__(args[0] or 0)

            self.pageSize_ = self.PageSize.A4
            self.pageOrientation_ = self.PageOrientation.Portrait
            self.topMargin_ = 0
            self.bottomMargin_ = 0
            self.leftMargin_ = 0
            self.rightMargin_ = 0
            self.p_ = 0
            self.printToPos_ = False
            self.currRecord_ = 0
            self.fillRecords_ = False

            self.setRelDpi(78.)

            self.cancelRender_ = False

            self.grandTotal_ = []
            # self.grandTotal_.setAutoDelete(True) #FIXME

            self.gDTFooters_ = []
            self.gDTSFooters_ = []
            for i in range(10):
                self.gDTFooters_.append([])
                # self.gDTFooters_[i].setAutoDelete(True) #FIXME
                self.gDTSFooters_.append([])

            self.dHeaders_ = []
            # self.dHeaders_.setAutoDelete(True) #FIXME

            self.details_ = []
            # self.details_.setAutoDelete(True) #FIXME

            self.dFooters_ = []
            # self.dFooters_.setAutoDelete(True) #FIXME

            self.addOnHeaders_ = []
            # self.addOnHeaders_.setAutoDelete(True) #FIXME

            self.addOnFooters_ = []
            # self.addOnFooters_.setAutoDelete(True) #FIXME

            MReportSection.resetIdSecGlob()

            self.rHeader_ = MReportSection("ReportHeader")
            self.rHeader_.setPrintFrequency(
                MReportSection.PrintFrequency.FirstPage)

            self.pHeader_ = MReportSection("PageHeader")
            self.pHeader_.setPrintFrequency(
                MReportSection.PrintFrequency.EveryPage)

            self.pFooter_ = MReportSection("PageFooter")
            self.pFooter_.setPrintFrequency(
                MReportSection.PrintFrequency.EveryPage)

            self.rFooter_ = MReportSection("ReportFooter")
            self.rFooter_.setPrintFrequency(
                MReportSection.PrintFrequency.LastPage)

            ps = QtCore.QSize(self.getPageMetrics(
                self.pageSize_, self.pageOrientation_))
            self.pageWidth_ = ps.width()
            self.pageHeight_ = ps.height()
            self.rd = QtXml.QDomDocument("KUGAR_DATA")
            self.rt = QtXml.QDomDocument("KUGAR_TEMPLATE")
            self.p_ = FLStylePainter()
            self.p_.setRelDpi(self.relCalcDpi_)

            self.records_ = QtXml.QDomNodeList()

    @decorators.NotImplementedWarn
    # def operator=(self, mre): #FIXME
    def operator(self, mre):
        return self

    @decorators.BetaImplementation
    def clear(self):
        self.clearGrantTotals()

        if self.grandTotal_:
            self.grandTotal_ = None
        for i in range(10):
            if self.gDTFooters_[i]:
                self.gDTFooters_[i] = None
            if self.gDTSFooters_[i]:
                self.gDTSFooters_[i] = None

        self.clearFormatting()

        if self.addOnHeaders_:
            self.addOnHeaders_.clear()
            self.addOnHeaders_ = None

        if self.dHeaders_:
            self.dHeaders_.clear()
            self.dHeaders_ = None

        if self.details_:
            self.details_.clear()
            self.details_ = None

        if self.dFooters_:
            self.dFooters_.clear()
            self.dFooters_ = None

        if self.addOnFooters_:
            self.addOnFooters_.clear()
            self.addOnFooters_ = None

        if self.rHeader_:
            self.rHeader_ = None

        if self.pHeader_:
            self.pHeader_ = None

        if self.pFooter_:
            self.pFooter_ = None

        if self.rFooter_:
            self.rFooter_ = None

        if self.rd:
            self.rd = None

        if self.rt:
            self.rt = None

    @decorators.BetaImplementation
    def clearGrantTotals(self):
        if self.grandTotal_:
            self.grandTotal_.clear()

        for i in range(10):
            if self.gDTFooters_[i]:
                self.gDTFooters_[i].clear()
            if self.gDTSFooters_[i]:
                self.gDTSFooters_[i].clear()

    @decorators.BetaImplementation
    def clearFormatting(self):
        self.rHeader_.clear()
        self.pHeader_.clear()

        for secIt in self.addOnHeaders_:
            secIt.clear()

        for secIt in self.dHeaders_:
            secIt.clear()

        for secIt in self.details_:
            secIt.clear()

        for secIt in self.dFooters_:
            secIt.clear()

        for secIt in self.addOnFooters_:
            secIt.clear()

        self.pFooter_.clear()
        self.rFooter_.clear()

    @decorators.BetaImplementation
    def setReportData(self, data):
        if data and isinstance(data, QtXml.QDomNode):
            self.rd = data.cloneNode(True).toDocument()
        elif not self.rd.setContent(data):
            QtCore.qWarning("Unable to parse report data")
            return False

        self.initData()
        return True

    @decorators.BetaImplementation
    def initData(self):
        n = self.rd.firstChild()
        while not n.isNull():
            if n.nodeName() == "KugarData":
                self.records_ = n.childNodes()
                attr = n.attributes()
                tempattr = attr.namedItem("Template")
                tempname = tempattr.nodeValue() or 0
                if not tempname.isNull():
                    self.preferedTemplate.emit(tempname)
                    break
            n = n.nextSibling()

    @decorators.BetaImplementation
    def setReportTemplate(self, tpl):
        self.clearFormatting()
        if tpl and isinstance(tpl, QtXml.QDomNode):
            self.rt = tpl.cloneNode(True).toDocument()
        elif not self.rt.setContent(tpl):
            QtCore.qWarning("Unable to parse report data")
            return False

        self.initTemplate()
        return True

    @decorators.BetaImplementation
    def initTemplate(self):
        MReportSection.resetIdSecGlob()

        if self.addOnHeaders_:
            self.addOnHeaders_.clear()

        if self.dHeaders_:
            self.dHeaders_.clear()

        if self.details_:
            self.details_.clear()

        if self.addOnFooters_:
            self.addOnFooters_.clear()

        if self.dFooters_:
            self.dFooters_.clear()

        report = self.rt.firstChild()
        while not report.isNull():
            if report.nodeName == "KugarTemplate":
                break
            report = report.nextSibling()

        self.setReportAttributes(report)

        children = report.childNodes()
        childCount = len(children)

        for j in range(childCount):
            child = children.item(j)

            if child.nodeType() == QtXml.QDomNode.NodeType.ElementNode:
                if child.nodeName() == "ReportHeader":
                    self.setSectionAttributes(self.rHeader_, child)

                elif child.nodeName() == "PageHeader":
                    self.setSectionAttributes(self.pHeader_, child)

                elif child.nodeName() == "AddOnHeader":
                    addOnHeader = MReportSection("AddOnHeader")
                    self.addOnHeaders_.append(addOnHeader)
                    self.setDetMiscAttributes(addOnHeader, child)
                    self.setDetailAttributes(addOnHeader, child)

                elif child.nodeName() == "DetailHeader":
                    dHeader = MReportSection("DetailHeader")
                    self.dHeaders_.append(dHeader)
                    self.setDetMiscAttributes(dHeader, child)
                    self.setDetailAttributes(dHeader, child)

                elif child.nodeName() == "Detail":
                    detail = MReportSection("Detail")
                    self.details_.append(detail)
                    self.setDetailAttributes(detail, child)

                elif child.nodeName() == "DetailFooter":
                    dFooter = MReportSection("DetailFooter")
                    self.setDetMiscAttributes(dFooter, child)
                    self.setDetailAttributes(dFooter, child)
                    self.dFooters_.append(dFooter)

                elif child.nodeName() == "AddOnFooter":
                    addOnFooter = MReportSection("AddOnFooter")
                    self.setDetMiscAttributes(addOnFooter, child)
                    self.setDetailAttributes(addOnFooter, child)
                    self.addOnFooters_.append(addOnFooter)

                elif child.nodeName() == "PageFooter":
                    self.setSectionAttributes(self.pFooter_, child)

                elif child.nodeName() == "ReportFooter":
                    self.setSectionAttributes(self.rFooter_, child)

    @decorators.BetaImplementation
    def slotCancelRendering(self):
        self.cancelRender_ = True

    @decorators.BetaImplementation
    def findDetailHeader(self, level):
        for sec in self.dHeaders_:
            if sec.getLevel() == level:
                return sec
        return 0

    @decorators.BetaImplementation
    def findAddOnHeader(self, level):
        for sec in self.addOnHeaders_:
            if sec.getLevel() == level:
                return sec
        return 0

    @decorators.BetaImplementation
    def findDetail(self, level):
        for sec in self.details_:
            if sec.getLevel() == level:
                return sec
        return 0

    @decorators.BetaImplementation
    def findDetailFooter(self, level):
        for sec in self.dFooters_:
            if sec.getLevel() == level:
                return sec
        return 0

    @decorators.BetaImplementation
    def findAddOnFooter(self, level):
        for sec in self.addOnFooters_:
            if sec.getLevel() == level:
                return sec

        for sec in self.addOnFooters_:
            if sec.getLevel() == -1:
                return sec
        return 0

    @decorators.BetaImplementation
    def mapToOdsCell(self, r):
        ret = QtCore.QRect()

        if r.x() <= self.AQ_ODSCELL_WIDTH:
            ret.setX(0)
        else:
            ret.setX(r.x() / self.AQ_ODSCELL_WIDTH)

        if r.y() <= self.AQ_ODSCELL_HEIGHT:
            ret.setY(0)
        else:
            ret.setY(r.y() / self.AQ_ODSCELL_HEIGHT)

        w = round(float(r.width()) / self.AQ_AQ_ODSCELL_WIDTH)
        if w == 0:
            w = 1
        ret.setWidth(w)

        h = round(float(r.height()) / self.AQ_AQ_ODSCELL_HEIGHT)
        if h == 0:
            h = 1
        ret.setWidth(h)

        return ret

    @decorators.BetaImplementation
    def execPage(self, painter, s, nrecords, aqmap):
        c = Qt.Q_UINT8
        tiny_len = Qt.Q_UINT8
        i_8 = Qt.Q_INT8
        i_16 = Qt.Q_INT16
        i1_16 = Qt.Q_INT16
        i2_16 = Qt.Q_INT16
        leng = Qt.Q_INT32
        ul = Qt.Q_UINT32
        p = QtCore.QPoint()
        p1 = QtCore.QPoint()
        p2 = QtCore.QPoint()
        r = QtCore.QRect()
        a = QtCore.QPointArray()
        string = ""
        str1 = ""
        color = QtCore.QColor()
        font = QtGui.QFont()
        pen = QtGui.QPen()
        brush = QtGui.QBrush()
        rgn = QtCore.QRegion()
        matrix = QtCore.QWMatrix()
        handled = False
        chkRow = 0

        while nrecords > 0 and not s.eof():
            nrecords -= 1

            handled = True
            s >> c
            s >> tiny_len
            if tiny_len == 255:
                s >> leng
            else:
                leng = tiny_len

            # if ((chkRow = (nrecords / 4) % 40) == 0) #FIXME
            chkRow = (nrecords / 4) % 40
            if chkRow == 0:
                self.signalRenderStatus.emit(nrecords / 4)
            if self.cancelRender_:
                return False

            if c == QtCore.QPaintDevice.PaintDeviceMetric.PdcNOP:
                pass
            elif c == QtCore.QPaintDevice.PaintDeviceMetric.PdcDrawPoint:
                s >> p
            elif c == QtCore.QPaintDevice.PaintDeviceMetric.PdcMoveTo:
                s >> p
            elif c == QtCore.QPaintDevice.PaintDeviceMetric.PdcLineTo:
                s >> p
            elif c == QtCore.QPaintDevice.PaintDeviceMetric.PdcDrawLine:
                s >> p1 >> p2
            elif c == QtCore.QPaintDevice.PaintDeviceMetric.PdcDrawRect:
                s >> r
            elif c == QtCore.QPaintDevice.PaintDeviceMetric.PdcDrawRoundRect:
                s >> r >> i1_16 >> i2_16
            elif c == QtCore.QPaintDevice.PaintDeviceMetric.PdcDrawEllipse:
                s >> r
            elif c == QtCore.QPaintDevice.PaintDeviceMetric.PdcDrawArc:
                s >> r >> i1_16 >> i2_16
            elif c == QtCore.QPaintDevice.PaintDeviceMetric.PdcDrawPie:
                s >> r >> i1_16 >> i2_16
            elif c == QtCore.QPaintDevice.PaintDeviceMetric.PdcDrawChord:
                s >> r >> i1_16 >> i2_16
            elif c == QtCore.QPaintDevice.PaintDeviceMetric.PdcDrawLineSegments:
                s >> a
            elif c == QtCore.QPaintDevice.PaintDeviceMetric.PdcDrawPolyline:
                s >> a
            elif c == QtCore.QPaintDevice.PaintDeviceMetric.PdcDrawPolygon:
                s >> a >> i_8
            elif c == QtCore.QPaintDevice.PaintDeviceMetric.PdcDrawCubicBezier:
                s >> a
            elif c == QtCore.QPaintDevice.PaintDeviceMetric.PdcDrawText:
                s >> p >> str1
                handled = False
            elif c == QtCore.QPaintDevice.PaintDeviceMetric.PdcDrawTextFormatted:
                s >> r >> i_16 >> str1
                handled = False
            elif c == QtCore.QPaintDevice.PaintDeviceMetric.PdcDrawText2:
                s >> p >> string
                handled = False
            elif c == QtCore.QPaintDevice.PaintDeviceMetric.PdcDrawText2Formatted:
                s >> r >> i_16 >> string
                wm = painter.worldMatrix()

                item = MReportEngine.AQPaintItem()
                item.rr_ = wm.mapRect(r)
                item.r_ = self.mapToOdsCell(item.rr_)
                item.str_ = string
                item.tf_ = i_16
                item.bgColor_ = painter.backgroundColor()
                item.brush_ = painter.brush()
                item.fnt_ = painter.font()
                item.pen_ = painter.pen()
                pKey = QtCore.QPoint(item.rr_.x(), item.r_.y())
                aqmap.insert(MReportEngine.AQPointKey(pKey), item)
            elif c == QtCore.QPaintDevice.PaintDeviceMetric.PdcDrawPixmap:
                pixmap = QtGui.QPixmap()
                s >> r >> pixmap
                wm = painter.worldMatrix()

                item = MReportEngine.AQPaintItem()
                item.rr_ = wm.mapRect(r)
                item.r_ = self.mapToOdsCell(item.rr_)
                item.str_ = "Pixmap"
                item.bgColor_ = painter.backgroundColor()
                item.pix_ = pixmap
                pKey = QtCore.QPoint(item.rr_.x(), item.r_.y())
                aqmap.insert(MReportEngine.AQPointKey(pKey), item)
            elif c == QtCore.QPaintDevice.PaintDeviceMetric.PdcDrawImage:
                image = QtCore.QImage()
                s >> r >> image
                handled = False
            elif c == QtCore.QPaintDevice.PaintDeviceMetric.PdcBegin:
                s >> ul
                if not self.execPage(painter, s, ul, aqmap):
                    return False
            elif c == QtCore.QPaintDevice.PaintDeviceMetric.PdcEnd:
                if nrecords == 0:
                    return True
            elif c == QtCore.QPaintDevice.PaintDeviceMetric.PdcSave:
                s >> string
                painter.save(string)
            elif c == QtCore.QPaintDevice.PaintDeviceMetric.PdcRestore:
                painter.restore()
            elif c == QtCore.QPaintDevice.PaintDeviceMetric.PdcSetBkColor:
                s >> color
                painter.setBackgroundColor(color)
            elif c == QtCore.QPaintDevice.PaintDeviceMetric.PdcSetBkMode:
                s >> i_8
                painter.setBackgroundMode(i_8)
            elif c == QtCore.QPaintDevice.PaintDeviceMetric.PdcSetROP:
                s >> i_8
                painter.setRasterOp(i_8)
            elif c == QtCore.QPaintDevice.PaintDeviceMetric.PdcSetBrushOrigin:
                s >> p
                painter.setBrushOrigin(p)
            elif c == QtCore.QPaintDevice.PaintDeviceMetric.PdcSetFont:
                s >> font
                painter.setFont(font)
            elif c == QtCore.QPaintDevice.PaintDeviceMetric.PdcSetPen:
                s >> pen
                painter.setPen(pen)
            elif c == QtCore.QPaintDevice.PaintDeviceMetric.PdcSetBrush:
                s >> brush
                painter.setBrush(brush)
            elif c == QtCore.QPaintDevice.PaintDeviceMetric.PdcSetTabStops:
                s >> i_16
            elif c == QtCore.QPaintDevice.PaintDeviceMetric.PdcSetTabArray:
                s >> i_16
            elif c == QtCore.QPaintDevice.PaintDeviceMetric.PdcSetVXform:
                s >> i_8
                painter.setViewXForm(i_8)
            elif c == QtCore.QPaintDevice.PaintDeviceMetric.PdcSetWindow:
                s >> r
                painter.setWindow(r)
            elif c == QtCore.QPaintDevice.PaintDeviceMetric.PdcSetViewport:
                s >> r
                painter.setViewport(r)
            elif c == QtCore.QPaintDevice.PaintDeviceMetric.PdcSetWXform:
                s >> i_8
                # painter.setWorldXForm(i_8) # FIXME
            elif c == QtCore.QPaintDevice.PaintDeviceMetric.PdcSetWMatrix:
                s >> matrix >> i_8
                painter.setWorldMatrix(matrix, i_8)
            elif c == QtCore.QPaintDevice.PaintDeviceMetric.PdcSaveWMatrix:
                painter.saveWorldMatrix()
            elif c == QtCore.QPaintDevice.PaintDeviceMetric.PdcRestoreWMatrix:
                painter.restoreWorldMatrix()
            elif c == QtCore.QPaintDevice.PaintDeviceMetric.PdcSetClip:
                s >> i_8
                painter.setClipping(i_8)
            elif c == QtCore.QPaintDevice.PaintDeviceMetric.PdcSetClipRegion:
                s >> rgn >> i_8
                painter.setClipRegion(rgn, i_8)
            else:
                QtCore.qWarning(
                    "mreporengine.cpp execPage: Invalid command {}".format(c))
                if leng:
                    s.device().at(s.device().at() + leng)

            if not handled:
                QtCore.qWarning("Command not handled cmd:{} len:{}".format(c, len))
                pass

    @decorators.BetaImplementation
    def precisionPartDecimal(self, string):
        comma = QtWidgets.QApplication.commaSeparator()
        posComma = string.rfind(comma)
        if posComma == -1:
            return 0
        strAux = string.strip()
        partDecimal = strAux[-(len(strAux) - posComma - 1):]
        prec = len(partDecimal)

        while prec > 0:
            ch = partDecimal[(prec - 1):prec]
            if ch.isdigit() and ch != "0":
                break
            prec -= 1
        return prec

    @decorators.BetaImplementation
    def exportToOds(self, pages):
        odsGen = AQOdsGenerator()
        spreadsheet = AQOdsSpreadSheet(odsGen)

        mapList = QtCore.QValueList()
        totalRecords = 0
        nullPdev = MReportEngine.AQNullPaintDevice()
        painter = QtGui.QPainter()
        curIdx = pages.getCurrentIndex()
        yOffset = 0
        aqmap = MReportEngine.AQPaintItemMap()
        dirtyMap = False

        painter.begin(nullPdev)
        for i in range(pages.pageCount()):
            pg = pages.getPageAt(i)
            ba = QtCore.QByteArray(pg.size() + Qt.Q_UINT32.__sizeof__())

            sWrite = QtCore.QDataStream(ba, Qt.IO_WriteOnly)
            sWrite << pg

            sRead = QtCore.QDataStream(ba, Qt.IO_ReadOnly)
            sRead.device().at(14)
            sRead.setVersion(5)

            c = Qt.Q_UINT8
            clen = Qt.Q_UINT8
            nrecords = Qt.Q_UINT32
            sRead >> c >> clen

            dummy = Qt.Q_INT32
            sRead >> dummy >> dummy >> dummy >> dummy
            sRead >> nrecords

            if not self.execPage(painter, sRead, nrecords, aqmap):
                return

            itAux = len(aqmap) - 1

            # if (*itAux).r_.y() >= self.AQ_ODS_ROWS_LIMIT: #FIXME
            if aqmap[itAux].r_.y() >= self.AQ_ODS_ROWS_LIMIT:
                mapList.append(aqmap)
                aqmap.clear()
                painter.resetXForm()
                yOffset = 0
                dirtyMap = False
            else:
                # painter.translate(0, (*itAux).rr_.y() - yOffset) #FIXME
                painter.translate(0, aqmap[itAux].rr_.y() - yOffset)
                # yOffset = (*itAux).rr_.y() #FIXME
                yOffset = aqmap[itAux].rr_.y()
                dirtyMap = True

        if dirtyMap:
            mapList.append(aqmap)

        totalRecords = totalRecords + aqmap.size()
        painter.end()

        pages.setCurrentPage(curIdx)
        painter = None
        nullPdev = None

        rowCount = len(self.records_) / 2
        if rowCount == 0:
            rowCount = 1
        relSteps = totalRecords / rowCount + 1
        step = 0
        nPage = 1

        for itList in mapList:
            nRow = 0
            nCol = 0
            curNRow = 0
            curNCol = 0
            curRow = 0
            sheet = AQOdsSheet(spreadsheet, "Pag.{}".format(nPage))

            aqmap = itList
            for it in aqmap:
                if (step % relSteps) == 0:
                    self.signalRenderStatus.emit((step / relSteps) % rowCount)
                if self.cancelRender_:
                    return

                cell = it.r_

                if (curNRow > cell.y()):
                    QtCore.qWarning(
                        "** MReportEngine::exportToOds curNRow > cell.y()")
                    pass

                if curRow and curNRow < cell.y():
                    curRow.close()
                    curRow = None
                    curRow = 0
                    nRow += 1

                curNRow = cell.y()
                while nRow < curNRow:
                    row = AQOdsRow(sheet)
                    row.coveredCell()
                    row.close()

                    nRow += 1

                if not curRow:
                    curRow = AQOdsRow(sheet)
                    curNCol = 0
                    nCol = 0

                if curNCol > cell.x():
                    QtCore.qWarning(
                        "** MReportEngine::exportToOds curNCol > cell.x()")
                    pass

                curNCol = cell.x()
                while nCol < curNCol:
                    curRow.coveredCell()

                    nCol += 1

                string = it.str_
                if string and string != "":
                    pix = it.pix_

                    if pix.isNull():
                        curRow.addBgColor(AQOdsColor(it.bgColor_.rgb()))
                        pen = it.pen_
                        curRow.addFgColor(AQOdsColor(pen.color().rgb()))

                        tf = it.tf_
                        if tf & QtGui.QPainter.HAlignment.AlignHCenter:
                            curRow.opIn(AQOdsStyle(Qt.Style.ALIGN_CENTER))
                        elif tf & QtGui.QPainter.HAlignment.AlignLeft:
                            curRow.opIn(AQOdsStyle(Qt.Style.ALIGN_LEFT))
                        else:
                            curRow.opIn(AQOdsStyle(Qt.Style.ALIGN_RIGHT))

                        fnt = it.fnt_
                        if fnt.bold():
                            curRow.opIn(AQOdsStyle(Qt.Style.TEXT_BOLD))
                        if fnt.italic():
                            curRow.opIn(AQOdsStyle(Qt.Style.TEXT_ITALIC))
                        if fnt.underline():
                            curRow.opIn(AQOdsStyle(Qt.Style.TEXT_UNDERLINE))

                        prec = self.precisionPartDecimal(string)
                        if prec > 0:
                            curRow.setFixedPrecision(prec)
                            ok = False
                            val = QtWidgets.QApplication.localeSystem().toDouble(string, ok)
                            if ok:
                                curRow.opIn(val, cell.width(), cell.height())
                            else:
                                curRow.opIn(string, cell.width(),
                                            cell.height())
                        else:
                            curRow.opIn(string, cell.width(), cell.height())
                    else:
                        pixName = "pix{}".format(pix.serialNumer())
                        pixFileName = FLDiskCache.AQ_DISKCACHE_DIRPATH + \
                            "/" + pixName + str(datetime.now()) + ".png"
                        pix.save(pixFileName, "PNG")
                        curRow.opIn(
                            AQOdsImage(
                                pixName,
                                AQOdsCentimeters(
                                    float(it.rr_.width()) / 100.0 * 2.54),
                                AQOdsCentimeters(
                                    float(it.rr_.height()) / 100.0 * 2.54),
                                AQOdsCentimeters(0),
                                AQOdsCentimeters(0),
                                pixFileName
                            )
                        )
                        cell.setWidth(1)
                else:
                    curRow.coveredCell()

                nCol = nCol + cell.width()
                step += 1

            if curRow:
                curRow.close()
                curRow = None
                curRow = 0

            sheet.close()
            nPage += 1

        spreadsheet.close()

        fileName = FLDiskCache.AQ_DISKCACHE_DIRPATH + \
            "/report_" + str(datetime.now()) + ".ods"
        odsGen.generateOds(fileName)
        # sys.openUrl(fileName) #FIXME
        sys.openUrl(fileName)

        self.signalRenderStatus.emit(rowCount)

    @decorators.BetaImplementation
    def renderReport(self, initRow=0, initCol=0, pages=0, flags=RenderReportFlags.Display.value):
        self.fillRecords_ = flags & MReportEngine.RenderReportFlags.FillRecords.value
        pageBreak = flags & MReportEngine.RenderReportFlags.PageBreak.value
        append = flags & MReportEngine.RenderReportFlags.Append.value
        self.cancelRender_ = False
        self.currRecord_ = 0
        self.p_.setStyleName(self.styleName_)

        self.signalRenderStatus.emit(1)

        currentPage = 0
        currentPageCopy = 0
        lastPageFound = False

        if pages == 0:
            pages = MPageCollection(self)
            self.currPage_ = 0
        else:
            if append and not pageBreak:
                self.currX_ = self.leftMargin_
                lastPageFound = True
                currentPage = pages.getLastPage()
                self.p_.painter().end()

                if currentPage:
                    currentPageCopy = QtGui.QPicture(currentPage)
                    self.p_.painter().begin(currentPage)
                    currentPageCopy.play(self.p_.painter())
                    currentPageCopy = None

        self.currHeight_ = self.pageHeight_ - \
            (self.bottomMargin_ + self.pFooter_.getHeight())
        self.currDate_ = datetime.today()

        self.clearGrantTotals()

        for i in range(self.rFooter_.getCalcFieldCount()):
            self.grandTotal_.append(QtCore.QMemArray())

        if not lastPageFound:
            self.startPage(pages)
        rowCount = len(self.records_)

        if rowCount <= 1:
            rowCount = 2

        nRecord = 0

        self.drawDetail(pages, 0, nRecord, initRow, initCol)

        self.endPage(pages)

        self.p_.painter().end()

        pages.setPageDimensions(QtCore.QSize(self.pageWidth_, self.pageHeight_))
        pages.setPageSize(self.pageSize_)
        pages.setPageOrientation(self.pageOrientation_)
        pages.setPrintToPos(self.printToPos_)
        pages.setPageMargins(self.topMargin_, self.leftMargin_,
                             self.bottomMargin_, self.rightMargin_)

        self.fillRecords_ = False

        self.signalRenderStatus.emit(rowCount / 2)

        return pages

    @decorators.BetaImplementation
    def startPage(self, pages, levelAddOn=-1):
        self.currY_ = self.topMargin_
        self.currX_ = self.leftMargin_

        pages.appendPage()
        self.currPage_ += 1

        self.p_.painter().begin(pages.getCurrentPage())

        self.drawReportHeader(pages)

        self.drawPageHeader(pages)

        if self.currPage_ > 1 and levelAddOn >= 0:
            self.drawAddOnHeader(pages, -1, self.grandTotal_)
            for i in range(levelAddOn + 1):
                self.drawAddOnHeader(pages, i, self.gDTFooters_[
                                     i], self.gDTSFooters_[i])

    @decorators.BetaImplementation
    def endPage(self, pages):
        self.drawReportFooter(pages)

        self.drawPageFooter(pages)

    @decorators.BetaImplementation
    def newPage(self, pages, levelAddOn=-1):
        self.drawPageFooter(pages)

        self.p_.painter().end()

        self.startPage(pages, levelAddOn)

    @decorators.BetaImplementation
    def drawReportHeader(self, pages):
        if self.rHeader_.getHeight() == 0:
            return

        if (self.rHeader_.printFrequency() == MReportSection.PrintFrequency.FirstPage and
                self.currPage_ == 1) or (self.rHeader_.printFrequency() == MReportSection.PrintFrequency.EveryPage):
            self.rHeader_.setPageNumber(self.currPage_)
            self.rHeader_.setReportDate(self.currDate_)
            sectionHeight = self.rHeader_.getHeight()
            self.rHeader_.draw(self.p_, self.leftMargin_,
                               self.currY_, sectionHeight)
            self.currY_ = self.currY_ + sectionHeight

    @decorators.BetaImplementation
    def drawPageHeader(self, pages):
        if self.pHeader_.getHeight() == 0:
            return

        if (self.currY_ + self.pHeader_.getHeight()) > self.currHeight_:
            self.newPage(pages)

        if (self.pHeader_.printFrequency() == MReportSection.PrintFrequency.FirstPage and
                self.currPage_ == 1) or (self.pHeader_.printFrequency() == MReportSection.PrintFrequency.EveryPage):
            self.pHeader_.setPageNumber(self.currPage_)
            self.pHeader_.setReportDate(self.currDate_)
            sectionHeight = self.pHeader_.getHeight()
            self.pHeader_.draw(self.p_, self.leftMargin_,
                               self.currY_, sectionHeight)
            self.currY_ = self.currY_ + sectionHeight

    @decorators.BetaImplementation
    def drawPageFooter(self, pages):
        if self.pFooter_.getHeight() == 0:
            return

        # record = self.records_.item(self.currRecord_)
        # fields = record.attributes()

        self.pFooter_.setCalcFieldData()

        if (self.pFooter_.printFrequency() == MReportSection.PrintFrequency.FirstPage and
                self.currPage_ == 1) or (self.pFooter_.printFrequency() == MReportSection.PrintFrequency.EveryPage):
            self.pFooter_.setPageNumber(self.currPage_)
            self.pFooter_.setReportDate(self.currDate_)
            sectionHeight = self.pFooter_.getHeight()
            self.pFooter_.draw(self.p_, self.leftMargin_, (self.pageHeight_ -
                                                           self.bottomMargin_) - self.pFooter_.getHeight(), sectionHeight)
            self.currY_ = self.currY_ + sectionHeight

    @decorators.BetaImplementation
    def drawDetail(self, pages, level, currRecord, initRow=0, initCol=0):
        self.currRecord_ = currRecord

        detail = self.findDetail(level)

        if not self.canDrawDetailHeader(level, currRecord, self.currY_):
            if level > 0:
                self.drawAddOnFooter(
                    pages, (level - 1), self.gDTFooters[(level - 1)], self.gDTSFooters[(level - 1)])
            self.newPage(pages, level)

            if not self.findAddOnHeader(level):
                self.drawDetailHeader(pages, level)
        else:
            self.drawDetailHeader(pages, level)

        if not detail:
            self.drawDetailFooter(pages, level)
            return

        self.gDTFooters[level].clear()
        self.gDTSFooters[level].clear()

        chkRow = 0
        loops = 0

        if initCol != 0:
            self.currX_ = self.leftMargin_ + \
                (detail.getWidth() * (initCol - 1))

        if initRow != 0:
            self.currY_ = self.topMargin_ + \
                (detail.getHeight() * (initRow - 1))

        self.currLevel_ = level

        stopVar = False
        while not stopVar:
            record = self.records_.item(currRecord)
            if record.nodeType() == QtXml.QDomNode.NodeType.ElementNode:
                if self.currLevel_ == level:
                    # if ((chkRow = (nrecords / 2) % 20) == 0) #FIXME
                    chkRow = (currRecord / 2) % 20
                    if chkRow == 0:
                        self.signalRenderStatus.emit(currRecord / 2)
                    if self.cancelRender_:
                        lblCancel = MLabelObject()
                        lblCancel.setFont(
                            "Arial", 20, MLabelObject.FontWeight.Bold, False)
                        lblCancel.setText(FLUtil.translate(
                            self, "app", "INFORME INCOMPLETO\nCANCELADO POR EL USUARIO"))
                        lblCancel.setGeometry(
                            20, self.pageHeight_ / 2, 450, 70)
                        lblCancel.setHorizontalAlignment(
                            MLabelObject.HAlignment.Center)
                        lblCancel.setVerticalAlignment(
                            MLabelObject.VAlignment.Middle)
                        lblCancel.draw(self.p_)
                        return

                    fields = record.attributes()
                    self.reserveSzieForCalcFields(fields, level)

                    detail.setPageNumber(self.currPage_)
                    detail.setReportDate(self.currDate_)

                    if not self.canDrawDetail(level, currRecord, self.currY_):
                        if loops:
                            self.drawAddOnFooter(pages, level, self.gDTFooters_[
                                                 level], self.gDTSFooters_[level])
                        else:
                            if level > 0:
                                self.drawAddOnFooter(
                                    pages, (level - 1), self.gDTFooters_[(level - 1)], self.gDTSFooters_[(level - 1)])
                        self.newPage(pages, level)

                    record = self.records_.item(currRecord)
                    ptrRecord = record

                    self.setFieldValues(fields, level, detail, ptrRecord)

                    if detail.mustBeDrawed(ptrRecord):
                        detail.setCalcFieldData(
                            0, 0, ptrRecord, self.fillRecords_)
                        sectionHeight = detail.getHeight()
                        detail.draw(self.p_, self.currX_,
                                    self.currY_, sectionHeight)

                        self.currX_ = self.currX_ + detail.getWidth()

                        if self.currX_ >= (self.pageWidth_ - self.rightMargin_ - self.leftMargin_):
                            self.currX = self.leftMargin_
                            self.currY_ = self.currY_ + sectionHeight
                    currRecord += 1
                else:
                    self.drawDetail(pages, self.currLevel_, currRecord)

                if currRecord < self.records_.count():
                    record = self.records_.item(currRecord)
                    fields = record.attributes()
                    detailValue = fields.namedItem("level").nodeValue() or 0
                    self.currLevel_ = int(detailValue)

                if self.cancelRender_:
                    lblCancel = MLabelObject()
                    lblCancel.setFont(
                        "Arial", 20, MLabelObject.FontWeight.Bold, False)
                    lblCancel.setText(FLUtil.translate(
                        self, "app", "INFORME INCOMPLETO\nCANCELADO POR EL USUARIO"))
                    lblCancel.setGeometry(20, self.pageHeight_ / 2, 450, 70)
                    lblCancel.setHorizontalAlignment(
                        MLabelObject.HAlignment.Center)
                    lblCancel.setVerticalAlignment(
                        MLabelObject.VAlignment.Middle)
                    lblCancel.draw(self.p_)
                    return

            loops += 1
            if level <= self.currLevel_ and currRecord < self.records_.count():
                stopVar = True

            self.drawDetailFooter(pages, level, self.gDTFooters_[
                                  level], self.gDTSFooters_[level])

            footer = self.findDetailFooter(level)
            if footer and currRecord < self.records_.count():
                if footer.newPage():
                    self.newPage(pages)

    @decorators.BetaImplementation
    def updateCsvData(self, level, currRecord, csvData):
        detail = self.findDetail(level)
        if not detail:
            return

        currLevel = level
        chkRow = 0

        stopVar = False
        while not stopVar:
            record = self.records_.item(currRecord)
            if record.nodeType == QtXml.QDomNode.NodeType.ElementNode:
                if currLevel == level:
                    # if ((chkRow = (nrecords / 2) % 20) == 0) #FIXME
                    chkRow = (currRecord / 2) % 20
                    if chkRow == 0:
                        self.signalRenderStatus.emit(currRecord / 2)

                    fields = record.attributes()
                    self.reserveSzieForCalcFields(fields, level)

                    record = self.records_.item(currRecord)
                    ptrRecord = record

                    self.setFieldValues(fields, level, detail, ptrRecord)

                    if detail.mustBeDrawed(ptrRecord):
                        detail.setCalcFieldData(
                            0, 0, ptrRecord, self.fillRecords_)

                        rS = self.findDetail(level + 1)

                        if not rS:
                            for i in range(level + 1):
                                rS = self.findDetailHeader(i)
                                if rS:
                                    csvData = csvData + rS.csvData()
                                rS = self.findDetail(i)
                                if rS:
                                    csvData = csvData + rS.csvData()
                            csvData = csvData + "\n"
                    currRecord += 1
                else:
                    self.updateCsvData(currLevel, currRecord, csvData)

                if currRecord < self.records_.count():
                    record = self.records_.item(currRecord)
                    fields = record.attributes()
                    detailValue = fields.namedItem("level").nodeValue() or 0
                    currLevel = int(detailValue)

            if level <= currLevel and currRecord < self.records_.count():
                stopVar = True

    @decorators.BetaImplementation
    def csvData(self):
        csvData = ""
        nRecord = 0
        self.updateCsvData(0, nRecord, csvData)
        self.signalRenderStatus.emit(len(self.records_) / 2)
        return csvData

    @decorators.BetaImplementation
    def canDrawDetailHeader(self, level, currRecord, yPos):
        headerHeight = 0
        header = self.findDetailHeader(level)
        if header:
            headerHeight = header.getHeight()

        if not self.canDrawDetail(level, currRecord, (yPos + headerHeight)):
            return False

        return True

    @decorators.BetaImplementation
    def canDrawDetail(self, level, currRecord, yPos):
        nextLevel = None
        record = self.records_.item(currRecord)

        if (currRecord + 1) < self.records_.count():
            nextRecord = self.records_.item(currRecord + 1)
            nextFields = nextRecord.attributes()

            detailValue = nextFields.namedItem("level").nodeValue() or 0
            nextLevel = int(detailValue)
        else:
            nextLevel = 0

        detailHeight = 0
        detail = self.findDetail(level)
        if detail:
            fields = record.attributes()
            self.setFieldValues(fields, level, detail, record, True)
            detailHeight = detail.getHeight()

        addOnFooterHeight = 0
        addOnFooter = self.findAddOnFooter(level)
        if addOnFooter:
            addOnFooterHeight = addOnFooter.getHeight()

        if level == nextLevel:
            if (yPos + detailHeight + addOnFooterHeight) > self.currHeight_:
                return False

        elif level > nextLevel:
            footersHeight = 0

            levelFooter = level
            while levelFooter > nextLevel:
                footerAux = self.findDetailFooter(levelFooter)

                if footerAux:
                    footersHeight = footersHeight + footerAux.getHeight()

                levelFooter -= 1

            addOnFooterAuxHeight = 0
            addOnFooterAux = self.findAddOnFooter(nextLevel)
            if addOnFooterAux:
                addOnFooterAuxHeight = addOnFooterAux.getHeight()

            if (yPos + detailHeight + footersHeight + addOnFooterAuxHeight) > self.currHeight_:
                return False

        elif level < nextLevel:
            headersHeight = 0
            levelFooter = level + 1
            while levelFooter <= nextLevel:
                headerAux = self.findDetailHeader(levelFooter)

                if headerAux:
                    headersHeight = headersHeight + headerAux.getHeight()

                levelFooter += 1

            detailAux = self.findDetail(nextLevel)
            if detailAux:
                headersHeight = headersHeight + detailAux.getHeight()

            addOnFooterAuxHeight = 0
            addOnFooterAux = self.findAddOnFooter(nextLevel)
            if addOnFooterAux:
                addOnFooterAuxHeight = addOnFooterAux.getHeight()

            if (self.currY_ + detailHeight + headersHeight + addOnFooterAuxHeight) > self.currHeight_:
                return False

        return True

    @decorators.BetaImplementation
    def reserveSizeForCalcFields(self, fields, level):
        j = level
        while j >= 0:
            footer = self.findDetailFooter(j)

            if footer:
                self.gDTSFooters_[j].reserve(footer.getCalcFieldCount())

                for i in range(footer.getCalcFieldCount()):
                    self.gDTFooters_[j].append([])

            if footer:
                for i in range(fields.count()):
                    calcIdx = footer.getCalcFieldIndex(
                        fields.item(i).nodeName())

                    if calcIdx != -1:
                        self.gDTSFooters_[
                            j][calcIdx] = fields.item(i).nodeValue() or 0
            j -= 1

    @decorators.BetaImplementation
    def setFieldValues(self, fields, level, detail, ptrRecord, noTotal=False):
        for i in range(detail.getFieldCount()):
            detailValue = fields.namedItem(detail.getFieldName(i)).nodeValue
            detail.setFieldData(i, detailValue, ptrRecord, self.fillRecords_)

            if noTotal:
                continue

            calcIdx = self.rFooter_.getCalcFieldIndex(detail.getFieldName(i))
            if calcIdx != -1:
                vsize = self.grandTotal_[calcIdx].size()
                self.grandTotal_[calcIdx].resize(vsize + 1)
                self.grandTotal_[calcIdx][vsize] = float(detailValue)

            j = level
            while j >= 0:
                footer = self.findDetailFooter(j)
                if not footer:
                    continue

                calcIdx = footer.getCalcFieldIndex(detail.getFieldName(i))
                if calcIdx == -1:
                    continue

                vsize = self.gDTFooters_[j][calcIdx].size()
                self.gDTFooters_[j][calcIdx].resize(vsize + 1)
                self.gDTFooters_[j][calcIdx][vsize] = float(detailValue)

                j -= 1

    @decorators.BetaImplementation
    def drawDetailFooter(self, pages, level, gDT=0, gDTS=0):
        footer = self.findDetailFooter(level)
        header = self.findDetailHeader(level)

        if footer:
            record = self.records_.item(self.currRecord_)

            if not footer.mustBeDrawed(record):
                return

            footer.setPageNumber(self.currPage_)
            footer.setReportDate(self.currDate_)

            if (self.currY_ + footer.getHeight()) > self.currHeight_:
                self.newPage(pages)
                for i in range(level + 1):
                    self.drawAddOnHeader(pages, i, self.gDTFooters_[
                                         i], self.gDTSFooters_[i])

            if gDT:
                footer.setCalcFieldData(gDT, gDTS, record, self.fillRecords_)
            if header:
                footer.drawHeaderObjects(self.p_, pages, header)

            sectionHeight = footer.getHeight()
            if footer.placeAtBottom():
                footer.draw(self.p_, self.leftMargin_, (self.pageHeight_ - self.bottomMargin_ -
                                                        self.pFooter_.getHeight()) - footer.getHeight(), sectionHeight)
            else:
                footer.draw(self.p_, self.leftMargin_,
                            self.currY_, sectionHeight)

            self.currY_ = self.currY_ + sectionHeight

    @decorators.BetaImplementation
    def drawDetailHeader(self, pages, level):
        header = self.findDetailHeader(level)

        if header:
            record = self.records_.item(self.currRecord_)

            if not header.mustBeDrawed(record):
                return

            header.setPageNumber(self.currPage_)
            header.setReportDate(self.currDate_)

            if (self.currY_ + header.getHeight()) > self.currHeight_:
                self.newPage(pages)

            fields = record.attributes()

            for i in range(header.getFieldCount()):
                value = fields.namedItem(header.getFieldName(i)).nodeValue() or 0
                header.setFieldData(i, value, record, self.fillRecords_)

            header.setCalcFieldData(0, 0, record, self.fillRecords_)

            sectionHeight = header.getHeight()
            header.draw(self.p_, self.leftMargin_, self.currY_, sectionHeight)
            header.setLastPageIndex(pages.getCurrentIndex())
            header.setOnPage(self.p_.painter().device())
            self.currY_ = self.currY_ + sectionHeight

    @decorators.BetaImplementation
    def drawAddOnHeader(self, pages, level, gDT, gDTS=0):
        header = self.findAddOnHeader(level)

        if header:
            record = self.records_.item(self.currRecord_)

            if not header.mustBeDrawed(record):
                return

            header.setPageNumber(self.currPage_)
            header.setReportDate(self.currDate_)

            if (self.currY_ + header.getHeight()) > self.currHeight_:
                self.newPage(pages)

            fields = record.attributes()

            for i in range(header.getFieldCount()):
                value = fields.namedItem(header.getFieldName(i)).nodeValue() or 0
                header.setFieldData(i, value, record, self.fillRecords_)

            if gDT and level > -1:
                header.setCalcFieldData(gDT, gDTS, record, self.fillRecords_)

            header.setCalcFieldDataGT(self.grandTotal_)

            sectionHeight = header.getHeight()
            header.draw(self.p_, self.leftMargin_, self.currY_, sectionHeight)
            self.currY_ = self.currY_ + sectionHeight

    @decorators.BetaImplementation
    def drawAddOnFooter(self, pages, level, gDT, gDTS):
        footer = self.findAddOnFooter(level)

        if footer:
            record = self.records_.item(self.currRecord_)

            if not footer.mustBeDrawed(record):
                return

            footer.setPageNumber(self.currPage_)
            footer.setReportDate(self.currDate_)

            fields = record.attributes()

            for i in range(footer.getFieldCount()):
                value = fields.namedItem(footer.getFieldName(i)).nodeValue() or 0
                footer.setFieldData(i, value, record, self.fillRecords_)

            if gDT and level > -1:
                footer.setCalcFieldData(gDT, gDTS, record, self.fillRecords_)

            footer.setCalcFieldDataGT(self.grandTotal_)

            sectionHeight = footer.getHeight()
            if footer.placeAtBottom():
                footer.draw(self.p_, self.leftMargin_, (self.pageHeight_ - self.bottomMargin_ -
                                                        self.pFooter_.getHeight()) - footer.getHeight(), sectionHeight)
            else:
                footer.draw(self.p_, self.leftMargin_,
                            self.currY_, sectionHeight)
            self.currY_ = self.currY_ + sectionHeight

    @decorators.BetaImplementation
    def drawReportFooter(self, pages):
        if self.rFooter_.getHeight() == 0:
            return

        if (self.currY_ + self.rFooter_.getHeight()) > self.currHeight_:
            self.newPage(pages)

        if self.rFooter_.printFrequency() == MReportSection.PrintFrequency.EveryPage or \
                self.rFooter_.printFrequency() == MReportSection.PrintFrequency.LastPage:
            self.rFooter_.setCalcFieldData(self.grandTotal_)

            self.rFooter_.setPageNumber(self.currPage_)
            self.rFooter_.setReportDate(self.currDate_)
            sectionHeight = self.rFooter_.getHeight()
            self.rFooter_.draw(self.p_, self.leftMargin_,
                               self.currY_, sectionHeight)
            self.currY_ = self.currY_ + sectionHeight

    @decorators.BetaImplementation
    def getPageMetrics(self, size, orientation):
        ps = QtCore.QSize()

        s = size.value if hasattr(size, "value") else size
        o = orientation.value if hasattr(orientation, "value") else orientation

        if s >= self.PageSize.Custom.value:
            ps.setWidth(self.customWidthMM_ / 25.4 * 78.)
            ps.setHeight(self.customHeightMM_ / 25.4 * 78.)
            return ps

        if False:
            # WIN32/MAC #FIXME
            pass
        else:
            # LINUX
            if not self.printToPos_:
                printer = QtPrintSupport.QPrinter(QtPrintSupport.QPrinter.HighResolution)
                printer.setFullPage(True)
                printer.setOrientation(o)
                printer.setPageSize(s)
                ps.setWidth(printer.widthMM() / 25.4 * 78.)
                ps.setHeight(printer.heightMM() / 25.4 * 78.)
                del printer
            else:
                printer = FLPosPrinter()
                ps.setWidth(printer.widthMM() / 25.4 * 78.)
                ps.setHeight(printer.heightMM() / 25.4 * 78.)
                del printer

        return ps

    @decorators.BetaImplementation
    def setReportAttributes(self, report):
        attributes = report.attributes()

        self.pageSize_ = int(attributes.namedItem("PageSize").nodeValue() or 0)
        if self.pageSize_ > self.PageSize.Custom.value:
            self.pageSize_ = self.PageSize.CustomOld.value

        self.pageOrientation_ = int(
            attributes.namedItem("PageOrientation").nodeValue() or 0)
        self.topMargin_ = int(attributes.namedItem("TopMargin").nodeValue() or 0)
        self.bottomMargin_ = int(
            attributes.namedItem("BottomMargin").nodeValue() or 0)
        self.leftMargin_ = int(attributes.namedItem("LeftMargin").nodeValue() or 0)
        self.rightMargin_ = int(
            attributes.namedItem("RightMargin").nodeValue() or 0)
        self.styleName_ = attributes.namedItem("StyleName").nodeValue() or 0

        if not attributes.namedItem("CustomWidthMM").isNull():
            self.customWidthMM_ = int(
                attributes.namedItem("CustomWidthMM").nodeValue() or 0)

        if not attributes.namedItem("CustomHeightMM").isNull():
            self.customHeightMM_ = int(
                attributes.namedItem("CustomHeightMM").nodeValue() or 0)

        if not attributes.namedItem("PrintToPos").isNull():
            self.printToPos_ = (attributes.namedItem(
                "PrintToPos").nodeValue().upper() == "TRUE")

        ps = QtCore.QSize(self.getPageMetrics(
            self.pageSize_, self.pageOrientation_))
        self.pageWidth_ = ps.width()
        self.pageHeight_ = ps.height()

    @decorators.BetaImplementation
    def setSectionAttributes(self, section, report):
        attributes = report.attributes()

        section.setHeight(int(attributes.namedItem("Height").nodeValue() or 0))
        section.setPrintFrequency(
            int(attributes.namedItem("PrintFrequency").nodeValue() or 0))
        if attributes.contains("SectionId"):
            section.setIdSec(
                int(attributes.namedItem("SectionId").nodeValue() or 0))

        children = report.childNodes()
        childCount = len(children)

        for i in range(childCount):
            child = children.item(i)

            if child.nodeType() == QtXml.QDomNode.NodeType.ElementNode:
                if child.nodeName() == "Line":
                    attributes = child.attributes()
                    line = MLineObject()

                    self.setLineAttributes(line, attributes)
                    section.addLine(line)
                elif child.nodeName() == "Label":
                    attributes = child.attributes()
                    label = MLabelObject()

                    self.setLabelAttributes(label, attributes)
                    section.addLabel(label)
                elif child.nodeName() == "Special":
                    attributes = child.attributes()
                    field = MSpecialObject()

                    self.setSpecialAttributes(field, attributes)
                    section.addSpecialField(field)
                elif child.nodeName() == "CalculatedField":
                    attributes = child.attributes()
                    field = MCalcObject()

                    self.setCalculatedFieldAttributes(field, attributes)
                    section.addCalculatedField(field)

    @decorators.BetaImplementation
    def setDetMiscAttributes(self, section, report):
        attributes = report.attributes()

        section.setDrawIf(attributes.namedItem("DrawIf").nodeValue() or 0)

        if (attributes.contains("SectionId")):
            section.setIdSec(
                int(attributes.namedItem("SectionId").nodeValue() or 0))

        levelNode = attributes.namedItem("Level")
        if not levelNode.isNull():
            section.setLevel(int(attributes.namedItem("Level").nodeValue() or 0))
        else:
            section.setLevel(-1)

        n = attributes.namedItem("NewPage")
        if not n.isNull():
            section.setNewPage(n.nodeValue().upper() == "TRUE")
        else:
            section.setNewPage(False)

        n = attributes.namedItem("PlaceAtBottom")
        if not n.isNull():
            section.setPlaceAtBottom(n.nodeValue().upper() == "TRUE")
        else:
            section.setPlaceAtBottom(False)

        n = attributes.namedItem("DrawAllPages")
        if not n.isNull():
            section.setDrawAllPages(n.nodeValue().upper() == "TRUE")
        else:
            section.setDrawAllPages(False)

    @decorators.BetaImplementation
    def setDetailAttributes(self, section, report):
        attributes = report.attributes()

        section.setHeight(int(attributes.namedItem("Height").nodeValue() or 0))

        if attributes.contains("SectionId"):
            section.setIdSec(
                int(attributes.namedItem("SectionId").nodeValue() or 0))

        levelNode = attributes.namedItem("Level")
        if not levelNode.isNull():
            section.setLevel(int(attributes.namedItem("Level").nodeValue() or 0))
        else:
            section.setLevel(-1)

        section.setDrawIf(attributes.namedItem("DrawIf").nodeValue() or 0)
        cols = attributes.namedItem("Cols").nodeValue() or 0
        if not cols:
            cols = "1"

        width = math.ceil((self.pageWidth_ - self.rightMargin_ -
                           self.leftMargin_) / float(cols))
        section.setWidth(width)

        children = report.childNodes()
        childCount = len(children)

        for i in range(childCount):
            child = children.item(i)

            if child.nodeType() == QtXml.QDomNode.NodeType.ElementNode:
                if child.nodeName() == "Line":
                    attributes = child.attributes()
                    line = MLineObject()

                    self.setLineAttributes(line, attributes)
                    section.addLine(line)
                elif child.nodeName() == "Label":
                    attributes = child.attributes()
                    label = MLabelObject()

                    self.setLabelAttributes(label, attributes)
                    section.addLabel(label)
                elif child.nodeName() == "Special":
                    attributes = child.attributes()
                    field = MSpecialObject()

                    self.setSpecialAttributes(field, attributes)
                    section.addSpecialField(field)
                elif child.nodeName() == "CalculatedField":
                    attributes = child.attributes()
                    field = MCalcObject()

                    self.setCalculatedFieldAttributes(field, attributes)
                    section.addCalculatedField(field)
                elif child.nodeName() == "Field":
                    attributes = child.attributes()
                    field = MFieldObject()

                    self.setFieldAttributes(field, attributes)
                    section.addField(field)

    @decorators.BetaImplementation
    def setLineAttributes(self, line, attr):
        line.setLine(int(attr.namedItem("X1").nodeValue() or 0), int(attr.namedItem("Y1").nodeValue(
        )), int(attr.namedItem("X2").nodeValue() or 0), int(attr.namedItem("Y2").nodeValue() or 0))

        tmp = attr.namedItem("Color").nodeValue() or 0

        leng = len(tmp)
        find = tmp.find(",")
        findRev = tmp.rfind(",")

        line.setColor(
            int(tmp[find:]),
            int(tmp[find + 1:leng - findRev - find - 1]),
            int(tmp[-(leng - findRev - 1):])
        )

        line.setWidth(int(attr.namedItem("Width").nodeValue() or 0))
        line.setStyle(int(attr.namedItem("Style").nodeValue() or 0))

        if attr.contains("ObjectId"):
            line.setObjectId(int(attr.namedItem("ObjectId").nodeValue() or 0))

    @decorators.BetaImplementation
    def setLabelAttributes(self, label, attr):
        label.setPaintFunction(attr.namedItem("PaintFunction").nodeValue() or 0)
        label.setLabelFunction(attr.namedItem("LabelFunction").nodeValue() or 0)
        label.setText(attr.namedItem("Text").nodeValue().strip())
        label.setGeometry(int(attr.namedItem("X").nodeValue() or 0), int(attr.namedItem("Y").nodeValue(
        )), int(attr.namedItem("Width").nodeValue() or 0), int(attr.namedItem("Height").nodeValue() or 0))

        tmp = attr.namedItem("BackgroundColor").nodeValue() or 0
        if tmp.upper() == "NOCOLOR":
            label.setTransparent(True)
            label.setBackgroundColor(255, 255, 255)
        else:
            leng = len(tmp)
            find = tmp.find(",")
            findRev = tmp.rfind(",")

            label.setTransparent(False)
            label.setBackgroundColor(
                int(tmp[find:]),
                int(tmp[find + 1:leng - findRev - find - 1]),
                int(tmp[-(leng - findRev - 1):])
            )

        tmp = attr.namedItem("ForegroundColor").nodeValue() or 0
        label.setForegroundColor(
            int(tmp[find:]),
            int(tmp[find + 1:leng - findRev - find - 1]),
            int(tmp[-(leng - findRev - 1):])
        )

        tmp = attr.namedItem("BorderColor").nodeValue() or 0
        label.setBorderColor(
            int(tmp[find:]),
            int(tmp[find + 1:leng - findRev - find - 1]),
            int(tmp[-(leng - findRev - 1):])
        )

        label.setBorderWidth(int(attr.namedItem("BorderWidth").nodeValue() or 0))
        label.setBorderStyle(int(attr.namedItem("BorderStyle").nodeValue() or 0))
        label.setFont(
            attr.namedItem("FontFamily").nodeValue() or 0,
            float(attr.namedItem("FontSize").nodeValue() or 0) * self.relCalcDpi_,
            int(attr.namedItem("FontWeight").nodeValue() or 0),
            False if int(attr.namedItem(
                "FontItalic").nodeValue() or 0) == 0 else True
        )
        label.setHorizontalAlignment(
            int(attr.namedItem("HAlignment").nodeValue() or 0))
        label.setVerticalAlignment(
            int(attr.namedItem("VAlignment").nodeValue() or 0))
        label.setWordWrap(False if int(attr.namedItem(
            "WordWrap").nodeValue() or 0) == 0 else True)
        label.setChangeHeight(False if int(attr.namedItem(
            "ChangeHeight").nodeValue() or 0) == 0 else True)
        label.setDrawAtBottom(False if int(attr.namedItem(
            "DrawAtBottom").nodeValue() or 0) == 0 else True)
        label.setAdjustFontSize(True if int(attr.namedItem(
            "AdjustFontSize").nodeValue() or 0) == 1 else False)

        if attr.contains("ObjectId"):
            label.setObjectId(int(attr.namedItem("ObjectId").nodeValue() or 0))

    @decorators.BetaImplementation
    def setSpecialAttributes(self, field, attr):
        field.setType(int(attr.namedItem("Type").nodeValue() or 0))
        field.setDateFormat(int(attr.namedItem("DateFormat").nodeValue() or 0))

        self.setLabelAttributes(field, attr)

    @decorators.BetaImplementation
    def setFieldAttributes(self, field, attr):
        field.setFieldName(attr.namedItem("Field").nodeValue() or 0)
        field.setDataType(int(attr.namedItem("DataType").nodeValue() or 0))
        field.setDateFormat(int(attr.namedItem("DateFormat").nodeValue() or 0))
        field.setPrecision(int(attr.namedItem("Precision").nodeValue() or 0))
        field.setCurrency(int(attr.namedItem("Currency").nodeValue() or 0))
        field.setCommaSeparator(
            int(attr.namedItem("CommaSeparator").nodeValue() or 0))
        field.setCodBarType(int(attr.namedItem("CodBarType").nodeValue() or 0))
        res = int(attr.namedItem("DataType").nodeValue() or 0)
        field.setCodBarRes(res if res > 0 else 72)
        field.setBlankZero(int(attr.namedItem("BlankZero").nodeValue() or 0))

        tmp = attr.namedItem("NegValueColor").nodeValue() or 0

        leng = len(tmp)
        find = tmp.find(",")
        findRev = tmp.rfind(",")

        field.setNegValueColor(
            int(tmp[find:]),
            int(tmp[find + 1:leng - findRev - find - 1]),
            int(tmp[-(leng - findRev - 1):])
        )
        self.setLabelAttributes(field, attr)

    @decorators.BetaImplementation
    def setCalculatedFieldAttributes(self, field, attr):
        field.setCalculationType(
            int(attr.namedItem("CalculationType").nodeValue() or 0))
        field.setCalculationFunction(
            attr.namedItem("FunctionName").nodeValue() or 0)
        self.setFieldAttributes(field, attr)

        field.setDrawAtHeader(attr.namedItem("DrawAtHeader").nodeValue() or 0)
        field.setFromGrandTotal(attr.namedItem("FromGrandTotal").nodeValue() or 0)
        self.setFieldAttributes(field, attr)

    @decorators.BetaImplementation
    def setRelDpi(self, relDpi):
        self.relDpi_ = relDpi

        if True:
            # LINUX
            pdm = QtWidgets.QApplication.desktop()
            if pdm.logicalDpiX() < pdm.logicalDpiY():
                self.relCalcDpi_ = self.relDpi_ / pdm.logicalDpiY()
            else:
                self.relCalcDpi_ = self.relDpi_ / pdm.logicalDpiX()
        elif False:
            # WIN32 #FIXME
            pass
        else:
            # MAC #FIXME
            pass

        if self.p_:
            self.p_.setRelDpi(self.relCalcDpi_)

    @decorators.BetaImplementation
    def copy(self, mre):
        self.clear()

        self.rd = mre.rd
        self.rt = mre.rt

        self.pageSize_ = mre.pageSize_
        self.pageOrientation_ = mre.pageOrientation_
        self.topMargin_ = mre.topMargin_
        self.bottomMargin_ = mre.bottomMargin_
        self.leftMargin_ = mre.leftMargin_
        self.rightMargin_ = mre.rightMargin_
        self.pageWidth_ = mre.pageWidth_
        self.pageHeight_ = mre.pageHeight_
        self.relDpi_ = mre.relDpi_
        self.relCalcDpi_ = mre.relCalcDpi_
        self.fillRecords_ = mre.fillRecords_

        self.rHeader_ = mre.rHeader_
        self.pHeader_ = mre.pHeader_

        temp = mre.details_
        # temp.setAutoDelete(True) #FIXME

        for detail in temp:
            self.details_.append(detail)

        del temp

        self.pFooter_ = mre.pFooter_
        self.rFooter_ = mre.rFooter_

        self.currY_ = mre.currY_
        self.currHeight_ = mre.currHeight_
        self.currPage_ = mre.currPage_
        self.currDate_ = mre.currDate_
        self.cancelRender_ = mre.cancelRender_

        self.grandTotal_ = mre.grandTotal_

    @decorators.BetaImplementation
    def getRenderSteps(self):
        return len(self.records_) / 2

    @decorators.BetaImplementation
    def relDpi(self):
        return self.relDpi_

    @decorators.BetaImplementation
    def relCalcDpi(self):
        return self.relCalcDpi_

    @decorators.BetaImplementation
    def setStyleName(self, style):
        self.styleName_ = style
