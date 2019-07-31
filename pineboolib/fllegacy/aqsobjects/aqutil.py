# -*- coding: utf-8 -*-
"""
AQUtil Module.

Use the resources of pineboolib.fllegacy.flutil.FLUtil.
"""

from pineboolib import logging
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from pineboolib.fllegacy.flutil import FLUtil


class AQUtil(object):
    """AQUtil Class."""

    _util: "FLUtil"

    def __init__(self) -> None:
        """Initialize a new instance."""

        from pineboolib.fllegacy.flutil import FLUtil

        self._util = FLUtil()
        self._logger = logging.getLogger(__name__)

    def __getattr__(self, name: str) -> Any:
        """Search attributes on self._util."""

        # self.logger.info("Usando function FAKE %s de FLUtil()", name)
        result = getattr(self._util, name, None)
        if result is None:
            raise Exception('AQUtil can\'t load "%s" attribute fom FLUtil!' % name)

        return result
