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
    connection_window.close()
    return connection_window.selected_project_config
