# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtCore

class QComboBox(QtWidgets.QComboBox):

    _parent = None

    def __init__(self, parent=None):
        self._parent = parent
        super(QComboBox, self).__init__(parent)

    # def __getattr__(self, name):
    #    return DefFun(self, name)

    @QtCore.pyqtProperty(str)
    def currentItem(self):
        return self.currentIndex

    @currentItem.setter
    def currentItem(self, i):
        if i:
            #if not pineboolib.project._DGI.localDesktop():
            #    pineboolib.project._DGI._par.addQueque("%s_setCurrentIndex" % self.objectName(), n)
            self.setCurrentIndex(i)

    def insertStringList(self, strl):
        #if not pineboolib.project._DGI.localDesktop():
        #    pineboolib.project._DGI._par.addQueque("%s_insertStringList" % self.objectName(), strl)
        self.insertItems(len(strl), strl)