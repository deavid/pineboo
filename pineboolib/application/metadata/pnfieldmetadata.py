# -*- coding: utf-8 -*-
"""Manage the data of a field in a table."""

from pineboolib.core.utils.utils_base import aqtt

from pineboolib.core.utils import logging
from pineboolib.interfaces import IFieldMetaData

from typing import List, Optional, Union, Any, TYPE_CHECKING

from .pnrelationmetadata import PNRelationMetaData

if TYPE_CHECKING:
    from pineboolib.interfaces import ITableMetaData


logger = logging.getLogger("PNFieldMetadata")


class PNFieldMetaData(IFieldMetaData):
    """PNFieldMetaData Class."""

    Serial = "serial"
    Unlock = "unlock"
    Check = "check"
    count_ = 0

    def __init__(self, *args, **kwargs) -> None:
        """
        Initialize the metadata with the collected data.

        @param n Field Name.
        @param to Alias ​​del campo, used in form labels.
        @param aN TRUE if it allows nulls (NULL), FALSE if it allows them (NOT NULL).
        @param _isPrimaryKey TRUE if it is a primary key, FALSE if it is not a primary key, be
                primary key implies being Index and Unique.
        @param t Field type.
        @param l Length of the field in characters, provided it is of type string
               of characters.
        @param c Indicates if the field is calculated.
        @param v Indicates if the field is visible.
        @param ed Indicates if the field is editable.
        @param pI Indicates the number of digits of the whole part.
        @param pD Indicates the number of decimals.
        @param iNX TRUE if the field is index.
        @param uNI TRUE if the field determines unique records.
        @param coun Indicates if it is an accountant. For automatic references.
        @param defValue Default value for the field.
        @param oT Indicates if the changes in the field are out of transaction.
        @param rX Regular expression used as a validation mask.
        @param vG Indicates if the field is visible in the grid of the table.
        @param gen Indicates if the field is generated.
        @param iCK Indicates if it is a composite key.
        """

        if len(args) == 1:
            self.inicializeFLFieldMetaData(args[0])
        else:
            self.inicializeNewFLFieldMetaData(*args, **kwargs)
        ++self.count_

    def inicializeFLFieldMetaData(self, other: "PNFieldMetaData") -> None:
        """Initialize by copying information from another metadata."""

        self.d = PNFieldMetaDataPrivate()
        self.copy(other)

    def inicializeNewFLFieldMetaData(
        self,
        n: str,
        a: str,
        aN: bool,
        isPrimaryKey: bool,
        t: str,
        length_: int = 0,
        c: bool = False,
        v: bool = True,
        ed: bool = True,
        pI: int = 4,
        pD: int = 0,
        iNX: bool = False,
        uNI: bool = False,
        coun: bool = False,
        defValue: Optional[str] = None,
        oT: bool = False,
        rX: Optional[str] = None,
        vG: bool = True,
        gen: bool = True,
        iCK: bool = False,
    ) -> None:
        """
        Initialize with the information collected.

        @param n Field Name.
        @param to Alias ​​del campo, used in form labels.
        @param aN TRUE if it allows nulls (NULL), FALSE if it allows them (NOT NULL).
        @param _isPrimaryKey TRUE if it is a primary key, FALSE if it is not a primary key, be
                primary key implies being Index and Unique.
        @param t Field type.
        @param l Length of the field in characters, provided it is of type string
               of characters.
        @param c Indicates if the field is calculated.
        @param v Indicates if the field is visible.
        @param ed Indicates if the field is editable.
        @param pI Indicates the number of digits of the whole part.
        @param pD Indicates the number of decimals.
        @param iNX TRUE if the field is index.
        @param uNI TRUE if the field determines unique records.
        @param coun Indicates if it is an accountant. For automatic references.
        @param defValue Default value for the field.
        @param oT Indicates if the changes in the field are out of transaction.
        @param rX Regular expression used as a validation mask.
        @param vG Indicates if the field is visible in the grid of the table.
        @param gen Indicates if the field is generated.
        @param iCK Indicates if it is a composite key.
        """
        self.d = PNFieldMetaDataPrivate(
            n, a, aN, isPrimaryKey, t, length_, c, v, ed, pI, pD, iNX, uNI, coun, defValue, oT, rX, vG, gen, iCK
        )

    def name(self) -> str:
        """
        Get the name of the field.

        @return Field Name.
        """
        if self.d.fieldName_ is None:
            return ""
        return self.d.fieldName_

    def setName(self, n: str) -> None:
        """
        Set the name for the field.

        @param n Field Name
        """

        self.d.fieldName_ = n

    def alias(self) -> str:
        """
        Get the alias of the field.

        @return Alias Name.
        """

        return aqtt(self.d.alias_)

    def allowNull(self) -> bool:
        """
        Get if it allows nulls.

        @return TRUE if it allows nulls, FALSE otherwise
        """

        return self.d.allowNull_

    def isPrimaryKey(self) -> bool:
        """
        Get if it is primary key.

        @return TRUE if it is primary key, FALSE otherwise
        """

        return self.d.isPrimaryKey_

    def setIsPrimaryKey(self, b: bool) -> None:
        """
        Set if it is primary key.

        @return TRUE if it is primary key, FALSE otherwise
        """

        self.d.isPrimaryKey_ = b

    def isCompoundKey(self) -> bool:
        """
        Get if it is a composite key.

        @return TRUE if it is a composite key, FALSE otherwise
        """

        if self.d.isCompoundKey_ is None:
            return False
        return self.d.isCompoundKey_

    def type(self) -> str:
        """
        Return the type of the field.

        @return The field type.
        """

        return str(self.d.type_)

    def length(self) -> int:
        """
        Get the length of the field.

        @return The length of the field.
        """

        return int(self.d.length_ or 0)

    def calculated(self) -> Any:
        """
        Get if the field is calculated.

        @return TRUE if the field is calculated, FALSE otherwise
        """

        return self.d.calculated_

    def setCalculated(self, c) -> None:
        """
        Set if the field is calculated.

        @param c Value TRUE if you want to set the field as calculated, FALSE otherwise.
        """
        self.d.calculated_ = c

    def editable(self) -> bool:
        """
        Get if the field is editable.

        @return TRUE if the field is editable, FALSE otherwise
        """
        return self.d.editable_ if self.d.editable_ is not None else False

    def setEditable(self, ed: bool) -> None:
        """
        Set whether the field is editable.

        @param ed Value TRUE if you want the field to be editable, FALSE otherwise.
        """
        self.d.editable_ = ed

    def visible(self) -> bool:
        """
        Get if the field is visible.

        @return TRUE if the field is visible, FALSE otherwise
        """
        return self.d.visible_

    def visibleGrid(self) -> bool:
        """
        Get if the field is visible in the grid of the table.

        @return TRUE if the field is visible in the grid of the table, FALSE otherwise
        """
        return self.d.visibleGrid_

    def generated(self) -> bool:
        """@return TRUE if the field is generated, that is, it is included in the queries."""

        return self.d.generated_

    def setGenerated(self, value: bool) -> None:
        """Set a field as generated."""

        self.d.generated_ = value

    def setVisible(self, v: bool) -> None:
        """
        Set if the field is visible.

        @param v Value TRUE if you want to make the field visible, FALSE otherwise.
        """

        self.d.visible_ = v

    def setVisibleGrid(self, v) -> None:
        """
        Set whether the field is visible in the grid of the table.

        @param v Value TRUE if you want to make the field visible, FALSE otherwise.
        """

        self.d.visibleGrid_ = v

    def partInteger(self) -> int:
        """
        Get the number of digits of the whole part.

        @return The number of digits of the entire part of the field.
        """

        return int(self.d.partInteger_ or 0)

    def partDecimal(self) -> int:
        """
        Get the number of digits of the decimal part.

        @return The number of digits of the decimal part of the field.
        """

        return int(self.d.partDecimal_ or 0)

    def isCounter(self) -> bool:
        """
        Get if the field is a counter.

        @return TRUE if the field is a reference with counter
        """
        return self.d.contador_

    def isIndex(self) -> bool:
        """
        Get if the field is index.

        @return TRUE if the field is index, FALSE otherwise
        """
        return self.d.isIndex_

    def isUnique(self) -> bool:
        """
        Get if the field determines unique records.

        @return TRUE if the field determines unique records, FALSE otherwise
        """
        return self.d.isUnique_

    def addRelationMD(self, r: "PNRelationMetaData") -> None:
        """
        Add a relationship with another table for this field.

        Add a new FLRelationMetaData object to the list of relationships for this field.
        Note that for one field there can only be one single ratio of type M1 (many to one), so in
        in case you want to add several relationships of this type for the field only the first one will be taken into account.
        Type 1M relationships (one to many) may all exist those necessary. See FLRelationMetaData :: Cardinality.

        @param r FlRelationMetaData object with the definition of the relationship to add.
        """

        isRelM1 = False
        # print("FLFieldMetadata(%s).addRelationMD(card %s)" % (self.name(), r.cardinality()))

        if r.cardinality() == PNRelationMetaData.RELATION_M1:
            isRelM1 = True
        if isRelM1 and self.d.relationM1_:
            logger.debug("addRelationMD: Se ha intentado crear más de una relación muchos a uno para el mismo campo")
            return
        if self.d.fieldName_ is None:
            logger.warning("addRelationMD: no fieldName")
            return
        r.setField(self.d.fieldName_)
        if isRelM1:
            self.d.relationM1_ = r
            return

        if not self.d.relationList_:
            self.d.relationList_ = []

        self.d.relationList_.append(r)

    def relationList(self) -> List["PNRelationMetaData"]:
        """
        To get the list of relationship definitions.

        Does not include the M1 relationship

        @return Object with the list of deficits in the field relations
        """

        return self.d.relationList_

    def relationM1(self) -> Optional["PNRelationMetaData"]:
        """
        Get the many-to-one relationship for this field.

        Not included in relationList ()

        @return Object FLRelationMetaData with the description of the relationship many to one for this field.
        """
        return self.d.relationM1_

    def setAssociatedField(self, r_or_name: Union[str, IFieldMetaData], f: str) -> None:
        """
        Set an associated field for this field, and the name of the foreign table field to use to filter.

            according to the value of the associated field.

        @param r FLFieldMetaData object or Name that defines the field to be associated with this
        @param f Name of the field to apply the filter

        """
        name = r_or_name.name() if not isinstance(r_or_name, str) else r_or_name

        self.d.associatedFieldName_ = name
        self.d.associatedFieldFilterTo_ = f

    def associatedField(self) -> Optional["ITableMetaData"]:
        """
        Return the associated field for this field.

        @return FLFieldMetaData object that defines the field associated with it, or 0 if there is no associated field.
        """
        mtd = self.metadata()
        return mtd and mtd.field(self.d.associatedFieldName_)

    def associatedFieldFilterTo(self) -> str:
        """
        Return the name of the field to be filtered according to the associated field.

        @return Field name of the foreign table M-1, to which the filter must be applied according to the value of the associated field.
        """
        return self.d.associatedFieldFilterTo_

    def associatedFieldName(self) -> Optional[str]:
        """
        Return the name of the associated field this.

        @return Name of the associated field.
        """

        return self.d.associatedFieldName_

    def defaultValue(self) -> Optional[Union[str, bool]]:
        """
        Return the default value for the field.

        @return Value that is assigned to the field by default
        """

        if self.d.defaultValue_ in (None, "null"):
            self.d.defaultValue_ = None

        if self.d.type_ in ("bool", "unlock") and isinstance(self.d.defaultValue_, str):
            return self.d.defaultValue_ == "true"

        return self.d.defaultValue_

    def outTransaction(self) -> bool:
        """
        Return if the field is modified out of transaction.

        @return TRUE if the field is modified out of transaction, FALSE otherwise
        """
        return self.d.outTransaction_ if self.d.outTransaction_ is not None else False

    def regExpValidator(self) -> Optional[str]:
        """
        Return the regular expression that serves as a validation mask for the field.

        @return Character string containing a regular expression, used as
            mask to validate the values ​​entered in the field
        """
        return self.d.regExpValidator_

    def optionsList(self) -> List[str]:
        """
        Return the list of options for the field.

        @return List of field options
        """
        return self.d.optionsList_

    def getIndexOptionsList(self, name: str) -> Optional[int]:
        """
        Return the index of a given field.

        @return List of field options.
        """
        if name in self.d.optionsList_:
            return self.d.optionsList_.index(name)

        return None

    def setOptionsList(self, ol: str) -> None:
        """
        Set the list of options for the field.

        @param ol Text string with options for the field.
        """
        self.d.optionsList_ = []
        if ol.find("QT_TRANSLATE") != -1:
            for componente in ol.split(";"):
                self.d.optionsList_.append(aqtt(componente))
        else:
            for componente in ol.split(","):
                self.d.optionsList_.append(aqtt(componente))

        if len(self.d.optionsList_) > 0:
            self.d.hasOptionsList_ = True
        else:
            self.d.hasOptionsList_ = False

    def isCheck(self) -> bool:
        """
        Get if the field is of type Check.
        """

        if self.d.type_ == self.Check:
            return True
        else:
            return False

    def hasOptionsList(self) -> bool:
        """
        Get if the field has a list of options.
        """

        return self.d.hasOptionsList_ if self.d.hasOptionsList_ is not None else False

    def fullyCalculated(self) -> bool:
        """
        Return if a field is fully calculated.
        """

        return self.d.fullyCalculated_

    def setFullyCalculated(self, c: bool) -> None:
        """
        Specify if a field is fully calculated.
        """

        self.d.fullyCalculated_ = c
        if c:
            self.d.generated_ = True

    def trimed(self) -> bool:
        """Return if a field is trimmed."""

        return self.d.trimmed_

    def setTrimed(self, t: bool) -> None:
        """Specify if a field is trimmed."""

        self.d.trimmed_ = t

    def setMetadata(self, mtd: "ITableMetaData") -> None:
        """
        Set the PNTableMetaData object to which it belongs.
        """
        self.d.mtd_ = mtd

    def metadata(self) -> Optional["ITableMetaData"]:
        """
        Get the FLTableMetaData object to which it belongs.
        """

        return self.d.mtd_

    def flDecodeType(self, fltype_=None) -> Optional[str]:
        """
        Get the type of the field converted to an equivalent type of the QVariant class.
        """

        _type = None
        # print("Decode", fltype)

        if fltype_ == "int":
            _type = "int"
        elif fltype_ == "serial" or fltype_ == "uint":
            _type = "uint"
        elif fltype_ == "bool" or fltype_ == "unlock":
            _type = "bool"
        elif fltype_ == "double":
            _type = "double"
        elif fltype_ == "time":
            _type = "time"
        elif fltype_ == "date":
            _type = "date"
        elif fltype_ == "string" or fltype_ == "pixmap" or fltype_ == "stringlist":
            _type = "string"
        elif fltype_ == "bytearray":
            _type = "bytearray"

        # print("Return", _type)
        return _type

    def searchOptions(self) -> Any:
        """
        Return different search options for this field.

        @return list of different options
        """

        return self.d.searchOptions_

    def setSearchOptions(self, ol) -> None:
        """
        Set the list of options for the field.

        @param ol Text string with options for the field.
        """

        self.d.searchOptions_ = []
        for dato in ol.split(","):
            self.d.searchOptions_.append(dato)

    def copy(self, other: "PNFieldMetaData") -> None:
        """
        Copy the metadata of another pnfieldmetadata.
        """

        if other is self:
            return

        od = other.d

        if od.relationM1_:
            self.d.relationM1_ = od.relationM1_

        self.d.clearRelationList()

        if od.relationList_:
            for r in od.relationList_:
                self.d.relationList_.append(r)

        self.d.fieldName_ = od.fieldName_
        self.d.alias_ = od.alias_
        self.d.allowNull_ = od.allowNull_
        self.d.isPrimaryKey_ = od.isPrimaryKey_
        self.d.type_ = od.type_
        self.d.length_ = od.length_
        self.d.calculated_ = od.calculated_
        self.d.fullyCalculated_ = od.fullyCalculated_
        self.d.trimmed_ = od.trimmed_
        self.d.visible_ = od.visible_
        self.d.editable_ = od.editable_
        self.d.partDecimal_ = od.partDecimal_
        self.d.partInteger_ = od.partInteger_
        self.d.isIndex_ = od.isIndex_
        self.d.isUnique_ = od.isUnique_
        self.d.contador_ = od.contador_
        self.d.associatedFieldName_ = od.associatedFieldName_
        self.d.associatedFieldFilterTo_ = od.associatedFieldFilterTo_
        self.d.defaultValue_ = od.defaultValue_
        self.d.optionsList_ = od.optionsList_
        self.d.outTransaction_ = od.outTransaction_
        self.d.regExpValidator_ = od.regExpValidator_
        self.d.visibleGrid_ = od.visibleGrid_
        self.d.generated_ = od.generated_
        self.d.isCompoundKey_ = od.isCompoundKey_
        self.d.hasOptionsList_ = od.hasOptionsList_

        # self = copy.deepcopy(other)

    def formatAssignValue(self, fieldName: str, value: Any, upper: bool) -> str:
        """
        Return the correct comparison for a given field.
        """

        if value is None or not fieldName:
            return "1 = 1"

        isText = False
        # if isinstance(value, str):
        if self.type() in ("string, time, date, pixmap"):
            isText = True

        formatV: Any = None

        if isText:
            formatV = "'%s'" % value
        else:
            formatV = value

        # if isinstance(value, (int, float)):
        # formatV = str(value)
        # else:
        # formatV = "'" + str(value) + "'"

        # print("FORMATV es %s, %s y value era %s" % (formatV, type(formatV), value.toString()))

        # if formatV == None:
        #    return "1 = 1"

        if upper and isText:
            fName = "upper(%s)" % fieldName
            formatV = formatV.upper()
        else:
            fName = fieldName

        return "%s = %s" % (fName, formatV)

    def __len__(self) -> int:
        """Return the length of a field."""

        return self.d.length_ if self.d.length_ is not None else 0


