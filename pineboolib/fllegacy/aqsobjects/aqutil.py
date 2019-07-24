# -*- coding: utf-8 -*-
from pineboolib import logging
from typing import Any


class AQUtil(object):

    util = None
    logger = None

    def __init__(self) -> None:
        from pineboolib.fllegacy.flutil import FLUtil

        self.util = FLUtil()
        self.logger = logging.getLogger(__name__)

    def __getattr__(self, name: str) -> Any:
        # self.logger.info("Usando function FAKE %s de FLUtil()", name)
        result = getattr(self.util, name, None)
        if result is None:
            raise Exception('AQUtil can\'t load "%s" attribute fom FLUtil!' % name)

        return result
