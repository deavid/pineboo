# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QFrame, QLabel, QSizePolicy, QApplication  # type: ignore
from PyQt5.QtXml import QDomDocument  # type: ignore
from PyQt5 import QtCore  # type: ignore
from PyQt5 import QtGui  # type: ignore

from pineboolib.core.utils import logging


from typing import Type, Any, Optional, Union
from PyQt5.Qt import QCursor  # type: ignore
from PyQt5.QtWidgets import QWidget  # type : ignore
from PyQt5.QtGui import QColor  # type: ignore

logger = logging.getLogger("AQS")

"""
Clase AQS
"""


class AQS(object):

    Box = None
    Plain = None
    translate = ["DockLeft", "ContextMenu"]

    def __init__(self) -> None:
        self.InDock: str = "InDock"
        self.OutSideDock: str = "OutSideDock"
        self.SmtpSslConnection: int = 1
        self.SmtpTlsConnection: int = 2
        self.SmtpAuthPlain: int = 1
        self.SmtpAuthLogin: int = 2
        self.SmtpSendOk: int = 11
        self.SmtpError: int = 7
        self.SmtpMxDnsError: int = 10
        self.SmtpSocketError: int = 12
        self.SmtpAttachError: int = 15
        self.SmtpServerError: int = 16
        self.SmtpClientError: int = 17

    """
    Muestra el dialog de selección de color
    @param color. Especifica el color inicial
    @param parent. Parent
    @param name. deprecated. Paramametro usado para compatibilidad
    """

    def ColorDialog_getColor(
        self, color: Optional[Union[int, str, QColor]] = None, parent: Optional["QWidget"] = None, name: Optional[str] = None
    ) -> Any:
        from PyQt5.QtWidgets import QColorDialog  # type: ignore

        if color is None:
            qcolor = QColor("black")
        elif not isinstance(color, QColor):
            qcolor = QColor(color)
        else:
            qcolor = color

        cL = QColorDialog(qcolor, parent)
        return cL.getColor()

    """
    Convierte un objeto a xml
    @param obj_. Objeto a procesar
    @param include_children. Incluir hijos del objeto dado
    @param include_complex_types. Incluir hijos complejos
    @return xml del objeto dado
    """

    @classmethod
    def toXml(cls: Type["AQS"], obj_: "QWidget", include_children: bool = True, include_complex_types: bool = False):
        xml_ = QDomDocument()

        if not obj_:
            return xml_

        e = xml_.createElement(type(obj_).__name__)
        e.setAttribute("class", type(obj_).__name__)
        xml_.appendChild(e)

        _meta = obj_.metaObject()

        i = 0
        # _p_properties = []
        for i in range(_meta.propertyCount()):
            mp = _meta.property(i)
            # if mp.name() in _p_properties:
            #    i += 1
            #    continue

            # _p_properties.append(mp.name())

            val = getattr(obj_, mp.name(), None)
            try:
                val = val()
            except Exception:
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

        if include_children:

            for child in obj_.children():

                itd = cls.toXml(child, include_children, include_complex_types)
                xml_.firstChild().appendChild(itd.firstChild())
        return xml_

    """
    Obtiene un QPixmap de un nombre de fichero dado
    @param name. Nombre del fichero
    @return QPixmap
    """

    @staticmethod
    def pixmap_fromMimeSource(name: str) -> Any:
        from pineboolib.core.utils.utils_base import pixmap_fromMimeSource

        return pixmap_fromMimeSource(name)

    Pixmap_fromMineSource = pixmap_fromMimeSource

    @classmethod
    def sha1(self, byte_array: bytes) -> Any:
        from pineboolib.pncontrolsfactory import QByteArray

        ba = QByteArray(byte_array)
        return ba.sha1()

    @classmethod
    def Application_setOverrideCursor(self, shape: "QCursor", replace: bool = False) -> None:
        QApplication.setOverrideCursor(shape)

    @classmethod
    def Application_restoreOverrideCursor(self) -> None:
        QApplication.restoreOverrideCursor()

    def __getattr__(self, name: str) -> Any:
        if name in self.translate:
            if name == "DockLeft":
                name = "LeftDockWidgetArea"

        ret_ = getattr(QtGui, "Q%sEvent" % name, None)

        if ret_ is None:
            for lib in [QFrame, QLabel, QSizePolicy, QtCore.Qt]:
                ret_ = getattr(lib, name, None)
                if ret_ is not None:
                    break

        if ret_ is not None:
            return ret_

        logger.warning("AQS: No se encuentra el atributo %s", name)
