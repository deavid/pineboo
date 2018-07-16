# -*- coding: utf-8 -*-

import os
import logging
from pineboolib.utils import filedir

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
        
        #Cargamos los parsers avalibles
        dirlist = os.listdir(filedir("plugins/kugar"))
        for f in dirlist:
            if not f[0:2] == "__" and not os.path.isfile(filedir("plugins/kugar", f)):
                self.avalibleParsers_.append(f)
        
        self.defaultParser_ = "kut2rml"
    
    
    def listAvalibles(self):
        return self.avalibleParsers_
    
    def defaultParser(self):
        return self.defaultParser_
    
    def loadParser(self, name):
        if not name in self.avalibleParsers_:
            logger.warn("No se encuentra el plugin %s", name)
            return None
        else:
            print("Cargando...", name)