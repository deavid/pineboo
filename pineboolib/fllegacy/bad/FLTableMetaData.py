# -*- coding: utf-8 -*-

from PyQt4 import QtCore


from pineboolib import decorators

"""
Mantiene la definicion de una tabla.

Esta clase mantienen la definicion de
ciertas caracteristicas de una tabla de la base
de datos.

Adicionalmente puede ser utilizada para la definición de
los metadatos de una consulta, ver def query().

@author InfoSiAL S.L.
"""

class FLTableMetaData():
    
    count_ = 0
    d = None
    alias = None # Obtiene el alias asociado a la tabla
    
    
    
    
    
    def __init__(self, *args, **kwargs):
        
        
        if len(args) == 1:
            self.inicializeFromFLTableMetaData(args[0])
        else:
            self.inicializeNewFLTableMetaData( args[0], args[1], args[2])
        
        ++self.count_
        self.d = FLTableMetaDataPrivate()
    
    #@param other otra FLTableMetaData
       
    @decorators.NotImplementedWarn
    def inicializeFromFLTableMetaData(self, other):
        self.copy(other)

    
    #@param n Nombre de la tabla a definir
    #@param a Alias de la tabla, utilizado en formularios
    #@param q (Opcional) Nombre de la consulta de la que define sus metadatos
    
    @decorators.NotImplementedWarn
    def inicializeNewFLTableMetaData(self, n, a, q = None):

    
    
    @decorators.NotImplementedWarn
    def __del__(self):
        del self
    






    
    

    
    
    
 

    
    

    """
    Obtiene el nombre de la tabla

    @return El nombre de la tabla que se describe
    """
    @decorators.NotImplementedWarn
    def name(self):
        
    """
    Establece el nombre de la tabla

    @param n Nombre de la tabla
    """
    @decorators.NotImplementedWarn
    def setName(self, n):

    """
    Establece el alias

    @param a Alias
    """
    @decorators.NotImplementedWarn
    def setAlias(self, a):

    """
    Establece el nombre de la consulta

    @param q Nombre de la consulta
    """
    @decorators.NotImplementedWarn
    def setQuery(self, q):



    """
    Obtiene el nombre de la consulta de la que define sus metadatos.

    El nombre corresponderá a la definición de una consulta mediante
    (fichero .qry). Si el nombre de la consulta está definido entonces
    el nombre de la tabla correponderá a la tabla principal de la consulta
    cuando esta referencie a varias tablas.
    """
    @decorators.NotImplementedWarn
    def query(self):

    """
    Obtiene si define los metadatos de una consulta
    """
    @decorators.NotImplementedWarn
    def isQuery(self):

    """
    Añade la descripción de un campo a lista de descripciones de campos.

    @param f Objeto FLFieldMetaData con la descripción del campo a añadir
    """
    @decorators.NotImplementedWarn
    def addFieldMD(self, f):

    """
    Elimina la descripción de un campo de la lista de descripciones de campos.

    @param fN Nombre del campo a eliminar
    """
    @decorators.NotImplementedWarn
    def removeFieldMD(self, fN):

    """
    Establece la clave compuesta de esta tabla.

    @param cK Objeto FLCompoundKey con la descripción de la clave compuesta
    """
    @decorators.NotImplementedWarn
    def setCompoundKey(self, cK):

    """
    Obtiene el nombre del campo que es clave primaria para esta tabla.

    @param prefixTable Si es True se añade un prefijo con el nombre de la tabla nombretabla.nombrecampo
    """
    @decorators.NotImplementedWarn
    def primaryKey(self, prefixTable = False):

    """
    Obtiene el alias de un campo a partir de su nombre.

    @param fN Nombre del campo
    """
    @decorators.NotImplementedWarn
    def fieldNameToAlias(self, fN):

    """
    Obtiene el nombre de un campo a partir de su alias.

    @param aN Nombre del alias del campo
    """
    @decorators.NotImplementedWarn
    def fieldAliasToName(self, aN):

    """
    Obtiene el tipo de un campo a partir de su nombre.

    @param fN Nombre del campo
    """
    @decorators.NotImplementedWarn
    def fieldType(self, fN):

    """
    Obtiene si un campo es clave primaria partir de su nombre.

    @param fN Nombre del campo
    """
    @decorators.NotImplementedWarn
    def fieldIsPrimaryKey(self, fN):

    """
    Obtiene si un campo es índice a partir de su nombre.

    @param fN Nombre del campo
    """
    @decorators.NotImplementedWarn
    def fieldIsIndex(self, fN):

    """
    Obtiene si un campo es contador.

    @param fN Nombre del campo
    @author Andrés Otón Urbano (baxas@eresmas.com)
    """
    @decorators.NotImplementedWarn
    def fieldIsCounter(self, fN):

    """
    Obtiene si un campo puede ser nulo

    @param fN Nombre del campo
    """
    @decorators.NotImplementedWarn
    def fieldAllowNull(self, fN):

    """
    Obtiene si un campo es único a partir de su nombre.

    @param fN Nombre del campo
    """
    @decorators.NotImplementedWarn
    def fieldIsUnique(self, fN):

    """
    Obtiene el nombre de la tabla foránea relacionada con un campo de esta tabla mediante
    una relacion M1 (muchos a uno).

    @param fN Campo de la relacion M1 de esta tabla, que se supone que esta relacionado
          con otro campo de otra tabla
    @return El nombre de la tabla relacionada M1, si hay relacion para el campo, o una cadena
        vacia sin el campo no está relacionado
    """
    @decorators.NotImplementedWarn
    def fieldTableM1(self, fN):

    """
    Obtiene el nombre del campo de la tabla foránea relacionado con el indicado mediante
    una relacion M1 (muchos auno).

    @param fN Campo de la relacion M1 de esta tabla, que se supone que esta relacionado
          con otro campo de otra tabla
    @return El nombre del campo foráneo relacionado con el indicado
    """
    @decorators.NotImplementedWarn
    def fieldForeignFieldM1(self, fN):

    """
    Obtiene el objeto relación que definen dos campos.

    @param fN Nombre del campo de esta tabla que forma parte de la relación
    @param fFN Nombre del campo foráneo a esta tabla que forma parte de la relación
    @param  fTN Nombre de la tabla foránea
    @return Devuelve un objeto FLRelationMetaData con la información de la relación, siempre y
        cuando esta exista. Si no existe devuelve 0
    """
    @decorators.NotImplementedWarn
    def relation(self, fN, fFN, fTN):

    """
    Obtiene la longitud de un campo a partir de su nombre.

    @param fN Nombre del campo
    """
    @decorators.NotImplementedWarn
    def fieldLength(self, fN):

    """
    Obtiene el número de dígitos de la parte entera de un campo a partir de su nombre.

    @param fN Nombre del campo
    """
    @decorators.NotImplementedWarn
    def fieldPartInteger(self, fN):

    """
    Obtiene el número de dígitos de la parte decimal de un campo a partir de su nombre.

    @param fN Nombre del campo
    """
    @decorators.NotImplementedWarn
    def fieldPartDecimal(self, fN):

    """
    Obtiene si un campo es calculado.

    @param fN Nombre del campo
    """
    @decorators.NotImplementedWarn
    def fieldCalculated(self, fN):

    """
    Obtiene si un campo es visible.

    @param fN Nombre del campo
    """
    @decorators.NotImplementedWarn
    def fieldVisible(self, fN):

    """ Obtiene los metadatos de un campo.

    @param fN Nombre del campo
    @return Un objeto FLFieldMetaData con lainformación o metadatos de un campo dado
    """
    @decorators.NotImplementedWarn
    def field(self, fN):

    #"""
    #Para obtener la lista de definiciones de campos.

    #@return Objeto con la lista de deficiones de campos de la tabla
    #"""
    #@decorators.NotImplementedWarn
    #def fieldList(self):

    """
    Para obtener una cadena con los nombres de los campos separados por comas.

    @param prefixTable Si es True se añade un prefijo a cada campo con el nombre de la tabla nombretabla.nombrecampo
    @return Cadena de caracteres con los nombres de los campos separados por comas
    """
    @decorators.NotImplementedWarn
    def fieldList(self, prefixTable = None):

    """
    Obtiene la lista de campos de una clave compuesta, a partir del nombre de
    un campo del que se quiere averiguar si está en esa clave compuesta.

    @param fN Nombre del campo del que se quiere averiguar si pertenece a una clave compuesta.
    @return Si el campo pertenece a una clave compuesta, devuelve la lista de campos
        que forman dicha clave compuesta, incluido el campo consultado. En el caso
        que el campo consultado no pertenezca a ninguna clave compuesta devuelve 0
    """
    @decorators.NotImplementedWarn
    def fieldListOfCompoundKey(self, fN):

    """
    Obtiene una cadena de texto que contiene los nombres de los campos separados por comas.

    El orden de los campos de izquierda a derecha es el correspondiente al orden en que
    se han añadido con el método addFieldMD() o addFieldName()
    """
    @decorators.NotImplementedWarn
    def fieldsNames(self:)

    """
    Lista de nombres de campos de la tabla que son del tipo FLFieldMetaData::Unlock
    """
    @decorators.NotImplementedWarn
    def fieldsNamesUnlock(self):

    """
    @return El indicador def concurWarn_
    """
    @decorators.NotImplementedWarn
    def concurWarn(self):

    """
    Establece el indicador def concurWarn_
    """
    @decorators.NotImplementedWarn
    def setConcurWarn(self, b = True):

    """
    @return El indicador def detectLocks_
    """
    @decorators.NotImplementedWarn
    def detectLocks(self):

    """
    Establece el indicador def detectLocks_
    """
    @decorators.NotImplementedWarn
    def setDetectLocks(self, b = True):

    """
    Establece el nombre de función a llamar para Full Text Search
    """
    @decorators.NotImplementedWarn
    def FTSFunction(self):
      
    @decorators.NotImplementedWarn
    def setFTSFunction(self, ftsfun):

    """
    Indica si lo metadatos están en caché (FLManager::cacheMetaData_)
    """
    @decorators.NotImplementedWarn
    def inCache(self):

    """
    Establece si lo metadatos están en caché (FLManager::cacheMetaData_)
    """
    @decorators.NotImplementedWarn
    def setInCache(self, b = True):

    
    @decorators.NotImplementedWarn
    def copy(self, FLTableMetaData other):
        


