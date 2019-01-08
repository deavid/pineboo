# -*- coding: utf-8 -*-
from pineboolib.utils import filedir
import os
import logging
import importlib

logger = logging.getLogger(__name__)

"""
Esta clase enlaza con el parser de kugar seleccionado en sistema/comportamiento
"""


class PNKugarPlugins(object):

    pluging_ = None
    avalibleParsers_ = []
    defaultParser_ = None

    """
    Constructor
    """

    def __init__(self):

        # Cargamos los parsers avalibles
        dirlist = os.listdir(filedir("plugins/kugar"))
        for f in dirlist:
            if not f[0:2] == "__" and not os.path.isfile(filedir("plugins/kugar", f)):
                self.avalibleParsers_.append(f)

        self.defaultParser_ = "kut2fpdf2"

    """
    Retorna una lista con los nombres de los conversores disponibles
    @return lista de nombres
    """

    def listAvalibles(self):
        return self.avalibleParsers_

    """
    Retorna el nombre del parser por defecto
    @return Nombre del parser por defecto
    """

    def defaultParser(self):
        return self.defaultParser_

    """
    Carga un parser determinado 
    @param name. Nombre del parser para usar por defecto
    """

    def loadParser(self, name):
        if not name in self.avalibleParsers_:
            logger.warn("No se encuentra el plugin %s", name)
            return None
        else:
            logger.info("PNKUGARPLUGINS:: Cargando kutparser %s", name)
            mod_ = importlib.import_module("pineboolib.plugins.kugar.%s.%s" % (name, name))
            return getattr(mod_, name)()
