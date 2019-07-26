import copy
import datetime
import decimal
from typing import Dict, List, Union, Optional, Any, TYPE_CHECKING

from pineboolib import logging
from pineboolib.application import types

if TYPE_CHECKING:
    from pineboolib.interfaces import isqlcursor
    from pineboolib.interfaces import ifieldmetadata

logger = logging.getLogger(__name__)

ACCEPTABLE_VALUES = (int, float, str, datetime.time, datetime.date, bool, types.Date, bytearray, decimal.Decimal, datetime.timedelta)
T_VALUE2 = Union[int, float, str, datetime.time, datetime.date, bool, types.Date, bytearray, datetime.timedelta, None]


class FieldStruct(object):
    """Specific class for fields exclusive within this private module"""

    tablename: Any
    name: str
    query_table: Any
    value: Any  # T_VALUE
    metadata: Any
    type_: Any
    modified: bool
    originalValue: Any  # T_VALUE
    generated: bool

    def __init__(self, field: "ifieldmetadata.IFieldMetaData"):
        self.name = str(field.name())
        self.value = None
        self.metadata = field
        self.type_ = field.type()
        self.modified = False
        self.originalValue = None
        self.generated = field.generated()

    def parse_value_input(self, value: T_VALUE2) -> T_VALUE2:
        """Given an user-provided input, it parses and reformats it suitable for database use"""
        txtvalue: str
        if self.type_ == "double" and value and value not in ("", "-"):
            if isinstance(value, str):
                if value.find(":") > -1:
                    # Convertimos a horas
                    list_ = value.split(":")
                    numvalue: int = int(list_[0])  # Horas
                    numvalue += int(list_[1]) // 60  # Minutos a hora
                    numvalue += int(list_[2]) // 3600  # Segundos a hora
                    return numvalue
                else:
                    if value.find(",") > -1:
                        value = value.replace(",", "")

                    return float(value)

        elif self.type_ in ("string", "stringlist"):
            if value is None:
                return None
            else:
                return str(value)

        elif self.type_ == "time":
            if value is not None:
                if isinstance(value, types.Date):
                    txtvalue = value.toString()
                elif isinstance(value, datetime.timedelta):
                    txtvalue = str(value)
                elif isinstance(value, str):
                    txtvalue = value
                else:
                    return None

                if txtvalue.find("T") > -1:
                    txtvalue = txtvalue[txtvalue.find("T") + 1 :]

                if txtvalue.find(".") > -1:
                    txtvalue = txtvalue[0 : txtvalue.find(".")]

                elif txtvalue.find("+") > -1:
                    txtvalue = txtvalue[0 : txtvalue.find("+")]
                return txtvalue

        elif self.type_ == "date":
            if value is None:
                return None
            if isinstance(value, types.Date):
                txtvalue = value.toString()
            else:
                txtvalue = str(value)

            if txtvalue.upper() == "NAN":
                return "NAN"
            else:
                if txtvalue.find("T") > -1:
                    txtvalue = txtvalue[: txtvalue.find("T")]

                list_ = txtvalue.split("-")
                return datetime.date(int(list_[0]), int(list_[1]), int(list_[2]))
        elif self.type_ in ("unlock", "bool"):
            if isinstance(value, str):
                if value == "true":
                    return True
                elif value == "false":
                    return False
                else:
                    raise ValueError("bool type can't accept %s" % value)

        return value

    """
    Comprueba si un campo tiene valor diferente. Esto es especialmente util para los número con decimales
    @return True si ha cambiado, False si es el mismo valor
    """

    def has_changed(self, val: T_VALUE2) -> bool:

        if self.value is None:
            if val is None:
                return False
            elif val in (None, "None"):
                return True

        if self.value in (None, "None"):
            return True

        if isinstance(self.value, str) and isinstance(val, str):
            return self.value != val
        elif isinstance(val, (datetime.date, datetime.time)):
            return str(self.value) != str(val)
        elif self.type_ in ("string", "stringlist"):
            return self.value != val
        elif self.type_ in ("int", "uint", "serial", "date"):
            return str(self.value) != str(val)
        elif self.type_ == "double":
            try:
                return float(self.value) != float(val)  # type: ignore
            except Exception:
                logger.trace("has_changed: Error converting %s != %s to floats", self.value, val)
                return True

        return True


