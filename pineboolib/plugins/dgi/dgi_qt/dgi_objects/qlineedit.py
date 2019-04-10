# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
from pineboolib import decorators

class QLineEdit(QtWidgets.QLineEdit):

    _parent = None
    WindowOrigin = 0

    def __init__(self, parent=None, name = None):
        super(QLineEdit, self).__init__(parent)
        self._parent = parent
        if name:
            #self.setText(text)
            self.setObjectName(name)
        #if not pineboolib.project._DGI.localDesktop():
        #    pineboolib.project._DGI._par.addQueque("%s_CreateWidget" % self._parent.objectName(), "QLineEdit")

    def getText(self):
        return super(QLineEdit, self).text()

    def setText(self, v):
        if not isinstance(v, str):
            v = str(v)
        super(QLineEdit, self).setText(v)
        #if not pineboolib.project._DGI.localDesktop():
        #    pineboolib.project._DGI._par.addQueque("%s_setText" % self._parent.objectName(), v)

    text = property(getText, setText)
    
    @decorators.NotImplementedWarn
    def setBackgroundOrigin(self, bgo):
        pass
    
    @decorators.NotImplementedWarn
    def setLineWidth(self, w):
        pass
    
    