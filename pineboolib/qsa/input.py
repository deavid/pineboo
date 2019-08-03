from PyQt5.QtWidgets import QInputDialog, QLineEdit, QWidget  # type: ignore
from typing import Any, Optional, Union, List


class Input(object):
    """
    Dialogo de entrada de datos
    """

    @classmethod
    def getText(cls, question: str, prevtxt: str = "", title: str = "Pineboo") -> Optional[str]:
        """
        Recoge texto
        @param question. Label del diálogo.
        @param prevtxt. Valor inicial a especificar en el campo
        @param title. Título del diálogo
        @return cadena de texto recogida
        """
        parent = QWidget()  # FIXME: Should be the mainWindow or similar
        text, ok = QInputDialog.getText(parent, title, question, QLineEdit.Normal, prevtxt)
        if not ok:
            return None
        return text

    @classmethod
    def getNumber(
        cls, question: str, value: Union[str, float], part_decimal: int, title: str = "Pineboo"
    ) -> Optional[float]:
        parent = QWidget()  # FIXME: Should be the mainWindow or similar
        text, ok = QInputDialog.getText(
            parent, title, question, QLineEdit.Normal, str(round(float(value), part_decimal))
        )
        if not ok:
            return None
        return float(text)

    @classmethod
    def getItem(
        cls,
        question: str,
        items_list: List[str] = [],
        title: str = "Pineboo",
        editable: bool = True,
    ) -> Any:
        """
        Recoge Item
        @param question. Label del diálogo.
        @param item_list. Lista de items.
        @param title. Título del diálogo.
        @return item, Item seleccionado.
        """

        parent = QWidget()  # FIXME: Should be the mainWindow or similar
        text, ok = QInputDialog.getItem(parent, title, question, items_list, 0, editable)
        if not ok:
            return None
        return text
