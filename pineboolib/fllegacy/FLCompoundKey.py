# -*- coding: utf-8 -*-

#Completa Si

from pineboolib.fllegacy.FLFieldMetaData import FLFieldMetaData
from pineboolib import decorators
from pineboolib.fllegacy.FLFieldMetaDataList import FLFieldMetaDataList



"""
Clase para definir claves compuestas.

Esta clase sirve para crear objetos que contienen
una lista con los campos que conforman una clave.
En la lista de campos se guardan los metadatos de estos,
es decir objetos FLFieldMetaData.

"""

class FLCompoundkey():
    
    """
    Lista de con los metadatos de los campos que componen la clave
    """
    fieldList_ = []
    
    def __init__(self, other = None):
        self.fieldList_ = FLFieldMetaDataList.FLFieldMetaDataList
        if other:
            self.copy(other)
        
    
    
    
    
    def __del__(self):
        self.fieldList_ = None

    """
    Añade la descripción de un campo a lista  de campos que componen la clave.

    @param f Objeto FLFieldMetaData con la descripción del campo a añadir
    """
    @decorators.BetaImplementation
    def addFieldMD(self, *f):
        x = FLFieldMetaData(f.name().lower(), f)
        x.attr = len(self.fieldList_) + 1
        self.fieldList_.append(x)
        

    """
    Obtiene si una campo pertenece a la clave compuesta.

    @param fN Nombre del campo del que se desea saber si pertenece o no a la clave compuesta
    @return TRUE si el campo forma parte de la clave compuesta, FALSE en caso contrario
    """
    @decorators.BetaImplementation
    def hasField(self, fN):
        for i in range(len(self.fieldList_)):
            if self.fieldList_[i].name() == fN:
                return True
        
        return False

    """
    Para obtener la lista de definiciones de campos que componen la clave.

    @return Objeto con la lista de deficiones de campos de la clave compuesta
    """
    @decorators.BetaImplementation
    def fieldList(self):
        return self.fieldList_


    @decorators.BetaImplementation
    def copy(self, *other):
        if self == other:
            return
        self.fieldList_ = other.fieldList_
    