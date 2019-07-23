# -*- coding: utf-8 -*-

# Completada Si
from pineboolib.core import decorators


class PNRelationMetaData:

    """
    Constantes de tipos de cardinalidades de una relacion
    """

    RELATION_1M = "1M"
    RELATION_M1 = "M1"

    count_ = 0

    d: "PNRelationMetaDataPrivate"

    def __init__(self, *args, **kwargs) -> None:
        if len(args) == 1:
            self.inicializeFromFLRelationMetaData(args[0])
        else:
            self.inicializeNewFLRelationMetaData(args[0], args[1], args[2], args[3], args[4], args[5])

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

    def inicializeNewFLRelationMetaData(self, fT: str, fF: str, rC: str, dC: bool = False, uC: bool = False, cI: bool = True) -> None:
        self.d = PNRelationMetaDataPrivate(fT, fF, rC, dC, uC, cI)

    @decorators.BetaImplementation
    def inicializeFromFLRelationMetaData(self, *other):
        self.d = PNRelationMetaDataPrivate()
        self.copy(other)

    """
    Establece el nombre del campo relacionado.

    @param fN Nombre del campo relacionado
    """

    def setField(self, fN: str) -> None:
        self.d.field_ = fN.lower()

    """
    Obtiene en el nombre del campo de la relacion.

    @return Devuelve el nombre del campo relacionado
    """

    def field(self) -> str:
        return self.d.field_

    """
    Obtiene el nombre de la tabla foránea.

    @return Devuelve el nombre de la tabla de la base de datos con la que se está relacionada
    """

    def foreignTable(self) -> str:
        return self.d.foreignTable_

    """
    Obtiene el nombre de la campo foráneo.

    @return Devuelve el nombre del campo de la tabla foránea con la que está relacionada
    """

    def foreignField(self) -> str:
        return self.d.foreignField_

    """
    Obtiene la cardinalidad de la relacion.

    @return Devuelve la cardinalidad de la relacion, mirando desde la tabla donde se
        define este objeto hacia la foránea
    """

    def cardinality(self) -> str:
        return self.d.cardinality_

    """
    Obtiene si la relación implica borrados en cascada, sólo se tiene en cuenta en cardinalidades M1.

    @return Devuelve TRUE si la relacion implica borrados en cascada, FALSE en caso contrario
    """

    @decorators.BetaImplementation
    def deleteCascade(self):
        return self.d.deleteCascade_ and self.d.cardinality_ == self.RELATION_M1

    """
    Obtiene si la relación implica modificaciones en cascada, sólo se tiene en cuenta en cardinalidades M1.

    @return Devuelve TRUE si la relacion implica modificaciones en cascada, FALSE en caso contrario
    """

    @decorators.BetaImplementation
    def updateCascade(self):
        return self.d.updateCascade_ and self.d.cardinality_ == self.RELATION_M1

    """
    Obtiene si se deben aplicar la reglas de integridad sobre la relación
    """

    @decorators.BetaImplementation
    def checkIn(self):
        return self.d.checkIn_

    @decorators.BetaImplementation
    def copy(self, other):
        if other == self:
            return
        if not isinstance(other, PNRelationMetaData):
            raise ValueError("FLRelationMetaData::copy requires an instance to a PNRelationMetaData class")
        self.d.field_ = other.d.field_
        self.d.foreignTable_ = other.d.foreignTable_
        self.d.foreignField_ = other.d.foreignField_
        self.d.cardinality_ = other.d.cardinality_
        self.d.deleteCascade_ = other.d.deleteCascade_
        self.d.updateCascade_ = other.d.updateCascade_
        self.d.checkIn_ = other.d.checkIn_


class PNRelationMetaDataPrivate:

    """
    Nombre del campo a relacionar
    """

    field_: str

    """
    Nombre de la tabla foránea a relacionar
    """
    foreignTable_: str

    """
    Nombre del campo foráneo relacionado
    """
    foreignField_: str

    """
    Cardinalidad de la relación
    """
    cardinality_: str

    """
    Indica si los borrados serán en cascada, en relaciones M1
    """
    deleteCascade_: bool

    """
    Indica si las modificaciones serán en cascada, en relaciones M1
    """
    updateCascade_: bool

    """
    Indica si se deben aplicar la reglas de integridad en esta relación
    """
    checkIn_ = None

    def __init__(self, *args, **kwargs) -> None:
        if len(args) == 0:
            self.inicializeFLRelationMetaDataPrivate()
        else:
            self.inicializeNewFLRelationMetaDataPrivate(args[0], args[1], args[2], args[3], args[4], args[5])

    def inicializeNewFLRelationMetaDataPrivate(self, fT: str, fF: str, rC: str, dC: bool, uC: bool, cI: bool) -> None:
        self.foreignTable_ = fT.lower()
        self.foreignField_ = fF.lower()
        self.cardinality_ = rC
        self.deleteCascade_ = dC
        self.updateCascade_ = uC
        self.checkIn_ = cI

    @decorators.BetaImplementation
    def inicializeFLRelationMetaDataPrivate(self):
        return
