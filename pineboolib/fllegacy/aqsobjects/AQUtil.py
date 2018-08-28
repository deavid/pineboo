# -*- coding: utf-8 -*-
import logging


class AQUtil(object):

    util = None
    logger = None

    def __init__(self):
        from pineboolib.fllegacy.FLUtil import FLUtil
        self.util = FLUtil()
        self.logger = logging.getLogger(__name__)

    def __getattr__(self, name):
        self.logger.info("Usando function FAKE %s de FLUtil()", name)
        return getattr(self.util, name)
