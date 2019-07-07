from pineboolib.fllegacy.flsqlquery import FLSqlQuery  # FIXME: Remove dependency


def nextCounter(self, *args):
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
                relleno = cadena.rjust(_len - len(cadena), "0")
                cadena = relleno + cadena

            # res = serie + cadena
            return cadena

        return None
