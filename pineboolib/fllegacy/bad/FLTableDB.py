# -*- coding: utf-8 -*-

from PyQt4 import QtCore,QtGui

from pineboolib import decorators
from pineboolib.fllegacy.FLSqlCursor import FLSqlCursor
from pineboolib.utils import DefFun
from pineboolib.fllegacy.FLRelationMetaData import FLRelationMetaData
from pineboolib.fllegacy.FLFieldMetaData import FLFieldMetaData
from pineboolib.fllegacy.FLTableMetaData import FLTableMetaData

class FLTableDB(QtGui.QWidget):
    _tableView = None
    _vlayout = None
    _lineEdit = None
    _comboBox_1 = None
    _comboBox_2 = None
    topWidget = QtGui.QWidget
    showed = False

    def __init__(self, parent = None, action_or_cursor = None, *args):
        print("FLTableDB:", parent, action_or_cursor , args)
        # TODO: Falta el lineeditsearch y el combo, que los QS lo piden
        super(FLTableDB,self).__init__(parent,*args)
        # TODO: LA inicialización final hay que hacerla más tarde, en el primer
        # show(), porque sino obligas a tenerlo todo preparado en el constructor.
        self._tableView = QtGui.QTableView()
        self._lineEdit = QtGui.QLineEdit()
        _label1 = QtGui.QLabel()
        _label2 = QtGui.QLabel()
        self._comboBox_1 = QtGui.QComboBox()
        self._comboBox_2 = QtGui.QComboBox()
        _label1.setText("Buscar")
        _label2.setText("en")
        self._vlayout = QtGui.QVBoxLayout()
        _hlayout =  QtGui.QHBoxLayout()
        self._tableView._v_header = self._tableView.verticalHeader()
        self._tableView._v_header.setDefaultSectionSize(18)
        self._tableView._h_header = self._tableView.horizontalHeader()
        self._tableView._h_header.setDefaultSectionSize(70)
        _hlayout.addWidget(_label1)
        _hlayout.addWidget(self._lineEdit)
        _hlayout.addWidget(_label2)
        _hlayout.addWidget(self._comboBox_1)
        _hlayout.addWidget(self._comboBox_2)
        self._vlayout.addLayout(_hlayout)
        self._vlayout.addWidget(self._tableView)
        self.setLayout(self._vlayout)
        self._parent = parent
        while True:
            parent_cursor = getattr(self._parent,"_cursor", None)
            if parent_cursor: break
            new_parent = self._parent.parentWidget()
            if new_parent is None: break
            self._parent = new_parent
            print(self._parent)

        self._tableView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self._tableView.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self._tableView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self._tableView.setAlternatingRowColors(True)

        if action_or_cursor is None and parent_cursor:
            action_or_cursor = parent_cursor
        if isinstance(action_or_cursor,FLSqlCursor):
            self._cursor = action_or_cursor
        elif isinstance(action_or_cursor,str):
            self._cursor = FLSqlCursor(action_or_cursor)
        else:
            self._cursor = None
        if self._cursor:
            self._tableView._h_header.setResizeMode(QtGui.QHeaderView.ResizeToContents)
            self._tableView.setModel(self._cursor._model)
            self._tableView.setSelectionModel(self._cursor.selection())
        self.tableRecords = self # control de tabla interno

        #Carga de comboBoxs y connects .- posiblemente a mejorar
        if self._cursor:
            for column in range(self._cursor._model.columnCount()):
                self._comboBox_1.addItem(self._cursor._model.headerData(column, QtCore.Qt.Horizontal, QtCore.Qt.DisplayRole))
                self._comboBox_2.addItem(self._cursor._model.headerData(column, QtCore.Qt.Horizontal, QtCore.Qt.DisplayRole))
        self._comboBox_1.addItem("*")
        self._comboBox_2.addItem("*")
        self._comboBox_1.setCurrentIndex(0)
        self._comboBox_2.setCurrentIndex(1)
        self._comboBox_1.currentIndexChanged.connect(self.comboBox_putFirstCol)
        self._comboBox_2.currentIndexChanged.connect(self.comboBox_putSecondCol)        

        self.sort = []
        self.timer_1 = QtCore.QTimer(self)
        self.timer_1.singleShot(100, self.loaded)

    def __getattr__(self, name): return DefFun(self, name)

    def loaded(self):
        # Es necesario pasar a modo interactivo lo antes posible
        # Sino, creamos un bug en el cierre de ventana: se recarga toda la tabla para saber el tamaño
        print("FLTableDB: setting columns in interactive mode")
        self._tableView._h_header.setResizeMode(QtGui.QHeaderView.Interactive)

    def cursor(self):
        assert self._cursor
        return self._cursor

    def obj(self):
        return self

    def comboBox_putFirstCol(self):
        self.putFirstCol(str(self._comboBox_1.currentText()))

    def comboBox_putSecondCol(self):
        self.putSecondCol(str(self._comboBox_2.currentText()))

    def putFirstCol(self, fN):
        _oldPos= None
        _oldFirst = self._tableView._h_header.logicalIndex(0)    
        for column in range(self._cursor._model.columnCount()):
            if self._cursor._model.headerData(column, QtCore.Qt.Horizontal, QtCore.Qt.DisplayRole).lower() == fN.lower():
                _oldPos = self._tableView._h_header.visualIndex(column) 
                if not self._comboBox_1.currentText() == fN:
                    self._comboBox_1.setCurrentIndex(column)
                    return False
                break

        if not _oldPos or fN == "*":
            return False
        else:         
            self._tableView._h_header.swapSections(_oldPos, 0)
            self._comboBox_2.setCurrentIndex(_oldFirst)
            return True

    def putSecondCol(self, fN):
        _oldPos= None
        _oldSecond = self._tableView._h_header.logicalIndex(1)
        for column in range(self._cursor._model.columnCount()):
            if self._cursor._model.headerData(column, QtCore.Qt.Horizontal, QtCore.Qt.DisplayRole).lower() == fN.lower():
                _oldPos = self._tableView._h_header.visualIndex(column)
                break

        if not _oldPos or fN == "*":
            return False
        if not self._comboBox_1.currentText() == fN:           
            self._tableView._h_header.swapSections(_oldPos, 1)
        else:
            self._comboBox_1.setCurrentIndex(_oldSecond)
        return True


    def setTableName(self, tableName):
        self._tableName = tableName
        if self.showed:
            if self.topWidget:
                self.initCursor()
            else:
                self.initFakeEditor()


    def setForeignField(self, foreingField):
        self._foreingField = foreingField
        if self.showed:
            if self.topWidget:
                self.initCursor()
            else:
                self.initFakeEditor()



    def setFieldRelation(self, fieldRelation):
        self._fieldRelation = fieldRelation
        if self.showed:
            if self.topWidget:
                self.initCursor()
            else:
                self.initFakeEditor()







    @decorators.NotImplementedWarn
    def initCursor(self):
        # si no existe crea la tabla
        if not self._cursor: return False
        if not self._cursor._model: return False

        self._tMD = 0

        if not self._sortField: self._tMD = self._cursor._model.name()
        if self._tMD:
            self.sortField_ = self._tMD.value(self._cursor._currentregister, self._tMD.primaryKey())
        ownTMD = False
        if not self._tableName:
            #if not cursor_->db()->manager()->existsTable(tableName_)) {
            ownTMD = True
            #tMD = cursor_->db()->manager()->createTable(tableName_);
        else:
            ownTMD = True
            self._tMD = self._cursor._model._table.name

        if not self._tMD:
            return

        if not self._foreignField or not self._fieldRelation:
            if not self._cursor._model:
                if ownTMD and self._tMD and not self._tMD.inCache():
                    self._tMD = None
        
            return

            if not self._cursor._model.name() == self._tableName:
                ctxt = self._cursor.context();
                self._cursor = FLSqlCursor(self._tableName)
                if self._cursor:
                    self._cursor.setContext(ctxt)
                    cursorAux = 0
        
                if ownTMD and self._tMD and not self._tMD.inCache():
                    self._tMD = None
        
                return
        
        else:
            cursorTopWidget = self.topWidget._cursor() # ::qt_cast<FLFormDB *>(topWidget)->cursor()
            if cursorTopWidget and not cursorTopWidget._model.name() == self._tableName:
                self._cursor = cursorTopWidget
    
  

        if not self._tableName or not self._foreignField or not self._fieldRelation or cursorAux:
            if ownTMD and self._tMD and not self._tMD.inCache():
                tMD = None
    
            return
  
        cursorAux = self._cursor
        curName = self._cursor._model.name()
        rMD = self._cursor._model.relation(self._foreignField,self._fieldRelation,self._tableName)
        testM1 = self._tMD.relation(self._fieldRelation, self._foreignField, curName)
        checkIntegrity = bool(False)

        if not rMD:
            if testM1:
                checkIntegrity = (testM1.cardinality() == FLRelationMetaData.RELATION_M1)
            fMD = FLTableMetaData(self._cursor._model.field(self._foreignField)) 
            if (fMD):
                tmdAux = self._cursor._model(self._tableName);
                if not tmdAux or tmdAux.isQuery():
                    checkIntegrity = False
                if tmdAux and not tmdAux.inCache(): # mirar inCache()
                    tmdAux = None
                rMD = FLRelationMetaData(self._tableName,self._fieldRelation, FLRelationMetaData.RELATION_1M, False, False, checkIntegrity)
                fMD.addRelationMD(rMD)
                print("FLTableDB : La relación entre la tabla del formulario %r y esta tabla %r de este campo no existe, pero sin embargo se han indicado los campos de relación( %r, %r )" % (curName, self._tableName, self._fieldRelation, self._foreignField))
                print("FLTableDB : Creando automáticamente %r.%r --1M--> %r.%r" %  (curName, self._foreignField, self._tableName, self._fieldRelation))

    
            else:
                print("FLTableDB : El campo ( %r ) indicado en la propiedad foreignField no se encuentra en la tabla ( %r )" % (self._foreignField, curName))
        rMD = testM1
        if not rMD:
            fMD = FLFieldMetaData(tMD.field(self._fieldRelation))
            if (fMD):
                rMD = FLRelationMetaData(curName,self._foreignField, FLRelationMetaData.RELATION_1M, False, False, False)
                fMD.addRelationMD(rMD)
                print("FLTableDB : Creando automáticamente %r.%r --1M--> %r.%r" % (self._tableName, self._fieldRelation, curName, self._foreignField))
            else:
                print("FLTableDB : El campo ( %r ) indicado en la propiedad fieldRelation no se encuentra en la tabla ( %r )" % (self._fieldRelation, self._tableName))

        self._cursor = FLSqlCursor(self._tableName, True, self._cursor.db().connectionName(), cursorAux, rMD, self);
        if not self._cursor:
            self._cursor = cursorAux
            cursorAux = 0
        else:
            self._cursor.setContext(cursorAux.context())
        if self.showed:
            self.disconnect(cursorAux, QtCore.SIGNAL('newBuffer()'), self.refresh())
            self.connect(cursorAux,QtCore.SIGNAL('newBuffer()'), self.refresh())
  

        if cursorAux and self.topWidget.isA("FLFormSearchDB"):
            self.topWidget.setCaption(self._cursor._model.alias())
            self.topWidget.setCursor(self._cursor) #::qt_cast<FLFormSearchDB *>(topWidget)->setCursor(cursor_);
  

        if ownTMD and tMD and not tMD.inCache():
            tMD = None


    @QtCore.pyqtSlot()
    def close(self):
        print("FLTableDB: close()")

    @QtCore.pyqtSlot()
    def refresh(self):
        print("FLTableDB: refresh()", self.parent().parent().parent())
        self._cursor.refresh()

    @QtCore.pyqtSlot()
    def show(self):
        print("FLTableDB: show event")
        super(FLTableDB, self).show()

    @QtCore.pyqtSlot()
    def insertRecord(self):
        self._cursor.insertRecord()

    @QtCore.pyqtSlot()
    def editRecord(self):
        self._cursor.editRecord()

    @QtCore.pyqtSlot()
    def deleteRecord(self):
        self._cursor.deleteRecord()

    @QtCore.pyqtSlot()
    def browseRecord(self):
        self._cursor.browseRecord()

    @QtCore.pyqtSlot()
    def copyRecord(self):
        self._cursor.copyRecord()
