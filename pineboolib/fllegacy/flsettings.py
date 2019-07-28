# -*- coding: utf-8 -*-
from pineboolib.core.settings import settings


from typing import List, Optional, Union, Any
from typing import SupportsFloat


class FLSettings(object):
    s = settings

    def readListEntry(self, key: str) -> List[str]:
        ret = self.s.value(key)
        if ret is None:
            return []
        if isinstance(ret, str):
            return [ret]
        if isinstance(ret, list):
            return ret

        raise ValueError("Configuration key %s does not contain a list" % key)

    def readEntry(self, _key: str, _def: Optional[Union[str, bool]] = None) -> Any:
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
            if isinstance(ret, (int, float, str)):
                return int(ret)
            else:
                raise ValueError(
                    "Configuration key %s cannot be converted to integer" % key
                )
        else:
            return _def

    def readDoubleEntry(
        self, key: str, _def: Union[bytes, str, SupportsFloat] = 0
    ) -> float:
        ret = self.s.value(key)
        if ret is None:
            ret = _def
        return float(ret)

    def readBoolEntry(self, key: str, _def: bool = False) -> bool:
        ret = self.s.value(key)
        if ret is None:
            return _def
        if isinstance(ret, str):
            return ret == "true"
        if isinstance(ret, int):
            return ret != 0
        if isinstance(ret, bool):
            return ret
        raise ValueError("Configuration key %s cannot be converted to boolean" % key)

    def writeEntry(self, key: str, value: Union[int, str, bool]) -> None:
        self.s.setValue(key, value)

    def writeEntryList(self, key: str, value: List[str]) -> None:
        # FIXME: This function flattens the array when saving in some cases. Should always save an array.
        val: Union[str, List[str]]
        if len(value) == 1:
            val = value[0]
        elif len(value) == 0:
            val = ""
        else:
            val = value

        self.s.setValue(key, val)
