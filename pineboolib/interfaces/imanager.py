"""
IManager Module.
"""
from typing import Any, Callable, Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from pineboolib.application.database import pnsqlquery  # noqa: F401
#     import pineboolib.application.database.pnconnection
#     import pineboolib.application.metadata.pnfieldmetadata
#     import pineboolib.application.metadata.pntablemetadata
#     import pineboolib.application.metadata.pnrelationmetadata
#     import pineboolib.fllegacy.flaction


class IManager(object):
    """
    Abstract class for FLManager.
    """

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
        """Create manager."""
        return None

    def action(self, n: str) -> Any:  # "pineboolib.fllegacy.flaction.FLAction"
        """Retrieve action object by name."""
        raise Exception("must be implemented")

    def alterTable(self, mtd1=..., mtd2=..., key=..., force=...) -> Any:
        """Issue an alter table to db."""
        return None

    def checkMetaData(self, mtd1, mtd2) -> Any:
        """Validate MTD against DB."""
        return None

    def cleanupMetaData(self) -> None:
        """Clean up MTD."""
        return None

    def createSystemTable(self, n: str) -> bool:
        """Create named system table."""
        return False

    def createTable(self, n_or_tmd) -> Any:
        """Create new table."""
        return None

    def existsTable(self, n: str, cache: bool = False) -> bool:
        """Check if table does exist in db."""
        return False

    def fetchLargeValue(self, refKey: str) -> Optional[str]:
        """Fetch from fllarge."""
        return None

    def finish(self) -> None:
        """Finish?."""
        return None

    def formatAssignValue(self, *args, **kwargs) -> str:
        """Format value for DB update."""
        return ""

    def formatAssignValueLike(self, *args, **kwargs) -> str:
        """Format value for DB "LIKE" statement."""
        return ""

    def formatValue(self, fMD_or_type: str, v: Any, upper: bool = False) -> str:
        """Format value for DB."""
        return ""

    def formatValueLike(self, *args, **kwargs) -> str:
        """Format value for DB LIKE."""
        return ""

    def init(self) -> None:
        """Initialize this object."""
        return None

    def initCount(self) -> int:
        """Track number of inits."""
        return 0

    def isSystemTable(self, n: str) -> bool:
        """Return if given name is a system table."""
        return False

    def loadTables(self) -> None:
        """Load tables."""
        return None

    def metadata(self, n, quick: bool = False) -> Optional[Any]:  # PNTableMetaData"
        """Retrieve table metadata by table name."""
        return None

    def metadataField(self, field, v: bool = False, ed: bool = False) -> Any:  # "PNFieldMetaData"
        """Retrieve field metadata."""
        raise Exception("must be implemented")

    def metadataRelation(self, relation) -> Any:  # "PNRelationMetaData"
        """Retrieve relationship."""
        raise Exception("must be implemented")

    def query(self, n, parent=...) -> Optional["pnsqlquery.PNSqlQuery"]:  # "PNSqlQuery"
        """Create query."""
        return None

    def storeLargeValue(self, mtd, largeValue: str) -> Optional[str]:
        """Store value in fllarge."""
        return None
