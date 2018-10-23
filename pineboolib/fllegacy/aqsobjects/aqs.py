# -*- coding: utf-8 -*-
from PyQt5.QtGui import QColor, QPixmap
from PyQt5.QtWidgets import QFrame, QLabel, QSizePolicy
from PyQt5 import QtCore
from PyQt5 import QtGui

from pineboolib.utils import filedir

import logging
from PyQt5.QtXml import QDomDocument

logger = logging.getLogger("AQS")

"""
Clase AQS
"""
class AQS(object):

    Box = None
    Plain = None
    translate = ["DockLeft", "ContextMenu"]
    InDock = None

    def __init__(self):
        self.InDock = "InDock"
        self.OutSideDock = "OutSideDock"

    """
    Muestra el dialog de selección de color
    @param color. Especifica el color inicial
    @param parent. Parent
    @param name. deprecated. Paramametro usado para compatibilidad
    """
    def ColorDialog_getColor(self, color=None, parent=None, name=None):
        from PyQt5.QtWidgets import QColorDialog
        from PyQt5.QtGui import QColor

        if color is None:
            color = QColor.black()

        if isinstance(color, str):
            color = QColor()

        cL = QColorDialog(color, parent)
        return cL.getColor()

    """
    Convierte un objeto a xml
    @param obj_. Objeto a procesar
    @param include_children. Incluir hijos del objeto dado
    @param include_complex_types. Incluir hijos complejos
    @return xml del objeto dado
    """
    def toXml(self, obj_, include_children=True, include_complex_types=False):
        xml_ = QDomDocument()

        if not obj_:
            return xml_

        e = xml_.createElement(type(obj_).__name__)
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

            if not val and not include_complex_types:
                i += 1
                continue
            e.setAttribute(mp.name(), val)

            i += 1

        if include_children == True:

            for child in obj_.children():

                itd = self.toXml(child, include_children, include_complex_types)
                xml_.firstChild().appendChild(itd.firstChild())
        return xml_

    """
    Obtiene un QPixmap de un nombre de ficehro dado
    @param name. Nombre del fichero
    @return QPixmap
    """
    def Pixmap_fromMineSource(self, name):
        import os
        file_name = filedir("../share/icons", name)
        return QPixmap(file_name) if os.path.exists(file_name) else None

    def __getattr__(self, name):

        ret_ = getattr(QtGui, "Q%sEvent" % name, None)
        if ret_:
            return ret_

        if name in self.translate:
            if name == "DockLeft":
                name = "LeftDockWidgetArea"

        for lib in [QFrame, QLabel, QSizePolicy, QtCore.Qt]:
            ret_ = getattr(lib, name, None)

            if ret_ is not None:
                return ret_

        logger.warn("AQS: No se encuentra el atributo %s", name)
