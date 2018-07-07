from enum import Enum

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtPrintSupport
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLayout, QApplication

from pineboolib import decorators

from pineboolib.fllegacy.kugar.mpagecollection import MPageCollection
from pineboolib.fllegacy.kugar.mpagedisplay import MPageDisplay

from pineboolib.fllegacy.FLUtil import FLUtil
from pineboolib.fllegacy.FLPosPrinter import FLPosPrinter
from pineboolib.fllegacy.FLDiskCache import FLDiskCache
from pineboolib.fllegacy.FLReportPages import FLReportPages


class MReportViewer(QWidget):

    M_PROGRESS_DELAY = 1000

    preferedTemplate = QtCore.pyqtSignal()

    class RenderReportFlags(Enum):
        Append = 0
        Display = 1
        PageBreak = 2
        FillRecords = 3

    class PrinterColorMode(Enum):
        PrintGrayScale = 0
        PrintColor = 1

    @decorators.BetaImplementation
    def __init__(self, parent=0, name=0):
        super(MReportViewer, self).__init__(parent)

        self.progress_ = 0
        self.totalSteps_ = 0
        self.printer_ = 0
        self.posprinter_ = 0
        self.numCopies_ = 1
        self.printToPos_ = False
        self.printerName_ = ""
        self.dpi_ = 300
        self.colorMode_ = QtPrintSupport.QPrinter.Color

        self.psprinter_ = 0
        self.scroller_ = QtWidgets.QScrollArea(self)
        self.rptEngine_ = 0
        self.report_ = FLReportPages()
        self.p_ = QtWidgets.QApplication.palette()
        self.g_ = self.p_.Active
        pal = self.scroller_.viewport().palette()
        pal.setBrush(QtGui.QPalette.Background, self.p_.mid())
        self.scroller_.viewport().setPalette(pal)
        self.display_ = MPageDisplay(self.scroller_.viewport())
        pal = self.display_.palette()
        pal.setColor(QtGui.QPalette.Background, Qt.white)
        self.display_.setPalette(pal)
        self.scroller_.setWidget(self.display_)
        self.display_.hide()

    @decorators.BetaImplementation
    def resolution(self):
        return self.dpi_

    @decorators.BetaImplementation
    def reportPages(self):
        return self.report_

    @decorators.BetaImplementation
    def colorMode(self):
        return self.colorMode_

    @decorators.BetaImplementation
    def setNumCopies(self, numCopies):
        self.numCopies_ = numCopies

    @decorators.BetaImplementation
    def setPrintToPos(self, printToPos):
        self.printToPos_ = printToPos

    @decorators.BetaImplementation
    def setPrinterName(self, printerName):
        self.printerName_ = printerName

    @decorators.BetaImplementation
    def setResolution(self, dpi):
        self.dpi_ = dpi

    @decorators.BetaImplementation
    def setColorMode(self, colorMode):
        self.colorMode_ = colorMode

    @decorators.BetaImplementation
    def paintEvent(self, event):
        del event

    @decorators.BetaImplementation
    def resizeEvent(self, event):
        self.scroller_.resize(event.size())

    @decorators.BetaImplementation
    def setReportData(self, data):
        if not self.rptEngine_:
            return False
        return self.rptEngine_.setReportData(data)

    @decorators.BetaImplementation
    def setReportTemplate(self, tpl):
        if not self.rptEngine_:
            return False
        return self.rptEngine_.setReportTemplate(tpl)

    @decorators.BetaImplementation
    def renderReport(self, initRow=0, initCol=0, append=False, dispRpt=None):
        ap = MReportViewer.RenderReportFlags.Append.value
        dp = MReportViewer.RenderReportFlags.Display.value
        flags = None
        if dispRpt is None:
            flags = append
        else:
            flags = ap if append else 0
            flags = flags | int(dp if dispRpt else 0)

        append = flags & ap
        dispRpt = flags & dp

        if not self.rptEngine_:
            return False

        if not append and self.report_ and self.report_.parent() == self:
            self.report_.deleteLater()
            self.report_ = 0

        if self.progress_:
            self.progress_.deleteLater()
            self.progress_ = 0

        self.report_ = self.rptEngine_.renderReport(
            initRow, initCol, flags, self.report_)

        self.insertChild(self.report_)

        if dispRpt:
            self.printToPos_ = self.report_.printToPos()

        if self.progress_:
            self.progress_.deleteLater()
            self.progress_ = 0

        fp = self.report_.getFirstPage()
        if dispRpt and self.report_ and fp:
            self.display_.setPageDimensions(self.report_.pageDimensions())
            self.display_.setPage(fp)
            self.display_.show()
            return True

        return False

    @decorators.BetaImplementation
    def slotUpdateDisplay(self):
        if self.report_ != 0:
            self.display_.setPageDimensions(self.report_.pageDimensions())
            if self.report_.getCurrentPage() != 0:
                self.display_.setPage(self.report_.getCurrentPage())
            self.display_.show()
        self.display_.repaint()

    @decorators.BetaImplementation
    def clearReport(self):
        if self.display_:
            self.display_.hide()

        if self.report_ and self.report_.parent() == self:
            self.report_.deleteLater()
            self.report_ = 0

    @decorators.BetaImplementation
    def printGhostReport(self):
        if False:
            # WIN32 #FIXME
            pass
        else:
            # LINUX/MAC OK
            pass

    @decorators.BetaImplementation
    def printGhostReportToPS(self):
        if False:
            # WIN32/MAC #FIXME
            pass
        else:
            # LINUX OK
            pass

    @decorators.BetaImplementation
    def printPosReport(self):
        if self.report_ == 0:
            return False

        self.posprinter_ = FLPosPrinter()
        self.posprinter_.setPaperWidth(self.report_.pageSize())
        self.posprinter_.setPrinterName(self.printerName_)

        painter = QtGui.QPainter()
        viewIdx = self.report_.getCurrentIndex()

        painter.begin(self.posprinter_)
        pdm = self.posprinter_.device()
        dim = self.report_.pageDimensions()
        painter.setWindow(0, 0, dim.width(), dim.height())
        painter.setViewport(0, 0, pdm.width(), pdm.height())

        for j in range(self.numCopies_):
            self.report_.setCurrentPage(1)
            page = self.report_.getCurrentPage()
            page.play(painter)

        painter.end()
        self.report_.setCurrentPage(viewIdx)

        del self.posprinter_

        return True

    @decorators.BetaImplementation
    def printReportToPdf(self, outPdfFile):
        if self.report_ == 0:
            return False

        gs = QtWidgets.QApplication.gsExecutable()
        gsOk = False
        procTemp = QtCore.QProcess()
        procTemp.addArgument(gs)
        procTemp.addArgument("--version")
        gsOk = procTemp.start()
        del procTemp

        if not gsOk:
            m = QtCore.QMessageBox(
                FLUtil.translate(self, "app", "Falta Ghostscript"),
                FLUtil.translate(
                    self, "app",
                    "Para poder exportar a PDF debe instalar Ghostscript"
                    "(http://www.ghostscript.com) y añadir\n"
                    "el directorio de instalación a la ruta de"
                    "búsqueda de programas\ndel sistema (PATH).\n\n"),
                Qt.QMessageBox.Critical,
                Qt.QMessageBox.Ok,
                Qt.QMessageBox.NoButton,
                Qt.QMessageBox.NoButton,
                self,
                0,
                False
            )
            m.show()
            return False

        outPsFile = FLDiskCache.AQ_DISKCACHE_DIRPATH + "/outprintpdf.ps"
        outPsPdfFile = FLDiskCache.AQ_DISKCACHE_DIRPATH + "/outprintps.pdf"

        QtCore.QFile.remove(outPsFile)
        QtCore.QFile.remove(outPsPdfFile)

        if not self.printReportToPs(outPsFile):
            return False

        proc = QtCore.QProcess()
        proc.addArgument(gs)
        proc.addArgument("-q")
        proc.addArgument("-dBATCH")
        proc.addArgument("-dNOPAUSE")
        proc.addArgument("-dSAFER")
        proc.addArgument("-dCompatibilityLevel=1.4")
        proc.addArgument("-dPDFSETTINGS=/printer")
        proc.addArgument("-dAutoFilterColorImages=false")
        proc.addArgument("-sColorImageFilter=FlateEncode")
        proc.addArgument("-dAutoFilterGrayImages=false")
        proc.addArgument("-sGrayImageFilter=FlateEncode")
        proc.addArgument("-r{}".format(self.dpi_))

        ps = self.report_.pageSize()
        if ps == QtPrintSupport.QPrinter.PageSize.A0:
            proc.addArgument("-sPAPERSIZE=a0")
        elif ps == QtPrintSupport.QPrinter.PageSize.A1:
            proc.addArgument("-sPAPERSIZE=a1")
        elif ps == QtPrintSupport.QPrinter.PageSize.A2:
            proc.addArgument("-sPAPERSIZE=a2")
        elif ps == QtPrintSupport.QPrinter.PageSize.A3:
            proc.addArgument("-sPAPERSIZE=a3")
        elif ps == QtPrintSupport.QPrinter.PageSize.A4:
            proc.addArgument("-sPAPERSIZE=a4")
        elif ps == QtPrintSupport.QPrinter.PageSize.A5:
            proc.addArgument("-sPAPERSIZE=a5")
        elif ps == QtPrintSupport.QPrinter.PageSize.B0:
            proc.addArgument("-sPAPERSIZE=b0")
        elif ps == QtPrintSupport.QPrinter.PageSize.B1:
            proc.addArgument("-sPAPERSIZE=b1")
        elif ps == QtPrintSupport.QPrinter.PageSize.B2:
            proc.addArgument("-sPAPERSIZE=b2")
        elif ps == QtPrintSupport.QPrinter.PageSize.B3:
            proc.addArgument("-sPAPERSIZE=b3")
        elif ps == QtPrintSupport.QPrinter.PageSize.B4:
            proc.addArgument("-sPAPERSIZE=b4")
        elif ps == QtPrintSupport.QPrinter.PageSize.B5:
            proc.addArgument("-sPAPERSIZE=b5")
        elif ps == QtPrintSupport.QPrinter.PageSize.Legal:
            proc.addArgument("-sPAPERSIZE=legal")
        elif ps == QtPrintSupport.QPrinter.PageSize.Letter:
            proc.addArgument("-sPAPERSIZE=letter")
        elif ps == QtPrintSupport.QPrinter.PageSize.Executive:
            proc.addArgument("-sPAPERSIZE=executive")
        else:
            sz = self.report_.pageDimensions()
            proc.addArgument("-dDEVICEWIDTHPOINTS={}".format(sz.width()))
            proc.addArgument("-dDEVICEHEIGHTPOINTS={}".format(sz.height()))

        proc.addArgument("-dAutoRotatePages=/PageByPage")
        proc.addArgument("-sOutputFile=" + outPsPdfFile)
        proc.addArgument("-sDEVICE=pdfwrite")
        proc.addArgument(outPsFile)

        if not proc.start():
            del proc
            return False

        while proc.isRunning():
            QtWidgets.QApplication.processEvents()

        del proc

        QtWidgets.QApplication.processEvents()

        proc = QtCore.QProcess()
        proc.addArgument(gs)
        proc.addArgument("-q")
        proc.addArgument("-dBATCH")
        proc.addArgument("-dNOPAUSE")
        proc.addArgument("-dSAFER")
        proc.addArgument("-dNODISPLAY")
        proc.addArgument("-dDELAYSAFER")
        proc.addArgument("--")
        proc.addArgument("pdfopt.ps")
        proc.addArgument(outPsPdfFile)
        proc.addArgument(outPdfFile)

        if not proc.start():
            del proc
            return False

        while proc.isRunning():
            QtWidgets.QApplication.processEvents()

        del proc

        QtWidgets.QApplication.processEvents()

        return True

    @decorators.BetaImplementation
    def printReportToPS(self, outPsFile):
        if self.report_ == 0:
            return False

        if False:
            # WIN32/MAC #FIXME
            return self.printGhostReportToPS(outPsFile)

        cnt = self.report_.pageCount()

        if cnt == 0:
            QtCore.QMessageBox.critical(
                self,
                "Kugar",
                FLUtil.translate(
                    self, "app", "No hay páginas en el\ninforme para."),
                QtCore.QMessageBox.Ok,
                QtCore.QMessageBox.NoButton,
                QtCore.QMessageBox.NoButton
            )
            return False

        self.printer_ = QtPrintSupport.QPrinter(
            QtPrintSupport.QPrinter.HighResolution
        )
        self.printer_.setPageSize(self.report_.pageSize())
        if self.printer_.pageSize() == QtPrintSupport.QPrinter.PageSize.Custom:
            self.printer_.setCustomPaperSize(self.report_.pageDimensions())
        self.printer_.setOrientation(self.report_.pageOrientation())
        self.printer_.setMinMax(1, cnt)
        self.printer_.setFromTo(1, cnt)
        self.printer_.setFullPage(True)
        self.printer_.setColorMode(self.colorMode_)
        self.printer_.setNumCopies(self.numCopies_)
        self.printer_.setOutputToFile(True)
        self.printer_.setOutputFileName(outPsFile)

        painter = QtGui.QPainter()
        printRev = False

        viewIdx = self.report_.getCurrentIndex()

        lpf = QtPrintSupport.QPrinter.PageOrder.LastPageFirst
        if self.printer_.pageOrder() == lpf:
            printRev = True

        printFrom = self.printer_.fromPage() - 1
        printTo = self.printer_.toPage()
        printCnt = (printTo - printFrom)
        printCopies = self.printer_.numCopies()
        self.totalSteps_ = printCnt * printCopies
        currentStep = 1

        self.printer_.setNumCopies(self.numCopies_)
        self.printer_.setResolution(self.dpi_)

        util = FLUtil()

        self.progress_ = util.createProgressDialog(
            FLUtil.translate(self, "app", "Imprimiendo Informe..."),
            self.totalSteps_
        )
        # self.progress_.setMinimunDuration(self.M_PROGRESS_DELAY)
        self.progress_.canceled.connect(self.slotCancelPrinting)
        util.setProgress(0)
        QtWidgets.QApplication.processEvents()

        painter.begin(self.printer_)
        pdm = self.printer_.device()
        dim = self.report_.pageDimensions()
        painter.setWindow(0, 0, dim.width(), dim.height())
        painter.setViewport(0, 0, pdm.width(), pdm.height())

        for j in range(printCopies):
            i = printFrom
            while i < printTo:
                if not self.printer_.aborted():
                    util.setProgress(currentStep)
                    QtWidgets.QApplication.processEvents()

                    if printRev:
                        self.report_.setCurrentPage(
                            i if printCnt == 1 else (printCnt - 1) - i)
                    else:
                        self.report_.setCurrentPage(i)

                    page = self.report_.getCurrentPage()
                    page.play(painter)
                    if (i - printFrom) < (printCnt - 1):
                        self.printer_.newPage()
                else:
                    j = printCopies
                    break

                i += 1
                currentStep += 1

            if j < (printCopies - 1):
                self.printer_.newPage()

        painter.end()
        self.report_.setCurrentPage(viewIdx)

        del self.printer_
        return True

    @decorators.BetaImplementation
    def printReport(self):
        if self.report_ == 0:
            return False

        self.report_.setPrintToPos(self.printToPos_)

        if self.report_.printToPos():
            return self.printToPosReport()

        if False:
            # WIN32 #FIXME
            pass

        cnt = self.report_.pageCount()

        if cnt == 0:
            QtCore.QMessageBox.critical(
                self,
                "Kugar",
                FLUtil.translate(
                    self, "app", "No hay páginas en el\ninforme para."),
                QtCore.QMessageBox.Ok,
                QtCore.QMessageBox.NoButton,
                QtCore.QMessageBox.NoButton
            )
            return False

        self.printer_ = QtPrintSupport.QPrinter(
            QtPrintSupport.QPrinter.HighResolution
        )
        self.printer_.setPageSize(self.report_.pageSize())
        if self.printer_.pageSize() == self.printer_.Custom:
            self.printer_.setCustomPaperSize(self.report_.pageDimensions())
        self.printer_.setOrientation(self.report_.pageOrientation())
        self.printer_.setPrintRange(self.printer_.AllPages)
        self.printer_.setFromTo(1, cnt)
        self.printer_.setFullPage(True)
        self.printer_.setColorMode(self.colorMode_)
        self.printer_.setCopyCount(self.numCopies_)
        if self.printerName_ and self.printerName_ != "":
            self.printer_.setPrinterName(self.printerName_)
        printProg = self.printer_.printProgram()
        if printProg and printProg != "":
            self.printer_.setPrintProgram(printProg)

        printNow = True
        if not self.printerName_ or self.printerName_ == "":
            dialog = QtPrintSupport.QPrintDialog()
            if dialog.exec_() != dialog.Accepted:
                printNow = False

            # printNow = self.printer_.setup(
                # QtWidgets.QApplication.focusWidget())

        if printNow:
            painter = QtGui.QPainter()
            printRev = False

            viewIdx = self.report_.getCurrentIndex()

            lpf = QtPrintSupport.QPrinter.LastPageFirst
            if self.printer_.pageOrder() == lpf:
                printRev = True

            printFrom = self.printer_.fromPage() - 1
            printTo = self.printer_.toPage()
            printCnt = (printTo - printFrom)
            printCopies = self.printer_.copyCount()
            self.totalSteps_ = printCnt * printCopies
            currentStep = 1

            self.printer_.setCopyCount(1)

            util = FLUtil()

            self.progress_ = util.createProgressDialog(
                util.translate("app", "Imprimiendo Informe..."),
                self.totalSteps_
            )
            # self.progress_.setMinimunDuration(self.M_PROGRESS_DELAY)
            self.progress_.canceled.connect(self.slotCancelPrinting)
            util.setProgress(0)
            QtWidgets.QApplication.processEvents()

            painter.begin(self.printer_)
            pdm = self.printer_.device()
            dim = self.report_.pageDimensions()
            painter.setWindow(0, 0, dim.width(), dim.height())
            painter.setViewport(0, 0, pdm.width(), pdm.height())

            for j in range(printCopies):
                i = printFrom
                while i < printTo:
                    if not self.printer_.aborted():
                        util.setProgress(currentStep)
                        QtWidgets.QApplication.processEvents()

                        if printRev:
                            self.report_.setCurrentPage(
                                i if printCnt == 1 else (printCnt - 1) - i)
                        else:
                            self.report_.setCurrentPage(i)

                        page = self.report_.getCurrentPage()
                        page.play(painter)
                        if (i - printFrom) < (printCnt - 1):
                            self.printer_.newPage()
                    else:
                        j = printCopies
                        break

                    i += 1
                    currentStep += 1

                if j < (printCopies - 1):
                    self.printer_.newPage()

            painter.end()
            self.report_.setCurrentPage(viewIdx)

            del self.printer_
            return True

        del self.printer_
        return False

    @decorators.BetaImplementation
    def slotFirstPage(self):
        if self.report_ == 0:
            return

        # if ((page = report->getFirstPage()) != 0) { #FIXME
        page = self.report_.getFirstPage()
        if page != 0:
            self.display_.setPage(page)
            self.display_.repaint()

    @decorators.BetaImplementation
    def slotNextPage(self):
        if self.report_ == 0:
            return

        index = self.report_.getCurrentIndex()

        # if ((page = report->getNextPage()) != 0) { #FIXME
        page = self.report_.getNextPage()
        if page != 0:
            self.display_.setPage(page)
            self.display_.repaint()
        else:
            self.report_.setCurrentPage(index)

    @decorators.BetaImplementation
    def slotPrevPage(self):
        if self.report_ == 0:
            return

        index = self.report_.getCurrentIndex()

        # if ((page = report->getPreviousPage()) != 0) { #FIXME
        page = self.report_.getPreviousPage()
        if page != 0:
            self.display_.setPage(page)
            self.display_.repaint()
        else:
            self.report_.setCurrentPage(index)

    @decorators.BetaImplementation
    def slotLastPage(self):
        if self.report_ == 0:
            return

        # if ((page = report->getLastPage()) != 0) { #FIXME
        page = self.report_.getLastPage()
        if page != 0:
            self.display_.setPage(page)
            self.display_.repaint()

    @decorators.BetaImplementation
    def slotZoomUp(self):
        if self.report_ == 0:
            return

        self.display_.zoomUp()
        self.display_.repaint()

    @decorators.BetaImplementation
    def slotZoomDown(self):
        if self.report_ == 0:
            return

        self.display_.zoomDown()
        self.display_.repaint()

    @decorators.BetaImplementation
    def slotCancelPrinting(self):
        if False:
            # WIN32/MAC #FIXME
            pass
        else:
            self.printer_.abort()

    @decorators.BetaImplementation
    def slotRenderProgress(self, p):
        util = FLUtil()
        if not self.rptEngine_:
            return

        if not self.progress_:
            self.totalSteps_ = self.rptEngine_.getRenderSteps()
            if self.totalSteps_ <= 0:
                self.totalSteps_ = 1
            self.progress_ = util.createProgressDialog(
                util.translate("app", "Creando informe..."),
                self.totalSteps_
            )
            # self.progress_.setMinimunDuration(self.M_PROGRESS_DELAY)
            self.progress_.canceled.connect(self.slotCancelPrinting)

        util.setProgress(p)
        QtWidgets.QApplication.processEvents()

    @decorators.BetaImplementation
    def sizeHint(self):
        return self.scroller_.sizeHint()

    @decorators.BetaImplementation
    def setReportEngine(self, r=0):
        if self.rptEngine_ == r:
            return

        if self.rptEngine_:
            self.rptEngine_.destroyed.disconnect(self.setReportEngine)
            self.rptEngine_.signalRenderStatus.disconnect(
                self.slotRenderProgress)
            self.rptEngine_.preferedTemplate.disconnect(self.preferedTemplate)

        self.rptEngine_ = r
        if self.rptEngine_:
            self.rptEngine_.destroyed.connect(self.setReportEngine)
            self.rptEngine_.signalRenderStatus.connect(self.slotRenderProgress)
            self.rptEngine_.preferedTemplate.connect(self.preferedTemplate)

    @decorators.BetaImplementation
    def setReportPages(self, pgs):
        if self.report_ and self.report_.parent() == self:
            self.report_.deleteLater()

        self.report_ = pgs

    @decorators.BetaImplementation
    def exportToOds(self):
        if not self.rptEngine_ or not self.report_:
            return

        self.rptEngine_.exportToOds(self.report_)
