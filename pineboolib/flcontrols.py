# encoding: UTF-8
from __future__ import print_function
from __future__ import unicode_literals
from builtins import str
import traceback
import sip
sip.setapi('QString', 1)

from PyQt4 import QtGui, QtCore # , uic

import pineboolib
#from pineboolib.qsaglobals import ustr
from pineboolib.utils import DefFun

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

def NotImplementedWarn(fn):
    def newfn(*args,**kwargs):
        ret = fn(*args,**kwargs)
        x_args = [ repr(a) for a in args] + [ "%s=%s" % (k,repr(v)) for k,v in list(kwargs.items())]
        print("WARN: Function not yet implemented: %s(%s) -> %s" % (fn.__name__,", ".join(x_args),repr(ret)))
        return ret
    return newfn

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

class QButtonGroup(QtGui.QFrame):
    def __getattr__(self, name): return DefFun(self, name)
    @property
    def selectedId(self): return 0



class FLSqlQuery(ProjectClass):
    def __init__(self, name = None, conn = None):
        super(FLSqlQuery,self).__init__()

        if name:
            # Cargar plantilla de query desde .qry
            print("FIXME: Cargar plantilla de query %r (.qry)" % name)
        if conn:
            # Asociar a otra conexión de base de datos
            print("FIXME: Asociar a otra conexión %r " % conn)

    def __getattr__(self, name): return DefFun(self, name)
    @NotImplementedWarn
    def setTablesList(self, tablelist):
        return True

    @NotImplementedWarn
    def setSelect(self, select):
        return True

    @NotImplementedWarn
    def setFrom(self, from_):
        return True

    @NotImplementedWarn
    def setWhere(self, where):
        return True

    @NotImplementedWarn
    def exec_(self):
        return True

    @NotImplementedWarn
    def next(self):
        return False

    @NotImplementedWarn
    def size(self):
        return 0

    @NotImplementedWarn
    def valueParam(self, name):
        return ""

    @NotImplementedWarn
    def setValueParam(self, name, value):
        return None



class FLSqlCursor(ProjectClass):
    Insert = 0
    Edit = 1
    Del = 2
    Browse = 3

    _current_changed = QtCore.pyqtSignal(int, name='currentChanged')

    def __init__(self, actionname=None):
        super(FLSqlCursor,self).__init__()
        self._valid = False
        if actionname is None: raise AssertionError
        self.setAction(actionname)
        self._commit_actions = True
        self._current_row = -1
        self._chk_integrity = True

    def __getattr__(self, name): return DefFun(self, name)

    def mainFilter(self):
        return self._model.where_filters.get("main-filter", "")

    def setMainFilter(self, newFilter):
        print("New main filter:", newFilter)
        self._model.where_filters["main-filter"] = newFilter

    def setAction(self, actionname):
        try:
            self._action = self._prj.actions[actionname]
        except KeyError:
            print("Accion no encontrada:", actionname)
            self._action = self._prj.actions["articulos"]

        if self._action.table:
            self._model = CursorTableModel(self._action, self._prj)
            self._selection = QtGui.QItemSelectionModel(self._model)
            self._selection.currentRowChanged.connect(self.selection_currentRowChanged)
            self._current_row = self._selection.currentIndex().row()
        self._valid = True
        self._chk_integrity = True
        self._commit_actions = True

    def action(self):
        return self._action.name

    @NotImplementedWarn
    def setActivatedCheckIntegrity(self, state):
        self._chk_integrity = bool(state)
        return True

    @NotImplementedWarn
    def setActivatedCommitActions(self, state):
        self._commit_actions = bool(state)
        return True

    def selection_currentRowChanged(self, current, previous):
        if self._current_row == current.row(): return False
        self._current_row = current.row()
        self._current_changed.emit(self.at())
        print("cursor:%s , row:%d" %(self._action.table, self._current_row ))

    def selection(self): return self._selection

    def select(self, where_filter = ""):
        print("Select filter:", where_filter)
        self._model.where_filters["select"] = where_filter
        self._model.refresh()
        return True

    def isValid(self):
        return self._valid

    def isNull(self,fieldname):
        return self._model.value(self._current_row, fieldname) is None

    @NotImplementedWarn
    def setNull(self,fieldname):
        return True

    def valueBuffer(self, fieldname):
        if self._current_row < 0 or self._current_row > self._model.rows: return None
        return self._model.value(self._current_row, fieldname)

    @NotImplementedWarn
    def setValueBuffer(self, fieldname, newvalue):
        return True

    @NotImplementedWarn
    def transaction(self, block = False):
        return True

    @NotImplementedWarn
    def commit(self):
        return True

    @NotImplementedWarn
    def rollback(self):
        return True

    def refresh(self):
        self._model.refresh()

    def size(self):
        return self._model.rowCount()

    def at(self):
        row = self._current_row
        if row < 0: return -1
        if row >= self._model.rows: return -2
        return row

    def move(self, row):
        if row < 0: row = -1
        if row >= self._model.rows: row = self._model.rows
        if self._current_row == row: return False
        topLeft = self._model.index(row,0)
        bottomRight = self._model.index(row,self._model.cols-1)
        new_selection = QtGui.QItemSelection(topLeft, bottomRight)
        self._selection.select(new_selection, QtGui.QItemSelectionModel.ClearAndSelect)
        self._current_row = row
        self._current_changed.emit(self.at())
        if row < self._model.rows and row >= 0: return True
        else: return False

    def moveby(self, pos):
        return self.move(pos+self._current_row)

    def first(self): return self.move(0)

    def prev(self): return self.moveby(-1)

    def __next__(self): return self.moveby(1)

    def last(self): return self.move(self._model.rows-1)

    @NotImplementedWarn
    def setModeAccess(self, modeAccess):
        return True

    @NotImplementedWarn
    def refreshBuffer(self):
        return True

    @NotImplementedWarn
    def commitBuffer(self):
        return True

    @QtCore.pyqtSlot()
    def insertRecord(self):
        print("Insert record, please!", self._action.name)

    @QtCore.pyqtSlot()
    def editRecord(self):
        print("Edit your record!", self._action.name)

    @QtCore.pyqtSlot()
    def deleteRecord(self):
        print("Drop the row!", self._action.name)

    @QtCore.pyqtSlot()
    def browseRecord(self):
        print("Inspect, inspect!", self._action.name)

    @QtCore.pyqtSlot()
    def copyRecord(self):
        print("Clone your clone", self._action.name)

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


