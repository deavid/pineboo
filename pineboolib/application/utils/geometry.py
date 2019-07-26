from pineboolib.core.settings import settings
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PyQt5.QtCore import QSize  # type: ignore


def saveGeometryForm(name: str, geo: "QSize") -> None:
    """
    Guarda la geometría de una ventana
    @param name, Nombre de la ventana
    @param geo, QSize con los valores de la ventana
    """
    from pineboolib.application import project  # FIXME

    if project.conn is None:
        raise Exception("Project is not connected yet")

    name = "geo/%s/%s" % (project.conn.DBName(), name)
    settings.set_value(name, geo)


def loadGeometryForm(name: str) -> "QSize":
    """
    Carga la geometría de una ventana
    @param name, Nombre de la ventana
    @return QSize con los datos de la geometríca de la ventana guardados.
    """
    from pineboolib.application import project  # FIXME

    if project.conn is None:
        raise Exception("Project is not connected yet")

    name = "geo/%s/%s" % (project.conn.DBName(), name)
    return settings.value(name, None)
