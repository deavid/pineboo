# -*- coding: utf-8 -*-

import os
from pineboolib.core.utils.utils_base import filedir
from pineboolib.core.settings import config
from pineboolib.application import project

from PyQt5.Qt import QTranslator  # type: ignore
from pineboolib import logging
from typing import Any, Dict


class FLTranslator(QTranslator):

    mulTiLang_ = False
    sysTrans_ = False
    AQ_DISKCACHE_FILEPATH = None  # FIXME
    AQ_DISKCACHE_DIRPATH = None  # FIXME
    idM_ = None
    lang_ = None
    translation_from_ = None
    ts_translation_contexts: Dict[str, Dict[str, str]] = {}

    def __init__(self, parent=None, name: str = None, multiLang=False, sysTrans=False) -> None:
        super(FLTranslator, self).__init__()
        self.logger = logging.getLogger("FLTranslator")
        self._prj = parent
        if not name:
            raise Exception("Name is mandatory")
        self.idM_ = name[: name.rfind("_")]
        self.lang_ = name[name.rfind("_") + 1 :]
        self.mulTiLang_ = multiLang
        self.sysTrans_ = sysTrans
        self.translation_from_qm = config.value("ebcomportamiento/translations_from_qm", False)

    """
    Carga en el traductor el contenido de un fichero de traducciones existente en la caché de disco

    El fichero debe introducirse en la caché de disco antes de llamar a este método, en
    caso contrario no se hará nada.

    @param key Clave sha1 que identifica al fichero en la caché de disco
    @return  TRUE si la operación tuvo éxito
    """

    def loadTsContent(self, key) -> Any:
        if project.conn is None:
            raise Exception("Project is not connected yet")
        if self.idM_ == "sys":
            ts_file = filedir("../share/pineboo/translations/%s.%s" % (self.idM_, self.lang_))
        else:
            ts_file = filedir(
                "%s/cache/%s/%s/file.ts/%s.%s/%s" % (project.tmpdir, project.conn.DBName(), self.idM_, self.idM_, self.lang_, key)
            )
        # qmFile = self.AQ_DISKCACHE_DIRPATH + "/" + key + ".qm"

        ret_ = None
        if not self.translation_from_qm:
            ret_ = self.load_ts("%s.ts" % ts_file)
            if not ret_:
                self.logger.warning("For some reason, i cannot load '%s.ts'", ts_file)
        else:

            qm_file = "%s.qm" % ts_file
            if os.path.exists(qm_file):
                if ts_file in (None, ""):
                    return False

            else:
                from pineboolib.fllegacy.fltranslations import FLTranslations

                trans = FLTranslations()
                trans.lrelease("%s.ts" % ts_file, qm_file, not self.mulTiLang_)

            ret_ = self.load(qm_file)
            if not ret_:
                self.logger.warning("For some reason, i cannot load '%s'", qm_file)

        return ret_

    def translate(self, *args) -> Any:
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
                    ret_ = self.ts_translation_contexts[context][source_text]

        return ret_

    def load_ts(self, file_name: str) -> bool:
        try:
            from pineboolib.core.utils.utils_base import load2xml

            root_ = load2xml(file_name)
            for context in root_.findall("context"):
                name_elem = context.find("name")
                if name_elem is None:
                    self.logger.warning("load_ts: <name> not found, skipping")
                    continue
                context_dict_key = name_elem.text
                if not context_dict_key:
                    continue
                if context_dict_key not in self.ts_translation_contexts.keys():
                    self.ts_translation_contexts[context_dict_key] = {}
                for message in context.findall("message"):
                    translation_elem, source_elem = (message.find("translation"), message.find("source"))
                    translation_text = translation_elem is not None and translation_elem.text
                    source_text = source_elem is not None and source_elem.text
                    if translation_text and source_text:
                        self.ts_translation_contexts[context_dict_key][source_text] = translation_text

            return True
        except Exception:
            return False
