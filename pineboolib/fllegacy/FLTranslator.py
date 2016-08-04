# -*- coding: utf-8 -*-

from PyQt4 import QtCore

from pineboolib.fllegacy import FLTranslations
from pineboolib import decorators

class FLTranslator():
    
    mulTiLang_ = False
    sysTrans_ = False
    AQ_DISKCACHE_FILEPATH = None #FIXME
    AQ_DISKCACHE_DIRPATH = None #FIXME
    
    @decorators.BetaImplementation
    def __init_(self, parent=None, name=None, multiLang= False, sysTrans=False):
        #QtCore.QTranslator(parent ? parent : qApp, name)
        self.mulTiLang_ = multiLang
        self.sysTrans_ = sysTrans
    
    """
    Carga en el traductor el contenido de un fichero de traducciones existente en la caché de disco

    El fichero debe introducirse en la caché de disco antes de llamar a este método, en
    caso contrario no se hará nada.

    @param key Clave sha1 que identifica al fichero en la caché de disco
    @return  TRUE si la operación tuvo éxito
    """
    @decorators.BetaImplementation
    def loadTsContent(self, key):
        tsFile = QtCore.QString(self.AQ_DISKCACHE_FILEPATH(key))
        qmFile = QtCore.QString(self.AQ_DISKCACHE_DIRPATH + "/" + key + ".qm")
        
        if QtCore.QFile.exist(qmFile):
            if tsFile.isEmpty():
                return False
            
            trans = FLTranslations
            
            trans.lrelease(tsFile,qmFile, not self.mulTiLang_)
        
        return QtCore.QTranslator.load(qmFile)
    
    @decorators.BetaImplementation
    def findMessage(self, context, sourceText, comment=None):
        if not comment:
            return QtCore.QTranslator.findMessage(context, sourceText)
        else:
            return QtCore.QTranslator.findMessage(context, sourceText, comment)
    
