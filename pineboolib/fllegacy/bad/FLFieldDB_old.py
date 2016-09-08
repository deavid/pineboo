# -*- coding: utf-8 -*-

from PyQt4 import QtCore,QtGui

from pineboolib import decorators
from pineboolib.fllegacy.FLSqlCursor import FLSqlCursor
from pineboolib.utils import DefFun



class FLFieldDB(QtGui.QWidget):
    _fieldName = "undefined"
    _label = None
    _dataControl = None 
    _layout = None
    _tableName = None
    _fieldAlias = None
    _loaded = False
    _topWidget = None
    _parent = None
    _cursor = None
    _tipo = None
    _fieldRelatio = None
    _foreignField = None
    _editable = True
    
    

    def __init__(self, parent, *args):
        super(FLFieldDB,self).__init__(parent,*args)
        #TODO: Detectar el tipo de campo y añadir los controles adecuados, Por defecto todos son campos de texto
        self._lineEdit = QtGui.QLineEdit()
        self._layout = QtGui.QHBoxLayout()
        self._label = QtGui.QLabel()
        spacer = QtGui.QSpacerItem(40,0,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Expanding)
        spacer2 = QtGui.QSpacerItem(0,30,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Expanding)
        self._layout.addItem(spacer)
        self._layout.addItem(spacer2)
        self._layout.addWidget(self._label)
        self._parent = parent
        self.setLayout(self._layout)
        self.timer_1 = QtCore.QTimer(self)
        self.timer_1.singleShot(100, self.loaded)
        self._tipo = None
        
        
    def loaded(self):
        #Asi damos tiempo a que el control se añada al formulario
        self._loaded = True
        value = None
        while True: #Ahora podemos buscar el cursor ... porque ya estamos añadidos al formulario
            parent_cursor = getattr(self._parent,"_cursor", None)
            if parent_cursor: 
                #print("FLFIeldDB(%s):Pariente %s con cursor encontrado" % (self._fieldAlias, self._parent))
                break
            new_parent = self._parent.parentWidget()
            if new_parent is None: 
                print("FLFIeldDB(%s):No se ha encontrado al padre con cursor" % self._fieldAlias)
                break
            self._parent = new_parent
            
        self._cursor = self._parent.parentWidget()._cursor
        if not self._cursor:
            self._cursor = self._parent._cursor
        #Si es un dato externo ...
        if not self._tableName is None and not self._tableName == "":
            self._editable = False
            cursorFr = FLSqlCursor(self._tableName)
            if not cursorFr._model is None and not isinstance(cursorFr._model, DefFun): #Para las tablas qye no existen
                #print("El tipo model es %s" % type(cursorFr._model))
                self._tipo = cursorFr._model.fieldType(self._fieldRelation)
                valueForeignField = self._cursor.valueBuffer(self._foreignField)
                if not valueForeignField is None and not valueForeignField == "":
                    if self._tipo == 'uint':
                        filtro = "%s = %s" % (self._fieldRelation, str(valueForeignField))
                    else:
                        filtro = "%s = '%s'" % (self._fieldRelation, str(valueForeignField))   
                    cursorFr.setMainFilter(filtro)
                    cursorFr.refresh()
                    cursorFr.first()
                    value = cursorFr.valueBuffer(self._fieldName)
                else:
                    value=""
            else:
                print("FLFieldDB: Campo %s.%s no encontrada." % (self._tableName, self._fieldName))
                value=""

        else:
            self._tableName =  self._cursor.table().name
            #print("Solicitando Alias de %s a tabla %s" % (self._fieldName, self._tableName))
            self.setFieldAlias(self._cursor._model.alias(self._fieldName))
            self._tipo = self._cursor._model.fieldType(self._fieldName)
            value = self._cursor.valueBuffer(self._fieldName)
        
        
        #print("\n\nCampo = %s.%s, Tipo = %s\nvalue = \"%s\"\nEditable = %s" % (self._tableName, self.fieldName, self._tipo, value, self._editable))
        if self._tipo == 'string' or self._tipo == 'uint' or self._tipo == 'double' or self._tipo == 'date' or self._tipo == 'serial':
            self._dataControl = QtGui.QLineEdit()
        elif self._tipo == 'bool':
            self._dataControl = QtGui.QCheckBox()
        elif self._tipo == 'stringlist':
            self._dataControl = QtGui.QLineEdit()
        else:
            print("FLFIeldDB(%s):Tipo de dato desconocido (%s) en %s.%s.¿Existe ese campo?" % (self._fieldAlias, self._tipo , self._tableName, self._fieldName ))
            self._dataControl = QtGui.QLineEdit()
        
        self._layout.addWidget(self._dataControl)
        
        if value:
            self.setValue(str(value))
        self.refresh() 
        
    
    def __getattr__(self, name): return DefFun(self, name)
            
    @property
    def fieldName(self):
        return self._fieldName

    @fieldName.setter
    def fieldName(self):
        return self._fieldName
        

    def setFieldName(self, fN):
        self._fieldName = fN
        self.refresh()
       
    @QtCore.pyqtSlot()
    def searchValue(self):
        print("FLFieldDB: searchValue()")
        return None

    @QtCore.pyqtSlot()
    def setMapValue(self):
        print("FLFieldDB: setMapValue()")
        return None        

    def setShowAlias(self, show):
        self._showAlias = bool(show)
        if not self._showAlias:
            self._label.setText("")

    
    def setTableName(self, tableName):
        self._tableName = tableName
        return True

    @decorators.NotImplementedWarn
    def setFilter(self, newFilter):
        self._filter = newFilter
        return True

    
    def setFieldAlias(self, fieldAlias):
        self._fieldAlias = fieldAlias
        return True


    def setForeignField(self, foreignField):
        self._foreignField = foreignField
        return True

    def setFieldRelation(self, fieldRelation):
        self._fieldRelation = fieldRelation
        return True



    def setShowEditor(self, show):
        self._showEditor = bool(show)
        self._lineEdit.setReadOnly(self._showEditor)
        return True
    
    def setValue(self, value):
        self._dataControl.setEnabled(self._editable)
        self._dataControl.setText(value)
        
    def refresh(self):
        if not self._fieldAlias is None:
            self._label.setText(self._fieldAlias)
        