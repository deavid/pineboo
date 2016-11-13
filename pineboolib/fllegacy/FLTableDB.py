# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from pineboolib import decorators
from pineboolib.fllegacy.FLDataTable import FLDataTable
from pineboolib.fllegacy.FLFormRecordDB import FLFormRecordDB
from pineboolib.fllegacy.FLSqlCursor import FLSqlCursor
from pineboolib.utils import DefFun
from pineboolib.fllegacy.FLRelationMetaData import FLRelationMetaData
from pineboolib.fllegacy.FLFormSearchDB import FLFormSearchDB
from pineboolib.fllegacy.FLFieldMetaData import FLFieldMetaData



class FLTableDB(QtGui.QWidget):

    """
    PLUGIN que contiene una tabla de la base de datos.

    Este objeto contiene todo lo necesario para manejar
    los datos de una tabla. Además de la funcionalidad de
    busqueda en la tabla por un campo, mediante filtros.

    Este plugin para que sea funcional debe tener como uno
    de sus padres o antecesor a un objeto FLFormDB.

    @author InfoSiAL S.L.
    """

    """
    Tipos de condiciones para el filtro
    """
    All = None
    Contains = None
    Starts = None
    End = None
    Equal = None
    Dist = None
    Greater = None
    Less = None
    FromTo = None
    Null = None
    NotNull = None


    _parent = None
    _name = None
    loadLater_ = None




    comboBoxFieldToSearch = None
    comboBoxFieldToSearch2 = None
    tableRecords_ = None
    lineEditSearch = None

    tabDataLayout = None
    tabControlLayout = None

    _initCursorWhenLoad = None
    _initTableRecordWhenLoad = None


    _controlsInit = None

    """
    constructor
    """

    def __init__(self, parent, name = None):
        super(FLTableDB, self).__init__(parent)

        self.timer_1 = QtCore.QTimer(self)
        self.timer_1.singleShot(0, self.loaded)
        self.topWidget = parent

    def __getattr__(self, name):
        return DefFun(self, name)






    def loaded(self):
        # Es necesario pasar a modo interactivo lo antes posible
        # Sino, creamos un bug en el cierre de ventana: se recarga toda la tabla para saber el tamaño
        #print("FLTableDB(%s): setting columns in interactive mode" % self._tableName)
        self._loaded = True
        while True: #Ahora podemos buscar el cursor ... porque ya estamos añadidos al formulario
            parent_cursor = getattr(self.topWidget,"cursor_", None)
            if parent_cursor: break
            new_parent = self.topWidget.parentWidget()
            if new_parent is None: break
            self.topWidget = new_parent
        
        
        if getattr(self.topWidget.parentWidget(), "cursor_", None):
            self.topWidget = self.topWidget.parentWidget()
            
        if not parent_cursor:
            print("FLTableDB : Uno de los padres o antecesores de FLTableDB deber ser de la clase FLFormDB o heredar de ella")
            return

        self.cursor_ = self.topWidget.cursor_
        self.setFont(QtGui.qApp.font())

        if not self._name:
            self.setName("FLTableDB")

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.refreshDelayed)

        self.showWidget()








        self.initCursor()
    def setName(self, name):
        self._name = name




    """
    Para obtener el cursor utilizado por el componente.

    return Objeto FLSqlCursor con el cursor que contiene los registros para ser utilizados en el formulario
    """
    def cursor(self):
        if not self.cursor_.d.buffer_:
            self.cursor_.refreshBuffer()
        return self.cursor_

    """
    Para obtener el nombre de la tabla asociada.

    @return Nombre de la tabla asociado
    """
    def tableName(self):
        return self.tableName_


    """
    Para establecer el nombre de la tabla asociada.

    @param fT Nombre de la tabla asociada
    """
    def setTableName(self, fT):
        self.tableName_ = fT
        if self.showed:
            if self.topwidget:
                self.initCursor()
            else:
                self.initFakeEditor()

        else:
            self._initCursorWhenLoad = True
            self._initTableRecordWhenLoad = True


    """
    Para obtener el nombre del campo foráneo.

    @return Nombre del campo
    """
    def foreignField(self):
        return self.foreignField_

    """
    Para establecer el nombre del campo foráneo.

    @param fN Nombre del campo
    """
    def setForeignField(self, fN):
        self.foreignField_ = fN
        if self.showed:
            if self.topwidget:
                self.initCursor()
            else:
                self.initFakeEditor()
        else:
            self._initCursorWhenLoad = True
            self._initTableRecordWhenLoad = True
    """
    Para obtener el nombre del campo relacionado.

    @return Nombre del campo
    """
    def fieldRelation(self):
        return self.fieldRelation_

    """
    Para establecer el nombre del campo relacionado.

    @param fN Nombre del campo
    """
    def setFieldRelation(self, fN):
        self.fieldRelation_ = fN
        if self.showed:
            if self.topwidget:
                self.initCursor()
            else:
                self.initFakeEditor()

        else:
            self._initCursorWhenLoad = True
            self._initTableRecordWhenLoad = True
    """
    Establece si el componente esta en modo solo lectura o no.
    """
    def setReadOnly(self, mode):
        if self.tableRecords_:
            self.readonly = mode
            self.tableRecords_.setFLReadOnly(mode)
            #self.readOnlyChanged(mode).emit() FIXME

        self.reqReadOnly_ = mode


    def readOnly(self):
        return self.reqReadOnly_

    """
    Establece si el componente esta en modo solo edición o no.
    """
    def setEditOnly(self, mode):
        if self.tableRecords_:
            self.editonly_ = mode
            self.tableRecords_.setEditOnly(mode)
            #self.editOnlyChanged(mode).emit() #FIXME

        self.reqEditOnly_ = mode

    def editOnly(self):
        return self.reqEditOnly_

    """
    Establece el componente a sólo inserción o no.
    """
    def setInsertOnly(self, mode):
        if self.tableRecords_:
            self.insertonly_ = mode
            self.tableRecords_.setInsertOnly(mode)
            self.insertOnlyChanged(mode).emit()

        self.reqInsertOnly = mode

    def insertOnly(self):
        return self.reqInsertOnly_

    """
    Establece el filtro inicial de búsqueda
    """
    def setInitSearch(self, iS):
        self.initSearch_ = iS

    """
    Establece el orden de las columnas de la tabla.

    @param fields Lista de los nombres de los campos ordenada según se desea que aparezcan en la tabla de izquierda a derecha
    """
    @decorators.NotImplementedWarn
    def setOrderCols(self, fields):
        pass

    """
    Devuelve la lista de los campos ordenada por sus columnas en la tabla de izquierda a derecha
    """
    @decorators.NotImplementedWarn
    def orderCols(self):
        return None

    """
    Establece el filtro de la tabla

    @param f Sentencia Where que establece el filtro
    """
    @decorators.NotImplementedWarn
    def setFilter(self, f):
        pass

    """
    Devuelve el filtro de la tabla

    @return Filtro
    """
    @decorators.NotImplementedWarn
    def filter(self):
        return None

    """
    Devuelve el filtro de la tabla impuesto en el Find

    @return Filtro
    """
    @decorators.NotImplementedWarn
    def findFilter(self):
        return None

    """
    Obtiene si la columna de selección está activada
    """
    @decorators.NotImplementedWarn
    def checkColumnEnabled(self):
        return None

    """
    Establece el estado de activación de la columna de selección

    El cambio de estado no será efectivo hasta el siguiente refresh.
    """
    @decorators.NotImplementedWarn
    def setCheckColumnEnabled(self, b):
        pass

    """
    Obiente el texto de la etiqueta de encabezado para la columna de selección
    """
    @decorators.NotImplementedWarn
    def aliasCheckColumn(self):
        pass


    """
    Establece el texto de la etiqueta de encabezado para la columna de selección

    El cambio del texto de la etiqueta no será efectivo hasta el próximo refresh
    """
    @decorators.NotImplementedWarn
    def setAliasCheckColumn(self, t):
        pass

    """
    Obtiene si el marco de búsqueda está oculto
    """
    @decorators.NotImplementedWarn
    def findHidden(self):
        return None

    """
    Oculta o muestra el marco de búsqueda

    @param  h TRUE lo oculta, FALSE lo muestra
    """
    @decorators.NotImplementedWarn
    def setFindHidden(self, h):
        pass

    """
    Obtiene si el marco para conmutar entre datos y filtro está oculto
    """
    @decorators.NotImplementedWarn
    def filterHidden(self):
        return None

    """
    Oculta o muestra el marco para conmutar entre datos y filtro

    @param  h TRUE lo oculta, FALSE lo muestra
    """
    @decorators.NotImplementedWarn
    def setFilterHidden(self, h):
        pass

    """
    Ver FLTableDB::showAllPixmaps_
    """
    @decorators.NotImplementedWarn
    def showAllPixmaps(self):
        return None

    """
    Ver FLTableDB::showAllPixmaps_
    """
    @decorators.NotImplementedWarn
    def setShowAllPixmaps(self, s):
        pass

    """
    Ver FLTableDB::functionGetColor_
    """
    @decorators.NotImplementedWarn
    def functionGetColor(self):
        pass

    """
    Ver FLTableDB::functionGetColor_
    """
    @decorators.NotImplementedWarn
    def setFunctionGetColor(self, f):
        pass

    """
    Asigna el nombre de función a llamar cuando cambia el filtro.
    """
    def setFilterRecordsFunction(self, fn):
        self.tableDB_filterRecords_functionName_ = fn

    """
    Ver FLTableDB::onlyTable_
    """
    @decorators.NotImplementedWarn
    def setOnlyTable(self, on = True):
        pass

    def onlyTable(self):
        return self.reqOnlyTable_

    """
    Ver FLTableDB::autoSortColumn_
    """
    @decorators.NotImplementedWarn
    def setAutoSortColumn(self, on = True):
        self.autoSortColumn_ = on

    def autoSortColumn(self):
        return self.autoSortColumn_



    """
    Filtro de eventos
    """

    def eventFilter(self, obj, ev):
        if not self.tableRecords_ or not self.lineEditSearch or not self.comboBoxFieldToSearch or not self.comboBoxFieldToSearch2 or not self.cursor_:
            return super(FLTableDB, self).eventFilter(obj, ev)

        if ev.type() == QtCore.QEvent.KeyPress and isinstance(obj, FLDataTable):
            k = ev

            if k.key() == QtCore.Qt.Key_F2:
                self.comboBoxFieldToSearch.popup()
                return True

        if ev.type() == QtCore.QEvent.KeyPress and isinstance(obj, QtGui.QLineEdit):
            k = ev

            if k.key() == QtCore.Qt.Key_Enter or k.key() == QtCore.Qt.Key_Return:
                self.tableRecords_.setFocus()
                return True


            if k.key() == QtCore.Qt.Key_Up:
                self.comboBoxFieldToSearch.setFocus()
                return True

            if k.key() == QtCore.Qt.Key_Down:
                self.tableRecords_.setFocus()
                return True

            if k.key() == QtCore.Qt.Key_F2:
                self.comboBoxFieldToSearch.popup()
                return True

            if k.text() == "'" or k.text() == "\\":
                return True

        if isinstance(obj, FLDataTable) or isinstance(obj, QtGui.QLineEdit):
            return False
        else:
            return super(FLTableDB, self).eventFilter(obj, ev)



    """
    Captura evento mostrar
    """
    def showEvent(self, e):
        super(FLTableDB, self).showEvent(e)
        self.showWidget()





    """
    Redefinida por conveniencia
    """

    def showWidget(self):
        if not self._loaded: #Esperamos a que la carga se realice
            timer = QtCore.QTimer(self)
            timer.singleShot(30, self.showWidget)
            return
        else:
            if not self.showed and not self._initCursorWhenLoad and self.cursor_ and self.tableRecords_:
                if not self.topWidget:
                    self.initFakeEditor()
                    self.showed = True
                    return

                tMD = None
                ownTMD = None
                if self.tableName_:
                    if not self.cursor_.db().manager().existsTable(self.tableName_):
                        ownTMD = True
                        tMD = self.cursor_.db().manager().createTable(self.tableName_)
                    else:
                        ownTMD = True
                        tMD = self.cursor_.db().manager().metadata(self.tableName_)

                    if not tMD:
                        return







                if not self.cursorAux:
                    if self.initSearch_:
                        self.refresh(True, True)
                        QtCore.QTimer.singleShot(0, self.tableRecords_.ensureRowSelectedVisible)
                    else:
                        self.refresh(True)
                        if self.tableRecords_.numRows() <= 0:
                            self.refresh(False, True)
                        else:
                            self.refreshDelayed()

                    if not isinstance(self.topWidget, FLFormRecordDB):
                        self.lineEditSearch.setFocus()

                if self.cursorAux:
                    if isinstance(self.topWidget, FLFormRecordDB) and self.cursorAux.modeAccess() == FLSqlCursor.Browse:
                        self.cursor_.setEdition(False)
                        self.setReadOnly(True)

                    if self.initSearch_:
                        self.refresh(True, True)
                        QtCore.QTimer.singleShot(0, self.tableRecords_.ensureRowSelectedVisible)
                    else:
                        self.refresh(True)
                        if self.tableRecords_.numRows() <= 0:
                            self.refresh(False, True)
                        else:
                            self.refreshDelayed()

                elif isinstance(self.topWidget, FLFormRecordDB) and self.cursor_.modeAccess() == FLSqlCursor.Browse and (tMD and not tMD.isQuery()):
                    self.cursor_.setEdition(False)
                    self.setReadOnly(True)


                if ownTMD and tMD and not tMD.inCache():
                    del tMD


            if self._initCursorWhenLoad:
                self._initCursorWhenLoad = False
                self.initCursor()
                self.showWidget()

            if not self.tableRecords_:
                if not self.tableName_:
                    if not self.cursor_:
                        self.initCursor()
                        QtCore.QTimer.singleShot(50, self.showWidget)
                        return
                    self.tableRecords()
                    self.setTableRecordsCursor()
                    self.showWidget()
                elif self.tableName_:
                    if not self.cursor_:
                        self.initCursor()
                        QtCore.QTimer.singleShot(50, self.showWidget)
                        return

                    if self.tableName_ == self.cursor_.curName():
                        self.tableRecords()
                        if self.cursor_.model():
                            self.setTableRecordsCursor()
                            self.showWidget()






    """
    Obtiene el componente tabla de registros
    """
    def tableRecords(self):

        self.tabDataLayout = QtGui.QVBoxLayout()
        self.comboBoxFieldToSearch = QtGui.QComboBox()
        self.comboBoxFieldToSearch2 = QtGui.QComboBox()
        self.lineEditSearch = QtGui.QLineEdit()
        label1 = QtGui.QLabel()
        label2 = QtGui.QLabel()

        label1.setText("Buscar")
        label2.setText("en")

        self.tabControlLayout = QtGui.QHBoxLayout()

        self.tabControlLayout.addWidget(label1)
        self.tabControlLayout.addWidget(self.lineEditSearch)
        self.tabControlLayout.addWidget(label2)
        self.tabControlLayout.addWidget(self.comboBoxFieldToSearch)
        self.tabControlLayout.addWidget(self.comboBoxFieldToSearch2)

        self.tabDataLayout.addLayout(self.tabControlLayout)


        if not self.tableRecords_:
            self.tableRecords_ = FLDataTable(self, "tableRecords")
            self.tableRecords_.setFocusPolicy(QtCore.Qt.StrongFocus)
            self.setFocusProxy(self.tableRecords_)
            self.tabDataLayout.addWidget(self.tableRecords_)
            self.lineEditSearch.installEventFilter(self)
            self.tableRecords_.installEventFilter(self)

            self.setLayout(self.tabDataLayout)
            self.setTabOrder(self.tableRecords_, self.lineEditSearch)
            self.setTabOrder(self.lineEditSearch, self.comboBoxFieldToSearch)
            self.setTabOrder(self.comboBoxFieldToSearch, self.comboBoxFieldToSearch2)

        self.lineEditSearch.textChanged.connect(self.filterRecords)
        model = self.cursor_.model()

        if model:
            for column in range(model.columnCount()):
                field = model.metadata().indexFieldObject(column)
                if not field.visibleGrid():
                    self.tableRecords_.setColumnHidden(column, True)
                else:
                    self.comboBoxFieldToSearch.addItem(model.headerData(column, QtCore.Qt.Horizontal, QtCore.Qt.DisplayRole))
                    self.comboBoxFieldToSearch2.addItem(model.headerData(column, QtCore.Qt.Horizontal, QtCore.Qt.DisplayRole))
            self.comboBoxFieldToSearch.addItem("*")
            self.comboBoxFieldToSearch2.addItem("*")
            self.comboBoxFieldToSearch.setCurrentIndex(0)
            self.comboBoxFieldToSearch2.setCurrentIndex(1)
            self.comboBoxFieldToSearch.currentIndexChanged.connect(self.putFirstCol)
            self.comboBoxFieldToSearch2.currentIndexChanged.connect(self.putSecondCol)
            self._controlsInit = True

        else:
            self.comboBoxFieldToSearch.addItem("*")
            self.comboBoxFieldToSearch2.addItem("*")

        return self.tableRecords_






    """
    Asigna el cursor actual del componente a la tabla de registros
    """

    def setTableRecordsCursor(self):
        self.tableRecords_.setFLSqlCursor(self.cursor_)
        try:
            self.tableRecords_.doubleClicked.disconnect(self.chooseRecord)
        except:
            pass
        self.tableRecords_.doubleClicked.connect(self.chooseRecord)

    """
    Refresca la pestaña datos aplicando el filtro
    """
    @decorators.NotImplementedWarn
    def refreshTabData(self):
        pass

    """
    Refresca la pestaña del filtro
    """
    @decorators.NotImplementedWarn
    def refreshTabFilter(self):
        pass

    """
    Para obtener la enumeración correspondiente a una condición para el filtro a partir de
    su literal
    """
    @decorators.NotImplementedWarn
    def decodeCondType(self, strCondType):
        pass

    """
    Construye la claúsula de filtro en SQL a partir del contenido de los valores
    definidos en la pestaña de filtro
    """
    @decorators.NotImplementedWarn
    def tdbFilterBuildWhere(self):
        pass

    """
    Inicializa un editor falso y no funcional.

    Esto se utiliza cuando se está editando el formulario con el diseñador y no
    se puede mostrar el editor real por no tener conexión a la base de datos.
    Crea una previsualización muy esquemática del editor, pero suficiente para
    ver la posisicón y el tamaño aproximado que tendrá el editor real.
    """
    @decorators.NotImplementedWarn
    def initFakeEditor(self):
        pass

    """
    Componente para visualizar los registros
    """
    tableRecords_ = None

    """
    Nombre de la tabla a la que esta asociado este componente.
    """
    tableName_ = None

    """
    Nombre del campo foráneo
    """
    foreignField_ = None

    """
    Nombre del campo de la relación
    """
    fieldRelation_ = None

    """
    Cursor con los datos de origen para el componente
    """
    cursor_ = None

    """
    Cursor auxiliar de uso interno para almacenar los registros de la tabla
    relacionada con la de origen
    """
    cursorAux = None

    """
    Matiene la ventana padre
    """
    topWidget = None

    """
    Indica que la ventana ya ha sido mostrada una vez
    """
    showed = None

    """
    Mantiene el filtro de la tabla
    """
    filter_ = None

    """
    Almacena si el componente está en modo sólo lectura
    """
    readonly_ = None
    reqReadOnly_ = None

    """
    Almacena si el componente está en modo sólo edición
    """
    editonly_ = None
    reqEditOnly_ = None

    """
    Indica si el componente está en modo sólo permitir añadir registros
    """
    insertonly_ = None
    reqInsertOnly_ = None

    """
    Almacena los metadatos del campo por el que está actualmente ordenada la tabla
    """
    sortField_ = None

    """
    Almacena los metadatos del campo por el que está actualmente ordenada la tabla en segunda instancia

    @author Silix - dpinelo
    """
    sortField2_ = None

    """
    Crónometro interno
    """
    timer = None

    """
    Filtro inicial de búsqueda
    """
    initSearch_ = None

    """
    Indica que la columna de seleción está activada
    """
    checkColumnEnabled_ = None

    """
    Indica el texto de la etiqueta de encabezado para la columna de selección
    """
    aliasCheckColumn_ = None

    """
    Indica el nombre para crear un pseudocampo en el cursor para la columna de selección
    """
    fieldNameCheckColumn_ = None

    """
    Indica que la columna de selección está visible
    """
    checkColumnVisible_ = None

    """
    Indica el número de columna por la que ordenar los registros
    """
    sortColumn_ = None

    """
    Indica el número de columna por la que ordenar los registros

    @author Silix - dpinelo
    """
    sortColumn2_ = None

    """
    Indica el número de columna por la que ordenar los registros

    @author Silix
    """
    sortColumn3_ = None

    """
    Indica el sentido ascendente o descendente del la ordenacion actual de los registros
    """
    orderAsc_ = None

    """
    Indica el sentido ascendente o descendente del la ordenacion actual de los registros

    @author Silix - dpinelo
    """
    orderAsc2_ = None

    """
    Indica el sentido ascendente o descendente del la ordenacion actual de los registros

    @author Silix
    """
    orderAsc3_ = None

    """
    Indica si se debe establecer automáticamente la primera columna como de ordenación
    """
    autoSortColumn_ = None

    """
    Almacena la última claúsula de filtro aplicada en el refresco
    """
    tdbFilterLastWhere_ = None

    """
    Diccionario que relaciona literales descriptivos de una condición de filtro
    con su enumeración
    """
    mapCondType = []

    """
    Indica si el marco de búsqueda está oculto
    """
    findHidden_ = None

    """
    Indica si el marco para conmutar entre datos y filtro está oculto
    """
    filterHidden_ = None

    """
    Indica si se deben mostrar los campos tipo pixmap en todas las filas
    """
    showAllPixmaps_ = None

    """
    Nombre de la función de script a invocar para obtener el color y estilo de las filas y celdas

    El nombre de la función debe tener la forma 'objeto.nombre_funcion' o 'nombre_funcion',
    en el segundo caso donde no se especifica 'objeto' automáticamente se añadirá como
    prefijo el nombre del formulario donde se inicializa el componente FLTableDB seguido de un punto.
    De esta forma si utilizamos un mismo formulario para varias acciones, p.e. master.ui, podemos controlar
    si usamos distintas funciones de obtener color para cada acción (distintos nombres de formularios) o
    una única función común para todas las acciones.

    Ej. Estableciendo 'tdbGetColor' si el componente se inicializa en el formulario maestro de clientes,
    se utilizará 'formclientes.tdbGetColor', si se inicializa en el fomulario maestro de proveedores, se
    utilizará 'formproveedores.tdbGetColor', etc... Si establecemos 'flfactppal.tdbGetColor' siempre se llama a
    esa función independientemente del formulario en el que se inicialize el componente.

    Cuando se está pintando una celda se llamará a esa función pasándole cinco parámentros:
    - Nombre del campo correspondiente a la celda
    - Valor del campo de la celda
    - Cursor de la tabla posicionado en el registro correspondiente a la fila que
      está pintando. AVISO: En este punto los valores del buffer son indefinidos, no se hace refreshBuffer
      por motivos de eficiencia
    - Tipo del campo, ver FLUtilInterface::Type en FLObjectFactory.h
    - Seleccionado. Si es TRUE indica que la celda a pintar está en la fila resaltada/seleccionada.
      Generalmente las celdas en la fila seleccionada se colorean de forma distinta al resto.

    La función debe devolver una array con cuatro cadenas de caracteres;

    [ "color_de_fondo", "color_lapiz", "estilo_fondo", "estilo_lapiz" ]

    En los dos primeros, el color, se puede utilizar cualquier valor aceptado por QColor::setNamedColor, ejemplos;

    "green"
    "#44ADDB"

    En los dos últimos, el estilo, se pueden utilizar los valores aceptados por QBrush::setStyle y QPen::setStyle,
    ver en FLDataTable.cpp las funciones nametoBrushStyle y nametoPenStyle, ejemplos;

    "SolidPattern"
    "DiagCrossPattern"
    "DotLine"
    "SolidLine"

    Si alguno de los valores del array es vacio "", entonces se utilizarán los colores o estilos establecidos por defecto.
    """
    functionGetColor_ = None

    """
    Indica que no se realicen operaciones con la base de datos (abrir formularios). Modo "sólo tabla".
    """
    onlyTable_ = None
    reqOnlyTable_ = None

    """
    Editor falso
    """
    fakeEditor_ = None

    tableDB_filterRecords_functionName_ = None


    """
    Actualiza el conjunto de registros.
    """
    @decorators.BetaImplementation
    @QtCore.pyqtSlot()
    @QtCore.pyqtSlot(bool)
    @QtCore.pyqtSlot(bool, bool)
    def refresh(self, refreshHead = False, refreshData = False):
        if not self.cursor_ or not self.tableRecords_:
            return

        tMD = self.cursor_.metadata()
        if not tMD:
            return

        if not self.tableName_:
            self.tableName_ = tMD.name()




        if refreshHead:
            if not self.tableRecords_.isHidden():
                self.tableRecords_.hide()

            model = self.cursor_.model()

            for column in range(model.columnCount()):
                field = model.metadata().indexFieldObject(column)
                if not field.visibleGrid():
                    self.tableRecords_.setColumnHidden(column, True)
                else:
                    self.tableRecords_.setColumnHidden(column, False)

            # FIXME: Este proceso es MUY LENTO. No deberíamos hacer esto.
            # Hay que buscar alguna forma manual de iterar las primeras N filas, o calcular un
            # valor por defecto rápidamente.
            self.tableRecords_._h_header.setResizeMode(QtGui.QHeaderView.ResizeToContents)
            if model.rows * model.cols > 500*10:
                # Esto evitará que se calcule para las que tienen más de 500*10 celdas.
                self.tableRecords_._h_header.setResizeMode(0)
            # ... de todos modos tendríamos que, con un timer o algo para desactivar el modo. Una vez
            # ... ya redimensionadas inicialmente, lo único que hace es lastrar Pineboo mucho.




        if refreshData or self.sender():

            finalFilter = self.filter_
            if self.tdbFilterBuildWhere_:
                if not finalFilter:
                    finalFilter = self.tdbFilterLastWhere_
                else:
                    finalFilter = "%s and %s" % (finalFilter, self.tdbFilterLastWhere_)

            self.tableRecords_.setPersistentFilter(finalFilter)
            self.tableRecords_.refresh()




        if self.initSearch_:
            try:
                self.lineEditSearch.textChanged.disconnect(self.filterRecords)
            except:
                pass
            self.lineEditSearch.setText(self.initSearch_)
            self.lineEditSearch.textChanged.connect(self.filterRecords)
            self.lineEditSearch.selectAll()
            self.initSearch_ = None
            self.seekCursor()

        if not self.readonly_ == self.reqReadOnly_ or (self.tableRecords_ and not self.readonly_ == self.tableRecords_.flReadOnly()):
            self.setReadOnly(self.reqReadOnly_)

        if not self.editonly_ == self.reqEditOnly_ or (self.tableRecords_ and not self.editonly_ == self.tableRecords_.editOnly()):
            self.setEditOnly(self.reqEditOnly_)


        if not self.insertonly_ == self.reqInsertOnly_ or (self.tableRecords_ and not self.insertonly_ == self.tableRecords_.insertOnly()):
            self.setInsetOnly(self.reqInsertOnly_)

        if not self.onlyTable_ == self.reqOnlyTable_ or (self.tableRecords_ and not self.onlyTable_ == self.tableRecords_.onlyTable()):
            self.setOnlyTable(self.reqOnlyTable_)

        if self.tableRecords_ and self.tableRecords_.isHidden():
            self.tableRecords_.show()

    """
    Actualiza el conjunto de registros con un retraso.

    Acepta un lapsus de tiempo en milisegundos, activando el cronómetro interno para
    que realize el refresh definitivo al cumplirse dicho lapsus.

    @param msec Cantidad de tiempo del lapsus, en milisegundos.
    """
    def refreshDelayed(self, msec = 50, refreshData = True):

        if not self.cursor_.modeAccess() == FLSqlCursor.Browse:
            return


        if refreshData:
            self._refreshData = True
        else:
            self._refreshData = False
            QtCore.QTimer.singleShot(msec, self.refreshDelayed2)

        self.seekCursor()

    def refreshDelayed2(self):
        self.refresh(False, self._refreshData)
        self._refreshData = None

    """
    Invoca al método FLSqlCursor::insertRecord()
    """
    @QtCore.pyqtSlot()
    def insertRecord(self):

        w = self.sender()
        if w and (not self.cursor_ or self.reqReadOnly_ or self.reqEditOnly_ or self.reqOnlyTable_ or (self.cursor_.cursorRelation() and self.cursor_.cursorRelation().isLocked())):
            w.setDisabled(True)
            return

        if self.cursor_:
            self.cursor_.insertRecord()

    """
    Invoca al método FLSqlCursor::editRecord()
    """
    @QtCore.pyqtSlot()
    def editRecord(self):
        w = self.sender()
        if w and (not self.cursor_ or self.reqReadOnly_ or self.reqEditOnly_ or self.reqOnlyTable_ or (self.cursor_.cursorRelation() and self.cursor_.cursorRelation().isLocked())):
            w.setDisabled(True)
            return

        if self.cursor_:
            self.cursor_.editRecord()
    """
    Invoca al método FLSqlCursor::browseRecord()
    """
    @QtCore.pyqtSlot()
    def browseRecord(self):

        w = self.sender()
        if w and (not self.cursor_ or self.reqOnlyTable_):
            w.setDisaBled(True)
            return

        if self.cursor_:
            self.cursor_.browseRecord()

    """
    Invoca al método FLSqlCursor::deleteRecord()
    """
    @QtCore.pyqtSlot()
    def deleteRecord(self):
        w = self.sender()
        if w and (not self.cursor_ or self.reqReadOnly_ or self.reqInsertOnly_ or self.reqEditOnly_ or self.reqOnlyTable_ or (self.cursor_.cursorRelation() and self.cursor_.cursorRelation().isLocked())):
            w.setDisabled(True)
            return

        if self.cursor_:
            self.cursor_.deleteRecord()

    """
    Invoca al método FLSqlCursor::copyRecord()
    """
    @QtCore.pyqtSlot()
    def copyRecord(self):
        w = self.sender()
        if w and (not self.cursor_ or self.reqReadOnly_ or self.reqEditOnly_ or self.reqOnlyTable_ or (self.cursor_.cursorRelation() and self.cursor_.cursorRelation().isLocked())):
            w.setDisabled(True)
            return

        if self.cursor_:
            self._cursor.copyRecord()

    """
    Coloca la columna como primera pasando el nombre del campo.

    Este slot está conectado al cuadro combinado de busqueda
    del componente. Cuando seleccionamos un campo este se coloca
    como primera columna y se reordena la tabla con esta columna.
    De esta manera siempre tendremos la tabla ordenada mediante
    el campo en el que queremos buscar.

    @param c Nombre del campo, esta columna intercambia su posion con la primera columna
    @return Falso si no existe el campo
    @author viernes@xmarts.com.mx
    @author InfoSiAL, S.L.
    """
    @QtCore.pyqtSlot(int)
    @QtCore.pyqtSlot(str)
    def putFirstCol(self, c ):
        _index = c
        if isinstance(c, str):
            _index = self.tableRecords_.realColumnIndex(c)

        if _index < 0:
            return False

        self.moveCol(_index, 0)
        return True

    """
    Coloca la columna como segunda pasando el nombre del campo.

    @author Silix - dpinelo
    """
    @QtCore.pyqtSlot(int)
    @QtCore.pyqtSlot(str)
    def putSecondCol(self, c):
        _index = c
        if isinstance(c, str):
            _index = self.tableRecords_.realColumnIndex(c)

        if _index < 0:
            return False

        self.moveCol(_index, 1)
        return True

    """
    Mueve una columna de un campo origen a la columna de otro campo destino

    @param  from  Nombre del campo de la columna de origen
    @param  to    Nombre del campo de la columna de destino
    @param  firstSearch dpinelo: Indica si se mueven columnas teniendo en cuenta que esta función
            se ha llamado o no, desde el combo principal de búsqueda y filtrado
    """
    @decorators.BetaImplementation
    def moveCol(self, from_,  to, firstSearch = True ):

        _oldFirst = None

        if from_ < 0 or to < 0:
            return

        tMD = self.cursor_.metadata()
        if not tMD:
            return

        self.tableRecords_.hide()


        textSearch = self.lineEditSearch.text()



        field = self.cursor_.metadata().indexFieldObject(to)

        if to == 0: # Si ha cambiado la primera columna


            try:
                self.comboBoxFieldToSearch.currentIndexChanged.disconnect(self.putFirstCol)
            except:
                pass

            self.comboBoxFieldToSearch.setCurrentIndex(from_)
            self.comboBoxFieldToSearch.currentIndexChanged.connect(self.putFirstCol)

            #Actializamos el segundo combo
            try:
                self.comboBoxFieldToSearch2.currentIndexChanged.disconnect(self.putSecondCol)
            except:
                pass
            #Falta mejorar
            if self.comboBoxFieldToSearch.currentIndex() == self.comboBoxFieldToSearch2.currentIndex():
                self.comboBoxFieldToSearch2.setCurrentIndex(self.tableRecords_._h_header.logicalIndex(0))
            self.comboBoxFieldToSearch2.currentIndexChanged.connect(self.putSecondCol)




        if (to == 1): #Si es la segunda columna ...
            try:
                self.comboBoxFieldToSearch2.currentIndexChanged.disconnect(self.putSecondCol)
            except:
                pass
            self.comboBoxFieldToSearch2.setCurrentIndex(from_)
            self.comboBoxFieldToSearch2.currentIndexChanged.connect(self.putSecondCol)


            if self.comboBoxFieldToSearch.currentIndex() == self.comboBoxFieldToSearch2.currentIndex():
                try:
                    self.comboBoxFieldToSearch.currentIndexChanged.disconnect(self.putFirstCol)
                except:
                    pass
                if self.comboBoxFieldToSearch.currentIndex() == self.comboBoxFieldToSearch2.currentIndex():
                    self.comboBoxFieldToSearch.setCurrentIndex(self.tableRecords_._h_header.logicalIndex(1))
                self.comboBoxFieldToSearch.currentIndexChanged.connect(self.putFirstCol)


        if not textSearch:
            textSearch = self.cursor_.value(field.name())

        self.refresh(True)

        if textSearch:
            self.refresh(False, True)
            try:
                self.lineEditSearch.textChanged.disconnect(self.filterRecords)
            except:
                pass
            self.lineEditSearch.setText(textSearch)
            self.lineEditSearch.textChanged.connect(self.filterRecords)
            self.lineEditSearch.selectAll()
            self.seekCursor()
            QtCore.QTimer.singleShot(0, self.tableRecords_.ensureRowSelectedVisible())
        else:
            self.refreshDelayed()



        from_ = self.tableRecords_.visualIndexToRealIndex(from_)
        self.tableRecords_._h_header.swapSections(from_, to)

        self.refresh(True)

        """
        if textSearch:
            self.refresh(False, True)

            if firstSearch:
                self.lineEditSearch.textChanged.disconnect(self.filterRecords)
                self.lineEditSearch.setText(textSearch)
                self.lineEditSearch.textChanged.connect(self.filterRecords)
                self.lineEditSearch.selectAll()

            self.seekCursor()
            QtCore.QTimer.singleShot(0,self.tableRecords_.ensureRowSelectedVisible)
        else:
            self.refreshDelayed()
            if not self.sender():
                self.lineEditSearch.setFocus()

        """
        #self.tableRecords_.show()
    """
    Inicia el cursor segun este campo sea de la tabla origen o de
    una tabla relacionada
    """
    def initCursor(self):
        if not self.topWidget or not self.cursor_:
            return

        if not self.cursor_.metadata():
            return

        tMD = None

        if not self.sortField_:
            tMD = self.cursor_.metadata()
            if tMD:
                self.sortField_ = tMD.field(tMD.primaryKey())


        ownTMD = None
        if self.tableName_:
            if not self.cursor_.db().manager().existsTable(self.tableName_):
                ownTMD = True
                tMD = self.cursor_.db().manager().createTable(self.tableName_)
            else:
                ownTMD = True
                tMD = self.cursor_.db().manager().metadata(self.tableName_)

            if not tMD:
                return

            if not self.foreignField_ or not self.fieldRelation_:
                if not self.cursor_.metadata():
                    if ownTMD and tMD and not tMD.inCache():
                        del tMD
                    return

                if not self.cursor_.metadata().name() == self.tableName_:
                    ctxt = self.cursor_.context()
                    self.cursor_ = FLSqlCursor(self.tableName_, True, self.cursor_.db().connectionName(), None, None , self)


                    if self.cursor_:
                        self.cursor_.setContext(ctxt)
                        self.cursorAux = None

                    if ownTMD and tMD and not tMD.inCache():
                        del tMD

                    return

            else:
                cursorTopWidget = self.topWidget.cursor()
                if cursorTopWidget and not cursorTopWidget.metadata().name() == self.tableName_:
                    self.cursor_ = cursorTopWidget

        if not self.tableName_ or not self.foreignField_ or not self.fieldRelation_ or self.cursorAux:
            if ownTMD and tMD and not tMD.inCache():
                del tMD

            return

        self.cursorAux = self.cursor_
        curName = self.cursor_.metadata().name()
        rMD =  self.cursor_.metadata().relation(self.foreignField_, self.fieldRelation_, self.tableName_)
        testM1 = tMD.relation(self.fieldRelation_, self.foreignField_, curName)
        checkIntegrity = False
        if not rMD:
            if testM1:
                if testM1.cardinality() == FLRelationMetaData.RELATION_M1:
                    checkIntegrity = True
            fMD = self.cursor_.metadata().field(self.foreignField_)
            if fMD:
                tmdAux = self.cursor_.db().manager().metadata(self.tableName_)
                if not tmdAux or tmdAux.isQuery():
                    checkIntegrity = False
                if tmdAux and not tmdAux.inCache():
                    del tmdAux

                rMD = FLRelationMetaData(self.tableName_, self.fieldRelation_, FLRelationMetaData.RELATION_1M, False, False, checkIntegrity)
                fMD.addRelationMD(rMD)
                #print("FLTableDB : La relación entre la tabla del formulario %s y esta tabla %s de este campo no existe, pero sin embargo se han indicado los campos de relación( %s, %s )" % ( curName, self.tableName_, self.fieldRelation_, self.foreignField_))
                #print("FLTableDB : Creando automáticamente %s.%s --1M--> %s.%s" % (curName, self.foreignField_, self.tableName_, self.fieldRelation_))
            else:
                #print("FLTableDB : El campo ( %s ) indicado en la propiedad foreignField no se encuentra en la tabla ( %s )" % (self.foreignField_, curName))
                pass

        rMD = testM1
        if not rMD:
            fMD = tMD.field(self.fieldRelation_)
            if fMD:
                rMD = FLRelationMetaData(curName, self.foreignField_, FLRelationMetaData.RELATION_1M, False, False, False)
                fMD.addRelationMD(rMD)
                print("FLTableDB : Creando automáticamente %s.%s --1M--> %s.%s" % (self.tableName_, self.fieldRelation_, curName, self.foreignField_))

            else:
                print("FLTableDB : El campo ( %s ) indicado en la propiedad fieldRelation no se encuentra en la tabla ( %s )" % (self.fieldRelation_, self.tableName_))

        self.cursor_ = FLSqlCursor(self.tableName_, True, self.cursor_.db().connectionName(), self.cursorAux, rMD, self)
        if not self.cursor_:
            self.cursor_ = self.cursorAux
            self.cursorAux = None

        else:

            self.cursor_.setContext(self.cursorAux.context())
            if self.showed:
                try:
                    self.cursorAux.newBuffer.disconnect(self.refresh)
                except:
                    pass

            self.cursorAux.newBuffer.connect(self.refresh)

        if self.cursorAux and isinstance(self.topWidget, FLFormSearchDB):
            self.topWidget.setCaption(self.cursor_.metadata().alias())
            self.topWidget_.setCursor(self.cursor_)

        if ownTMD or tMD and not tMD.inCache():
            del tMD



    """
    Posiciona el cursor en un registro valido
    """
    @decorators.NotImplementedWarn
    def seekCursor(self):
        return
        textSearch = self.lineEditSearch.text()
        if not textSearch:
            return

        if not self.cursor_:
            return

        fN = self.sortField_.name()
        textSearch.replace("%", "")

        if not "'" in textSearch and not "\\" in textSearch:
            sql = self.cursor_.executedQuery() + " LIMIT 1"
        """
            #QSqlQuery qry(sql, cursor_->db()->db()); #FIXME
            if (qry.first()) {
      QString v(qry.value(0).toString());
      int pos = -1;
      if (!v.upper().startsWith(textSearch.upper()))
        pos = cursor_->atFromBinarySearch(fN, textSearch, orderAsc_);
      if (pos == -1)
        pos = cursor_->atFromBinarySearch(fN, v, orderAsc_);
      cursor_->seek(pos, false, true);
      """
    """
    Redefinida por conveniencia
    """
    @decorators.NotImplementedWarn
    def setEnabled(self, b):
        pass

    """
    Establece el ancho de una columna

    @param  field Nombre del campo de la base de datos correspondiente a la columna
    @param  w     Ancho de la columna
    """
    @decorators.NotImplementedWarn
    def setColumnWidth(self, field, w):
        pass

    """
    @return Ancho de la columna
    """
    @decorators.NotImplementedWarn
    def columnWidth(self, c):
        pass

    """
    Establece el alto de una fila

    @param  row Número de orden de la fila, empezando en 0
    @param  h   Alto de la fila
    """
    @decorators.NotImplementedWarn
    def setRowHeight(self, row, h):
        pass
    """
    @return Alto de la fila
    """
    @decorators.NotImplementedWarn
    def rowHeight(self, row):
        pass

    """
    Exporta a una hoja de cálculo ODS y la visualiza
    """
    @decorators.NotImplementedWarn
    def exportToOds(self):
        pass

    """
    Conmuta el sentido de la ordenación de los registros de la tabla, de ascendente a descendente y
    viceversa. Los registros siempre se ordenan por la primera columna.
    Si la propiedad autoSortColumn es TRUE.
    """
    @decorators.NotImplementedWarn
    def switchSortOrder(self, col = 0):
        pass


    """
    Filtra los registros de la tabla utilizando el primer campo, según el patrón dado.

    Este slot está conectado al cuadro de texto de busqueda del componente,
    tomando el contenido de este como patrón para el filtrado.

    @param p Cadena de caracteres con el patrón de filtrado
    """
    @QtCore.pyqtSlot(str)
    def filterRecords(self, p):
        if not self.cursor_.model():
            return
        bFilter = None
        p = str(p)
        refreshData = None
        if "%" in p:
            refreshData = True
        msec_refresh = 400
        column = self.tableRecords_._h_header.logicalIndex(0)
        field = self.cursor_.model().metadata().indexFieldObject(column)

        bFilter = self.cursor_.db().manager().formatAssignValue(field, p, True)

        idMod = self.cursor_.db().managerModules().idModuleOfFile(self.cursor_.metadata().name() + ".mtd")

        functionQSA = idMod + ".tableDB_filterRecords_" + self.cursor_.metadata().name()

        vargs = []
        vargs.append(self.cursor_.metadata().name())
        vargs.append(p)
        vargs.append(field.name())
        vargs.append(bFilter)

        if functionQSA:
            msec_refresh = 800
            ret = self.cursor_._prj.call(functionQSA, vargs, None)
            if ret:
                bFilter = ret
                print("functionQSA:%s:" % functionQSA)
            else:
                if p == "":
                    bFilter = None


        self.refreshDelayed(msec_refresh, (bFilter or refreshData))
        self.filter_ = bFilter


    @decorators.NotImplementedWarn
    def setSortOrder(self, ascending):
        pass

    @decorators.NotImplementedWarn
    def isSortOrderAscending(self):
        pass

    """
    Activa la tabla de datos
    """
    @decorators.NotImplementedWarn
    def activeTabData(self, b):
        pass

    """
    Activa la tabla de filtro
    """
    @decorators.NotImplementedWarn
    def activeTabFilter(self, b):
        pass

    """
    Limpia e inicializa el filtro
    """
    @decorators.NotImplementedWarn
    def tdbFilterClear(self):
        pass


    """
    Señal emitida cuando se refresca por cambio de filtro
    """
    refreshed = QtCore.pyqtSignal()

    """
    Señal emitida cuando se establece si el componente es o no de solo lectura.
    """
    readOnlyChanged = QtCore.pyqtSignal(bool)

    """
    Señal emitida cuando se establece si el componente es o no de solo edición.
    """
    editOnlyChanged = QtCore.pyqtSignal(bool)

    """
    Señal emitida cuando se establece si el componente es o no de solo inserción.
    """
    insertOnlyChanged = QtCore.pyqtSignal(bool)

    """
    Señal emitida cuando se establece cambia el registro seleccionado.
    """
    #currentChanged = QtCore.pyqtSignal()

    @QtCore.pyqtSlot()
    @decorators.BetaImplementation
    def chooseRecord(self):
        if isinstance(self.topWidget, FLFormSearchDB):
            if self.topWidget.inExec_:
                    self.topWidget.accept()
                    return
            
        if self.cursor().isLocked():
            print("FLTable(%s):Registro bloqueado. Modo Solo lectura" % self.cursor().curName())
            self.browseRecord()
        else:   
            self.editRecord()
