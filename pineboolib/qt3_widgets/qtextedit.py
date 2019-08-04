# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets  # type: ignore
from pineboolib.core import decorators
from typing import Any


class QTextEdit(QtWidgets.QTextEdit):
    LogText = 0
    RichText = 1

    def __init__(self, parent=None) -> None:
        super(QTextEdit, self).__init__(parent)
        self.LogText = 0

    def setText(self, text) -> None:
        super(QTextEdit, self).setText(text)
        # if not project.DGI.localDesktop():
        #    project.DGI._par.addQueque("%s_setText" % self._parent.objectName(), text)

    def getText(self) -> Any:
        return super(QTextEdit, self).toPlainText()

    @decorators.NotImplementedWarn
    def textFormat(self):
        return

    @decorators.Incomplete
    def setTextFormat(self, value):
        if value == 0:  # LogText
            self.setReadOnly(True)
            self.setAcceptRichText(False)
        elif value == 1:
            self.setReadOnly(False)
            self.setAcceptRichText(True)

    def setShown(self, value) -> None:
        if value:
            super().show()
        else:
            super().hide()

    def getPlainText(self) -> Any:
        return super(QTextEdit, self).toPlainText()

    def setAutoFormatting(self, value) -> None:
        value = QtWidgets.QTextEdit.AutoAll
        super(QTextEdit, self).setAutoFormatting(value)

    text = property(getText, setText)
    PlainText = property(getPlainText, setText)
