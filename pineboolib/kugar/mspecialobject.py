from enum import Enum

from PyQt5 import QtCore

from pineboolib import decorators

from pineboolib.kugar.mreportobject import MReportObject
from pineboolib.kugar.mlabelobject import MLabelObject
from pineboolib.kugar.mutil import MUtil


class MSpecialObject(MLabelObject):

    class SpecialType(Enum):
        Date = 0
        PageNumber = 1

    @decorators.BetaImplementation
    def __init__(self, *args):
        super(MSpecialObject, self).__init__(*args)

        if isinstance(args[0], MSpecialObject):
            self.copy(args[0])
        else:
            self.text_ = None
            self.type_ = self.SpecialType.Date
            self.format_ = MUtil.DateFormatType.MDY_SLASH

    @decorators.NotImplementedWarn
    # def operator=(self, mso): #FIXME
    def operator(self, mso):
        return self

    @decorators.BetaImplementation
    def setText(self, d):
        if isinstance(d, QtCore.QDate):
            self.text_ = MUtil.formatDate(d, self.format_)
        else:
            self.text_.setNum(d)

    @decorators.BetaImplementation
    def setType(self, t):
        self.type_ = t

    @decorators.BetaImplementation
    def getType(self):
        return self.type_

    @decorators.BetaImplementation
    def setDateFormat(self, f):
        self.format_ = f

    @decorators.BetaImplementation
    def copy(self, mso):
        self.type_ = mso.type_

    @decorators.BetaImplementation
    def RTTI(self):
        return MReportObject.ReportObjectType.Special
