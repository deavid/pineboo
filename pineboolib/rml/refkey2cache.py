# -*- coding: utf-8 -*-
from PyQt5.QtGui import QPixmap
from pineboolib.utils import filedir, clearXPM
from pineboolib.fllegacy.FLSqlQuery import FLSqlQuery
import os
import logging


def parseKey(name=None):
    ret = None
    value = None
    if name is None:
        ret = None
    else:
        q = FLSqlQuery()
        # q.setForwardOnly(True)
        q.exec_("SELECT contenido FROM fllarge WHERE refkey='%s'" % name)
        if q.next():
            value = clearXPM(q.value(0))

        imgFile = filedir("../tempdata")
        imgFile += "/%s.png" % name
        if not os.path.exists(imgFile) and value:
            pix = QPixmap(value)
            if not pix.save(imgFile):
                self.logger.warn("rml:refkey2cache No se ha podido guardar la imagen %s" % imgFile)
                ret = None

        ret = imgFile

    return ret