class FLTableMetaDataPrivate():

    def __init__(self, n = None, a = None, q = None ):

    
    def __del__(self):
        del self


    """
    Añade el nombre de un campo a la cadena de nombres de campos, ver fieldsNames()

    @param n Nombre del campo
    """
    @decorators.NotImplementedWarn
    def addFieldName(self, n):

    """
    Elimina el nombre de un campo a la cadena de nombres de campos, ver fieldsNames()

    @param n Nombre del campo
    """
    @decorators.NotImplementedWarn
    def removeFieldName(self, n):

    """
    Formatea el alias del campo indicado para evitar duplicados

    @param  f   Campo objeto cuyo alias se desea formatear
    """
    @decorators.NotImplementedWarn
    def formatAlias(self, FLFieldMetaData f):

    """
    Limpia la lista de definiciones de campos
    """
    @decorators.NotImplementedWarn
    def clearFieldList(self):

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
    #FLFieldMetaDataList 
    fieldList_ = []

    """
    Clave compuesta que tiene esta tabla
    """
    FLCompoundKey compoundKey_ = None

    """
    Nombre de la consulta (fichero .qry) de la que define los metadatos
    """
    query_ = None 

    """
    Cadena de texto con los nombre de los campos separados por comas
    """
    fieldsNames_ = None 

    """
    Mapas alias<->nombre
    """
    #QMap<QtCore.QString, QtCore.QString> aliasFieldMap_ #FIXME
    #QMap<QtCore.QString, QtCore.QString> fieldAliasMap_ #FIXME

    """
    Lista de nombres de campos de la tabla que son del tipo FLFieldMetaData::Unlock
    """
    #QStringList 
    fieldsNamesUnlock_ = []

    """
    Clave primaria
    """
    primaryKey_= None
    """
    Indica si se debe avisar de colisión de concurrencia entre sesiones.

    Si este flag es True y dos o mas sesiones/usuarios están modificando los
    mismos campos,al validar un formulario (FLFormRecordDB::validateForm)
    mostrará un aviso de advertencia.

    Ver también FLSqlCursor::concurrencyFields().
    """
    bool concurWarn_= False

    """
    Indica si se deben comprobar riesgos de bloqueos para esta tabla

    Si este flag es True FLSqlCursor::commitBuffer() chequeará siempre
    los riesgos de bloqueo para esta tabla.

    Ver también FLSqlDatabase::detectRisksLocks
    """
    bool detectLocks_= False
  
    """
    Indica el nombre de función a llamar para la búsqueda con Full Text Search
    """
    ftsfun_= None
  
    """
    Indica si lo metadatos están en caché (FLManager::cacheMetaData_)
    """
    bool inCache_ = False

    @decorators.NotImplementedWarn
    def setCompoundKey(self, cK):
        self.compoundKey_ = cK
    
    @decorators.NotImplementedWarn
    def isQuery(self):
        return not self.query_.isEmpty()
    
    @decorators.NotImplementedWarn
    def name(self):
        return self.name_
    
    @decorators.NotImplementedWarn
    def alias(self):
        return self.alias_
    
    @decorators.NotImplementedWarn
    def query(self):
        return self.query_
    
    @decorators.NotImplementedWarn
    def fieldList(self):
        return self.fieldList_
    
    @decorators.NotImplementedWarn
    def fieldsNames(self):
        return self.fieldsNames_
    
    @decorators.NotImplementedWarn
    def setAlias(self, a):
        self.alias_ = a
        
    @decorators.NotImplementedWarn
    def setQuery(self, q):
        self.query_ = q
        
    @decorators.NotImplementedWarn
    def fieldsNamesUnlock(self):
        return self.fieldsNamesUnlock_
    
    @decorators.NotImplementedWarn
    def concurWarn(self):
        return self.concurWarn_
    
    @decorators.NotImplementedWarn
    def setConcurWarn(self, b):
        self.concurWarn_ = b
        
    @decorators.NotImplementedWarn
    def detectLocks(self):
        return self.detectLocks_
    
    @decorators.NotImplementedWarn
    def setDetectLocks(self, b):
        self.detectLocks_ = b

    @decorators.NotImplementedWarn
    def inCache(self):
        return self.inCache_

    @decorators.NotImplementedWarn
    def setInCache(self, b):
        self.inCache_ = b

    @decorators.NotImplementedWarn
    def FTSFunction(self):
        return self.ftsfun_

    @decorators.NotImplementedWarn
    def setFTSFunction(self, ftsfun):
        self.ftsfun_ = ftsfun


#endif