# -*- coding: utf-8 -*-
import logging
import json

from PyQt5.QtCore import QSettings

logger = logging.getLogger("core.settings")


class PinebooSettings(QSettings):
    def __init__(self, name=""):
        format = QSettings.IniFormat  # QSettings.NativeFormat - usar solo ficheros ini.
        scope = QSettings.UserScope
        organization = "Eneboo"
        application = "Pineboo" + name
        super(PinebooSettings, self).__init__(format, scope, organization, application)

    def dump_value(self, value):
        return json.dumps(value)

    def value(self, key, default=None):
        value = super(QSettings, self).value(key, None)
        if value is None:
            return default
        try:
            return json.loads(value)
        except Exception as exc:
            # No format, just string
            logger.debug("Error trying to parse json for %s: %s (%s)", key, exc, value)
            return value

    def set_value(self, key, value):
        return super(QSettings, self).setValue(key, json.dumps(value))

    setValue = set_value


config = PinebooSettings("Config")
settings = PinebooSettings("Settings")