class PNBuffer(object):
    """Cursor buffer. When a query is done, after first(), a PNBuffer is created which holds
    the fields of the record.
    """

    def __init__(self, cursor: "isqlcursor.ISqlCursor") -> None:
        """Create a Buffer from the specified PNSqlCursor"""
        super().__init__()
        if not cursor:
            raise Exception("Missing cursor")
        self.cursor_ = cursor
        self.fieldList_: List[FieldStruct] = []
        self.fieldDict_: Dict[str, FieldStruct] = {}
        self.line_: int = -1
        self.inicialized_: bool = False

        tmd = self.cursor_.metadata()
        if tmd is None:
            logger.warning("Metadata not found for specified cursor %s", self.cursor_.curName())
            return

        campos = tmd.fieldList()
        # FIXME: Should not inspect the fields in each create, this should be cached in the metadata()
        for campo in campos:
            field = FieldStruct(campo)
            self.fieldList_.append(field)
            self.fieldDict_[field.name.lower()] = field

    def count(self) -> int:
        """Cantidad de campos que componen el buffer
        @return int
        """
        return len(self.fieldList_)

    def clear_buffer(self):
        self.clearValues(True)
        self.setNoModifiedFields()

    def primeInsert(self, row: int = None) -> None:
        """Actualización inicial de los campos del buffer
        @param row = Linea del cursor
        """
        if self.inicialized_:
            logger.debug("(%s)PNBuffer. Se inicializa nuevamente el cursor", self.cursor_.curName())

        self.primeUpdate(row)
        self.inicialized_ = True

    def primeUpdate(self, row: int = None) -> None:
        """Initial copy of the cursor values into the buffer
        """
        if row is None or row < 0:
            row = self.cursor_.currentRegister()
        if row is None:
            raise Exception("Unexpected: No currentRegister")
        self.clear_buffer()

        if row == -1:
            logger.warning(
                "PrimeUpdate sobre posición inválida de %s, size: %s, filtro: %s, row: %s",
                self.cursor_.metadata().name(),
                self.cursor_.size(),
                self.cursor_.filter(),
                row,
                stack_info=True,
            )
            return

        for field in self.fieldsList():
            value = self.cursor_.model().value(row, field.name)
            if value is not None:
                if field.type_ in ("unlock", "bool"):
                    value = value in ("True", True, 1, "1")

                elif field.type_ == "date":
                    if isinstance(value, str):
                        date_ = value.split("-")
                        if len(date_[2]) == 4:
                            value = date_[2] + "-" + date_[1] + "-" + date_[0]

                elif field.type_ == "bytearray":
                    value = bytearray(value)

            field.value = value
            field.originalValue = copy.copy(value)
        # self.cursor_.bufferChanged.emit(field.name)
        self.setRow(row)

    def primeDelete(self) -> None:
        """Borra los valores de todos los campos del buffer"""
        for field in self.fieldList_:
            field.value = None
            field.modified = field.originalValue is not None

    def row(self) -> int:
        """Indica la linea del cursor a la que hace referencia el buffer
        @return int
        """
        return self.line_

    def setRow(self, l: int) -> None:
        """Setea la linea del cursor a la que se supone hace referencia el buffer
        @param l = registro del cursor
        """
        self.line_ = l

    def setNull(self, name) -> bool:
        """Setea a None el campo especificado
        @param name = Nombre del campo
        """
        return self.setValue(name, None)

    def isGenerated(self, name: str) -> bool:
        """Indica si el campo es generado o no
        @return bool (True es generado, False no es generado)
        """
        return self.fieldDict_[name].generated

    def setGenerated(self, f: Union[int, str, "ifieldmetadata.IFieldMetaData"], value: bool) -> None:
        """Setea que es generado un campo.
        @param f. FLFieldMetadata campo a marcar
        @param value. True o False si el campo es generado
        """
        if not isinstance(f, str) and not isinstance(f, int):
            f = f.name()
        self._field(f).generated = value

    def clearValues(self, b: bool) -> None:
        """Setea todos los valores a None y marca field.modified a True
        @param b bool (True, False no hace nada)
        """
        if not b:
            return
        for field in self.fieldList_:
            field.value = None
            field.modified = True

    def isEmpty(self) -> bool:
        """Indica si el buffer no se ha iniciado
        @return bool True está iniciado, False no está iniciado
        """
        return self.inicialized_

    def isNull(self, n: Union[str, int]) -> bool:
        """Indica si un valor esta vacío
        @param n (str,int) del campo a comprobar si está vacío
        @return bool (True vacío, False contiene valores)
        """
        field = self.field(n)

        if field is None:
            # FIXME: Esto es un error. Si el campo no existe, es una llamada
            # errónea.
            logger.debug("PNBuffer.isNull: Field <%s> not found", n)
            return True

        if field.type_ in ("bool", "unlock"):
            # FIXME: Why do we need this as an special case?
            return self.value(field.name) not in (True, False)

        # FIXME: This confuses empty with Null
        return field.value in (None, "")

    def value(self, n: Union[str, int]) -> T_VALUE2:
        """Retorna el valor de un campo
        @param n (str,int) del campo a recoger valor
        @return valor del campo
        """
        field = self._field(n)
        v = field.value

        if field.type_ in ("bool", "unlock"):
            v = field.value in (True, "true")
            return v

        if field.value is None:
            return None

        if field.type_ in ("str", "pixmap", "time", "date"):
            try:
                v = str(field.value)
            except Exception as e:
                logger.trace("Error trying to convert %s to string: %s", field.value, e)
                v = ""
        elif field.type_ in ("int", "uint", "serial"):
            try:
                v = int(field.value)
            except Exception as e:
                logger.trace("Error trying to convert %s to int: %s", field.value, e)
                v = 0

        elif field.type_ == "double":
            try:
                v = float(field.value)
            except Exception as e:
                logger.trace("Error trying to convert %s to float: %s", field.value, e)
                v = 0.0

        # logger.trace("---->retornando %s %s %s",v , type(v), field.value, field.name)
        return v

    def setValue(self, name: str, value: T_VALUE2, mark_: bool = True) -> bool:
        """Setea el valor de un campo del buffer
        @param name. Nombre del campo
        @param value. Valor a asignar al campo
        @param mark_. Si True comprueba que ha cambiado respecto al valor asignado en primeUpdate
                    y si ha cambiado lo marca como modificado (Por defecto a True)
        """
        if value is not None and not isinstance(value, ACCEPTABLE_VALUES):
            raise ValueError("No se admite el tipo %r , en setValue(%s,%r)" % (type(value), name, value))

        field = self.field(name)

        if field is None:
            logger.warning("setValue: no such field %s", name)
            return False

        if field.has_changed(value):
            field.value = field.parse_value_input(value)

            if mark_:
                if not field.value == field.originalValue:
                    field.modified = True
                else:
                    field.modified = False
                # self.setMd5Sum(value)

        return True

    def cursor(self) -> "isqlcursor.ISqlCursor":
        """Indica al cursor que pertenecemos
        @return Cursor al que pertenecemos
        """
        return self.cursor_

    def modifiedFields(self) -> List[str]:
        """Retorna los campos del buffer modificados desde original
        @return array Lista de campos modificados
        """
        lista = []
        for f in self.fieldsList():
            if f.modified:
                lista.append(f.name)

        return lista

    def setNoModifiedFields(self) -> None:
        """Setea todos los campos como no modificados
        """
        for f in self.fieldsList():
            f.modified = False

    def pK(self) -> Optional[str]:
        """Indica que campo del buffer es clave primaria
        @return Nombre del campo que es clave primaria
        """
        for f in self.fieldsList():
            if f.metadata.isPrimaryKey():
                return f.name
        logger.warning("PNBuffer.pk(): No se ha encontrado clave Primaria")
        return None

    def indexField(self, name) -> Optional[int]:
        """Indica la posicion del buffer de un campo determinado
        @param name
        @return Posición del campo a buscar
        """
        for i, f in enumerate(self.fieldsList()):
            if f.name == name:
                return i
        logger.warning("indexField: %s not found", name)
        return None

    def fieldsList(self) -> List[FieldStruct]:
        return self.fieldList_

    def field(self, n) -> Optional[FieldStruct]:
        """Retrieves a field by ID/position or by name
        Ingores errors and returns None if not found.
        Still can raise Exception if called with a bad type.
        """
        try:
            return self._field(n)
        except (KeyError, ValueError):
            return None

    def _field(self, n: Union[str, int]) -> FieldStruct:
        if isinstance(n, str):
            return self.fieldDict_[n.lower()]
        elif isinstance(n, int):
            if n < 0 or n >= len(self.fieldList_):
                raise ValueError("Value n:%s out of bounds" % n)
            return self.fieldList_[n]
        raise Exception("Bad call to _field, type not supported %s" % type(n))
