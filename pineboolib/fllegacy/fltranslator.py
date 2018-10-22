# -*- coding: utf-8 -*-

import os
from pineboolib.utils import filedir
from pineboolib.fllegacy.fltranslations import FLTranslations
from pineboolib import decorators

from PyQt5 import QtCore
from PyQt5.Qt import QTranslator


class FLTranslator(QTranslator):

    mulTiLang_ = False
    sysTrans_ = False
    AQ_DISKCACHE_FILEPATH = None  # FIXME
    AQ_DISKCACHE_DIRPATH = None  # FIXME
    idM_ = None
    lang_ = None

    def __init__(self, parent=None, name=None, multiLang=False, sysTrans=False):
        super(FLTranslator, self).__init__()
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

            return True

        trans = FLTranslations()
        trans.lrelease("%s.ts" % tsFile, qmFile, not self.mulTiLang_)
        return self.load(qmFile)

    @decorators.BetaImplementation
    def findMessage(self, context, sourceText, comment=None):
        if not comment:
            return QtCore.QTranslator.findMessage(context, sourceText)
        else:
            return QtCore.QTranslator.findMessage(context, sourceText, comment)
