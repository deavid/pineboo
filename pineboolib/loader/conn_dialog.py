import logging

logger = logging.getLogger("loader.conn_dialog")


def show_connection_dialog(project, app):
    """Show the connection dialog, and configure the project accordingly."""
    from .dlgconnect import DlgConnect

    connection_window = DlgConnect(project._DGI)
    connection_window.load()
    connection_window.show()
    ret = app.exec_()  # FIXME: App should be started before this function
    if connection_window.close():
        # if connection_window.ruta:
        #    prjpath = connection_window.ruta
        #    print("Cargando desde ruta %r " % prjpath)
        #    project.load(prjpath)
        # elif connection_window.database:
        if getattr(connection_window, "database", None):
            logger.info("Cargando credenciales")
            from pineboolib.fllegacy.flsettings import FLSettings

            project.deleteCache = FLSettings().readBoolEntry("ebcomportamiento/deleteCache", False)
            project.parseProject = FLSettings().readBoolEntry("ebcomportamiento/parseProject", False)
            project.load_db(
                connection_window.database,
                connection_window.hostname,
                connection_window.portnumber,
                connection_window.username,
                connection_window.password,
                connection_window.driveralias,
            )
        else:
            # FIXME: Wrong context for sys.exit. Not this function's responsibility
            import sys

            sys.exit(ret)
