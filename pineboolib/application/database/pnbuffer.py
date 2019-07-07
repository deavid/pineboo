from typing import Any
from pineboolib import logging
from pineboolib.application import types
import copy, datetime

logger = logging.getLogger(__name__)


class Struct(object):
    tablename: Any
    name: str
    query_table: Any
    value: Any
    metadata: Any
    type_: Any
    modified: Any
    originalValue: Any
    generated: Any


class PNBuffer(object):

    fieldList_ = None
    cursor_ = None
    clearValues_ = False
    line_ = None
    inicialized_ = False

    def __init__(self, cursor):
        super().__init__()
        self.cursor_ = cursor
        self.fieldList_ = []
        tmd = self.cursor().metadata()
        if not tmd:
            return
        else:
            campos = tmd.fieldList()
        for campo in campos:
            field = Struct()
            field.name = str(campo.name())
            field.value = None
            field.metadata = campo
            field.type_ = field.metadata.type()
            field.modified = False
            field.originalValue = None
            field.generated = campo.generated()

            self.line_ = None
            self.fieldList_.append(field)

    """
    Retorna el numero de campos que componen el buffer
    @return int
    """

    def count(self):
        return len(self.fieldsList())

    """
    Actualización inicial de los campos del buffer
    @param row = Linea del cursor
    """

    def primeInsert(self, row=None):
        if self.inicialized_:
            logger.debug("(%s)PNBuffer. Se inicializa nuevamente el cursor", self.cursor().curName())

        self.primeUpdate(row)
        self.inicialized_ = True

    def primeUpdate(self, row=None):

        if row is None or row < 0:
            row = self.cursor().currentRegister()

        for field in self.fieldsList():
            value = self.cursor().model().value(row, field.name)
            if value in ("None", None):
                value = None

            if field.type_ in ("unlock", "bool"):
                value = value in ("True", True, 1, "1")

            elif field.type_ == "date":
                if isinstance(value, str):
                    date_ = value.split("-")
                    if len(date_[2]) == 4:
                        value = date_[2] + "-" + date_[1] + "-" + date_[0]

            elif field.type_ == "bytearray":
                value = bytearray() if value is None else bytearray(value)

            field.value = value
            # val = self.cursor().model().value(row , field.name)
            # if val == "None":
            #    val = None
            # self.setValue(field.name, val)
            field.originalValue = copy.copy(field.value)
            # self.cursor().bufferChanged.emit(field.name)

        self.setRow(self.cursor().currentRegister())

    """
    Borra los valores de todos los campos del buffer
    """

    def primeDelete(self):
        for field in self.fieldList():
            self.setNull(field.name)

    """
    Indica la linea del cursor a la que hace referencia el buffer
    @return int
    """

    def row(self):
        return self.line_

    """
    Setea la linea del cursor a la que se supone hace referencia el buffer
    @param l = registro del cursor
    """

    def setRow(self, l):
        self.line_ = l

    """
    Setea a None el campo especificado
    @param name = Nombre del campo
    """

    def setNull(self, name):
        return self.setValue(name, None)

    """
    Indica si el campo es generado o no
    @return bool (True es generado, False no es generado)
    """

    def isGenerated(self, name):
        return self.field(name).generated

        """
    Setea que es generado un campo.
    @param f. FLFieldMetadata campo a marcar
    @param value. True o False si el campo es generado
    """

    def setGenerated(self, f, value):
        if not isinstance(f, str) and not isinstance(f, int):
            f = f.name()
        self.field(f).generated = value

    """
    Setea todos los valores a None y marca field.modified a True
    @param b bool (True, False no hace nada)
    """

    def clearValues(self, b):
        if b:
            for field in self.fieldList_:
                field.value = None
                field.modified = False

    """
    Indica si el buffer no se ha iniciado
    @return bool True está iniciado, False no está iniciado
    """

    def isEmpty(self):
        return self.inicialized_

    """
    Indica si un valor esta vacío
    @param n (str,int) del campo a comprobar si está vacío
    @return bool (True vacío, False contiene valores)
    """

    def isNull(self, n):
        field = self.field(n)

        if field is None:
            # FIXME: Esto es un error. Si el campo no existe, es una llamada
            # errónea.
            logger.debug("Call to cursor.isNull(None); This is an error.")
            return True

        if field.type_ in ("bool", "unlock"):
            return not (self.value(field.name) in (True, False))

        return field.value in (None, "")

    """
    Retorna el valor de un campo
    @param n (str,int) del campo a recoger valor
    @return valor del campo
    """

    def value(self, n):
        field = self.field(n)
        v = field.value

        if field.value is not None:
            if field.type_ in ("str", "pixmap", "time", "date"):
                try:
                    v = str(field.value)
                except Exception:
                    v = ""

            elif field.type_ in ("int", "uint", "serial"):
                try:
                    v = int(field.value)
                except Exception:
                    v = 0.0

            elif field.type_ == "double":
                try:
                    v = float(field.value)
                    if v == int(field.value):
                        v = int(field.value)
                except Exception:
                    v = 0.0

        if field.type_ in ("bool", "unlock"):
            v = field.value in (True, "true")

        # ret = self.convertToType(field.value, field.type_)
        # logger.trace("---->retornando %s %s %s",v , type(v), field.value, field.name)
        return v

    """
    Setea el valor de un campo del buffer
    @param name. Nombre del campo
    @param value. Valor a asignar al campo
    @param mark_. Si True comprueba que ha cambiado respecto al valor asignado en primeUpdate
                y si ha cambiado lo marca como modificado (Por defecto a True)
    """

    def setValue(self, name, value, mark_=True):
        if value is not None and not isinstance(value, (int, float, str, datetime.time, datetime.date, bool, types.Date, bytearray)):
            raise ValueError("No se admite el tipo %r , en setValue(%s,%r)" % (type(value), name, value))

        field = self.field(name)

        if field is None:
            return False

        elif field.type_ == "double" and value not in ("", "-", None):
            if isinstance(value, str) and value.find(":") > -1:
                # Convertimos a horas
                list_ = value.split(":")
                value = float(list_[0])  # Horas
                value += float(list_[1]) / 60  # Minutos a hora
                value += float(list_[2]) / 3600  # Segundos a hora

            else:
                if isinstance(value, str) and value.find(",") > -1:
                    value = value.replace(",", "")

                value = float(value)

        elif field.type_ in ("string", "stringlist") and not isinstance(value, str) and value is not None:
            value = str(value)

        elif field.type_ == "time":
            if value is not None:
                if isinstance(value, types.Date):
                    value = value.toString()
                elif isinstance(value, datetime.timedelta):
                    value = str(value)
            if isinstance(value, str) and value.find("T") > -1:
                value = value[value.find("T") + 1 :]

        elif field.type_ == "date":
            if isinstance(value, types.Date):
                value = value.toString()

            if isinstance(value, str):
                if value.find("T") > -1:
                    value = value[: value.find("T")]
                list_ = value.split("-")
                value = datetime.date(int(list_[0]), int(list_[1]), int(list_[2]))

        if self.hasChanged(field.name, value):

            field.value = value

            if mark_:
                if not field.value == field.originalValue:
                    field.modified = True
                else:
                    field.modified = False
                    # self.setMd5Sum(value)

        return True

    """
    Comprueba si un campo tiene valor diferente. Esto es especialmente util para los número con decimales
    @return True si ha cambiado, False si es el mismo valor
    """

    def hasChanged(self, name, value):

        field = self.field(name)

        if value is None and field.value is None:
            return False

        elif value in (None, "None"):
            return True

        if field.name == name:
            type_ = field.type_
            actual = field.value
            if actual in (None, "None"):
                return True

            if (actual == "" and value != "") or (actual != "" and value == ""):
                return True
            elif type_ in ("string", "stringlist"):
                return not (actual == value)
            elif type_ in ("int", "uint", "serial"):
                return not (str(actual) == str(value))
            elif type_ == "double":
                if value == "-":
                    return False

                if actual == "-":
                    return True
                try:
                    return not (float(actual) == float(value))
                except Exception:
                    return True
            elif type_ == "date":
                return not str(field.value) == str(value)

            else:
                return True

        return True

    """
    Indica al cursor que pertenecemos
    @return Cursor al que pertenecemos
    """

    def cursor(self):
        return self.cursor_

    """
    Retorna los campos del buffer modificados desde original
    @return array Lista de campos modificados
    """

    def modifiedFields(self):
        lista = []
        for f in self.fieldsList():
            if f.modified:
                lista.append(f.name)

        return lista

    """
    Setea todos los campos como no modificados
    """

    def setNoModifiedFields(self):
        for f in self.fieldsList():
            if f.modified:
                f.modified = False

    """
    Indica que campo del buffer es clave primaria
    @return Nombre del campo que es clave primaria
    """

    def pK(self):
        for f in self.fieldsList():
            if f.metadata.isPrimaryKey():
                return f.name

        logger.warning("PNBuffer.pk(): No se ha encontrado clave Primaria")

    """
    Indica la posicion del buffer de un campo determinado
    @param name
    @return Posición del campo a buscar
    """

    def indexField(self, name):
        i = 0
        for f in self.fieldsList():
            if f.name == name:
                return i

            i = i + 1

    def fieldsList(self):
        return self.fieldList_

    def field(self, n):
        if isinstance(n, str):
            for f in self.fieldsList():
                if f.name.lower() == n.lower():
                    return f
        else:
            i = 0
            for f in self.fieldsList():
                if i == n:
                    return f

                i = i + 1

        return None
