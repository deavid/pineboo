from pineboolib.flcontrols import ProjectClass
from pineboolib.utils import DefFun
from pineboolib import decorators

from PyQt4 import QtCore


class FLReportViewer(ProjectClass):
    Append = 0x01
    Display = 0x02
    PageBreak = 0x04

    _requestUpdateReport = QtCore.pyqtSignal(int, name='requestUpdateReport')
    template_ = None
    data_ = None
    append_ = None
    displayReport_ = None

    def __init__(self, *args):
        super(FLReportViewer,self).__init__()
        #  FLReportViewerInterface() : QObject(0), obj_(0) {
        #  FLReportViewerInterface(FLReportViewer *obj) : QObject(obj), obj_(0) {
        #  FLReportViewerInterface(QWidget *w, bool) : QObject(w) {
        #  FLReportViewerInterface(FLReportEngine *r) : QObject(0) {
        self.connects()
        self.template_ = None
        self.data_ = None
        self.displayReport_ = True

    def __getattr__(self, name): return DefFun(self, name)

    def connects(self):
        pass

    def renderReport(self, initRow = 0, initCol = 0, append = False, displayReport = True):
        self.append = append
        self.displayReport_ = displayReport
        return True

    @decorators.NotImplementedWarn
    def renderReport2(self, initRow = 0, initCol = 0, flags = Display):
        return True


    def setReportData(self, xmlDoc_Or_Query):
        self.data_ = xmlDoc_Or_Query


    def setReportTemplate(self,  t, style = None):
        self.template_ = t

    @decorators.NotImplementedWarn
    def reportData(self):
        return None

    @decorators.NotImplementedWarn
    def reportTemplate(self):
        return None

    
    def exec_(self):
        print("FIXME::FLReportViewer.exec_() !!!")
        return

    @decorators.NotImplementedWarn
    def show(self):
        return

    @decorators.NotImplementedWarn
    def csvData(self):
        return None

    @decorators.NotImplementedWarn
    def printReport(self): return None

    @decorators.NotImplementedWarn
    def printReportToPS(self,outPsFile): return None

    @decorators.NotImplementedWarn
    def printReportToPDF(self,outPdfFile): return None

    @decorators.NotImplementedWarn
    def setNumCopies(self,numCopies): return None

    @decorators.NotImplementedWarn
    def setPrintToPos(self,ptp): return None

    @decorators.NotImplementedWarn
    def setPrinterName(self,pName): return None

    @decorators.NotImplementedWarn
    def reportPrinted(self): return True

    @decorators.NotImplementedWarn
    def reparent(self,parentFrame): return None

    @decorators.NotImplementedWarn
    def slotFirstPage(self): return None

    @decorators.NotImplementedWarn
    def slotLastPage(self): return None

    @decorators.NotImplementedWarn
    def slotNextPage(self): return None

    @decorators.NotImplementedWarn
    def slotPrevPage(self): return None

    @decorators.NotImplementedWarn
    def slotZoomUp(self): return None

    @decorators.NotImplementedWarn
    def slotZoomDown(self): return None

    @decorators.NotImplementedWarn
    def exportFileCSVData(self): return None

    @decorators.NotImplementedWarn
    def exportToPDF(self): return None

    @decorators.NotImplementedWarn
    def sendEMailPDF(self): return None

    @decorators.NotImplementedWarn
    def saveSVGStyle(self): return None

    @decorators.NotImplementedWarn
    def saveSimpleSVGStyle(self): return None

    @decorators.NotImplementedWarn
    def loadSVGStyle(self): return None

    @decorators.NotImplementedWarn
    def setAutoClose(self,b): return None

    @decorators.NotImplementedWarn
    def setResolution(self,dpi): return None

    @decorators.NotImplementedWarn
    def setPixel(self,relDpi): return None

    @decorators.NotImplementedWarn
    def setDefaults(self): return None

    @decorators.NotImplementedWarn
    def updateReport(self): return None

    @decorators.NotImplementedWarn
    def updateDisplay(self): return None

"""
  void setStyleName(const QString &style) {
  MReportViewer *rptViewer() {
  void setReportEngine(FLReportEngine *r) {
  void rptViewerEmbedInParent(QWidget *parentFrame) {
  void setReportPages(FLReportPages *pgs) {
  FLPicture *getCurrentPage() {
  FLPicture *getFirstPage() {
  FLPicture *getPreviousPage() {
  FLPicture *getNextPage() {
  FLPicture *getLastPage() {
  FLPicture *getPageAt(uint i) {
  void clearPages() {
  void appendPage() {
  int getCurrentIndex() {
  void setCurrentPage(int idx) {
  void setPageSize(int s) {
  void setPageOrientation(int o) {
  void setPageDimensions(QSize dim) {
  int pageSize() {
  int pageOrientation() {
  QSize pageDimensions() {
  int pageCount() {
  QObject *child(const QString &objName) {
  void disableSlotsPrintExports(bool disablePrints = true, bool disableExports = true) {
  void setName(const QString &n) {
  FLReportViewer *obj() {
"""