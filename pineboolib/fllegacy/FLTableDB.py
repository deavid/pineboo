# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

from pineboolib import decorators
from pineboolib.utils import DefFun, filedir
from pineboolib.flcontrols import QComboBox, QTable

from pineboolib.fllegacy.FLDataTable import FLDataTable
from pineboolib.fllegacy.FLFormRecordDB import FLFormRecordDB
from pineboolib.fllegacy.FLSqlCursor import FLSqlCursor
from pineboolib.fllegacy.FLRelationMetaData import FLRelationMetaData
from pineboolib.fllegacy.FLFormSearchDB import FLFormSearchDB
from pineboolib.fllegacy.FLFieldMetaData import FLFieldMetaData
from pineboolib.fllegacy.FLUtil import FLUtil
from pineboolib.fllegacy.FLSettings import FLSettings
from pineboolib.fllegacy.FLFieldDB import FLDoubleValidator,\
    FLUIntValidator, FLIntValidator

import pineboolib
import logging
from PyQt5.QtWidgets import QTextEdit
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

    tdbFilter = None
    mapCondType = None

    _parent = None
    _name = None
    loadLater_ = None

    tdbFilter = None

    pbData = None
    pbFilter = None
    pbOdf = None

    comboBoxFieldToSearch = None
    comboBoxFieldToSearch2 = None
    tableRecords_ = None
    lineEditSearch = None

    tabDataLayout = None
    tabControlLayout = None

    dataLayout = None
    tabData = None
    tabFilter = None
    buttonsLayout = None
    masterLayout = None
    tabFilterLoaded = False

    _controlsInit = None

    tdbFilterBuildWhere_ = None
    filterHidden_ = False
    findHidden_ = False

    """
    Tamaño de icono por defecto
    """
    iconSize = None

    """
    constructor
    """

    def __init__(self, parent, name=None):
        super(FLTableDB, self).__init__(parent)
        self.topWidget = parent
        self.showAllPixmaps_ = True
        self.tdbFilterBuildWhere_ = None
        self.sortColumn_ = 0
        self.sortColumn2_ = 1
        self.sortColumn3_ = 2
        self.autoSortColumn_ = True
        self.tabFilterLoaded = False
        self.timer_1 = QtCore.QTimer(self)
        self._name = name
        self.checkColumnVisible_ = False
        self.tdbFilterLastWhere_ = u""
        self.filter_ = u""
        self.iconSize = pineboolib.project._DGI.iconSize()

    def __getattr__(self, name):
        return DefFun(self, name)

    def load(self):
        # Es necesario pasar a modo interactivo lo antes posible
        # Sino, creamos un bug en el cierre de ventana: se recarga toda la tabla para saber el tamaño
        # print("FLTableDB(%s): setting columns in interactive mode" % self._tableName)
        parent_cursor = None
        while True:  # Ahora podemos buscar el cursor ... porque ya estamos añadidos al formulario
            if isinstance(self.topWidget.parentWidget(), FLFormSearchDB):
                self.topWidget = self.topWidget.parentWidget()
            try:
                parent_cursor = self.topWidget.cursor()
            except Exception:
                logger.exception("Error ignorado al intentar encontrar el cursor padre")
            if not isinstance(parent_cursor, FLSqlCursor):
                parent_cursor = None
            if parent_cursor:
                break
            new_parent = self.topWidget.parentWidget()
            if new_parent is None:
                break
            self.topWidget = new_parent

        if not parent_cursor:
            print("FLTableDB : Uno de los padres o antecesores de FLTableDB deber ser de la clase FLFormDB o heredar de ella")
            return

        self.cursor_ = self.topWidget.cursor_
        self.setFont(QtWidgets.QApplication.font())

        if not self._name:
            self.setName("FLTableDB")

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.refreshDelayed)

        # FIXME: El problema de que aparezca al editar un registro que no es, es por carga doble de initCursor()
        # ...... Cuando se lanza showWidget, y tiene _initCursorWhenLoad, lanza initCursor y luego otra vez.
        # ...... esta doble carga provoca el error y deja en el formulario el cursor original.

        self.mapCondType = []

        self.initCursor()
        self._loaded = True
        self.showWidget()

        if DEBUG:
            print("**FLTableDB::name: %r cursor: %r" %
                  (self.objectName(), self.cursor_.d.nameCursor_))

    def setName(self, name):
        self._name = name

    """
    Inicia el cursor segun este campo sea de la tabla origen o de
    una tabla relacionada
    """

    def initCursor(self):
        if not self.topWidget or not self.cursor_:
            return

        if not self.cursor_.metadata():
            return

        tMD = self.cursor_.metadata()
        if not self.sortField_:
            if tMD:
                self.sortField_ = tMD.field(tMD.primaryKey())

        ownTMD = None
        if self.tableName_:
            if DEBUG:
                print("**FLTableDB::name: %r tableName: %r" %
                      (self.objectName(), self.tableName_))

            if not self.cursor_.db().manager().existsTable(self.tableName_):
                ownTMD = True
                tMD = self.cursor_.db().manager().createTable(self.tableName_)
            else:
                ownTMD = True
                tMD = self.cursor_.db().manager().metadata(self.tableName_)

            if not tMD or isinstance(tMD, bool):
                return

            if not self.foreignField_ or not self.fieldRelation_:
                if not self.cursor_.metadata():
                    if ownTMD and tMD and not tMD.inCache():
                        del tMD
                    return

                if not self.cursor_.metadata().name() == self.tableName_:
                    ctxt = self.cursor_.context()
                    self.cursor_ = FLSqlCursor(
                        self.tableName_, True, self.cursor_.db().connectionName(), None, None, self)

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
        rMD = self.cursor_.metadata().relation(
            self.foreignField_, self.fieldRelation_, self.tableName_)
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

                rMD = FLRelationMetaData(self.tableName_, self.fieldRelation_,
                                         FLRelationMetaData.RELATION_1M, False, False, checkIntegrity)
                fMD.addRelationMD(rMD)
                print("FLTableDB : La relación entre la tabla del formulario %s y esta tabla %s de este campo no existe, "
                      "pero sin embargo se han indicado los campos de relación( %s, %s )"
                      % (curName, self.tableName_, self.fieldRelation_, self.foreignField_))
                print("FLTableDB : Creando automáticamente %s.%s --1M--> %s.%s" %
                      (curName, self.foreignField_, self.tableName_, self.fieldRelation_))
            else:
                print("FLTableDB : El campo ( %s ) indicado en la propiedad foreignField no se encuentra en la tabla ( %s )" % (
                    self.foreignField_, curName))
                pass

        rMD = testM1
        if not rMD:
            fMD = tMD.field(self.fieldRelation_)
            if fMD:
                rMD = FLRelationMetaData(
                    curName, self.foreignField_, FLRelationMetaData.RELATION_1M, False, False, False)
                fMD.addRelationMD(rMD)
                if DEBUG:
                    print("FLTableDB : Creando automáticamente %s.%s --1M--> %s.%s" %
                          (self.tableName_, self.fieldRelation_, curName, self.foreignField_))

            else:
                if DEBUG:
                    print("FLTableDB : El campo ( %s ) indicado en la propiedad fieldRelation no se encuentra en la tabla ( %s )" % (
                        self.fieldRelation_, self.tableName_))

        self.cursor_ = FLSqlCursor(self.tableName_, True, self.cursor_.db(
        ).connectionName(), self.cursorAux, rMD, self)
        if not self.cursor_:
            self.cursor_ = self.cursorAux
            self.cursorAux = None

        else:

            self.cursor_.setContext(self.cursorAux.context())
            if self.showed:
                try:
                    self.cursorAux.newBuffer.disconnect(self.refresh)
                except Exception:
                    pass

            self.cursorAux.newBuffer.connect(self.refresh)

        if self.cursorAux and isinstance(self.topWidget, FLFormSearchDB):
            self.topWidget.setCaption(self.cursor_.metadata().alias())
            self.topWidget_.setCursor(self.cursor_)

        if ownTMD or tMD and not tMD.inCache():
            del tMD

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
        if self.topwidget:
            self.initCursor()
        else:
            self.initFakeEditor()

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
        if self.topwidget:
            self.initCursor()
        else:
            self.initFakeEditor()
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
        if self.topwidget:
            self.initCursor()
        else:
            self.initFakeEditor()
    """
    Establece si el componente esta en modo solo lectura o no.
    """

    def setReadOnly(self, mode):
        if self.tableRecords_:
            self.readonly = mode
            self.tableRecords_.setFLReadOnly(mode)
            self.readOnlyChanged.emit(mode)

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
            self.editOnlyChanged.emit(mode)

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
            self.insertOnlyChanged.emit(mode)

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
    @decorators.BetaImplementation
    def setOrderCols(self, fields):
        if not self.cursor_:
            return
        tMD = self.cursor_.metadata()
        if not tMD:
            return

        if not self.showed:
            self.showWidget()

        fieldsList = []

        for f in fields:
            fmd = tMD.field(f)
            if fmd:
                if fmd.visibleGrid():
                    fieldsList.append(f)

        hCount = self.cursor_.model().columnCount()

        if len(fieldsList) > hCount:
            return

        i = 0
        for fi in fieldsList:
            _index = self.tableRecords_.realColumnIndex(fi)
            self.moveCol(_index, i)
            i = i + 1

        self.tableRecords_.sortByColumn(self.tableRecords_.visualIndexToRealIndex(self.sortColumn_), QtCore.Qt.AscendingOrder)
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

    """
    Devuelve la lista de los campos ordenada por sus columnas en la tabla de izquierda a derecha
    """
    @decorators.BetaImplementation
    def orderCols(self):
        list_ = []

        if not self.cursor_:
            return list_

        tMD = self.cursor_.metadata()
        if not tMD:
            return list_

        if not self.showed:
            self.showWidget()

        model = self.cursor_.model()

        if model:
            for column in range(model.columnCount()):
                list_.append(self.tableRecords._model.headerData(column, QtCore.Qt.Horizontal, QtCore.Qt.DisplayRole))

        return list_

    """
    Establece el filtro de la tabla

    @param f Sentencia Where que establece el filtro
    """

    def setFilter(self, f):
        self.filter_ = f

    """
    Devuelve el filtro de la tabla

    @return Filtro
    """

    def filter(self):
        return self.filter_

    """
    Devuelve el filtro de la tabla impuesto en el Find

    @return Filtro
    """

    def findFilter(self):
        return self.tdbFilterLastWhere_

    """
    Obtiene si la columna de selección está activada
    """

    def checkColumnEnabled(self):
        return self.checkColumnEnabled_

    """
    Establece el estado de activación de la columna de selección

    El cambio de estado no será efectivo hasta el siguiente refresh.
    """

    def setCheckColumnEnabled(self, b):
        self.checkColumnEnabled_ = b

    """
    Obiente el texto de la etiqueta de encabezado para la columna de selección
    """
    @decorators.BetaImplementation
    def aliasCheckColumn(self):
        return self.tableRecords._model.headerData(self.tableRecords_.selectionModel().selectedColumns(), QtCore.Qt.Horizontal, QtCore.Qt.DisplayRole)

    """
    Establece el texto de la etiqueta de encabezado para la columna de selección

    El cambio del texto de la etiqueta no será efectivo hasta el próximo refresh
    """

    def setAliasCheckColumn(self, t):
        self.aliasCheckColumn_ = t

    """
    Obtiene si el marco de búsqueda está oculto
    """

    def findHidden(self):
        return self.findHidden_

    """
    Oculta o muestra el marco de búsqueda

    @param  h TRUE lo oculta, FALSE lo muestra
    """

    def setFindHidden(self, h):
        if self.findHidden_ is not h:
            self.findHidden_ = h
            if h:
                self.tabControlLayout.hide()
            else:
                self.tabControlLayout.show()

    """
    Obtiene si el marco para conmutar entre datos y filtro está oculto
    """

    def filterHidden(self):
        return self.filterHidden_

    """
    Oculta o muestra el marco para conmutar entre datos y filtro

    @param  h TRUE lo oculta, FALSE lo muestra
    """

    def setFilterHidden(self, h):
        if self.filterHidden_ is not h:
            self.filterHidden_ = h
            if h:
                self.tabFilter.hide()
            else:
                self.tabFilter.show()

    """
    Ver FLTableDB::showAllPixmaps_
    """

    def showAllPixmaps(self):
        return self.showAllPixmaps_

    """
    Ver FLTableDB::showAllPixmaps_
    """

    def setShowAllPixmaps(self, s):
        self.showAllPixmaps_ = s
        if self.tableRecords_:
            self.tableRecords_.model().setShowPixmap(self.showAllPixmaps_)

    """
    Ver FLTableDB::functionGetColor_
    """

    def functionGetColor(self):
        return self.functionGetColor_

    """
    Ver FLTableDB::functionGetColor_
    """

    def setFunctionGetColor(self, f):
        self.functionGetColor_ = f
        if self.topWidget:
            if f.contains('.'):
                self.tableRecords().setFunctionGetColor(f)
            else:
                self.tableRecords().setFunctionGetColor("%s.%s" % (self.topWidget.name(), f))

    """
    Asigna el nombre de función a llamar cuando cambia el filtro.
    """

    def setFilterRecordsFunction(self, fn):
        self.tableDB_filterRecords_functionName_ = fn

    """
    Ver FLTableDB::onlyTable_
    """

    def setOnlyTable(self, on=True):
        if self.tableRecords_:
            self.onlyTable_ = on
            self.tableRecords_.setOnlyTable(on)

        self.reqOnlyTable_ = on

    def onlyTable(self):
        return self.reqOnlyTable_

    """
    Ver FLTableDB::autoSortColumn_
    """
    @decorators.NotImplementedWarn
    def setAutoSortColumn(self, on=True):
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

        if isinstance(obj, FLDataTable) or isinstance(obj, pineboolib.project.resolveDGIObject("FLLineEdit")):
            return False
        else:
            return super(FLTableDB, self).eventFilter(obj, ev)

    """
    Captura evento mostrar
    """

    def showEvent(self, e):
        super(FLTableDB, self).showEvent(e)
        if self._loaded == True:
            self.showWidget()

    """
    Redefinida por conveniencia
    """

    def showWidget(self):
        if not self._loaded:
            return

        if not self.showed and self.cursor_ and self.tableRecords_:
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

            if ownTMD and tMD:
                if not tMD.inCache():
                    del tMD

        if not self.tableRecords_:
            if not self.tableName_:
                if not self.cursor_:
                    self.initCursor()
                    self.showWidget()
                    return
                self.tableRecords()
                self.setTableRecordsCursor()
                self.showWidget()
            elif self.tableName_:
                if not self.cursor_:
                    self.initCursor()
                    self.showWidget()
                    return

                if self.tableName_ == self.cursor_.curName():
                    self.tableRecords()
                    if self.cursor_.model():
                        self.setTableRecordsCursor()
                        self.showWidget()

    """
    Crear self.tableRecords_
    """

    def createTableRecors(self):

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHeightForWidth(True)

        sizePolicyClean = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicyClean.setHeightForWidth(True)

        sizePolicyGB = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.dataLayout = QtWidgets.QHBoxLayout()  # Contiene tabData y tabFilters
        self.tabData = QtWidgets.QGroupBox()  # contiene data
        self.tabData.setSizePolicy(sizePolicyGB)

        self.tabFilter = QtWidgets.QGroupBox()  # contiene filtros
        self.tabFilter.setSizePolicy(sizePolicyGB)

        dataL = QtWidgets.QVBoxLayout()
        filterL = QtWidgets.QVBoxLayout()
        self.tabData.setLayout(dataL)
        self.tabFilter.setLayout(filterL)

        # Contiene botones lateral (datos, filtros, odf)
        self.buttonsLayout = QtWidgets.QVBoxLayout()
        self.masterLayout = QtWidgets.QVBoxLayout()  # Contiene todos los layouts

        self.pbData = QtWidgets.QPushButton(self)
        self.pbData.setSizePolicy(sizePolicy)
        self.pbData.setMinimumSize(self.iconSize)
        self.pbData.setFocusPolicy(Qt.NoFocus)
        self.pbData.setIcon(QtGui.QIcon(
            filedir("../share/icons", "fltable-data.png")))
        self.pbData.setText("")
        self.pbData.setToolTip("Mostrar registros")
        self.pbData.setWhatsThis("Mostrar registros")
        self.buttonsLayout.addWidget(self.pbData)
        self.pbData.clicked.connect(self.activeTabData)

        self.pbFilter = QtWidgets.QPushButton(self)
        self.pbFilter.setSizePolicy(sizePolicy)
        self.pbFilter.setMinimumSize(self.iconSize)
        self.pbFilter.setFocusPolicy(Qt.NoFocus)
        self.pbFilter.setIcon(QtGui.QIcon(
            filedir("../share/icons", "fltable-filter.png")))
        self.pbFilter.setText("")
        self.pbFilter.setToolTip("Mostrar filtros")
        self.pbFilter.setWhatsThis("Mostrar filtros")
        self.buttonsLayout.addWidget(self.pbFilter)
        self.pbFilter.clicked.connect(self.activeTabFilter)

        self.pbOdf = QtWidgets.QPushButton(self)
        self.pbOdf.setSizePolicy(sizePolicy)
        self.pbOdf.setMinimumSize(self.iconSize)
        self.pbOdf.setFocusPolicy(Qt.NoFocus)
        self.pbOdf.setIcon(QtGui.QIcon(
            filedir("../share/icons", "fltable-odf.png")))
        self.pbOdf.setText("")
        self.pbOdf.setToolTip("Exportar a hoja de cálculo")
        self.pbOdf.setWhatsThis("Exportar a hoja de cálculo")
        self.buttonsLayout.addWidget(self.pbOdf)
        self.pbOdf.clicked.connect(self.exportToOds)
        if FLSettings().readEntry("ebcomportamiento/FLTableExport2Calc", "false") == "true":
            self.pbOdf.setDisabled(True)

        self.pbClean = QtWidgets.QPushButton(self)
        self.pbClean.setSizePolicy(sizePolicyClean)
        self.pbClean.setMinimumSize(self.iconSize)
        self.pbClean.setFocusPolicy(Qt.NoFocus)
        self.pbClean.setIcon(QtGui.QIcon(
            filedir("../share/icons", "fltable-clean.png")))
        self.pbClean.setText("")
        self.pbClean.setToolTip("Limpiar filtros")
        self.pbClean.setWhatsThis("Limpiar filtros")
        filterL.addWidget(self.pbClean)
        self.pbClean.clicked.connect(self.tdbFilterClear)

        spacer = QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.buttonsLayout.addItem(spacer)

        self.comboBoxFieldToSearch = QtWidgets.QComboBox()
        self.comboBoxFieldToSearch2 = QtWidgets.QComboBox()
        self.lineEditSearch = QtWidgets.QLineEdit()
        label1 = QtWidgets.QLabel()
        label2 = QtWidgets.QLabel()

        label1.setText("Buscar")
        label2.setText("en")

        self.tabControlLayout = QtWidgets.QHBoxLayout()

        self.tabControlLayout.addWidget(label1)
        self.tabControlLayout.addWidget(self.lineEditSearch)
        self.tabControlLayout.addWidget(label2)
        self.tabControlLayout.addWidget(self.comboBoxFieldToSearch)
        self.tabControlLayout.addWidget(self.comboBoxFieldToSearch2)

        self.masterLayout.addLayout(self.tabControlLayout)
        self.masterLayout.addLayout(self.dataLayout)

        self.tableRecords_ = FLDataTable(self, "tableRecords")
        self.tableRecords_.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setFocusProxy(self.tableRecords_)
        # metemos el tablerecord en el datalayout
        dataL.addWidget(self.tableRecords_)

        self.lineEditSearch.installEventFilter(self)
        self.tableRecords_.installEventFilter(self)

        self.setLayout(self.masterLayout)
        # self.setTabOrder(self.tableRecords_, self.lineEditSearch)
        self.setTabOrder(self.lineEditSearch, self.comboBoxFieldToSearch)
        self.setTabOrder(self.comboBoxFieldToSearch,
                         self.comboBoxFieldToSearch2)
        self.tableRecords_.recordChoosed.connect(self.currentChanged)

        self.lineEditSearch.textChanged.connect(self.filterRecords)
        model = self.cursor_.model()

        # Se añade data, filtros y botonera
        self.dataLayout.addWidget(self.tabData)
        self.dataLayout.addWidget(self.tabFilter)
        self.tabFilter.hide()
        self.dataLayout.addLayout(self.buttonsLayout)

        if model:
            for column in range(model.columnCount()):
                if model.metadata() is None:
                    return
                field = model.metadata().indexFieldObject(column)
                if not field.visibleGrid():
                    self.tableRecords_.setColumnHidden(column, True)
                else:
                    self.comboBoxFieldToSearch.addItem(model.headerData(
                        column, QtCore.Qt.Horizontal, QtCore.Qt.DisplayRole))
                    self.comboBoxFieldToSearch2.addItem(model.headerData(
                        column, QtCore.Qt.Horizontal, QtCore.Qt.DisplayRole))
            self.comboBoxFieldToSearch.addItem("*")
            self.comboBoxFieldToSearch2.addItem("*")
            self.comboBoxFieldToSearch.setCurrentIndex(self.sortColumn_)
            self.comboBoxFieldToSearch2.setCurrentIndex(self.sortColumn2_)
            self.comboBoxFieldToSearch.currentIndexChanged.connect(
                self.putFirstCol)
            self.comboBoxFieldToSearch2.currentIndexChanged.connect(
                self.putSecondCol)
            self._controlsInit = True

        else:
            self.comboBoxFieldToSearch.addItem("*")
            self.comboBoxFieldToSearch2.addItem("*")

        self.tdbFilter = QTable()
        filterL.addWidget(self.tdbFilter)

        return self.tableRecords_

    """
    Obtiene el componente tabla de registros
    """

    def tableRecords(self):
        if self.tableRecords_:
            return self.tableRecords_
        else:
            return self.createTableRecors()

    """
    Asigna el cursor actual del componente a la tabla de registros
    """

    def setTableRecordsCursor(self):
        self.tableRecords().setFLSqlCursor(self.cursor_)
        try:
            self.tableRecords().doubleClicked.disconnect(self.chooseRecord)
        except Exception:
            pass
        if FLSettings().readEntry("ebcomportamiento/FLTableDoubleClick", "false") == "false":
            self.tableRecords().doubleClicked.connect(self.chooseRecord)

        if self.checkColumnEnabled_:
            self.tableRecords().clicked.connect(self.tableRecords().setChecked)

    """
    Refresca la pestaña datos aplicando el filtro
    """

    def refreshTabData(self):
        tdbWhere = self.tdbFilterBuildWhere()
        if not tdbWhere == self.tdbFilterLastWhere_:
            self.tdbFilterLastWhere_ = tdbWhere

        self.refresh(False, True)

    """
    Refresca la pestaña del filtro
    """

    def refreshTabFilter(self):
        if self.tabFilterLoaded:
            return

        horizHeader = self.tableRecords().horizontalHeader()
        if not horizHeader:
            return

        hCount = horizHeader.count() - self.sortColumn_
        if self.tdbFilter.numRows() < hCount and self.cursor_:
            tMD = self.cursor_.metadata()
            if not tMD:
                return

            field = None
            editor_ = None
            type = None
            len = None
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
            self.tdbFilter.setColumnLabels(
                ",", util.tr("Campo,Condición,Valor,Desde,Hasta"))

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
                _label = self.cursor().model().headerData(i + self.sortColumn_,
                                                          QtCore.Qt.Horizontal, QtCore.Qt.DisplayRole)
                field = tMD.field(tMD.fieldAliasToName(_label))

                if not field:
                    i = i + 1
                    continue

                if not field.visibleGrid():
                    i = i + 1
                    continue

                self.tdbFilter.setText(_linea, 0, _label)

                type = field.type()
                len = field.length()
                partInteger = field.partInteger()
                partDecimal = field.partDecimal()
                rX = field.regExpValidator()
                ol = field.hasOptionsList()

                cond = QComboBox()
                if not type == "pixmap":
                    condList = [util.tr("Todos"), util.tr("Igual a Valor"), util.tr(
                        "Distinto de Valor"), util.tr("Vacío"), util.tr("No Vacío")]
                    if not type == "bool":
                        condList = [
                            util.tr("Todos"), util.tr("Igual a Valor"), util.tr("Distinto de Valor"), util.tr("Vacío"),
                            util.tr("No Vacío"), util.tr("Contiene Valor"), util.tr("Empieza por Valor"), util.tr("Acaba por Valor"),
                            util.tr("Mayor que Valor"), util.tr("Menor que Valor"), util.tr("Desde - Hasta")]
                    cond.insertStringList(condList)
                    self.tdbFilter.setCellWidget(_linea, 1, cond)

                j = 2
                while (j < 5):
                    editor_ = None
                    if type in ("uint, int", "double", "string", "stringList"):
                        if ol:
                            editor_ = QComboBox()
                            olTranslated = []
                            olNoTranslated = field.optionsList()
                            # print(field.optionsList())
                            # countOl = olNoTranslated.count()
                            for z in olNoTranslated:
                                olTranslated.append(
                                    util.translate("Metadata", z))

                            editor_.insertStringList(olTranslated)
                        else:
                            editor_ = pineboolib.project.resolveDGIObject(
                                "FLLineEdit")(self)

                            if type == "double":
                                editor_.setValidator(FLDoubleValidator(
                                    0, pow(10, partInteger) - 1, partDecimal, editor_))
                                editor_.setAlignment(Qt.AlignRight)
                            else:
                                if type in ("uint", "int"):
                                    if type == "uint":
                                        editor_.setValidator(FLUIntValidator(
                                            0, pow(10, partInteger) - 1, editor_))
                                    else:
                                        editor_.setValidator(FLIntValidator(
                                            pow(10, partInteger) - 1 * (-1), pow(10, partInteger) - 1, editor_))

                                    editor_.setAlignment(Qt.AlignRight)
                                else:
                                    if len > 0:
                                        editor_.setMaxLength(len)
                                        if rX:
                                            editor_.setValidator(rX, editor_)

                                    editor_.setAlignment(Qt.AlignLeft)

                    if type == "serial":
                        editor_ = pineboolib.project.resolveDGIObject(
                            "FLSpinBox")()
                        editor_.setMaxValue(pow(10, partInteger) - 1)

                    if type == "pixmap":
                        self.tdbFilter.setRowReadOnly(i, True)

                    if type == "date":
                        editor_ = pineboolib.project.resolveDGIObject(
                            "FLDateEdit")(self, _label)
                        # editor_.setOrder(FLDateEdit.DMY) # FIXME
                        editor_.setAutoAdvance(True)
                        editor_.setSeparator("-")
                        da = QtCore.QDate()
                        editor_.setDate(da.currentDate())

                    if type == "time":
                        editor_ = pineboolib.project.resolveDGIObject(
                            "FLTimeEdit")(self)
                        timeNow = QtCore.QTime.currentTime()
                        editor_.setTime(timeNow)

                    if type in (FLFieldMetaData.Unlock, "bool"):
                        editor_ = FLCheckBox(self)

                    if editor_:
                        self.tdbFilter.setCellWidget(_linea, j, editor_)

                    j = j + 1

                i = i + 1
                _linea = _linea + 1

        k = 0

        while k < 5:
            self.tdbFilter.adjustColumn(k)
            k = k + 1

        self.tabFilterLoaded = True  # Con esto no volvemos a cargar y reescribir el filtro

    """
    Para obtener la enumeración correspondiente a una condición para el filtro a partir de
    su literal
    """

    def decodeCondType(self, strCondType):
        i = 0
        while i < len(self.mapCondType):
            if strCondType == self.mapCondType[i]:
                return i

            i = i + 1

        return self.All

    """
    Construye la claúsula de filtro en SQL a partir del contenido de los valores
    definidos en la pestaña de filtro
    """

    def tdbFilterBuildWhere(self):
        if not self.topWidget_:
            return None

        rCount = self.tdbFilter.numRows()
        # rCount = self.cursor_.model().columnCount()
        if not rCount or not self.cursor_:
            return None

        tMD = self.cursor_.metadata()
        if not tMD:
            return None

        field = None
        cond = None
        type = None
        condType = None
        fieldName = None
        condValue = None
        where = ""
        fieldArg = None
        arg2 = None
        arg4 = None

        ol = None
        i = 0

        while i < rCount:
            fieldName = tMD.fieldAliasToName(self.tdbFilter.text(i, 0))
            field = tMD.field(fieldName)
            if not field:
                i = i + 1
                continue

            cond = self.tdbFilter.cellWidget(i, 1)

            if not cond:
                i = i + 1
                continue

            condType = self.decodeCondType(cond.currentText())
            if condType == self.All:
                i = i + 1
                continue

            if (tMD.isQuery()):
                qry = self.cursor_.db().manager().query(
                    self.cursor_.metadata().query(), self.cursor_)

                if qry:
                    list = qry.fieldList()

                    qField = None
                    for qField in list:
                        if qField.endswith(".%s" % fieldName):
                            break

                    fieldName = qField
            else:
                fieldName = tMD.name() + "." + fieldName

            fieldArg = fieldName
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
                        arg2 = self.cursor_.db().manager().formatValue(
                            type, editorOp1.currentText(), True)
                        arg4 = self.cursor_.db().manager().formatValue(
                            type, editorOp2.currentText(), True)
                    else:
                        editorOp1 = self.tdbFilter.cellWidget(i, 2)
                        arg2 = self.cursor_.db().manager().formatValue(
                            type, editorOp1.currentText(), True)
                else:
                    if condType == self.FromTo:
                        editorOp1 = self.tdbFilter.cellWidget(i, 3)
                        editorOp2 = self.tdbFilter.cellWidget(i, 4)
                        arg2 = self.cursor_.db().manager().formatValue(type, editorOp1.text(), True)
                        arg4 = self.cursor_.db().manager().formatValue(type, editorOp2.text(), True)
                    else:
                        editorOp1 = self.tdbFilter.cellWidget(i, 2)
                        arg2 = self.cursor_.db().manager().formatValue(type, editorOp1.text(), True)

            if type == "serial":
                if condType == self.FromTo:
                    editorOp1 = self.tdbFilter.cellWidget(i, 3)
                    editorOp2 = self.tdbFilter.cellWidget(i, 4)
                    arg2 = editorOp1.value()
                    arg4 = editorOp2.value()
                else:
                    editorOp1 = pineboolib.project.resolveDGIObject(
                        "FLSpinBox")(self.tdbFilter.cellWidget(i, 2))
                    arg2 = editorOp1.value()

            if type == "date":
                if condType == self.FromTo:
                    editorOp1 = self.tdbFilter.cellWidget(i, 3)
                    editorOp2 = self.tdbFilter.cellWidget(i, 4)
                    arg2 = self.cursor_.db().manager().formatValue(
                        type, editorOp1.date().toString("dd-MM-yyyy"))
                    arg4 = self.cursor_.db().manager().formatValue(
                        type, editorOp2.date().toString("dd-MM-yyyy"))
                else:
                    editorOp1 = self.tdbFilter.cellWidget(i, 2)
                    arg2 = self.cursor_.db().manager().formatValue(
                        type, editorOp1.date().toString("dd-MM-yyyy"))

            if type == "time":
                if condType == self.FromTo:
                    editorOp1 = self.tdbFilter.cellWidget(i, 3)
                    editorOp2 = self.tdbFilter.cellWidget(i, 4)
                    arg2 = self.cursor_.db().manager().formatValue(
                        type, editorOp1.time().toString(Qt.ISODate))
                    arg4 = self.cursor_.db().manager().formatValue(
                        type, editorOp2.time().toString(Qt.ISODate))
                else:
                    editorOp1 = self.tdbFilter.cellWidget(i, 2)
                    arg2 = self.cursor_.db().manager().formatValue(
                        type, editorOp1.time().toString(Qt.ISODate))

            if type in ("unlock", "bool"):
                editorOp1 = self.tdbFilter.cellWidget(i, 2)
                checked_ = False
                if editorOp1.isChecked():
                    checked_ = True
                arg2 = self.cursor_.db().manager().formatValue(type, checked_)

            if where:
                where += " AND"

            condValue = " " + fieldArg
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
                condValue += " >= " + str(arg2) + \
                    " AND " + fieldArg + " <= " + (arg4)
            elif condType == self.Null:
                condValue += " IS NULL "
            elif condType == self.notNull:
                condValue += " IS NOT NULL "

            where += condValue

            i = i + 1

        print("where-devuelto", where)
        return where

    """
    Inicializa un editor falso y no funcional.

    Esto se utiliza cuando se está editando el formulario con el diseñador y no
    se puede mostrar el editor real por no tener conexión a la base de datos.
    Crea una previsualización muy esquemática del editor, pero suficiente para
    ver la posisicón y el tamaño aproximado que tendrá el editor real.
    """
    @decorators.BetaImplementation
    def initFakeEditor(self):
        if not self.fakeEditor_:
            self.fakeEditor_ = QTextEdit(self.tabData)

            sizePolizy = QtWidgets.QSizePolicy(7, QtWidgets.QSizePolicy.Expanding)
            sizePolicy.setHeightForWidth(True)

            self.fakeEditor_.setSizePolicy(sizePolizy)
            self.fakeEditor_.setTabChangesFocus(True)
            self.fakeEditor_.setFocusPolicy(QtCore.Qt.StrongFocus)
            self.setFocusProxy(self.fakeEditor_)
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
    sortColumn_ = 0

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
    autoSortColumn_ = True

    """
    Almacena la última claúsula de filtro aplicada en el refresco
    """
    tdbFilterLastWhere_ = ""

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
    @QtCore.pyqtSlot()
    @QtCore.pyqtSlot(bool)
    @QtCore.pyqtSlot(bool, bool)
    def refresh(self, refreshHead=False, refreshData=True):
        if not self.cursor_ or not self.tableRecords_:
            return

        tMD = self.cursor_.metadata()
        if not tMD:
            return

        if not self.tableName_:
            self.tableName_ = tMD.name()

        if self.checkColumnEnabled_:
            if not self.checkColumnVisible_:
                fieldCheck = tMD.field(self.fieldNameCheckColumn_)
                if not fieldCheck:
                    self.fieldNameCheckColumn_ = "%s_check_column" % tMD.name()

                    if self.fieldNameCheckColumn_ not in tMD.fieldsNames():
                        fieldCheck = FLFieldMetaData(self.fieldNameCheckColumn_, self.tr(self.aliasCheckColumn_), True, False, FLFieldMetaData.Check,
                                                     0, False, True, True, 0, 0, False, False, False, None, False, None, True, False, False)
                        tMD.addFieldMD(fieldCheck)
                    else:
                        fieldCheck = tMD.field(self.fieldNameCheckColumn_)
                self.tableRecords().cursor().model().updateColumnsCount()
                self.tableRecords().header().reset()
                self.tableRecords().header().swapSections(self.tableRecords().realColumnIndex(fieldCheck.name()), self.sortColumn_)
                self.checkColumnVisible_ = True
                self.sortColumn_ = 1
                self.sortColumn2_ = 2
                self.sortColumn3_ = 3

                # for i in enumerate(buffer_.count()):
                #    buffer_.setGenerated(i, True)

        else:
            self.sortColumn_ = 0
            self.sortColumn2_ = 1
            self.sortColumn3_ = 2
            self.checkColumnVisible_ = False

        if refreshHead:
            if not self.tableRecords_.isHidden():
                self.tableRecords_.hide()

            model = self.cursor_.model()
            for column in range(model.columnCount()):
                field = model.metadata().indexFieldObject(column)
                if not field.visibleGrid() or (field.type() is "check" and not self.checkColumnEnabled_):
                    self.tableRecords_.setColumnHidden(column, True)
                else:
                    self.tableRecords_.setColumnHidden(column, False)

            # FIXME FIX: Esto lo he implementado en otro lado manualmente. A elminar, o mover algo de aquel código aquí.

            # FIXME: Este proceso es MUY LENTO. No deberíamos hacer esto.
            # Hay que buscar alguna forma manual de iterar las primeras N filas, o calcular un
            # valor por defecto rápidamente.
            # self.tableRecords_._h_header.setResizeMode(QtGui.QHeaderView.ResizeToContents)
            # if model.rows * model.cols > 500*10:
            #    # Esto evitará que se calcule para las que tienen más de 500*10 celdas.
            #    self.tableRecords_._h_header.setResizeMode(0)
            # ... de todos modos tendríamos que, con un timer o algo para desactivar el modo. Una vez
            # ... ya redimensionadas inicialmente, lo único que hace es lastrar Pineboo mucho.

        if refreshData or self.sender():

            finalFilter = self.filter_
            if self.tdbFilterLastWhere_:
                if not finalFilter:
                    finalFilter = self.tdbFilterLastWhere_
                else:
                    finalFilter = "%s AND %s" % (
                        finalFilter, self.tdbFilterLastWhere_)

            self.tableRecords_.setPersistentFilter(finalFilter)

            self.tableRecords_.model().setShowPixmap(self.showAllPixmaps_)
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

    def refreshDelayed(self, msec=50, refreshData=True):
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
    @QtCore.pyqtSlot(bool)
    def insertRecord(self, unknown=None):

        w = self.sender()
        # if (w and (not self.cursor_ or self.reqReadOnly_ or self.reqEditOnly_ or self.reqOnlyTable_ or (self.cursor_.cursorRelation()
        #      and self.cursor_.cursorRelation().isLocked()))):
        relationLock = False

        if isinstance(self.cursor().cursorRelation(), FLSqlCursor):
            relationLock = self.cursor_.cursorRelation().isLocked()

        if w and self.browseOnly() or self.onlyTable() or self.editOnly() or relationLock:
            w.setDisabled(True)
            return

        if self.cursor_:
            self.cursor_.insertRecord()

    """
    Invoca al método FLSqlCursor::editRecord()
    """
    @QtCore.pyqtSlot(bool)
    def editRecord(self, unknown=None):
        w = self.sender()

        # if w and (not self.cursor_ or self.reqReadOnly_ or self.reqEditOnly_ or self.reqOnlyTable_ or (self.cursor_.cursorRelation()
        #       and self.cursor_.cursorRelation().isLocked())):
        relationLock = False

        if isinstance(self.cursor().cursorRelation(), FLSqlCursor):
            relationLock = self.cursor_.cursorRelation().isLocked()

        if w and self.cursor().isLocked() or self.browseOnly() or self.onlyTable() or relationLock:
            w.setDisabled(True)
            return

        if self.cursor_:
            self.cursor_.editRecord()
    """
    Invoca al método FLSqlCursor::browseRecord()
    """
    @QtCore.pyqtSlot(bool)
    def browseRecord(self, unknown):

        w = self.sender()
        if w and (not self.cursor_ or self.reqOnlyTable_):
            w.setDisabled(True)
            return

        if self.cursor_:
            self.cursor_.browseRecord()

    """
    Invoca al método FLSqlCursor::deleteRecord()
    """
    @QtCore.pyqtSlot(bool)
    def deleteRecord(self, unknown):
        w = self.sender()
        if w and (not self.cursor_ or self.reqReadOnly_ or self.reqInsertOnly_ or self.reqEditOnly_ or self.reqOnlyTable_ or
                  (self.cursor_.cursorRelation() and self.cursor_.cursorRelation().isLocked())):
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
        if w and (not self.cursor_ or self.reqReadOnly_ or self.reqEditOnly_ or self.reqOnlyTable_ or (
                self.cursor_.cursorRelation() and self.cursor_.cursorRelation().isLocked())):
            w.setDisabled(True)
            return

        if self.cursor_:
            self.cursor_.copyRecord()

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
    def putFirstCol(self, c):
        _index = c
        if isinstance(c, str):
            _index = self.tableRecords_.realColumnIndex(c)

        if _index < 0:
            return False

        self.moveCol(_index, self.sortColumn_)
        self.tableRecords_.sortByColumn(self.tableRecords_.visualIndexToRealIndex(self.sortColumn_), QtCore.Qt.AscendingOrder)
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

        self.moveCol(_index, self.sortColumn2_)
        return True

    """
    Mueve una columna de un campo origen a la columna de otro campo destino

    @param  from  Nombre del campo de la columna de origen
    @param  to    Nombre del campo de la columna de destino
    @param  firstSearch dpinelo: Indica si se mueven columnas teniendo en cuenta que esta función
            se ha llamado o no, desde el combo principal de búsqueda y filtrado
    """
    @decorators.BetaImplementation
    def moveCol(self, from_, to, firstSearch=True):
        if from_ < 0 or to < 0:
            return

        tMD = self.cursor_.metadata()
        if not tMD:
            return

        self.tableRecords_.hide()

        textSearch = self.lineEditSearch.text()

        field = self.cursor_.metadata().indexFieldObject(to)

        if to == 0:  # Si ha cambiado la primera columna

            try:
                self.comboBoxFieldToSearch.currentIndexChanged.disconnect(
                    self.putFirstCol)
            except Exception:
                pass

            self.comboBoxFieldToSearch.setCurrentIndex(from_)
            self.comboBoxFieldToSearch.currentIndexChanged.connect(
                self.putFirstCol)

            # Actializamos el segundo combo
            try:
                self.comboBoxFieldToSearch2.currentIndexChanged.disconnect(
                    self.putSecondCol)
            except Exception:
                pass
            # Falta mejorar
            if self.comboBoxFieldToSearch.currentIndex() == self.comboBoxFieldToSearch2.currentIndex():
                self.comboBoxFieldToSearch2.setCurrentIndex(
                    self.tableRecords_._h_header.logicalIndex(self.sortColumn_))
            self.comboBoxFieldToSearch2.currentIndexChanged.connect(
                self.putSecondCol)

        if (to == 1):  # Si es la segunda columna ...
            try:
                self.comboBoxFieldToSearch2.currentIndexChanged.disconnect(
                    self.putSecondCol)
            except Exception:
                pass
            self.comboBoxFieldToSearch2.setCurrentIndex(from_)
            self.comboBoxFieldToSearch2.currentIndexChanged.connect(
                self.putSecondCol)

            if self.comboBoxFieldToSearch.currentIndex() == self.comboBoxFieldToSearch2.currentIndex():
                try:
                    self.comboBoxFieldToSearch.currentIndexChanged.disconnect(
                        self.putFirstCol)
                except Exception:
                    pass
                if self.comboBoxFieldToSearch.currentIndex() == self.comboBoxFieldToSearch2.currentIndex():
                    self.comboBoxFieldToSearch.setCurrentIndex(
                        self.tableRecords_._h_header.logicalIndex(self.sortColumn2_))
                self.comboBoxFieldToSearch.currentIndexChanged.connect(
                    self.putFirstCol)

        if not textSearch:
            textSearch = self.cursor_.value(field.name())

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
            QtCore.QTimer.singleShot(
                0, self.tableRecords_.ensureRowSelectedVisible())
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
        # self.tableRecords_.show()

    """
    Posiciona el cursor en un registro valido
    """
    @decorators.BetaImplementation
    def seekCursor(self):
        return
        textSearch = self.lineEditSearch.text()
        if not textSearch:
            return

        if not self.cursor_:
            return

        # fN = self.sortField_.name()
        textSearch.replace("%", "")

        # if "'" not in textSearch and "\\" not in textSearch:
        #     sql = self.cursor_.executedQuery() + " LIMIT 1"
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

    def setEnabled(self, b):
        self.setReadOnly(not b)

    """
    Establece el ancho de una columna

    @param  field Nombre del campo de la base de datos correspondiente a la columna
    @param  w     Ancho de la columna
    """
    @decorators.NotImplementedWarn
    def setColumnWidth(self, field, w):
        pass

    """
    Selecciona la fila indicada

    @param  r   Índice de la fila a seleccionar
    """

    def setCurrentRow(self, r):
        t = self.tableRecords_
        if not t:
            return

        t.selectRow(r)

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

    def switchSortOrder(self, col=0):
        if not self.autoSortColumn_:
            return

        if self.checkColumnVisible_:
            col = col - 1

        if col == self.sortColumn_:
            self.orderAsc_ = not self.orderAsc_
        elif col == self.sortColumn2_:
            self.orderAsc2_ = not self.orderAsc2_

        self.tableRecords().hide()
        self.refresh(True, True)

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

        if p:
            p = "%s%%" % p

        refreshData = False
        # if p.endswith("%"): refreshData = True

        msec_refresh = 400
        column = self.tableRecords_._h_header.logicalIndex(self.sortColumn_)
        field = self.cursor_.model().metadata().indexFieldObject(column)

        bFilter = self.cursor_.db().manager().formatAssignValue(field, p, True)

        idMod = self.cursor_.db().managerModules().idModuleOfFile(
            self.cursor_.metadata().name() + ".mtd")

        functionQSA = idMod + ".tableDB_filterRecords_" + self.cursor_.metadata().name()

        vargs = []
        vargs.append(self.cursor_.metadata().name())
        vargs.append(p)
        vargs.append(field.name())
        vargs.append(bFilter)

        if functionQSA:
            msec_refresh = 200
            ret = ""
            try:
                ret = self.cursor_._prj.call(functionQSA, vargs, None)
                print("functionQSA:%s:" % functionQSA)
            except Exception:
                pass

            if ret:
                bFilter = ret
            else:
                if p == "":
                    bFilter = None

        self.refreshDelayed(msec_refresh, refreshData)
        self.filter_ = bFilter

    def setSortOrder(self, ascending=True):
        if ascending:
            order = Qt.AscendingOrder
        else:
            order = Qt.DescendingOrder

        self.tableRecords_.sortByColumn(self.sortColumn_, order)

    def isSortOrderAscending(self):
        return self.orderAsc_

    """
    Activa la tabla de datos
    """

    def activeTabData(self, b):
        # if (self.topWidget and not self.tabTable.visibleWidget() == self.tabData):
        self.tabFilter.hide()
        self.tabData.show()
        self.refreshTabData()
        # self.tabTable.raiseWidget(self.tabData)

    """
    Activa la tabla de filtro
    """

    def activeTabFilter(self, b):
        # if (self.topWidget and not self.tabTable.visibleWidget() == self.tabFilter):
        self.tabData.hide()
        self.tabFilter.show()
        self.refreshTabFilter()
        # self.tabTable.raiseWidget(self.tabFilter)

    """
    Limpia e inicializa el filtro
    """

    def tdbFilterClear(self):
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

    @QtCore.pyqtSlot()
    def chooseRecord(self):
        if isinstance(self.topWidget, FLFormSearchDB):
            if self.topWidget.inExec_:
                self.topWidget.accept()
                return

        relationLock = False

        if isinstance(self.cursor().cursorRelation(), FLSqlCursor):
            relationLock = self.cursor_.cursorRelation().isLocked()

        if self.cursor().isLocked() or self.browseOnly() or relationLock:
            print("FLTable(%s):Registro bloqueado. Modo Solo lectura." %
                  self.cursor().curName())
            self.cursor().browseRecord()
        else:
            self.cursor().editRecord()

    def primarysKeysChecked(self):
        return self.tableRecords().primarysKeysChecked()

    def clearChecked(self):
        self.tableRecords().clearChecked()

    def setPrimaryKeyChecked(self, name, b):
        name = str(name)
        self.tableRecords().setPrimaryKeyChecked(name, b)
