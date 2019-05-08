# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

from pineboolib import decorators
from pineboolib.utils import DefFun, filedir


from pineboolib.plugins.dgi.dgi_qt.dgi_objects.fldatatable import FLDataTable
from pineboolib.fllegacy.flsqlcursor import FLSqlCursor
from pineboolib.fllegacy.flrelationmetadata import FLRelationMetaData
from pineboolib.plugins.dgi.dgi_qt.dgi_objects.flformsearchdb import FLFormSearchDB
from pineboolib.plugins.dgi.dgi_qt.dgi_objects.flformrecorddb import FLFormRecordDB
from pineboolib.plugins.dgi.dgi_qt.dgi_objects.flformdb  import FLFormDB
from pineboolib.fllegacy.flfieldmetadata import FLFieldMetaData
from pineboolib.fllegacy.flutil import FLUtil
from pineboolib.fllegacy.flsettings import FLSettings
from pineboolib.plugins.dgi.dgi_qt.dgi_objects.fldoublevalidator import FLDoubleValidator
from pineboolib.plugins.dgi.dgi_qt.dgi_objects.fluintvalidator import FLUIntValidator
from pineboolib.plugins.dgi.dgi_qt.dgi_objects.flintvalidator import  FLIntValidator

import pineboolib
import logging
from PyQt5.QtGui import QPixmap
logger = logging.getLogger(__name__)

