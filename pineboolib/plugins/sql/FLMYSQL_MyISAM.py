import sys
from PyQt5.QtCore import QTime
from pineboolib.flcontrols import ProjectClass
from pineboolib import decorators 
from pineboolib.dbschema.schemaupdater import text2bool
from pineboolib.fllegacy.FLUtil import FLUtil
from pineboolib.fllegacy.FLSqlQuery import FLSqlQuery
from pineboolib.utils import auto_qt_translate_text
import traceback
from PyQt5.Qt import qWarning, QApplication
from PyQt5.QtWidgets import QMessageBox





class FLMYSQL_MyISAM(object):
    
    version_ = None
    conn_ = None
    name_ = None
    alias_ = None
    errorList = None
    lastError_ = None
    
    def __init__(self):
        self.version_ = "0.2"
        self.conn_ = None
        self.name_ = "FLMYSQL_MyISAM"
        self.open_ = False
        self.errorList = []
        self.alias_ = "MySQL_MyISAM (EN OBRAS)"
    
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
            
            util = FLUtil()
        
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
        if not q.exec_():
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
        if not q.exec_():
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
        if not q.exec_():
            self.setLastError("No se pudo release a punto de salvaguarda", "release savepoint sv_%s" % n)
            return False
        
        return True 
    
            
    def setType(self, type_, leng = None):
        if leng:
            return "::%s(%s)" % (type_, leng)
        else:
            return "::%s" % type_  

    def useThreads(self):
        return True
    
    def useTimer(self):
        return False      
    
    def fetchAll(self, cursor, tablename, where_filter, fields, curname):
        return cursor.fetchall()    

    def existsTable(self, name):
        if not self.isOpen():
            return False
        
        t = FLSqlQuery()
        t.setForwardOnly(True)
        ok = t.exec_("select relname from pg_class where relname = '%s'" % name)
        if ok:
            ok = t.next()
        
        del t
        return ok  
    
    def sqlCreateTable(self, tmd):
        util = FLUtil()
        if not tmd:
            return None
        
        primaryKey = None
        sql = "CREATE TABLE %s (" % tmd.name()
        seq = None
        
        fieldList = tmd.fieldList()
        
        unlocks = 0
        for field in fieldList:
            if field.type() == "unlock":
                unlocks = unlocks + 1
        
        if unlocks > 1:
            qWarning(u"FLManager : No se ha podido crear la tabla " +  tmd.name())
            qWarning(u"FLManager : Hay mas de un campo tipo unlock. Solo puede haber uno.")
            return None
        
        i = 1
        for field in fieldList:
            sql = sql + field.name()
            if field.type() == "int":
                sql = sql + " INT2"
            elif field.type() == "uint":
                sql = sql + " INT4"
            elif field.type() in ("bool","unlock"):
                sql = sql + " BOOLEAN"
            elif field.type() == "double":
                sql = sql + " FLOAT8"
            elif field.type() == "time":
                sql = sql + " TIME"
            elif field.type() == "date":
                sql = sql + " DATE"
            elif field.type() == "pixmap":
                sql = sql + " TEXT"
            elif field.type() == "string":
                sql = sql + " VARCHAR"
            elif field.type() == "stringlist":
                sql = sql + " TEXT"
            elif field.type() == "bytearray":
                sql = sql + " BYTEA"
            elif field.type() == "serial":
                seq = "%s_%s_seq" % (tmd.name(), field.name())
                q = FLSqlQuery()
                q.setForwardOnly(True)
                q.exec_("SELECT relname FROM pg_class WHERE relname='%s'" % seq)
                if not q.next():
                    q.exec_("CREATE SEQUENCE %s" % seq)
                
                sql = sql + " INT4 DEFAULT NEXTVAL('%s')" % seq
                del q
        
            longitud = field.length()
            if longitud > 0:
                sql = sql + "(%s)" % longitud
            
            if field.isPrimaryKey():
                if primaryKey == None:
                    sql = sql + " PRIMARY KEY"
                else:
                    qWarning(QApplication.tr("FLManager : Tabla-> ") + tmd.name() +
                             QApplication.tr(" . Se ha intentado poner una segunda clave primaria para el campo ") +
                             field.name() + QApplication.tr(" , pero el campo ") + primaryKey +
                             QApplication.tr(" ya es clave primaria. Sólo puede existir una clave primaria en FLTableMetaData, use FLCompoundKey para crear claves compuestas."))
                    return None
            else:
                if field.isUnique():
                    sql = sql + " UNIQUE"
                if not field.allowNull():
                    sql = sql + " NOT NULL"
                else:
                    sql = sql + " NULL"
                
            if not i == len(fieldList):
                sql = sql + ","
                i = i + 1
        
        sql = sql + ")"
        
        return sql
    
    def mismatchedTable(self, table1, tmd_or_table2, db_):
        if isinstance(tmd_or_table2, str):
            mtd = db_.manager().metadata(tmd_or_table2, True)
            if not mtd:
                return False
            
            return False
            
            
            
            
        
        else:
            return self.mismatchedTable(table1, tmd_or_table2.name(), db_)
            

            
        
