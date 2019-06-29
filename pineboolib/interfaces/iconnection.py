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

    def finish(self):
        pass

    def connectionName(self):
        pass

    def useConn(self, name="default"):
        pass

    def removeConn(self, name="default"):
        pass

    def isOpen(self):
        pass

    def tables(self):
        pass

    def database(self, name=None):
        pass

    def DBName(self):
        pass

    def driver(self):
        pass

    def session(self):
        pass

    def engine(self):
        pass

    def declarative_base(self):
        pass

    def cursor(self):
        pass

    def conectar(self, db_name, db_host, db_port, db_userName, db_password):
        pass

    def driverName(self):
        pass

    def driverAlias(self):
        pass

    def driverNameToDriverAlias(self, name):
        pass

    def lastError(self):
        pass

    def host(self):
        pass

    def port(self):
        pass

    def user(self):
        pass

    def password(self):
        pass

    def seek(self, offs, whence=0):
        pass

    def manager(self):
        pass

    def md5TuplesStateTable(self, curname):
        pass

    def setInteractiveGUI(self, b):
        pass

    def setQsaExceptions(self, b):
        pass

    def db(self):
        pass

    def dbAux(self):
        pass

    def formatValue(self, t, v, upper):
        pass

    def formatValueLike(self, t, v, upper):
        pass

    def canSavePoint(self):
        pass

    def canTransaction(self):
        pass

    def doTransaction(self, cursor):
        pass

    def transactionLevel(self):
        pass

    def doRollback(self, cur):
        pass

    def interactiveGUI(self):
        pass

    def doCommit(self, cur, notify=True):
        pass

    def canDetectLocks(self):
        pass

    def commit(self):
        pass

    def managerModules(self):
        pass

    def canOverPartition(self):
        pass

    def savePoint(self, savePoint):
        pass

    def releaseSavePoint(self, savePoint):
        pass

    def Mr_Proper(self):
        pass

    def rollbackSavePoint(self, savePoint):
        pass

    def transaction(self):
        pass

    def commitTransaction(self):
        pass

    def rollbackTransaction(self):
        pass

    def nextSerialVal(self, table, field):
        pass

    def existsTable(self, name):
        pass

    def createTable(self, tmd):
        pass

    def mismatchedTable(self, tablename, tmd):
        pass

    def normalizeValue(self, text):
        pass

    def queryUpdate(self, name, update, filter):
        pass

    def execute_query(self, q):
        pass

    def alterTable(self, mtd_1, mtd_2, key, force=False):
        pass
