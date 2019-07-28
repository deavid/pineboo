# -*- coding: utf-8 -*-
import json
import time
from .utils import logging

from PyQt5.QtCore import QSettings, QSize

from typing import Dict, List, Any, Union, Tuple, Type

logger = logging.getLogger("core.settings")


class PinebooSettings(QSettings):
    CACHE_TIME_SEC = 30

    def __init__(self, name: str = "") -> None:
        format = QSettings.IniFormat  # QSettings.NativeFormat - usar solo ficheros ini.
        scope = QSettings.UserScope
        self.organization = "Eneboo"
        self.application = "Pineboo" + name
        self.cache: Dict[str, Tuple[float, Any]] = {}
        super().__init__(format, scope, self.organization, self.application)

    @staticmethod
    def dump_qsize(value: QSize) -> Dict[str, Any]:
        return {"__class__": "QSize", "width": value.width(), "height": value.height()}

    def dump_value(
        self, value: Union[QSize, str, bool, int, List[str], Dict[Any, Any]]
    ) -> str:
        if isinstance(value, QSize):
            value = self.dump_qsize(value)
        return json.dumps(value)

    def load_value(self, value_text: str) -> Any:
        value: Any = json.loads(value_text)
        if isinstance(value, dict) and "__class__" in value.keys():
            classname = value["__class__"]
            if classname == "QSize":
                return QSize(value["width"], value["height"])
            else:
                raise ValueError("Unknown classname %r" % classname)
        return value

    def value(self, key: str, defaultValue: Any = None, type: Type = None) -> Any:
        curtime = time.time()
        cachedVal = self.cache.get(key, None)
        if cachedVal:
            if curtime - cachedVal[0] > self.CACHE_TIME_SEC:
                del self.cache[key]
            else:
                return cachedVal[1]
        val = self._value(key, defaultValue)
        self.cache[key] = (curtime, val)
        return val

    def _value(self, key: str, default: Any = None) -> Any:
        value = super().value(key, None)
        if value is None:
            logger.debug(
                "%s.value(%s) -> Default: %s %r",
                self.application,
                key,
                type(default),
                default,
            )
            return default
        try:
            ret = self.load_value(value)
            logger.debug(
                "%s.value(%s) -> Loaded: %s %r", self.application, key, type(ret), ret
            )
            return ret
        except Exception as exc:
            # No format, just string
            logger.debug("Error trying to parse json for %s: %s (%s)", key, exc, value)
            return value

    def set_value(
        self, key: str, value: Union[QSize, str, bool, int, List[str]]
    ) -> None:
        logger.debug(
            "%s.set_value(%s) <- %s %r", self.application, key, type(value), value
        )
        return super().setValue(key, self.dump_value(value))

    setValue = set_value


config = PinebooSettings("Config")
settings = PinebooSettings("Settings")
