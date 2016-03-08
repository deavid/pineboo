# -*- coding: utf-8 -*-

from PyQt4 import QtCore

from pineboolib.fllegacy.FLRelationMetaData import FLRelationMetaData
from pineboolib.fllegacy.FLTableMetaData import FLTableMetaData
from pineboolib import decorators



class FLFieldMetaData():
    """
  @param n Nombre del campo
  @param a Alias del campo, utilizado en etiquetas de los formularios
  @param aN TRUE si permite nulos (NULL), FALSE si los permite (NOT NULL)
  @param _isPrimaryKey TRUE si es clave primaria, FALSE si no es clave primaria, ser
        clave primaria implica ser Indice y Único
  @param t Tipo del campo
  @param l Longitud del campo en caracteres, siempre que se de tipo cadena
       de caracteres
  @param c Indica si el campo es calculado
  @param v Indica si el campo es visible
  @param ed Indica si el campo es editable
  @param pI Indica el número de dígitos de la parte entera
  @param pD Indica el número de decimales
  @param iNX TRUE si el campo es índice
  @param uNI TRUE si el campo determina registros únicos
  @param coun Indica si es un contador. Para referencias automáticas
  @param defValue Valor por defecto para el campo
  @param oT Indica si las modificaciones en el campo son fuera de transaccion
  @param rX Expresion regular utilizada como mascara de validacion
  @param vG Indica si el campo es visible en la rejilla de la tabla
  @param gen Indica si el campo es generado.
  @param iCK Indica si es clave compuesta
    """  

    Serial = 100
    Unlock = 200
    Check = 300
    count_ = 0

    def __init__(self, n, a, aN, isPrimaryKey, t, l=0, c=False, v=True, ed=False, pI=4, pD=0, iNX=False, uNI=False,count=False,defValue=None,oT=False, rX=None, vG=True,gen=True,iCK=False):
        #FLFieldMetaData(const FLFieldMetaData *other);
        self._fieldName = n
        self._alias = a
        self._allowNull = bool(aN)
        self.__isPrimaryKey = bool(isPrimaryKey)
        self._type = t
        self._length = l
        self._calculated = bool(c)
        self._visible = bool(v)
        self._editable = bool(ed)
        self._partInteger = pI
        self._partDecimal = pD
        self._isIndex = bool(iNX)
        self._isUnique = bool(uNI)
        self._contador = bool(count)
        self._defaultValue = defValue
        self.__outTransaction = oT
        self._regExpValidator = rX
        self._visibleGrid = vG
        self._generated = bool(gen)
        self._isCompoundKey = bool(iCK)
        ++self.count_
    
    def __del__(self):
        --self.count_
        
        

    @decorators.BetaImplementation
    def name(self):
        return self._fieldName

    @decorators.BetaImplementation
    def setName(self, n):
        self._fieldName = n

    @decorators.BetaImplementation
    def alias(self):
        return self._alias

    @decorators.BetaImplementation
    def allowNull(self):
        return self._allowNull

    @decorators.BetaImplementation
    def isPrimaryKey(self):
        return self.__isPrimaryKey

    @decorators.BetaImplementation
    def isCompoundKey(self):
        return self._isCompoundKey
    
    @decorators.BetaImplementation
    def setIsPrimaryKey(self, b):
        self.__isPrimaryKey = bool(b)
    
    @decorators.BetaImplementation
    def type(self):
        return self._type
    
    @decorators.BetaImplementation
    def length(self):
        return self._length

    @decorators.BetaImplementation
    def calculated(self):
        return self._calculated

    @decorators.BetaImplementation
    def setCalculated(self, c):
        self._calculated = bool(c)

    @decorators.BetaImplementation
    def editable(self):
        return self._editable

    @decorators.BetaImplementation
    def setEditable(self, e):
        self._editable = e

    @decorators.BetaImplementation
    def visible(self):
        return self._visible

    @decorators.BetaImplementation
    def setVisible(self, v):
        self._visible = bool(v)

    @decorators.BetaImplementation
    def setVisibleGrid(self, vG):
        self._visibleGrid = bool(vG)

    @decorators.BetaImplementation
    def visibleGrid(self):
        return self._visibleGrid

    @decorators.BetaImplementation
    def genetated(self):
        return self._generated

    @decorators.BetaImplementation
    def partInteger(self):
        return self._partInteger

    @decorators.BetaImplementation
    def partDecimal(self):
        return self._partDecimal

    @decorators.BetaImplementation
    def isCounter(self):
        return self._contador

    @decorators.BetaImplementation
    def isIndex(self):
        return self._isIndex

    @decorators.BetaImplementation
    def isUnique(self):
        return self._isUnique    

    @decorators.BetaImplementation
    def addRelationMD(self, relationMD):
        isRelM1 = (relationMD.cardinality() == FLRelationMetaData.RELATION_M1)
        if (isRelM1 and self._relationM1):
            print("FLFieldMetaData: Se ha intentado crear más de una relación muchos a uno para el mismo campo")
            return 
        relationMD.setField(self._fieldName)
        if (isRelM1):
            self._relationM1 = relationMD
            return
        if not self._relationList:
            self._relationList = FLRelationMetaDataList
        self._relationList.append(relationMD)
        

    def clearRelationList(self):
        if not self._relationList:
            return
        
        r = FLRelationMetaData()
        it = FLRelationMetaData(self._relationList)
        while not it.current() == 0:
            r = it.current()
            ++it
            self._relationList.remove(r)
            if r.deref():
                del r 
        
        del self._relationList
        self._relationList = 0
        

    def relationM1(self):
        return self._relationM1 #FLRelationMetaData

    def setAssociatedField(self, fMD,field ):
        #completar

    def setAssociatedField(self, rName, f):
        #completar

    def associatedField(self):
        return self._associatedField

    def associatedFieldFilterTo(self):
        return self._associatedFieldFilterTo

    def associatedFieldName(self):
        return self._associatedField.name()

    def defaultValue(self):
        return self._defaultValue

    def outTransaction(self):
        return self.__outTransaction

    def regExpValidator(self):
        return self._regExpValidator

    def optionsList(self):
        return self._optionsList

    def setOptionsList(self, ol):
        self._optionsList.clear()
        olTranslated = QtCore.QString(ol)
        if ol.contains("QT_TRANSLATE_NOOP"):
            components =  QtCore.QStringList(olTranslated.split(","))
            component = QtCore.QString("")
            olTranslated = ""
            for i in range(len(components)):
                component = component.mid(30, component.length() - 32)
                if i > 0:
                    olTranslated += ","
                olTranslated += component
            
        
        self._optionsList = olTranslated.split(",")
        self._hasOptionsList = not self.optionsList_.empty()
        

    def isCheck(self):
        #completar

    def hasOptionsList(self):
        if(self._optionsList): return True
        return False

    def fullyCalculated(self):
        return self._calculated

    def setFullyCalculated(self, c):
        self._calculated = bool(c)

    def trimed(self):
        #return self._trimmed

    def setTrimed(self, t):
        self._trimmed = bool(t)

    def setMetadata(self, mTD):
        self._mTD = FLTableMetaData(mTD)

    def metadata(self):
        return self._mTD

    def flDecodeType(self, fltype): #revisar
        QtCore.QVariant.Type type;
        if fltype == QtCore.QVariant.Int: type = QtCore.QVariant.Int
        if fltype == FLFieldMetaData.Serial or fltype == QtCore.QVariant.UInt: type = QtCore.QVariant.UInt
        if fltype == QtCore.QVariant.Bool or fltype == FLFieldMetaData.Unlock: type = QtCore.QVariant.Bool
        if fltype == QtCore.QVariant.Double: type = QtCore.QVariant.Double
        if fltype == QtCore.QVariant.Time: type = QtCore.QVariant.Time
        if fltype == QtCore.QVariant.Date: type = QtCore.QVariant.Date
        if fltype == QtCore.QVariant.String or fltype == QtCore.QVariant.Pixmap or fltype == QtCore.QVariant.StringList: type = QtCore.QVariant.String
        if fltype == QtCore.QVariant.ByteArray: type = QtCore.QVariant.ByteArray
        return type        
    
    @decorators.BetaImplementation
    def searchOptions(self):
        return self._searchOptions
    
    @decorators.BetaImplementation
    def setSearchOptions(self, ol):
        self._searchOptions.clear()
        self._searchOptions = QtCore.QStringList::split(',', ol)
    
    @decorators.BetaImplementation    
    def copy(self, other):
        if other == self: return
        od = FLFieldMetaDataPrivate(other.d)
        if od._relationM1: 
            od._relationM1.ref()
            self._relationM1 = od._relationM1
        self.clearRelationList()
        if od._relationList:
            r = FLRelationMetaData()
            it = od._relationList
            while ((r = it.current()) != 0): # FIXME: MIRAR
                ++it
                if not self._relationList:
                    self._relationList = FLRelationMetaDataList()
                r.ref()
        self._relationList.append(r)
        self._fieldName = od._fieldName
        self._alias = od._alias
        self._allowNull = od._allowNull
        self._isPrimaryKey = od._isPrimaryKey
        self._type = od._type
        self._length = od._length
        self._calculated = od._calculated
        self._fullyCalculated = od._fullyCalculated
        self._trimmed = od._trimmed
        self._visible = od._visible
        self._editable = od._editable
        self._partInteger = od._partInteger
        self._partDecimal = od._partDecimal
        self._isIndex = od._isIndex
        self._isUnique = od._isUnique
        self._contador = od._contador
        self._associatedField = od._associatedField
        self._associatedFieldName = od._associatedFieldName
        self._associatedFieldFilterTo = od._associatedFieldFilterTo
        self._defaultValue = od._defaultValue
        self._optionsList = od._optionsList
        self._outTransaction = od._outTransaction
        self._regExpValidator = od._regExpValidator
        self._visibleGrid = od._visibleGrid
        self._generated = od._generated
        self._isCompoundKey = od._isCompoundKey
        self._hasOptionsList = od._hasOptionsList
