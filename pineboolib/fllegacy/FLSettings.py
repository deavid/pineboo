# -*- coding: utf-8 -*-

from PyQt5 import QtCore


class FLSettings(QtCore.QObject):

    s = QtCore.QSettings(QtCore.QSettings.NativeFormat,
                         QtCore.QSettings.UserScope, "Eneboo", "Pineboo")

    def readListEntry(self, key):
        ret = self.s.value(key)
        if isinstance(ret, str):
            ret = [ret]
        if ret is None:
            ret = []
        return ret

    def readEntry(self, _key, _def=None):
        ret = self.s.value(_key, None)  # devuelve un QVariant !!!!

        if "geo" in _key:
            # print("Geo vale", str(ret))
            # ret = ret.toSize()
            # print("Geo vale", str(ret))
            if not ret:
                ret = _def
        else:
            if ret in ["", None]:
                ret = _def

        #print("Retornando %s ---> %s (%s)" % (_key, ret, type(ret)))
        return ret

    def readNumEntry(self, key, _def=0):
        ret = self.s.value(key)
        if ret is not None:
            return int(ret)
        else:
            return _def

    def readDoubleEntry(self, key, _def=0):
        ret = self.s.value(key)
        if ret is None:
            ret = _def
        return float(ret)

    def readBoolEntry(self, key, _def=False):
        ret = self.s.value(key)
        if isinstance(ret, str):
            ret = ret == "true"
        if ret is None:
            ret = _def

        return ret

    def writeEntry(self, key, value):
        self.s.setValue(key, value)

    def writeEntryList(self, key, value):
        if len(value) == 1:
            val = value[0]
        else:
            val = value

        self.s.setValue(key, val)
