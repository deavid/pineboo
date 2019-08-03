# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets  # type: ignore
from PyQt5.QtCore import Qt  # type: ignore
from PyQt5.QtGui import QPixmap  # type: ignore

from pineboolib import logging
from pineboolib.core import decorators
from pineboolib.application.qsatypes.sysbasetype import SysBaseType
from .fldatatable import FLDataTable
from .flformsearchdb import FLFormSearchDB
from .flsqlcursor import FLSqlCursor


from pineboolib.application.metadata.pnrelationmetadata import PNRelationMetaData
from pineboolib.application.metadata.pnfieldmetadata import PNFieldMetaData

from .flutil import FLUtil
from pineboolib.core.settings import config
from .flapplication import aqApp


from typing import Any, Optional, List, Union


logger = logging.getLogger(__name__)
DEBUG = False


class FLTableDB(QtWidgets.QWidget):

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
    All = 0
    Contains = 1
    Starts = 2
    End = 3
    Equal = 4
    Dist = 5
    Greater = 6
    Less = 7
    FromTo = 8
    Null = 9
    NotNull = 10

    _parent = None
    _name: str
    loadLater_ = None

    tdbFilter: Optional[Any] = None

    pbData = None
    pbFilter = None
    pbOdf = None

    comboBoxFieldToSearch: QtWidgets.QComboBox
    comboBoxFieldToSearch2: QtWidgets.QComboBox
    lineEditSearch: QtWidgets.QLineEdit

    tabDataLayout = None
    tabControlLayout = None

    dataLayout = None
    tabData = None
    tabFilter = None
    buttonsLayout = None
    masterLayout = None
    tabFilterLoaded: bool

    _controlsInit = None

    _loaded: bool
    """
    Tamaño de icono por defecto
    """
    iconSize: Optional[Any] = None

    """
    Componente para visualizar los registros
    """
    tableRecords_: Optional[FLDataTable] = None

    """
    Nombre de la tabla a la que esta asociado este componente.
    """
    tableName_: Optional[str] = None

    """
    Nombre del campo foráneo
    """
    foreignField_: Optional[str] = None

    """
    Nombre del campo de la relación
    """
    fieldRelation_: Optional[str] = None

    """
    Cursor con los datos de origen para el componente
    """
    cursor_: Any = None

    """
    Cursor auxiliar de uso interno para almacenar los registros de la tabla
    relacionada con la de origen
    """
    cursorAux: Any = None

    """
    Matiene la ventana padre
    """
    topWidget: Any = None

    """
    Indica que la ventana ya ha sido mostrada una vez
    """
    showed = False

    """
    Mantiene el filtro de la tabla
    """
    filter_: str = ""

    """
    Almacena si el componente está en modo sólo lectura
    """
    readonly_: bool
    reqReadOnly_: bool

    """
    Almacena si el componente está en modo sólo edición
    """
    editonly_: bool
    reqEditOnly_: bool

    """
    Indica si el componente está en modo sólo permitir añadir registros
    """
    insertonly_: bool
    reqInsertOnly_: bool

    """
    Almacena los metadatos del campo por el que está actualmente ordenada la tabla
    """
    sortField_: Optional[PNFieldMetaData]

    """
    Almacena los metadatos del campo por el que está actualmente ordenada la tabla en segunda instancia

    @author Silix - dpinelo
    """
    sortField2_: Optional[PNFieldMetaData]

    """
    Crónometro interno
    """
    timer: Optional[QtCore.QTimer]

    """
    Filtro inicial de búsqueda
    """
    initSearch_: Optional[str]

    """
    Indica que la columna de seleción está activada
    """
    checkColumnEnabled_: bool

    """
    Indica el texto de la etiqueta de encabezado para la columna de selección
    """
    aliasCheckColumn_: str

    """
    Indica el nombre para crear un pseudocampo en el cursor para la columna de selección
    """
    fieldNameCheckColumn_: str

    """
    Indica que la columna de selección está visible
    """
    checkColumnVisible_: bool

    """
    Indica el número de columna por la que ordenar los registros
    """
    sortColumn_: int = 0

    """
    Indica el número de columna por la que ordenar los registros

    @author Silix - dpinelo
    """
    sortColumn2_: int

    """
    Indica el número de columna por la que ordenar los registros

    @author Silix
    """
    sortColumn3_: int

    """
    Indica el sentido ascendente o descendente del la ordenacion actual de los registros
    """
    orderAsc_: bool

    """
    Indica el sentido ascendente o descendente del la ordenacion actual de los registros

    @author Silix - dpinelo
    """
    orderAsc2_: bool

    """
    Indica el sentido ascendente o descendente del la ordenacion actual de los registros

    @author Silix
    """
    orderAsc3_: bool

    """
    Indica si se debe establecer automáticamente la primera columna como de ordenación
    """
    autoSortColumn_: bool

    """
    Almacena la última claúsula de filtro aplicada en el refresco
    """
    tdbFilterLastWhere_: Optional[str] = None

    """
    Diccionario que relaciona literales descriptivos de una condición de filtro
    con su enumeración
    """
    mapCondType: List[str]

    """
    Indica si el marco de búsqueda está oculto
    """
    findHidden_: bool

    """
    Indica si el marco para conmutar entre datos y filtro está oculto
    """
    filterHidden_: bool

    """
    Indica si se deben mostrar los campos tipo pixmap en todas las filas
    """
    showAllPixmaps_: bool

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
    functionGetColor_: Optional[str]

    """
    Indica que no se realicen operaciones con la base de datos (abrir formularios). Modo "sólo tabla".
    """
    onlyTable_: bool
    reqOnlyTable_: bool

    """
    Editor falso
    """
    fakeEditor_: Optional[Any] = None

    tableDB_filterRecords_functionName_: Optional[str]

    def __init__(
        self, parent: Optional["QtWidgets.QWidget"] = None, name: Optional[str] = None
    ) -> None:
        """
        constructor
        """
        if parent is None:
            return
        super(FLTableDB, self).__init__(parent)
        self.topWidget = parent
        self.showAllPixmaps_ = True
        self.sortColumn_ = 0
        self.sortColumn2_ = 1
        self.sortColumn3_ = 2
        self.sortField_ = None
        self.initSearch_ = None
        self.autoSortColumn_ = True
        self.orderAsc_ = True
        self.orderAsc2_ = True
        self.orderAsc3_ = True
        self.readonly_ = False
        self.editonly_ = False
        self.onlyTable_ = False
        self.insertonly_ = False
        self.reqReadOnly_ = False
        self.reqEditOnly_ = False
        self.reqInsertOnly_ = False
        self.reqOnlyTable_ = False
        self.tabFilterLoaded = False
        self.timer_1 = QtCore.QTimer(self)
        if name:
            self.setObjectName(name)
        self.checkColumnVisible_ = False
        self.checkColumnEnabled_ = False
        self.tdbFilterLastWhere_: Optional[str] = None
        self.filter_ = ""
        from pineboolib.application import project

        if project._DGI is not None:
            self.iconSize = project.DGI.iconSize()

        self.tabControlLayout = QtWidgets.QHBoxLayout()
        self.tabFilter = QtWidgets.QFrame()  # contiene filtros
        self.tabData = QtWidgets.QFrame()  # contiene data
        self.functionGetColor_ = None

        from .flformdb import FLFormDB

        while not isinstance(self.topWidget, FLFormDB):
            self.topWidget = self.topWidget.parentWidget()
            if not self.topWidget:
                break

        self._loaded = False
        self.createFLTableDBWidget()

    # def __getattr__(self, name):
    #    return DefFun(self, name)

    def load(self) -> None:

        # Es necesario pasar a modo interactivo lo antes posible
        # Sino, creamos un bug en el cierre de ventana: se recarga toda la tabla para saber el tamaño
        # print("FLTableDB(%s): setting columns in interactive mode" % self._tableName))
        if self.loaded():
            return

        if self.topWidget is not None:
            if not self.topWidget.cursor():
                logger.warning(
                    "FLTableDB : Uno de los padres o antecesores de FLTableDB deber ser de la clase FLFormDB o heredar de ella"
                )
                return

            self.cursor_ = self.topWidget.cursor()

        self.initCursor()
        # self.setFont(QtWidgets.QApplication.font())

        if not self.objectName():
            self.setObjectName("FLTableDB")

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.refreshDelayed)

        # FIXME: El problema de que aparezca al editar un registro que no es, es por carga doble de initCursor()
        # ...... Cuando se lanza showWidget, y tiene _initCursorWhenLoad, lanza initCursor y luego otra vez.
        # ...... esta doble carga provoca el error y deja en el formulario el cursor original.

        self.mapCondType = []

        self._loaded = True
        self.showWidget()

        if DEBUG:
            logger.warning(
                "**FLTableDB::name: %r cursor: %r", self.objectName(), self.cursor().d.nameCursor_
            )

    def loaded(self) -> bool:
        return self._loaded

    def initCursor(self) -> None:
        """
        Inicia el cursor segun este campo sea de la tabla origen o de
        una tabla relacionada
        """
        if not self.topWidget or not self.cursor():
            return

        if not self.cursor().metadata():
            return

        tMD = self.cursor().metadata()
        if self.sortField_ is None:
            if tMD is not None:
                self.sortField_ = tMD.field(tMD.primaryKey())

        ownTMD = None
        if self.tableName_:
            if DEBUG:
                logger.warning(
                    "**FLTableDB::name: %r tableName: %r", self.objectName(), self.tableName_
                )

            if not self.cursor().db().manager().existsTable(self.tableName_):
                ownTMD = True
                tMD = self.cursor().db().manager().createTable(self.tableName_)
            else:
                ownTMD = True
                manager_tmd = self.cursor().db().manager().metadata(self.tableName_)

                if not manager_tmd or isinstance(manager_tmd, bool):
                    return

                tMD = manager_tmd

            if not self.foreignField_ or not self.fieldRelation_:
                if not self.cursor().metadata():
                    if ownTMD and tMD and not tMD.inCache():
                        del tMD
                    return

                if not self.cursor().metadata().name() == self.tableName_:
                    ctxt = self.cursor().context()
                    self.cursor_ = FLSqlCursor(
                        self.tableName_, True, self.cursor().db().connectionName(), None, None, self
                    )

                    if self.cursor():
                        self.cursor().setContext(ctxt)
                        self.cursorAux = None

                    if ownTMD and tMD and not tMD.inCache():
                        del tMD

                    return

            else:
                cursorTopWidget = self.topWidget.cursor()
                if cursorTopWidget and cursorTopWidget.metadata().name() != self.tableName_:
                    self.cursor_ = cursorTopWidget

        if (
            not self.tableName_
            or not self.foreignField_
            or not self.fieldRelation_
            or self.cursorAux
        ):
            if ownTMD and tMD and not tMD.inCache():
                del tMD

            return

        self.cursorAux = self.cursor()
        curName = self.cursor().metadata().name()
        rMD = (
            self.cursor()
            .metadata()
            .relation(self.foreignField_, self.fieldRelation_, self.tableName_)
        )
        testM1 = tMD.relation(self.fieldRelation_, self.foreignField_, curName)
        checkIntegrity = False
        if not rMD:
            if testM1:
                if testM1.cardinality() == PNRelationMetaData.RELATION_M1:
                    checkIntegrity = True
            fMD = self.cursor().metadata().field(self.foreignField_)
            if fMD is not None:
                tmdAux = self.cursor().db().manager().metadata(self.tableName_)
                if not tmdAux or tmdAux.isQuery():
                    checkIntegrity = False
                if tmdAux and not tmdAux.inCache():
                    del tmdAux

                rMD = PNRelationMetaData(
                    self.tableName_,
                    self.fieldRelation_,
                    PNRelationMetaData.RELATION_1M,
                    False,
                    False,
                    checkIntegrity,
                )
                fMD.addRelationMD(rMD)
                logger.warning(
                    "FLTableDB : La relación entre la tabla del formulario %s y esta tabla %s de este campo no existe, "
                    "pero sin embargo se han indicado los campos de relación( %s, %s )",
                    curName,
                    self.tableName_,
                    self.fieldRelation_,
                    self.foreignField_,
                )
                logger.trace(
                    "FLTableDB : Creando automáticamente %s.%s --1M--> %s.%s",
                    curName,
                    self.foreignField_,
                    self.tableName_,
                    self.fieldRelation_,
                )
            else:
                logger.warning(
                    "FLTableDB : El campo ( %s ) indicado en la propiedad foreignField no se encuentra en la tabla ( %s )",
                    self.foreignField_,
                    curName,
                )
                pass

        rMD = testM1
        if not rMD:
            fMD = tMD.field(self.fieldRelation_)
            if fMD is not None:
                rMD = PNRelationMetaData(
                    curName, self.foreignField_, PNRelationMetaData.RELATION_1M, False, False, False
                )
                fMD.addRelationMD(rMD)
                if DEBUG:
                    logger.trace(
                        "FLTableDB : Creando automáticamente %s.%s --1M--> %s.%s",
                        self.tableName_,
                        self.fieldRelation_,
                        curName,
                        self.foreignField_,
                    )

            else:
                if DEBUG:
                    logger.warning(
                        "FLTableDB : El campo ( %s ) indicado en la propiedad fieldRelation no se encuentra en la tabla ( %s )",
                        self.fieldRelation_,
                        self.tableName_,
                    )

        self.cursor_ = FLSqlCursor(
            self.tableName_, True, self.cursor().db().connectionName(), self.cursorAux, rMD, self
        )
        if not self.cursor():
            self.cursor_ = self.cursorAux
            self.cursorAux = None

        else:
            self.cursor().setContext(self.cursorAux.context())
            if self.showed:
                try:
                    self.cursorAux.newBuffer.disconnect(self.refresh)
                except Exception:
                    pass

            self.cursorAux.newBuffer.connect(self.refresh)

        # Si hay cursorTopWidget no machaco el cursor de topWidget
        if self.cursorAux and isinstance(self.topWidget, FLFormSearchDB) and not cursorTopWidget:
            self.topWidget.setCaption(self.cursor().metadata().alias())
            self.topWidget.setCursor(self.cursor())

        if ownTMD or tMD and not tMD.inCache():
            del tMD

    def cursor(self) -> FLSqlCursor:
        """
        Para obtener el cursor utilizado por el componente.

        return Objeto FLSqlCursor con el cursor que contiene los registros para ser utilizados en el formulario
        """
        # if not self.cursor().buffer():
        #    self.cursor().refreshBuffer()
        return self.cursor_

    def tableName(self) -> str:
        """
        Para obtener el nombre de la tabla asociada.

        @return Nombre de la tabla asociado
        """
        if not self.tableName_:
            raise Exception("tableName_ is empty!")
        return self.tableName_

    def setTableName(self, fT: str) -> None:
        """
        Para establecer el nombre de la tabla asociada.

        @param fT Nombre de la tabla asociada
        """
        self.tableName_ = fT
        if self.topWidget:
            self.initCursor()
        else:
            self.initFakeEditor()

    def foreignField(self) -> Optional[str]:
        """
        Para obtener el nombre del campo foráneo.

        @return Nombre del campo
        """
        return self.foreignField_

    def setForeignField(self, fN: str) -> None:
        """
        Para establecer el nombre del campo foráneo.

        @param fN Nombre del campo
        """
        self.foreignField_ = fN
        if self.topWidget:
            self.initCursor()
        else:
            self.initFakeEditor()

    def fieldRelation(self) -> Optional[str]:
        """
        Para obtener el nombre del campo relacionado.

        @return Nombre del campo
        """
        return self.fieldRelation_

    def setFieldRelation(self, fN: str) -> None:
        """
        Para establecer el nombre del campo relacionado.

        @param fN Nombre del campo
        """
        self.fieldRelation_ = fN
        if self.topWidget:
            self.initCursor()
        else:
            self.initFakeEditor()

    def setReadOnly(self, mode: bool) -> None:
        """
        Establece si el componente esta en modo solo lectura o no.
        """

        if self.tableRecords_:
            self.readonly_ = mode
            self.tableRecords_.setFLReadOnly(mode)
            self.readOnlyChanged.emit(mode)

        self.reqReadOnly_ = mode

    def readOnly(self) -> bool:
        return self.reqReadOnly_

    def setEditOnly(self, mode: bool) -> None:
        """
        Establece si el componente esta en modo solo edición o no.
        """
        if self.tableRecords_:
            self.editonly_ = mode
            self.tableRecords_.setEditOnly(mode)
            self.editOnlyChanged.emit(mode)

        self.reqEditOnly_ = mode

    def editOnly(self) -> bool:
        return self.reqEditOnly_

    def setInsertOnly(self, mode: bool) -> None:
        """
        Establece el componente a sólo inserción o no.
        """
        if self.tableRecords_:
            self.insertonly_ = mode
            self.tableRecords_.setInsertOnly(mode)
            self.insertOnlyChanged.emit(mode)

        self.reqInsertOnly_ = mode

    def insertOnly(self) -> bool:
        return self.reqInsertOnly_

    def setInitSearch(self, iS: str) -> None:
        """
        Establece el filtro inicial de búsqueda
        """
        self.initSearch_ = iS

    @decorators.BetaImplementation
    def setOrderCols(self, fields: List[str]):
        """
        Establece el orden de las columnas de la tabla.

        @param fields Lista de los nombres de los campos ordenada según se desea que aparezcan en la tabla de izquierda a derecha
        """
        if not self.cursor() or not self.tableRecords_:
            return
        tMD = self.cursor().metadata()
        if not tMD:
            return

        if not self.showed:
            self.showWidget()

        fieldsList = []

        for f in fields:
            fmd = tMD.field(f)
            if fmd is not None:
                if fmd.visibleGrid():
                    fieldsList.append(f)

        hCount = self.cursor().model().columnCount()

        if len(fieldsList) > hCount:
            return

        i = 0
        for fi in fieldsList:
            _index = self.tableRecords_.column_name_to_column_index(fi)
            self.moveCol(_index, i)
            i = i + 1

        if not self.lineEditSearch:
            raise Exception("lineEditSearch is not defined!")

        self.setSortOrder(True)
        textSearch = self.lineEditSearch.text()
        self.refresh(True)

        if textSearch:
            self.refresh(False, True)

            try:
                self.lineEditSearch.textChanged.disconnect(self.filterRecords)
            except Exception:
                pass
            self.lineEditSearch.setText(textSearch)
            self.lineEditSearch.textChanged.connect(self.filterRecords)
            self.lineEditSearch.selectAll()
            self.seekCursor()
            QtCore.QTimer.singleShot(0, self.tableRecords_.ensureRowSelectedVisible)
        else:
            self.refreshDelayed()

    @decorators.BetaImplementation
    def orderCols(self) -> List[str]:
        """
        Devuelve la lista de los campos ordenada por sus columnas en la tabla de izquierda a derecha
        """
        list_: List[str] = []

        if not self.cursor():
            return list_

        tMD = self.cursor().metadata()
        if not tMD:
            return list_

        if not self.showed:
            self.showWidget()

        model = self.cursor().model()

        if model:
            if not self.tableRecords_:
                raise Exception("tableRecords_ is not defined!")

            for column in range(model.columnCount()):
                list_.append(
                    self.tableRecords_._model.headerData(
                        column, QtCore.Qt.Horizontal, QtCore.Qt.DisplayRole
                    )
                )

        return list_

    def setFilter(self, f: str) -> None:
        """
        Establece el filtro de la tabla

        @param f Sentencia Where que establece el filtro
        """
        self.filter_ = f

    def filter(self) -> str:
        """
        Devuelve el filtro de la tabla

        @return Filtro
        """
        return self.filter_

    def findFilter(self) -> Optional[str]:
        """
        Devuelve el filtro de la tabla impuesto en el Find

        @return Filtro
        """
        return self.tdbFilterLastWhere_

    def checkColumnEnabled(self) -> bool:
        """
        Obtiene si la columna de selección está activada
        """
        return self.checkColumnEnabled_

    def setCheckColumnEnabled(self, b: bool) -> None:
        """
        Establece el estado de activación de la columna de selección

        El cambio de estado no será efectivo hasta el siguiente refresh.
        """
        self.checkColumnEnabled_ = b

    @decorators.BetaImplementation
    def aliasCheckColumn(self) -> Optional[str]:
        """
        Obiente el texto de la etiqueta de encabezado para la columna de selección
        """
        if not self.tableRecords_:
            raise Exception("tableRecords_ is not defined!")

        return self.tableRecords_._model.headerData(
            self.tableRecords_.selectionModel().selectedColumns(),
            QtCore.Qt.Horizontal,
            QtCore.Qt.DisplayRole,
        )

    def setAliasCheckColumn(self, t: str) -> None:
        """
        Establece el texto de la etiqueta de encabezado para la columna de selección

        El cambio del texto de la etiqueta no será efectivo hasta el próximo refresh
        """
        self.aliasCheckColumn_ = t

    def findHidden(self) -> bool:
        """
        Obtiene si el marco de búsqueda está oculto
        """
        return self.findHidden_

    @decorators.Deprecated
    def setFindHidden(self, h: bool) -> None:
        """
        Oculta o muestra el marco de búsqueda

        @param  h TRUE lo oculta, FALSE lo muestra
        """
        # if self.findHidden_ is not h:
        #    self.findHidden_ = h
        #    if h:
        #        self.tabControlLayout.hide()
        #    else:
        #        self.tabControlLayout.show()
        pass

    def filterHidden(self) -> bool:
        """
        Obtiene si el marco para conmutar entre datos y filtro está oculto
        """
        return self.filterHidden_

    @decorators.Deprecated
    def setFilterHidden(self, h: bool) -> None:
        """
        Oculta o muestra el marco para conmutar entre datos y filtro

        @param  h TRUE lo oculta, FALSE lo muestra
        """
        # if self.filterHidden_ is not h:
        #    self.filterHidden_ = h
        #    if h:
        #        self.tabFilter.hide()
        #    else:
        #        self.tabFilter.show()
        pass

    def showAllPixmaps(self) -> bool:
        """
        Ver FLTableDB::showAllPixmaps_
        """
        return self.showAllPixmaps_

    def setShowAllPixmaps(self, s: bool) -> None:
        """
        Ver FLTableDB::showAllPixmaps_
        """
        self.showAllPixmaps_ = s

    def functionGetColor(self) -> Optional[str]:
        """
        Ver FLTableDB::functionGetColor_
        """
        return self.functionGetColor_

    def setFunctionGetColor(self, f: str) -> None:
        """
        Ver FLTableDB::functionGetColor_
        """
        self.functionGetColor_ = f

        # if self.tableRecords_ is not None:
        #    self.tableRecords().setFunctionGetColor("%s.%s" % (self.topWidget.name(), f))

    def setFilterRecordsFunction(self, fn: str) -> None:
        """
        Asigna el nombre de función a llamar cuando cambia el filtro.
        """
        self.tableDB_filterRecords_functionName_ = fn

    def setOnlyTable(self, on: bool = True) -> None:
        """
        Ver FLTableDB::onlyTable_
        """
        if self.tableRecords_:
            self.onlyTable_ = on
            self.tableRecords_.setOnlyTable(on)

        self.reqOnlyTable_ = on

    def onlyTable(self) -> bool:
        return self.reqOnlyTable_

    @decorators.NotImplementedWarn
    def setAutoSortColumn(self, on: bool = True):
        """
        Ver FLTableDB::autoSortColumn_
        """
        self.autoSortColumn_ = on

    def autoSortColumn(self) -> bool:
        return self.autoSortColumn_

    def eventFilter(self, obj: Any, ev: Any) -> Any:
        """
        Process user events.
        """
        if (
            not self.tableRecords_
            or not self.lineEditSearch
            or not self.comboBoxFieldToSearch
            or not self.comboBoxFieldToSearch2
            or not self.cursor()
        ):
            return super(FLTableDB, self).eventFilter(obj, ev)

        if ev.type() == QtCore.QEvent.KeyPress and isinstance(obj, FLDataTable):
            k = ev

            if k.key() == QtCore.Qt.Key_F2:
                self.comboBoxFieldToSearch.popup()
                return True

        if ev.type() == QtCore.QEvent.WindowUnblocked and isinstance(obj, FLDataTable):
            row = self.currentRow()
            self.tableRecords_.refresh()
            if row > -1:
                self.setCurrentRow(row)
            return True

        if ev.type() == QtCore.QEvent.KeyPress and isinstance(obj, QtWidgets.QLineEdit):
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

        if obj in (self.tableRecords_, self.lineEditSearch):
            return False
        else:
            return super(FLTableDB, self).eventFilter(obj, ev)

    def showEvent(self, e: Any) -> None:
        """
        Captura evento mostrar
        """
        super(FLTableDB, self).showEvent(e)
        self.load()
        if not self.loaded():
            self.showWidget()

    def showWidget(self) -> None:
        """
        Redefinida por conveniencia
        """
        if self.showed:
            return

        if not self.topWidget:
            self.initFakeEditor()
            self.showed = True
            return

        if not self.cursor():
            return

        self.showed = True

        # own_tmd = bool(self.tableName_)
        if self.tableName_:
            if not self.cursor().db().manager().existsTable(self.tableName_):
                tmd = self.cursor().db().manager().createTable(self.tableName_)
            else:
                tmd = self.cursor().db().manager().metadata(self.tableName_)

            if not tmd:
                return

        self.tableRecords()

        from .flformrecorddb import FLFormRecordDB

        if not self.cursorAux:
            if not self.initSearch_:
                self.refresh(True, True)
                if self.tableRecords_:
                    QtCore.QTimer.singleShot(0, self.tableRecords_.ensureRowSelectedVisible)
            else:
                self.refresh(True)
                if self.tableRecords_ and self.tableRecords_.numRows() <= 0:

                    self.refresh(False, True)
                else:
                    self.refreshDelayed()

            if not isinstance(self.topWidget, FLFormRecordDB) and self.lineEditSearch is not None:
                self.lineEditSearch.setFocus()

        if self.cursorAux:
            if (
                isinstance(self.topWidget, FLFormRecordDB)
                and self.cursorAux.modeAccess() == FLSqlCursor.Browse
            ):
                self.cursor().setEdition(False)
                self.setReadOnly(True)

            if self.initSearch_:
                self.refresh(True, True)
                if self.tableRecords_:
                    QtCore.QTimer.singleShot(0, self.tableRecords_.ensureRowSelectedVisible)
            else:
                self.refresh(True)
                if self.tableRecords_ and self.tableRecords_.numRows() <= 0:
                    self.refresh(False, True)
                else:
                    self.refreshDelayed()

        elif (
            isinstance(self.topWidget, FLFormRecordDB)
            and self.cursor().modeAccess() == FLSqlCursor.Browse
            and tmd
            and not tmd.isQuery()
        ):
            self.cursor().setEdition(False)
            self.setReadOnly(True)

        # if own_tmd and tmd and not tmd.inCache():
        #    del tmd

    def createFLTableDBWidget(self) -> None:
        from pineboolib.core.utils.utils_base import filedir

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHeightForWidth(True)

        sizePolicyClean = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicyClean.setHeightForWidth(True)

        sizePolicyGB = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )

        self.dataLayout = QtWidgets.QHBoxLayout()  # Contiene tabData y tabFilters
        # self.dataLayout.setContentsMargins(0, 0, 0, 0)
        # self.dataLayout.setSizeConstraint(0)

        self.tabDataLayout = QtWidgets.QVBoxLayout()
        filterL = QtWidgets.QVBoxLayout()

        if self.tabData:
            self.tabData.setSizePolicy(sizePolicyGB)
            self.tabData.setLayout(self.tabDataLayout)

        if self.tabFilter:
            self.tabFilter.setSizePolicy(sizePolicyGB)
            self.tabFilter.setLayout(filterL)

        # Fix para acercar el lineEdit con el fltable
        # self.tabData.setContentsMargins(0, 0, 0, 0)
        # self.tabFilter.setContentsMargins(0, 0, 0, 0)
        # self.tabDataLayout.setContentsMargins(0, 0, 0, 0)
        # filterL.setContentsMargins(0, 0, 0, 0)

        # Contiene botones lateral (datos, filtros, odf)
        self.buttonsLayout = QtWidgets.QVBoxLayout()
        self.masterLayout = QtWidgets.QVBoxLayout()  # Contiene todos los layouts

        if self.pbData is None:
            self.pbData = QtWidgets.QPushButton(self)
            self.pbData.setSizePolicy(sizePolicy)
            if self.iconSize is not None:
                self.pbData.setMinimumSize(self.iconSize)
            self.pbData.setFocusPolicy(QtCore.Qt.NoFocus)
            self.pbData.setIcon(QtGui.QIcon(filedir("../share/icons", "fltable-data.png")))
            self.pbData.setText("")
            self.pbData.setToolTip("Mostrar registros")
            self.pbData.setWhatsThis("Mostrar registros")
            self.buttonsLayout.addWidget(self.pbData)
            self.pbData.clicked.connect(self.activeTabData)

        self.pbFilter = QtWidgets.QPushButton(self)
        self.pbFilter.setSizePolicy(sizePolicy)
        if self.iconSize is not None:
            self.pbFilter.setMinimumSize(self.iconSize)
        self.pbFilter.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pbFilter.setIcon(QtGui.QIcon(filedir("../share/icons", "fltable-filter.png")))
        self.pbFilter.setText("")
        self.pbFilter.setToolTip("Mostrar filtros")
        self.pbFilter.setWhatsThis("Mostrar filtros")
        self.buttonsLayout.addWidget(self.pbFilter)
        self.pbFilter.clicked.connect(self.activeTabFilter)

        self.pbOdf = QtWidgets.QPushButton(self)
        self.pbOdf.setSizePolicy(sizePolicy)
        if self.iconSize is not None:
            self.pbOdf.setMinimumSize(self.iconSize)
        self.pbOdf.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pbOdf.setIcon(QtGui.QIcon(filedir("../share/icons", "fltable-odf.png")))
        self.pbOdf.setText("")
        self.pbOdf.setToolTip("Exportar a hoja de cálculo")
        self.pbOdf.setWhatsThis("Exportar a hoja de cálculo")
        self.buttonsLayout.addWidget(self.pbOdf)
        self.pbOdf.clicked.connect(self.exportToOds)
        if config.value("ebcomportamiento/FLTableExport2Calc", "false") == "true":
            self.pbOdf.setDisabled(True)

        self.pbClean = QtWidgets.QPushButton(self)
        self.pbClean.setSizePolicy(sizePolicyClean)
        if self.iconSize is not None:
            self.pbClean.setMinimumSize(self.iconSize)
        self.pbClean.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pbClean.setIcon(QtGui.QIcon(filedir("../share/icons", "fltable-clean.png")))
        self.pbClean.setText("")
        self.pbClean.setToolTip("Limpiar filtros")
        self.pbClean.setWhatsThis("Limpiar filtros")
        filterL.addWidget(self.pbClean)
        self.pbClean.clicked.connect(self.tdbFilterClear)

        spacer = QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.buttonsLayout.addItem(spacer)

        from pineboolib.qt3_widgets.qcombobox import QComboBox
        from pineboolib.qt3_widgets.qtable import QTable

        self.comboBoxFieldToSearch = QComboBox()
        self.comboBoxFieldToSearch2 = QComboBox()
        # self.comboBoxFieldToSearch.addItem("*")
        # self.comboBoxFieldToSearch2.addItem("*")
        self.lineEditSearch = QtWidgets.QLineEdit()
        self.lineEditSearch.textChanged.connect(self.filterRecords)
        label1 = QtWidgets.QLabel()
        label2 = QtWidgets.QLabel()

        label1.setText("Buscar")
        label2.setText("en")

        if self.tabControlLayout is not None:
            self.tabControlLayout.addWidget(label1)
            self.tabControlLayout.addWidget(self.lineEditSearch)
            self.tabControlLayout.addWidget(label2)
            self.tabControlLayout.addWidget(self.comboBoxFieldToSearch)
            self.tabControlLayout.addWidget(self.comboBoxFieldToSearch2)

            self.masterLayout.addLayout(self.tabControlLayout)
        self.masterLayout.addLayout(self.dataLayout)
        self.setLayout(self.masterLayout)

        # Se añade data, filtros y botonera
        if self.tabData is not None:
            self.dataLayout.addWidget(self.tabData)
        if self.tabFilter is not None:
            self.dataLayout.addWidget(self.tabFilter)
            self.tabFilter.hide()

        self.dataLayout.addLayout(self.buttonsLayout)
        self.comboBoxFieldToSearch.currentIndexChanged.connect(self.putFirstCol)
        self.comboBoxFieldToSearch2.currentIndexChanged.connect(self.putSecondCol)

        self.tdbFilter = QTable()
        filterL.addWidget(self.tdbFilter)

    def tableRecords(self) -> "FLDataTable":
        """
        Obtiene el componente tabla de registros
        """
        if self.tableRecords_ is None:
            self.tableRecords_ = FLDataTable(self.tabData, "tableRecords")
            if self.tableRecords_ is not None:
                self.tableRecords_.setFocusPolicy(QtCore.Qt.StrongFocus)
                self.setFocusProxy(self.tableRecords_)
                if self.tabDataLayout is not None:
                    self.tabDataLayout.addWidget(self.tableRecords_)
                self.setTabOrder(self.tableRecords_, self.lineEditSearch)
                self.setTabOrder(self.lineEditSearch, self.comboBoxFieldToSearch)
                self.setTabOrder(self.comboBoxFieldToSearch, self.comboBoxFieldToSearch2)
                if self.lineEditSearch is not None:
                    self.lineEditSearch.installEventFilter(self)
                self.tableRecords_.installEventFilter(self)

                if self.autoSortColumn_:
                    self.tableRecords_.header().sectionClicked.connect(self.switchSortOrder)

        t_cursor = self.tableRecords_.cursor_
        if (
            self.cursor()
            and self.cursor() is not t_cursor
            and self.cursor().metadata()
            and (
                not t_cursor
                or (
                    t_cursor
                    and t_cursor.metadata()
                    and t_cursor.metadata().name() != self.cursor().metadata().name()
                )
            )
        ):
            self.setTableRecordsCursor()

        return self.tableRecords_

    def setTableRecordsCursor(self) -> None:
        """
        Asigna el cursor actual del componente a la tabla de registros
        """
        if self.tableRecords_ is None:
            self.tableRecords_ = FLDataTable(self.tabData, "tableRecords")
            if self.tableRecords_ is not None:
                self.tableRecords_.setFocusPolicy(QtCore.Qt.StrongFocus)
                self.setFocusProxy(self.tableRecords_)
                if self.tabDataLayout is not None:
                    self.tabDataLayout.addWidget(self.tableRecords_)
                self.setTabOrder(self.tableRecords_, self.lineEditSearch)
                self.setTabOrder(self.lineEditSearch, self.comboBoxFieldToSearch)
                self.setTabOrder(self.comboBoxFieldToSearch, self.comboBoxFieldToSearch2)
                self.tableRecords_.installEventFilter(self)

                if self.lineEditSearch is not None:
                    self.lineEditSearch.installEventFilter(self)

        if self.checkColumnEnabled_:
            try:
                self.tableRecords_.clicked.disconnect(self.tableRecords_.setChecked)
            except Exception:
                logger.exception("setTableRecordsCursor: Error disconnecting setChecked signal")
            self.tableRecords_.clicked.connect(self.tableRecords_.setChecked)

        t_cursor = self.tableRecords_.cursor_
        if t_cursor is not self.cursor():
            self.tableRecords_.setFLSqlCursor(self.cursor())
            if t_cursor:
                self.tableRecords_.recordChoosed.disconnect(self.recordChoosedSlot)
                t_cursor.newBuffer.disconnect(self.currentChangedSlot)

            self.tableRecords_.recordChoosed.connect(self.recordChoosedSlot)
            self.cursor().newBuffer.connect(self.currentChangedSlot)

    @decorators.pyqtSlot()
    def recordChoosedSlot(self) -> None:
        if isinstance(self.topWidget, FLFormSearchDB) and self.topWidget.inExec_:
            self.topWidget.accept()
        else:
            self.cursor().chooseRecord()

    @decorators.pyqtSlot()
    def currentChangedSlot(self) -> None:
        self.currentChanged.emit()

    def currentRow(self) -> int:
        return self.cursor().at()

    def refreshTabData(self) -> None:
        """
        Refresca la pestaña datos aplicando el filtro
        """
        tdbWhere: Optional[str] = self.tdbFilterBuildWhere()
        if not tdbWhere == self.tdbFilterLastWhere_:
            self.tdbFilterLastWhere_ = tdbWhere

        self.refresh(False, True)

    def refreshTabFilter(self) -> None:
        """
        Refresca la pestaña del filtro
        """
        if self.tabFilterLoaded:
            return

        horizHeader = self.tableRecords().horizontalHeader()
        if not horizHeader:
            return

        hCount = horizHeader.count() - self.sortColumn_
        if self.tdbFilter and self.tdbFilter.numRows() < hCount and self.cursor():
            tMD = self.cursor().metadata()
            if not tMD:
                return

            field = None
            editor_ = None
            # type = None
            # len = None
            partInteger = None
            partDecimal = None
            rX = None
            ol = None

            self.tdbFilter.setSelectionMode(QtWidgets.QTableWidget.NoSelection)
            self.tdbFilter.setNumCols(5)

            _notVisibles = 0
            for f in tMD.fieldList():
                if not f.visibleGrid():
                    _notVisibles = _notVisibles + 1

            self.tdbFilter.setNumRows(hCount - _notVisibles)
            self.tdbFilter.setColumnReadOnly(0, True)
            util = FLUtil()
            self.tdbFilter.setColumnLabels(",", util.tr("Campo,Condición,Valor,Desde,Hasta"))

            self.mapCondType.insert(self.All, util.tr("Todos"))
            self.mapCondType.insert(self.Contains, util.tr("Contiene Valor"))
            self.mapCondType.insert(self.Starts, util.tr("Empieza por Valor"))
            self.mapCondType.insert(self.End, util.tr("Acaba por Valor"))
            self.mapCondType.insert(self.Equal, util.tr("Igual a Valor"))
            self.mapCondType.insert(self.Dist, util.tr("Distinto de Valor"))
            self.mapCondType.insert(self.Greater, util.tr("Mayor que Valor"))
            self.mapCondType.insert(self.Less, util.tr("Menor que Valor"))
            self.mapCondType.insert(self.FromTo, util.tr("Desde - Hasta"))
            self.mapCondType.insert(self.Null, util.tr("Vacío"))
            self.mapCondType.insert(self.NotNull, util.tr("No Vacío"))

            i = 0
            # for headT in hCount:
            _linea = 0

            while i < hCount:
                _label = (
                    self.cursor()
                    .model()
                    .headerData(i + self.sortColumn_, QtCore.Qt.Horizontal, QtCore.Qt.DisplayRole)
                )
                _alias = tMD.fieldAliasToName(_label)
                if _alias is None:
                    raise Exception("alias could not be solved")
                field = tMD.field(_alias)

                if field is None:
                    i = i + 1
                    continue

                if not field.visibleGrid():
                    i = i + 1
                    continue

                self.tdbFilter.setText(_linea, 0, _label)

                type_ = field.type()
                len_ = field.length()
                partInteger = field.partInteger()
                partDecimal = field.partDecimal()
                rX = field.regExpValidator()
                ol = field.hasOptionsList()
                from pineboolib.qt3_widgets.qcombobox import QComboBox

                cond = QComboBox(self)
                if not type_ == "pixmap":
                    condList = [
                        util.tr("Todos"),
                        util.tr("Igual a Valor"),
                        util.tr("Distinto de Valor"),
                        util.tr("Vacío"),
                        util.tr("No Vacío"),
                    ]
                    if not type_ == "bool":
                        condList = [
                            util.tr("Todos"),
                            util.tr("Igual a Valor"),
                            util.tr("Distinto de Valor"),
                            util.tr("Vacío"),
                            util.tr("No Vacío"),
                            util.tr("Contiene Valor"),
                            util.tr("Empieza por Valor"),
                            util.tr("Acaba por Valor"),
                            util.tr("Mayor que Valor"),
                            util.tr("Menor que Valor"),
                            util.tr("Desde - Hasta"),
                        ]
                    cond.insertStringList(condList)
                    self.tdbFilter.setCellWidget(_linea, 1, cond)

                j = 2
                while j < 5:
                    editor_ = None
                    if type_ in ("uint", "int", "double", "string", "stringlist"):
                        if ol:
                            editor_ = QComboBox(self)
                            olTranslated = []
                            olNoTranslated = field.optionsList()
                            for z in olNoTranslated:
                                olTranslated.append(util.translate("Metadata", z))

                            editor_.insertStringList(olTranslated)
                        else:
                            from pineboolib.fllegacy.fllineedit import FLLineEdit

                            editor_ = FLLineEdit(self)

                            if editor_ is None:
                                raise Exception("editor_ is Empty!")

                            if type_ == "double":
                                from .fldoublevalidator import FLDoubleValidator

                                editor_.setValidator(
                                    FLDoubleValidator(
                                        0, pow(10, partInteger) - 1, partDecimal, editor_
                                    )
                                )
                                editor_.setAlignment(Qt.AlignRight)
                            else:
                                if type_ in ("uint", "int"):
                                    if type_ == "uint":
                                        from .fluintvalidator import FLUIntValidator

                                        editor_.setValidator(
                                            FLUIntValidator(0, pow(10, partInteger) - 1, editor_)
                                        )
                                    else:
                                        from .flintvalidator import FLIntValidator

                                        editor_.setValidator(
                                            FLIntValidator(
                                                pow(10, partInteger) - 1 * (-1),
                                                pow(10, partInteger) - 1,
                                                editor_,
                                            )
                                        )

                                    editor_.setAlignment(Qt.AlignRight)
                                else:
                                    if len_ > 0:
                                        editor_.setMaxLength(len_)
                                        if rX:
                                            editor_.setValidator(
                                                QtGui.QRegExpValidator(QtCore.QRegExp(rX), editor_)
                                            )

                                    editor_.setAlignment(Qt.AlignLeft)

                    if type_ == "serial":
                        from pineboolib.fllegacy.flspinbox import FLSpinBox

                        editor_ = FLSpinBox()
                        if editor_ is None:
                            raise Exception("editor_ is Empty!")

                        editor_.setMaxValue(pow(10, partInteger) - 1)

                    if type_ == "pixmap":
                        from pineboolib.fllegacy.fllineedit import FLLineEdit

                        editor_ = FLLineEdit(self)
                        if editor_ is None:
                            raise Exception("editor_ is Empty!")

                        self.tdbFilter.setRowReadOnly(i, True)

                    if type_ == "date":
                        from pineboolib.fllegacy.fldateedit import FLDateEdit

                        if editor_ is None:
                            raise Exception("editor_ is Empty!")

                        editor_ = FLDateEdit(self, _label)
                        if editor_ is None:
                            raise Exception("editor_ is Empty!")

                        editor_.setOrder(FLDateEdit.DMY)
                        editor_.setAutoAdvance(True)
                        editor_.setCalendarPopup(True)
                        editor_.setSeparator("-")
                        da = QtCore.QDate()
                        editor_.setDate(da.currentDate())

                    if type_ == "time":
                        from pineboolib.fllegacy.fltimeedit import FLTimeEdit

                        editor_ = FLTimeEdit(self)
                        if editor_ is None:
                            raise Exception("editor_ is Empty!")

                        timeNow = QtCore.QTime.currentTime()
                        editor_.setTime(timeNow)

                    if type_ in (PNFieldMetaData.Unlock, "bool"):
                        from pineboolib.fllegacy.flcheckbox import FLCheckBox

                        editor_ = FLCheckBox(self)

                    if editor_:
                        self.tdbFilter.setCellWidget(_linea, j, editor_)

                    j += 1

                i += 1
                _linea += 1

        k = 0

        while k < 5:
            if self.tdbFilter:
                self.tdbFilter.adjustColumn(k)
            k += 1

        self.tabFilterLoaded = True  # Con esto no volvemos a cargar y reescribir el filtro

    def decodeCondType(self, strCondType: str) -> int:
        """
        Para obtener la enumeración correspondiente a una condición para el filtro a partir de
        su literal
        """
        i = 0
        while i < len(self.mapCondType):
            if strCondType == self.mapCondType[i]:
                return i

            i = i + 1

        return self.All

    def tdbFilterBuildWhere(self) -> Optional[str]:
        """
        Construye la claúsula de filtro en SQL a partir del contenido de los valores
        definidos en la pestaña de filtro
        """
        if not self.topWidget:
            return None

        if self.tdbFilter is None:
            return None

        rCount = self.tdbFilter.numRows()
        # rCount = self.cursor().model().columnCount()
        if not rCount or not self.cursor():
            return None

        tMD = self.cursor().metadata()
        if not tMD:
            return None

        field = None
        cond = None
        type = None
        condType = None
        fieldName = None
        condValue: str = ""
        where: str = ""
        fieldArg = ""
        arg2 = ""
        arg4 = ""

        ol = None

        for i in range(rCount):
            if self.tdbFilter is None:
                break
            fieldName = tMD.fieldAliasToName(self.tdbFilter.text(i, 0))
            if fieldName is None:
                raise Exception("fieldName could not be resolved!")

            field = tMD.field(fieldName)
            if field is None:
                continue

            cond = self.tdbFilter.cellWidget(i, 1)

            if not cond:
                continue

            condType = self.decodeCondType(cond.currentText)
            if condType == self.All:
                continue

            if tMD.isQuery():
                qry = (
                    self.cursor()
                    .db()
                    .manager()
                    .query(self.cursor().metadata().query(), self.cursor())
                )

                if qry:
                    list_ = qry.fieldList()

                    qField = None
                    for qField in list_:
                        if qField.endswith(".%s" % fieldName):
                            break

                    fieldName = qField
            else:
                fieldName = tMD.name() + "." + fieldName

            fieldArg = fieldName or ""
            arg2 = ""
            arg4 = ""
            type = field.type()
            ol = field.hasOptionsList()

            if type in ("string", "stringlist"):
                fieldArg = "UPPER(%s)" % fieldName

            if type in ("uint", "int", "double", "string", "stringlist"):
                if ol:
                    if condType == self.FromTo:
                        editorOp1 = self.tdbFilter.cellWidget(i, 3)
                        editorOp2 = self.tdbFilter.cellWidget(i, 4)
                        arg2 = (
                            self.cursor()
                            .db()
                            .manager()
                            .formatValue(type, editorOp1.currentText, True)
                        )
                        arg4 = (
                            self.cursor()
                            .db()
                            .manager()
                            .formatValue(type, editorOp2.currentText, True)
                        )
                    else:
                        editorOp1 = self.tdbFilter.cellWidget(i, 2)
                        arg2 = (
                            self.cursor()
                            .db()
                            .manager()
                            .formatValue(type, editorOp1.currentText, True)
                        )
                else:
                    if condType == self.FromTo:
                        editorOp1 = self.tdbFilter.cellWidget(i, 3)
                        editorOp2 = self.tdbFilter.cellWidget(i, 4)
                        arg2 = (
                            self.cursor().db().manager().formatValue(type, editorOp1.text(), True)
                        )
                        arg4 = (
                            self.cursor().db().manager().formatValue(type, editorOp2.text(), True)
                        )
                    else:
                        editorOp1 = self.tdbFilter.cellWidget(i, 2)
                        arg2 = (
                            self.cursor().db().manager().formatValue(type, editorOp1.text(), True)
                        )

            if type == "serial":
                if condType == self.FromTo:
                    editorOp1 = self.tdbFilter.cellWidget(i, 3)
                    editorOp2 = self.tdbFilter.cellWidget(i, 4)
                    arg2 = editorOp1.value()
                    arg4 = editorOp2.value()
                else:
                    from pineboolib.fllegacy.flspinbox import FLSpinBox

                    editorOp1 = FLSpinBox(self.tdbFilter.cellWidget(i, 2))
                    arg2 = editorOp1.value()

            if type == "date":
                util = FLUtil()
                if condType == self.FromTo:
                    editorOp1 = self.tdbFilter.cellWidget(i, 3)
                    editorOp2 = self.tdbFilter.cellWidget(i, 4)
                    arg2 = (
                        self.cursor()
                        .db()
                        .manager()
                        .formatValue(type, util.dateDMAtoAMD(str(editorOp1.text())))
                    )
                    arg4 = (
                        self.cursor()
                        .db()
                        .manager()
                        .formatValue(type, util.dateDMAtoAMD(str(editorOp2.text())))
                    )
                else:
                    editorOp1 = self.tdbFilter.cellWidget(i, 2)
                    arg2 = (
                        self.cursor()
                        .db()
                        .manager()
                        .formatValue(type, util.dateDMAtoAMD(str(editorOp1.text())))
                    )

            if type == "time":
                if condType == self.FromTo:
                    editorOp1 = self.tdbFilter.cellWidget(i, 3)
                    editorOp2 = self.tdbFilter.cellWidget(i, 4)
                    arg2 = (
                        self.cursor()
                        .db()
                        .manager()
                        .formatValue(type, editorOp1.time().toString(Qt.ISODate))
                    )
                    arg4 = (
                        self.cursor()
                        .db()
                        .manager()
                        .formatValue(type, editorOp2.time().toString(Qt.ISODate))
                    )
                else:
                    editorOp1 = self.tdbFilter.cellWidget(i, 2)
                    arg2 = (
                        self.cursor()
                        .db()
                        .manager()
                        .formatValue(type, editorOp1.time().toString(Qt.ISODate))
                    )

            if type in ("unlock", "bool"):
                editorOp1 = self.tdbFilter.cellWidget(i, 2)
                checked_ = False
                if editorOp1.isChecked():
                    checked_ = True
                arg2 = self.cursor().db().manager().formatValue(type, checked_)

            if where:
                where += " AND"

            condValue = " " + fieldArg
            if arg2 is None:
                arg2 = ""
            if condType == self.Contains:
                condValue += " LIKE '%" + arg2.replace("'", "") + "%'"
            elif condType == self.Starts:
                condValue += " LIKE '" + arg2.replace("'", "") + "%'"
            elif condType == self.End:
                condValue += " LIKE '%%" + arg2.replace("'", "") + "'"
            elif condType == self.Equal:
                condValue += " = " + str(arg2)
            elif condType == self.Dist:
                condValue += " <> " + str(arg2)
            elif condType == self.Greater:
                condValue += " > " + str(arg2)
            elif condType == self.Less:
                condValue += " < " + str(arg2)
            elif condType == self.FromTo:
                condValue += " >= " + str(arg2) + " AND " + fieldArg + " <= " + str(arg4)
            elif condType == self.Null:
                condValue += " IS NULL "
            elif condType == self.notNull:
                condValue += " IS NOT NULL "

            where += condValue

        return where

    @decorators.BetaImplementation
    def initFakeEditor(self) -> None:
        """
        Inicializa un editor falso y no funcional.

        Esto se utiliza cuando se está editando el formulario con el diseñador y no
        se puede mostrar el editor real por no tener conexión a la base de datos.
        Crea una previsualización muy esquemática del editor, pero suficiente para
        ver la posisicón y el tamaño aproximado que tendrá el editor real.
        """
        if not self.fakeEditor_:
            self.fakeEditor_ = QtWidgets.QTextEdit(self.tabData)

            sizePolicy = QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
            )
            sizePolicy.setHeightForWidth(True)

            self.fakeEditor_.setSizePolicy(sizePolicy)
            self.fakeEditor_.setTabChangesFocus(True)
            self.fakeEditor_.setFocusPolicy(QtCore.Qt.StrongFocus)
            self.setFocusProxy(self.fakeEditor_)
            if not self.tabDataLayout:
                raise Exception("self.tabDataLayout is not defined!")
            self.tabDataLayout.addWidget(self.fakeEditor_)
            self.setTabOrder(self.fakeEditor_, self.lineEditSearch)
            self.setTabOrder(self.fakeEditor_, self.comboBoxFieldToSearch)
            self.fakeEditor_.show()

            prty = ""
            if self.tableName_:
                prty = prty + "tableName: %s\n" % self.tableName_
            if self.foreignField_:
                prty = prty + "foreignField: %s\n" % self.foreignField_
            if self.fieldRelation_:
                prty = prty + "fieldRelation: %s\n" % self.fieldRelation_

            self.fakeEditor_.setText(prty)

    @decorators.pyqtSlot()
    @decorators.pyqtSlot(bool)
    @decorators.pyqtSlot(bool, bool)
    def refresh(self, refreshHead: bool = False, refreshData: bool = True) -> None:
        """
        Actualiza el conjunto de registros.
        """
        if not self.cursor() or not self.tableRecords_:
            return

        tMD = self.cursor().metadata()
        if not tMD:
            return
        if not self.tableName_:
            self.tableName_ = tMD.name()

        if self.checkColumnEnabled_:
            if not self.checkColumnVisible_:
                fieldCheck = tMD.field(self.fieldNameCheckColumn_)
                if fieldCheck is None:
                    self.fieldNameCheckColumn_ = "%s_check_column" % tMD.name()

                    if self.fieldNameCheckColumn_ not in tMD.fieldNames():
                        fieldCheck = PNFieldMetaData(
                            self.fieldNameCheckColumn_,
                            self.tr(self.aliasCheckColumn_),
                            True,
                            False,
                            PNFieldMetaData.Check,
                            0,
                            False,
                            True,
                            True,
                            0,
                            0,
                            False,
                            False,
                            False,
                            None,
                            False,
                            None,
                            True,
                            False,
                            False,
                        )
                        tMD.addFieldMD(fieldCheck)
                    else:
                        fieldCheck = tMD.field(self.fieldNameCheckColumn_)

                if fieldCheck is None:
                    raise Exception("fieldCheck is empty!")

                self.tableRecords().cur.model().updateColumnsCount()
                self.tableRecords().header().reset()
                self.tableRecords().header().swapSections(
                    self.tableRecords().column_name_to_column_index(fieldCheck.name()),
                    self.sortColumn_,
                )
                self.checkColumnVisible_ = True
                self.setTableRecordsCursor()
                self.sortColumn_ = 1
                self.sortColumn2_ = 2
                self.sortColumn3_ = 3

                # for i in enumerate(buffer_.count()):
                #    buffer_.setGenerated(i, True)

        else:
            self.setTableRecordsCursor()
            self.sortColumn_ = 0
            self.sortColumn2_ = 1
            self.sortColumn3_ = 2
            self.checkColumnVisible_ = False

        self.tableRecords_.setFunctionGetColor(
            self.functionGetColor(), getattr(self.topWidget, "iface", None)
        )

        if refreshHead:
            if not self.tableRecords().header().isHidden():
                self.tableRecords().header().hide()

            model = self.cursor().model()
            for column in range(model.columnCount()):
                field = model.metadata().indexFieldObject(column)
                if not field.visibleGrid() or (
                    field.type() == "check" and not self.checkColumnEnabled_
                ):
                    self.tableRecords_.setColumnHidden(column, True)
                else:
                    self.tableRecords_.setColumnHidden(column, False)

            if self.autoSortColumn_:
                s = []
                field_1 = self.tableRecords_.visual_index_to_field(self.sortColumn_)
                field_2 = self.tableRecords_.visual_index_to_field(self.sortColumn2_)
                field_3 = self.tableRecords_.visual_index_to_field(self.sortColumn3_)

                if field_1 is not None:
                    s.append("%s %s" % (field_1.name(), "ASC" if self.orderAsc_ else "DESC"))
                if field_2 is not None:
                    s.append("%s %s" % (field_2.name(), "ASC" if self.orderAsc_ else "DESC"))
                if field_3 is not None:
                    s.append("%s %s" % (field_3.name(), "ASC" if self.orderAsc_ else "DESC"))

                id_mod = (
                    self.cursor()
                    .db()
                    .managerModules()
                    .idModuleOfFile("%s.mtd" % self.cursor().metadata().name())
                )
                function_qsa = "%s.tableDB_setSort_%s" % (id_mod, self.cursor().metadata().name())

                vars: List[Any] = []
                vars.append(s)
                if field_1:
                    vars.append(field_1.name())
                    vars.append(self.orderAsc_)
                if field_2:
                    vars.append(field_2.name())
                    vars.append(self.orderAsc2_)
                if field_3:
                    vars.append(field_3.name())
                    vars.append(self.orderAsc3_)

                from pineboolib.application import project

                ret = project.call(function_qsa, vars, None, False)
                logger.debug("functionQSA: %s -> %r" % (function_qsa, ret))
                if ret and not isinstance(ret, bool):
                    if isinstance(ret, str):
                        ret = [ret]
                    if isinstance(ret, list):
                        s = ret

                self.tableRecords_.setSort(", ".join(s))

            if model:
                if self.comboBoxFieldToSearch is None:
                    raise Exception("comboBoxFieldSearch is not defined!")

                if self.comboBoxFieldToSearch2 is None:
                    raise Exception("comboBoxFieldSearch2 is not defined!")

                try:
                    self.comboBoxFieldToSearch.currentIndexChanged.disconnect(self.putFirstCol)
                    self.comboBoxFieldToSearch2.currentIndexChanged.disconnect(self.putSecondCol)
                except Exception:
                    logger.error("Se ha producido un problema al desconectar")
                    return

                self.comboBoxFieldToSearch.clear()
                self.comboBoxFieldToSearch2.clear()

                # cb1 = None
                # cb2 = None
                for column in range(model.columnCount()):
                    visual_column = self.tableRecords_.header().logicalIndex(column)
                    if visual_column is not None:
                        field = model.metadata().indexFieldObject(visual_column)
                        if not field.visibleGrid():
                            continue
                        #    self.tableRecords_.setColumnHidden(column, True)
                        # else:
                        self.comboBoxFieldToSearch.addItem(
                            model.headerData(
                                visual_column, QtCore.Qt.Horizontal, QtCore.Qt.DisplayRole
                            )
                        )
                        self.comboBoxFieldToSearch2.addItem(
                            model.headerData(
                                visual_column, QtCore.Qt.Horizontal, QtCore.Qt.DisplayRole
                            )
                        )

                self.comboBoxFieldToSearch.addItem("*")
                self.comboBoxFieldToSearch2.addItem("*")
                self.comboBoxFieldToSearch.setCurrentIndex(self.sortColumn_)
                self.comboBoxFieldToSearch2.setCurrentIndex(self.sortColumn2_)
                self.comboBoxFieldToSearch.currentIndexChanged.connect(self.putFirstCol)
                self.comboBoxFieldToSearch2.currentIndexChanged.connect(self.putSecondCol)

            else:
                self.comboBoxFieldToSearch.addItem("*")
                self.comboBoxFieldToSearch2.addItem("*")

            self.tableRecords_.header().show()

        if refreshData or self.sender():
            finalFilter = self.filter_
            if self.tdbFilterLastWhere_:
                if not finalFilter:
                    finalFilter = self.tdbFilterLastWhere_
                else:
                    finalFilter = "%s AND %s" % (finalFilter, self.tdbFilterLastWhere_)

            self.tableRecords_.setPersistentFilter(finalFilter)
            self.tableRecords_.setShowAllPixmaps(self.showAllPixmaps_)
            self.tableRecords_.refresh()

        if self.initSearch_:
            try:
                self.lineEditSearch.textChanged.disconnect(self.filterRecords)
            except Exception:
                pass
            self.lineEditSearch.setText(self.initSearch_)
            self.lineEditSearch.textChanged.connect(self.filterRecords)
            self.lineEditSearch.selectAll()
            self.initSearch_ = None
            # self.seekCursor()

        if not self.readonly_ == self.reqReadOnly_ or (
            self.tableRecords_ and not self.readonly_ == self.tableRecords_.flReadOnly()
        ):
            self.setReadOnly(self.reqReadOnly_)

        if not self.editonly_ == self.reqEditOnly_ or (
            self.tableRecords_ and not self.editonly_ == self.tableRecords_.editOnly()
        ):
            self.setEditOnly(self.reqEditOnly_)

        if not self.insertonly_ == self.reqInsertOnly_ or (
            self.tableRecords_ and not self.insertonly_ == self.tableRecords_.insertOnly()
        ):
            self.setInsetOnly(self.reqInsertOnly_)

        if not self.onlyTable_ == self.reqOnlyTable_ or (
            self.tableRecords_ and not self.onlyTable_ == self.tableRecords_.onlyTable()
        ):
            self.setOnlyTable(self.reqOnlyTable_)

        if self.tableRecords_ and self.tableRecords_.isHidden():
            self.tableRecords_.show()

        QtCore.QTimer.singleShot(50, self.setSortOrder)

    def refreshDelayed(self, msec: int = 50, refreshData: bool = True) -> None:
        """
        Actualiza el conjunto de registros con un retraso.

        Acepta un lapsus de tiempo en milisegundos, activando el cronómetro interno para
        que realize el refresh definitivo al cumplirse dicho lapsus.

        @param msec Cantidad de tiempo del lapsus, en milisegundos.
        """

        self._refreshData = True if refreshData else False
        QtCore.QTimer.singleShot(msec, self.refreshDelayed2)
        self.seekCursor()

    def refreshDelayed2(self) -> None:
        self.refresh(False, self._refreshData)
        self._refreshData = False

    @decorators.pyqtSlot(bool)
    def insertRecord(self, wait: bool = True) -> None:
        """
        Call method FLSqlCursor::insertRecord()
        """

        w = self.sender()
        # if (w and (not self.cursor() or self.reqReadOnly_ or self.reqEditOnly_ or self.reqOnlyTable_ or (self.cursor().cursorRelation()
        #      and self.cursor().cursorRelation().isLocked()))):
        relationLock = False
        cur_relation = self.cursor().cursorRelation()
        if cur_relation is not None:
            relationLock = cur_relation.isLocked()

        if w and (
            not self.cursor()
            or self.reqReadOnly_
            or self.reqEditOnly_
            or self.reqOnlyTable_
            or relationLock
        ):
            w.setDisabled(True)
            return

        if self.cursor():
            self.cursor().insertRecord(wait)

    @decorators.pyqtSlot(bool)
    def editRecord(self, wait: bool = True) -> None:
        """
        Call method FLSqlCursor::editRecord()
        """
        w = self.sender()
        cur_relation = self.cursor().cursorRelation()

        if (
            w
            and not isinstance(w, FLDataTable)
            and (
                not self.cursor()
                or self.reqReadOnly_
                or self.reqEditOnly_
                or self.reqOnlyTable_
                or (cur_relation and cur_relation.isLocked())
            )
        ):
            w.setDisabled(True)
            return

        if self.cursor():
            self.cursor().editRecord()

    @decorators.pyqtSlot(bool)
    def browseRecord(self, wait: bool = True) -> None:
        """
        Call method FLSqlCursor::browseRecord()
        """

        w = self.sender()

        if w and not isinstance(w, FLDataTable) and (not self.cursor() or self.reqOnlyTable_):
            w.setDisabled(True)
            return

        if self.cursor():
            self.cursor().browseRecord(wait)

    @decorators.pyqtSlot(bool)
    def deleteRecord(self, wait: bool = True) -> None:
        """
        Call method FLSqlCursor::deleteRecord()
        """
        w = self.sender()

        cur_relation = self.cursor().cursorRelation()

        if (
            w
            and not isinstance(w, FLDataTable)
            and (
                not self.cursor()
                or self.reqReadOnly_
                or self.reqInsertOnly_
                or self.reqEditOnly_
                or self.reqOnlyTable_
                or (cur_relation and cur_relation.isLocked())
            )
        ):
            w.setDisabled(True)
            return

        if self.cursor():
            self.cursor().deleteRecord(wait)

    @decorators.pyqtSlot()
    def copyRecord(self):
        """
        Call method FLSqlCursor::copyRecord()
        """
        w = self.sender()

        cur_relation = self.cursor().cursorRelation()

        if (
            w
            and not isinstance(w, FLDataTable)
            and (
                not self.cursor()
                or self.reqReadOnly_
                or self.reqEditOnly_
                or self.reqOnlyTable_
                or (cur_relation and cur_relation.isLocked())
            )
        ):
            w.setDisabled(True)
            return

        if self.cursor():
            self.cursor().copyRecord()

    @decorators.pyqtSlot(int)
    @decorators.pyqtSlot(str)
    def putFirstCol(self, col: Union[int, str]) -> None:
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
        if not self.tableRecords_:
            raise Exception("tableRecords_ is not defined!")

        _index = (
            self.tableRecords_.column_name_to_column_index(col)
            if isinstance(col, str)
            else self.tableRecords_.visual_index_to_column_index(col)
        )

        if _index is None or _index < 0:
            return
        self.moveCol(_index, self.sortColumn_)
        self.tableRecords_.sortByColumn(
            self.sortColumn_,
            QtCore.Qt.AscendingOrder if self.orderAsc_ else QtCore.Qt.DescendingOrder,
        )

    @decorators.pyqtSlot(int)
    @decorators.pyqtSlot(str)
    def putSecondCol(self, col: Union[int, str]) -> None:
        """
        Coloca la columna como segunda pasando el nombre del campo.

        @author Silix - dpinelo
        """
        if not self.tableRecords_:
            raise Exception("tableRecords_ is not defined!")
        _index = (
            self.tableRecords_.column_name_to_column_index(col)
            if isinstance(col, str)
            else self.tableRecords_.visual_index_to_column_index(col)
        )

        if _index is None or _index < 0:
            return

        self.moveCol(_index, self.sortColumn2_)

    @decorators.BetaImplementation
    def moveCol(self, from_: int, to: int, firstSearch: bool = True) -> None:
        """
        Mueve una columna de un campo origen a la columna de otro campo destino

        @param  from  Nombre del campo de la columna de origen
        @param  to    Nombre del campo de la columna de destino
        @param  firstSearch dpinelo: Indica si se mueven columnas teniendo en cuenta que esta función
        se ha llamado o no, desde el combo principal de búsqueda y filtrado
        """
        if from_ < 0 or to < 0:
            return

        tMD = self.cursor().metadata()
        if not tMD:
            return

        if not self.tableRecords_:
            raise Exception("tableRecords_ is not defined!")

        self.tableRecords_.hide()

        textSearch = self.lineEditSearch.text()

        field = self.cursor().metadata().indexFieldObject(to)

        if to == 0:  # Si ha cambiado la primera columna
            try:
                self.comboBoxFieldToSearch.currentIndexChanged.disconnect(self.putFirstCol)
            except Exception:
                logger.error("Se ha producido un problema al desconectar")
                return

            self.comboBoxFieldToSearch.setCurrentIndex(from_)
            self.comboBoxFieldToSearch.currentIndexChanged.connect(self.putFirstCol)

            # Actializamos el segundo combo
            try:
                self.comboBoxFieldToSearch2.currentIndexChanged.disconnect(self.putSecondCol)
            except Exception:
                pass
            # Falta mejorar
            if (
                self.comboBoxFieldToSearch.currentIndex()
                == self.comboBoxFieldToSearch2.currentIndex()
            ):
                self.comboBoxFieldToSearch2.setCurrentIndex(
                    self.tableRecords_._h_header.logicalIndex(self.sortColumn_)
                )
            self.comboBoxFieldToSearch2.currentIndexChanged.connect(self.putSecondCol)

        if to == 1:  # Si es la segunda columna ...
            try:
                self.comboBoxFieldToSearch2.currentIndexChanged.disconnect(self.putSecondCol)
            except Exception:
                pass
            self.comboBoxFieldToSearch2.setCurrentIndex(from_)
            self.comboBoxFieldToSearch2.currentIndexChanged.connect(self.putSecondCol)

            if (
                self.comboBoxFieldToSearch.currentIndex()
                == self.comboBoxFieldToSearch2.currentIndex()
            ):
                try:
                    self.comboBoxFieldToSearch.currentIndexChanged.disconnect(self.putFirstCol)
                except Exception:
                    pass
                if (
                    self.comboBoxFieldToSearch.currentIndex()
                    == self.comboBoxFieldToSearch2.currentIndex()
                ):
                    self.comboBoxFieldToSearch.setCurrentIndex(
                        self.tableRecords_._h_header.logicalIndex(self.sortColumn2_)
                    )
                self.comboBoxFieldToSearch.currentIndexChanged.connect(self.putFirstCol)

        if not textSearch:
            textSearch = self.cursor().valueBuffer(field.name())

        # self.refresh(True)

        if textSearch:
            self.refresh(False, True)
            try:
                self.lineEditSearch.textChanged.disconnect(self.filterRecords)
            except Exception:
                pass
            self.lineEditSearch.setText(str(textSearch))
            self.lineEditSearch.textChanged.connect(self.filterRecords)
            self.lineEditSearch.selectAll()
            self.seekCursor()
            QtCore.QTimer.singleShot(0, self.tableRecords_.ensureRowSelectedVisible)
        else:
            self.refreshDelayed()

        self.tableRecords_.header().swapSections(from_, to)

        self.refresh(True, False)

    @decorators.BetaImplementation
    def seekCursor(self) -> None:
        """
        Posiciona el cursor en un registro valido
        """
        return
        # textSearch = self.lineEditSearch.text()
        # if not textSearch:
        #     return
        #
        # if not self.cursor():
        #     return
        #
        # # fN = self.sortField_.name()
        # textSearch.replace("%", "")

        # if "'" not in textSearch and "\\" not in textSearch:
        #     sql = self.cursor().executedQuery() + " LIMIT 1"
        #   """
        #       #QSqlQuery qry(sql, cursor_->db()->db()); #FIXME
        #       if (qry.first()) {
        # QString v(qry.value(0).toString());
        # int pos = -1;
        # if (!v.upper().startsWith(textSearch.upper()))
        #   pos = cursor_->atFromBinarySearch(fN, textSearch, orderAsc_);
        # if (pos == -1)
        #   pos = cursor_->atFromBinarySearch(fN, v, orderAsc_);
        # cursor_->seek(pos, false, true);
        # """

    def setEnabled(self, b: bool) -> None:
        """
        Redefinida por conveniencia
        """
        self.setReadOnly(not b)

    def setColumnWidth(self, field: str, w: int) -> None:
        """
        Establece el ancho de una columna

        @param  field Nombre del campo de la base de datos correspondiente a la columna
        @param  w     Ancho de la columna
        """
        if self.tableRecords_:
            # col = self.tableRecords_.column_name_to_column_index(field) if isinstance(field, str) else field
            self.tableRecords_.setColWidth(field, w)

    def setCurrentRow(self, r: int) -> None:
        """
        Selecciona la fila indicada

        @param  r   Índice de la fila a seleccionar
        """
        t = self.tableRecords_
        if not t:
            return

        t.selectRow(r)
        t.scrollTo(t.cur.model().index(r, 0))

    @decorators.NotImplementedWarn
    def columnWidth(self, c: int) -> None:
        """
        @return Ancho de la columna
        """
        pass

    @decorators.NotImplementedWarn
    def setRowHeight(self, row: int, h: int) -> None:
        """
        Establece el alto de una fila

        @param  row Número de orden de la fila, empezando en 0
        @param  h   Alto de la fila
        """
        pass

    @decorators.NotImplementedWarn
    def rowHeight(self, row: int) -> None:
        """
        @return Alto de la fila
        """
        pass

    def exportToOds(self) -> None:
        """
        Exporta a una hoja de cálculo ODS y la visualiza
        """
        if not self.cursor():
            return

        cursor = FLSqlCursor(self.cursor().curName())
        filter_ = self.cursor().curFilter()
        if not filter_:
            filter_ = "1 = 1"
        if self.cursor().sort():
            filter_ += " ORDER BY %s" % self.cursor().sort()
        cursor.select(filter_)
        from pineboolib.qt3_widgets.messagebox import MessageBox as QMessageBox

        if config.value("ebcomportamiento/FLTableExport2Calc", False):
            QMessageBox.information(
                self.topWidget,
                self.tr("Opción deshabilitada"),
                self.tr("Esta opción ha sido deshabilitada por el administrador"),
                QMessageBox.Ok,
            )
            return

        mtd = cursor.metadata()
        if not mtd:
            return

        tdb = self.tableRecords()
        if not hasattr(tdb, "cursor"):
            return

        from pineboolib.fllegacy.aqsobjects.aqods import (
            AQOdsStyle,
            AQOdsGenerator,
            AQOdsSpreadSheet,
            AQOdsSheet,
            AQOdsRow,
            AQOdsColor,
            AQOdsImage,
        )

        # hor_header = tdb.horizontalHeader()
        title_style = [AQOdsStyle.Align_center, AQOdsStyle.Text_bold]
        border_bot = AQOdsStyle.Border_bottom
        border_right = AQOdsStyle.Border_right
        border_left = AQOdsStyle.Border_left
        italic = AQOdsStyle.Text_italic
        ods_gen = AQOdsGenerator
        spread_sheet = AQOdsSpreadSheet(ods_gen)
        sheet = AQOdsSheet(spread_sheet, mtd.alias())
        tdb_num_rows = cursor.size()
        tdb_num_cols = len(mtd.fieldNames())

        util = FLUtil()
        id_pix = 0
        pd = util.createProgressDialog("Procesando", tdb_num_rows)
        util.setProgress(1)
        row = AQOdsRow(sheet)
        row.addBgColor(AQOdsColor(0xE7E7E7))
        for i in range(tdb_num_cols):
            field = mtd.indexFieldObject(tdb.visual_index_to_logical_index(i))
            if field is not None and field.visibleGrid():
                row.opIn(title_style)
                row.opIn(border_bot)
                row.opIn(border_left)
                row.opIn(border_right)
                row.opIn(field.alias())

        row.close()

        # cur = tdb.cursor()
        # cur_row = tdb.currentRow()

        cursor.first()

        for r in range(tdb_num_rows):
            if pd.wasCanceled():
                break

            row = AQOdsRow(sheet)
            for c in range(tdb_num_cols):
                # idx = tdb.indexOf(c)  # Busca si la columna se ve
                # if idx == -1:
                #    continue

                field = mtd.indexFieldObject(tdb.visual_index_to_logical_index(c))
                if field is not None and field.visibleGrid():
                    val = cursor.valueBuffer(field.name())
                    if field.type() == "double":
                        row.setFixedPrecision(mtd.fieldPartDecimal(field.name()))
                        row.opIn(float(val))

                    elif field.type() == "date":
                        if val is not None:
                            val = str(val)
                            if val.find("T") > -1:
                                val = val[0 : val.find("T")]

                            row.opIn(val)
                        else:
                            row.coveredCell()

                    elif field.type() in ("bool", "unlock"):
                        str_ = self.tr("Sí") if val else self.tr("No")
                        row.opIn(italic)
                        row.opIn(str_)

                    elif field.type() == "pixmap":
                        if val:
                            if val.find("cacheXPM") > -1:
                                pix = QPixmap(val)
                                if not pix.isNull():

                                    pix_name = "pix%s_" % id_pix
                                    id_pix += 1
                                    row.opIn(
                                        AQOdsImage(
                                            pix_name,
                                            round((pix.width() * 2.54) / 98, 2) * 20,
                                            round((pix.height() * 2.54) / 98, 2) * 20,
                                            0,
                                            0,
                                            val,
                                        )
                                    )
                                else:
                                    row.coveredCell()

                            else:
                                row.coveredCell()
                        else:
                            row.coveredCell()

                    else:
                        if isinstance(val, list):
                            val = ",".join(val)

                        if val:
                            row.opIn(str(val))
                        else:
                            row.coveredCell()
            row.close()
            if not r % 4:
                util.setProgress(r)

            cursor.next()

        # cur.seek(cur_row)
        sheet.close()
        spread_sheet.close()
        from PyQt5.QtWidgets import qApp

        util.setProgress(tdb_num_rows)
        qApp.setOverrideCursor(QtCore.Qt.WaitCursor)
        file_name = "%s/%s%s.ods" % (
            aqApp.tmp_dir(),
            mtd.name(),
            QtCore.QDateTime.currentDateTime().toString("ddMMyyyyhhmmsszzz"),
        )
        ods_gen.generateOds(file_name)

        SysBaseType.openUrl(file_name)

        qApp.restoreOverrideCursor()
        util.destroyProgressDialog()

    def switchSortOrder(self, col: int = 0) -> None:
        """
        Conmuta el sentido de la ordenación de los registros de la tabla, de ascendente a descendente y
        viceversa. Los registros siempre se ordenan por la primera columna.
        Si la propiedad autoSortColumn es TRUE.
        """
        if not self.autoSortColumn_:
            return
        if self.tableRecords_:
            if self.tableRecords_.logical_index_to_visual_index(
                col
            ) == self.tableRecords_.visual_index_to_column_index(self.sortColumn_):

                self.orderAsc_ = not self.orderAsc_

            self.setSortOrder(self.orderAsc_, self.sortColumn_)

    @decorators.pyqtSlot(str)
    def filterRecords(self, p: str) -> None:
        """
        Filtra los registros de la tabla utilizando el primer campo, según el patrón dado.

        Este slot está conectado al cuadro de texto de busqueda del componente,
        tomando el contenido de este como patrón para el filtrado.

        @param p Cadena de caracteres con el patrón de filtrado
        """
        if not self.cursor().model():
            return
        bFilter: Optional[str] = None
        if not self.tableRecords_:
            raise Exception("tableRecords_ is not defined!")

        # if p:
        #    p = "%s%%" % p

        refreshData = False
        # if p.endswith("%"): refreshData = True

        msec_refresh = 400
        column = self.tableRecords_.header().logicalIndex(self.sortColumn_)
        colidx = self.tableRecords_.visual_index_to_column_index(column)
        if colidx is None:
            raise Exception("Unexpected: Column not found")
        field = self.cursor().model().metadata().indexFieldObject(colidx)
        bFilter = self.cursor().db().manager().formatAssignValueLike(field, p, True)

        idMod = (
            self.cursor()
            .db()
            .managerModules()
            .idModuleOfFile(self.cursor().metadata().name() + ".mtd")
        )
        functionQSA = idMod + ".tableDB_filterRecords_" + self.cursor().metadata().name()

        vargs = []
        vargs.append(self.cursor().metadata().name())
        vargs.append(p)
        vargs.append(field.name())
        vargs.append(bFilter)

        if functionQSA:
            msec_refresh = 200
            ret = None
            try:
                from pineboolib.application import project

                ret = project.call(functionQSA, vargs, None, False)
                logger.debug("functionQSA:%s:", functionQSA)
            except Exception:
                pass
            else:
                if ret is not isinstance(ret, bool):
                    bFilter = ret
                else:
                    if p == "":
                        bFilter = None

        self.refreshDelayed(msec_refresh, refreshData)
        if bFilter:
            self.filter_ = bFilter
        else:
            self.filter_ = ""

    def setSortOrder(self, ascending: bool = True, col_order: Optional[int] = None) -> None:

        order = Qt.AscendingOrder if ascending else Qt.DescendingOrder

        col = col_order if col_order is not None else self.sortColumn_
        if self.tableRecords_:
            while True:

                column = self.tableRecords_.header().logicalIndex(col)
                if not self.tableRecords_.isColumnHidden(column):
                    break
                col += 1
            self.tableRecords_.sortByColumn(column, order)

    def isSortOrderAscending(self) -> bool:
        return self.orderAsc_

    def activeTabData(self, b: bool) -> None:
        """
        Activa la tabla de datos
        """
        # if (self.topWidget and not self.tabTable.visibleWidget() == self.tabData):
        if self.tabFilter is not None:
            self.tabFilter.hide()
        if self.tabData is not None:
            self.tabData.show()
        self.refreshTabData()
        # self.tabTable.raiseWidget(self.tabData)

    def activeTabFilter(self, b: bool) -> None:
        """
        Activa la tabla de filtro
        """
        # if (self.topWidget and not self.tabTable.visibleWidget() == self.tabFilter):
        if self.tabData is not None:
            self.tabData.hide()
        if self.tabFilter is not None:
            self.tabFilter.show()
        self.refreshTabFilter()
        # self.tabTable.raiseWidget(self.tabFilter)

    def tdbFilterClear(self) -> None:
        """
        Limpia e inicializa el filtro
        """
        if not self.topWidget:
            return

        self.tabFilterLoaded = False
        self.refreshTabFilter()

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
    currentChanged = QtCore.pyqtSignal()

    def primarysKeysChecked(self) -> List[Any]:
        return self.tableRecords().primarysKeysChecked()

    def clearChecked(self) -> None:
        self.tableRecords().clearChecked()

    def setPrimaryKeyChecked(self, name: str, b: bool) -> None:
        self.tableRecords().setPrimaryKeyChecked(name, b)