class FLUtil(ProjectClass):
    progress_dialog_stack = []
    def __getattr__(self, name): return DefFun(self, name)

    def translate(self, group, string):
        return QtCore.QString(string)

    def sqlSelect(self, table, fieldname, where):
        if where: where = "AND " + where
        cur = pineboolib.project.conn.cursor()

        cur.execute("""SELECT %s FROM %s WHERE 1=1 %s LIMIT 1""" % (fieldname, table, where))
        for ret, in cur:
            return ret

    def createProgressDialog(self, title, steps):
        pd_widget = ProgressDialog()
        pd_widget.setup(title, steps)
        self.__class__.progress_dialog_stack.append(pd_widget)

    def setProgress(self, step_number):
        pd_widget = self.__class__.progress_dialog_stack[-1]
        pd_widget.setProgress(step_number)

    def destroyProgressDialog(self):
        pd_widget = self.__class__.progress_dialog_stack[-1]
        del self.__class__.progress_dialog_stack[-1]
        pd_widget.hide()
        pd_widget.close()

    def nombreCampos(self, tablename):
        prj = pineboolib.project
        table = prj.tables[tablename]
        campos = [ field.name for field in table.fields ]
        return [len(campos)]+campos

    def addMonths(self, fecha, offset):
        if isinstance(fecha, str) or isinstance(fecha, QtCore.QString):
            fecha = QtCore.QDate.fromString(fecha)
        if not isinstance(fecha, QtCore.QDate):
            print("FATAL: FLUtil.addMonths: No reconozco el tipo de dato %r" % type(fecha))
        return fecha.addMonths(offset)




