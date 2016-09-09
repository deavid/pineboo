# -*- coding: utf-8 -*-

from PyQt4 import QtCore,QtGui

from pineboolib import decorators
from pineboolib.fllegacy.FLSqlCursor import FLSqlCursor
from pineboolib.utils import DefFun

class FLTableDB(QtGui.QWidget):
    _tableView = None
    _vlayout = None
    _lineEdit = None
    _comboBox_1 = None
    _comboBox_2 = None
    _topWidget = None
    _cursor = None
    _loaded = False
    _cursorLoaded = False

    _tableName = None
    _foreignField = None
    _fieldRelation = None
    _action = None
    _foreignFilter = None

    def __init__(self, parent = None, action_or_cursor = None, *args):
        #print("FLTableDB:", parent, action_or_cursor , args)
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
            self._action = action_or_cursor
        else:
            self._cursor = None
        if self._cursor:
            self._tableView._h_header.setResizeMode(QtGui.QHeaderView.ResizeToContents)
            self._tableView.setModel(self._cursor.model())
            self._tableView.setSelectionModel(self._cursor.selection())
        self.tableRecords = self # control de tabla interno

        #Carga de comboBoxs y connects .- posiblemente a mejorar
        if self._cursor:
            i = 0
            for column in range(self._cursor.model().columnCount()):
                #print("Columna ", i)
                self._comboBox_1.addItem(self._cursor.model().headerData(column, QtCore.Qt.Horizontal, QtCore.Qt.DisplayRole))
                self._comboBox_2.addItem(self._cursor.model().headerData(column, QtCore.Qt.Horizontal, QtCore.Qt.DisplayRole))
        self._comboBox_1.addItem("*")
        self._comboBox_2.addItem("*")
        self._comboBox_1.setCurrentIndex(0)
        self._comboBox_2.setCurrentIndex(1)
        self._comboBox_1.currentIndexChanged.connect(self.comboBox_putFirstCol)
        self._comboBox_2.currentIndexChanged.connect(self.comboBox_putSecondCol)        

        self.sort = []
        self.timer_1 = QtCore.QTimer(self)
        self.timer_1.singleShot(100, self.loaded)
        self._topWidget = parent

    def __getattr__(self, name): return DefFun(self, name)

    def loaded(self):
        # Es necesario pasar a modo interactivo lo antes posible
        # Sino, creamos un bug en el cierre de ventana: se recarga toda la tabla para saber el tamaño
        #print("FLTableDB(%s): setting columns in interactive mode" % self._tableName)
        self._tableView._h_header.setResizeMode(QtGui.QHeaderView.Interactive)
        self._loaded = True
        while True: #Ahora podemos buscar el cursor ... porque ya estamos añadidos al formulario
            parent_cursor = getattr(self._parent,"_cursor", None)
            if parent_cursor: break
            new_parent = self._parent.parentWidget()
            if new_parent is None: break
            self._parent = new_parent
        self.initCursor()

    def cursor(self):   
        if not self._cursorLoaded:
            self.timer_cursor = QtCore.QTimer(self)
            self.timer_cursor.singleShot(100, self.cursor)
        else:
            if not self._cursor:
                self._cursor = None
                print("WARN: FLTableDB.cursor(): Cursor Inválido a", self._tableName)
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
        for column in range(self._cursor.model().columnCount()):
            if self._cursor.model().headerData(column, QtCore.Qt.Horizontal, QtCore.Qt.DisplayRole).lower() == fN.lower():
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
        if self._cursor is None:
            return
        _oldPos= None
        _oldSecond = self._tableView._h_header.logicalIndex(1)
        for column in range(self._cursor.model().columnCount()):
            if self._cursor.model().headerData(column, QtCore.Qt.Horizontal, QtCore.Qt.DisplayRole).lower() == fN.lower():
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
        self.initCursor()
        return True
    
    def tableName(self):
        return self._tableName
    
    def foreignField(self):
        return self._foreignField
    
    def fieldRelation(self):
        return self._fieldRelation


    def setForeignField(self, foreignField):
        self._foreignField = foreignField
        self.initCursor()
        return True


    def setFieldRelation(self, fieldRelation):
        self._fieldRelation = fieldRelation
        self.initCursor()
        return True
    
    def setActionName(self, action):
        self._action = action


    def showAlias(self, b):
        self._showAlias = b




    def initCursor(self):
        filtro = None
        self._cursorLoaded = True
        if not self._foreignField:
            return
        if not self._fieldRelation:
            return
        if not self._tableName:
            return
        
        if self._loaded:   

            tipo = self._cursor.model().fieldType(self._fieldRelation)
            foranea = self._parent.parentWidget().cursor().valueBuffer(self._foreignField)
            if foranea is None:
                #print("FLTable(%s): campo foraneo \"%s.%s\" no encontrado." % (self._tableName,self._parent.parentWidget()._cursor.table(), self._foreignField))
                return
            if tipo is "uint":
                self._foreignFilter = "%s = %s" % (self._fieldRelation, self._parent.parentWidget().cursor().valueBuffer(self._foreignField))
            else:
                self._foreignFilter = "%s = '%s'"  % (self._fieldRelation, self._parent.parentWidget().cursor().valueBuffer(self._foreignField))
            
            #print("Filtro:%s" % filtro)
            self._cursor.setMainFilter(self._foreignFilter)
            self._cursor.refresh()
        else:
            self._cursor = FLSqlCursor(self._tableName)
        
        
            
            

            #self._cursor.setMainFilter("%s = ")

    @QtCore.pyqtSlot()
    def close(self):
        print("FLTableDB: close()")

    @QtCore.pyqtSlot()
    def refresh(self):
        print("FLTableDB: refresh()", self.parent().parent().parent())
        self._cursor.setMainFilter(self._foreignFilter)

    @QtCore.pyqtSlot()
    def show(self):
        print("FLTableDB: show event")
        #super(FLTableDB, self).show()
        
        if self._cursor:
            self._tableView._h_header.setResizeMode(QtGui.QHeaderView.ResizeToContents)
            self._tableView.setModel(self._cursor.model())
            self._tableView.setSelectionModel(self._cursor.selection())
        self.tableRecords = self # control de tabla interno

        #Carga de comboBoxs y connects .- posiblemente a mejorar
        if self._cursor:
            for column in range(self._cursor.model().columnCount()):
                
                self._comboBox_1.addItem(self._cursor.model().headerData(column, QtCore.Qt.Horizontal, QtCore.Qt.DisplayRole))
                self._comboBox_2.addItem(self._cursor.model().headerData(column, QtCore.Qt.Horizontal, QtCore.Qt.DisplayRole))
        self._comboBox_1.addItem("*")
        self._comboBox_2.addItem("*")
        self._comboBox_1.setCurrentIndex(0)
        self._comboBox_2.setCurrentIndex(1)
        self._comboBox_1.currentIndexChanged.connect(self.comboBox_putFirstCol)
        self._comboBox_2.currentIndexChanged.connect(self.comboBox_putSecondCol)        

        self.sort = []
        self.timer_1 = QtCore.QTimer(self)
        self.timer_1.singleShot(100, self.loaded)
        

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
    
    @decorators.WorkingOnThis
    def setEditOnly(self, value):
        return True
    
    @decorators.WorkingOnThis
    def setReadOnly(self, value):
        return True
        
