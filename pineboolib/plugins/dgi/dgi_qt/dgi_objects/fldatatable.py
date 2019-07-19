# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets, Qt  # type: ignore
from pineboolib.core import decorators
from pineboolib.core.utils.utils_base import filedir
from pineboolib.fllegacy.flsqlcursor import FLSqlCursor
from pineboolib.fllegacy.flsettings import FLSettings
from PyQt5.QtWidgets import QCheckBox  # type: ignore
from pineboolib import logging
from typing import Any, Optional, TypeVar, List, Dict

_T1 = TypeVar("_T1")

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
    _parent = None
    filter_ = None
    sort_ = None
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
    cursor_ = None

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
    persistentFilter_ = None

    """
    Indicador para evitar refrescos anidados
    """
    refreshing_ = False
    refresh_timer_ = None

    """
    Indica si el componente es emergente ( su padre es un widget del tipo Popup )
    """
    popup_ = None

    """
    Indica el ancho de las columnas establecidas explícitamente con FLDataTable::setColumnWidth
    """
    widthCols_: Dict[str, int] = {}

    """
    Indica si se deben mostrar los campos tipo pixmap en todas las filas
    """
    showAllPixmaps_ = None

    """
    Nombre de la función de script a invocar para obtener el color de las filas y celdas
    """
    function_get_color = None

    """
    Indica que no se realicen operaciones con la base de datos (abrir formularios). Modo "sólo tabla".
    """
    onlyTable_ = False

    def __init__(self, parent=None, name=None, popup=False) -> None:
        super(FLDataTable, self).__init__(parent)

        if parent:
            self._parent = parent

        if not name:
            self.setName("FLDataTable")

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
        if self.timerViewRepaint_:
            self.timerViewRepaint_.stop()

        if self.cursor_:
            self.cursor_.restoreEditionFlag(self)
            self.cursor_.restoreBrowseFlag(self)

    def header(self) -> Any:
        return self._h_header

    """
    Establece el cursor
    """

    def setFLSqlCursor(self, c) -> None:
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

    """
    Establece un filtro persistente que siempre se aplica al cursor antes
    de hacer un refresh
    """

    def marcaRow(self, id_pk) -> None:
        if id_pk is not None:
            pos = self.model().findPKRow((id_pk,))
            if pos is not None:
                self.cursor().move(pos)
                # self.ensureRowSelectedVisible()

    def setPersistentFilter(self, pFilter) -> None:
        self.persistentFilter_ = pFilter

    def setFilter(self, f) -> None:
        self.filter_ = f

    """
    retorna el número de columnas
    """

    def numCols(self) -> Any:

        return self.horizontalHeader().count()

    def setSort(self, s) -> None:
        self.sort_ = s

    """
    Devuelve el cursor
    """

    def cursor(self) -> Any:
        return self.cursor_

    """
    Establece la tabla a sólo lectura o no
    """

    def setFLReadOnly(self, mode) -> None:

        if not self.cursor_ or self.cursor_.aqWasDeleted():
            return

        self.cursor_.setEdition(not mode, self)
        self.readonly_ = mode

    def flReadOnly(self) -> bool:
        return self.readonly_

    """
    Establece la tabla a sólo edición o no
    """

    def setEditOnly(self, mode) -> None:

        if not self.cursor_ or self.cursor_.aqWasDeleted():
            return

        self.editonly_ = mode

    def editOnly(self) -> bool:
        return self.editonly_

    """
    Establece la tabla a sólo insercion o no
    """

    def setInsertOnly(self, mode) -> None:

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
        for r in self.cursor().model()._checkColumn.keys():
            self.cursor().model()._checkColumn[r].setChecked(False)

    """
    Establece el estado seleccionado por chequeo para un regsitro, indicando el valor de su clave primaria
    """

    def setPrimaryKeyChecked(self, primaryKeyValue: object, on) -> None:
        if on:
            if primaryKeyValue not in self.primarysKeysChecked_:
                self.primarysKeysChecked_.append(primaryKeyValue)
                self.primaryKeyToggled.emit(primaryKeyValue, False)
        else:
            if primaryKeyValue in self.primarysKeysChecked_:
                self.primarysKeysChecked_.remove(primaryKeyValue)
                self.primaryKeyToggled.emit(primaryKeyValue, False)

        if primaryKeyValue not in self.cursor().model()._checkColumn.keys():
            self.cursor().model()._checkColumn[primaryKeyValue] = QCheckBox()

        self.cursor().model()._checkColumn[primaryKeyValue].setChecked(on)

    """
    Ver FLDataTable::showAllPixmaps_
    """

    def setShowAllPixmaps(self, s) -> None:
        self.showAllPixmaps_ = s

    def showAllPixmap(self) -> Any:
        return self.showAllPixmaps_

    """
    Ver FLDataTable::function_get_color
    """

    def setFunctionGetColor(self, f: str, iface=None) -> None:
        self.fltable_iface = iface
        self.function_get_color = f

    def functionGetColor(self) -> Any:
        return (self.function_get_color, self.fltable_iface)

    """
    Ver FLDataTable::onlyTable_
    """

    def setOnlyTable(self, on=True) -> None:
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

    def indexOf(self, i) -> Any:
        return self.header().visualIndex(i)

    """
    @return El nombre del campo en la tabla de una columna dada
    """

    def fieldName(self, col) -> Any:

        if not self.cursor_ or self.cursor_.aqWasDeleted():
            return None

        field = self.cursor_.field(self.indexOf(col))
        if field is None:
            return None

        return field.name()

    """
    Filtrado de eventos
    """

    def eventFilter(self, o, e) -> Any:
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
                from pineboolib import pncontrolsfactory

                chk = pncontrolsfactory.FLCheckBox(self.cellWidget(r, c))
                if chk:
                    chk.animateClick()

            settings = FLSettings()
            if not settings.readBoolEntry("ebcomportamiento/FLTableShortCut", False):
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
    def paintCell(self, p, row, col, cr, selected, cg):
        pass

    """
    Redefinido por conveniencia para pintar el campo
    """

    @decorators.NotImplementedWarn
    def paintField(self, p, field, cr, selected):
        pass

    """
    Redefinido por conveniencia, para evitar que aparezca el menu contextual
    con las opciones para editar registros
    """

    def contextMenuEvent(self, e) -> None:
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

            if cur.metadata():
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

    def setChecked(self, index) -> None:
        if not self.cursor_:
            return

        row = index.row()
        col = index.column()
        field = self.cursor_.metadata().indexFieldObject(col)
        _type = field.type()

        if _type != "check":
            return

        pK = str(self.cursor().model().value(row, self.cursor().metadata().primaryKey()))
        self.cursor().model()._checkColumn[pK].setChecked(not self.cursor().model()._checkColumn[pK].isChecked())
        self.setPrimaryKeyChecked(str(pK), self.cursor().model()._checkColumn[pK].isChecked())
        # print("FIXME: falta un repaint para ver el color!!")

    """
    Redefinida por conveniencia
    """

    def focusOutEvent(self, e) -> None:
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
    def drawContents(self, p, cx, cy, cw, ch):
        pass

    """ Uso interno """
    changingNumRows_ = None

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
    def getCellStyle(self, brush, pen, field, fieldTMD, row, selected, cg):
        pass

    paintFieldName_ = None
    paintFieldMtd_ = None

    def paintFieldMtd(self, f, t) -> Any:
        if self.paintFieldMtd_ and self.paintFieldName_ == f:
            return self.paintFieldMtd_

        self.paintFieldName_ = f
        self.paintFieldMtd_ = t.field(f)
        return self.paintFieldMtd_

    timerViewRepaint_ = None
    """
    Redefinida por conveniencia
    """

    def focusInEvent(self, e) -> None:
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

    def refresh(self, refresh_option=None) -> None:

        if not self.cursor_:
            return

        if self.popup_:
            self.cursor_.refresh()
        # if not self.refreshing_ and self.cursor_ and not self.cursor_.aqWasDeleted() and self.cursor_.metadata():
        if not self.refreshing_:

            # if self.function_get_color and self.cursor().model():
            #    if self.cursor().model().color_function_ != self.function_get_color:
            #        self.cursor().model().setColorFunction(self.function_get_color)

            self.refreshing_ = True
            self.hide()
            filter = self.persistentFilter_
            if self.filter_:
                if not self.persistentFilter_ or self.filter_ not in self.persistentFilter_:
                    if self.persistentFilter_:
                        filter = "%s AND %s" % (filter, self.filter_)
                    else:
                        filter = self.filter_

            self.cursor().setFilter(filter)
            if self.sort_:
                self.cursor().setSort(self.sort_)

            last_pk = None
            if self.cursor().buffer():
                pk_name = self.cursor().buffer().pK()
                if pk_name is not None:
                    last_pk = self.cursor().buffer().value(pk_name)

            self.cursor().refresh()

            self.marcaRow(last_pk)
            self.cursor().refreshBuffer()
            self.show()
            self.refreshing_ = False

    """
    Hace que la fila seleccionada esté visible
    """

    @QtCore.pyqtSlot()
    @QtCore.pyqtSlot(int)
    def ensureRowSelectedVisible(self, position=None):
        if position is None:
            if self.cursor():
                position = self.cursor().at()
            else:
                return

        # index = self.cursor().model().index(position, 0)
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

    def setColumnWidth(self, field, w) -> None:
        self.widthCols_[field] = w

    def resize_column(self, col, str_text: Optional[str]) -> None:
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

    def delayedViewportRepaint(self) -> None:
        if not self.timerViewRepaint_:
            self.timerViewRepaint_ = QtCore.QTimer(self)
            self.timerViewRepaint_.timeout.connect(self.repaintViewportSlot)

        if not self.timerViewRepaint_.isActive():
            self.setUpdatesEnabled(False)
            self.timerViewRepaint_.start(50)

    @QtCore.pyqtSlot()
    def repaintViewportSlot(self):

        vw = self.viewport()
        self.setUpdatesEnabled(True)
        if vw:
            vw.repaint(False)

    def cursorDestroyed(self, obj=None) -> None:

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

    def numRows(self) -> Any:
        if not self.cursor_:
            return -1

        return self.cursor_.model().size()

    """
    Retorna el index real (incusive columnas ocultas) a partir de un nombre de un campo
    @param name El nombre del campo a buscar en la tabla
    @return posicion de la columna en la tabla
    """

    def column_name_to_column_index(self, name) -> Any:
        """
        Retorna el index real (incusive columnas ocultas) a partir de un nombre de un campo
        @param name El nombre del campo a buscar en la tabla
        @return posicion de la columna en la tabla
        """
        if not isinstance(name, str) or not self.cursor_:
            return -1

        return self.cursor_.model().metadata().fieldIsIndex(name)

    def mouseDoubleClickEvent(self, e) -> None:
        if e.button() != QtCore.Qt.LeftButton:
            return

        self.recordChoosed.emit()

    def visual_index_to_column_index(self, c) -> Optional[int]:
        """
        Retorna el column index a partir de un index de columnas visibles.
        @param c posicion de la columna visible.
        @return index column de la columna
        """
        if not isinstance(c, int) or not self.cursor_:
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

    def visual_index_to_logical_index(self, c) -> Any:
        """
        Index visual a lógico
        """
        return self.header().logicalIndex(c)

    def logical_index_to_visual_index(self, c) -> Any:
        """
        Index lógico a Index Visual
        """
        return self.header().visualIndex(c)

    def visual_index_to_field(self, pos_) -> Any:
        if pos_ is None:
            logger.warning("visual_index_to_field: pos is None")
            return None
        colIdx = self.visual_index_to_column_index(pos_)
        if colIdx is None:
            logger.warning("visual_index_to_field: colIdx is None")
            return None

        logIdx = self.logical_index_to_visual_index(colIdx)
        if logIdx is None:
            logger.warning("visual_index_to_field: logIdx is None")
            return None

        mtd = self.model().metadata().indexFieldObject(logIdx)
        if mtd is not None:
            if not mtd.visibleGrid():
                raise ValueError("Se ha devuelto el field %s.%s que no es visible en el grid" % (mtd.metadata().name(), mtd.name()))

            return mtd

    def currentRow(self) -> Any:
        """
        Devuelve la fila actual
        """
        return self.currentIndex().row()

    def currentColumn(self) -> Any:
        """
        Devuelve la columna actual
        """
        return self.currentIndex().column()
