class FLRelationMetaData(self):
    RELATION_1M = 0
    RELATION_M1 = 1

    #@param fT Tabla foránea relacionada
    #@param fF Campo foráneo relacionado
    #@param rC Cardinalidad de la relacion
    #@param dC Borrado en cascada, sólo se tiene en cuenta en cardinalidades M1
    #@param uC Actualizaciones en cascada, sólo se tiene en cuenta en cardinalidades M1
    #@param cI Chequeos de integridad sobre la relacion

    def __init__(self, fT, fF, rC, dC, uC, cI):
        self._foreingTable = fT
        self._foreingField = fF
        self._cardinality = rC
        self._deleteCascade = bool(dC)
        self._updateCascade = bool(uC)
        self._checkIntegrity = bool(cI)

    def setField(self, fN):
        self._fienName = fN

    def field(self):
        return self._fieldName

    def foreingTable(self):
        return self._foreingTable

    def foreingField(self):
        return self._foreingField

    def cardinality(self):
        return self._cardinality

    def deleteCascade(self):
        return (self._deleteCascade and self._cardinality == RELATION_M1)

    def updateCascade(self):
        return (self._updateCascade and self._cardinality == RELATION_M1)

    def checkIn(self):
        return self._checkIntegrity
        

