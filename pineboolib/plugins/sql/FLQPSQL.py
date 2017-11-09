import sys
from PyQt5.QtCore import QTime
from pineboolib import decorators 
from pineboolib.dbschema.schemaupdater import text2bool
from pineboolib.fllegacy.FLUtil import FLUtil
from pineboolib.fllegacy.FLSqlQuery import FLSqlQuery
from pineboolib.utils import auto_qt_translate_text
import traceback
from PyQt5.Qt import qWarning, QApplication
from PyQt5.QtWidgets import QMessageBox





class FLQPSQL(object):
    
    version_ = None
    conn_ = None
    name_ = None
    alias_ = None
    errorList = None
    lastError_ = None
    
    def __init__(self):
        self.version_ = "0.4"
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
            qWarning(traceback.format_exc())
            qWarning("HINT: Instale el paquete python3-psycopg2 e intente de nuevo")
            sys.exit(0)
        
        conninfostr = "dbname=%s host=%s port=%s user=%s password=%s connect_timeout=5" % (
                        db_name, db_host, db_port,
                        db_userName, db_password)
        
        
        try:
            self.conn_ = psycopg2.connect(conninfostr)
        except psycopg2.OperationalError as e:
            
            if "does not exist" in str(e):
                if QMessageBox.No == QMessageBox.warning(None, "Pineboo", "La base de datos %s no existe.\n¿Desea crearla?" % db_name, QMessageBox.Ok | QMessageBox.No):
                    return False
                else:
                    conninfostr2 = "dbname=postgres host=%s port=%s user=%s password=%s connect_timeout=5" % (
                        db_host, db_port,
                        db_userName, db_password)
                    try:
                        tmpConn = psycopg2.connect(conninfostr2)
                        tmpConn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
                        
                        cursor = tmpConn.cursor()
                        cursor.execute("CREATE DATABASE %s" % db_name)
                        cursor.close()
                        return self.connect(db_name, db_host, db_port, db_userName, db_password)
                    except Exception:
                        qWarning(traceback.format_exc())
                        QMessageBox.information(None, "Pineboo", "ERROR: No se ha podido crear la Base de Datos %s" % db_name, QMessageBox.Ok)
                        print("ERROR: No se ha podido crear la Base de Datos %s" % db_name)
                        return False
            else:
                QMessageBox.information(None, "Pineboo", "Error de conexión\n%s" % str(e), QMessageBox.Ok)
                return False
                    
            
        #self.conn_.autocommit = True #Posiblemente tengamos que ponerlo a false para que las transacciones funcionen
        self.conn_.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        
        if self.conn_:
            self.open_ = True
        
        try:
            self.conn_.set_client_encoding("UTF8")
        except Exception:
            qWarning(traceback.format_exc())
        
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
            #qWarning ("PNSqlDriver(%s).formatValue(%s, %s) = %s" % (self.name_, type_, v, s))
            return s

    def canOverPartition(self):
        return True
    
    def nextSerialVal(self, table, field):
        q = FLSqlQuery()
        q.setSelect(u"nextval('" + table + "_" + field + "_seq')")
        q.setFrom("")
        q.setWhere("")
        if not q.exec_():
            qWarning("not exec sequence")
            return None
        if q.first():
            return q.value(0)
        else:
            return None
    
    def savePoint(self, n):
        if not self.isOpen():
            qWarning("PSQLDriver::savePoint: Database not open")
            return False
        
        cursor = self.conn_.cursor()
        try:
            cursor.execute("SAVEPOINT sv_%s" % n)
        except Exception:
            self.setLastError("No se pudo crear punto de salvaguarda", "SAVEPOINT sv_%s" % n)
            qWarning("PSQLDriver:: No se pudo crear punto de salvaguarda SAVEPOINT sv_%s" % n, traceback.format_exc())
            return False
        
        return True 
    
    def canSavePoint(self):
        return True
    
    def rollbackSavePoint(self, n):
        if not self.isOpen():
            qWarning("PSQLDriver::rollbackSavePoint: Database not open")
            return False
        

        cursor = self.conn_.cursor()
        try:
            cursor.execute("ROLLBACK TO SAVEPOINT sv_%s" % n)
        except Exception:
            self.setLastError("No se pudo rollback a punto de salvaguarda", "ROLLBACK TO SAVEPOINTt sv_%s" % n)
            qWarning("PSQLDriver:: No se pudo rollback a punto de salvaguarda ROLLBACK TO SAVEPOINT sv_%s" % n, traceback.format_exc())
            return False
        
        return True
    
    def setLastError(self, text, command):
        self.lastError_ = "%s (%s)" % (text, command)
    
    def lastError(self):
        return self.lastError_
    
    
    def commitTransaction(self):
        if not self.isOpen():
            qWarning("PSQLDriver::commitTransaction: Database not open")
        
        cursor = self.conn_.cursor()
        try:
            cursor.execute("COMMIT TRANSACTION")
        except Exception:
            self.setLastError("No se pudo aceptar la transacción", "COMMIT")
            qWarning("PSQLDriver:: No se pudo aceptar la transacción COMMIT",  traceback.format_exc())
            return False
        
        return True
    
    def rollbackTransaction(self):
        if not self.isOpen():
            qWarning("PSQLDriver::rollbackTransaction: Database not open")
        
        
        cursor = self.conn_.cursor()
        try:
            cursor.execute("ROLLBACK TRANSACTION")
        except Exception:
            self.setLastError("No se pudo deshacer la transacción", "ROLLBACK")
            qWarning("PSQLDriver:: No se pudo deshacer la transacción ROLLBACK",  traceback.format_exc())
            return False
        
        return True
    

    def transaction(self):
        if not self.isOpen():
            qWarning("PSQLDriver::transaction: Database not open")
        
        cursor = self.conn_.cursor()
        try:
            cursor.execute("BEGIN TRANSACTION")
        except Exception:
            self.setLastError("No se pudo crear la transacción", "BEGIN")
            qWarning("PSQLDriver:: No se pudo crear la transacción BEGIN",  traceback.format_exc())
            return False
        
        return True
    
    def releaseSavePoint(self, n):
        
        if not self.isOpen():
            qWarning("PSQLDriver::releaseSavePoint: Database not open")
            return False
        
        cursor = self.conn_.cursor()
        try:
            cursor.execute("RELEASE SAVEPOINT sv_%s" % n)
        except Exception:
            self.setLastError("No se pudo release a punto de salvaguarda", "RELEASE SAVEPOINT sv_%s" % n)
            qWarning("PSQLDriver:: No se pudo release a punto de salvaguarda RELEASE SAVEPOINT sv_%s" % n,  traceback.format_exc())
        
            return False
        
        return True 
    
            
    def setType(self, type_, leng = None):
        if leng:
            return "::%s(%s)" % (type_, leng)
        else:
            return "::%s" % type_
    
    
    def refreshQuery(self, curname, fields, table, where, cursor, conn):
        sql = "DECLARE %s NO SCROLL CURSOR WITH HOLD FOR SELECT %s FROM %s WHERE %s " % (curname , fields , table, where)
        try:
            cursor.execute(sql)
        except Exception:
            qWarning("CursorTableModel.Refresh", traceback.format_exc())
    
    def refreshFetch(self, number, curname, table, cursor, fields, where_filter):
        try:
            cursor.execute("FETCH %d FROM %s" % (number, curname))
        except Exception:
            qWarning("PSQLDriver.refreshFetch", traceback.format_exc())
    
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
                
        
        
        