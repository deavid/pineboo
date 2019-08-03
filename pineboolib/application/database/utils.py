"""
Provide some functions based on data.
"""

from pineboolib.core.utils import logging

from typing import Any, Union, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .pnsqlcursor import PNSqlCursor


logger = logging.getLogger("database.utils")


def nextCounter(
    name_or_series: str,
    cursor_or_name: Union[str, "PNSqlCursor"],
    cursor_: Optional["PNSqlCursor"] = None,
) -> Optional[Union[str, int]]:
    """
    Return the following value of a counter type field of a table.

    This method is very useful when inserting records in which
    the reference is sequential and we don't remember which one was the last
    number used The return value is a QVariant of the field type is
    the one that looks for the last reference. The most advisable thing is that the type
    of the field be 'String' because this way it can be formatted and be
    used to generate a barcode. The function anyway
    supports both that the field is of type 'String' and of type 'double'.

    @param name Field name
    @param cursor_ Cursor to the table where the field is located.
    @return Qvariant with the following number.
    @author Andrés Otón Urbano.
    """
    """
    dpinelo: This method is an extension of nextCounter but allowing the introduction of a first
    character sequence It is useful when we want to keep different counters within the same table.
    Example, Customer Group Table: We add a prefix field, which will be a letter: A, B, C, D.
    We want customer numbering to be of type A00001, or B000023. With this function, we can
    Keep using the counter methods when we add that letter.

    This method returns the following value of a counter type field of a table for a given series.

    This method is very useful when inserting records in which
    the reference is sequential according to a sequence and we don't remember which one was the last
    number used The return value is a QVariant of the field type is
    the one that looks for the last reference. The most advisable thing is that the type
    of the field be 'String' because this way it can be formatted and be
    used to generate a barcode. The function anyway
    supports both that the field is of type 'String' and of type 'double'.

    @param series series that differentiates counters
    @param name Field name
    @param cursor_ Cursor to the table where the field is located.
    @return Qvariant with the following number.
    @author Andrés Otón Urbano.
    """
    if cursor_ is None:
        from .pnsqlcursor import PNSqlCursor

        if not isinstance(cursor_or_name, PNSqlCursor):
            raise ValueError
        return _nextCounter_2(name_or_series, cursor_or_name)
    else:
        if not isinstance(cursor_or_name, str):
            raise ValueError
        return _nextCounter_3(name_or_series, cursor_or_name, cursor_)


def _nextCounter_2(name: str, cursor_: "PNSqlCursor") -> Optional[Union[str, int]]:
    from .pnsqlquery import PNSqlQuery

    if not cursor_:
        return None

    tMD = cursor_.metadata()
    if not tMD:
        return None

    field = tMD.field(name)
    if not field:
        return None

    type_ = field.type()

    if type_ not in ["string", "double"]:
        return None

    _len = int(field.length())
    cadena = None

    q = PNSqlQuery(None, cursor_.db().connectionName())
    q.setForwardOnly(True)
    q.setTablesList(tMD.name())
    q.setSelect(name)
    q.setFrom(tMD.name())
    q.setWhere("LENGTH(%s)=%s" % (name, _len))
    q.setOrderBy(name + " DESC")

    if not q.exec_():
        return None

    maxRange: int = 10 ** _len
    numero: int = maxRange

    while numero >= maxRange:
        if not q.next():
            numero = 1
            break

        try:
            numero = int(q.value(0))
            numero = numero + 1
        except Exception:
            pass

    if type_ == "string":
        cadena = str(numero)

        if len(cadena) < _len:
            relleno = None
            relleno = cadena.rjust(_len, "0")
            cadena = relleno

        return cadena

    if type_ == "double":
        return numero

    return None


def _nextCounter_3(serie: str, name: str, cursor_: "PNSqlCursor") -> Optional[str]:
    from .pnsqlquery import PNSqlQuery

    if not cursor_:
        return None

    tMD = cursor_.metadata()
    if not tMD:
        return None

    field = tMD.field(name)
    if not field:
        return None

    type_ = field.type()
    if type_ not in ["string", "double"]:
        return None

    _len: int = field.length() - len(serie)

    where = "length(%s)=%d AND substring(%s FROM 1 for %d) = '%s'" % (
        name,
        field.length(),
        name,
        len(serie),
        serie,
    )
    select = "substring(%s FROM %d) as %s" % (name, len(serie) + 1, name)
    q = PNSqlQuery(None, cursor_.db().connectionName())
    q.setForwardOnly(True)
    q.setTablesList(tMD.name())
    q.setSelect(select)
    q.setFrom(tMD.name())
    q.setWhere(where)
    q.setOrderBy(name + " DESC")

    if not q.exec_():
        return None

    maxRange: int = 10 ** _len
    numero: int = maxRange

    while numero >= maxRange:
        if not q.next():
            numero = 1
            break

        numero = int(q.value(0))
        numero = numero + 1

    if type_ in ["string", "double"]:
        cadena: str = str(numero)
        if len(cadena) < _len:
            relleno = "0" * (_len - len(cadena))
            cadena = relleno + cadena

        # res = serie + cadena
        return cadena

    return None


