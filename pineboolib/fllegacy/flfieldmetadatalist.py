# -*- coding: utf-8 -*-
from pineboolib.fllegacy.flfieldmetadata import FLFieldMetaData
from typing import List

# Completa Si


class FLFieldMetaDataList(object):
    """
    Lista de campos
    """

    # typedef QDict<FLFieldMetaData> FLFieldMetaDataList;
    FLFieldMetaDataList: List[FLFieldMetaData] = []
