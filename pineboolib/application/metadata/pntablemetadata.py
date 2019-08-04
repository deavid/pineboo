# -*- coding: utf-8 -*-
"""
Manage tables used by Pineboo.

Maintains the definition of a table.

This class maintains the definition of
certain characteristics of a base table
of data.

Additionally it can be used for the definition of
the metadata of a query, see FLTableMetaData :: query ().
"""

from pineboolib.core import decorators

from pineboolib.interfaces.itablemetadata import ITableMetaData
from pineboolib import logging
import copy

from typing import Any, Optional, List, Dict, TYPE_CHECKING
from .pnfieldmetadata import PNFieldMetaData
from .pncompoundkeymetadata import PNCompoundKeyMetaData

if TYPE_CHECKING:
    from .pnrelationmetadata import PNRelationMetaData  # noqa


class PNTableMetaData(ITableMetaData):
    """PNTableMetaData Class."""

    logger = logging.getLogger("CursorTableModel")
    d: "PNTableMetaDataPrivate"

    def __init__(self, n, a=None, q: str = None) -> None:
        """
        Collect the data to start.

        @param n Name of the table to define
        @param a Alias ​​of the table, used in forms
        @param q (Optional) Name of the query from which you define your metadata
        """

        super().__init__(n, a, q)
        # tmp = None

        if not a and not q:
            if isinstance(n, str):
                # print("FLTableMetaData(%s).init()" % args[0])
                self.inicializeFLTableMetaDataP(n)
            else:
                self.inicializeFLTableMetaData(n)
        else:
            self.inicializeNewFLTableMetaData(n, a, q)

    def inicializeFLTableMetaData(self, other: "PNTableMetaData") -> None:
        """
        Initialize the data from another PNTableMetaData.
        """

        self.d = PNTableMetaDataPrivate()
        self.d.fieldNames_ = []
        self.copy(other)

    def inicializeNewFLTableMetaData(self, n, a, q: str = None) -> None:
        """
        Initialize the data with the basic information.

        @param n Name of the table to define
        @param a Alias ​​of the table, used in forms
        @param q (Optional) Name of the query from which you define your metadata

        """
        self.d = PNTableMetaDataPrivate(n, a, q)
        self.d.fieldNames_ = []

    def inicializeFLTableMetaDataP(self, name: str) -> None:
        """
        Initialize the private part, without data. Just specify the name.
        """

        self.d = PNTableMetaDataPrivate(name)

        self.d.compoundKey_ = PNCompoundKeyMetaData()
        self.d.fieldNames_ = []

        """
        try:
            table = self._prj.tables[name]
        except:
            return None

        for field in table.fields:
            field.setMetadata(self)
            if field.isCompoundKey():
                self.d.compoundKey_.addFieldMD(field)
            if field.isPrimaryKey():
                self.d.primaryKey_ = field.name()

            self.d.fieldList_.append(field)
            self.d.fieldNames_.append(field.name())

            if field.type() == FLFieldMetaData.Unlock:
                self.d.fieldNamesUnlock_.append(field.name())
        """

    def name(self) -> str:
        """
        Get the name of the table.

        @return The name of the table described
        """

        return self.d.name_

    def setName(self, n: str) -> None:
        """
        Set the name of the table.

        @param n Table name
        """

        # QObject::setName(n);
        self.d.name_ = n

    def setAlias(self, a: str) -> None:
        """
        Set the alias.

        @param a Alias
        """

        self.d.alias_ = a

    def setQuery(self, q: str) -> None:
        """
        Set the name of the query.

        @param q Query name
        """

        self.d.query_ = q

    def alias(self) -> str:
        """
        Get the alias associated with the table.

        @return Alias.
        """

        return self.d.alias_

    def query(self) -> str:
        """
        Get the name of the query from which it defines its metadata.

        The name will correspond to the definition of a query by
        (.qry file). If the name of the query is defined then
        the name of the table will correspond to the main table of the query
        when referring to several tables.
        """

        return self.d.query_

    def isQuery(self) -> bool:
        """
        Get if you define the metadata of a query.
        """

        return True if self.d.query_ else False

    def addFieldMD(self, f: "PNFieldMetaData") -> None:
        """
        Add the description of a field to the list of field descriptions.

        @param f FLFieldMetaData object with the description of the field to add
        """

        # if f is None:
        #     return
        if not f.metadata():
            f.setMetadata(self)
        self.d.fieldList_.append(f)
        self.d.addFieldName(f.name())
        self.d.formatAlias(f)

        if f.type() == PNFieldMetaData.Unlock:
            self.d.fieldNamesUnlock_.append(f.name())
        if f.d.isPrimaryKey_:
            self.d.primaryKey_ = f.name().lower()

    def removeFieldMD(self, fN: str) -> None:
        """
        Remove the description of a field from the list of field descriptions.

        @param fN Name of the field to be deleted
        """

        # if fN is None:
        #     return
        # FIXME: FLFieldMetaData does not have .clear()
        # for key in self.d.fieldList_:
        #     if key.name().lower() == fN.lower():
        #         key.clear()
        self.d.removeFieldName(fN)

    def setCompoundKey(self, cK: Optional[PNCompoundKeyMetaData]) -> None:
        """
        Set the composite key of this table.

        @param cK FLCompoundKey object with the description of the composite key
        """

        self.d.compoundKey_ = cK

    def primaryKey(self, prefixTable=False) -> str:
        """
        Get the name of the field that is the primary key for this table.

        @param prefixTable If TRUE, a prefix with the name of the table is added; tablename.fieldname
        """

        if not self.d.primaryKey_:
            raise Exception("No primaryKey")

        if "." in self.d.primaryKey_:
            return self.d.primaryKey_

        if prefixTable:
            return str("%s.%s" % (self.d.name_, self.d.primaryKey_))
        else:
            return str(self.d.primaryKey_)

    def fieldNameToAlias(self, fN: str) -> str:
        """
        Get the alias of a field from its name.

        @param fN Field name
        """

        if not fN:
            return fN

        for key in self.d.fieldList_:
            if key.name().lower() == fN.lower():
                return key.alias()

        return fN

    def fieldAliasToName(self, aN: str) -> Optional[str]:
        """
        Get the name of a field from its alias.

        @param aN Field alias name
        """

        if not aN:
            return aN

        for key in self.d.fieldList_:
            if key.alias().lower() == aN.lower():
                return key.name()

        return None

    def fieldType(self, fN: str) -> Optional[int]:
        """
        Get the type of a field from its name.

        @param fN Field name
        """

        if not fN:
            return None
        fN = str(fN)
        type_ = None
        for f in self.d.fieldList_:
            if f.name() == fN.lower():
                type_ = f.type()
                break

        ret_ = None
        if type_ is not None:
            if type_ in ("string", "counter"):
                ret_ = 3
            elif type_ == "stringlist":
                ret_ = 4
            elif type_ == "uint":
                ret_ = 17
            elif type_ == "bool":
                ret_ = 18
            elif type_ == "double":
                ret_ = 19
            elif type_ == "date":
                ret_ = 26
            elif type_ == "time":
                ret_ = 27
            elif type_ == "serial":
                ret_ = 100
            elif type_ == "unlock":
                ret_ = 200
            elif type_ == "check":
                ret_ = 300
            else:
                # FIXME: Falta stringlist e int
                self.logger.warning(
                    "FIXME:: No hay definido un valor numérico para el tipo %s", type_
                )

        return ret_

    def fieldIsPrimaryKey(self, fN: str) -> Optional[bool]:
        """
        Get if a field is the primary key from its name.

        @param fN Field name.
        """

        if not fN:
            return None
        fN = str(fN)
        for f in self.d.fieldList_:
            if f.name() == fN.lower():
                return f.isPrimaryKey()

        return None

    def fieldIsIndex(self, field_name: str) -> int:
        """
        Get if a field is index based on its name.

        @param fN Field name.
        """

        if field_name in self.fieldNames():
            return self.fieldNames().index(field_name)

        self.logger.warning("FLTableMetaData.fieldIsIndex(%s) No encontrado", field_name)
        return -1

    def fieldIsCounter(self, fN: str) -> Optional[bool]:
        """
        Get if a field is a counter.

        @param fN Field name.
        @author Andrés Otón Urbano (baxas@eresmas.com)
        """

        if not fN:
            return False

        field = None

        for f in self.d.fieldList_:
            if f.name() == fN.lower():
                field = f
                break

        if field:
            return field.d.contador_

        return False

    def fieldAllowNull(self, fN: str) -> Optional[bool]:
        """
        Get if a field can be null.

        @param fN Field name
        """

        if not fN:
            return False

        for f in self.d.fieldList_:
            if f.name() == fN.lower():
                return f.allowNull()

        return False

    def fieldIsUnique(self, fN: str) -> Optional[bool]:
        """
        Get if a field is unique from its name.

        @param fN Field name.
        """

        if not fN:
            return False

        for f in self.d.fieldList_:
            if f.name() == fN.lower():
                return f.isUnique()

        return False

    def fieldTableM1(self, fN: str) -> Optional[str]:
        """
        Get the name of the foreign table related to a field in this table by an M1 relationship (many to one).

        @param fN Field of the relation M1 of this table, which is supposed to be related
            with another field from another table.
        @return The name of the related table M1, if there is a relationship for the field, or a string
            empty without the field is not related.
        """

        if not fN:
            return None

        field = None

        for f in self.fieldList():
            if f.name() == fN.lower():
                field = f
                break

        if field and field.d.relationM1_:
            return field.d.relationM1_.foreignTable()

        return None

    def fieldForeignFieldM1(self, fN: str) -> Optional[str]:
        """
        Get the name of the foreign table field related to the one indicated by an M1 relationship (many still).

        @param fN Field of the relation M1 of this table, which is supposed to be related
            with another field from another table.
        @return The name of the foreign field related to the indicated.
        """

        if not fN:
            return None

        field = None

        for f in self.fieldList():
            if f.name() == fN.lower():
                field = f
                break

        if field and field.d.relationM1_:
            return field.d.relationM1_.foreignField()

        return None

    def relation(self, fN: str, fFN: str, fTN: str) -> Optional["PNRelationMetaData"]:
        """
        Get the relationship object that defines two fields.

        @param fN Field name of this table that is part of the relationship.
        @param fFN Name of the foreign field to this table that is part of the relationship.
        @param fTN Name of the foreign table.
        @return Returns a FLRelationMetaData object with the relationship information, provided
            when it exists If it does not exist, it returns False.
        """

        if not fN:
            return None

        field = None

        for f in self.fieldList():
            if f.name() == fN.lower():
                field = f
                break

        if field:
            if (
                field.d.relationM1_
                and field.d.relationM1_.foreignField() == str(fFN).lower()
                and field.d.relationM1_.foreignTable() == str(fTN).lower()
            ):
                return field.d.relationM1_

            relationList = field.d.relationList_

            if relationList:
                for itR in relationList:
                    if (
                        itR.foreignField() == str(fFN).lower()
                        and itR.foreignTable() == str(fTN).lower()
                    ):
                        return itR

        return None

    def fieldLength(self, fN: str) -> Optional[int]:
        """
        Get the length of a field from its name.

        @param fN Field name.
        @return field length.
        """

        if not fN:
            return None

        for f in self.fieldList():
            if f.name() == fN.lower():
                return f.length()

        return None

    def fieldPartInteger(self, fN: str) -> Optional[int]:
        """
        Get the number of digits of the entire part of a field from its name.

        @param fN Field name.
        @return integer length.
        """

        if not fN:
            return None

        for f in self.fieldList():
            if f.name() == fN.lower():
                return f.partInteger()

        return None

    def fieldPartDecimal(self, fN: str) -> Optional[int]:
        """
        Get the number of digits of the decimal part of a field from its name.

        @param fN Field name.
        @return part decimal length.
        """

        if not fN:
            return None

        for f in self.fieldList():
            if f.name() == fN.lower():
                return f.partDecimal()

        return None

    def fieldCalculated(self, fN: str) -> Optional[int]:
        """
        Get if a field is calculated.

        @param fN Field name.
        """

        if not fN:
            return None

        for f in self.fieldList():
            if f.name() == fN.lower():
                return f.calculated()

        return None

    def fieldVisible(self, fN: str) -> None:
        """
        Get if a field is visible.

        @param fN Field name.
        """

        if not fN:
            return

        for f in self.fieldList():
            if f.name() == fN.lower():
                return f.visible()

        return

    def field(self, fN: str) -> Optional["PNFieldMetaData"]:
        """
        Get the metadata of a field.

        @param fN Field name.
        @return A FLFieldMetaData object with the information or metadata of a given field.
        """

        if not fN:
            return None

        for f in self.d.fieldList_:
            if f.name() == fN.lower():
                return f

        return None

    def fieldList(self) -> List[Any]:
        """
        Return a list of field definitions.

        @return Object with the table field deficits list
        """

        return self.d.fieldList_

    def fieldListArray(self, prefix_table: bool = False) -> List[str]:
        """
        To get a string with the names of the fields separated by commas.

        @param prefix_table If TRUE a prefix is ​​added to each field with the name of the table; tablename.fieldname
        @return String with the names of the fields separated by commas.
        """

        listado = []
        cadena = "%s." % self.name() if prefix_table else ""

        for field in self.d.fieldList_:
            listado.append("%s%s" % (cadena, field.name()))

        return listado

    # def fieldListObject(self):
    #    #print("FiledList count", len(self.d.fieldList_))
    #    return self.d.fieldList_

    def indexPos(self, field_name: str) -> int:
        """
        Return the position of a field in the real order.

        @param field_name. Field Name.
        @return position index or None.
        """

        return self.fieldIsIndex(field_name)

    def fieldListOfCompoundKey(self, fN: str) -> Optional[List[PNFieldMetaData]]:
        """
        Get the list of fields of a compound key, from the name of a field that you want to find out if it is in that compound key.

        @param fN Name of the field you want to find out if it belongs to a compound key.
        @return If the field belongs to a composite key, it returns the list of fields
          that form said composite key, including the consulted field. If
          that the consulted field does not belong to any compound key returns None
        """

        if self.d.compoundKey_:
            if self.d.compoundKey_.hasField(fN):
                return self.d.compoundKey_.fieldList()
        return None

    def fieldNames(self) -> List[str]:
        """
        Get a list of texts containing the names of fields separated by commas.

        The order of the fields from left to right corresponds to the order in which
        have been added with the addFieldMD () or addFieldName () method

        @return field name list.
        """

        return self.d.fieldNames_

    def fieldNamesUnlock(self) -> List[str]:
        """
        List of field names in the table that are of type PNFieldMetaData :: Unlock.

        @return field name list.
        """

        return self.d.fieldNamesUnlock_

    def concurWarn(self) -> bool:
        """
        Return concurWarn flag.

        @return True or False
        """

        return self.d.concurWarn_

    def setConcurWarn(self, b=True) -> None:
        """
        Enable concurWarn flag.

        @param b. True or False.
        """

        self.d.concurWarn_ = b

    @decorators.BetaImplementation
    def detectLocks(self) -> bool:
        """
        Return lock detection flag.

        @return b. True or False.
        """

        return self.d.detectLocks_

    def setDetectLocks(self, b=True) -> None:
        """
        Enable lock detection flag.

        @return b. True or False.
        """

        self.d.detectLocks_ = b

    def FTSFunction(self) -> str:
        """
        Return function name to call for Full Text Search.

        @return function name or None.
        """

        return self.d.ftsfun_

    def setFTSFunction(self, ftsfun: str) -> None:
        """
        Set the function name to call for Full Text Search.

        @param ftsfun. function name.
        """

        self.d.ftsfun_ = ftsfun

    def inCache(self) -> bool:
        """
        Return if the metadata is cached (FLManager :: cacheMetaData_).

        @return True or False.
        """

        return self.d.inCache_ if self.d else False

    def setInCache(self, b=True) -> None:
        """
        Set the metadata is cached (FLManager :: cacheMetaData_).

        @return True or False.
        """

        self.d.inCache_ = b

    def copy(self, other: "PNTableMetaData") -> None:
        """
        Copy the values ​​of a PNFieldMetaData from another.

        @param other. PNTableMetaData.
        """

        if other == self:
            return

        self.d = copy.copy(other.d)

    def indexFieldObject(self, position: int) -> "PNFieldMetaData":
        """
        Return the PNFieldMetaData of the given field.

        @param i. Position.
        @return PNfieldMetadata.
        """

        return self.d.fieldList_[position]


