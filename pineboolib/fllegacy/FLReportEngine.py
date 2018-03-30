from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtXml

from pineboolib import decorators
from pineboolib.flcontrols import ProjectClass
from pineboolib.rml.kut2rml import kut2rml
from pineboolib.rml.rml2pdf import rml2pdf
from pineboolib.utils import filedir

from pineboolib.fllegacy.FLDiskCache import FLDiskCache
from pineboolib.fllegacy.FLUtil import FLUtil
from PyQt5.QtXml import QDomNode as FLDomNodeInterface  # FIXME
import pineboolib

import os
import datetime


class FLReportEngine(object):

    class FLReportEnginePrivate(object):

        @decorators.BetaImplementation
        def __init__(self, q):
            self.qry_ = 0
            self.qFieldMtdList_ = 0
            self.qGroupDict_ = 0
            self.q_ = q
            self.template_ = ""

            self.qDoubleFieldList_ = []
            self.qImgFields_ = []

        @decorators.NotImplementedWarn
        def addRowToReportData(self, l):
            if not self.qry_.isValid():
                return
            row = QtXml.QDomElement(self.q_.rptXmlData().createElement("Row"))
            row.setAttribute("level", l)

            imgFieldsBack = []
            i = 0
            for it in self.qFieldList_:
                strVal = str(self.qry_.value(i, False))
                if self.qImgFields_ and self.qImgFields_[len(self.qImgFields_) - 1] == i:
                    imgFieldsBack.append(self.qImgFields_.pop())
                    if strVal in ["", "None"]:
                        row.setAttribute(it, strVal)
                        continue
                    imgFile = filedir("../tempdata")
                    imgFile += "/%s.png" % strVal
                    if not os.path.exists(imgFile):
                        #print("Creando", imgFile)
                        #print(self.qry_.value(i, True))
                        pix = QtGui.QPixmap(self.qry_.value(i, True))
                        if not pix.save(imgFile):
                            print("FLReportEngine::No se ha podido guardar", imgFile)
                    row.setAttribute(it, imgFile)
                else:
                    row.setAttribute(it, strVal)
                i += 1

            self.rows_.appendChild(row)
            self.qImgFields_ = imgFieldsBack

        @decorators.BetaImplementation
        def groupBy(self, levelMax, vA):
            if not self.qry_.isValid():
                return

            g = self.qGroupDict_
            lev = 0
            val = str(self.qry_.value(g[lev]))
            while lev < levelMax and vA[lev] == val:
                lev += 1

            for i in range(lev, levelMax):
                self.addRowToReportData(i)
                vA[i] = str(self.qry_.value(g[i]))

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
                    key = it[it.find(".") + 1:].lower()
                    if key in self.qFieldMtdList_.keys():
                        fmtd = self.qFieldMtdList_[key]
                        if fmtd.type() == "pixmap":
                            self.qImgFields_.append(i)
                        elif fmtd.type() == "double":
                            self.qDoubleFieldList_.append(it)
                    i -= 1
            else:
                self.qFieldList_.clear()
                self.qDoubleFieldList_.clear()
                self.qImgFields_.clear()
                self.qFieldMtdList_ = []
                self.qGroupDict_ = {}

    @decorators.BetaImplementation
    def __init__(self, parent):
        self.d_ = FLReportEngine.FLReportEnginePrivate(self)
        self.relDpi_ = 78.
        self.rd = None

    @decorators.NotImplementedWarn
    def rptXmlData(self):
        return self.rd

    @decorators.BetaImplementation
    def rptXmlTemplate(self):
        return self.rt

    @decorators.NotImplementedWarn
    def relDpi(self):
        return self.relDpi_

    @decorators.NotImplementedWarn
    def setReportData(self, q):
        if isinstance(q, FLDomNodeInterface):
            return self.setFLReportData(q.obj())
        if not q:
            return

        if not self.rd:
            self.rd = QtXml.QDomDocument("QUERY_DATA")

        tmpDoc = QtXml.QDomDocument("QUERY_DATA")

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
            vA = []
            for i in range(10):
                vA.append(None)
            while True:
                self.d_.groupBy(len(g), vA)
                if not q.next():
                    break

        data = QtXml.QDomElement(tmpDoc.createElement("queryData"))
        data.appendChild(self.d_.rows_)
        tmpDoc.appendChild(data)
        self.rd = tmpDoc
        self.d_.rows_.clear()

        self.initData()
        return True

    @decorators.NotImplementedWarn
    def setFLReportData(self, n):
        self.d_.setQuery(0)
        return super(FLReportEngine, self).setReportData(n)

    @decorators.BetaImplementation
    def setFLReportTemplate(self, t):
        # buscamos el .kut o el .rlab

        self.d_.template_ = t

        if not self.d_.qry_:
            mgr = pineboolib.project.conn.managerModules()

        else:
            mgr = self.d_.qry_.db().managerModules()

        rpt = mgr.contentCached(t + ".kut")
        if not rpt:
            rpt = mgr.contentCached(t + ".rlab")

        self.rt = rpt
        return True

    @decorators.BetaImplementation
    def rptQueryData(self):
        return self.d_.qry_

    @decorators.NotImplementedWarn
    def rptNameTemplate(self):
        return self.d_.template_

    @decorators.BetaImplementation
    def setReportTemplate(self, t):
        if isinstance(t, FLDomNodeInterface):
            return self.setFLReportData(t.obj())

        return self.setFLReportData(t)

    @decorators.NotImplementedWarn
    def reportData(self):
        return FLDomNodeInterface.nodeInterface(
            self.rd if self.rd else QtXml.QDomDocument()
        )

    @decorators.NotImplementedWarn
    def reportTemplate(self):
        return FLDomNodeInterface.nodeInterface(
            self.rt if self.rt else QtXml.QDomDocument()
        )

    @decorators.NotImplementedWarn
    def exportToOds(self, pages):
        if not pages or not pages.pageCollection():
            return

        super(FLReportEngine, self).exportToOds(pages.pageCollection())

    @decorators.BetaImplementation
    def renderReport(self, initRow=0, initCol=0, fRec=False, pages=None):
        if self.rt.find("KugarTemplate") > -1:
            parser = kut2rml()
            self.rt = parser.parse(self.d_.template_, self.rt, self.rd.toString(1))

            pdfname = filedir("../tempdata")
            pdfname += "/%s.pdf" % datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            rml2pdf.parsepdf.parse(self.rt, pdfname)

            # print(self.rd.toString(1))
        """
        fr = MReportEngine.RenderReportFlags.FillRecords.value

        pgs = FLReportPages()
        if pages:
            pgs.setPageCollection(pages)

        pgc = super(FLReportEngine, self).renderReport(
            initRow,
            initCol,
            pgs,
            fr if fRec else 0
        )

        pgs.setPageCollection(pgc)
        if not fRec or not self.d_.qry_ or not self.d_.qFieldMtdList_ or not self.d_.qDoubleFieldList_:
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
        """

    @decorators.BetaImplementation
    def initData(self):
        n = self.rd.firstChild()
        while not n.isNull():
            if n.nodeName() == "KugarData":
                self.records_ = n.childNodes()
                attr = n.attributes()
                tempattr = attr.namedItem("Template")
                tempname = tempattr.nodeValue() or None
                if tempname is not None:
                    self.preferedTemplate.emit(tempname)
                    break
            n = n.nextSibling()
