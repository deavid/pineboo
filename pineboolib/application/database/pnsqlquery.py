# -*- coding: utf-8 -*-
"""
Module for PNSqlQuery class.
"""

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
    PNSqlQueryPrivate class.

    Store internal values ​​of the query.
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

    _last_query: Union[bool, str]

    def __init__(self, name: Optional[str] = None) -> None:
        """Create a new instance of PNSqlQueryPrivate."""

        if name:
            self.name_ = name
        self.parameterDict_ = {}
        self.groupDict_ = {}
        self.fieldMetaDataList_ = {}
        self.orderBy_ = None
        self.where_ = ""
        self._last_query = False


class PNSqlQuery(object):
    """
    Handle queries with specific features.

    It offers the functionality to handle QSqlQuery queries and also offers methods
    to work with parameterized queries and grouping levels.
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
        """
        Initialize a new query.
        """

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
        """
        Delete cursor properties when closing.
        """

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
        """
        Return a sql inspector instance.

        Collect a query and return information about its composition.
        @return sql_inspector
        """

        if self._sql_inspector is None:
            logger.warning("sql_inspector: Query has not executed yet", stack_info=True)
            sql = self.sql()
            self._sql_inspector = sql_tools.sql_inspector(sql.lower())
        return self._sql_inspector

    def exec_(self, sql: Optional[str] = None) -> bool:
        """
        Run a query.

        This can be specified or calculated from the values ​​previously provided.
        @param sql. query text.
        @return True or False return if the execution is successful.
        """

        if self.invalidTablesList:
            return False

        if not sql:
            sql = self.sql()
        if not sql:
            return False

        self._sql_inspector = sql_tools.sql_inspector(sql.lower())

        sql = self.db().driver().fix_query(sql)
        if sql is None:
            raise Exception("The query is empty!")

        self._last_query = sql
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

    def addParameter(self, p: Optional["PNParameterQuery"]) -> None:
        """
        Add the parameter description to the parameter dictionary.

        @param p FLParameterQuery object with the description of the parameter to add.
        """

        if p:
            self.d.parameterDict_[p.name()] = p

    def addGroup(self, g: Optional["PNGroupByQuery"]) -> None:
        """
        Add a group description to the group dictionary.

        @param g PNGroupByQuery object with the description of the group to add.
        """

        if g:
            if not self.d.groupDict_:
                self.d.groupDict_ = {}

            self.d.groupDict_[g.level()] = g.field()

    def setName(self, name: str) -> None:
        """
        To set the name of the query.

        @param name. query name.
        """
        self.d.name_ = name

    def name(self) -> str:
        """
        To get the name of the query.
        """

        return self.d.name_

    def select(self) -> str:
        """
        To get the SELECT part of the SQL statement from the query.

        @return text string with the query SELECT.
        """

        return ",".join(self.d.fieldList_)

    def from_(self) -> str:
        """
        To get the FROM part of the SQL statement from the query.

        @return text string with the query FROM.
        """

        return self.d.from_

    def where(self) -> str:
        """
        To get the WHERE part of the SQL statement from the query.

        @return text string with the query WHERE.
        """

        return self.d.where_

    def orderBy(self) -> Optional[str]:
        """
        To get the ORDERBY part of the SQL statement from the query.

        @return text string with the query ORDERBY.
        """

        return self.d.orderBy_

    def setSelect(self, select: Union[str, List, "Array"], sep: str = ",") -> None:
        """
        To set the SELECT part of the SQL statement of the query.

        @param s Text string with the SELECT part of the SQL statement that
            Generate the query. This string should NOT include the reserved word.
            SELECT, nor the character '*' as a wild card. Only support the list
            of fields that should appear in the query separated by the string
            indicated in the parameter 'sep'
        @param sep String used as a separator in the field list. Default the comma is used.
        """

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

    def setFrom(self, f: str) -> None:
        """
        To set the FROM part of the SQL statement of the query.

        @param f Text string with the FROM part of the SQL statement that generate the query
        """

        self.d.from_ = f
        # self.d.from_ = f.strip_whitespace()
        # self.d.from_ = self.d.from_.simplifyWhiteSpace()

    def setWhere(self, w: str) -> None:
        """
        To set the WHERE part of the SQL statement of the query.

        @param s Text string with the WHERE part of the SQL statement that generates the query.
        """

        self.d.where_ = w
        # self.d.where_ = w.strip_whitespace()
        # self.d.where_ = self.d.where_.simplifyWhiteSpace()

    def setOrderBy(self, w: str) -> None:
        """
        To set the ORDER BY part of the SQL statement of the query.

        @param s Text string with the ORDER BY part of the SQL statement that generate the query
        """
        self.d.orderBy_ = w
        # self.d.orderBy_ = w.strip_whitespace()
        # self.d.orderBy_ = self.d.orderBy_.simplifyWhiteSpace()

    def sql(self) -> str:
        """
        To get the full SQL statement of the query.

        This method joins the three parts of the query (SELECT, FROM AND WHERE),
        replace the parameters with the value they have in the dictionary and return all in a text string.
        @return Text string with the full SQL statement that generates the query.
        """
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

    def parameterDict(self) -> Dict[str, Any]:
        """
         To obtain the parameters of the query.

        @return Parameter dictionary
        """
        return self.d.parameterDict_

    def groupDict(self) -> Dict[int, Any]:
        """
        To obtain the grouping levels of the query.

        @return Dictionary of grouping levels.
        """

        return self.d.groupDict_

    def fieldList(self) -> List[str]:
        """
        To get the list of field names.

        @return List of text strings with the names of the fields in the query.
        """

        if self.d.fieldList_:
            return self.d.fieldList_
        else:
            return self.sql_inspector.field_names()

    def setGroupDict(self, gd: Dict[int, Any]) -> None:
        """
        Assign a parameter dictionary to the query parameter dictionary.

        The parameter dictionary of the FLGroupByQueryDict type, already built,
        It is assigned as the new group dictionary of the query, in the event that
        There is already a dictionary of groups, this is destroyed and overwritten by the new one.
        The dictionary passed to this method becomes the property of the query, and she is the
        responsible for deleting it. If the dictionary to be assigned is null or empty this
        method does nothing.

        @param gd Dictionary of parameters.
        """
        if not gd:
            return

        self.d.groupDict_ = gd

    def setParameterDict(self, pd: Dict[str, Any]) -> None:
        """
        Assign a group dictionary to the group dictionary of the query.

        The group dictionary of the FLParameterQueryDict type, already built,
        It is assigned as the new dictionary of query parameters, in the event that
        There is already a dictionary of parameters, it is destroyed and overwritten by the new one.
        The dictionary passed to this method becomes the property of the query, and she is the
        responsible for deleting it. If the dictionary to be assigned is null or empty this
        method does nothing.

        @param pd Parameter dictionary
        """

        if not pd:
            return

        self.d.parameterDict_ = pd

    def showDebug(self) -> None:
        """
        Show the content of the query, by the standard output.

        It is intended only for debugging tasks.
        """
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

    def _value_quick(self, n: Union[str, int], raw: bool = False) -> Any:
        """Quick mode."""
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
        """Standart mode."""

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
        """
        Get the value of a query field.

        Given a name of a query field, this method returns a QVariant object
        with the value of that field. The name must correspond to the one placed in
        the SELECT part of the SQL statement of the query.

        @param n Name of the query field
        @param raw If TRUE and the value of the field is a reference to a large value
             (see FLManager :: storeLargeValue ()) returns the value of that reference,
             instead of content to which that reference points

        """
        _value = self._value_std

        if config.value("ebcomportamiento/std_query", False):
            _value = self._value_std
        return _value(n, raw)

    def isNull(self, n: str) -> bool:
        """
        Indicate whether a query field is null or not.

        Given a name of a query field, this method returns true if the query field is null.
        The name must correspond to the one placed in
        the SELECT part of the SQL statement of the query.

        @param n Name of the query field
        """

        if isinstance(n, str):
            pos_ = self.fieldNameToPos(n)

            return self._row[pos_] in (None, "None")

        raise Exception("isNull. field not found %s" % n)

    def posToFieldName(self, p: int) -> str:
        """
        Return the field name, given its position in the query.

        @param p Position of the field in the query, start at zero and left to right.
        @return Name of the corresponding field. If the field does not exist, it returns None.
        """
        return self.sql_inspector.posToFieldName(p)
        # if p < 0 or p >= len(self.d.fieldList_):
        #    return None
        # ret_ = None
        # try:
        #    ret_ = self.d.fieldList_[p]
        # except Exception:
        #    pass

        # return ret_

    def fieldNameToPos(self, name: str) -> int:
        """
        Return the position of a field in the query, given its name.

        @param n Field Name.
        @return Position of the field in the query. If the field does not exist, return -1.
        """

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

    def tablesList(self) -> List[str]:
        """
        To get the list of names of the query tables.

        @return List of names of the tables that become part of the query.
        """

        if self.d.tablesList_:
            return self.d.tablesList_
        else:
            return self.sql_inspector.table_names()

    def setTablesList(self, tl: Union[str, List]) -> None:
        """
        Set the list of names of the query tables.

        @param tl Text list (or a list) with the names of the tables separated by commas, e.g. "table1, table2, table3"
        """
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

    def setValueParam(self, name: str, v: Any) -> None:
        """
        Set the value of a parameter.

        @param name Parameter name.
        @param v Value for the parameters.
        """

        self.d.parameterDict_[name] = v

    def valueParam(self, name: str) -> Any:
        """
        Get the value of a parameter.

        @param name Parameter name.
        """

        if name in self.d.parameterDict_.keys():
            return self.d.parameterDict_[name]
        else:
            return None

    def size(self) -> int:
        """
        Report the number of results returned by the query.

        @return number of results.
        """
        return len(self._datos)

    def fieldMetaDataList(self) -> Any:
        """
        To get the list of query field definitions.

        @return Object with the list of deficiencies in the query fields.
        """

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

    def db(self) -> "IConnection":
        """
        Get the database you work on.

        @return PNConnection user by the query.
        """
        return self.d.db_

    def isValid(self) -> bool:
        """
        Return if the query has an invalid defined table.

        @return True or False.
        """

        return False if self.invalidTablesList else True

    def isActive(self) -> bool:
        """
        Indicate whether the data has been collected completely.

        @return True or False.
        """
        return self._is_active

    def at(self) -> Any:
        """
        Return the current position in the result list.

        @return line position.
        """

        return self._posicion

    def lastQuery(self) -> Union[bool, str]:
        """
        Return the last query made.

        @return query string.
        """

        return self._last_query

    def numRowsAffected(self) -> int:
        """
        Return Number of lines selected in the query.

        @return number of lines.
        """
        return len(self._datos)

    @decorators.NotImplementedWarn
    def lastError(self):
        """Not Implemented."""
        pass

    @decorators.NotImplementedWarn
    def isSelect(self):
        """Not Implemented."""
        pass

    @decorators.NotImplementedWarn
    def QSqlQuery_size(self):
        """Not Implemented."""
        pass

    @decorators.NotImplementedWarn
    def driver(self):
        """Not Implemented."""
        pass

    @decorators.NotImplementedWarn
    def result(self):
        """Not Implemented."""
        pass

    @decorators.NotImplementedWarn
    def isForwardOnly(self):
        """Not Implemented."""
        pass

    def setForwardOnly(self, forward) -> None:
        """Deprecated."""
        # No sirve para nada , por ahora
        pass

    @decorators.NotImplementedWarn
    def QSqlQuery_value(self, i):
        """Not Implemented."""
        pass

    def seek(self, i: int, relative=False) -> bool:
        """
        Position the cursor on a given result.

        @param i Position to search.
        @param relative Boolean indicates if the position is relative or absolut.
        @return True or False.
        """

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
        """
        Position the query cursor in the next record.

        @return True or False.
        """
        if not self._cursor:
            return False

        if self._datos:
            self._posicion += 1
            if self._posicion < len(self._datos):
                self._row = self._datos[self._posicion]
                return True

        return False

    def prev(self) -> bool:
        """
        Position the query cursor in the provious record.

        @return True or False.
        """
        if not self._cursor:
            return False

        if self._datos:
            self._posicion -= 1
            if self._posicion >= 0:
                self._row = self._datos[self._posicion]
                return True

        return False

    def first(self) -> bool:
        """
        Position the query cursor in the first record.

        @return True or False.
        """
        if not self._cursor:
            return False

        if self._datos:
            self._posicion = 0
            self._row = self._datos[self._posicion]
            return True

        return False

    def last(self) -> bool:
        """
        Position the query cursor in the last record.

        @return True or False.
        """
        if not self._cursor:
            return False

        if self._datos:
            self._posicion = len(self._datos) - 1
            self._row = self._datos[self._posicion]
            return True

        return False

    @decorators.NotImplementedWarn
    def prepare(self, query):
        """Not Implemented."""
        pass

    @decorators.NotImplementedWarn
    def bindValue(self, *args):
        """Not Implemented."""
        pass

    @decorators.NotImplementedWarn
    def addBindValue(self, *args):
        """Not Implemented."""
        pass

    @decorators.NotImplementedWarn
    def boundValue(self, *args):
        """Not Implemented."""
        pass

    @decorators.NotImplementedWarn
    def boundValues(self):
        """Not Implemented."""
        pass

    @decorators.NotImplementedWarn
    def executedQuery(self):
        """Not Implemented."""
        pass
