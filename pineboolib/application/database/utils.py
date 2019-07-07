from pineboolib import logging
from pineboolib.fllegacy.flsqlquery import FLSqlQuery  # FIXME: Remove dependency

logger = logging.getLogger("database.utils")


def nextCounter(*args):
    """
    Este metodo devuelve el siguiente valor de un campo tipo contador de una tabla.

    Este metodo es muy util cuando se insertan registros en los que
    la referencia es secuencial y no nos acordamos de cual fue el ultimo
    numero usado. El valor devuelto es un QVariant del tipo de campo es
    el que se busca la ultima referencia. Lo más aconsejable es que el tipo
    del campo sea 'String' porque así se le puede dar formato y ser
    usado para generar un código de barras. De todas formas la función
    soporta tanto que el campo sea de tipo 'String' como de tipo 'double'.

    @param name Nombre del campo
    @param cursor_ Cursor a la tabla donde se encuentra el campo.
    @return Qvariant con el numero siguiente.
    @author Andrés Otón Urbano.
    """
    """
    dpinelo: Este método es una extensión de nextCounter pero permitiendo la introducción de una primera
    secuencia de caracteres. Es útil cuando queremos mantener diversos contadores dentro de una misma tabla.
    Ejemplo, Tabla Grupo de clientes: Agregamos un campo prefijo, que será una letra: A, B, C, D.
    Queremos que la numeración de los clientes sea del tipo A00001, o B000023. Con esta función, podremos
    seguir usando los métodos counter cuando agregamos esa letra.

    Este metodo devuelve el siguiente valor de un campo tipo contador de una tabla para una serie determinada.

    Este metodo es muy util cuando se insertan registros en los que
    la referencia es secuencial según una secuencia y no nos acordamos de cual fue el último
    numero usado. El valor devuelto es un QVariant del tipo de campo es
    el que se busca la ultima referencia. Lo más aconsejable es que el tipo
    del campo sea 'String' porque así se le puede dar formato y ser
    usado para generar un código de barras. De todas formas la función
    soporta tanto que el campo sea de tipo 'String' como de tipo 'double'.

    @param serie serie que diferencia los contadores
    @param name Nombre del campo
    @param cursor_ Cursor a la tabla donde se encuentra el campo.
    @return Qvariant con el numero siguiente.
    @author Andrés Otón Urbano.
    """
    if len(args) == 2:
        name = args[0]
        cursor_ = args[1]

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

        q = FLSqlQuery(None, cursor_.db().connectionName())
        q.setForwardOnly(True)
        q.setTablesList(tMD.name())
        q.setSelect(name)
        q.setFrom(tMD.name())
        q.setWhere("LENGTH(%s)=%s" % (name, _len))
        q.setOrderBy(name + " DESC")

        if not q.exec_():
            return None

        maxRange = 10 ** _len
        numero = maxRange

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

    else:
        serie = args[0]
        name = args[1]
        cursor_ = args[2]

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

        _len = field.length() - len(serie)
        cadena = None

        where = "length(%s)=%d AND substring(%s FROM 1 for %d) = '%s'" % (name, field.length(), name, len(serie), serie)
        select = "substring(%s FROM %d) as %s" % (name, len(serie) + 1, name)
        q = FLSqlQuery(None, cursor_.db().connectionName())
        q.setForwardOnly(True)
        q.setTablesList(tMD.name())
        q.setSelect(select)
        q.setFrom(tMD.name())
        q.setWhere(where)
        q.setOrderBy(name + " DESC")

        if not q.exec_():
            return None

        maxRange = 10 ** _len
        numero = maxRange

        while numero >= maxRange:
            if not q.next():
                numero = 1
                break

            numero = int(q.value(0))
            numero = numero + 1

        if type_ in ["string", "double"]:
            cadena = numero
            if len(cadena) < _len:
                relleno = "0" * (_len - len(cadena))
                cadena = relleno + cadena

            # res = serie + cadena
            return cadena

        return None


