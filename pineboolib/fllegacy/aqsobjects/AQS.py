# -*- coding: utf-8 -*-
from PyQt5.QtGui import QColor, QCloseEvent
from PyQt5.QtWidgets import QFrame, QLabel, QSizePolicy
from PyQt5.QtCore import Qt

import logging

logger = logging.getLogger("AQS")

class AQS(object):

    Close = None
    Box = None
    Plain = None
    AlignTop = None

    def __init__(self):
        self.Close = QCloseEvent
        
    def ColorDialog_getColor(self, color=None, parent=None, name=None):
        from PyQt5.QtWidgets import QColorDialog
        from PyQt5.QtGui import QColor

        if color is None:
            color = QColor.black()

        if isinstance(color, str):
            color = QColor()

        cL = QColorDialog(color, parent)
        return cL.getColor()
    
    def __getattr__(self, name):
        for lib in [QFrame, QLabel, QSizePolicy, Qt]:
            ret_ = getattr(lib, name, None)
            if ret_ is not None:
                return ret_
        
        logger.warn("AQS: No se encuentra el atributo %s", name)
        
