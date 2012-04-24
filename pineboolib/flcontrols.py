# encoding: UTF-8
import pineboolib

from PyQt4 import QtGui, QtCore, uic
from pineboolib.qsaglobals import aqtt

Qt = QtCore.Qt

class QLayoutWidget(QtGui.QWidget):
    pass
    
class ProjectClass(object):
    def __init__(self):
        self._prj = pineboolib.project

class FLSqlCursor(ProjectClass):
    def __init__(self, actionname=None):
        super(FLSqlCursor,self).__init__()
        self._valid = False
        if actionname is None: raise AssertionError
        
        self._action = self._prj.actions[actionname]
        print "New Cursor:", actionname,self._action.table
            
        self._model = CursorTableModel(self._action, self._prj)
        self._valid = True
        self._selection = QtGui.QItemSelectionModel(self._model)
        self._selection.currentRowChanged.connect(self.selection_currentRowChanged)
        self._current_row = self._selection.currentIndex().row()
        
    def selection_currentRowChanged(self, current, previous):
        assert( previous.row() == self._current_row )
        self._current_row = current.row()
        print "cursor:%s , row:%d" %(self._action.table, self._current_row )
    
    def selection(self): return self._selection
        
    def isValid(self):
        return self._valid
    
    def valueBuffer(self, fieldname):
        if self._current_row < 0 or self._current_row > self._model.rows: return None
        return self._model.value(self._current_row, fieldname)
    
    def transaction(self, block = False):
        return True
    def commit(self):
        return True
    def rollback(self):
        return True
        

class FLUtil(ProjectClass):
    def translate(self, group, string):
        return QtCore.QString(string)
        
    def sqlSelect(self, table, fieldname, where):
        if where: where = "AND " + where
        cur = pineboolib.project.conn.cursor()
        cur.execute("""SELECT %s FROM %s WHERE 1=1 %s""" % (fieldname, table, where))
        for ret, in cur:
            return ret
            
            

class CursorTableModel(QtCore.QAbstractTableModel):
    rows = 15
    cols = 5
    def __init__(self, action,project, *args):
        super(CursorTableModel,self).__init__(*args)
        self._action = action
        self._prj = project
        if action:
            self._table = project.tables[action.table]
        cur = self._prj.conn.cursor()
        self.sql_fields = []
        self.field_aliases = []
        for field in self._table.fields:
            self.sql_fields.append(field.name)
            self.field_aliases.append(aqtt(field.alias))
            
        cur.execute("""SELECT %s FROM %s """ % (", ".join(self.sql_fields),self._table.name))

        self.modules = {}
        self.cols = len(self.sql_fields)
        self.rows = cur.rowcount
        self.data = []
        for row in cur:
            self.data.append(row)
        
    def value(self, row, fieldname):
        col = self.sql_fields.index(fieldname)
        return self.data[row][col]
        
    def columnCount(self, parent = None):
        if parent is None: parent = QtCore.QModelIndex()
        if parent.isValid(): raise AssertionError, "Valid parent passed to columnCount"
        return self.cols
    
    def rowCount(self, parent = None):
        if parent is None: parent = QtCore.QModelIndex()
        if parent.isValid(): raise AssertionError, "Valid parent passed to rowCount"
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
                val = self.data[row][col]
                if isinstance(val, str): val = unicode(val,"UTF-8")
                return val 
            except Exception,e:
                print row,col,e
                return "-InvalidData-"
        return None
            
            
class FLTableDB(QtGui.QTableView):
    def __init__(self, parent = None, action_or_cursor = None, *args):
        super(FLTableDB,self).__init__(parent,*args)
        self._v_header = self.verticalHeader()
        self._v_header.setDefaultSectionSize(18)
        self._h_header = self.horizontalHeader()
        self._h_header.setDefaultSectionSize(70)
        self._h_header.setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self._parent = parent
        while True:
            parent_cursor = getattr(self._parent,"_cursor", None)
            if parent_cursor: break
            new_parent = self._parent.parentWidget()
            if new_parent is None: break
            self._parent = new_parent
            print self._parent
            
        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.setAlternatingRowColors(True)
        
        if action_or_cursor is None and parent_cursor:
            action_or_cursor = parent_cursor
        if isinstance(action_or_cursor,FLSqlCursor): 
            self._cursor = action_or_cursor
        elif isinstance(action_or_cursor,basestring): 
            self._cursor = FLSqlCursor(action_or_cursor)
        else:
            self._cursor = None
        if self._cursor:
            self.setModel(self._cursor._model)
            self.setSelectionModel(self._cursor.selection())
        
    def cursor(self): return self._cursor
    
    def putFirstCol(self, fN): return True
    
class FLTable(QtGui.QTableWidget):
    pass
    
