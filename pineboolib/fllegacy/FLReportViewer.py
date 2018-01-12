from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from pineboolib import decorators
from pineboolib.flcontrols import ProjectClass

from pineboolib.kugar.mreportviewer import MReportViewer

from pineboolib.fllegacy.FLUtil import FLUtil
from pineboolib.fllegacy.FLReportEngine import FLReportEngine
from pineboolib.fllegacy.FLWidgetReportViewer import FLWidgetReportViewer
from pineboolib.fllegacy.FLSmtpClient import FLSmtpClient


class FLReportViewer(ProjectClass, FLWidgetReportViewer):

    def __init__(self, parent, name, embedInParent, rptEngine):
        pParam = 0 if parent and embedInParent else Qt.WStyle_Customize | Qt.WStyle_Maximize | Qt.WStyle_Title | Qt.WStyle_NormalBorder | Qt.WStyle_Dialog | Qt.WShowModal | Qt.WStyle_SysMenu

        super(FLReportViewer, self).__init__(parent, name, pParam)

        self.loop_ = False
        self.reportPrinted_ = False
        self.rptViewer_ = 0
        self.rptEngine_ = 0
        self.report_ = 0
        self.qry_ = 0
        self.slotsPrintDisabled_ = False
        self.slotsExportedDisabled_ = False
        self.printing_ = False

        if not name:
            self.setName("FLReportViewer")

        self.embedInParent_ = (parent and embedInParent)

        if self.embedInParent_:
            self.autoClose_ = False
            self.menubar.hide()
            self.chkAutoClose.hide()
            self.spnResolution.hide()
            self.spnPixel.hide()
            self.salir.setVisible(False)

            if not parent.layout():
                lay = Qt.QVBoxLayout(parent)
                lay.addWidget(self)
            else:
                parent.layout().add(self)
        else:
            self.autoClose_ = bool(FLUtil.readSettingEntry("rptViewer/autoClose", "false"))
            self.chkAutoClose.setChecked(self.autoClose_)

        self.rptViewer_ = MReportViewer(self)
        self.setReportEngine(FLReportEngine(self) if rptEngine == 0 else rptEngine)

        self.setFont(QtWidgets.QApplication.font())
        self.setFocusPolicy(Qt.QWidget.FocusPolicy.StrongFocus)

        self.lePara.setText(str(FLUtil.readSettingEntry("email/to")))
        self.leDe.setText(str(FLUtil.readSettingEntry("email/from")))
        self.leMailServer.setText(str(FLUtil.readSettingEntry("email/mailserver")))

        self.initCentralWidget_ = self.centralWidget()

        self.smtpClient_ = FLSmtpClient(self)
        self.smtpClient_.status.connect(self.lblEstado.setText)

        self.setCentralWidget(self.rptViewer_)
        self.frEmail.hide()
        self.initCentralWidget.hide()

        if not self.embedInParent_:
            self.spnResolution.setValue(int(FLUtil.readDBSettingEntry("rptViewer/dpi", str(self.rptViewer_.resolution()))))
            self.spnPixel.setValue(float(FLUtil.readDBSettingEntry("rptViewer/pixel", float(self.rptEngine_.relDpi()))) * 10.)

        self.report_ = self.rptViewer_.reportPages()

    @decorators.BetaImplementation
    def rptViewer(self):
        return self.rptViewer_

    @decorators.BetaImplementation
    def rptEngine(self):
        return self.rptEngine_

    @decorators.BetaImplementation
    def setReportEngine(self, r):
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

            self.ledStyle.setDisabled(False)
            self.save_page_SVG.setDisabled(False)
            self.save_page_tpl_SVG.setDisabled(False)
            self.load_tpl_SVG.setDisabled(False)
        else:
            self.ledStyle.setDisabled(True)
            self.save_page_SVG.setDisabled(True)
            self.save_page_tpl_SVG.setDisabled(True)
            self.load_tpl_SVG.setDisabled(True)

        if noSigDestroy:
            self.rptViewer_.setReportEngine(self.rptEngine_)

    @decorators.BetaImplementation
    def exec_(self):
        if self.loop_:
            return

        # Qt.QWidget.show() #FIXME
        self.show()

        if self.embedInParent_:
            return

        self.loop_ = True
        QtWidgets.QApplication.eventLoop().enterLoop()
        self.clearWFlags(Qt.WShowModal)

    @decorators.BetaImplementation
    def csvData(self):
        return self.rptEngine_.csvData() if self.rptEngine_ else ""

    @decorators.BetaImplementation
    def closeEvent(self, e):
        if self.printing_:
            return

        # Qt.QWidget.show() #FIXME
        self.show()
        self.frameGeometry()
        # Qt.QWidget.hide() #FIXME
        self.hide()

        if not self.embedInParent_:
            geo = Qt.QRect(self.x(), self.y(), self.width(), self.height())
            QtWidgets.QApplication.saveGeometryForm(self.name(), geo)

        if self.loop_ and not self.embedInParent_:
            self.loop_ = False
            QtWidgets.QApplication.eventLoop().exitLoop()

        # Qt.QWidget.closeEvent() #FIXME
        self.closeEvent(e)
        self.deleteLater()

    @decorators.BetaImplementation
    def showEvent(self, e):
        # Qt.QWidget.showEvent() #FIXME
        self.showEvent(e)

        if not self.embedInParent_:
            geo = Qt.QRect(QtWidgets.QApplication.geometryForm(self.name()))
            if geo.isValid():
                desk = QtWidgets.QApplication.desktop().availableGeometry(self)
                inter = desk.intersect(geo)
                self.resize(geo.size())
                if inter.width() * inter.height() > (geo.width() * geo.height() / 20):
                    self.move(geo.topLeft())

    @decorators.BetaImplementation
    def renderReport(self, initRow, initCol, append, displayReport=None):
        flags = None
        if displayReport is None:
            flags = append
        else:
            flags = MReportViewer.RenderReportFlags.Append if append else 0 | int(MReportViewer.RenderReportFlags.Display if displayReport else 0)

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

        fileName = Qt.QFileDialog.getSaveFileName(
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

        q = Qt.QMessageBox.question(
            self,
            FLUtil.translate(self, "app", "Sobreescribir {}").format(fileName),
            FLUtil.translate(self, "app", "Ya existe un fichero llamado {}. ¿ Desea sobreescribirlo ?").format(fileName),
            FLUtil.translate(self, "app", "&Sí"),
            FLUtil.translate(self, "app", "&No"),
            "",
            0,
            1
        )

        if Qt.QFile.exists(fileName) and q:
            return

        file = Qt.QFile(fileName)

        if file.open(Qt.IO_WriteOnly):
            stream = Qt.QTextStream(file)
            stream << self.csvData() << "\n"
            file.close()
        else:
            Qt.QMessageBox.critical(
                self,
                FLUtil.translate(self, "app", "Error abriendo fichero"),
                FLUtil.translate(self, "app", "No se pudo abrir el fichero {} para escribir: {}").arg(fileName, QtWidgets.QApplication.translate("QFile", file.errorString()))
            )

    @decorators.BetaImplementation
    def exportToPdf(self):
        if self.slotsExportedDisabled_:
            return

        fileName = Qt.QFileDialog.getSaveFileName(
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

        q = Qt.QMessageBox.question(
            self,
            FLUtil.translate(self, "app", "Sobreescribir {}").format(fileName),
            FLUtil.translate(self, "app", "Ya existe un fichero llamado {}. ¿ Desea sobreescribirlo ?").format(fileName),
            FLUtil.translate(self, "app", "&Sí"),
            FLUtil.translate(self, "app", "&No"),
            "",
            0,
            1
        )

        if Qt.QFile.exists(fileName) and q:
            return

        self.slotPrintReportToPDF(fileName)

    # @decorators.BetaImplementation
    # def sendEMailPdf(self):
    #     t = self.leDocumento.text()
    #     name = "informe.pdf" if not t or t == "" else t
    #     fileName = Qt.QFileDialog.getSaveFileName(
    #         AQ_USRHOME + "/" + name + ".pdf",
    #         FLUtil.translate(self, "app", "Fichero PDF a enviar (*.pdf)"),
    #         self,
    #         FLUtil.translate(self, "app", "Exportar a PDF para enviar"),
    #         FLUtil.translate(self, "app", "Exportar a PDF para enviar")
    #     )
