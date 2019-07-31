from typing import List, Optional, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from pineboolib.application.metadata.pnfieldmetadata import PNFieldMetaData  # noqa


class ITableMetaData:
    def __init__(self, n: str, a: Optional[str], q: Optional[str]) -> None:
        return

    def addFieldMD(self, f) -> None:
        return

    def field(self, fN: str) -> Any:
        return

    def fieldIsIndex(self, field_name: str) -> int:
        return -1

    def fieldList(self):
        return

    def fieldListOfCompoundKey(self, fN: str) -> Optional[List["PNFieldMetaData"]]:
        return []

    def fieldNameToAlias(self, fN: str) -> str:
        return ""

    def fieldNames(self) -> List[str]:
        return []

    def fieldNamesUnlock(self) -> List[str]:
        return []

    def inCache(self) -> bool:
        return False

    def indexFieldObject(self, position: int):
        return

    def indexPos(self, field_name: str) -> int:
        return 0

    def inicializeNewFLTableMetaData(self, n: str, a: str, q: Optional[str]) -> None:
        return

    def isQuery(self) -> bool:
        return False

    def name(self) -> str:
        return ""

    def primaryKey(self, prefixTable: bool) -> str:
        return ""

    def query(self) -> str:
        return ""

    def relation(self, fN: str, fFN: str, fTN: str):
        return

    def setCompoundKey(self, cK) -> None:
        return

    def setConcurWarn(self, b: bool) -> None:
        return

    def setDetectLocks(self, b: bool) -> None:
        return

    def setFTSFunction(self, ftsfun: str) -> None:
        return
