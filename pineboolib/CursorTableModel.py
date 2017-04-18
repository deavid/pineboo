# # -*- coding: utf-8 -*-
import math
from pineboolib.flcontrols import ProjectClass
from pineboolib import decorators
from pineboolib.qsaglobals import ustr
import pineboolib

from PyQt4 import QtCore
from pineboolib.fllegacy.FLSqlQuery import FLSqlQuery
from pineboolib.fllegacy.FLFieldMetaData import FLFieldMetaData
from pineboolib.fllegacy.FLTableMetaData import FLTableMetaData
import traceback
DisplayRole = QtCore.Qt.DisplayRole 
EditRole = QtCore.Qt.EditRole
Horizontal = QtCore.Qt.Horizontal
Vertical = QtCore.Qt.Vertical
QVariant_invalid = QtCore.QVariant()
QVariant = QtCore.QVariant
QAbstractTableModel_headerData = QtCore.QAbstractTableModel.headerData
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
            self._metadata = project.conn.manager().metadata(self._table.name)
        else:
            raise AssertionError
        self.sql_fields = []
        self.field_aliases = []
        self.field_type = []
        self.field_metaData = []

        # Indices de busqueda segun PK y CK. Los array "pos" guardan las posiciones
        # de las columnas afectadas. PK normalmente valdrá [0,].
        # CK puede ser [] o [2,3,4] por ejemplo.
        # En los IDX tendremos como clave el valor compuesto, en array, de la clave.
        # Como valor del IDX tenemos la posicion de la fila.
        # Si se hace alguna operación en _data como borrar filas intermedias hay
        # que invalidar los indices. Opcionalmente, regenerarlos.
        self.pkpos = []
        self.ckpos = []
        self.pkidx = {}
        self.ckidx = {}
        self.indexes_valid = False # Establecer a False otra vez si el contenido de los indices es erróneo.
        #for field in self._table.fields:
            #if field.visible_grid:
            #self.sql_fields.append(field.name())
            #self.field_metaData.append(field)
        #    self.tableMetadata().addField(field)
        self._data = []
        self._vdata = {}
        self._column_hints = []
        self.cols = len(self.tableMetadata().fieldListObject())
        self.col_aliases = [ str(self.tableMetadata().indexFieldObject(i).alias()) for i in range(self.cols) ]
        self.rows = 0
        self.rowsLoaded = 0
        self.where_filters = {}
        self.refresh()


    def metadata(self):
        #print("CursorTableModel: METADATA: " + self._table.name)
        return self._metadata

    def canFetchMore(self,index):
        ret = self.rows > self.rowsLoaded
        print("canFetchMore: %r" % ret)
        return ret
 
    def fetchMore(self,index):
        ROW_BATCH_COUNT = min(100 + self.rowsLoaded // 10, 5000)
        
        parent = index
        fromrow = self.rowsLoaded
        torow = min(self.rowsLoaded + ROW_BATCH_COUNT, self.rows) - 1
        if torow < fromrow: return
    
        print("refrescando modelo tabla %r , query %r, rows: %d %r" % (self._table.name, self._table.query_table, self.rows, (fromrow,torow)))
        self.beginInsertRows(parent, fromrow, torow)
        #print("QUERY:", sql)
        s_d_ap = self._data.append
        _vd = self._vdata
        for n,row in enumerate(self._cursor):
            n+=fromrow
            
            row = list(row)
            s_d_ap(row)
            #print("row: %d : %d " % (len(self._data),n + 1)) 
            #assert(len(self._data) == n + 1) 
            for r, val in enumerate(row):
                txt = ustr(val)
                ltxt = len(txt)
                if n < 150:
                    newlen = 40 + math.tanh(ltxt/3000.0) * 35000.0
                    self._column_hints[r] =  (self._column_hints[r] * 5 + newlen)/6.0
                _vd[n*1000+r] = QVariant(txt)
            
            self.indexUpdateRow(n)
            if n >= torow: break

            
        self._column_hints = [ int(x) for x in self._column_hints ]
        self.indexes_valid = True
        self.rowsLoaded = torow + 1
        self.endInsertRows()
        print("fin refresco modelo tabla %r , query %r, rows: %d %r" % (self._table.name, self._table.query_table, self.rows, (fromrow,torow)))
        topLeft = self.index(fromrow,0)
        bottomRight = self.index(torow,self.cols-1)
        self.dataChanged.emit(topLeft,bottomRight)
 

    def refresh(self):
        parent = QtCore.QModelIndex()
        oldrows = self.rowsLoaded
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
        # TODO: Convertir esto a un cursor de servidor (hasta 20.000 registros funciona bastante bien)
        if self._table.query_table:
            # FIXME: Como no tenemos soporte para Queries, desactivamos el refresh.
            print("No hay soporte para CursorTableModel con Queries: name %r , query %r" % (self._table.name, self._table.query_table))
            
            return
        self.sql_fields = []
        self.pkpos = []
        self.ckpos = []
        for n,field in enumerate(self.tableMetadata().fieldListObject()):
            #if field.visibleGrid():
            #    sql_fields.append(field.name())
            if field.isPrimaryKey(): self.pkpos.append(n)
            if field.isCompoundKey(): self.ckpos.append(n)

            self.sql_fields.append(field.name())

        sql = """SELECT %s FROM %s WHERE %s """ % (", ".join(self.sql_fields),self.tableMetadata().name(), where_filter)
        self._cursor.execute(sql)
        self.rows = 0
        self.rowsLoaded = 0
        self.endRemoveRows()
        if oldrows > 0:
            self.rowsRemoved.emit(parent, 0, oldrows - 1)
        newrows = self._cursor.rowcount
        #print("rows:", self.rows)
        self.rows = newrows
        self._data = []
        self._column_hints = [120.0] * len(self.sql_fields)
        self.fetchMore(parent)

    def indexUpdateRow(self, rownum):
        row = self._data[rownum]
        if self.pkpos:
            key = tuple([ row[x] for x in self.pkpos ])
            self.pkidx[key] = rownum
        if self.ckpos:
            key = tuple([ row[x] for x in self.ckpos ])
            self.ckidx[key] = rownum

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
    def updateValuesDB(self, pKValue, dict_update):
        row = self.findPKRow([pKValue])
        if row is None:
            raise AssertionError("Los indices del CursorTableModel no devolvieron un registro (%r)" % (pKValue))

        if self.value(row, self.pK()) != pKValue:
            raise AssertionError("Los indices del CursorTableModel devolvieron un registro erroneo: %r != %r" % (self.value(row, self.pK()), pKValue))

        self.setValuesDict(row, dict_update)
        pkey_name = self.tableMetadata().primaryKey()
        # TODO: la conversion de mogrify de bytes a STR va a dar problemas con los acentos...
        typePK_ = self.tableMetadata().field(self.tableMetadata().primaryKey()).type()
        pKValue = self._prj.conn.manager().formatValue(typePK_, pKValue, False)
        #if typePK_ == "string" or typePK_ == "pixmap" or typePK_ == "stringlist" or typePK_ == "time" or typePK_ == "date":
            #pKValue = str("'" + pKValue + "'")
            
        where_filter = "%s = %s" % (pkey_name, pKValue)
        print("pkvalue = %r" % pKValue)
        update_set = []

        for key, value in dict_update.items():
            type_ = self.tableMetadata().field(key).type()
            #if type_ == "string" or type_ == "pixmap" or type_ == "stringlist" or type_ == "time" or type_ == "date":
                #value = str("'" + value + "'")
            value = self._prj.conn.manager().formatValue(type_, value, False)
            #update_set.append("%s = %s" % (key, (self._cursor.mogrify("%s",[value]))))
            update_set.append("%s = %s" % (key, value))
            print("field %r = %r" % (key,value))

        update_set_txt = ", ".join(update_set)
        sql = """UPDATE %s SET %s WHERE %s RETURNING *""" % (self.tableMetadata().name(), update_set_txt, where_filter)
        print("MODIFYING SQL :: ", sql)
        self._cursor.execute(sql)
        returning_fields = [ x[0] for x in self._cursor.description ]

        for orow in self._cursor:
            dict_update = dict(zip(returning_fields, orow))
            self.setValuesDict(row, dict_update)



    """
    Asigna un valor una fila usando un diccionario
    @param row. Columna afectada
    @param update_dict. array clave-valor indicando el listado de claves y valores a actualizar
    """
    @decorators.BetaImplementation
    def setValuesDict(self, row, update_dict):

        print("CursorTableModel.setValuesDict(row %s) = %r" % (row, update_dict))

        try:
            for fieldname,value in update_dict.items():
                col = self.metadata().indexPos(fieldname)
                self._data[row][col] = value
                self._vdata[row*1000+col] = QtCore.QVariant(ustr(value))
            self.indexUpdateRow(row)

        except Exception:

            print("CursorTableModel.setValuesDict(row %s) = %r :: ERROR:" % (row, update_dict), traceback.format_exc())


    """
    Asigna un valor una celda
    @param row. Columna afectada
    @param fieldname. Nonbre de la fila afectada. Se puede obtener la columna con self.metadata().indexPos(fieldname)
    @param value. Valor a asignar. Puede ser texto, pixmap, etc...
    """
    def setValue(self, row, fieldname, value):
        # Reimplementación para que todo pase por el método genérico.
        self.setValuesDict(self, row, { fieldname : value } )

    """
    Crea una nueva linea en el tableModel
    @param buffer . PNBuffer a añadir
    """
    @decorators.NotImplementedWarn
    def newRowFromBuffer(self, buffer):
        pass

    def findPKRow(self, pklist):
        if not isinstance(pklist, (tuple, list)):
            raise ValueError("findPKRow expects a list as first argument. Enclose PK inside brackets [self.pkvalue]")
        if not self.indexes_valid:
            for n in range(self.rows):
                self.indexUpdateRow(n)
            self.indexes_valid = True
        pklist = tuple(pklist)
        if pklist not in self.pkidx:
            print("CursorTableModel.findPKRow:: PK not found: %r (requires list, not integer or string)" % pklist)
            return None
        return self.pkidx[pklist]

    def findCKRow(self, cklist):
        if not isinstance(cklist, (tuple, list)):
            raise ValueError("findCKRow expects a list as first argument.")
        if not self.indexes_valid:
            for n in range(self.rows):
                self.indexUpdateRow(n)
            self.indexes_valid = True
        cklist = tuple(cklist)
        if cklist not in self.ckidx:
            print("CursorTableModel.findCKRow:: CK not found: %r (requires list, not integer or string)" % pklist)
            return None
        return self.ckidx[cklist]


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
        return self.cols
        if parent is None: parent = QtCore.QModelIndex()
        if parent.isValid(): return 0
        #print(self.cols)
        print("colcount", self.cols)
        return self.cols

    def rowCount(self, parent = None):
        return self.rowsLoaded
        if parent is None: parent = QtCore.QModelIndex()
        if parent.isValid(): return 0
        print("rowcount", self.rows)
        return self.rows

    def headerData(self, section, orientation, role):
        if role == DisplayRole:
            if orientation == Horizontal:
                return self.col_aliases[section]
            elif orientation == Vertical:
                return section +1
        return QVariant_invalid
            
        return QAbstractTableModel_headerData(self, section, orientation, role)

    def data(self, index, role):
        row = index.row()
        col = index.column()
        if role == DisplayRole or role == EditRole:
            #if row > self.rowsLoaded: 
            return self._vdata[row*1000+col]
            

        return QVariant_invalid

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




