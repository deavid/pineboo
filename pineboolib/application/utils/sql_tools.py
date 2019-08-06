"""
Collect information from the query, such as field tables, lines, etc ...
"""

from pineboolib.core.utils import logging
import datetime
from typing import Dict, Iterable, Tuple, Union, Any, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from pineboolib.interfaces.ifieldmetadata import IFieldMetaData  # noqa: F401

logger = logging.getLogger(__name__)


class SqlInspector(object):
    """SqlInspector Class."""

    _sql_list: List[str]
    _sql: str
    _invalid_tables: List[str]

    def __init__(self, sql_text: str) -> None:
        """
        Initialize the class.

        @param sql_text . query string.
        """

        self._invalid_tables = []
        self._mtd_fields: Dict[int, "IFieldMetaData"] = {}
        self._field_names: Dict[str, int] = {}
        self._table_names: List[str] = []
        self._alias: Dict[str, str] = {}
        self._posible_float = False
        sql_text = sql_text.replace("\n", " ")
        sql_text = sql_text.replace("\t", " ")
        sql_text = sql_text.strip()
        self._sql = sql_text
        if sql_text.startswith("show"):
            return
        else:
            self._resolve_fields(sql_text)

            # self.table_names()
            # self.field_names()

    def mtd_fields(self) -> Dict[int, Any]:
        """
        Return a dictionary with the fields of the query.

        @return fields dictionary.
        """

        return self._mtd_fields

    def table_names(self) -> List[str]:
        """
        Return a list with the tables of the query.

        @return tables list.
        """

        return self._table_names

    def field_names(self) -> List[str]:  # FIXME: This does NOT preserve order!
        """
        Return a list with the name of the fields.

        @return fields list.
        """

        return list(self._field_names.keys())

    def fieldNameToPos(self, name: str) -> int:
        """
        Return the position of a field, from the name.

        @param name. field name.
        @return index position.
        """

        if name in self._field_names.keys():
            return self._field_names[name]
        else:
            if name.find(".") > -1:
                table_name = name[0 : name.find(".")]
                field_name = name[name.find(".") + 1 :]
                if table_name in self._alias.keys():
                    table_name = self._alias[table_name]
                    return self.fieldNameToPos("%s.%s" % (table_name, field_name))

        raise Exception("No se encuentra el campo %s el la query:\n%s" % (name, self._sql))

    def posToFieldName(self, pos) -> str:
        """
        Return the name of a field, from the position.

        @param name. field name.
        @return field name.
        """

        for k, v in self._field_names:
            if v == pos:
                return k

        raise Exception("fieldName not found!")

    def _resolve_fields(self, sql) -> None:
        """
        Break the query into the different data.

        @param sql. Quey string.
        """

        list_sql = sql.split(" ")

        if list_sql[0] == "select":
            if "from" not in list_sql:
                return  # Se entiende que es una consulta especial

            index_from = list_sql.index("from")
            fl: List[str] = []
            fields_list = list_sql[1:index_from]
            for field in fields_list:
                field = field.replace(" ", "")
                if field.find(",") > -1:
                    field = field.split(",")
                    fl = fl + field
                else:
                    fl.append(field)

            fields_list = fl
            fl = []
            for f in list(fields_list):
                if f == "":
                    continue
                fl.append(f)

            if "where" in list_sql:
                index_where = list_sql.index("where")
                tl = list_sql[index_from + 1 : index_where]
            else:
                tl = list_sql[index_from + 1 :]

            tablas = []
            self._alias = {}
            jump = 0
            # next_is_alias = None
            prev_ = ""
            last_was_table = False
            for t in tl:
                if jump > 0:
                    jump -= 1
                    prev_ = t
                    last_was_table = False
                    continue

                # if next_is_alias:
                #    alias[t] = next_is_alias
                #    next_is_alias = None
                #    prev_ = t
                #    continue

                # elif t in ("inner", "on"):
                #    print("Comprobando")
                #    if prev_ not in tablas:
                #        alias[prev_] = tablas[:-1]

                elif t == "on":
                    jump = 3
                    prev_ = t
                    last_was_table = False

                elif t in ("left", "join", "right", "inner", "outer"):
                    prev_ = t
                    last_was_table = False
                    continue

                # elif t == "on":
                # jump = 3
                #    prev_ = t
                #    continue
                # elif t == "as":
                #    next_is_alias = True
                #    continue
                else:
                    if last_was_table:
                        self._alias[t] = prev_
                        last_was_table = False
                    else:
                        tablas.append(t)
                        last_was_table = True
                    prev_ = t

            temp_tl: List[str] = []
            for t in tablas:
                temp_tl = temp_tl + t.split(",")

            tablas = temp_tl

            fl_finish = []
            for f in fl:
                field_name = f
                if field_name.find(".") > -1:
                    a_ = field_name[0 : field_name.find(".")]
                    f_ = field_name[field_name.find(".") + 1 :]
                    if a_.find("(") > -1:
                        a = a_[a_.find("(") + 1 :]
                    else:
                        a = a_

                    if a in self._alias.keys():
                        field_name = "%s.%s" % (a_.replace(a, self._alias[a]), f_)

                fl_finish.append(field_name)

            self._create_mtd_fields(fl_finish, tablas)

    def resolve_empty_value(self, pos) -> Any:
        """
        Return a data type according to field type and value None.

        @param pos. index postion.
        """

        if not self.mtd_fields():
            if self._sql.find("sum(") > -1:
                return 0
            return None

        type_ = "double"
        if pos not in self._mtd_fields.keys():
            if pos not in self._field_names.values():
                logger.warning(
                    "SQL_TOOLS : resolve_empty_value : No se encuentra la posición %s", pos
                )
                return None
        else:
            mtd = self._mtd_fields[pos]
            if mtd is not None:
                type_ = mtd.type()

        ret_: Any = None
        if type_ in ("double", "int", "uint", "serial"):
            ret_ = 0
        elif type_ in ("string", "stringlist", "pixmap"):
            ret_ = ""
        elif type_ in ("unlock", "bool"):
            ret_ = False
        elif type_ == "date":
            from pineboolib.application import types

            ret_ = types.Date()
        elif type_ == "time":
            ret_ = "00:00:00"
        elif type_ == "bytearray":
            ret_ = bytearray()

        return ret_

    def resolve_value(self, pos, value: Union[bytes, float, str, datetime.time], raw=False) -> Any:
        """
        Return a data type according to field type.

        @param pos. index postion.
        """

        if not self.mtd_fields():
            if isinstance(value, datetime.time):
                value = str(value)[0:8]
            return value

        type_ = "double"
        if pos not in self._mtd_fields.keys():
            if pos not in self._field_names.values():
                print(pos, self._field_names)
                logger.warning("SQL_TOOLS : resolve_value : No se encuentra la posición %s", pos)
                return None
        else:
            mtd = self._mtd_fields[pos]
            if mtd is not None:
                type_ = mtd.type()

        ret_: Any = value
        if type_ in ("string", "stringlist"):
            pass
        elif type_ == "double":
            ret_ = float(ret_)
        elif type_ in ("int", "uint", "serial"):
            ret_ = int(ret_)
        elif type_ == "pixmap":
            from pineboolib.application import project

            if project.conn is None:
                raise Exception("Project is not connected yet")

            metadata = mtd.metadata()
            if metadata is None:
                raise Exception("Metadata not found")
            if raw or not project.conn.manager().isSystemTable(metadata.name()):
                ret_ = project.conn.manager().fetchLargeValue(ret_)
        elif type_ == "date":
            from pineboolib.application import types

            ret_ = types.Date(str(ret_))
        elif type_ == "time":
            ret_ = str(ret_)
            if ret_.find(".") > -1:
                ret_ = ret_[0 : ret_.find(".")]
            elif ret_.find("+") > -1:
                ret_ = ret_[0 : ret_.find("+")]

        elif type_ in ("unlock", "bool"):
            pass
        elif type_ == "bytearray":
            ret_ = bytearray(ret_)
        else:
            ret_ = float(ret_)
            print("TIPO DESCONOCIDO", type_, ret_)

        return ret_

    def _create_mtd_fields(self, fields_list: Iterable, tables_list: Iterable) -> None:
        """
        Solve the fields that make up the query.

        @param fields_list. fields list.
        @param tables_list. tables list.
        """

        from pineboolib.application import project

        if project.conn is None:
            raise Exception("Project is not connected yet")

        _filter = ["sum(", "max(", "distint("]

        self._mtd_fields = {}
        self._invalid_tables = []
        self._table_names = list(tables_list)
        self._field_names = {k: n for n, k in enumerate(fields_list)}

        for number_, field_name_org in enumerate(list(fields_list)):
            # self._field_names.append(field_name_org)
            field_name = field_name_org
            for table_name in list(tables_list):
                mtd_table = project.conn.manager().metadata(table_name)
                if mtd_table is not None:
                    for fil in _filter:
                        if field_name.startswith(fil):
                            field_name = field_name.replace(fil, "")
                            field_name = field_name[:-1]

                    if field_name.find(".") > -1:
                        if table_name != field_name[0 : field_name.find(".")]:
                            continue
                        else:
                            field_name = field_name[field_name.find(".") + 1 :]
                    mtd_field = mtd_table.field(field_name)
                    if mtd_field is not None:
                        self._mtd_fields[number_] = mtd_field
                    # fields_list.remove(field_name_org)
            else:
                if table_name not in self._invalid_tables:
                    self._invalid_tables.append(table_name)
                    # tables_list.remove(table_name)


