from PyQt5.QtCore import Qt

from pineboolib import decorators
from pineboolib.flcontrols import ProjectClass

from pineboolib.kugar.mreportengine import MReportEngine

from pineboolib.fllegacy.FLReportPages import FLReportPages
from pineboolib.fllegacy.FLDiskCache import FLDiskCache
from pineboolib.fllegacy.FLUtil import FLUtil
# from pineboolib.fllegacy.FLDomNodeInterface import FLDomNodeInterface
from pineboolib.fllegacy.FLSqlConnections import FLSqlConnections


class FLReportEngine(MReportEngine):

    class FLReportEnginePrivate(ProjectClass):

        @decorators.BetaImplementation
        def __init__(self, q):
            self.qry_ = 0
            self.qFieldMtdList_ = 0
            self.qGroupDict_ = 0
            self.q_ = q

            self.qDoubleFieldList_ = Qt.QStringList()
            self.qImgFields_ = Qt.QValueStack()

        @decorators.BetaImplementation
        def addRowToReportData(self, l):
            if not self.qry_.isValid():
                return

            row = Qt.QDomElement(self.q_.rptXmlData().createElement("Row"))
            row.setAttribute("level", l)

            imgFieldsBack = Qt.QValueStack()
            i = 0

            it = self.qFieldList_.begin()
            while it != self.qFieldList_.end():
                rawVal = self.qry_.value(i, True)
                if not self.qImgFields_.isEmpty() and self.qImgFields_.top() == i:
                    strVal = str(rawVal)
                    imgFieldsBack.push_front(self.qImgFields_.pop())
                    if not strVal or strVal == "":
                        row.setAttribute(it, strVal)
                        continue
                    imgFile = FLDiskCache.AQ_DISKCACHE_DIRPATH + "/" + strVal + ".png"
                    if not Qt.QFile.exists(imgFile):
                        pix = Qt.QPixmap()
                        # pix.loadFromData(str(self.qry_.value(i))) #FIXME?
                        pix.loadFromData(self.qry_.value(i).toCString())
                        pix.save(imgFile, "PNG")
                    row.setAttribute(it, imgFile)
                else:
                    row.setAttribute(it, str(rawVal))

                it = it + 1
                i = i + 1

            self.rows_.appendChild(row)
            self.qImgFields_ = imgFieldsBack

        @decorators.BetaImplementation
        def groupBy(self, levelMax, vA):
            if not self.qry_.isValid():
                return

            g = self.qGroupDict_

            lev = 0
            while lev < levelMax and vA.at(lev) == str(self.qry_.value(g[str(lev)].field())):
                lev = lev + 1

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

                i = self.qFieldList_.size() - 1
                it = Qt.QStringList(self.qFieldList_.end())
                while i >= 0:
                    it = it - 1
                    fmtd = self.qFieldMtdList_.find(it.section('.', 1, 1).lower())
                    if fmtd:
                        if fmtd.type() == Qt.QPixmap:
                            self.qImgFields_.push(i)
                        elif fmtd.type() == Qt.Double:
                            self.qDoubleFieldList_ << it
                            break
                    i = i - 1
            else:
                self.qFieldList_.clear()
                self.qDoubleFieldList_.clear()
                self.qImgFields_.clear()
                self.qFieldMtdList_ = 0
                self.qGroupDict_ = 0

    @decorators.BetaImplementation
    def __init__(self, parent=0):
        super(FLReportEngine, self).__init__(parent)

        self.d_ = self.FLReportEnginePrivate(self)

    @decorators.BetaImplementation
    def rptXmlData(self):
        return self.rd_

    @decorators.BetaImplementation
    def rptXmlTemplate(self):
        return self.rt_

    @decorators.BetaImplementation
    def setReportData(self, q):
        if isinstance(q, FLDomNodeInterface):
            return self.setFLReportData(q.obj())

        if not q:
            return

        if not self.rd_:
            self.rd_ = Qt.QDomDocument("KUGAR_DATA")

        tmpDoc = Qt.QDomDocument("KUGAR_DATA")

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
            vA = Qt.QStringList()
            for i in range(10):
                vA.append("")
            while True:
                self.d_.groupBy(g.count(), vA)
                if not q.next():
                    break

        data = Qt.QDomElement(tmpDoc.createElement("KugarData"))
        data.appendChild(self.d_.rows_)
        tmpDoc.appendChild(data)
        self.rd_ = tmpDoc
        self.d_.rows_.clear()

        self.initData()
        return True

    @decorators.BetaImplementation
    def setFLReportData(self, n):
        self.d_.setQuery(0)
        return super(FLReportEngine, self).setReportData(n)

    @decorators.BetaImplementation
    def setFLReportTemplate(self, t):
        if isinstance(t, Qt.QDomNode):
            self.d_.template = ""
            return super(FLReportEngine, self).setReportTemplate(t)

        self.d_.template_ = t
        if not self.d_.qry_:
            return super(FLReportEngine, self).setReportTemplate(
                FLSqlConnections.database().managerModules().contentCached(t + ".kut")
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
        return self.d_.t_

    @decorators.BetaImplementation
    def setReportTemplate(self, t):
        if isinstance(t, FLDomNodeInterface):
            return self.setFLReportData(t.obj())

        return self.setFLReportData(t)

    @decorators.BetaImplementation
    def reportData(self):
        return FLDomNodeInterface.nodeInterface(self.rd_ if self.rd_ else Qt.QDomDocument())

    @decorators.BetaImplementation
    def reportTemplate(self):
        return FLDomNodeInterface.nodeInterface(self.rt_ if self.rt_ else Qt.QDomDocument())

    @decorators.BetaImplementation
    def exportToOds(self, pages):
        if not pages or not pages.pageCollection():
            return

        super(FLReportEngine, self).exportToOds(pages.pageCollection())

    @decorators.BetaImplementation
    def renderReport(self, initRow, initCol, fillRecords, pages):
        pgc = super(FLReportEngine, self).renderReport(
            initRow,
            initCol,
            pages.pageCollection() if pages else 0,
            MReportEngine.RenderReportFlags.FillRecords if fillRecords else 0
        )

        pgs = FLReportPages()
        pgs.setPageCollection(pgc)
        if not fillRecords or not self.d_.qry_ or not self.d_.qFieldMtdList_ or self.d_.qDoubleFieldList_.isEmpty():
            return pgs

        nl = Qt.QDomNodeList(self.rd_.elementsByTagName("Row"))
        for i in range(nl.count()):
            itm = nl.item(i)
            if itm.isNull():
                continue
            nm = itm.attributes()

            it = self.d_.qDoubleFieldList_.begin()
            while it != self.d_.qDoubleFieldList_.end():
                ita = nm.namedItem(it)
                if ita.isNull():
                    continue
                sVal = ita.nodeValue()
                if not sVal or sVal == "" or sVal.upper() == "NAN":
                    continue
                dVal = float(sVal)
                if not dVal:
                    dVal = 0
                decimals = self.d_.qFieldMtdList_.find(it.section('.', 1, 1).lower()).partDecimal()
                ita.setNodeValue(FLUtil.formatoMiles(round(dVal, decimals)))

                it = it + 1
        return pgs
