# -*- coding: utf-8 -*-

import os
from pineboolib.utils import filedir
from pineboolib.fllegacy.fltranslations import FLTranslations
from pineboolib.fllegacy.flsettings import FLSettings
from pineboolib import decorators

from PyQt5 import QtCore
from PyQt5.Qt import QTranslator
import logging


class FLTranslator(QTranslator):

    mulTiLang_ = False
    sysTrans_ = False
    AQ_DISKCACHE_FILEPATH = None  # FIXME
    AQ_DISKCACHE_DIRPATH = None  # FIXME
    idM_ = None
    lang_ = None

    ts_translation_contexts = {}
    def __init__(self, parent=None, name=None, multiLang=False, sysTrans=False):
        super(FLTranslator, self).__init__()
        self.logger = logging.getLogger("FLTranslator")
        self._prj = parent
        self.idM_ = name[0:len(name) - 3]
        self.lang_ = name[len(name) - 2:]
        self.mulTiLang_ = multiLang
        self.sysTrans_ = sysTrans

    """
    Carga en el traductor el contenido de un fichero de traducciones existente en la caché de disco

    El fichero debe introducirse en la caché de disco antes de llamar a este método, en
    caso contrario no se hará nada.

    @param key Clave sha1 que identifica al fichero en la caché de disco
    @return  TRUE si la operación tuvo éxito
    """

    def loadTsContent(self, key):
        if self.idM_ == "sys":
            tsFile = filedir("../share/pineboo/translations/%s.%s" %
                             (self.idM_, self.lang_))
        else:
            from pineboolib.pncontrolsfactory import aqApp
            tsFile = filedir("../tempdata/cache/%s/%s/file.ts/%s.%s/%s" %
                             (aqApp.db().database(), self.idM_, self.idM_, self.lang_, key))
        # qmFile = self.AQ_DISKCACHE_DIRPATH + "/" + key + ".qm"
        qmFile = "%s.qm" % tsFile
        if os.path.exists(qmFile):
            if tsFile in (None, ""):
                return False

        else:

            trans = FLTranslations()
            trans.lrelease("%s.ts" % tsFile, qmFile, not self.mulTiLang_)
        
        settings = FLSettings()
        ret_ = None
        if not settings.readBoolEntry("ebcomportamiento/translations_from_qm", False):
            ret_ = self.load_ts("%s.ts" % tsFile)
            if not ret_:
                self.logger.warn("For some reason, i cannot load '%s.ts'", tsFile)
        else:
            ret_ = self.load(qmFile)
            if not ret_:
                self.logger.warn("For some reason, i cannot load '%s'", qmFile)
        
        return ret_

    @decorators.BetaImplementation
    def translate(self, *args):
        context = args[0]
        source_text = args[1]
        settings = FLSettings()
        ret_ = None
        if settings.readBoolEntry("ebcomportamiento/translations_from_qm", False):
            ret_ = super(FLTranslator, self).translate(*args)
            if ret_ == "":
                ret_ = None
        else:
            if context in self.ts_translation_contexts.keys():
                if source_text in self.ts_translation_contexts[context]:
                    ret_ =  self.ts_translation_contexts[context][source_text]       
              
        return ret_
    
    def load_ts(self, file_name):
        try:
            from pineboolib.utils import load2xml
            root_ = load2xml(file_name)
            for context in root_.findall("context"):
                context_dict_key = context.find("name").text
                if not context_dict_key in self.ts_translation_contexts.keys():
                    self.ts_translation_contexts[context_dict_key] = {} 
                for message in context.findall("message"):
                    translation = getattr(message, "translation", None)
                    translation_text = message.find("translation").text
                    if translation_text is not None:
                        source_text = message.find("source").text
                        self.ts_translation_contexts[context_dict_key][source_text] = translation_text
            
            return True
        except Exception:
            return False
        
                    
        
    
    
