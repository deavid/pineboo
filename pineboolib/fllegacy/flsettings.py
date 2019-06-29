# -*- coding: utf-8 -*-
from pineboolib.core.settings import settings


from typing import List, Optional, Union


class FLSettings(object):
    s = settings

    def readListEntry(self, key: str) -> List[str]:
        ret = self.s.value(key)
        if isinstance(ret, str):
            ret = [ret]
        if ret is None:
            ret = []
        return ret

    def readEntry(self, _key: str, _def: Optional[Union[str, bool]] = None) -> Optional[Union[str, bool]]:
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

        # print("Retornando %s ---> %s (%s)" % (_key, ret, type(ret)))
        return ret

    def readNumEntry(self, key: str, _def: int = 0) -> int:
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

    def readBoolEntry(self, key: str, _def: bool = False) -> bool:
        ret = self.s.value(key)
        if isinstance(ret, str):
            ret = ret == "true"
        if ret is None:
            ret = _def

        return ret

    def writeEntry(self, key: str, value: Union[int, str, bool]) -> None:
        self.s.setValue(key, value)

    def writeEntryList(self, key: str, value: List[str]) -> None:

        if len(value) == 1:
            val = value[0]
        elif len(value) == 0:
            val = ""
        else:
            val = value

        self.s.setValue(key, val)
