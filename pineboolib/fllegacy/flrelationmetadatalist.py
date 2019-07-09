# -*- coding: utf-8 -*-
from pineboolib.fllegacy.flfieldmetadata import FLFieldMetaData
from typing import List

# Completa Si


class FLRelationMetaDataList:
    """
    Lista de relaciones
    """

    # typedef QDict<FLFieldMetaData> FLFieldMetaDataList;
    FLRelationMetaDataList: List[FLFieldMetaData] = []
