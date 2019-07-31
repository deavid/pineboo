"""
Manage form sizes.
"""

from pineboolib.core.settings import settings
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PyQt5.QtCore import QSize  # type: ignore


def saveGeometryForm(name: str, geo: "QSize") -> None:
    """
    Save the geometry of a window.

    @param name, window name.
    @param geo, QSize with window values.
    """
    from pineboolib.application import project  # FIXME

    if project.conn is None:
        raise Exception("Project is not connected yet")

    name = "geo/%s/%s" % (project.conn.DBName(), name)
    settings.set_value(name, geo)


def loadGeometryForm(name: str) -> "QSize":
    """
    Load the geometry of a window.

    @param name, window name
    @return QSize with the saved window geometry data.
    """
    from pineboolib.application import project  # FIXME

    if project.conn is None:
        raise Exception("Project is not connected yet")

    name = "geo/%s/%s" % (project.conn.DBName(), name)
    return settings.value(name, None)
