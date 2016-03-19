# -*- coding: utf-8 -*-

#Completa Si

from pineboolib import decorators
from pineboolib.fllegacy.FLFieldMetaData import FLFieldMetaData

import sip
from pineboolib.fllegacy.FLCompoundKey import FLCompoundkey
from pineboolib.fllegacy.FLFieldMetaDataList import FLFieldMetaDataList

# switch on QVariant in Python3
sip.setapi('QVariant', 2)
sip.setapi('QString', 1)

from PyQt4.QtCore import QString, QVariant

"""
Mantiene la definicion de una tabla.

Esta clase mantienen la definicion de
ciertas caracteristicas de una tabla de la base
de datos.

Adicionalmente puede ser utilizada para la definición de
los metadatos de una consulta, ver FLTableMetaData::query().

@author InfoSiAL S.L.
"""

class FLTableMetaData():


    d = None

    """
    constructor

    @param n Nombre de la tabla a definir
    @param a Alias de la tabla, utilizado en formularios
    @param q (Opcional) Nombre de la consulta de la que define sus metadatos
    """
  
    @decorators.BetaImplementation
    def __init__(self, *args, **kwargs):
        if len(args) == 1:
            self.inicializeFLTableMetaData(args[0])
        else:
            self.inicializeNewFLTableMetaData( args, kwargs)    
        ++self.count_
        
        
    @decorators.BetaImplementation    
    def inicializeFLTableMetaData(self, *other):
        self.d = FLTableMetaDataPrivate()
        self.copy()
        
                                           
    @decorators.BetaImplementation
    def inicializeNewFLTableMetaData(self, n, a, q = None):
        self.d = FLTableMetaDataPrivate(n, a, q)
    


    """
    destructor
    """   
    def __del__(self):
        del self.d
    
    """
    Obtiene el nombre de la tabla

    @return El nombre de la tabla que se describe
    """
    @decorators.BetaImplementation
    def name(self):
        return self.d.name_
    
    """
    Establece el nombre de la tabla

    @param n Nombre de la tabla
    """
    @decorators.BetaImplementation
    def setName(self, n):
        #QObject::setName(n);
        self.d.name_ = n
        

    """
    Establece el alias

    @param a Alias
    """
    @decorators.BetaImplementation
    def setAlias(self, a):
        self.d.alias_ = a

    """
    Establece el nombre de la consulta

    @param q Nombre de la consulta
    """
    @decorators.BetaImplementation
    def setQuery(self, q):
        self.d.query_ = q

    """
    Obtiene el alias asociado a la tabla
    """
    @decorators.BetaImplementation
    def alias(self):
        return self.d.alias_

    """
    Obtiene el nombre de la consulta de la que define sus metadatos.

    El nombre corresponderá a la definición de una consulta mediante
    (fichero .qry). Si el nombre de la consulta está definido entonces
    el nombre de la tabla correponderá a la tabla principal de la consulta
    cuando esta referencie a varias tablas.
    """
    @decorators.BetaImplementation
    def query(self):
        return self.d.query_

    """
    Obtiene si define los metadatos de una consulta
    """
    @decorators.BetaImplementation
    def isQuery(self):
        return (not self.d.query_.isEmpty())

    """
    Añade la descripción de un campo a lista de descripciones de campos.

    @param f Objeto FLFieldMetaData con la descripción del campo a añadir
    """
    @decorators.BetaImplementation
    def addFieldMD(self, f):
        if not f:
            return
        if not f.metadata():
            f.setMetadata(self)
        self.d.fieldList_[self.d.fieldName_.lower()] = f 
        self.d.addFieldName(f.d.fieldName_)
        self.d.formatAlias(f)
        if f.d.type_ == FLFieldMetaData.Unlock:
            self.d.fieldsNamesUnlock_.append(f.d.fieldName_)
        if f.d.isPrimaryKey_:
            self.d.primaryKey_ = f.d.fieldName_.lower()

    """
    Elimina la descripción de un campo de la lista de descripciones de campos.

    @param fN Nombre del campo a eliminar
    """
    @decorators.BetaImplementation
    def removeFieldMD(self, fN):
        if fN.isEmpty():
            return
        
        self.d.fieldList_[fN.lower()].clear()
        self.d.removeFieldName(fN)
                    
    """
    Establece la clave compuesta de esta tabla.

    @param cK Objeto FLCompoundKey con la descripción de la clave compuesta
    """
    @decorators.BetaImplementation
    def setCompoundKey(self, cK):
        self.d.compoundKey_ = cK

    """
    Obtiene el nombre del campo que es clave primaria para esta tabla.

    @param prefixTable Si es TRUE se añade un prefijo con el nombre de la tabla; nombretabla.nombrecampo
    """
    @decorators.BetaImplementation
    def primaryKey(self, prefixTable = False):
        if "." in self.d.primaryKey_:
            return self.d.primaryKey_
        
        if prefixTable:
            return (self.d.name_ + QString(".") + self.d.primaryKey_)
        else:
            return self.d.primaryKey_
  
    """
    Obtiene el alias de un campo a partir de su nombre.

    @param fN Nombre del campo
    """
    @decorators.BetaImplementation
    def fieldNameToAlias(self, fN):
        
        if fN.isEmpty():
            return fN
        
        for key in self.d.fieldAliasMap_.key():
            if self.d.fieldAliasMap_[key] == fN.lower():
                return self.d.fieldAliasMap_[key]
                    
        return fN
    
    """
    Obtiene el nombre de un campo a partir de su alias.

    @param aN Nombre del alias del campo
    """
    @decorators.BetaImplementation
    def fieldAliasToName(self, aN):
            
        if aN.isEmpty():
            return aN
        
        if self.d.fieldAliasMap_.has_key(aN):
            return self.d.fieldAliasMap_[aN]
        else:
            return aN
        
    

    """
    Obtiene el tipo de un campo a partir de su nombre.

    @param fN Nombre del campo
    """
    @decorators.BetaImplementation
    def fieldType(self, fN):
        if fN.isEmpty():
            return QVariant.Invalid
        else:
            if self.d.fieldList_[fN.lower()]:
                return self.d.fieldList_[fN.lower()].d.type_
            else:
                return QVariant.Invalid 


    """
    Obtiene si un campo es clave primaria partir de su nombre.

    @param fN Nombre del campo
    """
    @decorators.BetaImplementation
    def fieldIsPrimaryKey(self, fN):
        return (self.d.primaryKey_ == fN.lower())

    """
    Obtiene si un campo es índice a partir de su nombre.

    @param fN Nombre del campo
    """
    @decorators.BetaImplementation
    def fieldIsIndex(self, fN):
        if fN.isEmpty():
            return False
        
        field = None
        
        for f in self.d.fieldName_:
            if f.name() == fN.lower():
                field = f
                break
        
        if field:
            return field.d.isIndex_
        
        return False

    """
    Obtiene si un campo es contador.

    @param fN Nombre del campo
    @author Andrés Otón Urbano (baxas@eresmas.com)
    """
    @decorators.BetaImplementation
    def fieldIsCounter(self, fN):
        if fN.isEmpty():
            return False
        
        field = None
        
        for f in self.d.fieldName_:
            if f.name() == fN.lower():
                field = f
                break
        
        if field:
            return field.d.contador_
        
        return False

    """
    Obtiene si un campo puede ser nulo

    @param fN Nombre del campo
    """
    @decorators.BetaImplementation
    def fieldAllowNull(self, fN):
        if fN.isEmpty():
            return False
        
        field = None
        
        for f in self.d.fieldName_:
            if f.name() == fN.lower():
                field = f
                break
        
        if field:
            return field.d.allowNull_
        
        return False

    """
    Obtiene si un campo es único a partir de su nombre.

    @param fN Nombre del campo
    """
    @decorators.BetaImplementation
    def fieldIsUnique(self, fN):
        if fN.isEmpty():
            return False
        
        field = None
        
        for f in self.d.fieldName_:
            if f.name() == fN.lower():
                field = f
                break
        
        if field:
            return field.d.isUnique_
        
        return False

    """
    Obtiene el nombre de la tabla foránea relacionada con un campo de esta tabla mediante
    una relacion M1 (muchos a uno).

    @param fN Campo de la relacion M1 de esta tabla, que se supone que esta relacionado
        con otro campo de otra tabla
    @return El nombre de la tabla relacionada M1, si hay relacion para el campo, o una cadena
      vacia sin el campo no está relacionado
    """
    @decorators.BetaImplementation
    def fieldTableM1(self, fN):
        if fN.isEmpty():
            return False
        
        field = None
        
        for f in self.d.fieldName_:
            if f.name() == fN.lower():
                field = f
                break
        
        if field and field.d.relationM1_:
            return field.d.relationM1_.foreignTable()
        
        return QString.Null

    """
    Obtiene el nombre del campo de la tabla foránea relacionado con el indicado mediante
    una relacion M1 (muchos auno).

    @param fN Campo de la relacion M1 de esta tabla, que se supone que esta relacionado
        con otro campo de otra tabla
    @return El nombre del campo foráneo relacionado con el indicado
    """
    @decorators.BetaImplementation
    def fieldForeignFieldM1(self, fN):
        if fN.isEmpty():
            return False
        
        field = None
        
        for f in self.d.fieldName_:
            if f.name() == fN.lower():
                field = f
                break
        
        if field and field.d.relationM1_:
            return field.d.relationM1_.foreignField()
        
        return QString.Null        

    """
    Obtiene el objeto relación que definen dos campos.

    @param fN Nombre del campo de esta tabla que forma parte de la relación
    @param fFN Nombre del campo foráneo a esta tabla que forma parte de la relación
    @param  fTN Nombre de la tabla foránea
    @return Devuelve un objeto FLRelationMetaData con la información de la relación, siempre y
      cuando esta exista. Si no existe devuelve 0
    """
    @decorators.BetaImplementation
    def relation(self, fN, fFN, fTN):
        if fN.isEmpty():
            return
        
        field = None
        
        for f in self.d.fieldName_:
            if f.name() == fN.lower():
                field = f
                break
            
        if field:
            if field.d.relationM1_ and field.d.relationM1_.foreignField() == fFN.lower() and field.d.relationM1_.foreignTable() == fTN.lower():
                return field.d.relationM1_
            
            relationList = field.d.relationList_
            if not relationList:
                return
            
            if len(relationList) == 0:
                return
            
            for itR in relationList:
                if itR.foreignField() == fFN.lower() and itR.foreignTable() == fTN.lower():
                    return itR
            
            return
   

    """
    Obtiene la longitud de un campo a partir de su nombre.

    @param fN Nombre del campo
    """
    @decorators.BetaImplementation
    def fieldLength(self, fN):
        if fN.isEmpty():
            return
        
        
        field = None
        
        for f in self.d.fieldName_:
            if f.name() == fN.lower():
                field = f
                break
            
        if field:
            return field.d.length_ 
        
        return
        
    """
    Obtiene el número de dígitos de la parte entera de un campo a partir de su nombre.

    @param fN Nombre del campo
    """
    @decorators.BetaImplementation
    def fieldPartInteger(self, fN):
        if fN.isEmpty():
            return
        
        
        field = None
        
        for f in self.d.fieldName_:
            if f.name() == fN.lower():
                field = f
                break
            
        if field:
            return field.d.partInteger_ 
        
        return

    """
    Obtiene el número de dígitos de la parte decimal de un campo a partir de su nombre.

    @param fN Nombre del campo
    """
    @decorators.BetaImplementation
    def fieldPartDecimal(self, fN):
        if fN.isEmpty():
            return
        
        
        field = None
        
        for f in self.d.fieldName_:
            if f.name() == fN.lower():
                field = f
                break
            
        if field:
            return field.d.partDecimal_ 
        
        return
        

    """
    Obtiene si un campo es calculado.

    @param fN Nombre del campo
    """
    @decorators.BetaImplementation
    def fieldCalculated(self, fN):
        if fN.isEmpty():
            return
        
        
        field = None
        
        for f in self.d.fieldName_:
            if f.name() == fN.lower():
                field = f
                break
            
        if field:
            return field.d.calculated_ 
        
        return False       

    """
    Obtiene si un campo es visible.

    @param fN Nombre del campo
    """
    @decorators.BetaImplementation
    def fieldVisible(self, fN):

        if fN.isEmpty():
            return
        
        
        field = None
        
        for f in self.d.fieldName_:
            if f.name() == fN.lower():
                field = f
                break
            
        if field:
            return field.d.visible_ 
        
        return False   
        

    """ Obtiene los metadatos de un campo.

    @param fN Nombre del campo
    @return Un objeto FLFieldMetaData con lainformación o metadatos de un campo dado
    """
    @decorators.BetaImplementation
    def field(self, fN):

        if fN.isEmpty():
            return
        
        
        field = None
        
        for f in self.d.fieldName_:
            if f.name() == fN.lower():
                field = f
                break
        
        return field       

    """
    Para obtener la lista de definiciones de campos.

    @return Objeto con la lista de deficiones de campos de la tabla
    """
    #def fieldList(self):
    #    return self.d.fieldList_

    """
    Para obtener una cadena con los nombres de los campos separados por comas.

    @param prefixTable Si es TRUE se añade un prefijo a cada campo con el nombre de la tabla; nombretabla.nombrecampo
    @return Cadena de caracteres con los nombres de los campos separados por comas
    """
    @decorators.BetaImplementation
    def fieldList(self, prefixTable = None):
        
        if not prefixTable:
            return self.d.fieldList_
        
        fieldsNames = self.d.fieldsNames_
        ret = QString.null
        
        for it in fieldsNames:
            if "." in it:
                ret = ("," + self.d.name_ + ".").join(fieldsNames)
        
        return ret 
    
 
        

    """
    Obtiene la lista de campos de una clave compuesta, a partir del nombre de
    un campo del que se quiere averiguar si está en esa clave compuesta.

    @param fN Nombre del campo del que se quiere averiguar si pertenece a una clave compuesta.
    @return Si el campo pertenece a una clave compuesta, devuelve la lista de campos
      que forman dicha clave compuesta, incluido el campo consultado. En el caso
      que el campo consultado no pertenezca a ninguna clave compuesta devuelve 0
    """
    @decorators.BetaImplementation
    def fieldListOfCompoundKey(self, fN):
        if self.d.compoundKey_ and self.d.compoundKey_.hasField(fN):
            return self.d.compoundKey_.fieldList()
        return 

    """
    Obtiene una cadena de texto que contiene los nombres de los campos separados por comas.

    El orden de los campos de izquierda a derecha es el correspondiente al orden en que
    se han añadido con el método addFieldMD() o addFieldName()
    """
    @decorators.BetaImplementation
    def fieldsNames(self):
        return self.d.fieldsNames_

    """
    Lista de nombres de campos de la tabla que son del tipo FLFieldMetaData::Unlock
    """
    @decorators.BetaImplementation
    def fieldsNamesUnlock(self):
        return self.d.fieldsNamesUnlock_
    """
    @return El indicador FLTableMetaData::concurWarn_
    """
    @decorators.BetaImplementation
    def concurWarn(self):
        return self.d.concurWarn_

    """
    Establece el indicador FLTableMetaData::concurWarn_
    """
    @decorators.BetaImplementation
    def setConcurWarn(self, b = True):
        self.d.concurWarn_ = b

    """
    @return El indicador FLTableMetaData::detectLocks_
    """
    @decorators.BetaImplementation
    def detectLocks(self):
        return self.d.detectLocks_

    """
    Establece el indicador FLTableMetaData::detectLocks_
    """
    @decorators.BetaImplementation
    def setDetectLocks(self, b = True):
        self.d.detectLocks_ = b

    """
    Establece el nombre de función a llamar para Full Text Search
    """
    @decorators.BetaImplementation
    def FTSFunction(self):
        return self.d.ftsfun_
    
    @decorators.BetaImplementation
    def setFTSFunction(self, ftsfun):
        self.d.ftsfun_ = ftsfun

    """
    Indica si lo metadatos están en caché (FLManager::cacheMetaData_)
    """
    @decorators.BetaImplementation
    def inCache(self):
        return self.d.inCache_

    """
    Establece si lo metadatos están en caché (FLManager::cacheMetaData_)
    """
    @decorators.BetaImplementation
    def setInCache(self, b = True):
        self.d.inCache_ = b

    @decorators.BetaImplementation
    def copy(self, other):
        if other == self:
            return
     
        od = other.d
      
        if od.compoundKey_:
            self.d.compoundKey_ = FLCompoundkey(od.compoundKey_)
        
        self.d.clearFieldList()
        
        self.d.fieldList_ = od.d.fieldList_
        
        self.d.name_ = od.name_
        self.d.alias_ = od.alias_
        self.d.query_ = od.query_
        self.d.fieldsNames_ = od.fieldsNames_
        self.d.aliasFieldMap_ = od.aliasFieldMap_
        self.d.fieldAliasMap_ = od.fieldAliasMap_
        self.d.fieldsNamesUnlock_ = od.fieldsNamesUnlock_
        self.d.primaryKey_ = od.primaryKey_
        self.d.concurWarn_ = od.concurWarn_
        self.d.detectLocks_ = od.detectLocks_;

        for it2 in od.fieldList_.values():
            if not od.fieldList_[it2].d.associatedFieldName_.isEmpty():
                od.fieldList_[it2].d.associatedField_ = self.field(od.fieldList_[it2].d.associatedFieldName_)