class CursorTableModel(QtCore.QAbstractTableModel):
    rows = 15
    cols = 5
    def __init__(self, action,project, *args):
        super(CursorTableModel,self).__init__(*args)
        from pineboolib.qsaglobals import aqtt

        self._action = action
        self._prj = project
        if action and action.table:
            self._table = project.tables[action.table]
        else:
            raise AssertionError
        self.sql_fields = []
        self.field_aliases = []
        for field in self._table.fields:
            self.sql_fields.append(field.name)
            self.field_aliases.append(aqtt(field.alias))

        self._data = []
        self.cols = len(self.sql_fields)
        self.rows = 0
        self.where_filters = {}
        self.refresh()

    def refresh(self):
        parent = QtCore.QModelIndex()
        oldrows = self.rows
        self.beginRemoveRows(parent, 0, oldrows )
        where_filter = ""
        for k, wfilter in sorted(self.where_filters.items()):
            if wfilter is None: continue
            wfilter = wfilter.strip()
            if not wfilter: continue
            where_filter += " AND " + wfilter
        cur = self._prj.conn.cursor()
        # FIXME: Cuando la tabla es una query, aquí hay que hacer una subconsulta.
        # FIXME: Agregado limit de 5000 registros para evitar atascar pineboo
        # TODO: Convertir esto a un cursor de servidor
        sql = """SELECT %s FROM %s WHERE 1=1 %s LIMIT 5000""" % (", ".join(self.sql_fields),self._table.name, where_filter)
        cur.execute(sql)
        self.rows = 0
        self.endRemoveRows()
        if oldrows > 0:
            self.rowsRemoved.emit(parent, 0, oldrows - 1)
        newrows = cur.rowcount
        self.beginInsertRows(parent, 0, newrows - 1)
        print("QUERY:", sql)
        self.rows = newrows
        self._data = []
        for row in cur:
            self._data.append(row)
        self.endInsertRows()
        topLeft = self.index(0,0)
        bottomRight = self.index(self.rows-1,self.cols-1)
        self.dataChanged.emit(topLeft,bottomRight)
        print("rows:", self.rows)

    def value(self, row, fieldname):
        if row < 0 or row >= self.rows: return None
        col = self.sql_fields.index(fieldname)
        return self._data[row][col]

    def columnCount(self, parent = None):
        if parent is None: parent = QtCore.QModelIndex()
        if parent.isValid(): return 0
        #print "colcount", self.cols
        return self.cols

    def rowCount(self, parent = None):
        if parent is None: parent = QtCore.QModelIndex()
        if parent.isValid(): return 0
        #print "rowcount", self.rows
        return self.rows

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal:
            if role == QtCore.Qt.DisplayRole:
                return " %s " % self.field_aliases[section]
        return QtCore.QAbstractTableModel.headerData(self, section, orientation, role)

    def data(self, index, role = QtCore.Qt.DisplayRole):
        row = index.row()
        col = index.column()
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            try:
                val = self._data[row][col]
                ret = ustr(val)
                #print " data -> ", row, col, ret
                return ret
            except Exception as e:
                print("CursorTableModel.data:", row,col,e)
                print(traceback.format_exc())
                raise

        return None


class FLTableDB(QtGui.QTableView):
    def __init__(self, parent = None, action_or_cursor = None, *args):
        # TODO: Falta el lineeditsearch y el combo, que los QS lo piden
        super(FLTableDB,self).__init__(parent,*args)
        self._v_header = self.verticalHeader()
        self._v_header.setDefaultSectionSize(18)
        self._h_header = self.horizontalHeader()
        self._h_header.setDefaultSectionSize(70)
        self._parent = parent
        while True:
            parent_cursor = getattr(self._parent,"_cursor", None)
            if parent_cursor: break
            new_parent = self._parent.parentWidget()
            if new_parent is None: break
            self._parent = new_parent
            print(self._parent)

        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.setAlternatingRowColors(True)

        if action_or_cursor is None and parent_cursor:
            action_or_cursor = parent_cursor
        if isinstance(action_or_cursor,FLSqlCursor):
            self._cursor = action_or_cursor
        elif isinstance(action_or_cursor,str):
            self._cursor = FLSqlCursor(action_or_cursor)
        else:
            self._cursor = None
        if self._cursor:
            self._h_header.setResizeMode(QtGui.QHeaderView.ResizeToContents)
            self.setModel(self._cursor._model)
            self.setSelectionModel(self._cursor.selection())
        self.tableRecords = self # control de tabla interno
        self.sort = []
        self.timer_1 = QtCore.QTimer(self)
        self.timer_1.singleShot(100, self.loaded)

    def __getattr__(self, name): return DefFun(self, name)

    def loaded(self):
        # Es necesario pasar a modo interactivo lo antes posible
        # Sino, creamos un bug en el cierre de ventana: se recarga toda la tabla para saber el tamaño
        print("FLTableDB: setting columns in interactive mode")
        self._h_header.setResizeMode(QtGui.QHeaderView.Interactive)
        self.timer_1.deleteLater()
        self.timer_1 = None

    def cursor(self):
        assert self._cursor
        return self._cursor

    def obj(self):
        return self

    @NotImplementedWarn
    def putFirstCol(self, fN): return True

    def refresh(self):
        print("FLTableDB: refresh()")
        #self._cursor.refresh()

    @QtCore.pyqtSlot()
    def insertRecord(self):
        self._cursor.insertRecord()

    @QtCore.pyqtSlot()
    def editRecord(self):
        self._cursor.editRecord()

    @QtCore.pyqtSlot()
    def deleteRecord(self):
        self._cursor.deleteRecord()

    @QtCore.pyqtSlot()
    def browseRecord(self):
        self._cursor.browseRecord()

    @QtCore.pyqtSlot()
    def copyRecord(self):
        self._cursor.copyRecord()