class PNTableMetaDataPrivate:
    """PNTableMetaData Class."""

    """
    Nombre de la tabla
    """

    name_: str

    """
    Alias de la tabla
    """
    alias_: str

    """
    Lista de campos que tiene esta tabla
    """
    fieldList_: List["PNFieldMetaData"]

    """
    Clave compuesta que tiene esta tabla
    """
    compoundKey_: Optional[PNCompoundKeyMetaData] = None

    """
    Nombre de la consulta (fichero .qry) de la que define los metadatos
    """
    query_: str

    """
    Cadena de texto con los nombre de los campos separados por comas
    """
    fieldNames_: List[str] = []

    """
    Mapas alias<->nombre
    """
    aliasFieldMap_: Dict[str, str]
    fieldAliasMap_: Dict[str, str]

    """
    Lista de nombres de campos de la tabla que son del tipo FLFieldMetaData::Unlock
    """
    fieldNamesUnlock_: List[str] = []

    """
    Clave primaria
    """
    primaryKey_: Optional[str]

    """
    Indica si se debe avisar de colisión de concurrencia entre sesiones.

    Si este flag es true y dos o mas sesiones/usuarios están modificando los
    mismos campos,al validar un formulario (FLFormRecordDB::validateForm)
    mostrará un aviso de advertencia.

    Ver también FLSqlCursor::concurrencyFields().
    """
    concurWarn_: bool

    """
    Indica si se deben comprobar riesgos de bloqueos para esta tabla

    Si este flag es true FLSqlCursor::commitBuffer() chequeará siempre
    los riesgos de bloqueo para esta tabla.

    Ver también FLSqlDatabase::detectRisksLocks
    """
    detectLocks_: bool

    """
    Indica el nombre de función a llamar para la búsqueda con Full Text Search
    """
    ftsfun_: str

    """
    Indica si lo metadatos están en caché (FLManager::cacheMetaData_)
    """
    inCache_: bool

    count_ = 0

    def __init__(self, n: str = None, a=None, q: str = None) -> None:
        """
        Initialize the class.

        @param n metadata name.
        @param a metadata alias.
        @param q query string.
        """

        self.fieldList_ = []
        self.fieldNamesUnlock_ = []
        self.aliasFieldMap_ = {}
        self.fieldAliasMap_ = {}
        self.query_ = ""
        # print("Vaciando field list ahora",  len(self.fieldList_))
        if n is None:
            self.inicializeFLTableMetaDataPrivate()
        elif n and not a and not q:
            self.inicializeFLTableMetaDataPrivateS(n)
        else:
            self.inicializeNewFLTableMetaDataPrivate(n, a, q)
        self.count_ = self.count_ + 1

    def inicializeFLTableMetaDataPrivate(self) -> None:
        """
        Initialize class ends with empty data.
        """

        self.compoundKey_ = None
        self.inCache = False

    def inicializeNewFLTableMetaDataPrivate(self, n: str, a, q: str = None) -> None:
        """
        Initialize the class end with data.

        @param n metadata name.
        @param a metadata alias.
        @param q query string.
        """

        self.name_ = n.lower()
        self.alias_ = a
        self.compoundKey_ = None
        if q is not None:
            self.query_ = q
        self.concurWarn_ = False
        self.detectLocks_ = False
        self.inCache_ = False

    def inicializeFLTableMetaDataPrivateS(self, name) -> None:
        """
        Initialize the class end with basic data.

        @param name metadata name.
        """

        self.name_ = str(name)
        self.alias_ = self.name_

    def addFieldName(self, n: str) -> None:
        """
        Add the name of a field to the field name string, see fieldNames().

        @param n Field Name.
        """

        self.fieldNames_.append(n.lower())

    def removeFieldName(self, n: str) -> None:
        """
        Remove the name of a field from the field name string, see fieldNames().

        @param n Field Name
        """

        if self.fieldNames_:
            self.fieldNames_.remove(n)

    def formatAlias(self, f=None) -> None:
        """
        Format the alias of the indicated field to avoid duplicates.

        @param f Object field whose alias you want to format
        """

        if f is None:
            return

        alias = f.alias()
        field = f.name().lower()

        for aliasF in self.aliasFieldMap_:
            if aliasF == alias:
                alias = "%s(%s)" % (alias, str(len(self.aliasFieldMap_) + 1))
                break

        f.d.alias_ = alias

        self.aliasFieldMap_[alias] = field
        self.fieldAliasMap_[field] = alias

    def clearFieldList(self) -> None:
        """
        Clear the list of field definitions.
        """

        self.fieldList_ = []
        self.fieldNames_ = []
