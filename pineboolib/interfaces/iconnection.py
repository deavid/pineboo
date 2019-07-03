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
        pass

    def connectionName(self) -> None:
        pass

    def useConn(self, name="default") -> None:
        pass

    def removeConn(self, name="default") -> None:
        pass

    def isOpen(self) -> None:
        pass

    def tables(self) -> List[str]:
        pass

    def database(self, name=None) -> None:
        pass

    def DBName(self) -> str:
        pass

    def driver(self) -> Any:
        pass

    def session(self) -> Any:
        pass

    def engine(self) -> Any:
        pass

    def declarative_base(self) -> Any:
        pass

    def cursor(self) -> None:
        pass

    def conectar(self, db_name, db_host, db_port, db_userName, db_password) -> None:
        pass

    def driverName(self) -> None:
        pass

    def driverAlias(self) -> None:
        pass

    def driverNameToDriverAlias(self, name) -> None:
        pass

    def lastError(self) -> None:
        pass

    def host(self) -> None:
        pass

    def port(self) -> None:
        pass

    def user(self) -> None:
        pass

    def password(self) -> None:
        pass

    def seek(self, offs, whence=0) -> None:
        pass

    def manager(self) -> None:
        pass

    def md5TuplesStateTable(self, curname) -> None:
        pass

    def setInteractiveGUI(self, b) -> None:
        pass

    def setQsaExceptions(self, b) -> None:
        pass

    def db(self) -> None:
        pass

    def dbAux(self) -> None:
        pass

    def formatValue(self, t, v, upper) -> None:
        pass

    def formatValueLike(self, t, v, upper) -> None:
        pass

    def canSavePoint(self) -> None:
        pass

    def canTransaction(self) -> None:
        pass

    def doTransaction(self, cursor) -> None:
        pass

    def transactionLevel(self) -> None:
        pass

    def doRollback(self, cur) -> None:
        pass

    def interactiveGUI(self) -> None:
        pass

    def doCommit(self, cur, notify=True) -> None:
        pass

    def canDetectLocks(self) -> None:
        pass

    def commit(self) -> None:
        pass

    def managerModules(self) -> None:
        pass

    def canOverPartition(self) -> None:
        pass

    def savePoint(self, savePoint) -> None:
        pass

    def releaseSavePoint(self, savePoint) -> None:
        pass

    def Mr_Proper(self) -> None:
        pass

    def rollbackSavePoint(self, savePoint) -> None:
        pass

    def transaction(self) -> None:
        pass

    def commitTransaction(self) -> None:
        pass

    def rollbackTransaction(self) -> None:
        pass

    def nextSerialVal(self, table, field) -> None:
        pass

    def existsTable(self, name) -> None:
        pass

    def createTable(self, tmd) -> None:
        pass

    def mismatchedTable(self, tablename, tmd) -> None:
        pass

    def normalizeValue(self, text) -> None:
        pass

    def queryUpdate(self, name, update, filter) -> None:
        pass

    def execute_query(self, q) -> None:
        pass

    def alterTable(self, mtd_1, mtd_2, key, force=False) -> None:
        pass
