# -*- coding: utf-8 -*-
from .pnfieldmetadata import PNFieldMetaData
from typing import List

# Completa Si


class PNFieldMetaDataList(object):
    """
    Lista de campos
    """

    # typedef QDict<FLFieldMetaData> FLFieldMetaDataList;
    PNFieldMetaDataList: List[PNFieldMetaData] = []
