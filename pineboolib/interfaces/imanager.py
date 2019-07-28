from typing import Any, Callable, Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from pineboolib.application.database import pnsqlquery  # noqa: F401
#     import pineboolib.application.database.pnconnection
#     import pineboolib.application.metadata.pnfieldmetadata
#     import pineboolib.application.metadata.pntablemetadata
#     import pineboolib.application.metadata.pnrelationmetadata
#     import pineboolib.fllegacy.flaction


class IManager(object):
    __doc__: str
    buffer_: None
    cacheAction_: Optional[Dict[str, Any]]  # "pineboolib.fllegacy.flaction.FLAction"
    cacheMetaDataSys_: Optional[dict]
    cacheMetaData_: Optional[dict]
    db_: Optional[Any]  # "pineboolib.application.database.pnconnection.PNConnection"
    dictKeyMetaData_: Optional[Dict[str, Any]]
    initCount_: int
    listTables_: Any
    metadataCachedFails: list
    metadataDev: Callable
    queryGroup: Callable
    queryParameter: Callable

    def __init__(self, *args) -> None:
        return None

    def action(self, n: str) -> Any:  # "pineboolib.fllegacy.flaction.FLAction"
        raise Exception("must be implemented")

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

    def fetchLargeValue(self, refKey: str) -> Optional[str]:
        return None

    def finish(self) -> None:
        return None

    def formatAssignValue(self, *args, **kwargs) -> str:
        return ""

    def formatAssignValueLike(self, *args, **kwargs) -> str:
        return ""

    def formatValue(self, fMD_or_type: str, v: Any, upper: bool = False) -> str:
        return ""

    def formatValueLike(self, *args, **kwargs) -> str:
        return ""

    def init(self) -> None:
        return None

    def initCount(self) -> int:
        return 0

    def isSystemTable(self, n: str) -> bool:
        return False

    def loadTables(self) -> None:
        return None

    def metadata(self, n, quick: bool = False) -> Optional[Any]:  # PNTableMetaData"
        return None

    def metadataField(self, field, v: bool = False, ed: bool = False) -> Any:  # "PNFieldMetaData"
        raise Exception("must be implemented")

    def metadataRelation(self, relation) -> Any:  # "PNRelationMetaData"
        raise Exception("must be implemented")

    def query(self, n, parent=...) -> Optional["pnsqlquery.PNSqlQuery"]:  # "PNSqlQuery"
        return None

    def storeLargeValue(self, mtd, largeValue: str) -> Optional[str]:
        return None
