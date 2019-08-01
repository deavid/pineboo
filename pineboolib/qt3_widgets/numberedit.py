# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget  # type: ignore
from pineboolib.plugins.dgi.dgi_qt.dgi_objects.qlineedit import QLineEdit
from pineboolib.plugins.dgi.dgi_qt.dgi_objects.qlabel import QLabel
from pineboolib.plugins.dgi.dgi_qt.dgi_objects.qhboxlayout import QHBoxLayout
from PyQt5.Qt import QDoubleValidator  # type: ignore
from typing import Any, SupportsFloat, SupportsInt, Union


class NumberEdit(QWidget):
    """
    Diálogo para recoger un número
    """

    def __init__(self) -> None:
        super(NumberEdit, self).__init__()

        self.line_edit = QLineEdit(self)
        self.label_line_edit = QLabel(self)
        self.label_line_edit.setMinimumWidth(150)
        lay = QHBoxLayout(self)
        lay.addWidget(self.label_line_edit)
        lay.addWidget(self.line_edit)
        lay.setContentsMargins(0, 0, 0, 0)
        self.setLayout(lay)
        self.validator = QDoubleValidator()
        self.line_edit.setValidator(self.validator)

    def getValue(self) -> str:
        """
        Recoge el valor
        @return valor actual
        """
        return self.line_edit.getText()

    def setValue(self, value: Any) -> None:
        """
        Setea el valor dado como valor actual
        @param value. Nuevo valor actual
        """
        if value in ["", None]:
            return

        self.line_edit.setText(value)

    def getDecimals(self) -> int:
        """
        Recoge decimales
        @return decimales del valor actual
        """
        return self.line_edit.validator().decimals()

    def setDecimals(self, decimals: Union[bytes, str, SupportsInt]) -> None:
        """
        Setea decimales al valor actual
        @param decimals. Decimales a setear
        """
        self.line_edit.validator().setDecimals(int(decimals))

    def setMinimum(self, min: Union[bytes, str, SupportsFloat]) -> None:
        """
        Setea valor mínimo
        @param min. Valor mínimo especificable
        """
        if min in ["", None]:
            return

        self.line_edit.validator().setBottom(float(min))

    def getMinimum(self) -> Union[int, float]:
        """
        Recoge el valor mínimo seteable
        @return valor mínimo seteable
        """
        return self.line_edit.validator().bottom()

    def getMaximum(self) -> Union[int, float]:
        """
        Recoge el valor máximo seteable
        @return Valor máximo posible
        """
        return self.line_edit.validator().top()

    def setMaximum(self, max: Union[bytes, str, SupportsFloat]) -> Any:
        """
        Setea valor máximo
        @param max. Valor maximo especificable
        """
        if max in ["", None]:
            return

        return self.line_edit.validator().setTop(float(max))

    def getLabel(self) -> str:
        """
        Recoge la etiqueta del diálogo
        @return texto de la etiqueta del diálogo
        """
        return self.label_line_edit.get_text()

    def setLabel(self, label: str) -> None:
        """
        Setea la nueva etiqueta del diálogo
        @param label. Etiqueta del diálogo
        """
        self.label_line_edit.setText(label)

    label = property(getLabel, setLabel)
    value = property(getValue, setValue)
    decimals = property(getDecimals, setDecimals)
    mimimum = property(getMinimum, setMinimum)
    maximum = property(getMaximum, setMaximum)