class FLTableMetaDataPrivate():

    
    """
    Nombre de la tabla
    """
    name_ = None

    """
    Alias de la tabla
    """
    alias_ = None

    """
    Lista de campos que tiene esta tabla
    """
    fieldList_ = {}

    """
    Clave compuesta que tiene esta tabla
    """
    compoundKey_ = None

    """
    Nombre de la consulta (fichero .qry) de la que define los metadatos
    """
    query_ = None

    """
    Cadena de texto con los nombre de los campos separados por comas
    """
    fieldsNames_ = []

    """
    Mapas alias<->nombre
    """
    aliasFieldMap_ = {}
    fieldAliasMap_ = {}

    """
    Lista de nombres de campos de la tabla que son del tipo FLFieldMetaData::Unlock
    """
    fieldsNamesUnlock_ = []

    """
    Clave primaria
    """
    primaryKey_ = None

    """
    Indica si se debe avisar de colisión de concurrencia entre sesiones.

    Si este flag es true y dos o mas sesiones/usuarios están modificando los
    mismos campos,al validar un formulario (FLFormRecordDB::validateForm)
    mostrará un aviso de advertencia.

    Ver también FLSqlCursor::concurrencyFields().
    """
    concurWarn_ = None

    """
    Indica si se deben comprobar riesgos de bloqueos para esta tabla

    Si este flag es true FLSqlCursor::commitBuffer() chequeará siempre
    los riesgos de bloqueo para esta tabla.

    Ver también FLSqlDatabase::detectRisksLocks
    """
    detectLocks_ = None
  
    """
    Indica el nombre de función a llamar para la búsqueda con Full Text Search
    """
    ftsfun_ = None
  
    """
    Indica si lo metadatos están en caché (FLManager::cacheMetaData_)
    """
    inCache_ = None
  
  
  
  
  

    @decorators.BetaImplementation
    def __init__(self, *args, **kwargs):
        if len(args) == 0:
            self.inicializeFLTableMetaDataPrivate()
        else:
            self.inicializeNewFLTableMetaDataPrivate( args, kwargs)    
        ++self.count_
        
        
    @decorators.BetaImplementation    
    def inicializeFLTableMetaDataPrivate(self):
        self.compoundKey_ = None
        self.inCache = False
        
        self.fieldList_ = FLFieldMetaDataList()
                    
    @decorators.BetaImplementation
    def inicializeNewFLTableMetaDataPrivate(self, n, a, q = None):
        self.name_ = n.lowe()
        self.alias_ = a 
        self.compoundKey_ = 0
        self.query_ = q
        self.concurWarn_ = False
        self.detectLocks_ = False
        self.inCache_ = False
    
        self.fieldList_ = FLFieldMetaDataList()
        

    """
    Añade el nombre de un campo a la cadena de nombres de campos, ver fieldsNames()

    @param n Nombre del campo
    """
    @decorators.BetaImplementation
    def addFieldName(self, n):
        self.fieldsNames_.append(n.lower())

    """
    Elimina el nombre de un campo a la cadena de nombres de campos, ver fieldsNames()

    @param n Nombre del campo
    """
    @decorators.BetaImplementation
    def removeFieldName(self, n):
        
        if self.fieldsNames_:
            oldFN = self.fieldsNames_
            self.fieldsNames_ = []
            for value in oldFN:
                if not value.name().lower() == n.lower():
                    self.fieldsNames.append(value)

    """
    Formatea el alias del campo indicado para evitar duplicados

    @param  f   Campo objeto cuyo alias se desea formatear
    """
    @decorators.BetaImplementation
    def formatAlias(self,  f):
        if not f:
            return
        
        alias = QString(f.alias())
        field = QString(f.name().lower())
        
        if self.aliasFieldMap_.has_key(alias):
            alias += QString("(") + QString(len(self.aliasFieldMap_) + 1) + QString(")")
        
        f.d.alias_ = alias
        
        self.aliasFieldMap_[ alias ] = field
        self.fieldAliasMap_[ field ] = alias

    """
    Limpia la lista de definiciones de campos
    """
    @decorators.BetaImplementation
    def clearFieldList(self):
        self.fieldList_.clear()
        self.fieldsNames_.clear()


#endif