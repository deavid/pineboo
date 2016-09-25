# # -*- coding: utf-8 -*-

from pineboolib.flcontrols import ProjectClass
from pineboolib import decorators
from pineboolib.qsaglobals import ustr
import pineboolib

from PyQt4 import QtCore
from pineboolib.fllegacy.FLSqlQuery import FLSqlQuery
from pineboolib.fllegacy.FLFieldMetaData import FLFieldMetaData
from pineboolib.fllegacy.FLTableMetaData import FLTableMetaData
import traceback

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
            project.conn.manager().metadata(self._table.name)
        else:
            raise AssertionError
        self.sql_fields = []
        self.field_aliases = []
        self.field_type = []
        self.field_metaData = []
        #for field in self._table.fields:
            #if field.visible_grid:
            #self.sql_fields.append(field.name())
            #self.field_metaData.append(field)
        #    self.tableMetadata().addField(field)
        self._data = []
        self.cols = len(self.tableMetadata().fieldListObject())
        self.rows = 0
        self.where_filters = {}
        self.refresh()
        
    
    def metadata(self):
        return self._prj.conn.manager().metadata(self._table.name)

    def refresh(self):
        #print("refrescando modelo tabla %s" % self.tableMetadata().name())
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
        sql_fields = []
        for field in self.tableMetadata().fieldListObject():
            #if field.visibleGrid():
            #    sql_fields.append(field.name())
            sql_fields.append(field.name())
        sql = """SELECT %s FROM %s WHERE %s LIMIT 5000""" % (", ".join(sql_fields),self.tableMetadata().name(), where_filter)
        self._cursor.execute(sql)
        self.rows = 0
        self.endRemoveRows()
        if oldrows > 0:
            self.rowsRemoved.emit(parent, 0, oldrows - 1)
        newrows = self._cursor.rowcount
        self.beginInsertRows(parent, 0, newrows - 1)
        #print("QUERY:", sql)
        self.rows = newrows
        self._data = []
        for row in self._cursor:
            self._data.append(row)
        self.endInsertRows()
        topLeft = self.index(0,0)
        bottomRight = self.index(self.rows-1,self.cols-1)
        self.dataChanged.emit(topLeft,bottomRight)
        #print("rows:", self.rows)

    def value(self, row, fieldname):
        if row < 0 or row >= self.rows: return None
        
        col = self.metadata().indexPos(fieldname)
        campo = self._data[row][col]
        
        """
        if self.metadata().field(fieldname).type() == "pixmap":
            q = FLSqlQuery()     
            q.setSelect("contenido")
            q.setFrom("fllarge")
            q.setWhere("refkey == '%s'" % campo)
            q.exec_()
            q.first()
            return q.value(0)
        else:
            return campo
        """
        return campo   
        
        """
        value = None
        if row < 0 or row >= self.rows: return value
        try:
            #col = self.sql_fields.index(fieldname)
            col = self._prj.conn.manager.metadata(self._table.name).fieldIndex(fieldname)
        except:
            return value
        if self.field_type[col] == 'pixmap':
            campo = self._data[row][col]
            cur = pineboolib.project.conn.cursor()
            sql = "SELECT contenido FROM fllarge WHERE refkey ='%s'" % campo
            cur.execute(sql)
            for ret, in cur:
                value = ret
        else:
            value = self._data[row][col]
        return value
        """
    
    """
    Asigna un valor una celda
    @param row. Columna afectada
    @param fieldname. Nonbre de la fila afectata. Se puede obtener la columna con self.metadata().indexPos(fieldname)
    @param value. Valor a asignar. Puede ser texto, pixmap, etc...
    """
    @decorators.NotImplementedWarn
    def setValue(self, row, fieldname, value):
        col = self.metadata().indexPos(fieldname)
        print("CursorTableModel.setValueBuffer(row %s, col %s) = %s" % (row, col, value))
    
    """
    Crea una nueva linea en el tableModel
    @param buffer . PNBuffer a añadir
    """
    @decorators.NotImplementedWarn
    def newRowFromBuffer(self, buffer):
        pass
            

    def pK(self): #devuelve el nombre del campo pk
        return self.tableMetadata().primaryKey()
        #return self._pk

    def fieldType(self, fieldName): # devuelve el tipo de campo
        field = self.tableMetadata().field(fieldName)
        if field:
            return field.type()
        else:
            return None
        """
        value = None
        try:
            if not fieldName is None:
                value = self.field_metaData[self.sql_fields.index(fieldName)].type()
            else:
                value = None
            return value
        except:
            print("CursorTableModel: No se encuentra el campo %s" % fieldName)
            return None
            
        """
    def alias(self, fieldName):
        return self.tableMetadata().field(fieldName).alias()
        """
        value = None
        try:
            value = self.field_metaData[self.sql_fields.index(fieldName)].alias()
            return value
        except:
            return value
        """
    def columnCount(self, parent = None):
        if parent is None: parent = QtCore.QModelIndex()
        if parent.isValid(): return 0
        #print(self.cols)
        #print("colcount", self.cols)
        return self.cols

    def rowCount(self, parent = None):
        if parent is None: parent = QtCore.QModelIndex()
        if parent.isValid(): return 0
        #print("rowcount", self.rows)
        return self.rows

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal:
            if role == QtCore.Qt.DisplayRole:
                #if self.field_metaData[section].visibleGrid():
                #    return "%s" % self.field_metaData[section].alias()
                #else:
                #    return None
                #return self.field_metaData[section].alias()
                alias = str(self.tableMetadata().indexFieldObject(section).alias())
                #print(alias)
                return alias
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
    
    def fieldMetadata(self, fieldName):
        return self.tableMetadata().field(fieldName)
        """
        try:
            pos = self.field_metaData(fieldName)
            return self.field_metaData[pos]
        except:
            return False
            #print("CursorTableModel: %s.%s no hay datos" % ( self._table.name, fieldName ))
        """
    def tableMetadata(self):
        return self._prj.conn.manager().metadata(self._table.name)
        
    
        
        
