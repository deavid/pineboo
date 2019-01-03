# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtCore
from pineboolib import decorators

class QTextEdit(QtWidgets.QTextEdit):
    LogText = 0

    def __init__(self, parent = None):
        super(QTextEdit, self).__init__(parent)
        self.LogText = 0

    def setText(self, text):       
        super(QTextEdit, self).setText(text)
        #if not pineboolib.project._DGI.localDesktop():
        #    pineboolib.project._DGI._par.addQueque("%s_setText" % self._parent.objectName(), text)

    def getText(self):
        return super(QTextEdit, self).toPlainText()

    @decorators.NotImplementedWarn
    def textFormat(self):
        return

    @decorators.Incomplete
    def setTextFormat(self, value):
        if value == 0:  # LogText
            self.setReadOnly(True)

    def setShown(self, value):
        if value:
            super().show()
        else:
            super().hide()
    
    def getPlainText(self):
        return super(QTextEdit, self).toPlainText()

    def setAutoFormatting(self, value):
        value = QtWidgets.QTextEdit.AutoAll
        super(QTextEdit, self).setAutoFormatting(value)

    text = property(getText, setText)
    PlainText = property(getPlainText, setText)