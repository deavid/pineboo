from pineboolib.plugins.sql.flmysql_myisam import FLMYSQL_MYISAM


class FLMYSQL_INNODB(FLMYSQL_MYISAM):

    conn_ = None
    errorList = None

    def __init__(self):
        super(FLMYSQL_INNODB, self).__init__()
        self.name_ = "FLMYSQL_INNODB"
        self.alias_ = "MySQL INNODB (MYSQLDB)"
        self.noInnoDB = False

    def canSavePoint(self):
        return True

    def canTransaction(self):
        return True
