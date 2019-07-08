# -*- coding: utf-8 -*-
from pineboolib.core import decorators

from pineboolib.fllegacy.flfieldmetadata import FLFieldMetaData
from pineboolib.fllegacy.flcompoundkey import FLCompoundKey
from pineboolib import logging
import copy
import protocols
from typing import Any, Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from pineboolib.fllegacy import flfieldmetadata

"""
Mantiene la definicion de una tabla.

Esta clase mantienen la definicion de
ciertas caracteristicas de una tabla de la base
de datos.

Adicionalmente puede ser utilizada para la definición de
los metadatos de una consulta, ver FLTableMetaData::query().

@author InfoSiAL S.L.
"""


class FLTableMetaData(object):
    logger = logging.getLogger("CursorTableModel")
    d = None

    """
    constructor

    @param n Nombre de la tabla a definir
    @param a Alias de la tabla, utilizado en formularios
    @param q (Opcional) Nombre de la consulta de la que define sus metadatos
    """

    def __init__(self, n, a=None, q=None) -> None:
        super(FLTableMetaData, self).__init__()
        # tmp = None

        if not a and not q:
            if isinstance(n, str):
                # print("FLTableMetaData(%s).init()" % args[0])
                self.inicializeFLTableMetaDataP(n)
            else:
                self.inicializeFLTableMetaData(n)
        else:
            self.inicializeNewFLTableMetaData(n, a, q)

    def inicializeFLTableMetaData(self, other) -> None:
        self.d = FLTableMetaDataPrivate()
        self.d.fieldNames_ = []
        self.copy(other)

    def inicializeNewFLTableMetaData(self, n, a, q=None) -> None:
        self.d = FLTableMetaDataPrivate(n, a, q)
        self.d.fieldNames_ = []

    def inicializeFLTableMetaDataP(self, name) -> None:
        self.d = FLTableMetaDataPrivate(name)
        self.d.compoundKey_ = FLCompoundKey()
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

    """
    destructor
    """

    def __del__(self) -> None:
        self.d = None

    """
    Obtiene el nombre de la tabla

    @return El nombre de la tabla que se describe
    """

    def name(self) -> Any:
        return self.d.name_

    """
    Establece el nombre de la tabla

    @param n Nombre de la tabla
    """

    def setName(self, n) -> None:
        # QObject::setName(n);
        self.d.name_ = n

    """
    Establece el alias

    @param a Alias
    """

    def setAlias(self, a) -> None:
        self.d.alias_ = a

    """
    Establece el nombre de la consulta

    @param q Nombre de la consulta
    """

    def setQuery(self, q) -> None:
        self.d.query_ = q

    """
    Obtiene el alias asociado a la tabla
    """

    def alias(self) -> Any:
        return self.d.alias_

    """
    Obtiene el nombre de la consulta de la que define sus metadatos.

    El nombre corresponderá a la definición de una consulta mediante
    (fichero .qry). Si el nombre de la consulta está definido entonces
    el nombre de la tabla correponderá a la tabla principal de la consulta
    cuando esta referencie a varias tablas.
    """

    def query(self) -> Any:
        return self.d.query_

    """
    Obtiene si define los metadatos de una consulta
    """

    def isQuery(self) -> bool:
        return True if self.d.query_ else False

    """
    Añade la descripción de un campo a lista de descripciones de campos.

    @param f Objeto FLFieldMetaData con la descripción del campo a añadir
    """

    def addFieldMD(self, f: "flfieldmetadata.FLFieldMetaData") -> None:
        if f is None:
            return
        if not f.metadata():
            f.setMetadata(self)
        self.d.fieldList_.append(f)
        self.d.addFieldName(f.name())
        self.d.formatAlias(f)
        if f.type() == FLFieldMetaData.Unlock:
            self.d.fieldNamesUnlock_.append(f.name())
        if f.d.isPrimaryKey_:
            self.d.primaryKey_ = f.name().lower()

    """
    Elimina la descripción de un campo de la lista de descripciones de campos.

    @param fN Nombre del campo a eliminar
    """

    def removeFieldMD(self, fN: protocols.SupportsLower) -> None:
        if fN is None:
            return

        self.d.fieldList_[fN.lower()].clear()
        self.d.removeFieldName(fN)

    """
    Establece la clave compuesta de esta tabla.

    @param cK Objeto FLCompoundKey con la descripción de la clave compuesta
    """

    def setCompoundKey(self, cK) -> None:
        self.d.compoundKey_ = cK

    """
    Obtiene el nombre del campo que es clave primaria para esta tabla.

    @param prefixTable Si es TRUE se añade un prefijo con el nombre de la tabla; nombretabla.nombrecampo
    """

    def primaryKey(self, prefixTable=False) -> Any:
        if not self.d.primaryKey_:
            return None

        if "." in self.d.primaryKey_:
            return self.d.primaryKey_

        if prefixTable:
            return str("%s.%s" % (self.d.name_, self.d.primaryKey_))
        else:
            return str(self.d.primaryKey_)

    """
    Obtiene el alias de un campo a partir de su nombre.

    @param fN Nombre del campo
    """

    def fieldNameToAlias(self, fN: protocols.SupportsLower) -> Any:

        if not fN:
            return fN

        for key in self.d.fieldList_:
            if key.name().lower() == fN.lower():
                return key.alias()

        return None

    """
    Obtiene el nombre de un campo a partir de su alias.

    @param aN Nombre del alias del campo
    """

    def fieldAliasToName(self, aN: protocols.SupportsLower) -> Any:

        if not aN:
            return aN

        for key in self.d.fieldList_:
            if key.alias().lower() == aN.lower():
                return key.name()

        return None

    """
    Obtiene el tipo de un campo a partir de su nombre.

    @param fN Nombre del campo
    """

    def fieldType(self, fN) -> Optional[int]:
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
                self.logger.warning("FIXME:: No hay definido un valor numérico para el tipo %s", type_)

        return ret_

    """
    Obtiene si un campo es clave primaria partir de su nombre.

    @param fN Nombre del campo
    """

    def fieldIsPrimaryKey(self, fN) -> Any:
        if not fN:
            return None
        fN = str(fN)
        for f in self.d.fieldList_:
            if f.name() == fN.lower():
                return f.pK()

        return None

    """
    Obtiene si un campo es índice a partir de su nombre.

    @param fN Nombre del campo
    """

    def fieldIsIndex(self, field_name=None) -> Any:

        if field_name in self.fieldNames():
            return self.fieldNames().index(field_name)

        self.logger.warning("FLTableMetaData.fieldIsIndex(%s) No encontrado", field_name)
        return None

    """
    Obtiene si un campo es contador.

    @param fN Nombre del campo
    @author Andrés Otón Urbano (baxas@eresmas.com)
    """

    def fieldIsCounter(self, fN: protocols.SupportsLower) -> Any:
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

    def fieldAllowNull(self, fN: protocols.SupportsLower) -> Any:
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

    def fieldIsUnique(self, fN: protocols.SupportsLower) -> Any:
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

    def fieldTableM1(self, fN: protocols.SupportsLower) -> Any:
        if not fN:
            return False

        field = None

        for f in self.fieldList():
            if f.name() == fN.lower():
                field = f
                break

        if field and field.d.relationM1_:
            return field.d.relationM1_.foreignTable()

        return None

    """
    Obtiene el nombre del campo de la tabla foránea relacionado con el indicado mediante
    una relacion M1 (muchos auno).

    @param fN Campo de la relacion M1 de esta tabla, que se supone que esta relacionado
        con otro campo de otra tabla
    @return El nombre del campo foráneo relacionado con el indicado
    """

    def fieldForeignFieldM1(self, fN: protocols.SupportsLower) -> Any:
        if not fN:
            return False

        field = None

        for f in self.fieldList():
            if f.name() == fN.lower():
                field = f
                break

        if field and field.d.relationM1_:
            return field.d.relationM1_.foreignField()

        return None

    """
    Obtiene el objeto relación que definen dos campos.

    @param fN Nombre del campo de esta tabla que forma parte de la relación
    @param fFN Nombre del campo foráneo a esta tabla que forma parte de la relación
    @param  fTN Nombre de la tabla foránea
    @return Devuelve un objeto FLRelationMetaData con la información de la relación, siempre y
      cuando esta exista. Si no existe devuelve False
    """

    def relation(self, fN: protocols.SupportsLower, fFN, fTN) -> Any:
        if not fN:
            return False

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
                    if itR.foreignField() == str(fFN).lower() and itR.foreignTable() == str(fTN).lower():
                        return itR

            return False

    """
    Obtiene la longitud de un campo a partir de su nombre.

    @param fN Nombre del campo
    """

    def fieldLength(self, fN: protocols.SupportsLower) -> Any:
        if not fN:
            return

        for f in self.fieldList():
            if f.name() == fN.lower():
                return f.length()

        return

    """
    Obtiene el número de dígitos de la parte entera de un campo a partir de su nombre.

    @param fN Nombre del campo
    """

    def fieldPartInteger(self, fN: protocols.SupportsLower) -> Any:
        if not fN:
            return

        for f in self.fieldList():
            if f.name() == fN.lower():
                return f.partInteger()

        return

    """
    Obtiene el número de dígitos de la parte decimal de un campo a partir de su nombre.

    @param fN Nombre del campo
    """

    def fieldPartDecimal(self, fN: protocols.SupportsLower) -> Any:
        if not fN:
            return

        for f in self.fieldList():
            if f.name() == fN.lower():
                return f.partDecimal()

        return

    """
    Obtiene si un campo es calculado.

    @param fN Nombre del campo
    """

    def fieldCalculated(self, fN: protocols.SupportsLower) -> Any:
        if not fN:
            return

        for f in self.fieldList():
            if f.name() == fN.lower():
                return f.calculated()

        return

    """
    Obtiene si un campo es visible.

    @param fN Nombre del campo
    """

    def fieldVisible(self, fN: protocols.SupportsLower) -> None:

        if not fN:
            return

        for f in self.fieldList():
            if f.name() == fN.lower():
                f.visible()

        return

    """ Obtiene los metadatos de un campo.

    @param fN Nombre del campo
    @return Un objeto FLFieldMetaData con lainformación o metadatos de un campo dado
    """

    def field(self, fN: protocols.SupportsLower) -> Any:
        if not fN:
            return

        for f in self.d.fieldList_:
            if f.name() == fN.lower():
                return f

        return None

    """
    Para obtener la lista de definiciones de campos.

    @return Objeto con la lista de deficiones de campos de la tabla
    """

    """
    Para obtener una cadena con los nombres de los campos separados por comas.

    @param prefixTable Si es TRUE se añade un prefijo a cada campo con el nombre de la tabla; nombretabla.nombrecampo
    @return Cadena de caracteres con los nombres de los campos separados por comas
    """

    def fieldList(self) -> Any:
        return self.d.fieldList_

    def fieldListArray(self, prefix_table=False) -> List[str]:
        listado = []
        cadena = "%s." % self.name() if prefix_table else ""

        for field in self.d.fieldList_:
            listado.append("%s%s" % (cadena, field.name()))

        return listado

    # def fieldListObject(self):
    #    #print("FiledList count", len(self.d.fieldList_))
    #    return self.d.fieldList_

    def indexPos(self, field_name=None) -> Any:
        return self.fieldIsIndex(field_name)

    """
    Obtiene la lista de campos de una clave compuesta, a partir del nombre de
    un campo del que se quiere averiguar si está en esa clave compuesta.

    @param fN Nombre del campo del que se quiere averiguar si pertenece a una clave compuesta.
    @return Si el campo pertenece a una clave compuesta, devuelve la lista de campos
      que forman dicha clave compuesta, incluido el campo consultado. En el caso
      que el campo consultado no pertenezca a ninguna clave compuesta devuelve 0
    """

    def fieldListOfCompoundKey(self, fN) -> Any:
        if self.d.compoundKey_:
            if self.d.compoundKey_.hasField(fN):
                return self.d.compoundKey_.fieldList()
        return None

    """
    Obtiene una lista de textos que contiene los nombres de los campos separados por comas.

    El orden de los campos de izquierda a derecha es el correspondiente al orden en que
    se han añadido con el método addFieldMD() o addFieldName()
    """

    def fieldNames(self) -> Any:
        return self.d.fieldNames_

    """
    Lista de nombres de campos de la tabla que son del tipo FLFieldMetaData::Unlock
    """

    def fieldNamesUnlock(self) -> Any:
        return self.d.fieldNamesUnlock_

    """
    @return El indicador FLTableMetaData::concurWarn_
    """

    def concurWarn(self) -> Any:
        return self.d.concurWarn_

    """
    Establece el indicador FLTableMetaData::concurWarn_
    """

    def setConcurWarn(self, b=True) -> None:
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

    def setDetectLocks(self, b=True) -> None:
        self.d.detectLocks_ = b

    """
    Establece el nombre de función a llamar para Full Text Search
    """

    def FTSFunction(self) -> Any:
        return self.d.ftsfun_

    def setFTSFunction(self, ftsfun) -> None:
        self.d.ftsfun_ = ftsfun

    """
    Indica si lo metadatos están en caché (FLManager::cacheMetaData_)
    """

    def inCache(self) -> Any:
        return self.d and self.d.inCache_

    """
    Establece si lo metadatos están en caché (FLManager::cacheMetaData_)
    """

    def setInCache(self, b=True) -> None:
        self.d.inCache_ = b

    def copy(self, other) -> None:
        if other == self:
            return

        self.d = copy.copy(other.d)

    def indexFieldObject(self, position, show_exception=True) -> Any:
        i = 0
        ret = None
        for field in self.d.fieldList_:
            if position == i:
                ret = field
                break

            i += 1

        if ret is None and show_exception:
            self.logger.warning("FLTableMetadata(%s).indexFieldObject() Posicion %s no encontrado", self.name(), position)
        return ret


