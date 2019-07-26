from pineboolib.core.utils import logging
from pineboolib.core import decorators
from pineboolib.core.settings import config
from pineboolib.application.utils import sql_tools
from pineboolib.application import project
from pineboolib.interfaces.ifieldmetadata import IFieldMetaData
from typing import Any, Union, List, Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from pineboolib.interfaces.iconnection import IConnection  # noqa: F401
    from pineboolib.interfaces.iapicursor import IApiCursor  # noqa: F401
    from pineboolib.application.types import Array  # noqa: F401
    from .pnparameterquery import PNParameterQuery  # noqa: F401
    from .pngroupbyquery import PNGroupByQuery  # noqa: F401

logger = logging.getLogger(__name__)


class PNSqlQueryPrivate(object):
    """
    Nombre de la consulta
    """

    name_: str

    """
    Parte FROM de la consulta
    """
    from_: str

    """
    Parte WHERE de la consulta
    """
    where_: str

    """
    Parte ORDER BY de la consulta
    """
    orderBy_: Optional[str]

    """
    Base de datos sobre la que trabaja
    """
    db_: "IConnection"

    """
    Lista de parámetros
    """
    parameterDict_: Dict[str, Any] = {}

    """
    Lista de grupos
    """
    groupDict_: Dict[int, Any] = {}

    """
    Lista de nombres de los campos
    """
    fieldList_: List[str]

    """
    Lista de nombres de las tablas que entran a formar
    parte en la consulta
    """
    tablesList_: List[str]

    """
    Lista de con los metadatos de los campos de la consulta
    """
    fieldMetaDataList_: Dict[str, IFieldMetaData]

    def __init__(self, name: Optional[str] = None) -> None:
        if name:
            self.name_ = name
        self.parameterDict_ = {}
        self.groupDict_ = {}
        self.fieldMetaDataList_ = {}
        self.orderBy_ = None
        self.where_ = ""


