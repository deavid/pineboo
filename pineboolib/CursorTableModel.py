# # -*- coding: utf-8 -*-

from pineboolib.flcontrols import ProjectClass
from pineboolib import decorators
from pineboolib.qsaglobals import ustr

from PyQt4 import QtCore

class CursorTableModel(QtCore.QAbstractTableModel):
    rows = 15
    cols = 5
    _cursor = None

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
        self.field_type = []
        for field in self._table.fields:
            #if field.visible_grid:
            self.sql_fields.append(field.name)
            self.field_aliases.append(aqtt(field.alias))
            self.field_type.append(field.mtd_type)    
            if field.pk: self._pk = field.name

        self._data = []
        self.cols = len(self.sql_fields)
        self.rows = 0
        self.where_filters = {}
        self.refresh()

    def refresh(self):
        parent = QtCore.QModelIndex()
        oldrows = self.rows
        self.beginRemoveRows(parent, 0, oldrows )
        where_filter = " "
        for k, wfilter in sorted(self.where_filters.items()):
            if wfilter is None: continue
            wfilter = wfilter.strip()
            if not wfilter: continue
            if where_filter is " ":
                where_filter = wfilter
            else:
                where_filter += " AND " + wfilter
        if where_filter is " ":
            where_filter = "1=1"
        self._cursor = self._prj.conn.cursor()
        # FIXME: Cuando la tabla es una query, aquí hay que hacer una subconsulta.
        # FIXME: Agregado limit de 5000 registros para evitar atascar pineboo
        # TODO: Convertir esto a un cursor de servidor
        sql = """SELECT %s FROM %s WHERE %s LIMIT 5000""" % (", ".join(self.sql_fields),self._table.name, where_filter)
        self._cursor.execute(sql)
        self.rows = 0
        self.endRemoveRows()
        if oldrows > 0:
            self.rowsRemoved.emit(parent, 0, oldrows - 1)
        newrows = self._cursor.rowcount
        self.beginInsertRows(parent, 0, newrows - 1)
        print("QUERY:", sql)
        self.rows = newrows
        self._data = []
        for row in self._cursor:
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

    @decorators.NotImplementedWarn
    def setValue(self,fieldname, value):
        return True

    def pK(self): #devuelve el nombre del campo pk
        return self._pk

    def fieldType(self, fieldName): # devuelve el tipo de campo
        value = None
        try:
            if not fieldName is None:
                value = self.field_type[self.sql_fields.index(fieldName)]
            else:
                value = None
            return value
        except:
            print("CursorTableModel: No se encuentra el campo %s" % fieldName)
            return None
            
    
    def alias(self, fieldName):
        value = None
        try:
            value = self.field_aliases[self.sql_fields.index(fieldName)]
            return value
        except:
            return value
        
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
                return "%s" % self.field_aliases[section]
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
