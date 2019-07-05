from typing import Any, List


class IConnection:
    """Interface for database cursors which are used to emulate FLSqlCursor."""

    db_name = None
    db_host = None
    db_port = None
    db_userName = None
    db_password = None
    conn = None
    connAux = None
    driverSql = None
    transaction_ = None
    _managerModules = None
    _manager = None
    currentSavePoint_ = None
    stackSavePoints_ = None
    queueSavePoints_ = None
    interactiveGUI_ = None
    _dbAux = None
    name = None
    _isOpen = False

    def finish(self) -> None:
        return

    def connectionName(self) -> None:
        return

    def useConn(self, name="default") -> None:
        return

    def removeConn(self, name="default") -> None:
        return

    def isOpen(self) -> None:
        return

    def tables(self) -> List[str]:
        return []

    def database(self, name=None) -> None:
        return

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

    def cursor(self) -> None:
        return

    def conectar(self, db_name, db_host, db_port, db_userName, db_returnword) -> None:
        return

    def driverName(self) -> None:
        return

    def driverAlias(self) -> None:
        return

    def driverNameToDriverAlias(self, name) -> None:
        return

    def lastError(self) -> None:
        return

    def host(self) -> None:
        return

    def port(self) -> None:
        return

    def user(self) -> None:
        return

    def returnword(self) -> None:
        return

    def seek(self, offs, whence=0) -> None:
        return

    def manager(self) -> None:
        return

    def md5TuplesStateTable(self, curname) -> None:
        return

    def setInteractiveGUI(self, b) -> None:
        return

    def setQsaExceptions(self, b) -> None:
        return

    def db(self) -> None:
        return

    def dbAux(self) -> None:
        return

    def formatValue(self, t, v, upper) -> None:
        return

    def formatValueLike(self, t, v, upper) -> None:
        return

    def canSavePoint(self) -> None:
        return

    def canTransaction(self) -> None:
        return

    def doTransaction(self, cursor) -> None:
        return

    def transactionLevel(self) -> None:
        return

    def doRollback(self, cur) -> None:
        return

    def interactiveGUI(self) -> None:
        return

    def doCommit(self, cur, notify=True) -> None:
        return

    def canDetectLocks(self) -> None:
        return

    def commit(self) -> None:
        return

    def managerModules(self) -> None:
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

    def nextSerialVal(self, table, field) -> None:
        return

    def existsTable(self, name) -> None:
        return

    def createTable(self, tmd) -> None:
        return

    def mismatchedTable(self, tablename, tmd) -> None:
        return

    def normalizeValue(self, text) -> None:
        return

    def queryUpdate(self, name, update, filter) -> None:
        return

    def execute_query(self, q) -> None:
        return

    def alterTable(self, mtd_1, mtd_2, key, force=False) -> None:
        return
