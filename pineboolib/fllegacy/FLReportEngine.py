from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtXml

from pineboolib import decorators
from pineboolib.flcontrols import ProjectClass

from pineboolib.kugar.mreportengine import MReportEngine

from pineboolib.fllegacy.FLReportPages import FLReportPages
from pineboolib.fllegacy.FLDiskCache import FLDiskCache
from pineboolib.fllegacy.FLUtil import FLUtil
from PyQt5.QtXml import QDomNode as FLDomNodeInterface  # FIXME
import pineboolib


class FLReportEngine(MReportEngine):

    class FLReportEnginePrivate(ProjectClass):

        @decorators.BetaImplementation
        def __init__(self, q):
            super(FLReportEngine.FLReportEnginePrivate, self).__init__()
            self.qry_ = 0
            self.qFieldMtdList_ = 0
            self.qGroupDict_ = 0
            self.q_ = q
            self.template_ = ""

            self.qDoubleFieldList_ = []
            self.qImgFields_ = []

        @decorators.BetaImplementation
        def addRowToReportData(self, l):
            if not self.qry_.isValid():
                return

            row = QtXml.QDomElement(self.q_.rptXmlData().createElement("Row"))
            row.setAttribute("level", l)

            imgFieldsBack = []
            i = 0

            for it in self.qFieldList_:
                rawVal = self.qry_.value(i, True)
                empty = len(self.qImgFields_) == 0
                if not empty and self.qImgFields_.top() == i:
                    strVal = str(rawVal)
                    imgFieldsBack.push_front(self.qImgFields_.pop())
                    if not strVal or strVal == "":
                        row.setAttribute(it, strVal)
                        continue
                    imgFile = FLDiskCache.AQ_DISKCACHE_DIRPATH + "/"
                    imgFile += strVal + ".png"
                    if not QtCore.QFile.exists(imgFile):
                        pix = QtGui.QPixmap()
                        # pix.loadFromData(str(self.qry_.value(i))) #FIXME?
                        pix.loadFromData(self.qry_.value(i).toCString())
                        pix.save(imgFile, "PNG")
                    row.setAttribute(it, imgFile)
                else:
                    row.setAttribute(it, str(rawVal))
                i += 1

            self.rows_.appendChild(row)
            self.qImgFields_ = imgFieldsBack

        @decorators.BetaImplementation
        def groupBy(self, levelMax, vA):
            if not self.qry_.isValid():
                return

            g = self.qGroupDict_

            lev = 0
            val = str(self.qry_.value(g[str(lev)].field()))
            while lev < levelMax and vA.at(lev) == val:
                lev += 1

            for i in range(lev, levelMax):
                self.addRowToReportData(i)
                vA.at[i] = str(self.qry_.value(g[str(i)].field()))

            self.addRowToReportData(levelMax)

        @decorators.BetaImplementation
        def setQuery(self, qry):
            self.qry_ = qry

            if self.qry_:
                self.qFieldList_ = self.qry_.fieldList()
                self.qFieldMtdList_ = self.qry_.fieldMetaDataList()
                self.qGroupDict_ = self.qry_.groupDict()
                self.qDoubleFieldList_.clear()
                self.qImgFields_.clear()

                if not self.qFieldMtdList_:
                    return

                i = len(self.qFieldList_) - 1
                while i >= 0:
                    it = self.qFieldList_[i]
                    fmtd = self.qFieldMtdList_.find(
                        it.section('.', 1, 1).lower())
                    if fmtd:
                        if fmtd.type() == QtGui.QPixmap:
                            self.qImgFields_.append(i)
                        elif fmtd.type() == QtCore.Double:
                            self.qDoubleFieldList_.append(it)
                    i -= 1
            else:
                self.qFieldList_.clear()
                self.qDoubleFieldList_.clear()
                self.qImgFields_.clear()
                self.qFieldMtdList_ = 0
                self.qGroupDict_ = 0

    @decorators.BetaImplementation
    def __init__(self, parent=0):
        super(FLReportEngine, self).__init__(parent)

        self.d_ = FLReportEngine.FLReportEnginePrivate(self)

    @decorators.BetaImplementation
    def rptXmlData(self):
        return self.rd

    @decorators.BetaImplementation
    def rptXmlTemplate(self):
        return self.rt

    @decorators.BetaImplementation
    def setReportData(self, q):
        if isinstance(q, FLDomNodeInterface):
            return self.setFLReportData(q.obj())

        if not q:
            return

        if not self.rd:
            self.rd = QtXml.QDomDocument("KUGAR_DATA")

        tmpDoc = QtXml.QDomDocument("KUGAR_DATA")

        self.d_.rows_ = tmpDoc.createDocumentFragment()
        self.d_.setQuery(q)
        q.setForwardOnly(True)

        if not q.exec_():
            return False

        if not q.next():
            return False

        g = self.d_.qGroupDict_
        if not g:
            while True:
                self.d_.addRowToReportData(0)
                if not q.next():
                    break
        else:
            vA = QtCore.QStringListModel().stringList()
            for i in range(10):
                vA.append("")
            while True:
                self.d_.groupBy(len(g), vA)
                if not q.next():
                    break

        data = QtXml.QDomElement(tmpDoc.createElement("KugarData"))
        data.appendChild(self.d_.rows_)
        tmpDoc.appendChild(data)
        self.rd = tmpDoc
        self.d_.rows_.clear()

        self.initData()
        return True

    @decorators.BetaImplementation
    def setFLReportData(self, n):
        self.d_.setQuery(0)
        return super(FLReportEngine, self).setReportData(n)

    @decorators.BetaImplementation
    def setFLReportTemplate(self, t):
        if isinstance(t, QtXml.QDomNode):
            self.d_.template = ""
            return super(FLReportEngine, self).setReportTemplate(t)

        self.d_.template_ = t
        if not self.d_.qry_:
            mgr = pineboolib.project.conn.managerModules()
            return super(FLReportEngine, self).setReportTemplate(
                mgr.contentCached(t + ".kut")
            )
        else:
            return super(FLReportEngine, self).setReportTemplate(
                self.d_.qry_.db().managerModules().contentCached(t + ".kut")
            )

    @decorators.BetaImplementation
    def rptQueryData(self):
        return self.d_.qry_

    @decorators.BetaImplementation
    def rptNameTemplate(self):
        return self.d_.template_

    @decorators.BetaImplementation
    def setReportTemplate(self, t):
        if isinstance(t, FLDomNodeInterface):
            return self.setFLReportData(t.obj())

        return self.setFLReportData(t)

    @decorators.BetaImplementation
    def reportData(self):
        return FLDomNodeInterface.nodeInterface(
            self.rd if self.rd else QtXml.QDomDocument()
        )

    @decorators.BetaImplementation
    def reportTemplate(self):
        return FLDomNodeInterface.nodeInterface(
            self.rt if self.rt else QtXml.QDomDocument()
        )

    @decorators.BetaImplementation
    def exportToOds(self, pages):
        if not pages or not pages.pageCollection():
            return

        super(FLReportEngine, self).exportToOds(pages.pageCollection())

    @decorators.BetaImplementation
    def renderReport(self, initRow=0, initCol=0, fRec=False, pages=0):
        fr = MReportEngine.RenderReportFlags.FillRecords.value
        pgc = super(FLReportEngine, self).renderReport(
            initRow,
            initCol,
            pages.pageCollection() if pages else 0,
            fr if fRec else 0
        )

        pgs = FLReportPages()
        pgs.setPageCollection(pgc)
        empty = (self.d_.qDoubleFieldList_) == 0
        if not fRec or not self.d_.qry_ or not self.d_.qFieldMtdList_ or empty:
            return pgs

        nl = QtXml.QDomNodeList(self.rd.elementsByTagName("Row"))
        for i in range(nl.count()):
            itm = nl.item(i)
            if itm.isNull():
                continue
            nm = itm.attributes()

            for it in self.d_.qDoubleFieldList_:
                ita = nm.namedItem(it)
                if ita.isNull():
                    continue
                sVal = ita.nodeValue()
                if not sVal or sVal == "" or sVal.upper() == "NAN":
                    continue
                dVal = float(sVal)
                if not dVal:
                    dVal = 0
                decimals = self.d_.qFieldMtdList_.find(
                    it.section('.', 1, 1).lower()).partDecimal()
                ita.setNodeValue(FLUtil.formatoMiles(round(dVal, decimals)))
        return pgs
