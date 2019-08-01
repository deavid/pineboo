# -*- coding: utf-8 -*-
"""
AQS package.

Main entrance to the different AQS resources.
"""

from PyQt5.QtWidgets import QFrame, QLabel, QSizePolicy, QApplication, QWidget
from PyQt5.QtGui import QColor, QPixmap, QCursor
from PyQt5.QtXml import QDomDocument
from PyQt5 import QtCore
from PyQt5 import QtGui

from pineboolib.core.utils import logging


from typing import Any, Optional, Union


logger = logging.getLogger("AQS")


class AQS(object):
    """AQS Class."""

    Box = None
    Plain = None
    translate = ["DockLeft", "ContextMenu"]
    InDock: str = "InDock"
    OutSideDock: str = "OutSideDock"
    SmtpSslConnection: int = 1
    SmtpTlsConnection: int = 2
    SmtpAuthPlain: int = 1
    SmtpAuthLogin: int = 2
    SmtpSendOk: int = 11
    SmtpError: int = 7
    SmtpMxDnsError: int = 10
    SmtpSocketError: int = 12
    SmtpAttachError: int = 15
    SmtpServerError: int = 16
    SmtpClientError: int = 17

    @staticmethod
    def ColorDialog_getColor(
        color: Optional[Union[int, str, QColor]] = None, parent: Optional["QWidget"] = None, name: Optional[str] = None
    ) -> Any:
        """
        Display the color selection dialog.

        @param color. Specify the initial color.
        @param parent. Parent.
        @param name. deprecated. Parameter used for compatibility.
        """

        from PyQt5.QtWidgets import QColorDialog  # type: ignore

        if color is None:
            qcolor = QColor("black")
        elif not isinstance(color, QColor):
            qcolor = QColor(color)
        else:
            qcolor = color

        cL = QColorDialog(qcolor, parent)
        return cL.getColor()

    @classmethod
    def toXml(cls, obj_: "QWidget", include_children: bool = True, include_complex_types: bool = False):
        """
        Convert an object to xml.

        @param obj_. Object to be processed
        @param include_children. Include children of the given object
        @param include_complex_types. Include complex children
        @return xml of the given object
        """

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

    @staticmethod
    def pixmap_fromMimeSource(name: str) -> QPixmap:
        """
        Get a QPixmap of a given file name.

        @param name. File Name
        @return QPixmap
        """

        from pineboolib.core.utils.utils_base import pixmap_fromMimeSource

        return pixmap_fromMimeSource(name)

    Pixmap_fromMineSource = pixmap_fromMimeSource

    @classmethod
    def sha1(cls, byte_array: bytes) -> str:
        """
        Return the sha1 of a set of bytes.

        @param byte_array: bytes to process.
        @return sha1 string
        """

        from pineboolib.pncontrolsfactory import QByteArray

        ba = QByteArray(byte_array)
        return ba.sha1()

    @classmethod
    def Application_setOverrideCursor(cls, shape: "QCursor", replace: bool = False) -> None:
        """
        Set override cursor.

        @param. shape. QCursor instance to override.
        @param. replace. Not used.
        """

        QApplication.setOverrideCursor(shape)

    @classmethod
    def Application_restoreOverrideCursor(cls) -> None:
        """Restore override cursor."""
        QApplication.restoreOverrideCursor()

    def __getattr__(self, name: str) -> Any:
        """
        Return the attributes of the main classes, if it is not in the class.

        @param name. Attribute name.
        @return Attribute or None.
        """

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
            logger.info("AQS: Looking up attr: %r -> %r  (Please set these in AQS)", name, ret_)
            return ret_

        logger.warning("AQS: No se encuentra el atributo %s", name)
