"""projectconfig module."""

import re
import base64
import hashlib
import os.path
from typing import Tuple, Optional, Any

from xml.etree import ElementTree as ET

from pineboolib import logging
from pineboolib.core.utils.version import VersionNumber
from pineboolib.core.settings import config
from pineboolib.core.utils.utils_base import filedir, pretty_print_xml

VERSION_1_0 = VersionNumber("1.0")
VERSION_1_1 = VersionNumber("1.1")
VERSION_1_2 = VersionNumber("1.2")


class ProjectConfig:
    """
    Read and write XML on profiles. Represents a database connection configuration.
    """

    SAVE_VERSION = VERSION_1_1  #: Version for saving

    logger = logging.getLogger("loader.projectConfig")

    #: Folder where to read/write project configs.
    profile_dir: str = filedir(config.value("ebcomportamiento/profiles_folder", "../profiles"))

    database: str  #: Database Name, file path to store it, or :memory:
    host: Optional[str]  #: DB server Hostname. None for local files.
    port: Optional[int]  #: DB server port. None for local files.
    username: Optional[str]  #: Database User login name.
    password: Optional[str]  #: Database User login password.
    type: str  #: Driver Type name to use when connecting
    project_password: str  #: Password to cipher when load/saving. Empty string for no ciphering.
    description: str  #: Project name in GUI
    filename: str  #: File path to read / write this project from / to

    def __init__(
        self,
        database: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        type: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        load_xml: Optional[str] = None,
        connstring: Optional[str] = None,
        description: Optional[str] = None,
        filename: Optional[str] = None,
        project_password: str = "",
    ) -> None:
        """Initialize."""
        self.project_password = project_password

        if connstring:
            username, password, type, host, port, database = self.translate_connstring(connstring)
        elif load_xml:
            self.filename = load_xml
            self.load_projectxml()
            return
        if database is None:
            raise ValueError("Database is mandatory. Or use load_xml / connstring params")
        if type is None:
            raise ValueError("Type is mandatory. Or use load_xml / connstring params")
        self.database = database
        self.host = host
        self.port = port
        self.type = type
        self.username = username
        self.password = password
        self.description = description if description else "unnamed"
        if filename is None:
            file_basename = self.description.lower().replace(" ", "_")
            self.filename = os.path.join(self.profile_dir, "%s.xml" % file_basename)
        else:
            self.filename = filename

    def get_uri(self, show_password: bool = False) -> str:
        """Get connection as an URI."""
        host_port = ""
        if self.host:
            host_port += self.host
        if self.port:
            host_port += ":%d" % self.port

        user_pass = ""
        if self.username:
            user_pass += self.username
        if self.password:
            if show_password:
                user_pass += ":%s" % self.password
            else:
                pass_bytes: bytes = hashlib.sha256(self.password.encode()).digest()
                user_pass += ":*" + base64.b64encode(pass_bytes).decode()[:4]

        if user_pass:
            user_pass = "@%s" % user_pass

        uri = host_port + user_pass

        if self.database:
            if uri:
                uri += "/"
            uri += self.database

        return "[%s]://%s" % (self.type, uri)

    def __repr__(self) -> str:
        """Display the information in text mode."""
        if self.project_password:
            # 4 chars in base-64 is 3 bytes. 256**3 should be enough to know if you have the wrong
            # password.
            pass_bytes: bytes = hashlib.sha256(self.project_password.encode()).digest()
            passwd = "-" + base64.b64encode(pass_bytes).decode()[:4]
        else:
            passwd = ""
        return "<ProjectConfig%s name=%r uri=%r>" % (
            passwd,
            self.description,
            self.get_uri(show_password=False),
        )

    def __eq__(self, other: Any) -> bool:
        """Test for equality."""
        if not isinstance(other, ProjectConfig):
            return False
        if other.type != self.type:
            return False
        if other.get_uri(show_password=True) != self.get_uri(show_password=True):
            return False
        if other.description != self.description:
            return False
        if other.project_password != self.project_password:
            return False
        return True

    def load_projectxml(self) -> bool:
        """Collect the connection information from an xml file."""

        file_name = self.filename
        if not os.path.isfile(file_name):
            raise ValueError("El proyecto %r no existe." % file_name)

        tree = ET.parse(file_name)
        root = tree.getroot()
        version = VersionNumber(root.get("Version"), default="1.0")
        self.description = ""
        for xmldescription in root.findall("name"):
            self.description = xmldescription.text or ""

        for profile in root.findall("profile-data"):
            invalid_password = False
            if version == VERSION_1_0:
                stored_password = getattr(profile.find("password"), "text", "")
                if self.project_password != stored_password:
                    invalid_password = True
            else:
                profile_pwd = getattr(profile.find("password"), "text", "")
                if profile_pwd:
                    user_pwd = hashlib.sha256(self.project_password.encode()).hexdigest()
                    if profile_pwd != user_pwd:
                        invalid_password = True

            if invalid_password:
                raise PasswordMismatchError("La contraseña es errónea")

        from pineboolib.application.database.pnsqldrivers import PNSqlDrivers

        sql_drivers_manager = PNSqlDrivers()
        dbname_elem = root.find("database-name")
        if dbname_elem is None:
            raise ValueError("database-name not found")
        if not dbname_elem.text:
            raise ValueError("database-name not valid")
        self.database = dbname_elem.text
        for db in root.findall("database-server"):
            host_elem, port_elem, type_elem = (db.find("host"), db.find("port"), db.find("type"))
            if host_elem is None or port_elem is None or type_elem is None:
                raise ValueError("host, port and type are required")
            self.host = host_elem.text
            self.port = int(port_elem.text) if port_elem.text else None
            if type_elem.text:
                self.type = type_elem.text
            else:
                raise ValueError("No type defined")
            # FIXME: Move this to project, or to the connection handler.
            if self.type not in sql_drivers_manager.aliasList():
                self.logger.warning("Esta versión de pineboo no soporta el driver '%s'" % self.type)

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
                self.password = base64.b64decode(password_elem.text).decode()
            else:
                self.password = ""

        return True

    def save_projectxml(self, overwrite_existing: bool = True) -> None:
        """
        Save the connection.
        """
        profile = ET.Element("Profile")
        profile.set("Version", str(self.SAVE_VERSION))
        description = self.description
        filename = self.filename
        if not os.path.exists(self.profile_dir):
            os.mkdir(self.profile_dir)

        if not overwrite_existing and os.path.exists(filename):
            raise ProfileAlreadyExistsError

        passwDB = self.password or ""

        profile_user = ET.SubElement(profile, "profile-data")
        profile_password = ET.SubElement(profile_user, "password")
        if self.project_password:
            pass_profile = hashlib.sha256(self.project_password.encode()).hexdigest()
            profile_password.text = pass_profile

        name = ET.SubElement(profile, "name")
        name.text = description
        dbs = ET.SubElement(profile, "database-server")
        dbstype = ET.SubElement(dbs, "type")
        dbstype.text = self.type
        dbshost = ET.SubElement(dbs, "host")
        dbshost.text = self.host
        dbsport = ET.SubElement(dbs, "port")
        if self.port:
            dbsport.text = str(self.port)

        dbc = ET.SubElement(profile, "database-credentials")
        dbcuser = ET.SubElement(dbc, "username")
        dbcuser.text = self.username
        dbcpasswd = ET.SubElement(dbc, "password")
        dbcpasswd.text = base64.b64encode(passwDB.encode()).decode()
        dbname = ET.SubElement(profile, "database-name")
        dbname.text = self.database

        pretty_print_xml(profile)

        tree = ET.ElementTree(profile)

        tree.write(filename, xml_declaration=True, encoding="utf-8")

    @classmethod
    def translate_connstring(cls, connstring: str) -> Tuple[str, str, str, str, int, str]:
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
        driver_alias = "PostgreSQL (PSYCOPG2)"
        user_pass = None
        host_port = None
        if "/" not in connstring:
            dbname = connstring
            if not re.match(r"\w+", dbname):
                raise ValueError("base de datos no valida")
            return user, passwd, driver_alias, host, int(port), dbname

        uphpstring = connstring[: connstring.rindex("/")]
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
        return user, passwd, driver_alias, host, int(port), dbname


class ProfileAlreadyExistsError(Exception):
    """Report that project will not be overwritten."""


class PasswordMismatchError(Exception):
    """Provided password is wrong."""
