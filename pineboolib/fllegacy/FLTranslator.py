# -*- coding: utf-8 -*-

from PyQt5 import QtCore

from pineboolib.utils import filedir
from pineboolib.flcontrols import ProjectClass
from pineboolib.fllegacy.FLTranslations import FLTranslations
from pineboolib import decorators

class FLTranslator(ProjectClass):
    
    mulTiLang_ = False
    sysTrans_ = False
    AQ_DISKCACHE_FILEPATH = None #FIXME
    AQ_DISKCACHE_DIRPATH = None #FIXME
    idM_ = None
    
    
    def __init__(self, parent=None, name=None, multiLang= False, sysTrans=False):
        super(FLTranslator, self).__init__()
        #QtCore.QTranslator(parent ? parent : qApp, name)
        self.idM_ = name[0:len(name) -3]
        self.mulTiLang_ = multiLang
        self.sysTrans_ = sysTrans
    
    """
    Carga en el traductor el contenido de un fichero de traducciones existente en la caché de disco

    El fichero debe introducirse en la caché de disco antes de llamar a este método, en
    caso contrario no se hará nada.

    @param key Clave sha1 que identifica al fichero en la caché de disco
    @return  TRUE si la operación tuvo éxito
    """
    @decorators.NotImplementedWarn
    def loadTsContent(self, key):
        return None
        tsFile = filedir("../tempdata/cache/%s/%s/file.ts/%s" %(self.db_.db_name, self.idM_, key))
        qmFile = self.AQ_DISKCACHE_DIRPATH + "/" + key + ".qm"
        
        if QtCore.QFile.exist(qmFile):
            if tsFile.isEmpty():
                return False
            
            trans = FLTranslations()
            
            trans.lrelease(tsFile,qmFile, not self.mulTiLang_)
        
        return QtCore.QTranslator.load(qmFile)
    
    @decorators.BetaImplementation
    def findMessage(self, context, sourceText, comment=None):
        if not comment:
            return QtCore.QTranslator.findMessage(context, sourceText)
        else:
            return QtCore.QTranslator.findMessage(context, sourceText, comment)
    