def resolve_query(table_name: str, params: Dict[str, str]) -> Tuple[str, str]:
    """
    Solve the information of a DJANGO query.
    """

    or_where = ""
    and_where = ""
    where = ""
    order_by = ""
    from pineboolib.application import project

    if project.conn is None:
        raise Exception("Project is not connected yet")

    mtd = project.conn.manager().metadata(table_name)

    if hasattr(params, "_iterlists"):
        q: Any = params
        params = {k: q.getlist(k) if len(q.getlist(k)) > 1 else v for k, v in q.items()}

    for p in params:
        if p.startswith("q_"):
            or_where += " OR " if len(or_where) else ""
            or_where += resolve_where_params(p, params[p], mtd)
        elif p.startswith("s_"):
            and_where += " AND " if len(and_where) else ""
            and_where += resolve_where_params(p, params[p], mtd)
        elif p.startswith("o_"):
            order_by += resolve_order_params(p, params[p])

    if and_where != "":
        where += str(and_where)
    if or_where != "":
        where += " AND (" + str(or_where) + ")" if len(where) else str(or_where)
    if order_by:
        order_by = order_by.strip()[:-1]

    where = "1=1" if not len(where) else where

    return where, order_by


def resolve_order_params(key, valor: str) -> Any:
    """
    Solve the order information of a DJANGO query.
    """

    if valor.startswith("-"):
        valor = valor[1:] + " DESC, "
    else:
        valor += ", "

    return valor


