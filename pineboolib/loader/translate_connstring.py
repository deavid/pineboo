def translate_connstring(connstring):
    """Translate a DSN connection string into user, pass, etc.

    Acepta un parámetro "connstring" que tenga la forma user@host/dbname
    y devuelve todos los parámetros por separado. Tiene en cuenta los
    valores por defecto y las diferentes formas de abreviar que existen.
    """
    user = "postgres"
    passwd = None
    host = "127.0.0.1"
    port = "5432"
    dbname = ""
    driver_alias = ""
    user_pass = None
    host_port = None
    try:
        uphpstring = connstring[: connstring.rindex("/")]
    except ValueError:
        dbname = connstring
        if not re.match(r"\w+", dbname):
            raise ValueError("base de datos no valida")
        return user, passwd, host, port, dbname
    dbname = connstring[connstring.rindex("/") + 1 :]
    conn_list = [None, None] + uphpstring.split("@")
    user_pass, host_port = conn_list[-2], conn_list[-1]

    if user_pass:
        user_pass = user_pass.split(":") + [None, None, None]
        user, passwd, driver_alias = user_pass[0], user_pass[1] or passwd, user_pass[2] or driver_alias
        if user_pass[3]:
            raise ValueError("La cadena de usuario debe tener el formato user:pass:driver.")

    if host_port:
        host_port = host_port.split(":") + [None]
        host, port = host_port[0], host_port[1] or port
        if host_port[2]:
            raise ValueError("La cadena de host debe ser host:port.")

    if not re.match(r"\w+", user):
        raise ValueError("Usuario no valido")
    if not re.match(r"\w+", dbname):
        raise ValueError("base de datos no valida")
    if not re.match(r"\d+", port):
        raise ValueError("puerto no valido")
    logger.debug(
        "user:%s, passwd:%s, driver_alias:%s, host:%s, port:%s, dbname:%s", user, "*" * len(passwd), driver_alias, host, port, dbname
    )
    return user, passwd, driver_alias, host, port, dbname
