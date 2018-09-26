# -*- coding: utf-8 -*-
from PyQt5.QtGui import QColor, QPixmap
from PyQt5.QtWidgets import QFrame, QLabel, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5 import QtGui

from pineboolib.utils import filedir

import logging
from PyQt5.QtXml import QDomDocument

logger = logging.getLogger("AQS")


class AQS(object):

    Box = None
    Plain = None
    AlignTop = None
    translate = ["DockLeft", "ContextMenu"]
    InDock = None

    def __init__(self):
        self.InDock = "InDock"
        self.OutSideDock = "OutSideDock"

    def ColorDialog_getColor(self, color=None, parent=None, name=None):
        from PyQt5.QtWidgets import QColorDialog
        from PyQt5.QtGui import QColor

        if color is None:
            color = QColor.black()

        if isinstance(color, str):
            color = QColor()

        cL = QColorDialog(color, parent)
        return cL.getColor()

    def toXml(self, obj_, includeChildren=True, includeComplexTypes=False):
        xml_ = QDomDocument()

        if not obj_:
            return xml_

        e = xml_.createElement("object")
        e.setAttribute("class", type(obj_).__name__)
        xml_.appendChild(e)

        _meta = obj_.metaObject()

        num = _meta.propertyCount()
        i = 0
        _p_properties = []
        while i < num:
            mp = _meta.property(i)
            if mp.name() in _p_properties:
                i += 1
                continue

            _p_properties.append(mp.name())

            val = getattr(obj_, mp.name(), None)
            try:
                val = val()
            except:
                pass

            if val is None:
                i += 1
                continue

            val = str(val)

            if not val and not includeComplexTypes:
                i += 1
                continue
            e.setAttribute(mp.name(), val)

            i += 1

        if includeChildren == True:

            for child in obj_.children():

                itd = self.toXml(child, includeChildren, includeComplexTypes)
                xml_.firstChild().appendChild(itd.firstChild())
        return xml_

    def Pixmap_fromMineSource(self, name):
        return QPixmap(filedir("../share/icons", name))

    def __getattr__(self, name):

        ret_ = getattr(QtGui, "Q%sEvent" % name, None)
        if ret_:
            return ret_

        if name in self.translate:
            if name == "DockLeft":
                name = "LeftDockWidgetArea"

        for lib in [QFrame, QLabel, QSizePolicy, Qt]:
            ret_ = getattr(lib, name, None)

            if ret_ is not None:
                return ret_

        logger.warn("AQS: No se encuentra el atributo %s", name)
