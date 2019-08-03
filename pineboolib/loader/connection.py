from optparse import Values
from typing import Optional

from pineboolib.core.utils.utils_base import filedir
from pineboolib.application.database.pnconnection import PNConnection
from .projectconfig import ProjectConfig


DEFAULT_SQLITE_CONN = ProjectConfig(database="pineboo.sqlite3", type="SQLite3 (SQLITE3)")
IN_MEMORY_SQLITE_CONN = ProjectConfig(database=":memory:", type="SQLite3 (SQLITE3)")


def config_dbconn(options: Values) -> Optional[ProjectConfig]:
    if options.project:  # FIXME: --project debería ser capaz de sobreescribir algunas opciones
        if not options.project.endswith(".xml"):
            options.project += ".xml"
        prjpath = filedir("../profiles", options.project)
        return ProjectConfig(load_xml=prjpath)

    if options.connection:
        return ProjectConfig(connstring=options.connection)

    return None


def connect_to_db(config: ProjectConfig) -> "PNConnection":
    if config.database is None:
        raise ValueError("database not set")
    if config.host is None:
        raise ValueError("database not set")
    if config.port is None:
        raise ValueError("database not set")
    if config.username is None:
        raise ValueError("database not set")
    if config.password is None:
        raise ValueError("database not set")
    if config.type is None:
        raise ValueError("database not set")
    connection = PNConnection(config.database, config.host, int(config.port), config.username, config.password, config.type)
    return connection
