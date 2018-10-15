# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from pineboolib import decorators
from pineboolib.utils import filedir
from pineboolib.fllegacy import FLSqlCursor
from pineboolib.fllegacy.FLSettings import FLSettings
from PyQt5.QtWidgets import QApplication, QCheckBox
import pineboolib


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
    readonly_ = None

    """
    Almacena la tabla está en modo sólo edición
    """
    editonly_ = None

    """
    Indica si la tabla está en modo sólo inserción
    """
    insertonly_ = None

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
    primarysKeysChecked_ = []

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
    widthCols_ = []

    """
    Indica si se deben mostrar los campos tipo pixmap en todas las filas
    """
    showAllPixmaps_ = None

    """
    Nombre de la función de script a invocar para obtener el color de las filas y celdas
    """
    functionGetColor_ = None

    """
    Indica que no se realicen operaciones con la base de datos (abrir formularios). Modo "sólo tabla".
    """
    onlyTable_ = None

    def __init__(self, parent=None, name=None, popup=False):
        super(FLDataTable, self).__init__(parent)

        if parent:
            self._parent = parent

        if not name:
            self.setName("FLDataTable")

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

        self.popup_ = popup

    """
    desctructor
    """

    def __del__(self):
        if self.timerViewRepaint_:
            self.timerViewRepaint_.stop()

        if self.cursor_:
            self.cursor_.restoreEditionFlag(self)
            self.cursor_.restoreBrowseFlag(self)

    def header(self):
        return self._h_header

    """
    Establece el cursor
    """

    def setFLSqlCursor(self, c):
        if c and c.metadata():
            cur_chg = False
            if self.cursor_ and not self.cursor_ == c:
                self.cursor_.restoreEditionFlag(self)
                self.cursor_.restoreBrowseFlag(self)
                self.cursor_.bufferCommited.disconnect(self.ensureRowSelectedVisible)

                cur_chg = True

            if not self.cursor_ or cur_chg:
                self.cursor_ = c
                self.setFLReadOnly(self.readonly_)
                self.setEditOnly(self.editonly_)
                self.setInsertOnly(self.insertonly_)
                self.setOnlyTable(self.onlyTable_)

                self.cursor_.bufferCommited.connect(self.ensureRowSelectedVisible)

                self.setModel(self.cursor_.model())
                self.setSelectionModel(self.cursor_.selection())
                self.model().sort(self.visualIndexToRealIndex(0), 0)
                self.installEventFilter(self)
            # if self.cursor_.at() >= 0:
            #    QtCore.QTimer.singleShot(2000, self.marcaRow) #Por ahora es 3000 para que de tiempo a mostrarse FIXME
    """
    Establece un filtro persistente que siempre se aplica al cursor antes
    de hacer un refresh
    """

    def marcaRow(self):
        self.selectRow(self.cursor_.at())

    def setPersistentFilter(self, pFilter):
        self.persistentFilter_ = pFilter

    def setFilter(self, f):
        self.filter_ = f

    """
    retorna el número de columnas
    """

    def numCols(self):

        return self.horizontalHeader().count()

    def setSort(self, s):
        self.sort_ = s
    """
    Devuelve el cursor
    """

    def cursor(self):
        return self.cursor_

    """
    Establece la tabla a sólo lectura o no
    """

    def setFLReadOnly(self, mode):

        if not self.cursor_ or self.cursor_.aqWasDeleted():
            return

        self.cursor_.setEdition(not mode, self)
        self.readonly_ = mode

    def flReadOnly(self):
        return self.readonly_

    """
    Establece la tabla a sólo edición o no
    """

    def setEditOnly(self, mode):

        if not self.cursor_ or self.cursor_.aqWasDeleted():
            return

        self.editonly_ = mode

    def editOnly(self):
        return self.editonly_

    """
    Establece la tabla a sólo insercion o no
    """

    def setInsertOnly(self, mode):

        if not self.cursor_ or self.cursor_.aqWasDeleted():
            return

        self.cursor_.setEdition(not mode, self)
        self.insertonly_ = mode

    def insertOnly(self):
        return self.insertonly_

    """
    Obtiene la lista con las claves primarias de los registros seleccionados por chequeo
    """

    def primarysKeysChecked(self):
        return self.primarysKeysChecked_

    """
    Limpia la lista con las claves primarias de los registros seleccionados por chequeo
    """

    def clearChecked(self):
        self.primarysKeysChecked_.clear()
        for r in self.cursor().model()._checkColumn.keys():
            self.cursor().model()._checkColumn[r].setChecked(False)

    """
    Establece el estado seleccionado por chequeo para un regsitro, indicando el valor de su clave primaria
    """

    def setPrimaryKeyChecked(self, primaryKeyValue, on):
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

    def setShowAllPixmaps(self, s):
        self.showAllPixmaps_ = s

    """
    Ver FLDataTable::functionGetColor_
    """

    def setFunctionGetColor(self, f):

        self.functionGetColor_ = f

    def functionGetColor(self):
        return self.functionGetColor_

    """
    Ver FLDataTable::onlyTable_
    """

    def setOnlyTable(self, on=True):
        if not self.cursor_ or self.cursor_.aqWasDeleted():
            return

        self.cursor_.setEdition(not on, self)
        self.cursor_.setBrowse(not on, self)
        self.onlyTable_ = on

    def onlyTable(self):
        return self.onlyTable_

    """
    Redefinida por conveniencia
    """

    def indexOf(self, i):
        return self.header().visualIndex(i)

    """
    @return El nombre del campo en la tabla de una columna dada
    """

    def fieldName(self, col):

        if not self.cursor_ or self.cursor_.aqWasDeleted():
            return None

        field = self.cursor_.field(self.indexOf(col))
        if not field:
            return None

        return field.name()

    """
    Filtrado de eventos
    """

    def eventFilter(self, o, e):
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
                from pineboolib.pncontrolsfactory import FLCheckBox
                chk = FLCheckBox(self.cellWidget(r, c))
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

    def contextMenuEvent(self, e):
        super(FLDataTable, self).contextMenuEvent(e)

        if not self.cursor_ or not self.cursor_.isValid() or not self.cursor_.metadata():
            return

        mtd = self.cursor_.metadata()
        pri_key = mtd.primaryKey()

        field = mtd.field(pri_key)
        if not field:
            return

        rel_list = field.relationList()
        if not rel_list:
            return

        db = self.cursor_.db()
        pri_key_val = self.cursor_.valueBuffer(pri_key)
        popup = pineboolib.pncontrolsfactory.QMenu(self)

        menu_frame = pineboolib.pncontrolsfactory.QWidget(self, QtCore.Qt.Popup)

        lay = pineboolib.pncontrolsfactory.QVBoxLayout()
        menu_frame.setLayout(lay)

        tmp_pos = e.globalPos()

        for rel in rel_list:
            cur = FLSqlCursor.FLSqlCursor(rel.foreignTable(), True, db.connectionName(), None, None, popup)

            if cur.metadata():
                mtd = cur.metadata()
                field = mtd.field(rel.foreignField())
                if not field:
                    continue

                sub_popup = pineboolib.pncontrolsfactory.QMenu(self)
                sub_popup.setTitle(mtd.alias())
                sub_popup_frame = pineboolib.pncontrolsfactory.QWidget(sub_popup, QtCore.Qt.Popup)
                lay_popup = pineboolib.pncontrolsfactory.QVBoxLayout(sub_popup)
                sub_popup_frame.setLayout(lay_popup)

                dt = pineboolib.pncontrolsfactory.FLDataTable(None, "FLDataTable", True)
                lay_popup.addWidget(dt)

                dt.setFLSqlCursor(cur)
                filter = db.manager().formatAssignValue(field, pri_key_val, False)
                cur.setFilter(filter)
                dt.setFilter(filter)
                dt.refresh()

                horiz_header = dt.header()
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

    def setChecked(self, index):
        row = index.row()
        col = index.column()
        field = self.cursor_.metadata().indexFieldObject(col)
        _type = field.type()

        if _type is not "check":
            return

        pK = str(self.cursor().model().value(row, self.cursor().metadata().primaryKey()))
        self.cursor().model()._checkColumn[pK].setChecked(not self.cursor().model()._checkColumn[pK].isChecked())
        self.setPrimaryKeyChecked(str(pK), self.cursor().model()._checkColumn[pK].isChecked())
    """
    Redefinida por conveniencia
    """

    def focusOutEvent(self, e):
        # setPaletteBackgroundColor(qApp->palette().color(QPalette::Active, QColorGroup::Background)) FIXME
        pass

    """
    Redefinida por conveniencia
    """

    def handleError(self):
        pass

    """
    Redefinida por conveniencia
    """
    @decorators.NotImplementedWarn
    def drawContents(self, p, cx, cy, cw, ch):
        pass

    """ Uso interno """
    changingNumRows_ = None

    def syncNumRows(self):
        # print("syncNumRows")

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

    def paintFieldMtd(self, f, t):

        if self.paintFieldMtd_ and self.paintFieldName_ == f:
            return self.paintFieldMtd_

        self.paintFieldName_ = f
        self.paintFieldMtd_ = t.field(f)
        return self.paintFieldMtd_

    timerViewRepaint_ = None
    """
    Redefinida por conveniencia
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
    Redefinida por conveniencia
    """
    @decorators.Incomplete
    def refresh(self):
        if self.popup_:
            self.cursor_.refresh()
        # if not self.refreshing_ and self.cursor_ and not self.cursor_.aqWasDeleted() and self.cursor_.metadata():
        if not self.refreshing_ and self.cursor():

            if self.functionGetColor_ and self.cursor().model():
                if self.cursor().model().color_function_ != self.functionGetColor_:
                    self.cursor().model().setColorFunction(self.functionGetColor_)

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

            self.cursor().refresh()
            self.marcaRow()
            self.show()
            self.refreshing_ = False

    """
    Hace que la fila seleccionada esté visible
    """
    @QtCore.pyqtSlot()
    def ensureRowSelectedVisible(self):
        if self.cursor():
            if not self.selectedIndexes():
                self.selectRow(self.cursor().at())
            self.scrollTo(self.cursor().model().index(self.cursor().at(), 0))
        # FIXME: Asegurarme de que esté pintada la columna seleccionada

    """
    Foco rápido sin refrescos para optimizar
    """

    def setQuickFocus(self):
        # setPaletteBackgroundColor(qApp->palette().color(QPalette::Active, QColorGroup::Base)); FIXME
        super(FLDataTable, self).setFocus()

    """
    Establece el ancho de una columna

    @param  field Nombre del campo de la base de datos correspondiente a la columna
    @param  w     Ancho de la columna
    """

    def setColumnWidth(self, field, w):
        self.widthCols_.insert(field, w)

    def delayedViewportRepaint(self):
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

    def cursorDestroyed(self, obj=None):

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

    def numRows(self):
        if not self.cursor_:
            return -1

        return self.cursor_.model().rowCount()

    def indexVisualColumn(self, name):

        return

    """
    Retorna el index real (incusive columnas ocultas) a partir de un nombre de un campo
    @param name El nombre del campo a buscar en la tabla
    @return posicion de la columna en la tabla
    """

    def realColumnIndex(self, name):
        # print("FLDataTable:realColumnIndex")
        if not isinstance(name, str) or not self.cursor_:
            return -1

        return self.cursor_.model().metadata().fieldIsIndex(name)

    def mouseDoubleClickEvent(self, e):
        if e.button() != QtCore.Qt.LeftButton:
            return

        settings = FLSettings()
        if not settings.readBoolEntry("ebcomportamiento/FLTableDoubleClick", False):
            self.recordChoosed.emit()

    """
    Retorna el index real a partir de un index de columnas visibles.
    @param c posicion de la columna visible.
    @return posicion real de la columna
    """

    def visualIndexToRealIndex(self, c):
        if not isinstance(c, int) or not self.cursor_:
            return

        visible_id = -1
        ret_ = None
        for column in range(self.model().columnCount()):
            if not self.isColumnHidden(self.header().visualIndex(column)):
                visible_id += 1

                if visible_id == c:
                    ret_ = column
                    break

        return ret_

    def currentRow(self):
        return self.currentIndex().row()

    def currentColumn(self):
        return self.currentIndex().column()
