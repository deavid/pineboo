# -*- coding: utf-8 -*-


from PyQt4 import QtCore

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

class FLFieldMetaData()

    Serial = 100
    Unlock = 200
    Check = 300

    def __init__(self, n, a, aN, isPrimaryKey, t, l=0, c=False, v=True, ed=False, pI=4, pD=0, iNX=False, uNI=False,coun=False,defValue=None,oT=False, rX=None, vG=True,gen=True,iCK=False):
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


    def name(self):
        return self._fieldName

    def setName(self, n):
        self._fieldName = n

    def alias(self):
        return self._alias

    def allowNull(self):
        return self._allowNull

    def isPrimaryKey(self):
        return self.__isPrimaryKey

    def isCompoundKey(self):
        return self._isCompoundKey
    
    def setIsPrimaryKey(self, b):
        self.__isPrimaryKey = bool(b)

    def type(self):
        return self._type

    def length(self):
        return self._length

    def calculated(self):
        return self._calculated

    def setCalculated(self, c):
        self._calculated = bool(c)

    def editable(self):
        return self._editable

    def setEditable(self, e):
        self._editable = e

    def visible(self):
        retrun self._visible

    def setVisible(self, v):
        self._visible = bool(v)

    def setVisibleGrid(self, vG):
        self._visibleGrid = bool(vG)

    def visibleGrid(self):
        return self._visibleGrid

    def genetated(self):
        return self._generated

    def partInteger(self):
        return self._partInteger

    def partDecimal(self):
        return self._partDecimal

    def isCounter(self):
        return self._contador

    def isIndex(self):
        return self._isIndex

    def isUnique(self):
        return self._isUnique    

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
        

    def relationList(self):
        #completar ....

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
        self._optionsList = ol

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
        QVariant.Type type;
        if fltype == QVariant.Int: type = QVariant.Int
        if fltype == FLFieldMetaData.Serial or fltype == QVariant.UInt: type = QVariant.UInt
        if fltype == QVariant.Bool or fltype == FLFieldMetaData.Unlock: type = QVariant.Bool
        if fltype == QVariant.Double: type = QVariant.Double
        if fltype == QVariant.Time: type = QVariant.Time
        if fltype == QVariant.Date: type = QVariant.Date
        if fltype == QVariant.String or fltype == QVariant.Pixmap or fltype == QVariant.StringList: type = QVariant.String
        if fltype == QVariant.ByteArray: type = QVariant.ByteArray
        return type        
  
    def searchOptions(self):
        return self._searchOptions

    def setSearchOptions(self, ol):
        self._searchOptions = QStringList::split(',', ol)
        
    def copy(other):
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