def sqlSelect(
    f: str,
    s: str,
    w: str,
    tL: Optional[Union[str, List]] = None,
    size: int = 0,
    connName: str = "default",
) -> Any:
    """
    Execute a query of type select, returning the results of the first record found.

    @param f: from the query statement.
    @param s: Select statement of the query, which will be the name of the field to return.
    @param w: Where statement of the query.
    @param tL: Tableslist statement of the query. Required when more than one table is included in the from statement.
    @param size: Number of lines found. (-1 if there is error).
    @param connName Connection name.
    @return Value resulting from the query or false if it finds nothing.
    """
    if not w:
        return False

    from .pnsqlquery import PNSqlQuery

    q = PNSqlQuery(None, connName)
    if tL:
        q.setTablesList(tL)
    else:
        q.setTablesList(f)

    q.setSelect(s)
    q.setFrom(f)
    q.setWhere(w)
    # q.setForwardOnly(True)
    if not q.exec_():
        return False

    if q.next():
        valor = q.value(0)
        # if isinstance(valor, datetime.date):
        #    valor = str(valor)
        return valor

    return False


def quickSqlSelect(f: str, s: str, w: str, connName: str = "default") -> Any:
    """
    Quick version of sqlSelect. Run the query directly without checking.Use with caution.
    """
    from .pnsqlquery import PNSqlQuery

    if not w:
        sql = "select " + s + " from " + f
    else:
        sql = "select " + s + " from " + f + " where " + w

    q = PNSqlQuery(None, connName)
    if not q.exec_(sql):
        return False

    return q.value(0) if q.first() else False


def sqlInsert(
    t: str, fL_: Union[str, List[str]], vL_: Union[str, List[str]], connName: str = "default"
) -> bool:
    """
    Perform the insertion of a record in a table using an FLSqlCursor object.

    @param t Table name.
    @param fL Comma separated list of field names.
    @param vL Comma separated list of corresponding values.
    @param connName Connection name.
    @return True in case of successful insertion, false in any other case.
    """

    fL: List[str] = fL_.split(",") if isinstance(fL_, str) else fL_
    vL: List[str] = vL_.split(",") if isinstance(vL_, str) else vL_

    if not len(fL) == len(vL):
        return False

    from .pnsqlcursor import PNSqlCursor

    c = PNSqlCursor(t, True, connName)
    c.setModeAccess(PNSqlCursor.Insert)
    c.refreshBuffer()

    i = 0
    for f in fL:
        if vL[i] is None:
            c.bufferSetNull(f)
        else:
            c.setValueBuffer(f, vL[i])

        i = i + 1

    return c.commitBuffer()


def sqlUpdate(
    t: str, fL: Union[str, List[str]], vL: Union[str, List[str]], w: str, connName: str = "default"
) -> bool:
    """
    Modify one or more records in a table using an FLSqlCursor object.

    @param t Table name.
    @param fL Comma separated list of field names.
    @param vL Comma separated list of corresponding values.
    @param w Where statement to identify the records to be edited.
    @param connName Connection name.
    @return True in case of successful insertion, false in any other case.
    """
    from .pnsqlcursor import PNSqlCursor

    c = PNSqlCursor(t, True, connName)
    c.select(w)
    c.setForwardOnly(True)
    while c.next():

        c.setModeAccess(PNSqlCursor.Edit)
        c.refreshBuffer()

        if isinstance(fL, list):
            i = 0
            for f in fL:
                c.setValueBuffer(f, vL[i])
                i = i + 1
        else:
            c.setValueBuffer(fL, vL)

        if not c.commitBuffer():
            return False

    return True


def sqlDelete(t: str, w: str, connName: str = "default") -> bool:
    """
    Delete one or more records in a table using an FLSqlCursor object.

    @param t Table name.
    @param w Where statement to identify the records to be deleted.
    @param connName Connection name.
    @return True in case of successful insertion, false in any other case.
    """
    from .pnsqlcursor import PNSqlCursor

    c = PNSqlCursor(t, True, connName)

    # if not c.select(w):
    #     return False
    c.select(w)
    c.setForwardOnly(True)

    while c.next():
        c.setModeAccess(PNSqlCursor.Del)
        c.refreshBuffer()
        if not c.commitBuffer():
            return False

    return True


def quickSqlDelete(t: str, w: str, connName: str = "default") -> None:
    """
    Quick version of sqlDelete. Execute the query directly without checking and without committing signals.Use with caution.
    """
    execSql("DELETE FROM %s WHERE %s" % (t, w))


def execSql(sql: str, connName: str = "default") -> bool:
    """
    Run a query.
    """
    from pineboolib.application import project

    if project.conn is None:
        raise Exception("Project is not connected yet")

    conn_ = project.conn.useConn(connName)
    cur = conn_.cursor()
    try:
        logger.warning("execSql: Ejecutando la consulta : %s", sql)
        # sql = conn_.db().driver().fix_query(sql)
        cur.execute(sql)
        conn_.conn.commit()
        return True
    except Exception as exc:
        logger.exception("execSql: Error al ejecutar la consulta SQL: %s %s", sql, exc)
        return False
