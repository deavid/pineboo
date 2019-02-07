# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore
from pineboolib import decorators


class QDateEdit(QtWidgets.QDateEdit):

    _parent = None
    _date = None
    separator_ = None

    def __init__(self, parent = None, name=None):
        super(QDateEdit, self).__init__(parent)
        super(QDateEdit, self).setDisplayFormat("dd-MM-yyyy")
        if name:
            self.setObjectName(name)
        self.setSeparator("-")
        self._parent = parent
        self.date_ = super(QDateEdit, self).date().toString(QtCore.Qt.ISODate)
        #if not pineboolib.project._DGI.localDesktop():
        #    pineboolib.project._DGI._par.addQueque("%s_CreateWidget" % self._parent.objectName(), "QDateEdit")

    def getDate(self):
        ret = super(QDateEdit, self).date().toString(QtCore.Qt.ISODate)
        if ret != "2000-01-01":
            return ret
        else:
            return None

    def setDate(self, v):
        if not isinstance(v, str):
            if hasattr(v, "toString"):
                print("v", v, type(v))
                v = v.toString("yyyy%sMM%sdd" % (self.separator(), self.separator()))
            else:
                v = str(v)

        date = QtCore.QDate.fromString(v[:10], "yyyy-MM-dd")
        super(QDateEdit, self).setDate(date)
        #if not pineboolib.project._DGI.localDesktop():
        #    pineboolib.project._DGI._par.addQueque("%s_setDate" % self._parent.objectName(), "QDateEdit")

    date = property(getDate, setDate)

    @decorators.NotImplementedWarn
    def setAutoAdvance(self, b):
        pass

    def setSeparator(self, c):
        self.separator_ = c
        self.setDisplayFormat("dd%sMM%syyyy" % (self.separator(), self.separator()))

    def separator(self):
        return self.separator_

    def __getattr__(self, name):
        if name == "date":
            return super(QDateEdit, self).date().toString(QtCore.Qt.ISODate)