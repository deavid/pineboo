# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from pineboolib import decorators
from pineboolib.utils import filedir
from pineboolib.fllegacy import FLSqlCursor


class FLDataTable(QtGui.QTableView):
  
    """
    Clase que es una redefinicion de la clase QDataTable,
    especifica para las necesidades de AbanQ.

    @author InfoSiAL S.L.
    """

    """
    constructor
    """
    _parent = None

    def __init__(self, parent = None, name = None, popup = False):
        super(FLDataTable, self).__init__(parent)
        
        if parent: 
            self._parent = parent
        
        if not name:
            self.setName("FLDataTable")
        
        self.pixOk_ = filedir("icons","unlock.png")
        self.pixNo_ = filedir("icons","lock.png")
        
        self._v_header = self.verticalHeader()
        self._v_header.setDefaultSectionSize(18)
        self._h_header = self.horizontalHeader()
        self._h_header.setDefaultSectionSize(70)
        self._h_header.setResizeMode(QtGui.QHeaderView.Interactive)
        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.setAlternatingRowColors(True)
        
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
    

    """
    Establece el cursor
    """
    def setFLSqlCursor(self, c):
        if c and c.metadata():           
            curChg = None
            if self.cursor_ and not self.cursor_ == c:
                self.cursor_.restoreEditionFlag(self)
                self.cursor_.restoreBrowseFlag(self)
                curChg = True
            
            self.cursor_ = c
            
            if self.cursor_:
                if curChg:
                    self.setFLReadOnly(self.readonly_)
                    self.setEditOnly(self.editonly_)
                    self.setInsertOnly(self.insertonly_)
                    self.setOnlyTable(self.onlyTable_)
                                
            self.setModel(self.cursor_.model())
            self.setSelectionModel(self.cursor_.selection())
            #if self.cursor_.at() >= 0:
            #    QtCore.QTimer.singleShot(2000, self.marcaRow) #Por ahora es 3000 para que de tiempo a mostrarse FIXME
    """
    Establece un filtro persistente que siempre se aplica al cursor antes
    de hacer un refresh
    """
    
    def marcaRow(self):

        self.selectRow(self.cursor_.at())
    
    def setPersistentFilter(self, pFilter):
        self.persistentFilter_ = pFilter
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
    @decorators.NotImplementedWarn
    def primarysKeysChecked(self):
        pass

    """
    Limpia la lista con las claves primarias de los registros seleccionados por chequeo
    """
    def clearChecked(self):
        self.primarysKeysChecked_ = []

    """
    Establece el estado seleccionado por chequeo para un regsitro, indicando el valor de su clave primaria
    """
    def setPrimaryKeyChecked(self, primaryKeyValue, on):
        return self.primarysKeysChecked_

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
    @decorators.NotImplementedWarn
    def setOnlyTable(self, on = True):
        pass
    
    def onlyTable(self):
        return self.onlyTable_
    
    """
    Redefinida por conveniencia
    """
    
    def indexOf(self, i):
        return super(FLDataTable, self).indexOf(i)
        
  
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
    @decorators.NotImplementedWarn
    def eventFilter(self, o, e):
        pass

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
    def paintField(self, p, field,  cr, selected):
        pass

    """
    Redefinido por conveniencia, para evitar que aparezca el menu contextual
    con las opciones para editar registros
    """
    @decorators.NotImplementedWarn
    def contentsContextMenuEvent(self, e):
        pass
    """
    Redefine por conveniencia, el comportamiento al hacer doble clic sobre una
    celda
    """
    @decorators.NotImplementedWarn
    def contentsMouseDoubleClickEvent(self, e):
        pass

    """
    Redefinida por conveniencia
    """
    def focusOutEvent(self, e):
        #setPaletteBackgroundColor(qApp->palette().color(QPalette::Active, QColorGroup::Background)) FIXME
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
    refreshing_ = None
    refresh_timer_ = None

    """
    Indica si el componente es emergente ( su padre es un widget del tipo Popup )
    """
    popup_ = None
    
    """
    Indica el ancho de las columnas establecidas explícitamente con FLDataTable::setColumnWidth
    """
    widthCols_ =[]

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

    """ Uso interno """
    changingNumRows_ = None
    
    def syncNumRows(self):
        
        if self.changingNumRows_:
            return
        
        if not self.numRows() == self.cursor_.size():
            self.changingNumRows_ = True
            self.setNumRows(self.cursor_.sizze())
            self.changingNumRows_ = False
            

    """ Uso interno """
    @decorators.NotImplementedWarn
    def getCellStyle(self, brush, pen, field,fieldTMD, row, selected, cg):
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
            #setPaletteBackgroundColor(qApp->palette().color(QPalette::Active, QColorGroup::Base)); FIXME
            super(FLDataTable, self).refresh()
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
            
        if not self.refreshing_ and self.cursor_ and not self.cursor_.aqWasDeleted() and self.cursor_.metadata():
            self.refreshing_ = True
            if self.persistentFilter_:
                self.cursor_.setFilter(self.persistentFilter_)
            self.cursor_.refresh() 
            
            
            QtCore.QTimer.singleShot(0, self.show)
        self.refreshing_ = False
    
    
                   

    """
    Hace que la fila seleccionada esté visible
    """
    @decorators.NotImplementedWarn
    def ensureRowSelectedVisible(self):
        pass
    """
        if self.rowSelected > -1:
            if not self.isUpdatesEnabled() or not self.viewport().isUpdaesEnabled():
                return
            
            cw = self.columnWidth(self.colSelected)
            margin = self.visibleHeight() / 2
            y = self.rowPos(self.rowSelected) + self.rowHeight(self.rowSelected) / 2
            if cw < self.visibleWidth():
                self.ensureVisible(self.columnPos(self.colSelected) + cw /2, y, cw /2, margin)
            else:
                self.ensureVisible(self.columnPos(self.colSelected), y, None, margin)
  
    """
    """
    Foco rápido sin refrescos para optimizar
    """
    def setQuickFocus(self):
        #setPaletteBackgroundColor(qApp->palette().color(QPalette::Active, QColorGroup::Base)); FIXME
        super(FLDataTable, self).setFocus()

    """
    Establece el ancho de una columna

    @param  field Nombre del campo de la base de datos correspondiente a la columna
    @param  w     Ancho de la columna
    """
    def setColumnWidth(self, field, w):
        self.widthCols_.insert(field, w)
    
    """
    Activado cuando se hace click en el chequeo de la columna de selección
    """
    def setChecked(self, on):
        
        chk = self.sender()
        if not chk or not self.cursor_ or self.cursor_.aqWasDeleted() or not self.cursor_.metadata():
            return 
        
        curAt = self.cursor_.at()
        posAt = chk.row()
        
        if self.cursor_.seek(posAt):
            primaryKeyValue= self.cursor_.value(self.cursor_.metadata().primaryKey())
            self.setPrimaryKeyChecked(primaryKeyValue, on)
            self.cursor_.seek(curAt)


    def delayedViewportRepaint(self):
        if not self.timerViewRepaint_:
            self.timerViewRepaint_ = QtCore.QTimer(self)
            self.timerViewRepaint_.timeout.connect(self.repaintViewportSlot())
        
        if not self.timerViewRepaint_.isActive():
            self.setUpdatesEnabled(False)
            self.timerViewRepaint_.start(50)
    

    def repaintViewportSlot(self):
        
        vw = self.viewport()
        self.setUpdatesEnabled(True)
        if vw:
            vw.repaint(False)
        
    
    def cursorDestroyed(self, obj = None):
        
        if not obj or not isinstance(obj , FLSqlCursor ):
            return
        
        self.cursor_ = None
             


    """
    Indica que se ha elegido un registro
    """
    recordChoosed = QtCore.pyqtSignal()
    

    def currentChanged(self, row, row2):
        self.cursor_.selection_currentRowChanged(row, row2)

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
        
        return self.cursor_.model().columnCount()
    
    def indexVisualColumn(self, name):
        
            return
        
        
    """
    Retorna el index real (incusive columnas ocultas) a partir de un nombre de un campo
    @param name El nombre del campo a buscar en la tabla
    @return posicion de la columna en la tabla
    """
    
    def realColumnIndex(self, name):
        if not isinstance(name, str) or not self.cursor_:
            return -1
      
        return self.cursor_.model().metadata().fieldIsIndex(name)
        
        
    """
    Retorna el index real (incusive columnas ocultas) a partir de un index de columnas visibles.
    @param c posicion de la columna visible.
    @return posicion real de la columna
    """   
    def visualIndexToRealIndex(self, c):  
        if not isinstance(c, int) or not self.cursor_:return
        
        model = self.cursor_.model()
        posReal = 0
        posVisual = 0
        _return = None
        for column in range(model.columnCount()):
            field = model.metadata().indexFieldObject(column)
            if not field.visibleGrid():
                posVisual = posVisual - 1
            else:
                if c == posVisual:
                    _return = posReal
                    break
            
            posVisual = posVisual + 1    
            posReal = posReal + 1
        
        _return = self._h_header.visualIndex(posReal)      
        return _return
                
        
             
            
                 
            
            
        
        
        
        
class FLCheckBox(QtGui.QCheckBox):
    
    row_ = None
    
    def __init__(self, parent, row = 0, name = 0):
        super(FLCheckBox, self).__init__(parent, name)
        
        self.row_ = row
    
    def row(self):
        return self.row_
    
    def drawButton(self, p):
        rect = None
        wrect = self.rect()
        
        rect = QtCore.QRect((wrect.width -13) /2, (wrect.height -13) /2, 13 ,13)
        if self.isChecked():
            bu = QtGui.QBrush(QtCore.Qt.green)
            p.fillRect(0, 0, wrect.width() -1, wrect.height() -1, bu)
        
        #irect = QtGui.QStyle.visualRect(Qt_LayoutDirection, QRect, QRect)
        irect = QtGui.QStyle().visualRect(self.layoutDirection() , rect, self.rect())
        p.fillRect(irect, QtCore.Qt.white)
        p.drawRect(irect)
        
    
    def hitButton(self, pos):
        
        return self.rect().contains(pos)
    

#endif