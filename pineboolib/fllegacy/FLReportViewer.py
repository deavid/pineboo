from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtXml
from PyQt5.QtCore import Qt

from pineboolib import decorators
from pineboolib import qt3ui
from pineboolib.utils import filedir
import pineboolib

from pineboolib.kugar.mreportviewer import MReportViewer

from pineboolib.fllegacy.FLUtil import FLUtil
from pineboolib.fllegacy.FLPicture import FLPicture
from pineboolib.fllegacy.FLSqlQuery import FLSqlQuery
from pineboolib.fllegacy.FLSqlCursor import FLSqlCursor
from pineboolib.fllegacy.FLStylePainter import FLStylePainter
from pineboolib.fllegacy.FLSmtpClient import FLSmtpClient
from pineboolib.fllegacy.FLReportEngine import FLReportEngine
AQ_USRHOME = "."  # FIXME


class FLReportViewer(QtWidgets.QMainWindow):

    def __init__(self, parent=None, name=0, embedInParent=False, rptEngine=0):
        pParam = 0 if parent and embedInParent else 0
        pParam = pParam | Qt.WindowMaximizeButtonHint | Qt.WindowTitleHint
        pParam = pParam | 0 | Qt.Dialog | Qt.WindowModal
        pParam = pParam | Qt.WindowSystemMenuHint

        super(FLReportViewer, self).__init__(parent, pParam)

        self.loop_ = False
        self.eventloop = QtCore.QEventLoop()
        self.reportPrinted_ = False
        self.rptViewer_ = 0
        self.rptEngine_ = 0
        self.report_ = 0
        self.qry_ = 0
        self.slotsPrintDisabled_ = False
        self.slotsExportedDisabled_ = False
        self.printing_ = False
        self.embedInParent_ = True if parent and embedInParent else False
        self.ui_ = {}

        qt3ui.loadUi(filedir('forms/FLWidgetReportViewer.ui'), self)

        if not name:
            self.setName("FLReportViewer")

        if self.embedInParent_:
            self.autoClose_ = False
            self.ui_["menubar"].hide()
            self.ui_["chkAutoClose"].hide()
            self.ui_["spnResolution"].hide()
            self.ui_["spnPixel"].hide()
            self.ui_["salir"].setVisible(False)

            if not parent.layout():
                lay = QtCore.QVBoxLayout(parent)
                lay.addWidget(self)
            else:
                parent.layout().add(self)
        else:
            self.autoClose_ = bool(FLUtil().readSettingEntry(
                "rptViewer/autoClose", "false"))
            self.ui_["chkAutoClose"].setChecked(self.autoClose_)

        self.rptViewer_ = MReportViewer(self)
        self.setReportEngine(FLReportEngine(
            self) if rptEngine == 0 else rptEngine)

        self.setFont(QtWidgets.QApplication.font())
        self.setFocusPolicy(Qt.StrongFocus)

        util = FLUtil()

        self.ui_["lePara"].setText(str(util.readSettingEntry("email/to")))
        self.ui_["leDe"].setText(str(util.readSettingEntry("email/from")))
        self.ui_["leMailServer"].setText(
            str(util.readSettingEntry("email/mailserver")))

        wrv = self.ui_["FLWidgetReportViewer"]
        self.initCentralWidget_ = wrv.centralWidget()

        self.smtpClient_ = FLSmtpClient(self)
        self.smtpClient_.status.connect(self.ui_["lblEstado"].setText)

        wrv.setCentralWidget(self.rptViewer_)
        self.ui_["frEMail"].hide()
        if self.initCentralWidget_:
            self.initCentralWidget_.hide()
        if not self.embedInParent_:
            self.ui_["spnResolution"].setValue(int(util.readSettingEntry(
                "rptViewer/dpi", str(self.rptViewer_.resolution()))))
            self.ui_["spnPixel"].setValue(float(util.readSettingEntry(
                "rptViewer/pixel", float(self.rptEngine_.relDpi()))) * 10.)

        self.report_ = self.rptViewer_.reportPages()

    @decorators.BetaImplementation
    def rptViewer(self):
        return self.rptViewer_

    @decorators.BetaImplementation
    def rptEngine(self):
        return self.rptEngine_

    @decorators.BetaImplementation
    def setReportEngine(self, r=0):
        if self.rptEngine_ == r:
            return

        sender = self.sender()
        noSigDestroy = not (sender and sender == self.rptEngine_)

        if self.rptEngine_:
            self.rptEngine_.destroyed.disconnect(self.setReportEngine)
            if noSigDestroy and self.rptEngine_.parent() == self:
                self.rptEngine_.deleteLater()
                self.rptEngine_ = 0

        self.rptEngine_ = r
        if self.rptEngine_:
            self.template_ = self.rptEngine_.rptNameTemplate()
            self.qry_ = self.rptEngine_.rptQueryData()
            if self.rptEngine_.rptXmlTemplate():
                self.xmlTemplate_ = self.rptEngine_.rptXmlTemplate()
            if self.rptEngine_.rptXmlTemplate():
                self.xmlData_ = self.rptEngine_.rptXmlTemplate()
            self.rptEngine_.destroyed.connect(self.setReportEngine)

            self.ui_["ledStyle"].setDisabled(False)
            self.ui_["save_page_SVG"].setDisabled(False)
            self.ui_["save_page_tpl_SVG"].setDisabled(False)
            self.ui_["load_tpl_SVG"].setDisabled(False)
        else:
            self.ui_["ledStyle"].setDisabled(True)
            self.ui_["save_page_SVG"].setDisabled(True)
            self.ui_["save_page_tpl_SVG"].setDisabled(True)
            self.ui_["load_tpl_SVG"].setDisabled(True)

        if noSigDestroy:
            self.rptViewer_.setReportEngine(self.rptEngine_)

    @decorators.BetaImplementation
    def exec_(self):
        if self.loop_:
            print("FLReportViewer::exec(): Se ha detectado una llamada recursiva")
            return

        self.show()
        self.eventloop.exec_()

        if self.embedInParent_:
            return

        self.loop_ = True
        # self.clearWFlags(Qt.WShowModal) # FIXME

    @decorators.BetaImplementation
    def csvData(self):
        return self.rptEngine_.csvData() if self.rptEngine_ else ""

    @decorators.BetaImplementation
    def closeEvent(self, e):
        if self.printing_:
            return

        self.show()
        self.frameGeometry()
        self.hide()

        if not self.embedInParent_:
            geo = QtCore.QRect(self.x(), self.y(), self.width(), self.height())
            pineboolib.project.saveGeometryForm(self.name(), geo)

        if self.loop_ and not self.embedInParent_:
            self.loop_ = False

        self.eventloop.exit()

        super(FLReportViewer, self).closeEvent(e)
        self.deleteLater()

    @decorators.BetaImplementation
    def showEvent(self, e):
        super(FLReportViewer, self).showEvent(e)

        if not self.embedInParent_:
            geo = QtCore.QRect(self.geometry())
            if geo and geo.isValid():
                desk = QtWidgets.QApplication.desktop().availableGeometry(self)
                inter = desk.intersected(geo)
                self.resize(geo.size())
                geodim = geo.width() * geo.height()
                if inter.width() * inter.height() > (geodim / 20):
                    self.move(geo.topLeft())

    @decorators.BetaImplementation
    def renderReport(self, initRow=0, initCol=0, append=False, dRpt=None):
        flags = None
        if dRpt is None:
            flags = append
        else:
            ap = MReportViewer.RenderReportFlags.Append.value
            dp = MReportViewer.RenderReportFlags.Display.value
            flags = ap if append else 0 | int(dp if dRpt else 0)

        if not self.rptEngine_:
            return False

        ret = self.rptViewer_.renderReport(initRow, initCol, flags)
        self.report_ = self.rptViewer_.reportPages()
        return ret

    @decorators.BetaImplementation
    def slotFirstPage(self):
        self.rptViewer_.slotFirstPage()

    @decorators.BetaImplementation
    def slotLastPage(self):
        self.rptViewer_.slotLastPage()

    @decorators.BetaImplementation
    def slotNextPage(self):
        self.rptViewer_.slotNextPage()

    @decorators.BetaImplementation
    def slotPrevPage(self):
        self.rptViewer_.slotPrevPage()

    @decorators.BetaImplementation
    def slotZoomUp(self):
        self.rptViewer_.slotZoomUp()

    @decorators.BetaImplementation
    def slotZoomDown(self):
        self.rptViewer_.slotZoomDown()

    @decorators.BetaImplementation
    def exportFileCSVData(self):
        if self.slotsExportedDisabled_:
            return

        fileName = QtCore.QFileDialog.getSaveFileName(
            "",
            FLUtil.translate(self, "app", "Fichero CSV (*.csv *.txt)"),
            self,
            FLUtil.translate(self, "app", "Exportar a CSV"),
            FLUtil.translate(self, "app", "Exportar a CSV")
        )

        if not fileName or fileName == "":
            return

        if not fileName.upper().contains(".CSV"):
            fileName = fileName + ".csv"

        q = QtCore.QMessageBox.question(
            self,
            FLUtil.translate(self, "app", "Sobreescribir {}").format(fileName),
            FLUtil.translate(
                self,
                "app",
                "Ya existe un fichero llamado {}. ¿Desea sobreescribirlo?"
            ).format(fileName),
            FLUtil.translate(self, "app", "&Sí"),
            FLUtil.translate(self, "app", "&No"),
            "",
            0,
            1
        )

        if QtCore.QFile.exists(fileName) and q:
            return

        file = QtCore.QFile(fileName)

        if file.open(Qt.IO_WriteOnly):
            stream = QtCore.QTextStream(file)
            stream << self.csvData() << "\n"
            file.close()
        else:
            QtCore.QMessageBox.critical(
                self,
                FLUtil.translate(self, "app", "Error abriendo fichero"),
                FLUtil.translate(
                    self,
                    "app",
                    "No se pudo abrir el fichero {} para escribir: {}"
                ).format(
                    fileName,
                    QtWidgets.QApplication.translate(
                        "QFile", file.errorString()
                    )
                )
            )

    @decorators.BetaImplementation
    @QtCore.pyqtSlot()
    def exportToPDF(self):
        if self.slotsExportedDisabled_:
            return

        fileName = QtCore.QFileDialog.getSaveFileName(
            "",
            FLUtil.translate(self, "app", "Fichero PDF (*.pdf)"),
            self,
            FLUtil.translate(self, "app", "Exportar a PDF"),
            FLUtil.translate(self, "app", "Exportar a PDF")
        )

        if not fileName or fileName == "":
            return

        if not fileName.upper().contains(".PDF"):
            fileName = fileName + ".pdf"

        q = QtCore.QMessageBox.question(
            self,
            FLUtil.translate(self, "app", "Sobreescribir {}").format(fileName),
            FLUtil.translate(
                self,
                "app",
                "Ya existe un fichero llamado {}. ¿Desea sobreescribirlo?"
            ).format(fileName),
            FLUtil.translate(self, "app", "&Sí"),
            FLUtil.translate(self, "app", "&No"),
            "",
            0,
            1
        )

        if QtCore.QFile.exists(fileName) and q:
            return

        self.slotPrintReportToPDF(fileName)

    @decorators.BetaImplementation
    @QtCore.pyqtSlot()
    def sendEMailPDF(self):
        t = self.ui_.leDocumento.text()
        name = "informe.pdf" if not t or t == "" else t
        fileName = QtCore.QFileDialog.getSaveFileName(
            AQ_USRHOME + "/" + name + ".pdf",
            FLUtil.translate(self, "app", "Fichero PDF a enviar (*.pdf)"),
            self,
            FLUtil.translate(self, "app", "Exportar a PDF para enviar"),
            FLUtil.translate(self, "app", "Exportar a PDF para enviar")
        )

        if not fileName or fileName == "":
            return

        if not fileName.upper().contains(".PDF"):
            fileName = fileName + ".pdf"

        q = QtCore.QMessageBox.question(
            self,
            FLUtil.translate(self, "app", "Sobreescribir {}").format(fileName),
            FLUtil.translate(
                self,
                "app",
                "Ya existe un fichero llamado {}. ¿Desea sobreescribirlo?"
            ).format(fileName),
            FLUtil.translate(self, "app", "&Sí"),
            FLUtil.translate(self, "app", "&No"),
            "",
            0,
            1
        )

        if QtCore.QFile.exists(fileName) and q:
            return

        autoCloseSave = self.autoClose_
        self.slotPrintReportToPDF(fileName)
        self.autoClose_ = autoCloseSave

        FLUtil.writeSettingEntry("email/to", self.ui_.lePara.text())
        FLUtil.writeSettingEntry("email/from", self.ui_.leDe.text())
        FLUtil.writeSettingEntry(
            "email/mailserver", self.ui_.leMailServer.text()
        )

        fi = QtCore.QFileInfo(fileName)
        name = fi.fileName()

        self.smtpClient_.setMailServer(self.ui_.leMailServer.text())
        self.smtpClient_.setTo(self.ui_.lePara.text())
        self.smtpClient_.setFrom(self.ui_.leDe.text())
        asutxt = self.ui_.leAsunto.text()
        self.smtpClient_.setSubject(name if asutxt == "" else asutxt)
        self.smtpClient_.setBody(self.ui_.leCuerpo.text() + "\n\n")

        html = "<html><body><a href=\"http://abanq.org/\">"
        html += "<img src=\"cid:logo.png@3d8b627b6292\"/>"
        html += "</a><br/><br/></body></html>"
        self.smtpClient_.addTextPart(html, "text/html")
        self.smtpClient_.addAttachment(fileName)
        self.smtpClient_.startSend()

    @decorators.BetaImplementation
    def showInitCentralWidget(self, show):
        wrv = self.ui_["FLWidgetReportViewer"]
        if show:
            self.rptViewer_.hide()
            wrv.setCentralWidget(self.initCentralWidget_)
            self.ui_.leDocumento.setText(
                "doc-" + str(
                    QtCore.QDateTime.currentDateTime()
                ).replace(":", ",").replace(" ", "")
            )
            self.ui_.frEMail.show()
            self.initCentralWidget_.show()
        else:
            self.initCentralWidget_.hide()
            self.ui_.frEMail.hide()
            wrv.setCentralWidget(self.rptViewer_)
            self.rptViewer_.show()

    @decorators.BetaImplementation
    def saveSVGStyle(self):
        if self.report_:
            fileName = QtCore.QFileDialog.getSaveFileName(
                "",
                FLUtil.translate(self, "app", "Fichero SVG (*.svg)"),
                self,
                FLUtil.translate(self, "app", "Guardar en SVG"),
                FLUtil.translate(self, "app", "Guardar en SVG")
            )

            if not fileName or fileName == "":
                return

            if not fileName.upper().contains(".SVG"):
                fileName = fileName + ".svg"

            q = QtCore.QMessageBox.question(
                self,
                FLUtil.translate(
                    self, "app", "Sobreescribir {}").format(fileName),
                FLUtil.translate(
                    self,
                    "app",
                    "Ya existe un fichero llamado {}. ¿Desea sobreescribirlo?"
                ).format(fileName),
                FLUtil.translate(self, "app", "&Sí"),
                FLUtil.translate(self, "app", "&No"),
                "",
                0,
                1
            )

            if QtCore.QFile.exists(fileName) and q:
                return

            FLStylePainter.setSVGMode(True)
            self.updateReport()
            FLStylePainter.setSVGMode(False)

            fileNames = []

            for i in range(self.report_.pageCount()):
                fname = fileName + str(i)
                fileNames.append(fname)
                page = self.report_.getPageAt(i)
                psize = self.report_.pageDimensions()
                page.setBoundingRect(QtCore.QRect(QtCore.QPoint(0, 0), psize))
                page.save(fname, "svg")

            FLStylePainter.normalizeSVGFile(fileName, fileNames)

            self.updateReport()

    @decorators.BetaImplementation
    def saveSimpleSVGStyle(self):
        backStyleName = self.styleName_
        self.styleName_ = "_simple"
        self.saveSVGStyle()
        self.styleName_ = backStyleName
        self.updateReport()

    @decorators.BetaImplementation
    def loadSVGStyle(self):
        fileName = QtCore.QFileDialog.getOpenFileName(
            "",
            FLUtil.translate(self, "app", "Fichero SVG (*.svg)"),
            self,
            FLUtil.translate(self, "app", "Cargar estilo SVG"),
            FLUtil.translate(self, "app", "Cargar estilo SVG")
        )

        if not fileName or fileName == "":
            return

        self.ui_.ledStyle.setText("file:" + fileName)
        self.updateReport()

    @decorators.BetaImplementation
    def slotExit(self):
        self.close()

    @decorators.BetaImplementation
    def slotPrintReportToPs(self, outPsFile):
        if self.slotsPrintDisabled_:
            return

        self.setDisabled(True)
        self.printing_ = True
        self.reportPrinted_ = self.rptViewer_.printReportToPs(outPsFile)
        if self.reportPrinted_ and self.autoClose_:
            QtCore.QTimer.singleShot(0, self.slotExit)
        self.printing_ = False
        self.setDisabled(False)

    @decorators.BetaImplementation
    def slotPrintReportToPdf(self, outPdfFile):
        if self.slotsPrintDisabled_:
            return

        self.setDisabled(True)
        self.printing_ = True
        self.reportPrinted_ = self.rptViewer_.printReportToPdf(outPdfFile)
        if self.reportPrinted_ and self.autoClose_:
            QtCore.QTimer.singleShot(0, self.slotExit)
        self.printing_ = False
        self.setDisabled(False)

    @decorators.BetaImplementation
    def slotPrintReport(self):
        if self.slotsPrintDisabled_:
            return

        self.setDisabled(True)
        self.printing_ = True
        self.reportPrinted_ = self.rptViewer_.printReport()
        if self.reportPrinted_ and self.autoClose_:
            QtCore.QTimer.singleShot(0, self.slotExit)
        self.printing_ = False
        self.setDisabled(False)

    @decorators.BetaImplementation
    def setReportData(self, d):
        if isinstance(d, FLSqlQuery):
            self.qry_ = d
            if self.rptEngine_ and self.rptEngine_.setReportData(d):
                self.xmlData_ = self.rptEngine_.rptXmlData()
                return True
            return False
        elif isinstance(d, FLSqlCursor):
            if not self.rptEngine_:
                return False
            return self.rptEngine_.setReportData(d)
        elif isinstance(d, QtXml.QDomNode):
            self.xmlData_ = d
            self.qry_ = 0
            if not self.rptEngine_:
                return False
            return self.rptEngine_.setReportData(d)
        return False

    @decorators.BetaImplementation
    def setReportTemplate(self, t, style=""):
        if isinstance(t, QtXml.QDomNode):
            self.xmlTemplate_ = t
            self.template_ = ""
            self.styleName_ = style
            if not self.rptEngine_:
                return False

            self.rptEngine_.setFLReportTemplate(t)
            self.rptEngine_.setStyleName(style)
            return True
        else:
            self.template_ = t
            self.styleName_ = style
            if self.rptEngine_ and self.rptEngine_.setFLReportTemplate(t):
                self.rptEngine_.setStyleName(style)
                self.xmlTemplate_ = self.rptEngine_.rptXmlTemplate()
                return True
            return False
        return False

    @decorators.BetaImplementation
    def sizeHint(self):
        return self.rptViewer_.sizeHint()

    @decorators.BetaImplementation
    def setNumCopies(self, numCopies):
        self.rptViewer_.setNumCopies(numCopies)

    @decorators.BetaImplementation
    def setPrintToPos(self, ptp):
        self.rptViewer_.setPrintToPos(ptp)

    @decorators.BetaImplementation
    def setPrinterName(self, pName):
        self.rptViewer_.setPrinterName(pName)

    @decorators.BetaImplementation
    def reportPrinted(self):
        return self.reportPrinted_

    @decorators.BetaImplementation
    def setAutoClose(self, b):
        if self.embedInParent_:
            self.autoClose_ = False
        else:
            self.autoClose_ = b

    @QtCore.pyqtSlot(int)
    @decorators.BetaImplementation
    def setResolution(self, dpi):
        FLUtil.writeSettingEntry("rptViewer/dpi", str(dpi))
        self.rptViewer_.setResolution(dpi)

    @QtCore.pyqtSlot(int)
    @decorators.BetaImplementation
    def setPixel(self, relDpi):
        FLUtil.writeSettingEntry("rptViewer/pixel", str(float(relDpi / 10.)))
        if self.rptEngine_:
            self.rptEngine_.setRelDpi(relDpi / 10.)

    @decorators.BetaImplementation
    def setDefaults(self):
        self.spnResolution_.setValue(300)

        if True:
            # Linux
            self.spnPixel_.setValue(780)
        elif False:
            # WIN32 #FIXME
            pass
        else:
            # MAC #FIXME
            pass

    @decorators.BetaImplementation
    def updateReport(self):
        self.requestUpdateReport.emit()

        if self.qry_ or (self.xmlData_ and self.xmlData_ != ""):
            if not self.rptEngine_:
                self.setReportEngine(FLReportEngine(self))

            self.setResolution(self.spnResolution_.value())
            self.setPixel(self.spnPixel_.value())

            if self.template_ and self.template_ != "":
                self.setReportTemplate(self.template_, self.styleName_)
            else:
                self.setReportTemplate(self.xmlTemplate_, self.styleName_)

            if self.qry_:
                self.setReportData(self.qry_)
            else:
                self.setReportData(self.xmlData_)

            self.renderReport(0, 0, False, False)

        self.updateDisplay()

    @decorators.BetaImplementation
    def getCurrentPage(self):
        if self.report_:
            return FLPicture(self.report_.getCurrentPage(), self)
        return 0

    @decorators.BetaImplementation
    def getFirstPage(self):
        if self.report_:
            return FLPicture(self.report_.getFirstPage(), self)
        return 0

    @decorators.BetaImplementation
    def getPreviousPage(self):
        if self.report_:
            return FLPicture(self.report_.getPreviousPage(), self)
        return 0

    @decorators.BetaImplementation
    def getNextPage(self):
        if self.report_:
            return FLPicture(self.report_.getNextPage(), self)
        return 0

    @decorators.BetaImplementation
    def getLastPage(self):
        if self.report_:
            return FLPicture(self.report_.getLastPage(), self)
        return 0

    @decorators.BetaImplementation
    def getPageAt(self, i):
        if self.report_:
            return FLPicture(self.report_.getPageAt(i), self)
        return 0

    @decorators.BetaImplementation
    def updateDisplay(self):
        self.rptViewer_.slotUpdateDisplay()

    @decorators.BetaImplementation
    def clearPages(self):
        if self.report_:
            self.report_.clear()

    @decorators.BetaImplementation
    def appendPage(self):
        if self.report_:
            self.report_.appendPage()

    @decorators.BetaImplementation
    def getCurrentIndex(self):
        if self.report_:
            return self.report_.getCurrentIndex()
        return -1

    @decorators.BetaImplementation
    def setCurrentPage(self, idx):
        if self.report_:
            self.report_.setCurrentPage(idx)

    @decorators.BetaImplementation
    def setPageSize(self, s):
        if self.report_:
            self.report_.setPageSize(s)

    @decorators.BetaImplementation
    def setPageOrientation(self, o):
        if self.report_:
            self.report_.setPageOrientation(o)

    @decorators.BetaImplementation
    def setPageDimensions(self, dim):
        if self.report_:
            self.report_.setPageDimensions(dim)

    @decorators.BetaImplementation
    def pageSize(self):
        if self.report_:
            return self.report_.pageSize()
        return -1

    @decorators.BetaImplementation
    def pageOrientation(self):
        if self.report_:
            return self.report_.pageOrientation()
        return -1

    @decorators.BetaImplementation
    def pageDimensions(self):
        if self.report_:
            return self.report_.pageDimensions()
        return QtCore.QSize()

    @decorators.BetaImplementation
    def pageCount(self):
        if self.report_:
            return self.report_.pageCount()
        return -1

    @decorators.BetaImplementation
    def setStyleName(self, style):
        self.styleName_ = style

    @decorators.BetaImplementation
    def rptViewerEmbedInParent(self, parentFrame):
        if not parentFrame:
            return

        self.ui_["FLWidgetReportViewer"].setCentralWidget(0)
        self.rptViewer_.reparent(parentFrame, 0, QtCore.QPoint(0, 0))

        if not parentFrame.layout():
            lay = QtCore.QVBoxLayout(parentFrame)
            lay.addWidget(self.rptViewer_)
        else:
            parentFrame.layout().add(self.rptViewer_)

        self.rptViewer_.show()

    @decorators.BetaImplementation
    def rptViewerReparent(self, parentFrame):
        if not parentFrame:
            return

        actExit = QtCore.QAction(self.child("salir", "QAction"))
        if actExit:
            actExit.setVisible(False)

        self.reparent(parentFrame, 0, QtCore.QPoint(0, 0))

        if not parentFrame.layout():
            lay = QtCore.QVBoxLayout(parentFrame)
            lay.addWidget(self)
        else:
            parentFrame.layout().add(self)

        self.show()

    @decorators.BetaImplementation
    def setReportPages(self, pgs):
        self.setReportEngine(0)
        self.qry_ = 0
        self.xmlData_ = QtXml.QDomNode()
        self.rptViewer_.setReportPages(pgs.pageCollection() if pgs else 0)
        self.report_ = self.rptViewer_.reportPages()

    @decorators.BetaImplementation
    def setColorMode(self, c):
        self.rptViewer_.setColorMode(c)

    @decorators.BetaImplementation
    def colorMode(self):
        return self.rptViewer_.colorMode()

    @decorators.BetaImplementation
    def disableSlotsPrintExports(self, dPrints=True, dExports=True):
        self.slotsPrintDisabled_ = dPrints
        self.slotsExportedDisabled_ = dExports

    @decorators.BetaImplementation
    def exportToOds(self):
        if self.slotsExportedDisabled_:
            return

        self.rptViewer_.exportToOds()

    @decorators.BetaImplementation
    def setName(self, n):
        self.name_ = n

    @decorators.BetaImplementation
    def name(self):
        return self.name_
