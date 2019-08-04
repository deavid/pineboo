"""projectconfig module."""

import re
from typing import Any, Tuple, Optional

from pineboolib import logging
from pineboolib.core.utils.version import VersionNumber

VERSION_1_0 = VersionNumber("1.0")
VERSION_1_1 = VersionNumber("1.1")
VERSION_1_2 = VersionNumber("1.2")


class ProjectConfig:
    """
    Read and write XML on profiles. Represents a database connection configuration.
    """

    logger = logging.getLogger("loader.projectConfig")

    def __init__(
        self,
        database: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[str] = None,
        type: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        load_xml: Optional[str] = None,
        connstring: Optional[str] = None,
    ) -> None:
        """Initialize."""

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

    def __repr__(self) -> str:
        """Display the information in text mode."""

        return "<ProjectConfig database=%s host:port=%s:%s type=%s user=%s>" % (
            self.database,
            self.host,
            self.port,
            self.type,
            self.username,
        )

    def load_projectxml(self, file_name: str) -> bool:
        """Collect the connection information from an xml file."""

        import hashlib
        import os.path
        from xml.etree import ElementTree as ET

        if not os.path.isfile(file_name):
            raise ValueError("el proyecto %r no existe." % file_name)

        tree = ET.parse(file_name)
        root = tree.getroot()
        version = VersionNumber(root.get("Version"), default="1.0")

        for profile in root.findall("profile-data"):
            invalid_password = False
            if version == VERSION_1_0:
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

        from pineboolib.application.database.pnsqldrivers import PNSqlDrivers

        sql_drivers_manager = PNSqlDrivers()
        dbname_elem = root.find("database-name")
        if dbname_elem is None:
            raise ValueError("database-name not found")
        self.database = dbname_elem.text
        for db in root.findall("database-server"):
            host_elem, port_elem, type_elem = (db.find("host"), db.find("port"), db.find("type"))
            if host_elem is None or port_elem is None or type_elem is None:
                raise ValueError("host, port and type are required")
            self.host = host_elem.text
            self.port = port_elem.text
            self.type = type_elem.text
            # FIXME: Move this to project, or to the connection handler.
            if self.type not in sql_drivers_manager.aliasList():
                self.logger.warning("Esta versión de pineboo no soporta el driver '%s'" % self.type)
                self.database = None
                return False

        for credentials in root.findall("database-credentials"):
            username_elem, password_elem = (
                credentials.find("username"),
                credentials.find("password"),
            )
            if username_elem is None:
                self.username = ""
            else:
                self.username = username_elem.text
            if password_elem is not None and password_elem.text:
                import base64

                self.password = base64.b64decode(password_elem.text).decode()
            else:
                self.password = ""

        return True

    @classmethod
    def translate_connstring(cls, connstring: str) -> Tuple[Any, Any, Any, Any, Any, Any]:
        """
        Translate a DSN connection string into user, pass, etc.

        Accept a "connstring" parameter that has the form user @ host / dbname
        and returns all parameters separately. It takes into account the
        default values ​​and the different abbreviations that exist.
        """
        user = "postgres"
        passwd = ""
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
            return user, passwd, driver_alias, host, port, dbname
        dbname = connstring[connstring.rindex("/") + 1 :]
        up, hp = uphpstring.split("@")
        conn_list = [None, None, up, hp]
        _user_pass, _host_port = conn_list[-2], conn_list[-1]

        if _user_pass:
            user_pass = _user_pass.split(":") + ["", "", ""]
            user, passwd, driver_alias = (
                user_pass[0],
                user_pass[1] or passwd,
                user_pass[2] or driver_alias,
            )
            if user_pass[3]:
                raise ValueError("La cadena de usuario debe tener el formato user:pass:driver.")

        if _host_port:
            host_port = _host_port.split(":") + [""]
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
            "user:%s, passwd:%s, driver_alias:%s, host:%s, port:%s, dbname:%s",
            user,
            "*" * len(passwd),
            driver_alias,
            host,
            port,
            dbname,
        )
        return user, passwd, driver_alias, host, port, dbname
