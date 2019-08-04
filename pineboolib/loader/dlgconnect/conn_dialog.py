"""conn_dialog module."""

from pineboolib import logging

from PyQt5.QtWidgets import QApplication  # type: ignore
from pineboolib.loader.projectconfig import ProjectConfig
from typing import Optional

logger = logging.getLogger("loader.conn_dialog")


def show_connection_dialog(app: QApplication) -> Optional[ProjectConfig]:
    """Show the connection dialog, and configure the project accordingly."""
    from .dlgconnect import DlgConnect

    connection_window = DlgConnect()
    connection_window.load()
    connection_window.show()
    app.exec_()  # FIXME: App should be started before this function
    if connection_window.close():
        project_config = None
        if getattr(connection_window, "database", None):
            project_config = ProjectConfig(
                connection_window.database,
                connection_window.hostname,
                connection_window.portnumber,
                connection_window.driveralias,
                connection_window.username,
                connection_window.password,
            )

        return project_config
    return None
