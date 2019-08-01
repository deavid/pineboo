# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets, Qt  # type: ignore
from PyQt5.QtWidgets import QCheckBox


from pineboolib.core import decorators
from pineboolib.core.utils.utils_base import filedir
from pineboolib.core.settings import config

# type: ignore
from .flsqlcursor import FLSqlCursor


from pineboolib import logging
from typing import Any, Optional, List, Dict, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from pineboolib.application.database.pncursortablemodel import PNCursorTableModel  # noqa: F401
    from pineboolib.application.metadata.pnfieldmetadata import PNFieldMetaData  # noqa: F401

logger = logging.getLogger(__name__)


class FLDataTable(QtWidgets.QTableView):

    """
    Clase que es una redefinicion de la clase QDataTable,
    especifica para las necesidades de AbanQ.

    @author InfoSiAL S.L.
    """

    """
    constructor
    """
    _parent: Optional[Any] = None
    filter_ = ""
    sort_ = ""
    fltable_iface = None

    """
    Numero de la fila (registro) seleccionada actualmente
    """
    rowSelected = -1

    """
    Numero de la columna (campo) seleccionada actualmente
    """
    colSelected = -1

    """
    Cursor, con los registros
    """
    cursor_: Optional[FLSqlCursor] = None

    """
    Almacena la tabla está en modo sólo lectura
    """
    readonly_: bool = False

    """
    Almacena la tabla está en modo sólo edición
    """
    editonly_: bool = False

    """
    Indica si la tabla está en modo sólo inserción
    """
    insertonly_: bool = False

    """
    Texto del último campo dibujado en la tabla
    """
    lastTextPainted_ = None

    """
    Pixmap precargados
    """
    pixOk_ = None
    pixNo_ = None

    """
    Lista con las claves primarias de los registros seleccionados por chequeo
    """
    primarysKeysChecked_: List[object] = []

    """
    Filtro persistente para el cursor
    """
    persistentFilter_ = ""

    """
    Indicador para evitar refrescos anidados
    """
    refreshing_ = False
    refresh_timer_ = None

    """
    Indica si el componente es emergente ( su padre es un widget del tipo Popup )
    """
    popup_ = False

    """
    Indica el ancho de las columnas establecidas explícitamente con FLDataTable::setColumnWidth
    """
    widthCols_: Dict[str, int] = {}

    """
    Indica si se deben mostrar los campos tipo pixmap en todas las filas
    """
    showAllPixmaps_ = False

    """
    Nombre de la función de script a invocar para obtener el color de las filas y celdas
    """
    function_get_color = None

    """
    Indica que no se realicen operaciones con la base de datos (abrir formularios). Modo "sólo tabla".
    """
    onlyTable_ = False

    def __init__(self, parent: Optional[Any] = None, name: Optional[str] = None, popup: bool = False):
        super(FLDataTable, self).__init__(parent)

        if parent:
            self._parent = parent

        if name is None:
            name = "FLDataTable"
        self.setObjectName(name)

        self.readonly_ = False
        self.editonly_ = False
        self.insertonly_ = False

        self.pixOk_ = filedir("../share/icons", "unlock.png")
        self.pixNo_ = filedir("../share/icons", "lock.png")
        self.paintFieldMtd_ = None
        self.refreshing_ = False

        self._v_header = self.verticalHeader()
        self._v_header.setDefaultSectionSize(22)
        self._h_header = self.horizontalHeader()
        self._h_header.setDefaultSectionSize(120)
        self._h_header.setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
        self.sortByColumn(0, QtCore.Qt.AscendingOrder)
        self.fltable_iface = None
        self.popup_ = popup

    """
    desctructor
    """

    def __del__(self) -> None:
        # if self.timerViewRepaint_:
        #    self.timerViewRepaint_.stop()

        if self.cursor_:
            self.cursor_.restoreEditionFlag(self)
            self.cursor_.restoreBrowseFlag(self)

    def header(self) -> Any:
        return self._h_header

    def model(self) -> "PNCursorTableModel":
        return super().model()

    """
    Establece el cursor
    """

    def setFLSqlCursor(self, c: FLSqlCursor) -> None:
        if c and c.metadata():
            cur_chg = False
            if self.cursor_ and not self.cursor_ == c:
                self.cursor_.restoreEditionFlag(self)
                self.cursor_.restoreBrowseFlag(self)
                self.cursor_.d._current_changed.disconnect(self.ensureRowSelectedVisible)
                self.cursor_.cursorUpdated.disconnect(self.refresh)

                cur_chg = True

            if not self.cursor_ or cur_chg:
                self.cursor_ = c
                self.setFLReadOnly(self.readonly_)
                self.setEditOnly(self.editonly_)
                self.setInsertOnly(self.insertonly_)
                self.setOnlyTable(self.onlyTable_)

                self.cursor_.d._current_changed.connect(self.ensureRowSelectedVisible)
                self.cursor_.cursorUpdated.connect(self.refresh)

                self.setModel(self.cursor_.model())
                self.setSelectionModel(self.cursor_.selection())
                # self.model().sort(self.header().logicalIndex(0), 0)
                self.installEventFilter(self)
                self.model().set_parent_view(self)
            # if self.cursor_.at() >= 0:
            #    QtCore.QTimer.singleShot(2000, self.marcaRow) #Por ahora es 3000 para que de tiempo a mostrarse FIXME

    def marcaRow(self, id_pk: Optional[Any]) -> None:
        """
        Establece un filtro persistente que siempre se aplica al cursor antes
        de hacer un refresh
        """
        if id_pk is not None:
            pos = self.model().findPKRow((id_pk,))
            if pos is not None:
                self.cur.move(pos)
                # self.ensureRowSelectedVisible()

    def setPersistentFilter(self, pFilter: str) -> None:
        pFilter_none: Optional[str] = pFilter
        if pFilter_none is None:
            raise Exception("Invalid use of setPersistentFilter with None")
        self.persistentFilter_ = pFilter

    def setFilter(self, f: str) -> None:
        self.filter_ = f

    def numCols(self) -> int:
        """
        retorna el número de columnas
        """

        return self.horizontalHeader().count()

    def setSort(self, s: str) -> None:
        self.sort_ = s

    # def cursor(self) -> Optional[FLSqlCursor]:
    #    """
    #    Devuelve el cursor
    #    """
    #    return self.cursor_

    @property
    def cur(self) -> FLSqlCursor:
        if self.cursor_ is None:
            raise Exception("Cursor not set yet")
        if self.cursor_.aqWasDeleted():
            raise Exception("Cursor was deleted")
        return self.cursor_

    def setFLReadOnly(self, mode: bool) -> None:
        """
        Establece la tabla a sólo lectura o no
        """

        if not self.cursor_ or self.cursor_.aqWasDeleted():
            return

        self.cursor_.setEdition(not mode, self)
        self.readonly_ = mode

    def flReadOnly(self) -> bool:
        return self.readonly_

    """
    Establece la tabla a sólo edición o no
    """

    def setEditOnly(self, mode: bool) -> None:

        if not self.cursor_ or self.cursor_.aqWasDeleted():
            return

        self.editonly_ = mode

    def editOnly(self) -> bool:
        return self.editonly_

    """
    Establece la tabla a sólo insercion o no
    """

    def setInsertOnly(self, mode: bool) -> None:

        if not self.cursor_ or self.cursor_.aqWasDeleted():
            return

        self.cursor_.setEdition(not mode, self)
        self.insertonly_ = mode

    def insertOnly(self) -> bool:
        return self.insertonly_

    """
    Obtiene la lista con las claves primarias de los registros seleccionados por chequeo
    """

    def primarysKeysChecked(self) -> list:
        return self.primarysKeysChecked_

    """
    Limpia la lista con las claves primarias de los registros seleccionados por chequeo
    """

    def clearChecked(self) -> None:
        self.primarysKeysChecked_.clear()
        model = self.cur.model()
        for r in model._checkColumn.keys():
            model._checkColumn[r].setChecked(False)

    """
    Establece el estado seleccionado por chequeo para un regsitro, indicando el valor de su clave primaria
    """

    def setPrimaryKeyChecked(self, primaryKeyValue: str, on: bool) -> None:
        model = self.cur.model()
        if on:
            if primaryKeyValue not in self.primarysKeysChecked_:
                self.primarysKeysChecked_.append(primaryKeyValue)
                self.primaryKeyToggled.emit(primaryKeyValue, False)
        else:
            if primaryKeyValue in self.primarysKeysChecked_:
                self.primarysKeysChecked_.remove(primaryKeyValue)
                self.primaryKeyToggled.emit(primaryKeyValue, False)

        if primaryKeyValue not in model._checkColumn.keys():
            model._checkColumn[primaryKeyValue] = QCheckBox()

        model._checkColumn[primaryKeyValue].setChecked(on)

    """
    Ver FLDataTable::showAllPixmaps_
    """

    def setShowAllPixmaps(self, s: bool) -> None:
        self.showAllPixmaps_ = s

    def showAllPixmap(self) -> bool:
        return self.showAllPixmaps_

    """
    Ver FLDataTable::function_get_color
    """

    def setFunctionGetColor(self, f: Optional[str], iface: Optional[Any] = None) -> None:
        self.fltable_iface = iface
        self.function_get_color = f

    def functionGetColor(self) -> Tuple[Optional[str], Any]:
        return (self.function_get_color, self.fltable_iface)

    """
    Ver FLDataTable::onlyTable_
    """

    def setOnlyTable(self, on: bool = True) -> None:
        if not self.cursor_ or self.cursor_.aqWasDeleted():
            return

        self.cursor_.setEdition(not on, self)
        self.cursor_.setBrowse(not on, self)
        self.onlyTable_ = on

    def onlyTable(self) -> bool:
        return self.onlyTable_

    """
    Redefinida por conveniencia
    """

    def indexOf(self, i: int) -> str:
        return self.header().visualIndex(i)

    def fieldName(self, col: int) -> str:
        """
        @return El nombre del campo en la tabla de una columna dada
        """
        field = self.cur.field(self.indexOf(col))
        if field is None:
            raise Exception("Field not found")
        return field.name

    """
    Filtrado de eventos
    """

    def eventFilter(self, o: Any, e: Any) -> bool:
        r = self.currentRow()
        c = self.currentColumn()
        nr = self.numRows()
        nc = self.numCols()
        if e.type() == QtCore.QEvent.KeyPress:
            key_event = e

            if key_event.key() == QtCore.Qt.Key_Escape and self.popup_ and self.parentWidget():
                self.parentWidget().hide()
                return True

            if key_event.key() == QtCore.Qt.Key_Insert:
                return True

            if key_event.key() == QtCore.Qt.Key_F2:
                return True

            if key_event.key() == QtCore.Qt.Key_Up and r == 0:
                return True

            if key_event.key() == QtCore.Qt.Key_Left and c == 0:
                return True

            if key_event.key() == QtCore.Qt.Key_Down and r == nr - 1:
                return True

            if key_event.key() == QtCore.Qt.Key_Right and c == nc - 1:
                return True

            if key_event.key() in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return) and r > -1:
                self.recordChoosed.emit()
                return True

            if key_event.key() == QtCore.Qt.Key_Space:
                self.setChecked(self.model().index(r, c))

            if not config.value("ebcomportamiento/FLTableShortCut", False):
                if key_event.key() == QtCore.Qt.Key_A and not self.popup_:
                    if self.cursor_ and not self.readonly_ and not self.editonly_ and not self.onlyTable_:

                        self.cursor_.insertRecord()
                        return True
                    else:
                        return False

                if key_event.key() == QtCore.Qt.Key_C and not self.popup_:
                    if self.cursor_ and not self.readonly_ and not self.editonly_ and not self.onlyTable_:
                        self.cursor_.copyRecord()
                        return True
                    else:
                        return False

                if key_event.key() == QtCore.Qt.Key_M and not self.popup_:
                    if self.cursor_ and not self.readonly_ and not self.onlyTable_:
                        self.cursor_.editRecord()
                        return True
                    else:
                        return False

                if key_event.key() == QtCore.Qt.Key_Delete and not self.popup_:
                    if self.cursor_ and not self.readonly_ and not self.editonly_ and not self.onlyTable_:
                        self.cursor_.deleteRecord()
                        return True
                    else:
                        return False

                if key_event.key() == QtCore.Qt.Key_V and not self.popup_:
                    if self.cursor_ and not self.onlyTable_:
                        self.cursor_.browseRecord()
                        return True

            return False

        return super(FLDataTable, self).eventFilter(o, e)

    """
    Redefinido por conveniencia para pintar la celda
    """

    @decorators.NotImplementedWarn
    def paintCell(self, p: Any, row: int, col: int, cr: Any, selected: bool, cg: Any) -> None:
        pass

    """
    Redefinido por conveniencia para pintar el campo
    """

    @decorators.NotImplementedWarn
    def paintField(self, p: Any, field: str, cr: Any, selected: bool) -> None:
        pass

    """
    Redefinido por conveniencia, para evitar que aparezca el menu contextual
    con las opciones para editar registros
    """

    def contextMenuEvent(self, e: Any) -> None:
        super(FLDataTable, self).contextMenuEvent(e)

        if not self.cursor_ or not self.cursor_.isValid() or not self.cursor_.metadata():
            return

        mtd = self.cursor_.metadata()
        pri_key = mtd.primaryKey()

        field = mtd.field(pri_key)
        if field is None:
            return

        rel_list = field.relationList()
        if not rel_list:
            return

        db = self.cursor_.db()
        pri_key_val = self.cursor_.valueBuffer(pri_key)

        from pineboolib import pncontrolsfactory

        popup = pncontrolsfactory.QMenu(self)

        menu_frame = pncontrolsfactory.QWidget(self, QtCore.Qt.Popup)

        lay = pncontrolsfactory.QVBoxLayout()
        menu_frame.setLayout(lay)

        tmp_pos = e.globalPos()

        for rel in rel_list:
            cur = FLSqlCursor(rel.foreignTable(), True, db.connectionName(), None, None, popup)

            if cur.d.metadata_:
                mtd = cur.metadata()
                field = mtd.field(rel.foreignField())
                if field is None:
                    continue

                sub_popup = pncontrolsfactory.QMenu(self)
                sub_popup.setTitle(mtd.alias())
                sub_popup_frame = pncontrolsfactory.QWidget(sub_popup, QtCore.Qt.Popup)
                lay_popup = pncontrolsfactory.QVBoxLayout(sub_popup)
                sub_popup_frame.setLayout(lay_popup)

                dt = pncontrolsfactory.FLDataTable(None, "FLDataTable", True)
                lay_popup.addWidget(dt)

                dt.setFLSqlCursor(cur)
                filter = db.manager().formatAssignValue(field, pri_key_val, False)
                cur.setFilter(filter)
                dt.setFilter(filter)
                dt.refresh()

                # horiz_header = dt.header()
                for i in range(dt.numCols()):
                    field = mtd.indexFieldObject(i)
                    if not field:
                        continue

                    if not field.visibleGrid():
                        dt.setColumnHidden(i, True)

                sub_menu = popup.addMenu(sub_popup)
                sub_menu.hovered.connect(sub_popup_frame.show)
                sub_popup_frame.move(tmp_pos.x() + 200, tmp_pos.y())  # FIXME: Hay que mejorar esto ...

        popup.move(tmp_pos.x(), tmp_pos.y())

        popup.exec_(e.globalPos())
        del popup
        e.accept()

    """
    Redefine por conveniencia, el comportamiento al hacer clic sobre una
    celda
    """

    def setChecked(self, index: Any) -> None:
        row = index.row()
        col = index.column()
        field = self.cur.metadata().indexFieldObject(col)
        _type = field.type()

        if _type != "check":
            return
        model = self.cur.model()
        pK = str(model.value(row, self.cur.metadata().primaryKey()))
        model._checkColumn[pK].setChecked(not model._checkColumn[pK].isChecked())
        self.setPrimaryKeyChecked(str(pK), model._checkColumn[pK].isChecked())
        # print("FIXME: falta un repaint para ver el color!!")

    """
    Redefinida por conveniencia
    """

    def focusOutEvent(self, e: Any) -> None:
        # setPaletteBackgroundColor(qApp->palette().color(QPalette::Active, QColorGroup::Background)) FIXME
        pass

    """
    Redefinida por conveniencia
    """

    def handleError(self) -> None:
        pass

    """
    Redefinida por conveniencia
    """

    @decorators.NotImplementedWarn
    def drawContents(self, p: Any, cx: Any, cy: Any, cw: Any, ch: Any) -> None:
        pass

    """ Uso interno """
    changingNumRows_ = False

    def syncNumRows(self) -> None:
        # print("syncNumRows")
        if not self.cursor_:
            return

        if self.changingNumRows_:
            return
        if self.numRows() != self.cursor_.size():
            self.changingNumRows_ = True
            self.setNumRows(self.cursor_.size())
            self.changingNumRows_ = False

    """ Uso interno """

    @decorators.NotImplementedWarn
    def getCellStyle(self, brush: Any, pen: Any, field: Any, fieldTMD: Any, row: Any, selected: Any, cg: Any) -> None:
        pass

    paintFieldName_: Optional[str] = None
    paintFieldMtd_: Optional[Any] = None

    def paintFieldMtd(self, f: Any, t: Any) -> Any:
        if self.paintFieldMtd_ and self.paintFieldName_ == f:
            return self.paintFieldMtd_

        self.paintFieldName_ = f
        self.paintFieldMtd_ = t.field(f)
        return self.paintFieldMtd_

    timerViewRepaint_ = None
    """
    Redefinida por conveniencia
    """

    def focusInEvent(self, e: Any) -> None:
        obj = self
        # refresh = True
        while obj.parent():
            if getattr(obj, "inExec_", False):
                # refresh = False
                break
            else:
                obj = obj.parent()

        # if refresh:
        #    self.refresh()
        super().focusInEvent(e)

    """
    def setFocus(self):

        if not self.cursor_ or self.cursor_.aqWasDeleted():
            return

        if not self.hasFocus():
            # setPaletteBackgroundColor(qApp->palette().color(QPalette::Active, QColorGroup::Base)); FIXME
            super(FLDataTable, self).update()  # refresh en Qt4 -> update()
        else:
            self.syncNumRows()

        super(FLDataTable, self).setFocus()
    """
    """
    Redefinida por conveniencia
    """

    def refresh(self, refresh_option: Any = None) -> None:

        if not self.cursor_:
            return

        if self.popup_:
            self.cursor_.refresh()
        # if not self.refreshing_ and self.cursor_ and not self.cursor_.aqWasDeleted() and self.cursor_.metadata():
        if not self.refreshing_:

            # if self.function_get_color and self.cur.model():
            #    if self.cur.model().color_function_ != self.function_get_color:
            #        self.cur.model().setColorFunction(self.function_get_color)

            self.refreshing_ = True
            self.hide()
            filter: str = self.persistentFilter_
            if self.filter_:
                if self.filter_ not in self.persistentFilter_:
                    if self.persistentFilter_:
                        filter = "%s AND %s" % (filter, self.filter_)
                    else:
                        filter = self.filter_

            self.cur.setFilter(filter)
            if self.sort_:
                self.cur.setSort(self.sort_)

            last_pk = None
            buffer = self.cur.buffer()
            if buffer:
                pk_name = buffer.pK()
                if pk_name is not None:
                    last_pk = buffer.value(pk_name)

            self.cur.refresh()

            self.marcaRow(last_pk)
            self.cur.refreshBuffer()
            self.show()
            self.refreshing_ = False

    """
    Hace que la fila seleccionada esté visible
    """

    @decorators.pyqtSlot()
    @decorators.pyqtSlot(int)
    def ensureRowSelectedVisible(self, position: Optional[int] = None) -> None:
        if position is None:
            if self.cursor():
                position = self.cur.at()
            else:
                return

        # index = self.cur.model().index(position, 0)
        # if index is not None:
        #    self.scrollTo(index)

    """
    Foco rápido sin refrescos para optimizar
    """

    def setQuickFocus(self) -> None:
        # setPaletteBackgroundColor(qApp->palette().color(QPalette::Active, QColorGroup::Base)); FIXME
        super(FLDataTable, self).setFocus()

    """
    Establece el ancho de una columna

    @param  field Nombre del campo de la base de datos correspondiente a la columna
    @param  w     Ancho de la columna
    """

    def setColWidth(self, field: str, w: int) -> None:
        self.widthCols_[field] = w

    def resize_column(self, col: int, str_text: Optional[str]) -> None:
        if str_text is None:
            return

        str_text = str(str_text)

        field = self.model().metadata().indexFieldObject(col)
        if field.name() in self.widthCols_.keys():
            if self.columnWidth(col) < self.widthCols_[field.name()]:
                self.header().resizeSection(col, self.widthCols_[field.name()])
        else:
            wC = self.header().sectionSize(col)

            fm = Qt.QFontMetrics(self.header().font())
            wH = fm.horizontalAdvance(field.alias() + "W")
            if wH < wC:
                wH = wC

            wC = fm.horizontalAdvance(str_text) + fm.maxWidth()
            if wC > wH:
                self.header().resizeSection(col, wC)
                if col == 0 and self.popup_:
                    pw = self.parentWidget()
                    if pw and pw.width() < wC:
                        self.resize(wC, pw.height())
                        pw.resize(wC, pw.height())

    # def delayedViewportRepaint(self) -> None:
    #    if not self.timerViewRepaint_:
    #        self.timerViewRepaint_ = QtCore.QTimer(self)
    #        self.timerViewRepaint_.timeout.connect(self.repaintViewportSlot)

    #    if not self.timerViewRepaint_.isActive():
    #        self.setUpdatesEnabled(False)
    #        self.timerViewRepaint_.start(50)

    # @decorators.pyqtSlot()
    # def repaintViewportSlot(self) -> None:

    #    vw = self.viewport()
    #    self.setUpdatesEnabled(True)
    #    if vw:
    #        vw.repaint(False)

    def cursorDestroyed(self, obj: Optional[Any] = None) -> None:

        if not obj or not isinstance(obj, FLSqlCursor):
            return

        self.cursor_ = None

    """
    Indica que se ha elegido un registro
    """
    recordChoosed = QtCore.pyqtSignal()
    """
    Indica que ha cambiado el estado del campo de selección de un registro. Es decir
    se ha incluido o eliminado su clave primaria de la lista de claves primarias seleccionadas.
    Esta señal se emite cuando el usuario hace click en el control de chequeo y cuando se cambia
    programáticamente el chequeo mediante el método FLDataTable::setPrimaryKeyChecked.

    @param  primaryKeyValue El valor de la clave primaria del registro correspondiente
    @param  on  El nuevo estado; TRUE chequeo activado, FALSE chequeo desactivado
    """
    primaryKeyToggled = QtCore.pyqtSignal(str, bool)

    """
    Numero de registros que ofrece el cursor
    """

    def numRows(self) -> int:
        if not self.cursor_:
            return -1

        return self.cursor_.model().size()

    """
    Retorna el index real (incusive columnas ocultas) a partir de un nombre de un campo
    @param name El nombre del campo a buscar en la tabla
    @return posicion de la columna en la tabla
    """

    def column_name_to_column_index(self, name: str) -> int:
        """
        Retorna el index real (incusive columnas ocultas) a partir de un nombre de un campo
        @param name El nombre del campo a buscar en la tabla
        @return posicion de la columna en la tabla
        """
        if not self.cursor_:
            return -1

        return self.cursor_.model().metadata().fieldIsIndex(name)

    def mouseDoubleClickEvent(self, e: Any) -> None:
        if e.button() != QtCore.Qt.LeftButton:
            return

        self.recordChoosed.emit()

    def visual_index_to_column_index(self, c: int) -> Optional[int]:
        """
        Retorna el column index a partir de un index de columnas visibles.
        @param c posicion de la columna visible.
        @return index column de la columna
        """
        if not self.cursor_:
            return None

        visible_id = -1
        ret_ = None
        for column in range(self.model().columnCount()):
            if not self.isColumnHidden(self.logical_index_to_visual_index(column)):
                visible_id += 1

                if visible_id == c:
                    ret_ = column
                    break

        return ret_

    def visual_index_to_logical_index(self, c: int) -> int:
        """
        Index visual a lógico
        """
        return self.header().logicalIndex(c)

    def logical_index_to_visual_index(self, c: int) -> int:
        """
        Index lógico a Index Visual
        """
        return self.header().visualIndex(c)

    def visual_index_to_field(self, pos_: int) -> Optional["PNFieldMetaData"]:
        # if pos_ is None:
        #     logger.warning("visual_index_to_field: pos is None")
        #     return None
        colIdx = self.visual_index_to_column_index(pos_)
        if colIdx is None:
            logger.warning("visual_index_to_field: colIdx is None")
            return None

        logIdx = self.logical_index_to_visual_index(colIdx)
        # if logIdx is None:
        #     logger.warning("visual_index_to_field: logIdx is None")
        #     return None
        model: "PNCursorTableModel" = self.model()
        mtd = model.metadata()
        mtdfield = mtd.indexFieldObject(logIdx)
        if not mtdfield.visibleGrid():
            raise ValueError("Se ha devuelto el field %s.%s que no es visible en el grid" % (mtd.name(), mtdfield.name()))

        return mtdfield

    def currentRow(self) -> int:
        """
        Devuelve la fila actual
        """
        return self.currentIndex().row()

    def currentColumn(self) -> int:
        """
        Devuelve la columna actual
        """
        return self.currentIndex().column()
