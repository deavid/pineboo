import sys
from PyQt5.QtCore import QTime
from pineboolib.flcontrols import ProjectClass
from pineboolib import decorators 
from pineboolib.dbschema.schemaupdater import text2bool
from pineboolib.fllegacy import FLUtil
from pineboolib.fllegacy.FLSqlQuery import FLSqlQuery



class FLMYSQL_NO_INNODB(object):
    
    version_ = None
    conn_ = None
    name_ = None
    alias_ = None
    errorList = None
    lastError_ = None
    
    def __init__(self):
        self.version_ = "0.2"
        self.conn_ = None
        self.name_ = "FLMYSQL"
        self.open_ = False
        self.errorList = []
        self.alias_ = "MySQL"
    
    def version(self):
        return self.version_
    
    def driverName(self):
        return self.name_
    
    def isOpen(self):
        return self.open_
    
    def connect(self, db_name, db_host, db_port, db_userName, db_password):
        
        try:
            import MySQLdb
        except ImportError:
            print(traceback.format_exc())
            print("HINT: Instale el paquete python3-mysqldb e intente de nuevo")
            sys.exit(0)
        
        self.conn_ = MySQLdb.connect(db_host, db_userName, db_password, db_name)
        
        if self.conn_:
            self.open_ = True

        
        return self.conn_
     
    
    
    def formatValue(self, type_, v, upper):
            
            util = FLUtil.FLUtil()
        
            s = None
            
            if v == None:
                v = ""
            # TODO: psycopg2.mogrify ???

            if type_ == "bool" or type_ == "unlock":
                s = text2bool(v)

            elif type_ == "date":
                s = "'%s'" % util.dateDMAtoAMD(v)
                
            elif type_ == "time":
                time = QTime(s)
                s = "'%s'" % time

            elif type_ == "uint" or type_ == "int" or type_ == "double" or type_ == "serial":
                s = v

            else:
                if upper == True and type_ == "string":
                    v = v.upper()

                s = "'%s'" % v
            #print ("PNSqlDriver(%s).formatValue(%s, %s) = %s" % (self.name_, type_, v, s))
            return s

    def canOverPartition(self):
        return True
    
    @decorators.BetaImplementation
    def hasFeature(self, value):
        
        if value == "Transactions":
            return  True
        
        
        
        if getattr(self.conn_, value, None):
            return True
        else:
            return False
    
    
    def nextSerialVal(self, table, field):
        q = FLSqlQuery()
        q.setSelect(u"nextval('" + table + "_" + field + "_seq')")
        q.setFrom("")
        q.setWhere("")
        if not q.exec():
            print("not exec sequence")
            return None
        if q.first():
            return q.value(0)
        else:
            return None
    
    @decorators.NotImplementedWarn
    def savePoint(self, number):
        pass
    
    def canSavePoint(self):
        return True
    
    def rollbackSavePoint(self, n):
        if not self.canSavePoint():
            return False
        
        if not self.isOpen():
            print("PSQLDriver::rollbackSavePoint: Database not open")
            return False
        
        cmd = ("rollback to savepoint sv_%s" % n)

        q = FLSqlQuery()
        q.setSelect(cmd)
        q.setFrom("")
        q.setWhere("")
        if not q.exec():
            self.setLastError("No se pudo deshacer punto de salvaguarda", "rollback to savepoint sv_%s" % n)
            return False
        
        return True 
    
    def setLastError(self, text, command):
        self.lastError_ = "%s (%s)" % (text, command)
    
    def lastError(self):
        return self.lastError_
    
    
    def commitTransaction(self):
        if not self.isOpen():
            print("PSQLDriver::commitTransaction: Database not open")
        
        if not self.conn_.commit():
            self.setLastError("No se pudo aceptar la transacción", "COMMIT")
            return False
        
        return True
    
    def rollbackTransaction(self):
        if not self.isOpen():
            print("PSQLDriver::commitTransaction: Database not open")
        
        if not self.conn_.rollback():
            self.setLastError("No se pudo deshacer la transacción", "ROLLBACK")
            return False
        
        return True
    
    @decorators.BetaImplementation
    def transaction(self):
        return True
    
    def releaseSavePoint(self, n):
        if not self.canSavePoint():
            return False
        
        if not self.isOpen():
            print("PSQLDriver::releaseSavePoint: Database not open")
            return False
        
        cmd = ("release savepoint sv_%s" % n)

        q = FLSqlQuery()
        q.setSelect(cmd)
        q.setFrom("")
        q.setWhere("")
        if not q.exec():
            self.setLastError("No se pudo release a punto de salvaguarda", "release savepoint sv_%s" % n)
            return False
        
        return True 
    
            
    def setType(self, type_, leng = None):
        if leng:
            return "::%s(%s)" % (type_, leng)
        else:
            return "::%s" % type_       
            
            
        
