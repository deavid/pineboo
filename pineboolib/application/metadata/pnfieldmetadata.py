# -*- coding: utf-8 -*-
from pineboolib.core.utils.utils_base import aqtt

from pineboolib.core.utils import logging
from pineboolib.interfaces import IFieldMetaData

from typing import List, Optional, Union, Any, TYPE_CHECKING

from .pnrelationmetadata import PNRelationMetaData

if TYPE_CHECKING:
    from pineboolib.interfaces import ITableMetaData


logger = logging.getLogger("PNFieldMetadata")


class PNFieldMetaData(IFieldMetaData):
    """
  @param n Nombre del campo
  @param a Alias del campo, utilizado en etiquetas de los formularios
  @param aN TRUE si permite nulos (NULL), FALSE si los permite (NOT NULL)
  @param _isPrimaryKey TRUE si es clave primaria, FALSE si no es clave primaria, ser
        clave primaria implica ser Indice y Único
  @param t Tipo del campo
  @param l Longitud del campo en caracteres, siempre que se de tipo cadena
       de caracteres
  @param c Indica si el campo es calculado
  @param v Indica si el campo es visible
  @param ed Indica si el campo es editable
  @param pI Indica el número de dígitos de la parte entera
  @param pD Indica el número de decimales
  @param iNX TRUE si el campo es índice
  @param uNI TRUE si el campo determina registros únicos
  @param coun Indica si es un contador. Para referencias automáticas
  @param defValue Valor por defecto para el campo
  @param oT Indica si las modificaciones en el campo son fuera de transaccion
  @param rX Expresion regular utilizada como mascara de validacion
  @param vG Indica si el campo es visible en la rejilla de la tabla
  @param gen Indica si el campo es generado.
  @param iCK Indica si es clave compuesta
    """

    Serial = "serial"
    Unlock = "unlock"
    Check = "check"
    count_ = 0

    def __init__(self, *args, **kwargs) -> None:

        if len(args) == 1:
            self.inicializeFLFieldMetaData(args[0])
        else:
            self.inicializeNewFLFieldMetaData(*args, **kwargs)
        ++self.count_

    def inicializeFLFieldMetaData(self, other) -> None:
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
        self.d = PNFieldMetaDataPrivate(
            n,
            a,
            aN,
            isPrimaryKey,
            t,
            length_,
            c,
            v,
            ed,
            pI,
            pD,
            iNX,
            uNI,
            coun,
            defValue,
            oT,
            rX,
            vG,
            gen,
            iCK,
        )

    """
    Obtiene el nombre del campo.

    @return Nombre del campo
    """

    def name(self) -> str:
        if self.d.fieldName_ is None:
            return ""
        return self.d.fieldName_

    """
    Establece el nombre para el campo

    @param n Nombre del campo
    """

    def setName(self, n) -> None:
        self.d.fieldName_ = n

    """
    Obtiene el alias del campo.

    @return Alias del campo
    """

    def alias(self) -> str:
        return aqtt(self.d.alias_)

    """
    Obtiene si permite nulos.

    @return TRUE si permite nulos, FALSE en caso contrario
    """

    def allowNull(self) -> bool:
        if self.d.allowNull_ is None:
            return False
        return self.d.allowNull_

    """
    Obtiene si es clave primaria.

    @return TRUE si es clave primaria, FALSE en caso contrario
    """

    def isPrimaryKey(self) -> bool:
        if self.d.isPrimaryKey_ is None:
            return False
        return self.d.isPrimaryKey_

    def setIsPrimaryKey(self, b) -> None:
        self.d.isPrimaryKey_ = b

    """
    Obtiene si es clave compuesta.

    @return TRUE si es clave compuesta, FALSE en caso contrario
    """

    def isCompoundKey(self) -> bool:
        if self.d.isCompoundKey_ is None:
            return False
        return self.d.isCompoundKey_

    """
    Obtiene el tipo del campo.

    @return El tipo del campo
    """

    def type(self) -> str:
        return str(self.d.type_)

    """
    Obtiene la longitud del campo.

    @return La longitud del campo
    """

    def length(self) -> int:
        return int(self.d.length_ or 0)

    """
    Obtiene si el campo es calculado.

    @return TRUE si el campo es calculado, FALSE en caso contrario
    """

    def calculated(self) -> Any:
        return self.d.calculated_

    """
    Establece si el campo es calculado.

    @param c Valor TRUE si se quiere poner el campo como calculado, FALSE en caso contrario
    """

    def setCalculated(self, c) -> None:
        self.d.calculated_ = c

    """
    Obtiene si el campo es editable.

    @return TRUE si el campo es editable, FALSE en caso contrario
    """

    def editable(self) -> bool:
        return self.d.editable_ if self.d.editable_ is not None else False

    """
    Establece si el campo es editable.

    @param ed Valor TRUE si se quiere que el campo sea editable, FALSE
          en caso contrario
    """

    def setEditable(self, ed: bool) -> None:
        self.d.editable_ = ed

    """
    Obtiene si el campo es visible.

    @return TRUE si el campo es visible, FALSE en caso contrario
    """

    def visible(self) -> bool:
        return self.d.visible_ if self.d.visible_ is not None else False

    """
    Obtiene si el campo es visible en la rejilla de la tabla.

    @return TRUE si el campo es visible en la rejilla de la tabla, FALSE en caso contrario
    """

    def visibleGrid(self) -> bool:
        return self.d.visibleGrid_

    """
    @return TRUE si el campo es generado, es decir, se incluye en las consultas
    """

    def generated(self) -> bool:
        return self.d.generated_

    def setGenerated(self, value) -> None:
        self.d.generated_ = value

    """
    Establece si el campo es visible.

    @param v Valor TRUE si se quiere poner el campo como visible, FALSE
         en caso contrario
    """

    def setVisible(self, v: bool) -> None:
        self.d.visible_ = v

    """
    Establece si el campo es visible en la rejilla de la tabla.

    @param v Valor TRUE si se quiere poner el campo como visible, FALSE
         en caso contrario
    """

    def setVisibleGrid(self, v) -> None:
        self.d.visibleGrid_ = v

    """
    Obtiene el número de dígitos de la parte entera.

    @return El número de dígitos de la parte entera del campo
    """

    def partInteger(self) -> int:
        return int(self.d.partInteger_ or 0)

    """
    Obtiene el número de dígitos de la parte decimal.

    @return El número de dígitos de la parte decimal del campo
    """

    def partDecimal(self) -> int:
        return int(self.d.partDecimal_ or 0)

    """
    Obtiene si el campo es contador.

    @return TRUE si el campo es una referencia con contador
    """

    def isCounter(self) -> Any:
        return self.d.contador_

    """
    Obtiene si el campo es índice.

    @return TRUE si el campo es índice, FALSE en caso contrario
    """

    def isIndex(self) -> Any:
        return self.d.isIndex_

    """
    Obtiene si el campo determina registros únicos.

    @return TRUE si el campo determina registros únicos, FALSE en caso contrario
    """

    def isUnique(self) -> Any:
        return self.d.isUnique_

    """
    Tipo de datos lista de relaciones
    """
    # typedef QPtrList<FLRelationMetaData> FLRelationMetaDataList; //
    # FLRelationMetaDataList.py

    """
    Añade una relacion con otra tabla para este campo.

    Añade un nuevo objeto FLRelationMetaData, a la lista
    de relaciones para este campo.

    Hay que notar que para un campo solo puede existir una
    sola relacion del tipo M1 (muchos a uno), por lo que en
    el caso de que se quieran añadir varias relaciones de
    este tipo para el campo solo se tendrá en cuenta la primera.
    Relaciones del tipo 1M (uno a muchos) pueden existir todas
    las que sean necesarias. Ver FLRelationMetaData::Cardinality.

    @param r Objeto FlRelationMetaData con la definicion de la
         relacion a añadir """

    def addRelationMD(self, r: "PNRelationMetaData") -> None:

        isRelM1 = False
        # print("FLFieldMetadata(%s).addRelationMD(card %s)" % (self.name(), r.cardinality()))

        if r.cardinality() == PNRelationMetaData.RELATION_M1:
            isRelM1 = True
        if isRelM1 and self.d.relationM1_:
            logger.debug(
                "addRelationMD: Se ha intentado crear más de una relación muchos a uno para el mismo campo"
            )
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

    """
    Para obtener la lista de definiciones de las relaciones.

     No incluye la relacion M1

    @return Objeto con la lista de deficiones de la relaciones del campo
    """

    def relationList(self) -> List["PNRelationMetaData"]:
        return self.d.relationList_

    """
    Para obtener la relacion muchos a uno para este campo.

       No incluida en relationList()

    @return Objeto FLRelationMetaData con la descripcion de la relacion
        muchos a uno para este campo
    """

    def relationM1(self) -> Optional["PNRelationMetaData"]:
        return self.d.relationM1_

    """
    Establece un campo asociado para este campo, y el nombre
    del campo de la tabla foránea que se debe utilizar para filtrar según
    el valor del campo asociado.

    Ver FLFieldMetaData::associatedField_
    Ver FLFieldMetaData::associatedFieldFilterTo_

    @param r Objeto FLFieldMetaData que define el campo que se quiere asociar a este
    @param f Nombre del campo a aplicar el filtro
    """
    # def setAssociatedField(self, *r, f):
    #    self.d.associatedField_ = r
    #    self.d.associatedFieldFilterTo_ = f

    """
    Sobrecargada por conveniencia

    @param r Nombre del campo que se quiere asociar a este
    @param f Nombre del campo a aplicar el filtro
    """
    # def setAssociatedField(self, rName, f):
    #    self.d.associatedFieldName_ = rName
    #    self.d.associatedFieldFilterTo_ = f

    def setAssociatedField(self, r_or_name: Union[str, IFieldMetaData], f: str) -> None:
        name = r_or_name.name() if not isinstance(r_or_name, str) else r_or_name

        self.d.associatedFieldName_ = name
        self.d.associatedFieldFilterTo_ = f

    """
    Devuelve el campo asociado para este campo.

    Ver FLFieldMetaData::associatedField_

    @return Objeto FLFieldMetaData que define el campo asociado a este, o 0
      si no hay campo asociado
    """

    def associatedField(self) -> Optional["ITableMetaData"]:
        mtd = self.metadata()
        return mtd and mtd.field(self.d.associatedFieldName_)

    """
    Devuelve el nombre del campo que hay que filtrar según el campo asociado.

    Ver FLFieldMetaData::associatedFieldFilterTo_

    @return Nombre del campo de la tabla foránea M-1, al que hay que aplicar el filtro
      según el valor del campo asociado
    """

    def associatedFieldFilterTo(self) -> str:
        return self.d.associatedFieldFilterTo_

    """
    Devuelve el nombre del campo asociado este.

    Ver FLFieldMetaData::associatedField_

    @return Nombre del campo asociado
    """

    def associatedFieldName(self) -> Optional[str]:
        return self.d.associatedFieldName_

    """
    Devuelve el valor por defecto para el campo.

    @return Valor que se asigna por defecto al campo
    """

    def defaultValue(self) -> Optional[Union[str, bool]]:
        if self.d.defaultValue_ in (None, "null"):
            self.d.defaultValue_ = None

        if self.d.type_ in ("bool", "unlock") and isinstance(self.d.defaultValue_, str):
            return self.d.defaultValue_ == "true"

        return self.d.defaultValue_

    """
    Devuelve si el campo se modifica fuera de transaccion,
    ver FLFieldMetaData::outTransaction_.

    @return TRUE si el campo se modifica fuera de transaccion, FALSE en caso contrario
    """

    def outTransaction(self) -> bool:
        return self.d.outTransaction_ if self.d.outTransaction_ is not None else False

    """
    Devuelve la expresion regular que sirve como mascara de validacion para el campo.

    @return Cadena de caracteres que contiene una expresion regular, utilizada como
        mascara para validar los valores introducidos en el campo
    """

    def regExpValidator(self) -> Optional[str]:
        return self.d.regExpValidator_

    """
    Devuelve la lista de opciones para el campo

    @return Lista de opciones del campo
    """

    def optionsList(self) -> List[str]:
        return self.d.optionsList_

    """
    Devuelve el index de un campo determinado

    @return Lista de opciones del campo
    """

    def getIndexOptionsList(self, name: str) -> Optional[int]:
        if name in self.d.optionsList_:
            return self.d.optionsList_.index(name)

        return None

    """
    Establece la lista de opciones para el campo

    @param ol Cadena de texto con la opciones para el campo
          separada por comas, p.e. "opcion1,opcion2,opcion3"
    """

    def setOptionsList(self, ol: str) -> None:
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

    """
    Obtiene si el campo es de tipo Check
    """

    def isCheck(self) -> bool:
        if self.d.type_ == self.Check:
            return True
        else:
            return False

    """
    Obtiene si el campo tiene lista de opciones
    """

    def hasOptionsList(self) -> bool:
        return self.d.hasOptionsList_ if self.d.hasOptionsList_ is not None else False

    """
    Ver FLFieldMetaData::fullyCaclulated_
    """

    def fullyCalculated(self) -> Any:
        return self.d.fullyCalculated_

    def setFullyCalculated(self, c: bool) -> None:
        self.d.fullyCalculated_ = c
        if c:
            self.d.generated_ = True

    """
    Ver FLFieldMetaData::trimmed_
    """

    def trimed(self) -> Any:
        return self.d.trimmed_

    def setTrimed(self, t: bool) -> None:
        self.d.trimmed_ = t

    """
    Establece el objeto FLTableMetaData al que pertenece
    """

    def setMetadata(self, mtd: "ITableMetaData") -> None:
        self.d.mtd_ = mtd

    """
    Obtiene el objeto FLTableMetaData al que pertenece
    """

    def metadata(self) -> Optional["ITableMetaData"]:
        return self.d.mtd_

    """
    Obtiene el tipo del campo convertido a un tipo equivalente de la clase QVariant
    """

    def flDecodeType(self, fltype_) -> Optional[str]:

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
        elif fltype_ == "string" or fltype_ == "pixmap" or fltype_ == "stringList":
            _type = "string"
        elif fltype_ == "bytearray":
            _type = "bytearray"

        # print("Return", _type)
        return _type

    """
    Devuelve diferentes opciones de búsqueda para este campo.

    @return lista de las distintas opciones
    """

    def searchOptions(self) -> Any:
        return self.d.searchOptions_

    """
    Establece la lista de opciones para el campo

    @param ol Cadena de texto con la opciones para el campo
          separada por comas, p.e. "opcion1,opcion2,opcion3"
    """

    def setSearchOptions(self, ol) -> None:
        self.d.searchOptions_ = []
        for dato in ol.split(","):
            self.d.searchOptions_.append(dato)

    def copy(self, other) -> None:
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
        return self.d.length_ if self.d.length_ is not None else 0


