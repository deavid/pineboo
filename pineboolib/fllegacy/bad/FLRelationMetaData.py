# -*- coding: utf-8 -*-

from pineboolib import decorators

class FLRelationMetaData():
    RELATION_1M = 0
    RELATION_M1 = 1
    
    field_ = None
    count_ = 0
    
    def __init__(self, *args, **kwargs):
        if len(args) == 1:
            self.inicializeFromFLRelationMetaData(args[0])
        else:
            self.inicializeNewFLRelationMetaData( args[0], args[1], args[2], args[3], args[4], args[5])
            
    #@param fT Tabla foránea relacionada
    #@param fF Campo foráneo relacionado
    #@param rC Cardinalidad de la relacion
    #@param dC Borrado en cascada, sólo se tiene en cuenta en cardinalidades M1
    #@param uC Actualizaciones en cascada, sólo se tiene en cuenta en cardinalidades M1
    #@param cI Chequeos de integridad sobre la relacion
    
    @decorators.BetaImplementation
    def inicializeNewFLRelationMetaData(self, fT, fF, rC, dC, uC, cI):
        self._foreignTable = fT
        self._foreignField = fF
        self._cardinality = rC
        self._deleteCascade = bool(dC)
        self._updateCascade = bool(uC)
        self._checkIntegrity = bool(cI)
        ++self.count_
    
    #@param other FLRelationMetaData
    
    @decorators.BetaImplementation
    def inicializeFromFLRelationMetaData(self, other):
        self.copy(other)
        ++self.count_
    
    def __del__(self):
        del self
        --self.count_
    
 
    def setField(self, fN):
        self._fieldName = fN
        

    def field(self):
        return self._fieldName

    def foreingTable(self):
        return self._foreignTable

    def foreingField(self):
        return self._foreignField

    def cardinality(self):
        return self._cardinality

    def deleteCascade(self):
        return (self._deleteCascade and self._cardinality == FLRelationMetaData.RELATION_M1)

    def updateCascade(self):
        return (self._updateCascade and self._cardinality == FLRelationMetaData.RELATION_M1)

    def checkIn(self):
        return self._checkIntegrity
    
    @decorators.BetaImplementation
    def copy(self, other):
        if other == self:
            return
        
        self.field_ = other.field_ 
        self._foreignTable = other._foreignTable
        self._foreignField = other._foreignField
        self._cardinality = other._cardinality
        self._deleteCascade = other._deleteCascade
        self._updateCascade = other._updateCascade
        self._checkIntegrity = other._checkIntegrity
        
    
    
        