class FLTableMetaDataPrivate:

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
    fieldList_ = None

    """
    Clave compuesta que tiene esta tabla
    """
    compoundKey_ = None

    """
    Nombre de la consulta (fichero .qry) de la que define los metadatos
    """
    query_ = []

    """
    Cadena de texto con los nombre de los campos separados por comas
    """
    fieldNames_ = []

    """
    Mapas alias<->nombre
    """
    aliasFieldMap_ = {}
    fieldAliasMap_ = {}

    """
    Lista de nombres de campos de la tabla que son del tipo FLFieldMetaData::Unlock
    """
    fieldNamesUnlock_ = []

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

    count_ = 0

    def __init__(self, n: protocols.SupportsLower = None, a=None, q=None) -> None:
        self.fieldList_ = []
        self.fieldNamesUnlock_ = []
        self.aliasFieldMap_ = {}
        self.fieldAliasMap_ = {}
        # print("Vaciando field list ahora",  len(self.fieldList_))
        if n is None:
            self.inicializeFLTableMetaDataPrivate()
        elif n and not a and not q:
            self.inicializeFLTableMetaDataPrivateS(n)
        else:
            self.inicializeNewFLTableMetaDataPrivate(n, a, q)
        self.count_ = self.count_ + 1

    def inicializeFLTableMetaDataPrivate(self) -> None:
        self.compoundKey_ = None
        self.inCache = False

    def inicializeNewFLTableMetaDataPrivate(self, n: protocols.SupportsLower, a, q=None) -> None:
        self.name_ = n.lower()
        self.alias_ = a
        self.compoundKey_ = 0
        self.query_ = q
        self.concurWarn_ = False
        self.detectLocks_ = False
        self.inCache_ = False

    def inicializeFLTableMetaDataPrivateS(self, name) -> None:
        self.name_ = str(name)
        self.alias_ = self.name_

    """
    Añade el nombre de un campo a la cadena de nombres de campos, ver fieldNames()

    @param n Nombre del campo
    """

    def addFieldName(self, n: protocols.SupportsLower) -> None:
        self.fieldNames_.append(n.lower())

    """
    Elimina el nombre de un campo a la cadena de nombres de campos, ver fieldNames()

    @param n Nombre del campo
    """

    def removeFieldName(self, n) -> None:

        if self.fieldNames_:
            oldFN = self.fieldNames_
            self.fieldNames_ = []
            for value in oldFN:
                if not value.name().lower() == n.lower():
                    self.fieldNames.append(value)

    """
    Formatea el alias del campo indicado para evitar duplicados

    @param  f   Campo objeto cuyo alias se desea formatear
    """

    def formatAlias(self, f=None) -> None:
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

    """
    Limpia la lista de definiciones de campos
    """

    def clearFieldList(self) -> None:
        self.fieldList_ = []
        self.fieldNames_ = []


# endif