def resolve_where_params(key: str, valor: Optional[str], mtd_table) -> str:
    """Solve where information from a DJANGO query."""

    list_params = key.split("__")
    campo = "_".join(list_params[0].split("_")[1:])
    tipo = list_params[1]
    where = ""
    if campo == "pk":
        return "1=1"

    if tipo.endswith("[]"):
        tipo = tipo[:-2]

    if valor is None:
        return "%s = ''" % campo

    field = mtd_table.field(campo)
    if field is not None:
        field_type = field.type()
    else:
        logger.warning(
            "pineboolib.utils.resolve_where_params No se encuentra el campo %s en la tabla %s.",
            campo,
            mtd_table.name(),
        )
        return ""
    # valor = aqApp.db().manager().formatValue(field_type , valor, False)

    if field_type in ["bool", "unlock"]:
        valor = "True" if valor == "true" else "False"

    if tipo == "contains":
        where = campo + " LIKE '%" + valor + "%'"
    elif tipo == "icontains":
        where = "UPPER(CAST(" + campo + " AS TEXT)) LIKE UPPER('%" + valor + "%')"
    elif tipo == "exact":
        where = campo + " = '" + valor + "'"
    elif tipo == "iexact":
        where = "UPPER(CAST(" + campo + " AS TEXT)) = UPPER('" + valor + "')"
    elif tipo == "startswith":
        where = campo + " LIKE '" + valor + "%'"
    elif tipo == "istartswith":
        where = campo + " ILIKE '" + valor + "%'"
    elif tipo == "endswith":
        where = campo + " LIKE '%" + valor + "'"
    elif tipo == "iendswith":
        where = campo + " ILIKE '%" + valor + "'"
    elif tipo == "lt":
        where = campo + " < '" + valor + "'"
    elif tipo == "lte":
        where = campo + " <= '" + valor + "'"
    elif tipo == "gt":
        where = campo + " > '" + valor + "'"
    elif tipo == "gte":
        where = campo + " >= '" + valor + "'"
    elif tipo == "ne":
        where = campo + " <> '" + valor + "'"
    elif tipo == "in":
        where = campo + " IN ('" + "', '".join(valor) + "')"

    return where


def resolve_pagination(query: Dict[str, Any]) -> Tuple[str, str]:
    """Solve the pagination of a DJANGO query."""

    init = 0
    limit = 0
    for k, v in query.items():
        if k.startswith("p_"):
            if k.endswith("l"):
                limit = v
            elif k.endswith("o"):
                init = v

                # if query[k] == "true":
                #    page = 0
                # else:
                #    page = int(v)

    if limit != 0:
        # init = page * limit
        return (str(init), str(limit))
    else:
        return ("0", "50")


def get_tipo_aqnext(tipo) -> int:
    """Solve the type of data used by DJANGO."""

    tipo_ = 3
    # subtipo_ = None

    if tipo in ["int", "uint", "serial"]:
        tipo_ = 16
    elif tipo in ["string", "stringlist", "pixmap", "counter"]:
        tipo_ = 3
    elif tipo in ["double"]:
        tipo_ = 19
    elif tipo in ["bool", "unlock"]:
        tipo_ = 18
    elif tipo in ["date"]:
        tipo_ = 26
    elif tipo in ["time"]:
        tipo_ = 27

    return tipo_
