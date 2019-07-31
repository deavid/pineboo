# -*- coding: utf-8 -*-
"""PNFieldMetaData list."""

from .pnfieldmetadata import PNFieldMetaData
from typing import List

# Completa Si


class PNFieldMetaDataList(object):
    """PNFieldMetaData Class."""

    # typedef QDict<FLFieldMetaData> FLFieldMetaDataList;
    PNFieldMetaDataList: List[PNFieldMetaData] = []
