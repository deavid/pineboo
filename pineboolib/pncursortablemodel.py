# # -*- coding: utf-8 -*-
import math
import traceback
import threading
import logging
import time
import itertools

from pineboolib.utils import filedir
import pineboolib

from PyQt5 import QtCore, QtGui, QtWidgets


DEBUG = False


"""
Esta clase es el enlace entre FLSqlCursor y el SGBD
"""


class PNCursorTableModel(QtCore.QAbstractTableModel):
    logger = logging.getLogger("CursorTableModel")
    rows = 15
    cols = 5
    _cursor_db = None
    _cursorConn = None
    USE_THREADS = False
    USE_TIMER = False
    CURSOR_COUNT = itertools.count()
    rowsLoaded = 0
    where_filters = {}
    _metadata = None
    _sortOrder = None
    _checkColumn = None
    _disable_refresh = None
    color_function_ = None
    color_dict_ = None
    _parent = None
    """
    Constructor
    @param action. action relacionada al cursor
    @param conn. Objeto PNConnection
    """

    def __init__(self, action, conn, parent):
        super(PNCursorTableModel, self).__init__()

        self._action = action
        self._cursorConn = conn
        self._parent = parent
        if self._action.table():
            self._metadata = self._cursorConn.manager().metadata(self._action.table())
        else:
            return

        self.USE_THREADS = self._cursorConn.driver().useThreads()
        self.USE_TIMER = self._cursorConn.driver().useTimer()

        self.rowsLoaded = 0
        self.sql_fields = []
        self.sql_fields_omited = []
        self.sql_fields_without_check = []
        self.field_aliases = []
        self.field_type = []
        self.field_metaData = []
        self.col_aliases = []

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
        self._checkColumn = {}
        # Establecer a False otra vez si el contenido de los indices es erróneo.
        self.indexes_valid = False
        self._data = []
        self._vdata = []
        self._column_hints = []
        self.updateColumnsCount()
        self.rows = 0
        self.rowsLoaded = 0
        self.pendingRows = 0
        self.lastFetch = 0
        self.fetchedRows = 0
        self._showPixmap = True
        self.color_function_ = None
        self.color_dict_ = {}

        self.where_filters = {}
        self.where_filters["main-filter"] = None
        self.where_filters["filter"] = None

        if self.USE_THREADS:
            self.fetchLock = threading.Lock()
            self.threadFetcher = threading.Thread(target=self.threadFetch)
            self.threadFetcherStop = threading.Event()

        if self.USE_TIMER:
            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(self.updateRows)
            self.timer.start(1000)

        self.canFetchMore = True
        self._disable_refresh = False

        self._cursor_db = self._cursorConn.cursor()
        # self.refresh()

    """
    Indica si se pueden recoger mas datos del la tabla
    @return Boolean indicado Sí o No
    """

    def canFetchMore(self, *args):
        return self.canFetchMore

    """
    Desactiva el refresco. Ej. FLSqlQuery.setForwardOnly(True)
    @param disable. True o False
    """

    def disable_refresh(self, disable):
        self._disable_refresh = disable

    """
    Indica el tipo de orden a usar y sobre que columna
    @param col. Columna usada 
    @param order. 0 ASC, 1 DESC
    """

    def sort(self, col, order):
        # order 0 ascendente , 1 descendente
        ord = "ASC"
        if order == 1:
            ord = "DESC"
        self._sortOrder = "%s %s" % (self.metadata().indexFieldObject(col).name(), ord)
        self.refresh()

    """
    Retorna una cadena de texto con el valor de sortOrder
    @return Cadena de texto con información de columna y orden
    """

    def getSortOrder(self):
        return self._sortOrder

    """
    Setea el ORDERBY
    """

    def setSortOrder(self, sO):
        self._sortOrder = sO

    def setColorFunction(self, f):
        self.color_function_ = f

    def dict_color_function(self):
        return self.color_function_
    """
    Retorna información de un registro. Puede ser desde Alineación, color de fondo, valor ... dependiendo del rol
    @param index. Posición del registro
    @param role. Tipo de información solicitada
    @return Inofrmación del objeto solicitada
    """

    def data(self, index, role):
        if self.dict_color_function():
            if not index in self.color_dict_.keys():
                from pineboolib.pncontrolsfactory import aqApp
                field_name = None
                field_value = None
                cursor = self._parent
                selected = False
                type = None

                self.color_dict_[index] = aqApp.call(
                    self.dict_color_function(), [field_name, field_value, cursor, selected, type], None)
        # print("Data ", index, role)
        # print("Registros", self.rowCount())
        # roles
        # 0 QtCore.Qt.DisplayRole
        # 1 QtCore.Qt.DecorationRole
        # 2 QtCore.Qt.EditRole
        # 3 QtCore.Qt.ToolTipRole
        # 4 QtCore.Qt.StatusTipRole
        # 5 QtCore.Qt.WhatThisRole
        # 6 QtCore.Qt.FontRole
        # 7 QtCore.Qt.TextAlignmentRole
        # 8 QtCore.Qt.BackgroundRole
        # 9 QtCore.Qt.ForegroundRole

        row = index.row()
        col = index.column()
        field = self.metadata().indexFieldObject(col)
        _type = field.type()

        if _type is not "check":
            r = [x for x in self._data[row]]
            self._data[row] = r
            d = r[col]
        else:
            pK = str(self.value(row, self.metadata().primaryKey()))
            if not pK in self._checkColumn.keys():
                d = QtWidgets.QCheckBox()
                self._checkColumn[pK] = d

        if role == QtCore.Qt.CheckStateRole and _type == "check":
            if pK in self._checkColumn.keys():
                if self._checkColumn[pK].isChecked():
                    return QtCore.Qt.Checked

            return QtCore.Qt.Unchecked

        if role == QtCore.Qt.TextAlignmentRole:
            if _type in ("int", "double", "uint"):
                d = QtCore.Qt.AlignRight
            elif _type in ("bool", "unlock", "date", "time", "pixmap", "check"):
                d = QtCore.Qt.AlignCenter
            else:
                d = None

            return d

        if role in (QtCore.Qt.DisplayRole, QtCore.Qt.EditRole):
            # r = self._vdata[row]
            if _type is "bool":
                if d in (True, "1"):
                    d = "Sí"
                else:
                    d = "No"

            elif _type in ("unlock", "pixmap"):
                d = None

            elif _type in ("string", "stringlist") and not d:
                d = ""

            elif _type in ("date", "time") and d:
                d = str(d)

            elif _type is "check":
                return

            return d

        if role == QtCore.Qt.DecorationRole:
            icon = None
            if _type == "unlock":

                if d in (True, "1"):
                    icon = QtGui.QIcon(filedir("../share/icons", "unlock.png"))
                else:
                    icon = QtGui.QIcon(filedir("../share/icons", "lock.png"))

            if _type == "pixmap" and self._showPixmap:
                pass

            return icon

        if role == QtCore.Qt.BackgroundRole:
            if _type == "bool":
                if d in (True, "1"):
                    d = QtGui.QBrush(QtCore.Qt.green)
                else:
                    d = QtGui.QBrush(QtCore.Qt.red)

            elif _type == "check":
                d = self._checkColumn[pK]
                if d.isChecked():
                    d = QtGui.QBrush(QtCore.Qt.green)
                else:
                    d = QtGui.QBrush(QtCore.Qt.white)

            else:
                d = None

            return d

        if role == QtCore.Qt.ForegroundRole:
            if _type == "bool":
                if d in (True, "1"):
                    d = QtGui.QBrush(QtCore.Qt.black)
                else:
                    d = QtGui.QBrush(QtCore.Qt.white)
            else:
                d = None

            return d

        return None

    """
    Setea si se muestran los pixmap en el grid de datos
    @param show. Boolean.
    """

    def setShowPixmap(self, show):
        self._showPixmap = show

    """
    Cuando el driver SQL soporta Threa, recoge info de la tabla
    """

    def threadFetch(self):
        if not self.metadata():
            return

        self.refreshFetch(2000)

    """
    Actualiza los registros virtuales que gestiona el modelo
    """

    def updateRows(self):
        if self.USE_THREADS:
            ROW_BATCH_COUNT = 200 if self.threadFetcher.is_alive() else 0
        elif self.USE_TIMER:
            ROW_BATCH_COUNT = 200 if self.timer.isActive() else 0
        else:
            return

        parent = QtCore.QModelIndex()
        fromrow = self.rowsLoaded
        torow = self.fetchedRows - ROW_BATCH_COUNT - 1
        if torow - fromrow < 10:
            return
        if DEBUG:
            self.logger.info("Updaterows %s (UPDATE:%d)", self.metadata().name(), torow - fromrow + 1)

        self.beginInsertRows(parent, fromrow, torow)
        self.rowsLoaded = torow + 1
        self.endInsertRows()
        topLeft = self.index(fromrow, 0)
        bottomRight = self.index(torow, self.cols - 1)
        self.dataChanged.emit(topLeft, bottomRight)

    """
    Recoge nuevos datos del la BD
    @param index. Tableindex padre.
    @param tablename. Nombre de la tabla a recoger datos.
    @param where_filter. Filtro usado para recoger datos.
    """

    def fetchMore(self, index, tablename=None, where_filter=None):
        tiempo_inicial = time.time()
        # ROW_BATCH_COUNT = min(200 + self.rowsLoaded // 10, 1000)
        ROW_BATCH_COUNT = 1000

        parent = index
        fromrow = self.rowsLoaded
        # FIXME: Hay que borrar luego las que no se cargaron al final...
        torow = self.rowsLoaded + ROW_BATCH_COUNT
        if self.fetchedRows - ROW_BATCH_COUNT - 1 > torow:
            torow = self.fetchedRows - ROW_BATCH_COUNT - 1

        # print("refrescando modelo tabla %r , query %r, rows: %d %r" % (self._table.name, self._table.query_table, self.rows, (fromrow,torow)))
        if torow < fromrow:
            return

        # print("QUERY:", sql)
        if self.fetchedRows <= torow and self.canFetchMore:

            if self.USE_THREADS and self.threadFetcher.is_alive():
                self.threadFetcher.join()

            if tablename is None:
                tablename = self.metadata().name()

            if where_filter is None:
                where_filter = self.where_filter
            c_all = self._cursorConn.driver().fetchAll(self.cursorDB(), tablename, where_filter,
                                                       self.sql_str, self._curname)
            newrows = len(c_all)  # self._cursor.rowcount
            from_rows = self.rows
            self._data += c_all
            self._vdata += [None] * newrows
            self.fetchedRows += newrows
            self.rows += newrows
            self.canFetchMore = newrows > 0

            self.pendingRows = 0
            self.indexUpdateRowRange((from_rows, self.rows))
            if self.USE_THREADS is True:
                self.threadFetcher = threading.Thread(target=self.threadFetch)
                self.threadFetcher.start()

        if torow > self.rows - 1:
            torow = self.rows - 1
        if torow < fromrow:
            return
        self.beginInsertRows(parent, fromrow, torow)
        if fromrow == 0:
            data_trunc = self._data[:200]
            for row in data_trunc:
                for r, val in enumerate(row):
                    txt = str(val)
                    ltxt = len(txt)
                    newlen = int(40 + math.tanh(ltxt / 3000.0) * 35000.0)
                    self._column_hints[r] += newlen
            for r in range(len(self._column_hints)):
                self._column_hints[r] /= len(self._data[:200]) + 1
            self._column_hints = [int(x) for x in self._column_hints]

        self.indexes_valid = True
        self.rowsLoaded = torow + 1
        self.endInsertRows()
        # print("fin refresco modelo tabla %r , query %r, rows: %d %r" % (self._table.name, self._table.query_table, self.rows, (fromrow,torow)))
        topLeft = self.index(fromrow, 0)
        bottomRight = self.index(torow, self.cols - 1)
        self.dataChanged.emit(topLeft, bottomRight)
        tiempo_final = time.time()
        self.lastFetch = tiempo_final
        # if self.USE_THREADS == True and not self.threadFetcher.is_alive() and self.pendingRows > 0:
        #    self.threadFetcher = threading.Thread(target=self.threadFetch)
        #    self.threadFetcherStop = threading.Event()
        #    self.threadFetcher.start()

        if tiempo_final - tiempo_inicial > 0.2:
            self.logger.info("fin refresco tabla '%s'  :: rows: %d %r  ::  (%.3fs)", self.metadata().name(),
                             self.rows, (fromrow, torow), tiempo_final - tiempo_inicial)

    """
    Comprueba que los campos referidos en una Query existen. Si algun campo no existe lo marca como a omitir
    @param qry. Query con los campos a usar
    """

    def _refresh_field_info(self, qry):
        for n, field in enumerate(self.metadata().fieldList()):
            # if field.visibleGrid():
            #    sql_fields.append(field.name())
            if field.isPrimaryKey():
                self.pkpos.append(n)
            if field.isCompoundKey():
                self.ckpos.append(n)

            if self.metadata().isQuery():
                found = False
                for table in qry.tablesList():
                    # print("Comprobando %s en %s" % (field.name(), pineboolib.project.conn.manager().metadata(table).fieldList()))
                    if self._cursorConn.manager().metadata(table).field(field.name()):
                        self.sql_fields.append("%s.%s" % (table, field.name()))
                        found = True
                        break
                # Omito los campos que aparentemente no existen
                if not found and not field.name() in self.sql_fields_omited:
                    if pineboolib.project.debugLevel > 50:
                        self.logger.info("CursorTableModel.refresh(): Omitiendo campo '%s' referenciado en query %s. El campo no existe en %s ",
                                         field.name(), self.metadata().name(), qry.tablesList())
                    self.sql_fields_omited.append(field.name())

            else:
                if field.type() != field.Check:
                    self.sql_fields_without_check.append(field.name())

                self.sql_fields.append(field.name())

    """
    Refresca la información que va a gestionar esta clase
    """

    def refresh(self):
        if self._disable_refresh:
            return

        if not self.metadata():
            self.logger.warn("ERROR: CursorTableModel :: No hay tabla",
                             pineboolib.project.tables[self._action.table()].name)
            return

        parent = QtCore.QModelIndex()
        oldrows = self.rowsLoaded
        self.beginRemoveRows(parent, 0, oldrows)
        if self.USE_THREADS is True:
            self.threadFetcherStop.set()
            if self.threadFetcher.is_alive():
                self.threadFetcher.join()

        self.rows = 0
        self.rowsLoaded = 0
        self.fetchedRows = 0
        self.sql_fields = []
        self.sql_fields_without_check = []
        self.pkpos = []
        self.ckpos = []
        self._data = []
        self.endRemoveRows()
        if oldrows > 0:
            self.rowsRemoved.emit(parent, 0, oldrows - 1)
        where_filter = None
        for k, wfilter in sorted(self.where_filters.items()):
            if wfilter is None:
                continue
            wfilter = wfilter.strip()
            if not wfilter:
                continue
            if not where_filter:
                where_filter = wfilter
            elif wfilter not in where_filter:
                where_filter += " AND " + wfilter
        if not where_filter:
            where_filter = "1 = 1"

        self.where_filter = where_filter
        # Si no existe un orderBy y se ha definido uno desde FLTableDB ...
        if self.where_filter.find("ORDER BY") == -1 and self.getSortOrder():
            if self.where_filter.find(";") > -1:  # Si el where termina en ; ...
                self.where_filter = self.where_filter.replace(";", " ORDER BY %s;" % self.getSortOrder())
            else:
                self.where_filter = "%s ORDER BY %s" % (self.where_filter, self.getSortOrder())

        if not self.metadata():
            return

        if self.metadata().isQuery():
            qry = self._cursorConn.manager().query(self.metadata().query())
            from_ = qry.from_()
        else:
            qry = None
            from_ = self.metadata().name()

        self._refresh_field_info(qry)

        self._curname = "cur_%s_%08d" % (self.metadata().name(), next(self.CURSOR_COUNT))

        if self.sql_fields_without_check:
            self.sql_str = ", ".join(self.sql_fields_without_check)
        else:
            self.sql_str = ", ".join(self.sql_fields)

        self._cursorConn.driver().refreshQuery(self._curname, self.sql_str,
                                               from_, self.where_filter, self.cursorDB(), self._cursorConn.db())

        self.refreshFetch(1000)
        self.rows = 0
        self.canFetchMore = True
        # print("rows:", self.rows)
        self.pendingRows = 0

        self._column_hints = [120.0] * len(self.sql_fields)
        # self.threadFetcher = threading.Thread(target=self.threadFetch)
        # self.threadFetcherStop = threading.Event()
        # self.threadFetcher.start()
        self.fetchMore(parent, self.metadata().name(), self.where_filter)
        # print("%s:: rows: %s" % (self._curname, self.rows))

    """
    Recoge info actualizada de la BD de una cierta cantidad de registros
    @param n. Número de registros a recoger
    """

    def refreshFetch(self, n):
        self._cursorConn.driver().refreshFetch(n, self._curname, self.metadata().name(), self.cursorDB(),
                                               self.sql_str, self.where_filter)

    """
    Actualiza el index de la fila, que se usa para localizar registros virtuales del TableModel
    @param rownum. Número de fila
    """

    def indexUpdateRow(self, rownum):
        row = self._data[rownum]
        if self.pkpos:
            key = tuple([row[x] for x in self.pkpos])
            self.pkidx[key] = rownum
        if self.ckpos:
            key = tuple([row[x] for x in self.ckpos])
            self.ckidx[key] = rownum

    """
    Actualiza el index de un rango de filas, que se usan para localizar registros en el tableModel
    @param  rowramge. Array desde:hasta
    """

    def indexUpdateRowRange(self, rowrange):
        rows = self._data[rowrange[0]:rowrange[1]]
        if self.pkpos:
            for n, row in enumerate(rows):
                key = tuple([row[x] for x in self.pkpos])
                self.pkidx[key] = n + rowrange[0]
        if self.ckpos:
            for n, row in enumerate(rows):
                key = tuple([row[x] for x in self.ckpos])
                self.ckidx[key] = n + rowrange[0]

    """
    Devuelve el valor de una columna de una fila determinada
    @param row. Fila
    @param fieldName. Nombre del campo.
    @return Valor contenido
    """

    def value(self, row, fieldName):
        if row is None or row < 0 or row >= self.rows:
            return None
        col = None
        if not self.metadata().isQuery():
            col = self.metadata().indexPos(fieldName)
        else:
            # Comparo con los campos de la qry, por si hay algun hueco que no se detectaria con indexPos
            for x, fQ in enumerate(self.sql_fields):
                if fieldName == fQ[fQ.find(".") + 1:]:
                    col = x
                    break

            if not col:
                return None

        type_ = self.metadata().field(fieldName).type()

        if type_ is "check":
            return

        campo = self._data[row][col]

        if type_ in ("serial", "uint", "int"):
            if campo not in (None, "None"):
                campo = int(campo)
            elif campo == "None":
                self.logger.warnign("Campo no deberia ser un string 'None'")

        return campo

    """
    Actualiza los datos de un registro del tableModel en la BD
    @param pKValue. Pirmary Key del registro a actualizar en la BD
    @param dict_update. Campos que se actualizarán
    """

    def updateValuesDB(self, pKValue, dict_update):
        row = self.findPKRow([pKValue])
        if row is None:
            raise AssertionError(
                "Los indices del CursorTableModel no devolvieron un registro (%r)" % (pKValue))

        if self.value(row, self.pK()) != pKValue:
            raise AssertionError("Los indices del CursorTableModel devolvieron un registro erroneo: %r != %r" % (
                self.value(row, self.pK()), pKValue))

        self.setValuesDict(row, dict_update)
        pkey_name = self.metadata().primaryKey()
        # TODO: la conversion de mogrify de bytes a STR va a dar problemas con los acentos...
        typePK_ = self.metadata().field(self.metadata().primaryKey()).type()
        pKValue = self._cursorConn.manager().formatValue(typePK_, pKValue, False)
        # if typePK_ == "string" or typePK_ == "pixmap" or typePK_ == "stringlist" or typePK_ == "time" or typePK_ == "date":
        # pKValue = str("'" + pKValue + "'")

        where_filter = "%s = %s" % (pkey_name, pKValue)
        update_set = []

        for key, value in dict_update.items():
            type_ = self.metadata().field(key).type()
            # if type_ == "string" or type_ == "pixmap" or type_ == "stringlist" or type_ == "time" or type_ == "date":
            # value = str("'" + value + "'")
            if type_ in ("string", "stringlist"):
                value = self._cursorConn.normalizeValue(value)
            value = self._cursorConn.manager().formatValue(type_, value, False)

            # update_set.append("%s = %s" % (key, (self._cursor.mogrify("%s",[value]))))
            update_set.append("%s = %s" % (key, value))

        if len(update_set) == 0:
            return

        update_set_txt = ", ".join(update_set)
        sql = self._cursorConn.driver().queryUpdate(
            self.metadata().name(), update_set_txt, where_filter)
        # print("MODIFYING SQL :: ", sql)
        try:
            self.cursorDB().execute(sql)
        except Exception as e:
            self.logger.exception("ERROR: CursorTableModel.Update %s:", self.metadata().name())
            # self._cursor.execute("ROLLBACK")
            return

        try:
            returning_fields = [x[0] for x in self.cursorDB().description]

            for orow in self.cursorDB():
                dict_update = dict(zip(returning_fields, orow))
                self.setValuesDict(row, dict_update)

        except Exception:
            self.logger.exception("updateValuesDB: Error al assignar los valores de vuelta al buffer")

    """
    Asigna un valor una fila usando un diccionario
    @param row. Columna afectada
    @param update_dict. array clave-valor indicando el listado de claves y valores a actualizar
    """

    def setValuesDict(self, row, update_dict):

        if DEBUG:
            self.logger.info("CursorTableModel.setValuesDict(row %s) = %r", row, update_dict)

        try:
            if isinstance(self._data[row], tuple):
                self._data[row] = list(self._data[row])
            r = self._vdata[row]
            if r is None:
                r = [str(x) for x in self._data[row]]
                self._vdata[row] = r
            colsnotfound = []
            for fieldname, value in update_dict.items():
                # col = self.metadata().indexPos(fieldname)
                try:
                    col = self.sql_fields.index(fieldname)
                    self._data[row][col] = value
                    r[col] = value
                except ValueError:
                    colsnotfound.append(fieldname)
            if colsnotfound:
                self.logger.warn("CursorTableModel.setValuesDict:: columns not found: %r", colsnotfound)
            self.indexUpdateRow(row)

        except Exception as e:

            self.logger.exception("CursorTableModel.setValuesDict(row %s) = %r :: ERROR:", row, update_dict)

    """
    Asigna un valor una celda
    @param row. Columna afectada
    @param fieldname. Nonbre de la fila afectada. Se puede obtener la columna con self.metadata().indexPos(fieldname)
    @param value. Valor a asignar. Puede ser texto, pixmap, etc...
    """

    def setValue(self, row, fieldname, value):
        # Reimplementación para que todo pase por el método genérico.
        self.setValuesDict(self, row, {fieldname: value})

    """
    Crea una nueva linea en el tableModel
    @param buffer . PNBuffer a añadir
    """

    def Insert(self, cursor):
        # Metemos lineas en la tabla de la bd
        pKValue = None
        buffer = cursor.buffer()
        campos = None
        valores = None
        for b in buffer.fieldsList():
            value = None
            if buffer.value(b.name) is None:
                value = cursor.metadata().field(b.name).defaultValue()
            else:
                value = buffer.value(b.name)

            if value is not None:  # si el campo se rellena o hay valor default
                if b.name == cursor.metadata().primaryKey():
                    pKValue = value
                if b.type_ in ("string", "stringlist") and isinstance(value, str):

                    value = self._cursorConn.normalizeValue(value)
                value = self._cursorConn.manager().formatValue(b.type_, value, False)
                if not campos:
                    campos = b.name
                    valores = value
                else:
                    campos = u"%s,%s" % (campos, b.name)
                    valores = u"%s,%s" % (valores, value)
        if campos:
            sql = """INSERT INTO %s (%s) VALUES (%s)""" % (buffer.cursor_.d.curName_, campos, valores)
            # conn = self._cursorConn.db()
            try:
                # print(sql)
                self.cursorDB().execute(sql)
                # self.refresh()
                if pKValue is not None:
                    cursor.move(self.findPKRow((pKValue, )))
            except Exception as e:
                self.logger.exception("CursorTableModel.%s.Insert() :: ERROR:", self.metadata().name())
                # self._cursor.execute("ROLLBACK")
                return False

            # conn.commit()

            return True

    """
    Borra una linea en el tableModel
    @param cursor . Objecto FLSqlCursor
    """

    def Delete(self, cursor):
        pKName = self.metadata().primaryKey()
        typePK = self.metadata().field(pKName).type()
        tableName = self.metadata().name()
        val = self._cursorConn.manager().formatValue(typePK, self.value(cursor.d._currentregister, pKName))
        sql = "DELETE FROM %s WHERE %s = %s" % (tableName, pKName, val)
        # conn = self._cursorConn.db()
        try:
            self.cursorDB().execute(sql)
        except Exception as e:
            self.logger.exception("CursorTableModel.%s.Delete() :: ERROR:", self.metadata().name())
            # self._cursor.execute("ROLLBACK")
            return

        # conn.commit()
        self.refresh()

    """
    Delvuelve el index de un registro a raíz de Su Primary Key
    @param pklist. Lista con la PK a encontrar. Hay que meterno entre [] aunque solo sea un registro.
    @return index de la linea buscada
    """

    def findPKRow(self, pklist):
        if not isinstance(pklist, (tuple, list)):
            raise ValueError(
                "findPKRow expects a list as first argument. Enclose PK inside brackets [self.pkvalue]")
        if not self.indexes_valid:
            for n in range(self.rows):
                self.indexUpdateRow(n)
            self.indexes_valid = True

        pklist = tuple(pklist)

        if pklist not in self.pkidx:
            self.logger.info(
                "CursorTableModel.%s.findPKRow:: PK not found: %r", self.metadata().name(), pklist)
            return None
        return self.pkidx[pklist]

    """
    Delvuelve el index de un registro a raíz de Su Composed Key
    @param cklist. Lista con la CK a encontrar.
    @return index de la linea buscada
    """

    def findCKRow(self, cklist):
        if not isinstance(cklist, (tuple, list)):
            raise ValueError("findCKRow expects a list as first argument.")
        if not self.indexes_valid:
            for n in range(self.rows):
                self.indexUpdateRow(n)
            self.indexes_valid = True
        cklist = tuple(cklist)
        if cklist not in self.ckidx:
            self.logger.warn(
                "CursorTableModel.%s.findCKRow:: CK not found: %r ", self.metadata().name(), cklist)
            return None
        return self.ckidx[cklist]

    """
    Devuelve el nombre del campo que es PK
    @return nombre del campo PK
    """

    def pK(self):
        return self.metadata().primaryKey()

    """
    Devuelve el tipo de un campo determinado
    @param fieldName. Nombre del campo
    @return Tipo de campo
    """

    def fieldType(self, fieldName):
        field = self.metadata().field(fieldName)
        return field.type() if field else None

    """
    Devuelve el alias de un campo determinado
    @param fieldName. Nombre del campo
    @return alias del campo
    """

    def alias(self, fieldName):
        field = self.metadata().field(fieldName)
        return field.alias() if field else None

    """
    Devuelve el número de columnas
    @return Número de columnas
    """

    def columnCount(self, *args):
        return self.cols

    """
    Actualiza el número de columnas existentes en el tableModel
    """

    def updateColumnsCount(self):
        self.cols = len(self.metadata().fieldList())
        self.loadColAliases()
        if self.metadata().isQuery():
            qry = self._cursorConn.manager().query(self.metadata().query())
        else:
            qry = None
        self._refresh_field_info(qry)

    """
    Devuelve el número de lineas
    @return Número de lineas
    """

    def rowCount(self, parent=None):
        return self.rowsLoaded

    """
    Devuelve datos de la cebecera
    @param section. Columna
    @param orientation. Horizontal, Vertical
    @param role. Solo es util QtCore.Qt.DisplayRole, El resto de roles es omitido por headerData
    @return info segun sección, orientación y rol.
    """

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                if not self.col_aliases:
                    self.loadColAliases()
                return self.col_aliases[section]
            elif orientation == QtCore.Qt.Vertical:
                return section + 1
        return None

    """
    Carga los alias de las diferentes columnas.
    """

    def loadColAliases(self):
        self.col_aliases = [str(self.metadata().indexFieldObject(i).alias()) for i in range(self.cols)]

    """
    Devuelve el FLFieldMetadata de un campo
    @param fieldName. Nombre del campo
    @return FLFieldMetadata
    """

    def fieldMetadata(self, fieldName):
        return self.metadata().field(fieldName)

    """
    Devuelve el FLTableMetaData de este tableModel
    @return Objeto FLTableMetaData
    """

    def metadata(self):
        return self._metadata

    """
    Devuelve el cursor a la BD usado
    @return Objeto cursor
    """

    def cursorDB(self):
        return self._cursor_db
