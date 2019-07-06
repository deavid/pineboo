from PyQt5.QtWidgets import QInputDialog, QLineEdit


class Input(object):
    """
    Dialogo de entrada de datos
    """

    @classmethod
    def getText(cls, question, prevtxt="", title="Pineboo"):
        """
        Recoge texto
        @param question. Label del diálogo.
        @param prevtxt. Valor inicial a especificar en el campo
        @param title. Título del diálogo
        @return cadena de texto recogida
        """
        text, ok = QInputDialog.getText(None, title, question, QLineEdit.Normal, prevtxt)
        if not ok:
            return None
        return text

    @classmethod
    def getNumber(cls, question, value, part_decimal, title="Pineboo"):
        text, ok = QInputDialog.getText(None, title, question, QLineEdit.Normal, str(round(float(value), part_decimal)))
        if not ok:
            return None
        return float(text)

    @classmethod
    def getItem(cls, question, items_list=[], title="Pineboo", editable=True):
        """
        Recoge Item
        @param question. Label del diálogo.
        @param item_list. Lista de items.
        @param title. Título del diálogo.
        @return item, Item seleccionado.
        """

        text, ok = QInputDialog.getItem(None, title, question, items_list, 0, editable)
        if not ok:
            return None
        return text
