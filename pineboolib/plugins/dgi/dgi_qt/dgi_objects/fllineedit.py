# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets  # type: ignore
from pineboolib import logging
from pineboolib.fllegacy.flapplication import aqApp
from typing import Any


class FLLineEdit(QtWidgets.QLineEdit):
    logger = logging.getLogger(__name__)
    _tipo: str = ""
    partDecimal = 0
    partInteger = 0
    _maxValue = None
    autoSelect = True
    _name = None
    _longitudMax = None
    _parent = None
    _last_text = None
    _formating = False

    lostFocus = QtCore.pyqtSignal()

    def __init__(self, parent, name=None) -> None:
        super(FLLineEdit, self).__init__(parent)
        self._name = name
        if hasattr(parent, "fieldName_"):
            if isinstance(parent.fieldName_, str):
                self._fieldName = parent.fieldName_

            self._tipo = parent.cursor_.metadata().field(self._fieldName).type()
            self.partDecimal = 0
            self.autoSelect = True
            self.partInteger = parent.cursor_.metadata().field(self._fieldName).partInteger()

            self._parent = parent

            if self._tipo == "string":
                self._longitudMax = parent.cursor_.metadata().field(self._fieldName).length()
                self.setMaxLength(self._longitudMax)

            if self._tipo in ("int", "uint", "double"):
                self.setAlignment(QtCore.Qt.AlignRight)

    def setText(self, text_, check_focus=True) -> None:
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
            if aqApp.commaSeparator() == ",":
                s = s.replace(".", ",")

            val, ok = aqApp.localeSystem().toDouble(s)
            if ok:
                s = aqApp.localeSystem().toString(val, "f", self.partDecimal)
            if minus:
                s = "-%s" % s

        elif self._tipo in ("int"):
            val, ok = aqApp.localeSystem().toInt(s)
            if ok:
                s = aqApp.localeSystem().toString(val)

        elif self._tipo in ("uint"):
            val, ok = aqApp.localeSystem().toUInt(s)
            if ok:
                s = aqApp.localeSystem().toString(val)

        super().setText(s)

    def text(self) -> Any:
        text_ = super().text()
        if text_ == "":
            return text_

        ok = False
        minus = False

        if self._tipo == "double":
            if text_[0] == "-":
                minus = True
                text_ = text_[1:]

            val, ok = aqApp.localeSystem().toDouble(text_)
            if ok:
                text_ = str(val)

            if minus:
                text_ = "-%s" % text_

        elif self._tipo == "uint":
            val, ok = aqApp.localeSystem().toUInt(text_)
            if ok:
                text_ = str(val)

        elif self._tipo == "int":
            val, ok = aqApp.localeSystem().toInt(text_)

            if ok:
                text_ = str(val)

        return text_

    def setMaxValue(self, max_value) -> None:
        self._maxValue = max_value

    def focusOutEvent(self, f) -> None:
        if self._tipo in ("double", "int", "uint"):
            text_ = super(FLLineEdit, self).text()

            if self._tipo == "double":

                val, ok = aqApp.localeSystem().toDouble(text_)

                if ok:
                    text_ = aqApp.localeSystem().toString(val, "f", self.partDecimal)
                super().setText(text_)
            else:

                self.setText(text_)
        super().focusOutEvent(f)

    def focusInEvent(self, f) -> None:
        if self.isReadOnly():
            return

        if self._tipo in ("double", "int", "uint"):
            self.blockSignals(True)
            s = self.text()
            if self._tipo == "double":
                if s != "":
                    s = aqApp.localeSystem().toString(float(s), "f", self.partDecimal)
                if aqApp.commaSeparator() == ",":
                    s = s.replace(".", "")
                else:
                    s = s.replace(",", "")

            v = self.validator()
            if v:
                pos = 0
                v.validate(s, pos)

            super().setText(s)
            self.blockSignals(False)

        if self.autoSelect and not self.selectedText() and not self.isReadOnly():
            self.selectAll()

        super().focusInEvent(f)
