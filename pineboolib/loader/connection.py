from pineboolib.core.utils.utils_base import filedir
from .projectconfig import ProjectConfig

from typing import Optional
from pineboolib.application.database.pnconnection import PNConnection

DEFAULT_SQLITE_CONN = ProjectConfig(database="pineboo.sqlite3", type="SQLite3 (SQLITE3)")


def config_dbconn(options) -> Optional[ProjectConfig]:
    if options.project:  # FIXME: --project debería ser capaz de sobreescribir algunas opciones
        if not options.project.endswith(".xml"):
            options.project += ".xml"
        prjpath = filedir("../profiles", options.project)
        return ProjectConfig(load_xml=prjpath)

    if options.connection:
        return ProjectConfig(connstring=options.connection)

    return None


def connect_to_db(config) -> "PNConnection":

    connection = PNConnection(config.database, config.host, config.port, config.username, config.password, config.type)
    return connection
