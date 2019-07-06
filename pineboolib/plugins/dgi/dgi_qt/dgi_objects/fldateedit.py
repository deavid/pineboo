# -*- coding: utf-8 -*-

from PyQt5 import QtCore
from pineboolib.plugins.dgi.dgi_qt.dgi_objects.qdateedit import QDateEdit
from pineboolib.application.utils.date_conversion import convert_to_qdate


class FLDateEdit(QDateEdit):

    valueChanged = QtCore.pyqtSignal()
    DMY = "dd-MM-yyyy"
    _parent = None

    def __init__(self, parent, name):
        super(FLDateEdit, self).__init__(parent, name)
        self.setMinimumWidth(90)
        self.setMaximumWidth(90)
        self._parent = parent

    def setOrder(self, order):
        self.setDisplayFormat(order)

    def getDate(self):
        return super(FLDateEdit, self).date

    def setDate(self, d=None):
        if d in (None, "NAN", ""):
            date = QtCore.QDate.fromString(str("01-01-2000"), "dd-MM-yyyy")
        else:
            date = convert_to_qdate(d)

        super(FLDateEdit, self).setDate(date)
        # if not pineboolib.project._DGI.localDesktop():
        #    pineboolib.project._DGI._par.addQueque("%s_setDate" % self._parent.objectName(), date.toString())
        # else:
        self.setStyleSheet("color: black")

    date = property(getDate, setDate)