class PNFieldMetaDataPrivate(object):
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
    allowNull_ = None

    """
    Almacena si el campo es clave primaria
    """
    isPrimaryKey_ = None

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
    calculated_ = None

    """
    Indica si el campo es totalmente calculado.
    Esto indica que el valor campo del campo es dinámico y se calcula en cada refresco.
    Un campo totalmente calculado implica que es generado.
    """
    fullyCalculated_ = None

    """
    Indica que al leer el campo de la base de datos los espacios mas a la derecha
    son eliminados.
    """
    trimmed_ = None

    """
    Indica si el campo es visible
    """
    visible_ = None

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
    isIndex_ = None

    """
    Indica si el campo es único
    """
    isUnique_ = None

    """
    Indica si el campo es un contador de referencia y abanq en el
    momento de insertar un registro debe intentar calcular cual sería el
    siguiente numero.

    @author Andrés Otón Urbano (andresoton@eresmas.com)
    """
    contador_ = None

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

        self.regExpValidator_ = ""
        self.searchOptions_ = []
        if not args:
            self.inicializeEmpty()
        else:
            self.inicialize(*args, **kwargs)

    def inicializeEmpty(self) -> None:
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
            logger.info(
                "%s:: El campo %s no tiene especificado tipo y se especifica tipo %s",
                __name__,
                self.fieldName_,
                self.type_,
            )

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
        self.clearRelationList()
        if self.relationM1_ and self.relationM1_.deref():
            self.relationM1_ = None

    """
    Limpia la lista de definiciones de relaciones
    """

    def clearRelationList(self) -> None:
        self.relationList_ = []
