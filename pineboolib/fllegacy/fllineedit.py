# -*- coding: utf-8 -*-
"""Fllineedit module."""

from PyQt5 import QtCore, QtWidgets  # type: ignore
from pineboolib import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)


class FLLineEdit(QtWidgets.QLineEdit):
    """FLLineEdit class."""

    _tipo: str
    _part_decimal: int
    _part_integer: int
    _max_value: int
    _auto_select: bool
    _name: str
    _longitud_max: int
    _parent: QtWidgets.QWidget
    _last_text: str
    _formating: bool
    _field_name: str

    lostFocus = QtCore.pyqtSignal()

    def __init__(self, parent: QtWidgets.QWidget, name: str = "") -> None:
        """Inicialize."""

        super(FLLineEdit, self).__init__(parent)
        self._name = name
        if hasattr(parent, "fieldName_"):
            if isinstance(parent.fieldName_, str):
                self._field_name = parent.fieldName_

            self._tipo = parent.cursor_.metadata().field(self._field_name).type()
            self._part_decimal = 0
            self._auto_select = True
            self._formating = False
            self._part_integer = parent.cursor_.metadata().field(self._field_name).partInteger()

            self._parent = parent

            if self._tipo == "string":
                self._longitud_max = parent.cursor_.metadata().field(self._field_name).length()
                self.setMaxLength(self._longitud_max)

            if self._tipo in ("int", "uint", "double"):
                self.setAlignment(QtCore.Qt.AlignRight)

    def setText(self, text_: str, check_focus: bool = True) -> None:
        """Set text to control."""

        text_ = str(text_)
        # if not project.DGI.localDesktop():
        #    project.DGI._par.addQueque("%s_setText" % self._parent.objectName(), text_)
        # else:
        if check_focus:

            if text_ in ("", None) or self.hasFocus():
                super().setText(text_)
                return

        ok = False
        s = text_
        minus = False

        if self._tipo == "double":
            if s[0] == "-":
                minus = True
                s = s[1:]

            val, ok = QtCore.QLocale.system().toDouble(s.replace(".", ","))

            if ok:
                s = QtCore.QLocale.system().toString(float(s), "f", self._part_decimal)
            if minus:
                s = "-%s" % s

        elif self._tipo in ("int"):
            val, ok = QtCore.QLocale.system().toInt(s)
            if ok:
                s = QtCore.QLocale.system().toString(val)

        elif self._tipo in ("uint"):
            val, ok = QtCore.QLocale.system().toUInt(s)
            if ok:
                s = QtCore.QLocale.system().toString(val)

        super().setText(str(s))

    def text(self) -> str:
        """Return text from control."""

        text_ = super().text()
        if text_ == "":
            return text_

        ok = False
        minus = False

        if self._tipo == "double":
            if text_[0] == "-":
                minus = True
                text_ = text_[1:]

            val, ok = QtCore.QLocale.system().toDouble(text_)
            if ok:
                text_ = str(val)

            if minus:
                text_ = "-%s" % text_

        elif self._tipo == "uint":
            val, ok = QtCore.QLocale.system().toUInt(text_)
            if ok:
                text_ = str(val)

        elif self._tipo == "int":
            val, ok = QtCore.QLocale.system().toInt(text_)

            if ok:
                text_ = str(val)

        return text_

    def setMaxValue(self, max_value: int) -> None:
        """Set max value for numeric types."""

        self._max_value = max_value

    def focusOutEvent(self, f: Any) -> None:
        """Focus out event."""

        if self._tipo in ("double", "int", "uint"):
            text_ = super().text()

            if self._tipo == "double":

                val, ok = QtCore.QLocale.system().toDouble(text_)

                if ok:
                    text_ = QtCore.QLocale.system().toString(val, "f", self._part_decimal)
                super().setText(text_)
            else:

                self.setText(text_)
        super().focusOutEvent(f)

    def focusInEvent(self, f: Any) -> None:
        """Focus in event."""

        if self.isReadOnly():
            return

        if self._tipo in ("double", "int", "uint"):
            self.blockSignals(True)
            s = self.text()
            if self._tipo == "double":
                if s != "":
                    s = QtCore.QLocale.system().toString(float(s), "f", self._part_decimal)

                if QtCore.QLocale.system().toString(float(s), "f", 1)[1] == ",":
                    s = s.replace(".", "")
                else:
                    s = s.replace(",", "")

            v = self.validator()
            if v:
                pos = 0
                v.validate(s, pos)

            super().setText(s)
            self.blockSignals(False)

        if self._auto_select and not self.selectedText() and not self.isReadOnly():
            self.selectAll()

        super().focusInEvent(f)
