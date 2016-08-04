# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals

from PyQt4 import QtGui, QtCore # , uic

import pineboolib
#from pineboolib.qsaglobals import ustr
from pineboolib.utils import DefFun
from pineboolib import decorators

Qt = QtCore.Qt
# TODO: separar en otro fichero de utilidades

def ustr1(t):
    if isinstance(t, str): return t
    #if isinstance(t, QtCore.QString): return str(t)
    #if isinstance(t, str): return str(t,"UTF-8")
    try:
        return str(t)
    except Exception as e:
        print("ERROR Coercing to string:", repr(t))
        print("ERROR", e.__class__.__name__, str(e))
        return None

def ustr(*t1):
    return "".join([ ustr1(t) for t in t1 ])

class QLayoutWidget(QtGui.QWidget):
    pass

class ProjectClass(QtCore.QObject):
    def __init__(self):
        super(ProjectClass, self).__init__()
        self._prj = pineboolib.project

class QCheckBox(QtGui.QCheckBox):
    def __getattr__(self, name): return DefFun(self, name)

    @QtCore.pyqtProperty(int)
    def checked(self):
        return self.isChecked()

    @checked.setter
    def checked(self, v):
        self.setCheckState(v)



class QComboBox(QtGui.QComboBox):
    def __getattr__(self, name): return DefFun(self, name)
    @property
    def currentItem(self): return self.currentIndex

    def setCurrentItem(self, i): return self.setCurrentIndex(i)

class QButtonGroup(QtGui.QFrame):
    def __getattr__(self, name): return DefFun(self, name)
    @property
    def selectedId(self): return 0


class ProgressDialog(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        super(ProgressDialog,self).__init__(*args, **kwargs)
        self.title = "Untitled"
        self.step = 0
        self.steps = 100
    def __getattr__(self, name): return DefFun(self, name)

    def setup(self, title, steps):
        self.title = title
        self.step = 0
        self.steps = steps
        self.setWindowTitle("%s - %d/%d" % (self.title,self.step,self.steps))
        self.setWindowModality(QtCore.Qt.ApplicationModal)

    def setProgress(self, step):
        self.step = step
        self.setWindowTitle("%s - %d/%d" % (self.title,self.step,self.steps))
        if step > 0: self.show()
        self.update()
        QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.ExcludeUserInputEvents)


class FLTable(QtGui.QTableWidget):
    def __getattr__(self, name): return DefFun(self, name)



class FLReportViewer(ProjectClass):
    Append = 0x01
    Display = 0x02
    PageBreak = 0x04

    _requestUpdateReport = QtCore.pyqtSignal(int, name='requestUpdateReport')

    def __init__(self, *args):
        super(FLReportViewer,self).__init__()
        #  FLReportViewerInterface() : QObject(0), obj_(0) {
        #  FLReportViewerInterface(FLReportViewer *obj) : QObject(obj), obj_(0) {
        #  FLReportViewerInterface(QWidget *w, bool) : QObject(w) {
        #  FLReportViewerInterface(FLReportEngine *r) : QObject(0) {
        self.connects()

    def __getattr__(self, name): return DefFun(self, name)

    def connects(self):
        pass

    @decorators.NotImplementedWarn
    def renderReport(self, initRow = 0, initCol = 0, append = False, displayReport = True):
        return True

    @decorators.NotImplementedWarn
    def renderReport2(self, initRow = 0, initCol = 0, flags = Display):
        return True

    @decorators.NotImplementedWarn
    def setReportData(self, xmlDoc_Or_Query):
        return None

    @decorators.NotImplementedWarn
    def setReportTemplate(self,  t, style = None):
        return True

    @decorators.NotImplementedWarn
    def reportData(self):
        return None

    @decorators.NotImplementedWarn
    def reportTemplate(self):
        return None

    @decorators.NotImplementedWarn
    def exec_(self):
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


class QLineEdit(QtGui.QLineEdit):
    def __init__(self, *args, **kwargs):
        super(QLineEdit, self).__init__(*args,**kwargs)
        class TextEmul:
            def __init__(self, parent, f):
                self.parent = parent
                self.f = f
            def __call__(self):
                return self.f()
            def __str__(self):
                return self.f()
            def __getattr__(self, name):
                return getattr(self.f(),name)

        self.text = TextEmul(self, super(QLineEdit,self).text)

    def __getattr__(self, name):
        print("flcontrols.QLineEdit: Emulando método %r" % name)
        return self.defaultFunction

    def defaultFunction(self, *args, **kwargs):
        print("flcontrols.QLineEdit: llamada a método no implementado", args,kwargs)

class QListView(QtGui.QListView):
    def __init__(self, *args, **kwargs):
        super(QListView, self).__init__(*args, **kwargs)

    def __getattr__(self, name):
        print("flcontrols.QListView: Emulando método %r" % name)
        return self.defaultFunction

    def defaultFunction(self, *args, **kwargs):
        print("flcontrols.QListView: llamada a método no implementado", args,kwargs)

class QPushButton(QtGui.QPushButton):
    @property
    def pixmap(self):
        return self.icon()

    @pixmap.setter
    def pixmap(self, value):
        return self.setIcon(value)

    def setPixmap(self, value):
        return self.setIcon(value)

    def getToggleButton(self):
        return self.isCheckable()
    def setToggleButton(self, v):
        return self.setCheckable(v)

    toggleButton = property(getToggleButton,setToggleButton)