def sqlSelect(f, s, w, tL=None, size=0, connName="default"):
    """
    Ejecuta una query de tipo select, devolviendo los resultados del primer registro encontrado

    @param f: Sentencia from de la query
    @param s: Sentencia select de la query, que será el nombre del campo a devolver
    @param w: Sentencia where de la query
    @param tL: Sentencia tableslist de la query. Necesario cuando en la sentencia from se incluya más de una tabla
    @param size: Número de líneas encontradas. (-1 si hay error)
    @param connName Nombre de la conexion
    @return Valor resultante de la query o falso si no encuentra nada.
    """
    if w is None or w == "":
        return False

    q = FLSqlQuery(None, connName)
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


def quickSqlSelect(f, s, w, connName="default"):
    """
    Versión rápida de sqlSelect. Ejecuta directamente la consulta sin realizar comprobaciones.
    Usar con precaución.
    """
    if not w:
        sql = "select " + s + " from " + f
    else:
        sql = "select " + s + " from " + f + " where " + w

    q = FLSqlQuery(None, connName)
    if not q.exec_(sql):
        return False

    return q.value(0) if q.first() else False


def sqlInsert(t, fL, vL, connName="default"):
    """
    Realiza la inserción de un registro en una tabla mediante un objeto FLSqlCursor

    @param t Nombre de la tabla
    @param fL Lista separada con comas de los nombres de los campos
    @param vL Lista separada con comas de los valores correspondientes
    @param connName Nombre de la conexion
    @return Verdadero en caso de realizar la inserción con éxito, falso en cualquier otro caso
    """
    from pineboolib.fllegacy.flsqlcursor import FLSqlCursor

    fL = fL.split(",") if isinstance(fL, str) else fL
    vL = vL.split(",") if isinstance(vL, str) else vL

    if not len(fL) == len(vL):
        return False

    c = FLSqlCursor(t, True, connName)
    c.setModeAccess(FLSqlCursor.Insert)
    c.refreshBuffer()

    i = 0
    for f in fL:
        if vL[i] is None:
            c.bufferSetNull(f)
        else:
            c.setValueBuffer(f, vL[i])

        i = i + 1

    return c.commitBuffer()


def sqlUpdate(t, fL, vL, w, connName="default"):
    """
    Realiza la modificación de uno o más registros en una tabla mediante un objeto FLSqlCursor

    @param t Nombre de la tabla
    @param fL Lista separada con comas de los nombres de los campos
    @param vL Lista separada con comas de los valores correspondientes
    @param w Sentencia where para identificar los registros a editar.
    @param connName Nombre de la conexion
    @return Verdadero en caso de realizar la inserción con éxito, falso en cualquier otro caso
    """
    from pineboolib.fllegacy.flsqlcursor import FLSqlCursor

    c = FLSqlCursor(t, True, connName)
    c.select(w)
    c.setForwardOnly(True)
    while c.next():

        c.setModeAccess(FLSqlCursor.Edit)
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


def sqlDelete(t, w, connName="default"):
    """
    Borra uno o más registros en una tabla mediante un objeto FLSqlCursor

    @param t Nombre de la tabla
    @param w Sentencia where para identificar los registros a borrar.
    @param connName Nombre de la conexion
    @return Verdadero en caso de realizar la inserción con éxito, falso en cualquier otro caso
    """
    from pineboolib.fllegacy.flsqlcursor import FLSqlCursor

    c = FLSqlCursor(t, True, connName)

    # if not c.select(w):
    #     return False
    c.select(w)
    c.setForwardOnly(True)

    while c.next():
        c.setModeAccess(FLSqlCursor.Del)
        c.refreshBuffer()
        if not c.commitBuffer():
            return False

    return True


def quickSqlDelete(t, w, connName="default"):
    """
    Versión rápida de sqlDelete. Ejecuta directamente la consulta sin realizar comprobaciones y sin disparar señales de commits.
    Usar con precaución.
    """
    execSql("DELETE FROM %s WHERE %s" % (t, w))


def execSql(sql, connName="default"):
    """
    Uso interno
    """
    from pineboolib import pncontrolsfactory

    conn_ = pncontrolsfactory.aqApp.db().useConn(connName)
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
