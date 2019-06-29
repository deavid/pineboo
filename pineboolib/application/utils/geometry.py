from pineboolib.core.settings import settings


def saveGeometryForm(name, geo):
    """
    Guarda la geometría de una ventana
    @param name, Nombre de la ventana
    @param geo, QSize con los valores de la ventana
    """
    from pineboolib import project  # FIXME

    name = "geo/%s/%s" % (project.conn.DBName(), name)
    settings.set_value(name, geo)


def loadGeometryForm(name):
    """
    Carga la geometría de una ventana
    @param name, Nombre de la ventana
    @return QSize con los datos de la geometríca de la ventana guardados.
    """
    from pineboolib import project  # FIXME

    name = "geo/%s/%s" % (project.conn.DBName(), name)
    return settings.value(name, None)