class PNFieldMetaDataPrivate(object):
    """PNFieldMetaDataPrivate Class."""

    """
    Nombre del campo en la tabla
    """

    fieldName_ = None

    """
    Alias o mote para el campo, usado como
    etiqueta de campos en los formularios
    """
    alias_ = None

    """
    Almacena si el campo permite ser nulo
    """
    allowNull_: bool

    """
    Almacena si el campo es clave primaria
    """
    isPrimaryKey_: bool

    """
    Tipo del campo
    """
    type_ = None

    """
    Longitud del campo
    """
    length_ = None

    """
    Indica si el campo es calculado de forma diferida.
    Esto indica que el campo se calcula al editar o insertar un registro, en el commit.
    """
    calculated_: bool

    """
    Indica si el campo es totalmente calculado.
    Esto indica que el valor campo del campo es dinámico y se calcula en cada refresco.
    Un campo totalmente calculado implica que es generado.
    """
    fullyCalculated_: bool

    """
    Indica que al leer el campo de la base de datos los espacios mas a la derecha
    son eliminados.
    """
    trimmed_: bool

    """
    Indica si el campo es visible
    """
    visible_: bool

    """
    Indica si el campo es editable
    """
    editable_ = None

    """
    Indica el número de dígitos de la parte entera
    """
    partInteger_ = None

    """
    Indica el númeor de dígitos de la parte decimal
    """
    partDecimal_ = None

    """
    Indica si el campo es índice
    """
    isIndex_: bool

    """
    Indica si el campo es único
    """
    isUnique_: bool

    """
    Indica si el campo es un contador de referencia y abanq en el
    momento de insertar un registro debe intentar calcular cual sería el
    siguiente numero.

    @author Andrés Otón Urbano (andresoton@eresmas.com)
    """
    contador_: bool

    """
    Lista de relaciones para este campo
    """
    relationList_: List["PNRelationMetaData"] = []

    """
    Mantiene, si procede, la relación M1 (muchos a uno)
    para el campo (solo puede haber una relacion de este tipo para un campo)
    """
    relationM1_: Any = None

    """
    Asocia este campo con otro, para efectuar filtros en búsquedas.

    El campo que se asocia a este debe tener una relación M-1.
    Este campo también debe tener una relación M-1. Al asociar un campo a este,
    las búsquedas mediante los botones de búsqueda en los formularios de edición
    de registros vendrán condicionadas por el valor del campo asociado en el
    momento de realizar dicha búsqueda. Cuando se realiza una búsqueda para
    este campo la tabla relacionada con él (M-1) será mostrada para elegir un
    registro de todos los posibles, en el caso normal se muestran todos los registros,
    pero cuando se asocia un campo sólo se muestran aquellos registros que satisfagan el
    valor del campo asociado. Ejemplo : En la tabla albaranes asociamos el campo
    'codemporig' al campo 'codalmorig' (NO es lo mismo que asociar 'codalmorig'
    a 'codemporig') cuando abrimos el formulario de albaranes elegimos una empresa
    origen (codemporig), cuando vayamos a elegir un almacen origen (codalmorig) sólo
    se podrá elegir entre los almacenes que son de la empresa origen , ya que el formulario
    de búsqueda sólo se mostrarán los almacenes cuyo código de empresa
    (ver FLFieldMetaData::associatedFieldFilterTo_) sea igual al valor de la empresa origen
    elegida (codemporig)
    """
    associatedFieldName_ = ""

    """
    Nombre del campo que se debe filtra según el campo asociado.

    Esta propiedad sólo tiene sentido cuando hay un campo asociado a este,
    ver FLFieldMetaData ::associatedField_ , y si ese campo tiene una relacion M-1. Indica
    el nombre del campo de la tabla foránea en la relación M-1, que se debe utilizar para filtrar
    los registros según el valor del campo asociado. Ejemplo : En la tabla albaranes asociamos el campo
    'codemporig' al campo 'codalmorig' (NO es lo mismo que asociar 'codalmorig'
    a 'codemporig'), e indicamos que el campo de filtro es 'codempresa' de la tabla relacionada M-1 con el
    campo 'codalmorig' (Almacenes) . Cuando abrimos el formulario de albaranes elegimos una empresa
    origen (codemporig), cuando vayamos a elegir un almacen origen (codalmorig) sólo se podrá elegir
    entre los almacenes que son de la empresa origen, ya que el formulario de búsqueda sólo se mostrarán
    los almacenes cuyo código de empresa (el campo indicado de filtro ) sea igual al valor de la empresa
    origen elegida (codemporig)
    """
    associatedFieldFilterTo_ = ""

    """
    Valor por defecto para el campo
    """
    defaultValue_ = None

    """
    Lista de opciones para el campo
    """
    optionsList_: List[str]

    """
    Indica si las modificaciones del campo se hacen fuera de cualquier transaccion.

    Al estar activado este flag, todos los cambios en el valor de este campo se
    realizan fuera de la transaccion y de forma exclusiva. Es decir los cambios
    realizados en el campo son inmediatamente reflejados en la tabla sin esperar a
    que se termine transaccion, y de forma exclusiva (bloqueando el registro al que
    pertenece el campo mientras se modifica). Esto permite en el acto hacer visibles
    para todas las demas conexiones de la base de datos los cambios realizados en un campo.
    Hay que tener en cuenta que al tener el campo esta caracteristica especial de modificarse
    fuera de la transaccion, el "rollback" no tendra efecto sobre los cambios realizados
    en el y siempre permanecera en la base de datos la ultima modificacion efectuada en
    el campo.
    """
    outTransaction_ = None

    """
    Almacena la expresion regular que sirve como mascara de validacion para el campo.
    """
    regExpValidator_ = None

    """
    Indica si el campo debe ser visible en la rejilla de la tabla.
    """
    visibleGrid_ = True

    """
    Indica si el campo es generado, es decir, se incluye en las consultas
    """
    generated_ = False

    """
    Almacena si el campo es clave compuesta
    """
    isCompoundKey_ = None

    """
    Indica si el campo toma su valor de una lista de opciones
    """
    hasOptionsList_ = None

    """
    Contiene las distintas opciones de búsqueda
    """
    searchOptions_: List[str]

    """
    Objeto FLTableMetaData al que pertenece
    """
    mtd_: Optional["ITableMetaData"] = None

    def __init__(self, *args, **kwargs) -> None:
        """Initialize the class."""

        self.regExpValidator_ = ""
        self.searchOptions_ = []
        self.allowNull_ = False
        self.isPrimaryKey_ = False

        if not args:
            self.inicializeEmpty()
        else:
            self.inicialize(*args, **kwargs)

    def inicializeEmpty(self) -> None:
        """Fill in the data without information."""

        self.relationList_ = []
        self.relationM1_ = None
        self.associatedFieldFilterTo_ = ""
        self.associatedFieldName_ = ""
        self.mtd_ = None

    def inicialize(
        self,
        n: str,
        a: str,
        aN: bool,
        iPK: bool,
        t: Optional[str],
        length_: int,
        c: bool,
        v: bool,
        ed: bool,
        pI: int,
        pD: int,
        iNX: bool,
        uNI: bool,
        coun: bool,
        defValue: Optional[str],
        oT: bool,
        rX: Optional[str],
        vG: bool,
        gen: bool,
        iCK: bool,
    ) -> None:
        """
        Fill in the data with information.

        @param n Field Name.
        @param to Alias ​​del campo, used in form labels.
        @param aN TRUE if it allows nulls (NULL), FALSE if it allows them (NOT NULL).
        @param _isPrimaryKey TRUE if it is a primary key, FALSE if it is not a primary key, be
                primary key implies being Index and Unique.
        @param t Field type.
        @param l Length of the field in characters, provided it is of type string
               of characters.
        @param c Indicates if the field is calculated.
        @param v Indicates if the field is visible.
        @param ed Indicates if the field is editable.
        @param pI Indicates the number of digits of the whole part.
        @param pD Indicates the number of decimals.
        @param iNX TRUE if the field is index.
        @param uNI TRUE if the field determines unique records.
        @param coun Indicates if it is an accountant. For automatic references.
        @param defValue Default value for the field.
        @param oT Indicates if the changes in the field are out of transaction.
        @param rX Regular expression used as a validation mask.
        @param vG Indicates if the field is visible in the grid of the table.
        @param gen Indicates if the field is generated.
        @param iCK Indicates if it is a composite key.
        """

        self.fieldName_ = n.lower()
        self.alias_ = a
        if c:
            self.allowNull_ = True
        else:
            self.allowNull_ = aN
        self.isPrimaryKey_ = iPK
        self.type_ = t
        self.length_ = length_
        self.calculated_ = c
        self.visible_ = v
        self.editable_ = ed
        self.partInteger_ = pI
        self.partDecimal_ = pD
        self.isIndex_ = iNX
        self.isUnique_ = uNI
        self.contador_ = coun
        self.relationList_ = []
        self.relationM1_ = None
        self.associatedFieldFilterTo_ = ""
        self.associatedFieldName_ = ""
        self.defaultValue_ = defValue
        self.outTransaction_ = oT
        self.regExpValidator_ = rX
        self.visibleGrid_ = vG
        self.generated_ = gen
        self.isCompoundKey_ = iCK
        self.hasOptionsList_ = False
        self.mtd_ = None
        self.fullyCalculated_ = False
        self.trimmed_ = False
        self.optionsList_ = []

        if self.type_ is None:
            if self.partDecimal_ > 0:
                self.type_ = "double"
            elif self.length_ > 0:
                self.type_ = "string"
            else:
                self.type_ = "uint"
            logger.info("%s:: El campo %s no tiene especificado tipo y se especifica tipo %s", __name__, self.fieldName_, self.type_)

        if int(length_) < 0:
            self.length_ = 0

        if int(pI) < 0:
            self.partInteger_ = 0
        if int(pD) < 0:
            self.partDecimal_ = 0
        # print("Tipo ", t)

        if not t == "string" and not int(length_) == 0:
            self.length_ = 0

        # if not t == "int" and not t == "uint" and t == "double" and not int(pI) == 0:
        # self.partInteger_ = 0

        if t == "double" and not int(pD) >= 0:
            self.partDecimal_ = 0

    def __del_(self):
        """
        Delete properties when deleted.
        """
        self.clearRelationList()
        if self.relationM1_ and self.relationM1_.deref():
            self.relationM1_ = None

    def clearRelationList(self) -> None:
        """
        Clear the list of relationship definitions.
        """
        self.relationList_ = []
