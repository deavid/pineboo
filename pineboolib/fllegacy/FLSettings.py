# -*- coding: utf-8 -*-

from PyQt5 import QtCore
from pineboolib import decorators


class FLSettings(QtCore.QObject):

    s = QtCore.QSettings(QtCore.QSettings.NativeFormat,
                         QtCore.QSettings.UserScope, "Eneboo", "Pineboo")

    @decorators.BetaImplementation
    def readListEntry(self, key, retOk=False):
        ret = self.s.value(key)
        return ret

    def readEntry(self, _key, _def=None, retOk=False):
        ret = self.s.value(_key, None)  # devuelve un QVariant !!!!

        if "geo" in _key:
            # print("Geo vale", str(ret))
            # ret = ret.toSize()
            # print("Geo vale", str(ret))
            if not ret:
                ret = _def
        else:
            if ret in ["", None] and _def is not None:
                ret = _def

        #print("Retornando %s ---> %s (%s)" % (_key, ret, type(ret)))
        return ret

    @decorators.BetaImplementation
    def readNumEntry(self, key, _def=0, retOk=False):
        ret = self.s.value(key)
        return int(ret)

    @decorators.BetaImplementation
    def readDoubleEntry(self, key, _def=0, retOk=False):
        ret = self.s.value(key)
        return float(ret)

    def readBoolEntry(self, key, _def=False, retOk=False):
        ret = self.s.value(key)
        if isinstance(ret, str):
            ret = ret == "true"
        if ret is None:
            ret = _def

        return ret

    def writeEntry(self, key, value):
        self.s.setValue(key, value)

    @decorators.BetaImplementation
    def writeEntryList(self, key, value):
        self.s.setValue(key, value)
