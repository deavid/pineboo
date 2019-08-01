# -*- coding: utf-8 -*-
"""
AQUtil Module.

Use the resources of pineboolib.fllegacy.flutil.FLUtil.
"""

from pineboolib import logging
from pineboolib.fllegacy.flutil import FLUtil


class AQUtil(FLUtil):
    """AQUtil Class."""

    def __init__(self) -> None:
        """Initialize a new instance."""

        self._logger = logging.getLogger(__name__)
