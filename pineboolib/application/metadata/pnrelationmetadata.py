# -*- coding: utf-8 -*-
"""PNRelationMetaData manages relations between tables."""

from pineboolib.core import decorators


class PNRelationMetaData:
    """PNRelationMetaData Class."""

    """
    Constantes de tipos de cardinalidades de una relacion
    """

    RELATION_1M = "1M"
    RELATION_M1 = "M1"

    count_ = 0

    d: "PNRelationMetaDataPrivate"

    def __init__(self, *args, **kwargs) -> None:
        """Initialize the relation."""

        if len(args) == 1:
            self.inicializeFromFLRelationMetaData(args[0])
        else:
            self.inicializeNewFLRelationMetaData(
                args[0], args[1], args[2], args[3], args[4], args[5]
            )

        ++self.count_

    def inicializeNewFLRelationMetaData(
        self, fT: str, fF: str, rC: str, dC: bool = False, uC: bool = False, cI: bool = True
    ) -> None:
        """
        Fill in the relation data.

        @param fT Related foreign table.
        @param fF Related foreign field.
        @param rC Cardinality of the relation.
        @param dC Deleted in cascade, only taken into account in M1 cardinalities.
        @param uC Cascade updates, only taken into account in M1 cardinalities.
        @param cI Integrity checks on the relation.
        """

        self.d = PNRelationMetaDataPrivate(fT, fF, rC, dC, uC, cI)

    @decorators.BetaImplementation
    def inicializeFromFLRelationMetaData(self, other: "PNRelationMetaData"):
        """
        Fill in the data from another relation.

        @param other. original PNRelationMetaData.
        """

        self.d = PNRelationMetaDataPrivate()
        self.copy(other)

    def setField(self, fN: str) -> None:
        """
        Set the name of the related field.

        @param fN Related field name.
        """

        self.d.field_ = fN.lower()

    def field(self) -> str:
        """
        Get in the name of the related field.

        @return Returns the name of the related field
        """

        return self.d.field_

    def foreignTable(self) -> str:
        """
        Get the name of the foreign table.

        @return Returns the name of the database table with which it is related
        """

        return self.d.foreignTable_

    def foreignField(self) -> str:
        """
        Get the name of the foreign field.

        @return Returns the name of the foreign table field with which it is related
        """

        return self.d.foreignField_

    def cardinality(self) -> str:
        """
        Get the cardinality of the relationship.

        @return Returns the cardinality of the relationship, looking from the table where define this object towards the outside
        """

        return self.d.cardinality_

    @decorators.BetaImplementation
    def deleteCascade(self) -> bool:
        """
        Get if the relationship implies cascaded deletions, it is only taken into account in M1 cardinalities.

        @return Returns TRUE if the relationship implies cascaded deletions, FALSE otherwise
        """

        return self.d.deleteCascade_ and self.d.cardinality_ == self.RELATION_M1

    @decorators.BetaImplementation
    def updateCascade(self) -> bool:
        """
        Get if the relationship involves cascade modifications, it is only taken into account in M1 cardinalities.

        @return Returns TRUE if the relationship implies cascading modifications, FALSE otherwise
        """

        return self.d.updateCascade_ and self.d.cardinality_ == self.RELATION_M1

    @decorators.BetaImplementation
    def checkIn(self) -> bool:
        """
        Get if the integrity rules on the relationship should be applied.
        """

        return self.d.checkIn_

    @decorators.BetaImplementation
    def copy(self, other: "PNRelationMetaData") -> None:
        """Copy a PNRelationMetaData to another."""

        if other == self:
            return
        if not isinstance(other, PNRelationMetaData):
            raise ValueError(
                "FLRelationMetaData::copy requires an instance to a PNRelationMetaData class"
            )
        self.d.field_ = other.d.field_
        self.d.foreignTable_ = other.d.foreignTable_
        self.d.foreignField_ = other.d.foreignField_
        self.d.cardinality_ = other.d.cardinality_
        self.d.deleteCascade_ = other.d.deleteCascade_
        self.d.updateCascade_ = other.d.updateCascade_
        self.d.checkIn_ = other.d.checkIn_


class PNRelationMetaDataPrivate:
    """PNRelationMetaDataPrivate Class."""

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
    checkIn_: bool

    def __init__(self, *args, **kwargs) -> None:
        """Initialize the class."""

        if len(args) == 0:
            self.inicializeFLRelationMetaDataPrivate()
        else:
            self.inicializeNewFLRelationMetaDataPrivate(
                args[0], args[1], args[2], args[3], args[4], args[5]
            )

    def inicializeNewFLRelationMetaDataPrivate(
        self, fT: str, fF: str, rC: str, dC: bool, uC: bool, cI: bool
    ) -> None:
        """Fill initial values ​​with given values."""

        self.foreignTable_ = fT.lower()
        self.foreignField_ = fF.lower()
        self.cardinality_ = rC
        self.deleteCascade_ = dC
        self.updateCascade_ = uC
        self.checkIn_ = cI

    @decorators.BetaImplementation
    def inicializeFLRelationMetaDataPrivate(self):
        """Initialize the empty class."""

        return
