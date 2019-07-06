from typing import Any, Callable, Dict, Mapping, Optional, Union, TYPE_CHECKING

if TYPE_CHECKING:
    import pineboolib.pnconnection
    import pineboolib.fllegacy.flaction
    import pineboolib.fllegacy.fltablemetadata
    import pineboolib.fllegacy.flfieldmetadata
    import pineboolib.fllegacy.flrelationmetadata
    import pineboolib.fllegacy.flsqlquery


class IManager(object):
    __doc__: str
    buffer_: None
    cacheAction_: Optional[Dict[str, "pineboolib.fllegacy.flaction.FLAction"]]
    cacheMetaDataSys_: Optional[dict]
    cacheMetaData_: Optional[dict]
    db_: Optional["pineboolib.pnconnection.PNConnection"]
    dictKeyMetaData_: Optional[Dict[str, Any]]
    initCount_: int
    listTables_: Any
    metadataCachedFails: list
    metadataDev: Callable
    queryGroup: Callable
    queryParameter: Callable

    def __init__(self, *args) -> None:
        return None

    def action(self, n: str) -> "pineboolib.fllegacy.flaction.FLAction":
        return None

    def alterTable(self, mtd1=..., mtd2=..., key=..., force=...) -> Any:
        return None

    def checkMetaData(self, mtd1, mtd2) -> Any:
        return None

    def cleanupMetaData(self) -> None:
        return None

    def createSystemTable(self, n: str) -> bool:
        return False

    def createTable(self, n_or_tmd) -> Any:
        return None

    def existsTable(self, n: str, cache: bool = False) -> bool:
        return False

    def fetchLargeValue(self, refKey: Mapping[slice, Any]) -> Optional[str]:
        return None

    def finish(self) -> None:
        return None

    def formatAssignValue(self, *args, **kwargs) -> str:
        return ""

    def formatAssignValueLike(self, *args, **kwargs) -> str:
        return ""

    def formatValue(self, fMD_or_type: str, v: Optional[Union[int, str]], upper: bool = False) -> str:
        return ""

    def formatValueLike(self, *args, **kwargs) -> Any:
        return None

    def init(self) -> None:
        return None

    def initCount(self) -> int:
        return 0

    def isSystemTable(self, n: str) -> bool:
        return False

    def loadTables(self) -> None:
        return None

    def metadata(self, n, quick: bool = False) -> Optional["pineboolib.fllegacy.fltablemetadata.FLTableMetaData"]:
        return None

    def metadataField(self, field, v: bool = False, ed: bool = False) -> "pineboolib.fllegacy.flfieldmetadata.FLFieldMetaData":
        return None

    def metadataRelation(self, relation) -> "pineboolib.fllegacy.flrelationmetadata.FLRelationMetaData":
        return None

    def query(self, n, parent=...) -> Optional["pineboolib.fllegacy.flsqlquery.FLSqlQuery"]:
        return None

    def storeLargeValue(self, mtd, largeValue: Mapping[slice, Any]) -> Optional[str]:
        return None