import time

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
    _loaded = False
    """
    Tamaño de icono por defecto
    """
    iconSize = None

    """
    constructor
    """

    def __init__(self, parent=None, name=None):
        if parent is None:
            return
        super(FLTableDB, self).__init__(parent)
        self.topWidget = parent
        self.showAllPixmaps_ = True
        self.tdbFilterBuildWhere_ = None
        self.sortColumn_ = 0
        self.sortColumn2_ = 1
        self.sortColumn3_ = 2
        self.autoSortColumn_ = True
        self.orderAsc_ = True
        self.orderAsc2_ = True
        self.orderAsc3_ = True
        self.tabFilterLoaded = False
        self.timer_1 = QtCore.QTimer(self)
        if name:
            self.setObjectName(name)
        self.checkColumnVisible_ = False
        self.tdbFilterLastWhere_ = None
        self.filter_ = None
        self.iconSize = pineboolib.project._DGI.iconSize()
        self.tabControlLayout = QtWidgets.QHBoxLayout()
        self.tabFilter = QtWidgets.QFrame()  # contiene filtros
        self.functionGetColor_ = None

        while not isinstance(self.topWidget, FLFormDB):
            self.topWidget = self.topWidget.parentWidget()
            if not self.topWidget:
                break

        self._loaded = False
        self.createFLTableDBWidget()

    def __getattr__(self, name):
        return DefFun(self, name)

    def load(self):

        # Es necesario pasar a modo interactivo lo antes posible
        # Sino, creamos un bug en el cierre de ventana: se recarga toda la tabla para saber el tamaño
        # print("FLTableDB(%s): setting columns in interactive mode" % self._tableName))
        if self.loaded():
            return
        

        if not self.topWidget.cursor():
            print("FLTableDB : Uno de los padres o antecesores de FLTableDB deber ser de la clase FLFormDB o heredar de ella")
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
            print("**FLTableDB::name: %r cursor: %r" %
                  (self.objectName(), self.cursor_.d.nameCursor_))

    def loaded(self):
        return self._loaded
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
        if self.sortField_ is None:
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
                if cursorTopWidget and cursorTopWidget.metadata().name() != self.tableName_:
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
            if fMD is not None:
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
            if fMD is not None:
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

        # Si hay cursorTopWidget no machaco el cursor de topWidget
        if self.cursorAux and isinstance(self.topWidget, FLFormSearchDB) and not cursorTopWidget:
            self.topWidget.setCaption(self.cursor_.metadata().alias())
            self.topWidget.setCursor(self.cursor_)

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
        if self.topWidget:
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
        if self.topWidget:
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
        if self.topWidget:
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

        self.reqInsertOnly_ = mode

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
            if fmd is not None:
                if fmd.visibleGrid():
                    fieldsList.append(f)

        hCount = self.cursor_.model().columnCount()

        if len(fieldsList) > hCount:
            return

        i = 0
        for fi in fieldsList:
            _index = self.tableRecords_.column_name_to_column_index(fi)
            self.moveCol(_index, i)
            i = i + 1

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
    @decorators.Deprecated
    def setFindHidden(self, h):
        # if self.findHidden_ is not h:
        #    self.findHidden_ = h
        #    if h:
        #        self.tabControlLayout.hide()
        #    else:
        #        self.tabControlLayout.show()
        pass

    """
    Obtiene si el marco para conmutar entre datos y filtro está oculto
    """

    def filterHidden(self):
        return self.filterHidden_

    """
    Oculta o muestra el marco para conmutar entre datos y filtro

    @param  h TRUE lo oculta, FALSE lo muestra
    """
    @decorators.Deprecated
    def setFilterHidden(self, h):
        # if self.filterHidden_ is not h:
        #    self.filterHidden_ = h
        #    if h:
        #        self.tabFilter.hide()
        #    else:
        #        self.tabFilter.show()
        pass

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

        
        #if self.tableRecords_ is not None:
        #    self.tableRecords().setFunctionGetColor("%s.%s" % (self.topWidget.name(), f))
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

        if obj in (self.tableRecords_, self.lineEditSearch):
            return False
        else:
            return super(FLTableDB, self).eventFilter(obj, ev)

    """
    Captura evento mostrar
    """

    def showEvent(self, e):
        super(FLTableDB, self).showEvent(e)
        self.load()
        if not self.loaded():
            self.showWidget()

    """
    Redefinida por conveniencia
    """

    def showWidget(self):
        if self.showed:
            return

        if not self.topWidget:
            self.initFakeEditor()
            self.showed = True
            return
        
        if not self.cursor_:
            return

        self.showed = True

        own_tmd = False
        if self.tableName_:
            own_tmd = True
            if not self.cursor_.db().manager().existsTable(self.tableName_):
                tmd = self.cursor_.db().manager().createTable(self.tableName_)
            else:
                tmd = self.cursor_.db().manager().metadata(self.tableName_)

            if not tmd:
                return

        self.tableRecords()
        if not self.cursorAux:
            if not self.initSearch_:
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
            if isinstance(self.topWidget, FLFormRecordDB) and self.cursor_.modeAccess == FLSqlCursor.Browse:
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
            

        elif isinstance(self.topWidget, FLFormRecordDB) and self.cursor_.modeAccess() == FLSqlCursor.Browse and tmd and not tmd.isQuery():
            self.cursor_.setEdition(False)
            self.setReadOnly(True)
        

        # if own_tmd and tmd and not tmd.inCache():
        #    del tmd

    def createFLTableDBWidget(self):
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHeightForWidth(True)

        sizePolicyClean = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicyClean.setHeightForWidth(True)

        sizePolicyGB = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.dataLayout = QtWidgets.QHBoxLayout()  # Contiene tabData y tabFilters
        #self.dataLayout.setContentsMargins(0, 0, 0, 0)
        #self.dataLayout.setSizeConstraint(0)
        self.tabData = QtWidgets.QFrame()  # contiene data
        self.tabData.setSizePolicy(sizePolicyGB)
        


        self.tabFilter.setSizePolicy(sizePolicyGB)
        

        self.tabDataLayout = QtWidgets.QVBoxLayout()
        
        filterL = QtWidgets.QVBoxLayout()
        self.tabData.setLayout(self.tabDataLayout)
        
        #Fix para acercar el lineEdit con el fltable
        #self.tabData.setContentsMargins(0, 0, 0, 0)
        #self.tabFilter.setContentsMargins(0, 0, 0, 0)
        #self.tabDataLayout.setContentsMargins(0, 0, 0, 0)
        #filterL.setContentsMargins(0, 0, 0, 0)
        
        self.tabFilter.setLayout(filterL)

        # Contiene botones lateral (datos, filtros, odf)
        self.buttonsLayout = QtWidgets.QVBoxLayout()
        self.masterLayout = QtWidgets.QVBoxLayout()  # Contiene todos los layouts

        self.pbData = QtWidgets.QPushButton(self)
        self.pbData.setSizePolicy(sizePolicy)
        self.pbData.setMinimumSize(self.iconSize)
        self.pbData.setFocusPolicy(QtCore.Qt.NoFocus)
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
        self.pbFilter.setFocusPolicy(QtCore.Qt.NoFocus)
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
        self.pbOdf.setFocusPolicy(QtCore.Qt.NoFocus)
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
        self.pbClean.setFocusPolicy(QtCore.Qt.NoFocus)
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

        from pineboolib.pncontrolsfactory import QComboBox
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
        

        self.tabControlLayout.addWidget(label1)
        self.tabControlLayout.addWidget(self.lineEditSearch)
        self.tabControlLayout.addWidget(label2)
        self.tabControlLayout.addWidget(self.comboBoxFieldToSearch)
        self.tabControlLayout.addWidget(self.comboBoxFieldToSearch2)

        self.masterLayout.addLayout(self.tabControlLayout)
        self.masterLayout.addLayout(self.dataLayout)
        self.setLayout(self.masterLayout)

        # Se añade data, filtros y botonera
        self.dataLayout.addWidget(self.tabData)
        self.dataLayout.addWidget(self.tabFilter)
        self.tabFilter.hide()
        self.dataLayout.addLayout(self.buttonsLayout)
        self.comboBoxFieldToSearch.currentIndexChanged.connect(self.putFirstCol)
        self.comboBoxFieldToSearch2.currentIndexChanged.connect(self.putSecondCol)

        from pineboolib.pncontrolsfactory import QTable
        self.tdbFilter = QTable()
        filterL.addWidget(self.tdbFilter)

    """
    Obtiene el componente tabla de registros
    """

    def tableRecords(self):
        if not self.tableRecords_:
            self.tableRecords_ = FLDataTable(self.tabData, "tableRecords")
            self.tableRecords_.setFocusPolicy(QtCore.Qt.StrongFocus)
            self.setFocusProxy(self.tableRecords_)
            self.tabDataLayout.addWidget(self.tableRecords_)
            self.setTabOrder(self.tableRecords_, self.lineEditSearch)
            self.setTabOrder(self.lineEditSearch, self.comboBoxFieldToSearch)
            self.setTabOrder(self.comboBoxFieldToSearch, self.comboBoxFieldToSearch2)
            self.lineEditSearch.installEventFilter(self)
            self.tableRecords_.installEventFilter(self)
            if self.autoSortColumn_:
                self.tableRecords_.header().sectionClicked.connect(self.switchSortOrder)

        t_cursor = self.tableRecords_.cursor()
        if self.cursor_ and self.cursor_ is not t_cursor and self.cursor_.metadata() and (not t_cursor or (t_cursor and t_cursor.metadata() and t_cursor.metadata().name() != self.cursor_.metadata().name())):
            self.setTableRecordsCursor()

        return self.tableRecords_

    """
    Asigna el cursor actual del componente a la tabla de registros
    """

    def setTableRecordsCursor(self):

        if not self.tableRecords_:
            self.tableRecords_ = FLDataTable(self.tabData, "tableRecords")
            self.tableRecords_.setFocusPolicy(QtCore.Qt.StrongFocus)
            self.setFocusProxy(self.tableRecords_)
            self.tabDataLayout.addWidget(self.tableRecords_)
            self.setTabOrder(self.tableRecords_, self.lineEditSearch)
            self.setTabOrder(self.lineEditSearch, self.comboBoxFieldToSearch)
            self.setTabOrder(self.comboBoxFieldToSearch, self.comboBoxFieldToSearch2)
            self.lineEditSearch.installEventFilter(self)
            self.tableRecords_.installEventFilter(self)

        if self.checkColumnEnabled_:
            try:
                self.tableRecords_.clicked.disconnect(self.tableRecords_.setChecked)
            except:
                pass
            self.tableRecords_.clicked.connect(self.tableRecords_.setChecked)

        t_cursor = self.tableRecords_.cursor()
        if t_cursor is not self.cursor_:
            self.tableRecords_.setFLSqlCursor(self.cursor_)
            if t_cursor:
                self.tableRecords_.recordChoosed.disconnect(self.recordChoosedSlot)
                t_cursor.newBuffer.disconnect(self.currentChangedSlot)
            
            self.tableRecords_.recordChoosed.connect(self.recordChoosedSlot)
            self.cursor_.newBuffer.connect(self.currentChangedSlot)

    @QtCore.pyqtSlot()
    def recordChoosedSlot(self):
        if isinstance(self.topWidget, FLFormSearchDB) and self.topWidget.inExec_:
            self.topWidget.accept()
        else:
            self.cursor().chooseRecord()

    @QtCore.pyqtSlot()
    def currentChangedSlot(self):
        self.currentChanged.emit()
    
    def currentRow(self):
        return self.cursor().at()
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

                if field is None:
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
                from pineboolib.pncontrolsfactory import QComboBox
                cond = QComboBox()
                if not type == "pixmap":
                    condList = [util.tr("Todos"), util.tr("Igual a Valor"), util.tr(
                        "Distinto de Valor"), util.tr("Vacío"), util.tr("No Vacío")]
                    if not type == "bool":
                        condList = [
                            util.tr("Todos"), util.tr("Igual a Valor"), util.tr("Distinto de Valor"), util.tr("Vacío"),
                            util.tr("No Vacío"), util.tr("Contiene Valor"), util.tr(
                                "Empieza por Valor"), util.tr("Acaba por Valor"),
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
                            editor_ = pineboolib.pncontrolsfactory.FLLineEdit(self)

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
                                            editor_.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(rX), editor_))

                                    editor_.setAlignment(Qt.AlignLeft)

                    if type == "serial":
                        editor_ = pineboolib.pncontrolsfactory.FLSpinBox()
                        editor_.setMaxValue(pow(10, partInteger) - 1)

                    if type == "pixmap":
                        self.tdbFilter.setRowReadOnly(i, True)

                    if type == "date":
                        editor_ = pineboolib.pncontrolsfactory.FLDateEdit(self, _label)
                        # editor_.setOrder(FLDateEdit.DMY) # FIXME
                        editor_.setAutoAdvance(True)
                        editor_.setSeparator("-")
                        da = QtCore.QDate()
                        editor_.setDate(da.currentDate())

                    if type == "time":
                        editor_ = pineboolib.pncontrolsfactory.FLTimeEdit(self)
                        timeNow = QtCore.QTime.currentTime()
                        editor_.setTime(timeNow)

                    if type in (FLFieldMetaData.Unlock, "bool"):
                        editor_ = pineboolib.pncontrolsfactory.FLCheckBox(self)

                    if editor_:
                        self.tdbFilter.setCellWidget(_linea, j, editor_)

                    j += 1

                i += 1
                _linea += 1

        k = 0

        while k < 5:
            self.tdbFilter.adjustColumn(k)
            k += 1

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
        if not self.topWidget:
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
            if field is None:
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
                    editorOp1 = pineboolib.pncontrolsfactory.FLSpinBox(self.tdbFilter.cellWidget(i, 2))
                    arg2 = editorOp1.value()

            if type == "date":
                util = FLUtil()
                if condType == self.FromTo:
                    editorOp1 = self.tdbFilter.cellWidget(i, 3)
                    editorOp2 = self.tdbFilter.cellWidget(i, 4)
                    arg2 = self.cursor_.db().manager().formatValue(
                        type, util.dateDMAtoAMD(editorOp1.date))
                    arg4 = self.cursor_.db().manager().formatValue(
                        type, util.dateDMAtoAMD(editorOp2.date))
                else:
                    editorOp1 = self.tdbFilter.cellWidget(i, 2)
                    arg2 = self.cursor_.db().manager().formatValue(
                        type, util.dateDMAtoAMD(editorOp1.date))

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
    filter_ = ""

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
                if fieldCheck is None:
                    self.fieldNameCheckColumn_ = "%s_check_column" % tMD.name()

                    if self.fieldNameCheckColumn_ not in tMD.fieldsNames():
                        fieldCheck = FLFieldMetaData(self.fieldNameCheckColumn_, self.tr(self.aliasCheckColumn_), True, False, FLFieldMetaData.Check,
                                                     0, False, True, True, 0, 0, False, False, False, None, False, None, True, False, False)
                        tMD.addFieldMD(fieldCheck)
                    else:
                        fieldCheck = tMD.field(self.fieldNameCheckColumn_)

                self.tableRecords().cursor().model().updateColumnsCount()
                self.tableRecords().header().reset()
                self.tableRecords().header().swapSections(self.tableRecords().column_name_to_column_index(fieldCheck.name()), self.sortColumn_)
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
        
        self.tableRecords_.setFunctionGetColor(self.functionGetColor())

        if refreshHead:
            if not self.tableRecords().header().isHidden():
                self.tableRecords().header().hide()

            model = self.cursor_.model()
            for column in range(model.columnCount()):
                field = model.metadata().indexFieldObject(column)
                if not field.visibleGrid() or (field.type() is "check" and not self.checkColumnEnabled_):
                    self.tableRecords_.setColumnHidden(column, True)
                else:
                    self.tableRecords_.setColumnHidden(column, False)
                    

            if self.autoSortColumn_:
                s = []
                field_1 = self.tableRecords_.visual_index_to_field(self.sortColumn_)
                field_2 = self.tableRecords_.visual_index_to_field(self.sortColumn2_)
                field_3 = self.tableRecords_.visual_index_to_field(self.sortColumn3_)
                
                if field_1 is not None:
                    s.append(field_1.name() + " ASC" if self.orderAsc_ else " DESC")
                if field_2 is not None:
                    s.append(field_2.name() + " ASC" if self.orderAsc2_ else " DESC")
                if field_3 is not None:
                    s.append(field_3.name() + " ASC" if self.orderAsc3_ else " DESC")

                id_mod = self.cursor_.db().managerModules().idModuleOfFile("%s.mtd" % self.cursor_.metadata().name())
                function_qsa = "%s.tabeDB_setSort_%s" % (id_mod, self.cursor_.metadata().name())

                vars = []
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
                    
                from pineboolib.pncontrolsfactory import aqApp
                ret = aqApp.call(function_qsa, vars, None, False)
                if not isinstance(ret, bool):
                    s = ret
                    logger.debug("functionQSA: %s %s" % (function_qsa, ret.join(", ")))
                else:
                    logger.debug("functionQSA: %s -> NULL" % (function_qsa))

                self.tableRecords_.setSort(s)

            if model:
                try:
                    self.comboBoxFieldToSearch.currentIndexChanged.disconnect(self.putFirstCol)
                    self.comboBoxFieldToSearch2.currentIndexChanged.disconnect(self.putSecondCol)
                except Exception:
                    logger.error("Se ha producido un problema al desconectar")
                    return

                self.comboBoxFieldToSearch.clear()
                self.comboBoxFieldToSearch2.clear()

                cb1 = None
                cb2 = None
                for column in range(model.columnCount()):
                    visual_column = self.tableRecords_.header().logicalIndex(column)
                    if visual_column is not None:
                        field = model.metadata().indexFieldObject(visual_column)
                        if not field.visibleGrid():
                            continue
                        #    self.tableRecords_.setColumnHidden(column, True)
                        # else:
                        self.comboBoxFieldToSearch.addItem(model.headerData(visual_column, QtCore.Qt.Horizontal, QtCore.Qt.DisplayRole))
                        self.comboBoxFieldToSearch2.addItem(model.headerData(visual_column, QtCore.Qt.Horizontal, QtCore.Qt.DisplayRole))

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
                    finalFilter = "%s AND %s" % (
                        finalFilter, self.tdbFilterLastWhere_)
            
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
        
        QtCore.QTimer.singleShot(50, self.setSortOrder)

    """
    Actualiza el conjunto de registros con un retraso.

    Acepta un lapsus de tiempo en milisegundos, activando el cronómetro interno para
    que realize el refresh definitivo al cumplirse dicho lapsus.

    @param msec Cantidad de tiempo del lapsus, en milisegundos.
    """

    def refreshDelayed(self, msec=50, refreshData=True):
        
        self._refreshData = True if refreshData else False
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

        if w and (not self.cursor_ or self.reqReadOnly_ or self.reqEditOnly_ or self.reqOnlyTable_ or relationLock):
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
        if isinstance(w, FLDataTable):
            w = None
        if w and (not self.cursor_ or self.reqReadOnly_ or self.reqEditOnly_ or self.reqOnlyTable_ or (self.cursor_.cursorRelation() and self.cursor_.cursorRelation().isLocked())):
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
        if isinstance(w, FLDataTable):
            w = None
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
        if isinstance(w, FLDataTable):
            w = None
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
        if isinstance(w, FLDataTable):
            w = None
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
    def putFirstCol(self, col):
        _index = self.tableRecords_.column_name_to_column_index(col) if isinstance(col, str) else self.tableRecords_.visual_index_to_column_index(col)

            
        if _index is None or _index < 0:
            return False
        self.moveCol(_index, self.sortColumn_)
        self.tableRecords_.sortByColumn(
            self.sortColumn_, QtCore.Qt.AscendingOrder if self.orderAsc_ else QtCore.Qt.DescendingOrder)

        return True

    """
    Coloca la columna como segunda pasando el nombre del campo.

    @author Silix - dpinelo
    """
    @QtCore.pyqtSlot(int)
    @QtCore.pyqtSlot(str)
    def putSecondCol(self, col):
        _index = self.tableRecords_.column_name_to_column_index(col) if isinstance(col, str) else self.tableRecords_.visual_index_to_column_index(col)

        if _index is None or _index < 0:
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
                self.comboBoxFieldToSearch.currentIndexChanged.disconnect(self.putFirstCol)
            except Exception:
                logger.error("Se ha producido un problema al desconectar")
                return

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

        if to == 1:  # Si es la segunda columna ...
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
            textSearch = self.cursor_.valueBuffer(field.name())

        self.refresh(True)

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
            QtCore.QTimer.singleShot(
                0, self.tableRecords_.ensureRowSelectedVisible)
        else:
            self.refreshDelayed()

        self.tableRecords_.header().swapSections(from_, to)

        self.refresh(True, False)

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
    def setColumnWidth(self, field, w):
        if self.tableRecords_:
            col = self.tableRecords_.column_name_to_column_index(field) if isinstance(field, str) else field
            
            self.tableRecords_.setColumnWidth(col, w)
                
            


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

    def exportToOds(self):
        if not self.cursor_:
            return
        
        cursor = FLSqlCursor(self.cursor_.curName())
        cursor.select(self.cursor_.filter())

        from pineboolib.pncontrolsfactory import aqApp, QMessageBox
        settings = FLSettings()
        if settings.readBoolEntry("ebcomportamiento/FLTableExport2Calc", False):
            QMessageBox.information(self.topWidget, self.tr("Opción deshabilitada"), self.tr(
                "Esta opción ha sido deshabilitada por el administrador"), QtWidgets.QMessageBox.Ok)
            return

        mtd = cursor.metadata()
        if not mtd:
            return

        tdb = self.tableRecords()
        if not hasattr(tdb, "cursor"):
            return

        from pineboolib.pncontrolsfactory import AQOdsGenerator, AQOdsSpreadSheet, AQOdsSheet, AQOdsRow, AQOdsColor, AQOdsStyle
        hor_header = tdb.horizontalHeader()
        title_style = [AQOdsStyle.Align_center, AQOdsStyle.Text_bold]
        border_bot = AQOdsStyle.Border_bottom
        border_right = AQOdsStyle.Border_right
        border_left = AQOdsStyle.Border_left
        italic = AQOdsStyle.Text_italic
        ods_gen = AQOdsGenerator
        spread_sheet = AQOdsSpreadSheet(ods_gen)
        sheet = AQOdsSheet(spread_sheet, mtd.alias())
        tdb_num_rows = cursor.size()
        tdb_num_cols = len(mtd.fieldsNames())
        
        util = FLUtil()

        pd = util.createProgressDialog("Procesando", tdb_num_rows)
        util.setProgress(1)
        row = AQOdsRow(sheet)
        row.addBgColor(AQOdsColor(0xe7e7e7))
        for i in range(tdb_num_cols):
            field = mtd.indexFieldObject(tdb.visual_index_to_logical_index(i))
            if field is not None and field.visibleGrid():
                row.opIn(title_style)
                row.opIn(border_bot)
                row.opIn(border_left)
                row.opIn(border_right)
                row.opIn(field.alias())

        row.close()

        #cur = tdb.cursor()
        #cur_row = tdb.currentRow()

        cursor.first()

        for r in range(tdb_num_rows):
            if pd.wasCanceled():
                break

            row = AQOdsRow(sheet)
            for c in range(tdb_num_cols):
                #idx = tdb.indexOf(c)  # Busca si la columna se ve
                #if idx == -1:
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
                                val = val[0:val.find("T")]
                                
                            row.opIn(val)
                        else:
                            row.coveredCell()
                            
                        
                            

                    elif field.type() in ["bool", "unlock"]:
                        str_ = self.tr("Sí") if val == True else self.tr("No")
                        row.opIn(italic)
                        row.opIn(str_)

                    else:
                        str_ = val
                        if str_ is not None:
                            cs = None
                            if isinstance(str_, list):
                                cs = ",".join(str_)
                            elif str(str_).startswith("RK@"):
                                cs = cursor.fetchLargeValue(str_)

                            if cs is not None:
                                pix = QPixmap(cs)

                                if not pix.isNull():
                                    
                                    pix_name = "pix%s_" % pix.serialNumber()
                                    pix_file_name = "%s/%s.png" % (aqApp.tmp_dir(), pix_name,
                                                               QtCore.QDateTime.currentDateTime().toString("ddMMyyyyhhmmsszzz"))
                                    pix.save(pix_file_name, "PNG")
                                    #print("Metiendo imagen")
                                    row.opIn(AQOdsImage(pix_name, double((pix.width() * 2.54) / 98) * 1000,
                                                        double((pix.height() * 2.54) / 98) * 1000, 0, 0, pix_file_name))
                                else:
                                    row.coveredCell()
                            else:
                                row.opIn(str(str_))
                        else:
                            row.coveredCell()
            row.close()
            if not r % 4:
                util.setProgress(r)
            cursor.next()

        #cur.seek(cur_row)
        sheet.close()
        spread_sheet.close()
        
        util.setProgress(tdb_num_rows)
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        file_name = "%s/%s%s.ods" % (aqApp.tmp_dir(), mtd.name(), QtCore.QDateTime.currentDateTime().toString("ddMMyyyyhhmmsszzz"))
        ods_gen.generateOds(file_name)
        
        aqApp.call("sys.openUrl", [file_name], None)

        QtWidgets.QApplication.restoreOverrideCursor()
        util.destroyProgressDialog()

    """
    Conmuta el sentido de la ordenación de los registros de la tabla, de ascendente a descendente y
    viceversa. Los registros siempre se ordenan por la primera columna.
    Si la propiedad autoSortColumn es TRUE.
    """

    def switchSortOrder(self, col=0):
        if not self.autoSortColumn_:
            return
        if self.tableRecords_.logical_index_to_visual_index(col) == self.tableRecords_.visual_index_to_column_index(self.sortColumn_): 
        
            self.orderAsc_ = not self.orderAsc_

        self.setSortOrder(self.orderAsc_,  col)

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

        #if p:
        #    p = "%s%%" % p

        refreshData = False
        # if p.endswith("%"): refreshData = True

        msec_refresh = 400
        column = self.tableRecords_.header().logicalIndex(self.sortColumn_)
        field = self.cursor_.model().metadata().indexFieldObject(column)
        bFilter = self.cursor_.db().manager().formatAssignValueLike(field, p, True)

        idMod = self.cursor_.db().managerModules().idModuleOfFile(self.cursor_.metadata().name() + ".mtd")
        functionQSA = idMod + ".tableDB_filterRecords_" + self.cursor_.metadata().name()

        vargs = []
        vargs.append(self.cursor_.metadata().name())
        vargs.append(p)
        vargs.append(field.name())
        vargs.append(bFilter)

        if functionQSA:
            msec_refresh = 200
            ret = None
            try:
                from pineboolib.pncontrolsfactory import aqApp
                ret = aqApp.call(functionQSA, vargs, None, False)
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
        self.filter_ = bFilter

    def setSortOrder(self, ascending=True, col_order = None):
        order = Qt.AscendingOrder if ascending else Qt.DescendingOrder
        col = self.sortColumn_
        while True:
            column = self.tableRecords_.header().logicalIndex(col)
            if not self.tableRecords_.isColumnHidden(column):
                break
            col += 1
        self.tableRecords_.sortByColumn(column, order)

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

    def primarysKeysChecked(self):
        return self.tableRecords().primarysKeysChecked()

    def clearChecked(self):
        self.tableRecords().clearChecked()

    def setPrimaryKeyChecked(self, name, b):
        name = str(name)
        self.tableRecords().setPrimaryKeyChecked(name, b)
