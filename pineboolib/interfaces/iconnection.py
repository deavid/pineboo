from .imanager import IManager
from .iapicursor import IApiCursor

from typing import Any, List, Dict, Optional


class IConnection:
    """Interface for database cursors which are used to emulate FLSqlCursor."""

    db_name: str
    db_host: str
    db_port: int
    db_userName: str
    db_password: str
    conn: Any  # connection from the actual driver
    connAux: Dict[str, "IConnection"]
    driverSql = None
    transaction_: int
    _managerModules = None
    _manager = None
    currentSavePoint_: Optional[Any]  # Optional["PNSqlSavePoint"]
    stackSavePoints_: List[Any]  # List["PNSqlSavePoint"]
    queueSavePoints_: List[Any]  # List["PNSqlSavePoint"]
    interactiveGUI_: bool
    driverName_: str
    _dbAux = None
    name: str
    _isOpen: bool
    driver_ = None

    def finish(self) -> None:
        return

    def connectionName(self) -> str:
        return ""

    def useConn(self, name: str = "default") -> "IConnection":
        return self

    def removeConn(self, name="default") -> bool:
        return True

    def isOpen(self) -> bool:
        return False

    def tables(self, t_: Optional[str] = None) -> List[str]:
        return []

    def database(self, name=None) -> "IConnection":
        return self

    def DBName(self) -> str:
        return ""

    def driver(self) -> Any:
        return None

    def session(self) -> Any:
        return None

    def engine(self) -> Any:
        return None

    def declarative_base(self) -> Any:
        return None

    def dictDatabases(self) -> Dict[str, "IConnection"]:
        return {}

    def cursor(self) -> IApiCursor:
        return IApiCursor()

    def lastActiveCursor(self) -> Optional[Any]:  # returns FLSqlCuror
        return None

    def conectar(self, db_name, db_host, db_port, db_userName, db_returnword) -> None:
        return

    def driverName(self) -> str:
        return ""

    def driverAlias(self) -> str:
        return ""

    def driverNameToDriverAlias(self, name) -> str:
        return ""

    def lastError(self) -> str:
        return ""

    def host(self) -> str:
        return ""

    def port(self) -> int:
        return 0

    def user(self) -> str:
        return ""

    def returnword(self) -> None:
        return

    def seek(self, offs, whence=0) -> None:
        return

    def manager(self) -> IManager:
        return IManager()

    def md5TuplesStateTable(self, curname) -> None:
        return

    def setInteractiveGUI(self, b) -> None:
        return

    def setQsaExceptions(self, b) -> None:
        return

    def db(self) -> "IConnection":
        return self

    def dbAux(self) -> "IConnection":
        return self

    def formatValue(self, t, v, upper) -> str:
        return ""

    def formatValueLike(self, t, v, upper) -> str:
        return ""

    def canSavePoint(self) -> bool:
        return True

    def canTransaction(self) -> bool:
        return True

    def doTransaction(self, cursor) -> bool:
        return False

    def transactionLevel(self) -> int:
        return 0

    def doRollback(self, cur) -> bool:
        return False

    def interactiveGUI(self) -> bool:
        return False

    def doCommit(self, cur, notify=True) -> bool:
        return False

    def canDetectLocks(self) -> bool:
        return False

    def commit(self) -> None:
        return

    def managerModules(self) -> Any:
        return

    def canOverPartition(self) -> None:
        return

    def savePoint(self, savePoint) -> None:
        return

    def releaseSavePoint(self, savePoint) -> None:
        return

    def Mr_Proper(self) -> None:
        return

    def rollbackSavePoint(self, savePoint) -> None:
        return

    def transaction(self) -> None:
        return

    def commitTransaction(self) -> None:
        return

    def rollbackTransaction(self) -> None:
        return

    def nextSerialVal(self, table, field) -> Any:
        return

    def existsTable(self, name) -> bool:
        return False

    def createTable(self, tmd) -> bool:
        return False

    def mismatchedTable(self, tablename: str, tmd) -> bool:
        return False

    def normalizeValue(self, text: str) -> Optional[str]:
        return None

    def queryUpdate(self, name, update, filter) -> None:
        return

    def execute_query(self, q: str) -> None:
        return

    def alterTable(self, mtd_1, mtd_2, key, force=False) -> bool:
        return False
