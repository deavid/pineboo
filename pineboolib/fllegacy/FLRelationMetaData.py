# -*- coding: utf-8 -*-

#Completada Si

from pineboolib import decorators


class FLRelationMetaData():
    
    """
    Constantes de tipos de cardinalidades de una relacion 
    """
    
    RELATION_1M = "1M"
    RELATION_M1 = "M1"
    
    
    count_ = 0
    
    d = None
    
    
    
    def __init__(self, *args, **kwargs):
        if len(args) == 1:
            self.inicializeFromFLRelationMetaData(args[0])
        else:
            self.inicializeNewFLRelationMetaData( args[0], args[1], args[2], args[3], args[4], args[5])
        
        ++self.count_

    """
    constructor

    @param fT Tabla foránea relacionada
    @param fF Campo foráneo relacionado
    @param rC Cardinalidad de la relacion
    @param dC Borrado en cascada, sólo se tiene en cuenta en cardinalidades M1
    @param uC Actualizaciones en cascada, sólo se tiene en cuenta en cardinalidades M1
    @param cI Chequeos de integridad sobre la relacion
    """
    def inicializeNewFLRelationMetaData(self, fT, fF, rC, dC = False, uC = False, cI = True):
        self.d = FLRelationMetaDataPrivate(fT, fF, rC, dC, uC, cI) 
    
    @decorators.BetaImplementation    
    def inicializeFromFLRelationMetaData(self, *other):
        self.d = FLRelationMetaDataPrivate()
        self.copy(other)
    
    
    """
    destructor
    """
    def __del__(self):
        --self.count_
        del self.d
        
    
    """
    Establece el nombre del campo relacionado.

    @param fN Nombre del campo relacionado
    """
    def setField(self, fN):
        self.d.field_ = fN.lower()

    """
    Obtiene en el nombre del campo de la relacion.

    @return Devuelve el nombre del campo relacionado
    """
    def field(self):
        return self.d.field_

    """
    Obtiene el nombre de la tabla foránea.

    @return Devuelve el nombre de la tabla de la base de datos con la que se está relacionada
    """
    def foreignTable(self):
        return self.d.foreignTable_
        
    """
    Obtiene el nombre de la campo foráneo.

    @return Devuelve el nombre del campo de la tabla foránea con la que está relacionada
    """
    def foreignField(self):
        return self.d.foreignField_

    """
    Obtiene la cardinalidad de la relacion.

    @return Devuelve la cardinalidad de la relacion, mirando desde la tabla donde se
        define este objeto hacia la foránea
    """
    def cardinality(self):
        return self.d.cardinality_

    """
    Obtiene si la relación implica borrados en cascada, sólo se tiene en cuenta en cardinalidades M1.

    @return Devuelve TRUE si la relacion implica borrados en cascada, FALSE en caso contrario
    """
    @decorators.BetaImplementation
    def deleteCascade(self):
        return (self.d.deleteCascade_ and self.d.cardinality_ == self.RELATION_M1)

    """
    Obtiene si la relación implica modificaciones en cascada, sólo se tiene en cuenta en cardinalidades M1.

    @return Devuelve TRUE si la relacion implica modificaciones en cascada, FALSE en caso contrario
    """
    @decorators.BetaImplementation
    def updateCascade(self):
        return (self.d.updateCascade_ and self.d.cardinality_ == self.RELATION_M1)

    """
    Obtiene si se deben aplicar la reglas de integridad sobre la relación
    """
    @decorators.BetaImplementation
    def checkIn(self):
        return self.d.checkIn_
        
    @decorators.BetaImplementation
    def copy(self, *other):
        if other == self:
            return
        self.d.field_ = other.d.field_
        self.d.foreignTable_ = other.d.foreignTable_
        self.d.foreignField_ = other.d.foreignField_
        self.d.cardinality_ = other.d.cardinality_
        self.d.deleteCascade_ = other.d.deleteCascade_
        self.d.updateCascade_ = other.d.updateCascade_
        self.d.checkIn_ = other.d.checkIn_
   


class FLRelationMetaDataPrivate():
    
    """
    Nombre del campo a relacionar
    """
    Field_ = None

    """
    Nombre de la tabla foránea a relacionar
    """
    foreignTable_ = None

    """
    Nombre del campo foráneo relacionado
    """
    foreignField_ = None

    """
    Cardinalidad de la relación
    """
    cardinality_ = None

    """
    Indica si los borrados serán en cascada, en relaciones M1
    """
    deleteCascade_ = None

    """
    Indica si las modificaciones serán en cascada, en relaciones M1
    """
    updateCascade_ = None

    """
    Indica si se deben aplicar la reglas de integridad en esta relación
    """
    checkIn_ = None

    def __init__(self, *args, **kwargs):
        if len(args) == 0:
            self.inicializeFromFLRelationMetaDataPrivate()
        else:
            self.inicializeNewFLRelationMetaDataPrivate( args[0], args[1], args[2], args[3], args[4], args[5])
            
            
    def inicializeNewFLRelationMetaDataPrivate(self, fT, fF, rC, dC, uC, cI):
        self.foreignTable_ = str(fT).lower()
        self.foreignField_ = str(fF).lower()
        self.cardinality_ = rC
        self.deleteCascade_ = dC
        self.updateCascade_ = uC
        self.checkIn_ = cI
    
    
    @decorators.BetaImplementation    
    def inicializeFLRelationMetaDataPrivate(self):
        return
        
        
