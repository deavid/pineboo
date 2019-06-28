from .projectconfig import ProjectConfig

DEFAULT_SQLITE_CONN = ProjectConfig("pineboo.sqlite3", None, None, None, None, "SQLite3 (SQLITE3)")


def config_dbconn(options):
    from pineboolib.core.utils import filedir
    from .projectconfig import ProjectConfig

    if options.project:  # FIXME: --project debería ser capaz de sobreescribir algunas opciones
        if not options.project.endswith(".xml"):
            options.project += ".xml"
        prjpath = filedir("../profiles", options.project)
        return ProjectConfig(load_xml=prjpath)

    if options.connection:
        return ProjectConfig(connstring=options.connection)

    return None


def connect_to_db(config):
    from pineboolib.pnconnection import PNConnection

    connection = PNConnection(
        config.dbname, config.dbserver.host, config.dbserver.port, config.dbauth.username, config.dbauth.password, config.dbserver.type
    )
    return connection