class FLTable(QtGui.QTableWidget):
    def __getattr__(self, name): return DefFun(self, name)

class FLFormSearchDB( QtGui.QWidget ):
    _accepted = None
    _cursor = None

    def __init__(self,cursor):
        super(FLFormSearchDB,self).__init__()
        self._accepted = False
        self._cursor = FLSqlCursor(cursor)

    def __getattr__(self, name): return DefFun(self, name)

    @NotImplementedWarn
    def setCursor(self):
        print("Definiendo cursor")

    @NotImplementedWarn
    def setMainWidget(self):
        print("Creamos la ventana")

    @NotImplementedWarn
    def exec_(self, valor):
        print("Ejecutamos la ventana y esperamos respuesta, introducimos desde y hasta en cursor")
        return valor

    @NotImplementedWarn
    def setFilter(self):
        print("configuramos Filtro")

    @NotImplementedWarn
    def accepted(self):
        return self._accepted

    @NotImplementedWarn
    def cursor(self):
        return self._cursor


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

    @NotImplementedWarn
    def renderReport(self, initRow = 0, initCol = 0, append = False, displayReport = True):
        return True

    @NotImplementedWarn
    def renderReport2(self, initRow = 0, initCol = 0, flags = Display):
        return True

    @NotImplementedWarn
    def setReportData(self, xmlDoc_Or_Query):
        return None

    @NotImplementedWarn
    def setReportTemplate(self,  t, style = None):
        return True

    @NotImplementedWarn
    def reportData(self):
        return None

    @NotImplementedWarn
    def reportTemplate(self):
        return None

    @NotImplementedWarn
    def exec_(self):
        return

    @NotImplementedWarn
    def show(self):
        return

    @NotImplementedWarn
    def csvData(self):
        return None

    @NotImplementedWarn
    def printReport(self): return None

    @NotImplementedWarn
    def printReportToPS(self,outPsFile): return None

    @NotImplementedWarn
    def printReportToPDF(self,outPdfFile): return None

    @NotImplementedWarn
    def setNumCopies(self,numCopies): return None

    @NotImplementedWarn
    def setPrintToPos(self,ptp): return None

    @NotImplementedWarn
    def setPrinterName(self,pName): return None

    @NotImplementedWarn
    def reportPrinted(self): return True

    @NotImplementedWarn
    def reparent(self,parentFrame): return None

    @NotImplementedWarn
    def slotFirstPage(self): return None

    @NotImplementedWarn
    def slotLastPage(self): return None

    @NotImplementedWarn
    def slotNextPage(self): return None

    @NotImplementedWarn
    def slotPrevPage(self): return None

    @NotImplementedWarn
    def slotZoomUp(self): return None

    @NotImplementedWarn
    def slotZoomDown(self): return None

    @NotImplementedWarn
    def exportFileCSVData(self): return None

    @NotImplementedWarn
    def exportToPDF(self): return None

    @NotImplementedWarn
    def sendEMailPDF(self): return None

    @NotImplementedWarn
    def saveSVGStyle(self): return None

    @NotImplementedWarn
    def saveSimpleSVGStyle(self): return None

    @NotImplementedWarn
    def loadSVGStyle(self): return None

    @NotImplementedWarn
    def setAutoClose(self,b): return None

    @NotImplementedWarn
    def setResolution(self,dpi): return None

    @NotImplementedWarn
    def setPixel(self,relDpi): return None

    @NotImplementedWarn
    def setDefaults(self): return None

    @NotImplementedWarn
    def updateReport(self): return None

    @NotImplementedWarn
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

class QPushButton(QtGui.QPushButton):
    @property
    def pixmap(self):
        return self.icon()

    @pixmap.setter
    def pixmap(self, value):
        return self.setIcon(value)

    def setPixmap(self, value):
        return self.setIcon(value)

