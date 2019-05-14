from pineboolib.plugins.sql.flmysql_myisam2 import FLMYSQL_MYISAM2


class FLMYSQL_INNODB2(FLMYSQL_MYISAM2):

    version_ = None
    conn_ = None
    name_ = None
    alias_ = None
    errorList = None
    lastError_ = None

    def __init__(self):
        super(FLMYSQL_INNODB2, self).__init__()
        self.name_ = "FLMYSQL_INNODB2"
        self.alias_ = "MySQL INNODB (PyMySQL)"
        self.noInnoDB = False

    def canSavePoint(self):
        return True
    
    def canTransaction(self):
        return True