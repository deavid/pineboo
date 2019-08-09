"""Input module."""

from PyQt5.QtWidgets import QInputDialog, QLineEdit, QWidget  # type: ignore
from typing import Any, Optional, Union, List


class Input(object):
    """
    Data entry dialog.
    """

    @classmethod
    def getText(cls, question: str, prevtxt: str = "", title: str = "Pineboo") -> Optional[str]:
        """
        Return Text.

        @param question. Label of the dialogue.
        @param prevtxt. Initial value to specify in the field.
        @param title. Title of the dialogue.
        @return string of collected text.
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
        """Return number."""

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
        Return Item.

        @param question. Label of the dialogue.
        @param item_list. Items List.
        @param title. Title of the dialogue.
        @return item, Selected item.
        """

        parent = QWidget()  # FIXME: Should be the mainWindow or similar
        text, ok = QInputDialog.getItem(parent, title, question, items_list, 0, editable)
        if not ok:
            return None
        return text
