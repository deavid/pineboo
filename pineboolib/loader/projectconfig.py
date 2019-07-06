from pineboolib import logging
import re


from typing import Optional


class ProjectConfig:
    logger = logging.getLogger("loader.projectConfig")

    def __init__(
        self,
        database: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[str] = None,
        type: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        load_xml: None = None,
        connstring: None = None,
    ) -> None:
        if connstring:
            username, password, type, host, port, database = self.translate_connstring(connstring)
        self.database = database
        self.host = host
        self.port = port
        self.type = type
        self.username = username
        self.password = password
        if load_xml:
            self.load_projectxml(load_xml)

    def load_projectxml(self, file_name: str) -> bool:
        import hashlib
        import os.path
        from xml.etree import ElementTree as ET

        if not os.path.isfile(file_name):
            raise ValueError("el proyecto %r no existe." % file_name)

        tree = ET.parse(file_name)
        root = tree.getroot()

        version = root.get("Version")
        if version is None:
            version = 1.0
        else:
            version = float(version)  # FIXME: Esto es muy mala idea. Tratar versiones como float causará problemas al comparar.

        for profile in root.findall("profile-data"):
            invalid_password = False
            if version == 1.0:
                if getattr(profile.find("password"), "text", None) is not None:
                    invalid_password = True
            else:
                profile_pwd = getattr(profile.find("password"), "text", None)
                user_pwd = hashlib.sha256("".encode()).hexdigest()
                if profile_pwd != user_pwd:
                    invalid_password = True

            if invalid_password:
                self.logger.warning("No se puede cargar un profile con contraseña por consola")
                return False

        from pineboolib.pnsqldrivers import PNSqlDrivers

        sql_drivers_manager = PNSqlDrivers()

        self.database = root.find("database-name").text
        for db in root.findall("database-server"):
            self.host = db.find("host").text
            self.port = db.find("port").text
            self.type = db.find("type").text
            # FIXME: Move this to project, or to the connection handler.
            if self.type not in sql_drivers_manager.aliasList():
                self.logger.warning("Esta versión de pineboo no soporta el driver '%s'" % self.dbserver.type)
                self.database = None
                return False

        for credentials in root.findall("database-credentials"):
            self.username = credentials.find("username").text
            ps = credentials.find("password").text
            if ps:
                import base64

                self.password = base64.b64decode(ps).decode()
            else:
                self.password = ""

        return True

    @classmethod
    def translate_connstring(cls, connstring):
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
            user, passwd, driver_alias = (user_pass[0], user_pass[1] or passwd, user_pass[2] or driver_alias)
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
        cls.logger.debug(
            "user:%s, passwd:%s, driver_alias:%s, host:%s, port:%s, dbname:%s", user, "*" * len(passwd), driver_alias, host, port, dbname
        )
        return user, passwd, driver_alias, host, port, dbname
