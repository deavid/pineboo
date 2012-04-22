# encoding: UTF-8
import pineboolib

from PyQt4 import QtGui, QtCore, uic
Qt = QtCore.Qt


class ProjectClass(object):
    def __init__(self):
        self._prj = pineboolib.project

class FLSqlCursor(ProjectClass):
    def __init__(self, actionname=None):
        super(FLSqlCursor,self).__init__()
        self._valid = False
        if actionname is None: 
            self._action = None
            self._model = None
            self._valid = False
            return 
        self._action = self._prj.actions[actionname]
        print "New Cursor:", actionname,self._action
        self._model = CursorTableModel(self._action, self._prj)
        self._valid = True
        
    def isValid(self):
        return self._valid
    
    def valueBuffer(self, fieldname):
        return ""
    
    def transaction(self, block = False):
        return True

class FLUtil(ProjectClass):
    def translate(self, group, string):
        return string
        

class CursorTableModel(QtCore.QAbstractTableModel):
    rows = 15
    cols = 5
    def __init__(self, action,project, *args):
        super(CursorTableModel,self).__init__(*args)
        self._action = action
        self._prj = project
        self._table = project.tables[action.table]
        
    def columnCount(self, parent = None):
        if parent is None: parent = QtCore.QModelIndex()
        if parent.isValid(): raise AssertionError, "Valid parent passed to columnCount"
        return self.cols
    
    def rowCount(self, parent = None):
        if parent is None: parent = QtCore.QModelIndex()
        if parent.isValid(): raise AssertionError, "Valid parent passed to rowCount"
        return self.rows

    def data(self, index, role = QtCore.Qt.DisplayRole):
        row = index.row()
        col = index.column()
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            return "Data"
        return None
            
            
class FLTableDB(QtGui.QTableView):
    def __init__(self, parent = None, action_or_cursor = None, *args):
        super(FLTableDB,self).__init__(parent,*args)
        self._parent = parent
        parent_cursor = getattr(parent,"_cursor", None)
        if action_or_cursor is None and parent_cursor:
            action_or_cursor = parent_cursor
        print "###",parent , action_or_cursor
        if isinstance(action_or_cursor,FLSqlCursor) or action_or_cursor: # <-- isinstance devuelve False???
            self._cursor = action_or_cursor
        else:
            self._cursor = FLSqlCursor(action_or_cursor)
        self.setModel(self._cursor._model)
        
        
    def cursor(self): return self._cursor
    
class FLTable(QtGui.QTableWidget):
    pass
    
