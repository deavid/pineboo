import sys
from PyQt5.QtCore import QTime
from pineboolib.flcontrols import ProjectClass
from pineboolib import decorators 
from pineboolib.dbschema.schemaupdater import text2bool
from pineboolib.fllegacy import FLUtil
from pineboolib.fllegacy.FLSqlQuery import FLSqlQuery
from pineboolib.utils import auto_qt_translate_text
import traceback





class FLQPSQL(object):
    
    version_ = None
    conn_ = None
    name_ = None
    alias_ = None
    errorList = None
    lastError_ = None
    
    def __init__(self):
        self.version_ = "0.3"
        self.conn_ = None
        self.name_ = "FLQPSQL"
        self.open_ = False
        self.errorList = []
        self.alias_ = "PostgreSQL"
    
    def version(self):
        return self.version_
    
    def driverName(self):
        return self.name_
    
    def isOpen(self):
        return self.open_
    
    def connect(self, db_name, db_host, db_port, db_userName, db_password):
        
        try:
            import psycopg2
        except ImportError:
            print(traceback.format_exc())
            print("HINT: Instale el paquete python3-psycopg2 e intente de nuevo")
            sys.exit(0)
        
        conninfostr = "dbname=%s host=%s port=%s user=%s password=%s connect_timeout=5" % (
                        db_name, db_host, db_port,
                        db_userName, db_password)
        
        
        
        self.conn_ = psycopg2.connect(conninfostr)
        #self.conn_.autocommit = True #Posiblemente tengamos que ponerlo a false para que las transacciones funcionen
        self.conn_.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        
        if self.conn_:
            self.open_ = True
        
        try:
            self.conn_.set_client_encoding("UTF8")
        except Exception:
            print(traceback.format_exc())
        
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
                s = "'%s'" % v

            elif type_ == "uint" or type_ == "int" or type_ == "double" or type_ == "serial":
                s = v

            else:
                v = auto_qt_translate_text(v)
                if upper == True and type_ == "string":
                    v = v.upper()

                s = "'%s'" % v
            #print ("PNSqlDriver(%s).formatValue(%s, %s) = %s" % (self.name_, type_, v, s))
            return s

    def canOverPartition(self):
        return True
    
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
    
    def savePoint(self, n):
        if not self.isOpen():
            print("PSQLDriver::savePoint: Database not open")
            return False
        
        cursor = self.conn_.cursor()
        try:
            cursor.execute("SAVEPOINT sv_%s" % n)
        except Exception:
            self.setLastError("No se pudo crear punto de salvaguarda", "SAVEPOINT sv_%s" % n)
            print("PSQLDriver:: No se pudo crear punto de salvaguarda SAVEPOINT sv_%s" % n, traceback.format_exc())
            return False
        
        return True 
    
    def canSavePoint(self):
        return True
    
    def rollbackSavePoint(self, n):
        if not self.isOpen():
            print("PSQLDriver::rollbackSavePoint: Database not open")
            return False
        

        cursor = self.conn_.cursor()
        try:
            cursor.execute("ROLLBACK TO SAVEPOINT sv_%s" % n)
        except Exception:
            self.setLastError("No se pudo rollback a punto de salvaguarda", "ROLLBACK TO SAVEPOINTt sv_%s" % n)
            print("PSQLDriver:: No se pudo rollback a punto de salvaguarda ROLLBACK TO SAVEPOINT sv_%s" % n, traceback.format_exc())
            return False
        
        return True
    
    def setLastError(self, text, command):
        self.lastError_ = "%s (%s)" % (text, command)
    
    def lastError(self):
        return self.lastError_
    
    
    def commitTransaction(self):
        if not self.isOpen():
            print("PSQLDriver::commitTransaction: Database not open")
        
        try:
            self.conn_.commit()
        except Exception:
            self.setLastError("No se pudo aceptar la transacción", "COMMIT")
            print("PSQLDriver:: No se pudo aceptar la transacción COMMIT",  traceback.format_exc())
            return False
        
        return True
    
    def rollbackTransaction(self):
        if not self.isOpen():
            print("PSQLDriver::rollbackTransaction: Database not open")
        
        
        try:
            self.conn_.rollback()
        except Exception:
            self.setLastError("No se pudo deshacer la transacción", "ROLLBACK")
            print("PSQLDriver:: No se pudo deshacer la transacción ROLLBACK",  traceback.format_exc())
            return False
        
        return True
    

    def transaction(self):
        if not self.isOpen():
            print("PSQLDriver::transaction: Database not open")
        
        cursor = self.conn_.cursor()
        try:
            cursor.execute("BEGIN")
        except Exception:
            self.setLastError("No se pudo crear la transacción", "BEGIN")
            print("PSQLDriver:: No se pudo crear la transacción BEGIN",  traceback.format_exc())
            return False
        
        return True
    
    def releaseSavePoint(self, n):
        
        if not self.isOpen():
            print("PSQLDriver::releaseSavePoint: Database not open")
            return False
        
        cursor = self.conn_.cursor()
        try:
            cursor.execute("RELEASE SAVEPOINT sv_%s" % n)
        except Exception:
            self.setLastError("No se pudo release a punto de salvaguarda", "RELEASE SAVEPOINT sv_%s" % n)
            print("PSQLDriver:: No se pudo release a punto de salvaguarda RELEASE SAVEPOINT sv_%s" % n,  traceback.format_exc())
        
            return False
        
        return True 
    
            
    def setType(self, type_, leng = None):
        if leng:
            return "::%s(%s)" % (type_, leng)
        else:
            return "::%s" % type_
    
    
    def refreshQuery(self, declare, fields, table, where):
        return "DECLARE %s NO SCROLL CURSOR WITH HOLD FOR SELECT %s FROM %s WHERE %s " % (declare , fields , table, where)
    
    def refreshFetch(self, number, curname, table, cursor):
        try:
            cursor.execute("FETCH %d FROM %s" % (number, curname))
        except Exception:
            print("PSQLDriver.refreshFetch", traceback.format_exc())
    
    def useThreads(self):
        return True
    
    def useTimer(self):
        return False        
            
            
        