class PNSqlQuery(object):
    """
    Maneja consultas con características específicas para AbanQ, hereda de QSqlQuery.

    Ofrece la funcionalidad para manejar consultas de QSqlQuery y además ofrece métodos
    para trabajar con consultas parametrizadas y niveles de agrupamiento.

    @author InfoSiAL S.L.
    """

    countRefQuery: int = 0
    invalidTablesList = False
    _is_active: bool
    _fieldNameToPosDict: Optional[Dict[str, int]]
    _sql_inspector: Optional[sql_tools.sql_inspector]
    _row: List[Any]
    _datos: List[Any]
    _posicion: int
    _cursor: "IApiCursor"

    def __init__(self, cx=None, connection_name: Union[str, "IConnection"] = "default") -> None:
        # super(FLSqlQuery, self).__init__()

        if project.conn is None:
            raise Exception("Project is not connected yet")
        self._sql_inspector = None
        self._fieldNameToPosDict = None
        self.d = PNSqlQueryPrivate(cx)
        if isinstance(connection_name, str):
            self.d.db_ = project.conn.useConn(connection_name)
        else:
            self.d.db_ = connection_name

        self.countRefQuery = self.countRefQuery + 1
        self._row = []
        self._datos = []
        self.invalidTablesList = False
        self.d.fieldList_ = []
        self._is_active = False

        retornoQry = None
        if cx:
            retornoQry = project.conn.manager().query(cx, self)

        if retornoQry:
            self.d = retornoQry.d

    def __del__(self) -> None:
        try:
            del self.d
            del self._datos
            if self._cursor is not None:
                self._cursor.close()
                del self._cursor
        except Exception:
            pass

        self.countRefQuery = self.countRefQuery - 1

    @property
    def sql_inspector(self) -> sql_tools.sql_inspector:
        if self._sql_inspector is None:
            logger.warning("sql_inspector: Query has not executed yet", stack_info=True)
            sql = self.sql()
            self._sql_inspector = sql_tools.sql_inspector(sql.lower())
        return self._sql_inspector

    """
    Ejecuta la consulta
    """

    def exec_(self, sql: Optional[str] = None) -> bool:
        if self.invalidTablesList:
            return False

        if not sql:
            sql = self.sql()
        if not sql:
            return False

        self._sql_inspector = sql_tools.sql_inspector(sql.lower())

        sql = self.db().driver().fix_query(sql)

        try:

            self._cursor = self.db().cursor()
            if self._cursor is None:
                raise Exception("self._cursor is empty!")
            logger.trace("exec_: Ejecutando consulta: <%s> en <%s>", sql, self._cursor)
            self._cursor.execute(sql)
            self._datos = self._cursor.fetchall()
            self._posicion = -1
            self._is_active = True
        except Exception as exc:
            logger.error(exc)
            logger.info("Error ejecutando consulta: <%s>", sql)
            logger.trace("Detalle:", stack_info=True)
            return False
        # conn.commit()

        return True

    """
    Añade la descripción parámetro al diccionario de parámetros.

    @param p Objeto FLParameterQuery con la descripción del parámetro a añadir
    """

    def addParameter(self, p: Optional["PNParameterQuery"]) -> None:
        if p:
            self.d.parameterDict_[p.name()] = p

    """
    Añade la descripción de un grupo al diccionario de grupos.

    @param g Objeto FLGroupByQuery con la descripción del grupo a añadir
    """

    def addGroup(self, g: Optional["PNGroupByQuery"]) -> None:
        if g:
            if not self.d.groupDict_:
                self.d.groupDict_ = {}

            self.d.groupDict_[g.level()] = g.field()

    """
    Para establecer el nombre de la consulta.

    @param n Nombre de la consulta
    """

    def setName(self, n: str) -> None:
        self.d.name_ = n

    """
    Para obtener el nombre de la consulta
    """

    def name(self) -> str:
        return self.d.name_

    """
    Para obtener la parte SELECT de la sentencia SQL de la consulta
    """

    def select(self) -> str:
        return ",".join(self.d.fieldList_)

    """
    Para obtener la parte FROM de la sentencia SQL de la consulta
    """

    def from_(self) -> str:
        return self.d.from_

    """
    Para obtener la parte WHERE de la sentencia SQL de la consulta
    """

    def where(self) -> str:
        return self.d.where_

    """
    Para obtener la parte ORDER BY de la sentencia SQL de la consulta
    """

    def orderBy(self) -> Optional[str]:
        return self.d.orderBy_

    """
    Para establecer la parte SELECT de la sentencia SQL de la consulta.

    @param  s Cadena de texto con la parte SELECT de la sentencia SQL que
            genera la consulta. Esta cadena NO debe incluir la palabra reservada
            SELECT, ni tampoco el caracter '*' como comodín. Solo admite la lista
            de campos que deben aparecer en la consulta separados por la cadena
            indicada en el parámetro 'sep'
    @param  sep Cadena utilizada como separador en la lista de campos. Por defecto
              se utiliza la coma.
    """

    def setSelect(self, select: Union[str, List, "Array"], sep: str = ",") -> None:
        list_fields = []

        if isinstance(select, str):
            if sep in select:
                # s = s.replace(" ", "")

                prev = ""
                for f in select.split(sep):

                    field_ = prev + f
                    if field_.count("(") == field_.count(")"):
                        list_fields.append(field_)
                        prev = ""
                    else:
                        prev = "%s," % field_

        elif isinstance(select, list):
            list_fields = list(select)
        else:
            for k, v in select:
                list_fields.append(v)

            # s = s.split(sep)

        # self.d.select_ = s.strip_whitespace()
        # self.d.select_ = self.d.select_.simplifyWhiteSpace()

        if not list_fields and isinstance(select, str) and not "*" == select:
            self.d.fieldList_.clear()
            self.d.fieldList_.append(select)
            return

        # fieldListAux = s.split(sep)
        # for f in s:
        #    f = str(f).strip()

        table: Optional[str]
        field: Optional[str]
        self.d.fieldList_.clear()

        for f in list_fields:
            table = field = None
            try:
                if f.startswith(" "):
                    f = f[1:]
                table = f[: f.index(".")]
                field = f[f.index(".") + 1 :]
            except Exception:
                pass

            if field == "*" and not table:
                mtd = self.db().manager().metadata(table, True)
                if mtd is not None:
                    self.d.fieldList_ = mtd.fieldNames()
                    if not mtd.inCache():
                        del mtd

            else:
                self.d.fieldList_.append(f)

            # self.d.select_ = ",".join(self.d.fieldList_)

    """
    Para establecer la parte FROM de la sentencia SQL de la consulta.

    @param f Cadena de texto con la parte FROM de la sentencia SQL que
           genera la consulta
    """

    def setFrom(self, f: str) -> None:
        self.d.from_ = f
        # self.d.from_ = f.strip_whitespace()
        # self.d.from_ = self.d.from_.simplifyWhiteSpace()

    """
    Para establecer la parte WHERE de la sentencia SQL de la consulta.

    @param s Cadena de texto con la parte WHERE de la sentencia SQL que
        genera la consulta
    """

    def setWhere(self, w: str) -> None:
        self.d.where_ = w
        # self.d.where_ = w.strip_whitespace()
        # self.d.where_ = self.d.where_.simplifyWhiteSpace()

    """
    Para establecer la parte ORDER BY de la sentencia SQL de la consulta.

    @param s Cadena de texto con la parte ORDER BY de la sentencia SQL que
           genera la consulta
    """

    def setOrderBy(self, w: str) -> None:
        self.d.orderBy_ = w
        # self.d.orderBy_ = w.strip_whitespace()
        # self.d.orderBy_ = self.d.orderBy_.simplifyWhiteSpace()

    """
    Para obtener la sentencia completa SQL de la consulta.

    Este método une las tres partes de la consulta (SELECT, FROM Y WHERE),
    sustituye los parámetros por el valor que tienen en el diccionario y devuelve
    todo en una cadena de texto.

    @return Cadena de texto con la sentencia completa SQL que genera la consulta
    """

    def sql(self) -> str:
        # for tableName in self.d.tablesList_:
        #    if not self.d.db_.manager().existsTable(tableName) and not self.d.db_.manager().createTable(tableName):
        #        return

        res = None

        if not self.d.fieldList_:
            logger.warning("sql(): No select yet. Returning empty")
            return ""

        select = ",".join(self.d.fieldList_)

        if not self.d.from_:
            res = "SELECT %s" % select
        elif not self.d.where_:
            res = "SELECT %s FROM %s" % (select, self.d.from_)
        else:
            res = "SELECT %s FROM %s WHERE %s" % (select, self.d.from_, self.d.where_)

        if self.d.groupDict_ and not self.d.orderBy_:
            res = res + " ORDER BY "
            initGD = False
            i = 0
            while i < len(self.d.groupDict_):
                gD: str = self.d.groupDict_[i]
                if not initGD:
                    res = res + gD
                    initGD = True
                else:
                    res = res + ", " + gD

                i = i + 1

        elif self.d.orderBy_:
            res = res + " ORDER BY " + self.d.orderBy_

        if self.d.parameterDict_:
            for pD in self.d.parameterDict_.keys():
                v = self.d.parameterDict_[pD]

                if not v:
                    if not project._DGI:
                        raise Exception("project._DGI is empty!")
                    dialog = project.DGI.QInputDialog

                    if dialog is not None:
                        v = dialog.getText(None, "Entrada de parámetros de la consulta", pD)
                        if v:
                            v = v[0]

                res = res.replace("[%s]" % pD, "'%s'" % v)

        return res

    """
    Para obtener los parametros de la consulta.

    @return Diccionario de parámetros
    """

    def parameterDict(self) -> Dict[str, Any]:
        return self.d.parameterDict_

    """
    Para obtener los niveles de agrupamiento de la consulta.

    @return Diccionario de niveles de agrupamiento
    """

    def groupDict(self) -> Dict[int, Any]:
        return self.d.groupDict_

    """
    Para obtener la lista de nombres de los campos.

    @return Lista de cadenas de texto con los nombres de los campos de la
          consulta
    """

    def fieldList(self) -> List[str]:
        if self.d.fieldList_:
            return self.d.fieldList_
        else:
            return self.sql_inspector.field_names()

    """
    Asigna un diccionario de parámetros, al diccionario de parámetros de la consulta.

    El diccionario de parámetros del tipo FLGroupByQueryDict , ya construido,
    es asignado como el nuevo diccionario de grupos de la consulta, en el caso de que
    ya exista un diccionario de grupos, este es destruido y sobreescrito por el nuevo.
    El diccionario pasado a este método pasa a ser propiedad de la consulta, y ella es la
    encargada de borrarlo. Si el diccionario que se pretende asignar es nulo o vacío este
    método no hace nada.

    @param gd Diccionario de parámetros
    """

    def setGroupDict(self, gd: Dict[int, Any]) -> None:
        if not gd:
            return

        self.d.groupDict_ = gd

    """
    Asigna un diccionario de grupos, al diccionario de grupos de la consulta.

    El diccionario de grupos del tipo FLParameterQueryDict , ya construido,
    es asignado como el nuevo diccionario de parámetros de la consulta, en el caso de que
    ya exista un diccionario de parámetros, este es destruido y sobreescrito por el nuevo.
    El diccionario pasado a este método pasa a ser propiedad de la consulta, y ella es la
    encargada de borrarlo. Si el diccionario que se pretende asignar es nulo o vacío este
    método no hace nada.

    @param pd Diccionario de parámetros
    """

    def setParameterDict(self, pd: Dict[str, Any]) -> None:
        if not pd:
            return

        self.d.parameterDict_ = pd

    """
    Este método muestra el contenido de la consulta, por la sálida estándar.

    Está pensado sólo para tareas de depuración
    """

    def showDebug(self) -> None:
        if not self.isActive():
            logger.warning("DEBUG : La consulta no está activa : No se ha ejecutado exec() o la sentencia SQL no es válida")

        logger.warning("DEBUG : Nombre de la consulta : %s", self.d.name_)
        logger.warning("DEBUG : Niveles de agrupamiento :")
        if self.d.groupDict_:
            for lev in self.d.groupDict_.values():
                logger.warning("**Nivel : %s", lev.level())
                logger.warning("**Campo : %s", lev.field())
        else:
            logger.warning("**No hay niveles de agrupamiento")

        # logger.warning("DEBUG : Parámetros : ")
        # if self.d.parameterDict_:
        #     if par in self.d.parameterDict_:
        #         logger.warning("**Nombre : %s", par.name())
        #         logger.warning("Alias : %s", par.alias())
        #         logger.warning("Tipo : %s", par.type())
        #         logger.warning("Valor : %s", par.value())
        # else:
        #     logger.warning("**No hay parametros")

        logger.warning("DEBUG : Sentencia SQL")
        logger.warning("%s", self.sql())
        if not self.d.fieldList_:
            logger.warning("DEBUG ERROR : No hay campos en la consulta")
            return

        logger.warning("DEBUG: Campos de la consulta : ")
        for f in self.d.fieldList_:
            logger.warning("**%s", f)

        logger.warning("DEBUG : Contenido de la consulta : ")

        linea = ""

        for it in self.d.fieldList_:
            linea += "__%s" % self.value(it)

        logger.warning(linea)

    """
    Obtiene el valor de un campo de la consulta.

    Dado un nombre de un campo de la consulta, este método devuelve un objeto QVariant
    con el valor de dicho campo. El nombre debe corresponder con el que se coloco en
    la parte SELECT de la sentenica SQL de la consulta.

    @param n Nombre del campo de la consulta
    @param raw Si TRUE y el valor del campo es una referencia a un valor grande
             (ver FLManager::storeLargeValue()) devuelve el valor de esa referencia,
             en vez de contenido al que apunta esa referencia
    """

    def _value_quick(self, n: Union[str, int], raw: bool = False) -> Any:
        # Fast version of self.value
        if self._fieldNameToPosDict is None:
            self._fieldNameToPosDict = {v: n for n, v in enumerate(self.d.fieldList_)}
        try:
            if isinstance(n, int):
                ret = self._row[n]
            else:
                ret = self._row[self._fieldNameToPosDict[n]]
        except Exception as e:
            logger.debug("_value_quick: Error %s, falling back to default implementation", e)
            ret = self._value_std(n, raw)
        return ret

    def _value_std(self, n: Union[str, int, None], raw: bool = False) -> Any:
        if n is None:
            logger.trace("value::invalid use with n=None.", stack_info=True)
            return None

        if isinstance(n, str):
            pos: int = self.sql_inspector.fieldNameToPos(n.lower())
        if isinstance(n, int):
            pos = n

        ret = self._row[pos]

        if ret in (None, "None"):
            ret = self.sql_inspector.resolve_empty_value(pos)
        else:
            try:
                ret = self.sql_inspector.resolve_value(pos, ret, raw)
            except Exception:
                logger.exception("value::error retrieving row position %s", pos)

        return ret

    def value(self, n: Union[str, int], raw: bool = False) -> Any:
        _value = self._value_std

        if config.value("ebcomportamiento/std_query", False):
            _value = self._value_std
        return _value(n, raw)

    """
    def _value_std(self, n, raw=False):
        # Eneboo version
        pos = None
        name = None
        table_name = None
        field_name = None
        # field = None
        mtd_field = None
        retorno = None
        if n is None:
            self.logger.trace("value::invalid use with n=None.", stack_info=True)
            return None
        if isinstance(n, str):
            pos = self.fieldNameToPos(n)
            name = n
        else:
            pos = n
            name = self.posToFieldName(n)

        if name not in self.fields_cache.keys():
            self.logger.debug("value()::name %s not in cache", name)

            if name:
                tables_list = self.tablesList()
                if name.find(".") > -1 and name[0 : name.find(".")] in tables_list:
                    table_name = name[0 : name.find(".")]
                    field_name = name[name.find(".") + 1 :]
                else:
                    if not tables_list and self.from_():
                        tl = self.from_().replace(" ", "")
                        tables_list = tl.split(",")

                    for t in tables_list:
                        mtd = (
                            self.d.db_.manager().metadata(t, True)
                            if t.find("=") == -1
                            else None
                        )
                        name_fixed = name
                        if name_fixed.upper().startswith(
                            "SUM("
                        ) or name_fixed.upper().startswith("COUNT("):
                            name_fixed = name_fixed.replace(")", "")
                            name_fixed = name_fixed.replace("SUM(", "")
                            name_fixed = name_fixed.replace("COUNT(", "")

                        if mtd is not None and name_fixed in mtd.fieldNames():
                            table_name = t
                            field_name = name_fixed
                            break

                if field_name is not None:
                    mtd_field = (
                        self.d.db_.manager()
                        .metadata(table_name, False)
                        .field(field_name)
                    )
                    self.fields_cache[name] = mtd_field

        else:
            mtd_field = self.fields_cache[name]

        try:
            if self._row is not None:
                retorno = self._row[pos]
        except Exception:
            self.logger.exception("value::error retrieving row position %s", pos)

        if retorno is None:
            if mtd_field is not None:
                # retorno = self.db().formatValue(mtd_field.type(), None, False)
                if mtd_field.type() in ("double", "uint", "int"):
                    retorno = 0
                elif mtd_field.type() == "string":
                    retorno = ""
                elif mtd_field.type() == "bytearray":
                    retorno = bytearray()
            elif name and name.find("SUM(") > -1:
                retorno = 0
        else:
            import datetime

            if isinstance(retorno, str):  # str
                if mtd_field is not None:
                    if mtd_field.type() == "date":
                        retorno = pineboolib.qsa.Date(retorno)

                    elif mtd_field.type() == "pixmap":
                        if not raw:
                            if not self.d.db_.manager().isSystemTable(
                                mtd_field.metadata().name()
                            ):
                                raw = True
                        if raw:
                            retorno = self.d.db_.manager().fetchLargeValue(retorno)
                    elif mtd_field.type() == "string":
                        if retorno == "None":
                            retorno = ""

                elif retorno.find(":") > -1:
                    if retorno.find(":") < retorno.find("."):
                        retorno = retorno[: retorno.find(".")]

            elif isinstance(retorno, datetime.date):  # date
                retorno = pineboolib.qsa.Date(str(retorno))

            elif isinstance(retorno, float):  # float
                if retorno == int(retorno):
                    retorno = int(retorno)

            elif isinstance(retorno, (datetime.time, datetime.timedelta)):  # time
                retorno = str(retorno)[:8]
            # elif isinstance(retorno, memoryview):
            #    retorno = bytearray(retorno)
            elif not isinstance(retorno, (str, int, bool, float, pineboolib.qsa.Date)):
                retorno = float(retorno)

        return retorno
    """
    """
    Indica si un campo de la consulta es nulo o no

    Dado un nombre de un campo de la consulta, este método devuelve true si el campo de la consulta es nulo.
    El nombre debe corresponder con el que se coloco en
    la parte SELECT de la sentenica SQL de la consulta.

    @param n Nombre del campo de la consulta
    """

    def isNull(self, n: str) -> bool:
        if isinstance(n, str):
            pos_ = self.fieldNameToPos(n)

            return self._row[pos_] in (None, "None")

        raise Exception("isNull. field not found %s" % n)

    """
    Devuelve el nombre de campo, dada su posicion en la consulta.

    @param p Posicion del campo en la consulta, empieza en cero y de izquierda
       a derecha
    @return Nombre del campo correspondiente. Si no existe el campo devuelve
      QString::null
    """

    def posToFieldName(self, p: int) -> str:
        return self.sql_inspector.posToFieldName(p)
        # if p < 0 or p >= len(self.d.fieldList_):
        #    return None
        # ret_ = None
        # try:
        #    ret_ = self.d.fieldList_[p]
        # except Exception:
        #    pass

        # return ret_

    """
    Devuelve la posición de una campo en la consulta, dado su nombre.

    @param n Nombre del campo
    @return Posicion del campo en la consulta. Si no existe el campo devuelve -1
    """

    def fieldNameToPos(self, name: str) -> int:
        return self.sql_inspector.fieldNameToPos(name.lower())
        # i = 0
        # for field in self.d.fieldList_:
        #    if field.lower() == n.lower():
        #        return i
        #    i = i + 1
        # if n in self.d.fieldList_:
        #    return self.d.fieldList_.index(n)
        # else:
        #    return False

    """
    Para obtener la lista de nombres de las tablas de la consulta.

    @return Lista de nombres de las tablas que entran a formar parte de la
        consulta
    """

    def tablesList(self) -> List[str]:
        if self.d.tablesList_:
            return self.d.tablesList_
        else:
            return self.sql_inspector.table_names()

    """
    Establece la lista de nombres de las tablas de la consulta

    @param tl Cadena de texto con los nombres de las tablas
        separados por comas, p.e. "tabla1,tabla2,tabla3"
    """

    def setTablesList(self, tl: Union[str, List]) -> None:
        self.d.tablesList_ = []
        if isinstance(tl, list):
            table_list = ",".join(tl)
        else:
            table_list = tl

        table_list = table_list.replace(" ", "")
        for tabla in table_list.split(","):
            if not self.db().manager().existsTable(tabla) and len(table_list.split(",")) >= 1:
                self.invalidTablesList = True

            self.d.tablesList_.append(tabla)

    """
    Establece el valor de un parámetro.

    @param name Nombre del parámetro
    @param v Valor para el parámetros
    """

    def setValueParam(self, name: str, v: Any) -> None:
        self.d.parameterDict_[name] = v

    """
    Obtiene el valor de un parámetro.

    @param name Nombre del parámetro.
    """

    def valueParam(self, name: str) -> Any:
        if name in self.d.parameterDict_.keys():
            return self.d.parameterDict_[name]
        else:
            return None

    """
    Redefinicion del método size() de QSqlQuery
    """

    def size(self) -> int:
        return len(self._datos)

    """
    Para obtener la lista de definiciones de campos de la consulta

    @return Objeto con la lista de deficiones de campos de la consulta
    """

    def fieldMetaDataList(self) -> Any:
        if not self.d.fieldMetaDataList_:
            self.d.fieldMetaDataList_ = {}
        table = None
        field = None
        for f in self.d.fieldList_:
            table = f[: f.index(".")]
            field = f[f.index(".") + 1 :]
            mtd = self.db().manager().metadata(table, True)
            if not mtd:
                continue
            fd = mtd.field(field)
            if fd:
                self.d.fieldMetaDataList_[field.lower()] = fd

            if not mtd.inCache():
                del mtd

        return self.d.fieldMetaDataList_

    countRefQuery = 0

    """
    Para obtener la base de datos sobre la que trabaja
    """

    def db(self) -> "IConnection":
        return self.d.db_

    def isValid(self) -> bool:
        return False if self.invalidTablesList else True

    def isActive(self) -> bool:
        return self._is_active

    def at(self) -> Any:
        return self._posicion

    def lastQuery(self) -> Union[bool, str]:
        return self.sql()

    def numRowsAffected(self) -> int:
        return len(self._datos)

    @decorators.NotImplementedWarn
    def lastError(self):
        pass

    @decorators.NotImplementedWarn
    def isSelect(self):
        pass

    @decorators.NotImplementedWarn
    def QSqlQuery_size(self):
        pass

    @decorators.NotImplementedWarn
    def driver(self):
        pass

    @decorators.NotImplementedWarn
    def result(self):
        pass

    @decorators.NotImplementedWarn
    def isForwardOnly(self):
        pass

    def setForwardOnly(self, forward) -> None:
        # No sirve para nada , por ahora
        pass

    @decorators.NotImplementedWarn
    def QSqlQuery_value(self, i):
        pass

    def seek(self, i: int, relative=False) -> bool:
        if not self._cursor:
            return False

        pos = i
        if relative:
            pos = i + self._posicion

        if self._datos:
            if pos > 0 and pos < len(self._datos) - 1:
                self._posicion = pos
                self._row = self._datos[self._posicion]
                return True

        return False

    def next(self) -> bool:
        if not self._cursor:
            return False

        if self._datos:
            self._posicion += 1
            if self._posicion < len(self._datos):
                self._row = self._datos[self._posicion]
                return True

        return False

    def prev(self) -> bool:
        if not self._cursor:
            return False

        if self._datos:
            self._posicion -= 1
            if self._posicion >= 0:
                self._row = self._datos[self._posicion]
                return True

        return False

    def first(self) -> bool:
        if not self._cursor:
            return False

        if self._datos:
            self._posicion = 0
            self._row = self._datos[self._posicion]
            return True

        return False

    def last(self) -> bool:
        if not self._cursor:
            return False

        if self._datos:
            self._posicion = len(self._datos) - 1
            self._row = self._datos[self._posicion]
            return True

        return False

    @decorators.NotImplementedWarn
    def prepare(self, query):
        pass

    @decorators.NotImplementedWarn
    def bindValue(self, *args):
        pass

    @decorators.NotImplementedWarn
    def addBindValue(self, *args):
        pass

    @decorators.NotImplementedWarn
    def boundValue(self, *args):
        pass

    @decorators.NotImplementedWarn
    def boundValues(self):
        pass

    @decorators.NotImplementedWarn
    def executedQuery(self):
        pass
