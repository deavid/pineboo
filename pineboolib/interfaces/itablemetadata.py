from typing import List, Optional


class ITableMetaData:
    def __init__(self, n: str, a: Optional[str], q: Optional[str]) -> None:
        pass

    def addFieldMD(self, f) -> None:
        pass

    def field(self, fN: Optional[str]):
        pass

    def fieldIsIndex(self, field_name: Optional[str]) -> int:
        pass

    def fieldList(self, prefix_table: bool):
        pass

    def fieldListOfCompoundKey(self, fN: str) -> None:
        pass

    def fieldNameToAlias(self, fN: str) -> str:
        pass

    def fieldNames(self) -> List[str]:
        pass

    def fieldNamesUnlock(self) -> List[str]:
        pass

    def inCache(self) -> bool:
        pass

    def indexFieldObject(self, position: int, show_exception: bool):
        pass

    def indexPos(self, field_name: Optional[str]) -> int:
        pass

    def inicializeNewFLTableMetaData(self, n: str, a: str, q: Optional[str]) -> None:
        pass

    def isQuery(self) -> bool:
        pass

    def name(self) -> str:
        pass

    def primaryKey(self, prefixTable: bool) -> str:
        pass

    def query(self) -> str:
        pass

    def relation(self, fN: str, fFN: str, fTN: str):
        pass

    def setCompoundKey(self, cK) -> None:
        pass

    def setConcurWarn(self, b: bool) -> None:
        pass

    def setDetectLocks(self, b: bool) -> None:
        pass

    def setFTSFunction(self, ftsfun: None) -> None:
        pass
