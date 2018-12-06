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
    translation_from_ = None
    ts_translation_contexts = {}
    def __init__(self, parent=None, name=None, multiLang=False, sysTrans=False):
        super(FLTranslator, self).__init__()
        self.logger = logging.getLogger("FLTranslator")
        self._prj = parent
        self.idM_ = name[0:len(name) - 3]
        self.lang_ = name[len(name) - 2:]
        self.mulTiLang_ = multiLang
        self.sysTrans_ = sysTrans
        settings = FLSettings()
        self.translation_from_qm = settings.readBoolEntry("ebcomportamiento/translations_from_qm", False)

    """
    Carga en el traductor el contenido de un fichero de traducciones existente en la caché de disco

    El fichero debe introducirse en la caché de disco antes de llamar a este método, en
    caso contrario no se hará nada.

    @param key Clave sha1 que identifica al fichero en la caché de disco
    @return  TRUE si la operación tuvo éxito
    """

    def loadTsContent(self, key):
        if self.idM_ == "sys":
            ts_file = filedir("../share/pineboo/translations/%s.%s" %
                             (self.idM_, self.lang_))
        else:
            from pineboolib.pncontrolsfactory import aqApp
            ts_file = filedir("%s/cache/%s/%s/file.ts/%s.%s/%s" %
                             (aqApp.tmp_dir(), aqApp.db().database(), self.idM_, self.idM_, self.lang_, key))
        # qmFile = self.AQ_DISKCACHE_DIRPATH + "/" + key + ".qm"
        
        
        ret_ = None
        if not self.translation_from_qm:
            ret_ = self.load_ts("%s.ts" % ts_file)
            if not ret_:
                self.logger.warn("For some reason, i cannot load '%s.ts'", ts_file)
        else:
            
            qm_file = "%s.qm" % ts_file
            if os.path.exists(qm_file):
                if ts_file in (None, ""):
                    return False

            else:

                trans = FLTranslations()
                trans.lrelease("%s.ts" % ts_file, qm_file, not self.mulTiLang_)
            
            
            
            
            
            ret_ = self.load(qm_file)
            if not ret_:
                self.logger.warn("For some reason, i cannot load '%s'", qm_file)
        
        return ret_

    def translate(self, *args):
        context = args[0]
        if context.endswith("PlatformTheme"):
            context = "QMessageBox"
        source_text = args[1]
        ret_ = None
        if self.translation_from_qm:
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
        
                    
        
    
    
