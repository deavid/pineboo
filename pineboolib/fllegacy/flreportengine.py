from typing import List
from PyQt5 import QtXml  # type: ignore
from PyQt5.QtXml import QDomNode as FLDomNodeInterface  # type: ignore # FIXME

from pineboolib.core import decorators
from pineboolib import logging
from pineboolib.application.database.pnsqlquery import PNSqlQuery
from typing import Any, Optional, Dict


class FLReportEngine(object):

    report_ = None
    rt: str = ""  # KUGAR *.kut template data as a string

    def __init__(self, parent) -> None:
        self.d_ = FLReportEngine.FLReportEnginePrivate(self)
        self.relDpi_ = 78.0
        self.rd: Optional[QtXml.QDomDocument] = None
        self.logger = logging.getLogger("FLReportEngine")
        from pineboolib.application.parsers.kugarparser.kut2fpdf import Kut2FPDF

        self.parser_: Kut2FPDF = Kut2FPDF()

    class FLReportEnginePrivate(object):
        rows_: Optional[Any]

        def __init__(self, q):
            self.qry_: Optional[PNSqlQuery] = None
            self.qFieldMtdList_ = None
            self.qGroupDict_: Dict[int, str] = {}
            self.q_ = q
            self.template_ = ""

            self.qFieldList_: List[str] = []
            self.qDoubleFieldList_: List[str] = []
            self.qImgFields_: List[str] = []
            self.report_ = None

        def addRowToReportData(self, l):
            if not self.qry_.isValid():
                return

            row = self.q_.rptXmlData().createElement("Row")
            row.setAttribute("level", l)
            i = 0
            for it in self.qFieldList_:
                strVal = str(self.qry_.value(it, False))
                if self.qImgFields_:
                    if self.qImgFields_[-1] == i:
                        self.qImgFields_.append(self.qImgFields_.pop())
                        if strVal in ["", "None"]:
                            row.setAttribute(it, strVal)
                            continue

                    key = self.qry_.value(i, False)
                    row.setAttribute(it, key)

                else:
                    row.setAttribute(it, strVal)
                i += 1

            self.rows_.appendChild(row)

        def groupBy(self, levelMax, vA):
            if not self.qry_.isValid():
                return

            # self.qGroupDict_
            lev = 0

            while lev < levelMax and str(self.qry_.value(self.qGroupDict_[lev])) == str(
                vA[lev]
            ):
                lev += 1

            for i in range(lev, levelMax):
                self.addRowToReportData(i)
                vA[i] = str(self.qry_.value(self.qGroupDict_[i]))

            self.addRowToReportData(levelMax)

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
                    key = it[it.find(".") + 1 :].lower()
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

    def rptXmlData(self) -> Any:
        return self.rd

    def rptXmlTemplate(self) -> str:
        return self.rt

    def relDpi(self) -> float:
        return self.relDpi_

    def setReportData(self, q=None) -> Optional[bool]:
        if isinstance(q, FLDomNodeInterface):
            return self.setFLReportData(q)
        if q is None:
            return None

        self.rd = QtXml.QDomDocument("KugarData")

        self.d_.rows_ = (
            self.rd.createDocumentFragment()
        )  # FIXME: Don't set the private from the public.
        self.d_.setQuery(q)
        q.setForwardOnly(True)
        if q.exec_() and q.next():
            g = self.d_.qGroupDict_
            if not g:
                while True:
                    self.d_.addRowToReportData(0)
                    if not q.next():
                        break
            else:
                vA: List[None] = []
                for i in range(10):
                    vA.append(None)

                ok = True
                while ok:
                    self.d_.groupBy(len(g), vA)
                    if not q.next():
                        ok = False

        data = self.rd.createElement("KugarData")
        data.appendChild(self.d_.rows_)
        self.rd.appendChild(data)
        self.d_.rows_.clear()

        self.initData()
        return True

    def setFLReportData(self, n) -> bool:
        self.d_.setQuery(0)
        tmp_doc = QtXml.QDomDocument("KugarData")
        tmp_doc.appendChild(n)
        self.rd = tmp_doc
        return True
        # return super(FLReportEngine, self).setReportData(n)

    def setFLReportTemplate(self, t) -> bool:
        # buscamos el .kut o el .rlab

        self.d_.template_ = t

        if not self.d_.qry_:
            from pineboolib.application import project

            if project.conn is None:
                raise Exception("Project is not connected yet")
            mgr = project.conn.managerModules()

        else:
            mgr = self.d_.qry_.db().managerModules()

        self.rt = mgr.contentCached("%s.kut" % t)

        if not self.rt:
            self.logger.error("FLReportEngine::No se ha podido cargar %s.kut", t)
            return False

        return True

    def rptQueryData(self) -> Optional[PNSqlQuery]:
        return self.d_.qry_

    def rptNameTemplate(self) -> str:
        return self.d_.template_

    @decorators.BetaImplementation
    def setReportTemplate(self, t):
        if isinstance(t, FLDomNodeInterface):
            return self.setFLReportData(t.obj())

        return self.setFLReportData(t)

    def reportData(self) -> Any:
        return self.rd if self.rd else QtXml.QDomDocument()

    def reportTemplate(self) -> Any:
        return self.rt if self.rt else QtXml.QDomDocument()

    @decorators.NotImplementedWarn
    def csvData(self) -> str:
        # FIXME: Should return the report converted to CSV
        return ""

    @decorators.NotImplementedWarn
    def exportToOds(self, pages):
        if not pages or not pages.pageCollection():
            return
        # FIXME: exportToOds not defined in superclass
        # super(FLReportEngine, self).exportToOds(pages.pageCollection())

    def renderReport(self, init_row=0, init_col=0, flags=False, pages=None) -> bool:
        if self.rd and self.rt and self.rt.find("KugarTemplate") > -1:
            data = self.rd.toString(1)
            self.report_ = self.parser_.parse(
                self.d_.template_, self.rt, data, self.report_, flags
            )

            return True if self.report_ else False

        return False

        # # print(self.rd.toString(1))
        # """
        # fr = MReportEngine.RenderReportFlags.FillRecords.value
        #
        # pgs = FLReportPages()
        # if pages:
        #     pgs.setPageCollection(pages)
        #
        # pgc = super(FLReportEngine, self).renderReport(
        #     initRow,
        #     initCol,
        #     pgs,
        #     fr if fRec else 0
        # )
        #
        # pgs.setPageCollection(pgc)
        # if not fRec or not self.d_.qry_ or not self.d_.qFieldMtdList_ or not self.d_.qDoubleFieldList_:
        #     return pgs
        #
        # nl = QtXml.QDomNodeList(self.rd.elementsByTagName("Row"))
        # for i in range(nl.count()):
        #     itm = nl.item(i)
        #     if itm.isNull():
        #         continue
        #     nm = itm.attributes()
        #
        #     for it in self.d_.qDoubleFieldList_:
        #         ita = nm.namedItem(it)
        #         if ita.isNull():
        #             continue
        #         sVal = ita.nodeValue()
        #         if not sVal or sVal == "" or sVal.upper() == "NAN":
        #             continue
        #         dVal = float(sVal)
        #         if not dVal:
        #             dVal = 0
        #         decimals = self.d_.qFieldMtdList_.find(
        #             it.section('.', 1, 1).lower()).partDecimal()
        #         ita.setNodeValue(FLUtil.formatoMiles(round(dVal, decimals)))
        # return pgs
        # """

    def initData(self) -> None:
        if not self.rd:
            raise Exception(
                "RD is missing. Initialize properly before calling initData"
            )
        n = self.rd.firstChild()
        while not n.isNull():
            if n.nodeName() == "KugarData":
                self.records_ = n.childNodes()
                attr = n.attributes()
                tempattr = attr.namedItem("Template")
                tempname = tempattr.nodeValue() or None
                if tempname is not None:
                    # FIXME: We need to add a signal:
                    # self.preferedTemplate.emit(tempname)
                    break
            n = n.nextSibling()

    def number_pages(self) -> Any:
        return self.parser_.number_pages() if self.parser_ else 0
