# # -*- coding: utf-8 -*-
import math
import threading
import time
import itertools
import locale
from datetime import date

from PyQt5 import QtCore, QtGui, Qt  # type: ignore
from PyQt5.QtCore import pyqtSignal  # type: ignore
from PyQt5 import QtWidgets  # type: ignore  # FIXME: Not allowed here! this is for QCheckBox but it's not needed

from pineboolib.core.utils.utils_base import filedir
from pineboolib.core.utils import logging
from pineboolib.application.utils.date_conversion import date_amd_to_dma
from typing import Any, Iterable, Optional, Union, List, Dict, Tuple, cast, TYPE_CHECKING

if TYPE_CHECKING:
    from pineboolib.application.metadata.pnfieldmetadata import PNFieldMetaData  # noqa: F401
    from pineboolib.application.metadata.pntablemetadata import PNTableMetaData  # noqa: F401
    from pineboolib.application.database.pnsqlcursor import PNSqlCursor  # noqa: F401
    from pineboolib.application.database.pnsqlquery import PNSqlQuery  # noqa: F401
    from pineboolib.interfaces.iconnection import IConnection
    from pineboolib.interfaces.iapicursor import IApiCursor

DEBUG = False


class PNCursorTableModel(QtCore.QAbstractTableModel):
    """
    Esta clase es el enlace entre FLSqlCursor y el SGBD
    """

    logger = logging.getLogger("CursorTableModel")
    rows = 15
    cols = 5
    USE_THREADS = False
    USE_TIMER = True
    CURSOR_COUNT = itertools.count()
    rowsLoaded = 0
    where_filter: str
    where_filters: Dict[str, str] = {}
    _metadata = None
    _sortOrder = ""
    _disable_refresh = None
    color_function_ = None
    need_update = False
    _driver_sql = None
    _size = None
    parent_view: Optional[QtWidgets.QTableView]  # type is FLDatatable
    sql_str = ""
    canFetchMoreRows: bool
    _initialized: Optional[
        bool
    ] = None  # Usa 3 estado None, True y False para hacer un primer refresh retardado si pertenece a un fldatatable

    def __init__(self, conn: "IConnection", parent: "PNSqlCursor") -> None:
        """
        Constructor
        @param conn. Objeto PNConnection
        @param parent. FLSqlCursor relacionado
        """
        super(PNCursorTableModel, self).__init__()
        if parent is None:
            raise ValueError("Parent is mandatory")
        self._cursorConn = conn
        self._parent: "PNSqlCursor" = parent
        self.parent_view = None

        # self._metadata = self._parent.metadata()
        if not self.metadata():
            return

        self._driver_sql = self.db().driver()
        self.USE_THREADS = self.driver_sql().useThreads()
        self.USE_TIMER = self.driver_sql().useTimer()
        if self.USE_THREADS and self.USE_TIMER:
            self.USE_TIMER = False
            self.logger.warning("SQL Driver supports Threads and Timer, defaulting to Threads")

        if not self.USE_THREADS and not self.USE_TIMER:
            self.USE_TIMER = True
            self.logger.warning("SQL Driver supports neither Threads nor Timer, defaulting to Timer")
        self.USE_THREADS = False
        self.USE_TIMER = True
        self.rowsLoaded = 0
        self.sql_fields: List[str] = []
        self.sql_fields_omited: List[str] = []
        self.sql_fields_without_check: List[str] = []
        # self.field_aliases = []
        # self.field_type = []
        # self.field_metaData = []
        self.col_aliases: List[str] = []

        # Indices de busqueda segun PK y CK. Los array "pos" guardan las posiciones
        # de las columnas afectadas. PK normalmente valdrá [0,].
        # CK puede ser [] o [2,3,4] por ejemplo.
        # En los IDX tendremos como clave el valor compuesto, en array, de la clave.
        # Como valor del IDX tenemos la posicion de la fila.
        # Si se hace alguna operación en _data como borrar filas intermedias hay
        # que invalidar los indices. Opcionalmente, regenerarlos.
        self.pkpos: List[int] = []
        self.ckpos: List[int] = []
        self.pkidx: Dict[Tuple, int] = {}
        self.ckidx: Dict[Tuple, int] = {}
        self._checkColumn: Dict[str, Any] = {}
        # Establecer a False otra vez si el contenido de los indices es erróneo.
        self.indexes_valid = False
        self._data: List[List[Any]] = []
        self._vdata: List[Optional[List[Any]]] = []
        self._column_hints: List[int] = []
        self.updateColumnsCount()
        self.rows = 0
        self.rowsLoaded = 0
        self.pendingRows = 0
        self.lastFetch = 0.0
        self.fetchedRows = 0
        self._showPixmap = True
        self.color_function_ = None
        # self.color_dict_ = {}

        self.where_filter = "1=1"
        self.where_filters = {}
        self.where_filters["main-filter"] = ""
        self.where_filters["filter"] = ""
        self.sql_str = ""

        if self.USE_THREADS:
            self.fetchLock = threading.Lock()
            self.threadFetcher = threading.Thread(target=self.threadFetch)
            self.threadFetcherStop = threading.Event()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateRows)
        self.timer.start(1000)

        self.canFetchMoreRows = True
        self._disable_refresh = False

        self._cursor_db: IApiCursor = self.db().cursor()
        self._initialized = None
        # self.refresh()

    def disable_refresh(self, disable: bool) -> None:
        """
        Desactiva el refresco. Ej. FLSqlQuery.setForwardOnly(True)
        @param disable. True o False
        """
        self._disable_refresh = disable

    def sort(self, column: int, order: QtCore.Qt.SortOrder = QtCore.Qt.AscendingOrder) -> None:
        """
        Indica el tipo de orden a usar y sobre que columna
        @param col. Columna usada
        @param order. 0 ASC, 1 DESC
        """
        col = column
        # order 0 ascendente , 1 descendente
        ord = "ASC"
        if order == 1:
            ord = "DESC"

        field_mtd = self.metadata().indexFieldObject(col)
        if field_mtd.type() == "check":
            return

        col_name = field_mtd.name()

        order_list: List[str] = []
        found_ = False
        if self._sortOrder:
            for column_name in self._sortOrder.split(","):
                if col_name in column_name and ord in column_name:
                    found_ = True
                    order_list.append("%s %s" % (col_name, ord))
                else:
                    order_list.append(column_name)

            if not found_:
                self.logger.debug(
                    "%s. Se intenta ordernar por una columna (%s) que no está definida en el order by previo (%s). "
                    "El order by previo se perderá" % (__name__, col_name, self._sortOrder)
                )
            else:
                self._sortOrder = ",".join(order_list)

        if not found_:
            self._sortOrder = "%s %s" % (col_name, ord)
            self.refresh()

    def getSortOrder(self) -> Any:
        """
        Retorna una cadena de texto con el valor de sortOrder
        @return Cadena de texto con información de columna y orden
        """
        return self._sortOrder

    def setSortOrder(self, sort_order: Union[List[str], str]) -> None:
        """
        Setea el ORDERBY
        """
        self._sortOrder = ""
        if isinstance(sort_order, list):
            self._sortOrder = ",".join(sort_order)

        else:
            self._sortOrder = sort_order

    # def setColorFunction(self, f):
    #    self.color_function_ = f

    # def dict_color_function(self):
    #    return self.color_function_

    def data(self, index: QtCore.QModelIndex, role: int = QtCore.Qt.DisplayRole) -> Any:
        """ (overload of QAbstractTableModel)
        Retorna información de un registro. Puede ser desde Alineación, color de fondo, valor ... dependiendo del rol
        @param index. Posición del registro
        @param role. Tipo de información solicitada
        @return Inofrmación del objeto solicitada
        """
        row = index.row()
        col = index.column()
        field = self.metadata().indexFieldObject(col)
        _type = field.type()
        res_color_function: List[str] = []

        if _type != "check":
            r = [x for x in self._data[row]]
            self._data[row] = r
            d = r[col]
        else:
            pK = str(self.value(row, self.metadata().primaryKey()))
            if pK not in self._checkColumn.keys():
                d = QtWidgets.QCheckBox()  # FIXME: Not allowed here. This is GUI. This can be emulated with TRUE/FALSE
                self._checkColumn[pK] = d

        if self.parent_view and role in [QtCore.Qt.BackgroundRole, QtCore.Qt.ForegroundRole]:
            fun_get_color, iface = self.parent_view.functionGetColor()
            if fun_get_color is not None:
                context_ = None
                fun_name_ = None
                if fun_get_color.find(".") > -1:
                    list_ = fun_get_color.split(".")
                    import pineboolib.qsa as qsa_tree

                    qsa_widget = getattr(qsa_tree, list_[0], None)
                    fun_name_ = list_[1]
                    if qsa_widget:
                        context_ = qsa_widget.iface
                else:
                    context_ = iface
                    fun_name_ = fun_get_color

                function_color = getattr(context_, fun_name_, None)
                if function_color is not None:
                    field_name = field.name()
                    field_value = d
                    cursor = self._parent
                    selected = False
                    res_color_function = function_color(field_name, field_value, cursor, selected, _type)
                else:
                    raise Exception("No se ha resuelto functionGetColor %s desde %s" % (fun_get_color, context_))
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

        if role == QtCore.Qt.CheckStateRole and _type == "check":
            if pK in self._checkColumn.keys():
                if self._checkColumn[pK].isChecked():
                    return QtCore.Qt.Checked

            return QtCore.Qt.Unchecked

        elif role == QtCore.Qt.TextAlignmentRole:
            d = QtCore.Qt.AlignVCenter
            if _type in ("int", "double", "uint"):
                d = d | QtCore.Qt.AlignRight
            elif _type in ("bool", "date", "time"):
                d = d | QtCore.Qt.AlignCenter
            elif _type in ("unlock", "pixmap"):
                d = d | QtCore.Qt.AlignHCenter

            return d

        elif role in (QtCore.Qt.DisplayRole, QtCore.Qt.EditRole):
            # r = self._vdata[row]
            if _type == "bool":
                if d in (True, "1"):
                    d = "Sí"
                else:
                    d = "No"

            elif _type in ("unlock", "pixmap"):

                d = None

            elif _type in ("string", "stringlist") and not d:
                d = ""

            elif _type == "time" and d:
                d = str(d)

            elif _type == "date":
                # Si es str lo paso a datetime.date
                if d and isinstance(d, str):
                    if len(d.split("-")[0]) == 4:
                        d = date_amd_to_dma(d)

                    if d:
                        list_ = d.split("-")
                        d = date(int(list_[2]), int(list_[1]), int(list_[0]))

                if d and isinstance(d, date):
                    # Cogemos el locale para presentar lo mejor posible la fecha
                    try:
                        locale.setlocale(locale.LC_TIME, "")
                        date_format = locale.nl_langinfo(locale.D_FMT)
                        date_format = date_format.replace("y", "Y")  # Año con 4 dígitos
                        date_format = date_format.replace("/", "-")  # Separadores
                        d = d.strftime(date_format)
                    except AttributeError:
                        import platform

                        self.logger.warning("locale specific date format is not yet implemented for %s", platform.system())

            elif _type == "check":
                return

            elif _type == "double":
                if d is not None:
                    d = QtCore.QLocale.system().toString(float(d), "f", field.partDecimal())
            elif _type in ("int", "uint"):
                if d is not None:
                    d = QtCore.QLocale.system().toString(int(d))
            if self.parent_view is not None:
                self.parent_view.resize_column(col, d)

            return d

        elif role == QtCore.Qt.DecorationRole:
            pixmap = None
            if _type in ("unlock", "pixmap"):

                if _type == "unlock":
                    if d in (True, "1"):
                        pixmap = QtGui.QPixmap(filedir("../share/icons", "unlock.png"))
                    else:
                        pixmap = QtGui.QPixmap(filedir("../share/icons", "lock.png"))
                    if self.parent_view is not None:
                        if self.parent_view.showAllPixmap() or row == self.parent_view.cursor().at():
                            if pixmap and not pixmap.isNull() and self.parent_view:

                                row_height = self.parent_view.rowHeight(row)  # Altura row
                                row_width = self.parent_view.columnWidth(col)
                                new_pixmap = QtGui.QPixmap(row_width, row_height)  # w , h
                                center_width = (row_width - pixmap.width()) / 2
                                center_height = (row_height - pixmap.height()) / 2
                                new_pixmap.fill(QtCore.Qt.transparent)
                                painter = Qt.QPainter(new_pixmap)
                                painter.drawPixmap(center_width, center_height, pixmap.width(), pixmap.height(), pixmap)

                                pixmap = new_pixmap

                else:
                    if self.parent_view is not None:
                        if self.parent_view and self.parent_view.showAllPixmap():
                            if not self.db().manager().isSystemTable(self._parent.table()):
                                d = self.db().manager().fetchLargeValue(d)
                            else:
                                from pineboolib.application.utils.xpm import cacheXPM

                                d = cacheXPM(d)
                            if d:
                                pixmap = QtGui.QPixmap(d)

            return pixmap

        elif role == QtCore.Qt.BackgroundRole:
            if _type == "bool":
                if d in (True, "1"):
                    d = QtGui.QBrush(QtCore.Qt.green)
                else:
                    d = QtGui.QBrush(QtCore.Qt.red)

            elif _type == "check":
                obj_ = self._checkColumn[pK]
                if obj_.isChecked():
                    d = QtGui.QBrush(QtCore.Qt.green)
                else:
                    d = QtGui.QBrush(QtCore.Qt.white)

            else:
                if res_color_function and len(res_color_function) and res_color_function[0] != "":
                    color_ = QtGui.QColor(res_color_function[0])
                    style_ = getattr(QtCore.Qt, res_color_function[2], None)
                    d = QtGui.QBrush(color_)
                    d.setStyle(style_)
                else:
                    d = None

            return d

        elif role == QtCore.Qt.ForegroundRole:
            if _type == "bool":
                if d in (True, "1"):
                    d = QtGui.QBrush(QtCore.Qt.black)
                else:
                    d = QtGui.QBrush(QtCore.Qt.white)
            else:
                if res_color_function and len(res_color_function) and res_color_function[1] != "":
                    color_ = QtGui.QColor(res_color_function[1])
                    style_ = getattr(QtCore.Qt, res_color_function[2], None)
                    d = QtGui.QBrush(color_)
                    d.setStyle(style_)
                else:
                    d = None

            return d

        # else:
        #    print("role desconocido", role)

        return None

    """
    Cuando el driver SQL soporta Thread, recoge info de la tabla
    """

    def threadFetch(self) -> None:
        if not self.metadata():
            return

        self.refreshFetch(2000)

    """
    Actualiza los registros virtuales que gestiona el modelo
    """

    def updateRows(self) -> None:
        if self.USE_THREADS:
            ROW_BATCH_COUNT = 200 if self.threadFetcher.is_alive() else 0
        elif self.USE_TIMER:
            ROW_BATCH_COUNT = 200 if self.timer.isActive() else 0
        else:
            return

        parent = QtCore.QModelIndex()
        fromrow = self.rowsLoaded
        torow = self.fetchedRows - ROW_BATCH_COUNT - 1
        if torow - fromrow < 5:
            if self.canFetchMoreRows:
                self.logger.trace("Updaterows %s (updated:%d)", self.metadata().name(), self.fetchedRows)
                self.fetchMore(parent, self.metadata().name(), self.where_filter)
            return

        self.logger.trace("Updaterows %s (UPDATE:%d)", self.metadata().name(), torow - fromrow + 1)

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

    def fetchMore(
        self, index: QtCore.QModelIndex, tablename: Optional[str] = None, where_filter: Optional[str] = None, size_hint: int = 1000
    ) -> None:
        if not self.sql_str:
            return

        tiempo_inicial = time.time()
        # ROW_BATCH_COUNT = min(200 + self.rowsLoaded // 10, 1000)
        ROW_BATCH_COUNT = size_hint

        parent = index
        fromrow = self.rowsLoaded
        # FIXME: Hay que borrar luego las que no se cargaron al final...
        torow = self.rowsLoaded + ROW_BATCH_COUNT
        if self.fetchedRows - ROW_BATCH_COUNT - 1 > torow:
            torow = self.fetchedRows - ROW_BATCH_COUNT - 1
        if tablename is None:
            tablename = self.metadata().name()

        self.logger.trace("refrescando modelo tabla %r, rows: %d %r" % (tablename, self.rows, (fromrow, torow)))
        if torow < fromrow:
            return

        # print("QUERY:", sql)
        if self.fetchedRows <= torow and self.canFetchMoreRows:

            if self.USE_THREADS and self.threadFetcher.is_alive():
                self.threadFetcher.join()

            if where_filter is None:
                where_filter = self.where_filter

            c_all = self.driver_sql().fetchAll(self.cursorDB(), tablename, where_filter, self.sql_str, self._curname)
            newrows = len(c_all)  # self._cursor.rowcount
            from_rows = self.rows
            self._data += c_all
            self._vdata += [None] * newrows
            self.fetchedRows += newrows
            self.rows += newrows
            self.canFetchMoreRows = bool(newrows > 0)
            self.logger.trace("refrescando modelo tabla %r, new rows: %d  fetched: %d", tablename, newrows, self.fetchedRows)
            if not self.USE_THREADS:
                self.refreshFetch(ROW_BATCH_COUNT)

            self.pendingRows = 0
            self.indexUpdateRowRange((from_rows, self.rows))
            # if self.USE_THREADS is True:
            #     self.threadFetcher = threading.Thread(target=self.threadFetch)
            #     self.threadFetcher.start()

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
                self._column_hints[r] = int(self._column_hints[r] // (len(self._data[:200]) + 1))
            # self._column_hints = [int(x) for x in self._column_hints]

        self.indexes_valid = True
        self.rowsLoaded = torow + 1
        self.endInsertRows()
        # print("fin refresco modelo tabla %r , query %r, rows: %d %r"
        #        % (self._table.name, self._table.query_table, self.rows, (fromrow,torow)))
        topLeft = self.index(fromrow, 0)
        bottomRight = self.index(torow, self.cols - 1)
        self.dataChanged.emit(topLeft, bottomRight)
        tiempo_final = time.time()
        self.lastFetch = tiempo_final
        if self.USE_THREADS and not self.threadFetcher.is_alive() and self.canFetchMoreRows:
            self.threadFetcher = threading.Thread(target=self.threadFetch)
            self.threadFetcherStop = threading.Event()
            self.threadFetcher.start()

        if tiempo_final - tiempo_inicial > 0.2:
            self.logger.info(
                "fin refresco tabla '%s'  :: rows: %d %r  ::  (%.3fs)",
                self.metadata().name(),
                self.rows,
                (fromrow, torow),
                tiempo_final - tiempo_inicial,
            )

    """
    Comprueba que los campos referidos en una Query existen. Si algun campo no existe lo marca como a omitir
    @param qry. Query con los campos a usar
    """

    def _refresh_field_info(self) -> None:
        is_query = self.metadata().isQuery()
        qry_tables = []
        qry = None
        # if qry is None:
        #    return
        if is_query:
            qry = self.db().manager().query(self.metadata().query())
            if qry is None:
                raise Exception(" The query %s return empty value" % self.metadata().query())
            qry_select = [x.strip() for x in (qry.select()).split(",")]
            qry_fields: Dict[str, str] = {fieldname.split(".")[-1]: fieldname for fieldname in qry_select}

            for table in qry.tablesList():
                mtd = self.db().manager().metadata(table, True)
                if mtd:
                    qry_tables.append((table, mtd))

        for n, field in enumerate(self.metadata().fieldList()):
            # if field.visibleGrid():
            #    sql_fields.append(field.name())
            if field.isPrimaryKey():
                self.pkpos.append(n)
            if field.isCompoundKey():
                self.ckpos.append(n)

            if is_query:
                if field.name() in qry_fields:
                    self.sql_fields.append(qry_fields[field.name()])
                else:
                    found = False
                    for table, mtd in qry_tables:
                        if field.name() in mtd.fieldNames():
                            self.sql_fields.append("%s.%s" % (table, field.name()))
                            found = True
                            break
                    # Omito los campos que aparentemente no existen
                    if not found and not field.name() in self.sql_fields_omited:

                        if qry is None:
                            raise Exception("The qry is empty!")

                        # NOTE: Esto podría ser por ejemplo porque no entendemos los campos computados.
                        self.logger.error(
                            "CursorTableModel.refresh(): Omitiendo campo '%s' referenciado en query %s. El campo no existe en %s ",
                            field.name(),
                            self.metadata().name(),
                            qry.tablesList(),
                        )
                        self.sql_fields_omited.append(field.name())

            else:
                if field.type() != field.Check:
                    self.sql_fields_without_check.append(field.name())

                self.sql_fields.append(field.name())

    """
    Refresca la información que va a gestionar esta clase
    """

    def refresh(self) -> None:
        if self._initialized is None and self.parent_view:  # Si es el primer refresh y estoy conectado a un FLDatatable()
            self._initialized = True
            QtCore.QTimer.singleShot(1, self.refresh)
            return

        if self._initialized:  # Si estoy inicializando y no me ha enviado un sender, cancelo el refesh
            obj = self.sender()
            if not obj:
                return

        self._initialized = False

        if self._disable_refresh and self.rows > 0:
            return

        if not self.metadata():
            self.logger.warning("ERROR: CursorTableModel :: No hay tabla %s", self.metadata().name())
            return

        """ FILTRO WHERE """
        where_filter = ""
        for k, wfilter in sorted(self.where_filters.items()):
            # if wfilter is None:
            #     continue
            wfilter = wfilter.strip()

            if not wfilter:
                continue
            if not where_filter:
                where_filter = wfilter
            elif wfilter not in where_filter:
                if where_filter not in wfilter:
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
        """ FIN """

        parent = QtCore.QModelIndex()
        oldrows = self.rowsLoaded
        self.beginRemoveRows(parent, 0, oldrows)
        if self.USE_THREADS:
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
            cast(pyqtSignal, self.rowsRemoved).emit(parent, 0, oldrows - 1)

        if self.metadata().isQuery():
            query = self.db().manager().query(self.metadata().query())
            if query is None:
                raise Exception("query is empty!")
            from_ = query.from_()
        else:
            from_ = self.metadata().name()

        self._refresh_field_info()

        self._curname = "cur_%s_%08d" % (self.metadata().name(), next(self.CURSOR_COUNT))
        if self.sql_fields_without_check:
            self.sql_str = ", ".join(self.sql_fields_without_check)
        else:
            self.sql_str = ", ".join(self.sql_fields)

        SZ_FETCH = max(1000, oldrows)
        self.driver_sql().refreshQuery(self._curname, self.sql_str, from_, self.where_filter, self.cursorDB(), self.db().db())

        self.refreshFetch(SZ_FETCH)
        self.need_update = False
        self.rows = 0
        self.canFetchMoreRows = True
        # print("rows:", self.rows)
        self.pendingRows = 0

        self._column_hints = [120] * len(self.sql_fields)
        # self.threadFetcher = threading.Thread(target=self.threadFetch)
        # self.threadFetcherStop = threading.Event()
        # self.threadFetcher.start()
        # self.color_dict_.clear()  # Limpiamos diccionario de colores
        self.fetchMore(parent, self.metadata().name(), self.where_filter, size_hint=SZ_FETCH)
        # print("%s:: rows: %s" % (self._curname, self.rows))

    """
    Recoge info actualizada de la BD de una cierta cantidad de registros
    @param n. Número de registros a recoger
    """

    def refreshFetch(self, n: int) -> None:
        self.driver_sql().refreshFetch(n, self._curname, self.metadata().name(), self.cursorDB(), self.sql_str, self.where_filter)

    """
    Actualiza el index de la fila, que se usa para localizar registros virtuales del TableModel
    @param rownum. Número de fila
    """

    def indexUpdateRow(self, rownum: int) -> None:
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

    def indexUpdateRowRange(self, rowrange: Tuple[int, int]) -> None:
        rows = self._data[rowrange[0] : rowrange[1]]
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

    def value(self, row: Optional[int], fieldName: str) -> Any:
        if row is None or row < 0 or row >= self.rows:
            return None
        col = None
        if not self.metadata().isQuery():
            col = self.metadata().indexPos(fieldName)
        else:
            # Comparo con los campos de la qry, por si hay algun hueco que no se detectaria con indexPos
            for x, fQ in enumerate(self.sql_fields):
                if fieldName == fQ[fQ.find(".") + 1 :]:
                    col = x
                    break

            if not col:
                return None
        mtdfield = self.metadata().field(fieldName)
        if mtdfield is None:
            raise Exception("fieldName: %s not found" % fieldName)
        type_ = mtdfield.type()

        if type_ == "check":
            return None

        campo = self._data[row][col]

        if type_ in ("serial", "uint", "int"):
            if campo not in (None, "None"):
                campo = int(campo)
            elif campo == "None":
                self.logger.warning("Campo no deberia ser un string 'None'")

        return campo

    """
    Actualiza los datos de un registro del tableModel en la BD
    @param pKValue. Pirmary Key del registro a actualizar en la BD
    @param dict_update. Campos que se actualizarán
    """

    def updateValuesDB(self, pKValue: Any, dict_update: Dict[str, Any]) -> bool:
        self.logger.trace("updateValuesDB: init: pKValue %s, dict_update %s", pKValue, dict_update)
        row = self.findPKRow([pKValue])
        # if row is None:
        #    raise AssertionError(
        #        "Los indices del CursorTableModel no devolvieron un registro (%r)" % (pKValue))
        if row is None:
            return False

        if self.value(row, self.pK()) != pKValue:
            raise AssertionError(
                "Los indices del CursorTableModel devolvieron un registro erroneo: %r != %r" % (self.value(row, self.pK()), pKValue)
            )

        self.setValuesDict(row, dict_update)
        pkey_name = self.metadata().primaryKey()
        # TODO: la conversion de mogrify de bytes a STR va a dar problemas con los acentos...
        mtdfield = self.metadata().field(pkey_name)
        if mtdfield is None:
            raise Exception("Primary Key %s not found" % pkey_name)
        typePK_ = mtdfield.type()
        pKValue = self.db().manager().formatValue(typePK_, pKValue, False)
        # if typePK_ == "string" or typePK_ == "pixmap" or typePK_ == "stringlist" or typePK_ == "time" or typePK_ == "date":
        # pKValue = str("'" + pKValue + "'")

        where_filter = "%s = %s" % (pkey_name, pKValue)
        update_set = []

        for key, value in dict_update.items():
            mtdfield = self.metadata().field(key)
            if mtdfield is None:
                raise Exception("Field %s not found" % key)
            type_ = mtdfield.type()
            # if type_ == "string" or type_ == "pixmap" or type_ == "stringlist" or type_ == "time" or type_ == "date":
            # value = str("'" + value + "'")
            if type_ in ("string", "stringlist"):
                value = self.db().normalizeValue(value)
            value = self.db().manager().formatValue(type_, value, False)

            # update_set.append("%s = %s" % (key, (self._cursor.mogrify("%s",[value]))))
            update_set.append("%s = %s" % (key, value))

        if len(update_set) == 0:
            return False

        update_set_txt = ", ".join(update_set)
        sql = self.driver_sql().queryUpdate(self.metadata().name(), update_set_txt, where_filter)
        # print("MODIFYING SQL :: ", sql)
        try:
            self.db().execute_query(sql)
        except Exception:
            self.logger.exception("ERROR: CursorTableModel.Update %s:", self.metadata().name())
            # self._cursor.execute("ROLLBACK")
            return False

        try:
            if self.cursorDB().description:
                returning_fields = [x[0] for x in self.cursorDB().description]

                for orow in self.cursorDB():
                    dict_update = dict(zip(returning_fields, orow))
                    self.setValuesDict(row, dict_update)

        except Exception:
            self.logger.exception("updateValuesDB: Error al assignar los valores de vuelta al buffer")

        self.need_update = True

        return True

    """
    Asigna un valor una fila usando un diccionario
    @param row. Columna afectada
    @param update_dict. array clave-valor indicando el listado de claves y valores a actualizar
    """

    def setValuesDict(self, row: int, update_dict: Dict[str, Any]) -> None:

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
                self.logger.warning("CursorTableModel.setValuesDict:: columns not found: %r", colsnotfound)
            self.indexUpdateRow(row)

        except Exception:
            self.logger.exception("CursorTableModel.setValuesDict(row %s) = %r :: ERROR:", row, update_dict)

    """
    Asigna un valor una celda
    @param row. Columna afectada
    @param fieldname. Nonbre de la fila afectada. Se puede obtener la columna con self.metadata().indexPos(fieldname)
    @param value. Valor a asignar. Puede ser texto, pixmap, etc...
    """

    def setValue(self, row: int, fieldname: str, value: Any) -> None:
        # Reimplementación para que todo pase por el método genérico.
        self.setValuesDict(row, {fieldname: value})

    """
    Crea una nueva linea en el tableModel
    @param buffer . PNBuffer a añadir
    """

    def Insert(self, fl_cursor: "PNSqlCursor") -> bool:
        # Metemos lineas en la tabla de la bd
        # pKValue = None
        buffer = fl_cursor.buffer()
        if buffer is None:
            raise Exception("Cursor has no buffer")
        campos = ""
        valores = ""
        for b in buffer.fieldsList():
            value: Any = None
            if buffer.value(b.name) is None:
                mtdfield = fl_cursor.metadata().field(b.name)
                if mtdfield is None:
                    raise Exception("field %s not found" % b.name)
                value = mtdfield.defaultValue()
            else:
                value = buffer.value(b.name)

            if value is not None:  # si el campo se rellena o hay valor default
                # if b.name == fl_cursor.metadata().primaryKey():
                #    pKValue = value
                if b.type_ in ("string", "stringlist") and isinstance(value, str):
                    value = self.db().normalizeValue(value)
                value = self.db().manager().formatValue(b.type_, value, False)
                if not campos:
                    campos = b.name
                    valores = value
                else:
                    campos = u"%s,%s" % (campos, b.name)
                    valores = u"%s,%s" % (valores, value)
        if campos:
            sql = """INSERT INTO %s (%s) VALUES (%s)""" % (fl_cursor.d.curName_, campos, valores)
            # conn = self._cursorConn.db()
            try:
                # print(sql)
                self.db().execute_query(sql)
                # self.refresh()
                # if pKValue is not None:
                #    fl_cursor.move(self.findPKRow((pKValue,)))

                self.need_update = True
            except Exception:
                self.logger.exception("CursorTableModel.%s.Insert() :: SQL: %s", self.metadata().name(), sql)
                # self._cursor.execute("ROLLBACK")
                return False

            # conn.commit()

            return True
        return False

    """
    Borra una linea en el tableModel
    @param cursor . Objecto FLSqlCursor
    """

    def Delete(self, cursor: "PNSqlCursor") -> None:
        pKName = self.metadata().primaryKey()
        mtdfield = self.metadata().field(pKName)
        if mtdfield is None:
            raise Exception("PK Field %s not found" % pKName)
        typePK = mtdfield.type()
        tableName = self.metadata().name()
        val = self.db().manager().formatValue(typePK, self.value(cursor.d._currentregister, pKName))
        sql = "DELETE FROM %s WHERE %s = %s" % (tableName, pKName, val)
        # conn = self._cursorConn.db()
        try:
            self.db().execute_query(sql)
            self.need_update = True
        except Exception:
            self.logger.exception("CursorTableModel.%s.Delete() :: ERROR:", self.metadata().name())
            # self._cursor.execute("ROLLBACK")
            return

        # conn.commit()

    """
    Delvuelve el index de un registro a raíz de Su Primary Key
    @param pklist. Lista con la PK a encontrar. Hay que meterno entre [] aunque solo sea un registro.
    @return index de la linea buscada
    """

    def findPKRow(self, pklist: Iterable[Any]) -> Optional[int]:
        if not isinstance(pklist, (tuple, list)):
            raise ValueError("findPKRow expects a list as first argument. Enclose PK inside brackets [self.pkvalue]")
        if not self.indexes_valid:
            for n in range(self.rows):
                self.indexUpdateRow(n)
            self.indexes_valid = True

        pklist = tuple(pklist)
        if pklist[0] is None:
            raise ValueError("Primary Key can't be null")
        parent = QtCore.QModelIndex()
        while self.canFetchMoreRows and pklist not in self.pkidx:
            self.fetchMore(parent, self.metadata().name(), self.where_filter)
            if not self.indexes_valid:
                for n in range(self.rows):
                    self.indexUpdateRow(n)
                self.indexes_valid = True

        if pklist not in self.pkidx:
            self.logger.info(
                "CursorTableModel.%s.findPKRow:: PK not found: %r (from: %r)", self.metadata().name(), pklist, list(self.pkidx.keys())[:8]
            )
            return None
        return self.pkidx[pklist]

    """
    Delvuelve el index de un registro a raíz de Su Composed Key
    @param cklist. Lista con la CK a encontrar.
    @return index de la linea buscada
    """

    def findCKRow(self, cklist: Iterable[Any]) -> Optional[int]:
        if not isinstance(cklist, (tuple, list)):
            raise ValueError("findCKRow expects a list as first argument.")
        if not self.indexes_valid:
            for n in range(self.rows):
                self.indexUpdateRow(n)
            self.indexes_valid = True
        cklist = tuple(cklist)
        if cklist not in self.ckidx:
            self.logger.warning("CursorTableModel.%s.findCKRow:: CK not found: %r ", self.metadata().name(), cklist)
            return None
        return self.ckidx[cklist]

    """
    Devuelve el nombre del campo que es PK
    @return nombre del campo PK
    """

    def pK(self) -> str:
        return self.metadata().primaryKey()

    """
    Devuelve el tipo de un campo determinado
    @param fieldName. Nombre del campo
    @return Tipo de campo
    """

    def fieldType(self, fieldName: str) -> str:
        field = self.metadata().field(fieldName)
        if field is None:
            raise Exception("field %s not found" % fieldName)
        return field.type()

    """
    Devuelve el alias de un campo determinado
    @param fieldName. Nombre del campo
    @return alias del campo
    """

    def alias(self, fieldName: str) -> str:
        field = self.metadata().field(fieldName)
        if field is None:
            raise Exception("field %s not found" % fieldName)
        return field.alias()

    """
    Devuelve el número de columnas
    @return Número de columnas
    """

    def columnCount(self, *args: List[Any]) -> int:
        # if args:
        #    self.logger.warning("columnCount%r: wrong arg count", args, stack_info=True)
        return self.cols

    """
    Actualiza el número de columnas existentes en el tableModel
    """

    def updateColumnsCount(self) -> None:
        self.cols = len(self.metadata().fieldList())
        self.loadColAliases()
        if self.metadata().isQuery():
            self._refresh_field_info()

    """
    Devuelve el número de lineas
    @return Número de lineas
    """

    def rowCount(self, parent: QtCore.QModelIndex = None) -> int:
        return self.rowsLoaded

    """
    Devuelve el tamaño de registros seleccionados con el cursor
    @return lineas seleccionadas
    """

    def size(self) -> int:

        size = 0
        mtd = self.metadata()
        if mtd:
            where_ = self.where_filter
            from_ = self.metadata().name()

            if mtd.isQuery():
                qry = self.db().manager().query(self.metadata().query())
                if qry is None:
                    raise Exception("Query not found")
                from_ = qry.from_()

            if self.where_filter.find("ORDER BY") > -1:
                where_ = self.where_filter[: self.where_filter.find("ORDER BY")]

            from pineboolib.application.database.pnsqlquery import PNSqlQuery  # noqa: F811

            q = PNSqlQuery(None, self.db().name)
            q.exec_("SELECT COUNT(*) FROM %s WHERE %s" % (from_, where_))
            if q.first():
                size = q.value(0)

        return size

    """
    Devuelve datos de la cebecera
    @param section. Columna
    @param orientation. Horizontal, Vertical
    @param role. Solo es util QtCore.Qt.DisplayRole, El resto de roles es omitido por headerData
    @return info segun sección, orientación y rol.
    """

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = QtCore.Qt.DisplayRole) -> Any:
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

    def loadColAliases(self) -> None:
        self.col_aliases = [str(self.metadata().indexFieldObject(i).alias()) for i in range(self.cols)]

    """
    Devuelve el FLFieldMetadata de un campo
    @param fieldName. Nombre del campo
    @return FLFieldMetadata
    """

    def fieldMetadata(self, fieldName: str) -> "PNFieldMetaData":
        field = self.metadata().field(fieldName)
        if field is None:
            raise Exception("fieldName %s not found" % fieldName)
        return field

    """
    Devuelve el FLTableMetaData de este tableModel
    @return Objeto FLTableMetaData
    """

    def metadata(self) -> "PNTableMetaData":
        if self._parent.d.metadata_ is None:
            raise Exception("Metadata not set")
        return self._parent.d.metadata_

    def driver_sql(self) -> Any:
        return self._driver_sql

    """
    Devuelve el cursor a la BD usado
    @return Objeto cursor
    """

    def cursorDB(self) -> "IApiCursor":
        return self._cursor_db

    def db(self) -> "IConnection":
        return self._cursorConn

    def set_parent_view(self, parent_view: QtWidgets.QTableView) -> None:
        self.parent_view = parent_view
