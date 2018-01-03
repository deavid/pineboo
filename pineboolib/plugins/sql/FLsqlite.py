import os, sys
from PyQt5.QtCore import QTime
from pineboolib.flcontrols import ProjectClass
from pineboolib import decorators 
from pineboolib.dbschema.schemaupdater import text2bool
from pineboolib.fllegacy import FLUtil
from pineboolib.fllegacy.FLSqlQuery import FLSqlQuery
from pineboolib.utils import auto_qt_translate_text
from pineboolib.fllegacy.FLUtil import FLUtil
import traceback





class FLsqlite(object):
    
    version_ = None
    conn_ = None
    name_ = None
    alias_ = None
    errorList = None
    lastError_ = None
    declare = None
    db_filename = None
    sql = None
    rowsFetched = None
    
    def __init__(self):
        self.version_ = "0.5"
        self.conn_ = None
        self.name_ = "FLsqlite"
        self.open_ = False
        self.errorList = []
        self.alias_ = "SQLite3"
        self.declare = []
        self.db_filename = None
        self.sql = None
        self.rowsFetched = {}
    
    def version(self):
        return self.version_
    
    def driverName(self):
        return self.name_
    
    def isOpen(self):
        return self.open_
    
    def connect(self, db_name, db_host, db_port, db_userName, db_password):
        
        db_filename = db_name
        db_is_new = not os.path.exists(db_filename)
        
        try:
            import sqlite3
        except ImportError:
            print(traceback.format_exc())
            print("HINT: Instale el paquete python3-sqlite3 e intente de nuevo")
            sys.exit(0)
            
        self.conn_ = sqlite3.connect(db_filename)
        self.conn_.isolation_level = None
        
        if db_is_new:
            print("La base de datos %s no existe" % db_filename)
        
        
        if self.conn_:
            self.open_ = True
        
        #self.conn_.text_factory = os.fsdecode
        self.conn_.text_factory = lambda x: str(x, 'latin1')
        self.db_filename = db_name
        
        return self.conn_
     
    
    
    def formatValue(self, type_, v, upper):
            
            util = FLUtil()
        
            s = None
            # TODO: psycopg2.mogrify ???
            if type_ == "pixmap" and v.find("'") > -1:
                v = self.normalizeValue(v)

            if type_ == "bool" or type_ == "unlock":
                if isinstance(v, str):
                    if v[0].lower() == "t":
                        s = 1
                    else:
                        s = 0
                elif isinstance(v, bool):
                    if v == True:
                        s = 1
                    else:
                        s = 0

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
                    #v = v.encode("UTF-8")
                s = "'%s'" % v
            #print ("PNSqlDriver(%s).formatValue(%s, %s) = %s" % (self.name_, type_, v, s))
            return s
    
    def DBName(self):
        return self.db_filename[self.db_filename.rfind("/") + 1:-5]
            


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
            print("SQL3Driver::savePoint: Database not open")
            return False
        
        cursor = self.conn_.cursor()
        try:
            cursor.execute("SAVEPOINT sv_%s" % n)
        except Exception:
            self.setLastError("No se pudo crear punto de salvaguarda", "SAVEPOINT sv_%s" % n)
            print("SQL3Driver:: No se pudo crear punto de salvaguarda SAVEPOINT sv_%s" % n, traceback.format_exc())
            return False
        
        return True 
    
    def canSavePoint(self):
        return True
    
    def rollbackSavePoint(self, n):
        if not self.isOpen():
            print("SQL3Driver::rollbackSavePoint: Database not open")
            return False
        

        cursor = self.conn_.cursor()
        try:
            cursor.execute("ROLLBACK TRANSACTION TO SAVEPOINT sv_%s" % n)
        except Exception:
            self.setLastError("No se pudo rollback a punto de salvaguarda", "ROLLBACK TO SAVEPOINTt sv_%s" % n)
            print("SQL3Driver:: No se pudo rollback a punto de salvaguarda ROLLBACK TO SAVEPOINT sv_%s" % n, traceback.format_exc())
            return False
        
        return True
    
    def setLastError(self, text, command):
        self.lastError_ = "%s (%s)" % (text, command)
    
    def lastError(self):
        return self.lastError_
    
    
    def commitTransaction(self):
        if not self.isOpen():
            print("SQL3Driver::commitTransaction: Database not open")
        
        cursor = self.conn_.cursor()
        try:
            cursor.execute("COMMIT TRANSACTION")
        except Exception:
            self.setLastError("No se pudo aceptar la transacción", "COMMIT")
            print("SQL3Driver:: No se pudo aceptar la transacción COMMIT",  traceback.format_exc())
            return False
        
        return True
    
    def rollbackTransaction(self):
        if not self.isOpen():
            print("SQL3Driver::rollbackTransaction: Database not open")
        
        cursor = self.conn_.cursor()
        try:
            cursor.execute("ROLLBACK TRANSACTION")
        except Exception:
            self.setLastError("No se pudo deshacer la transacción", "ROLLBACK")
            print("SQL3Driver:: No se pudo deshacer la transacción ROLLBACK",  traceback.format_exc())
            return False
        
        return True
    

    def transaction(self):
        if not self.isOpen():
            print("SQL3Driver::transaction: Database not open")
        
        cursor = self.conn_.cursor()
        try:
            cursor.execute("BEGIN TRANSACTION")
        except Exception:
            self.setLastError("No se pudo crear la transacción", "BEGIN")
            print("SQL3Driver:: No se pudo crear la transacción BEGIN",  traceback.format_exc())
            return False
        
        return True
    
    def releaseSavePoint(self, n):
        
        if not self.isOpen():
            print("SQL3Driver::releaseSavePoint: Database not open")
            return False
        
        cursor = self.conn_.cursor()
        try:
            cursor.execute("RELEASE SAVEPOINT sv_%s" % n)
        except Exception:
            self.setLastError("No se pudo release a punto de salvaguarda", "RELEASE SAVEPOINT sv_%s" % n)
            print("SQL3Driver:: No se pudo release a punto de salvaguarda RELEASE SAVEPOINT sv_%s" % n,  traceback.format_exc())
        
            return False
        
        return True 
    

    def setType(self, type_, leng = None):
        if leng:
            return " %s(%s)" % (type_.upper(), leng)
        else:
            return " %s" % type_.upper()             
    
    
    def refreshQuery(self, curname, fields, table, where, cursor, conn):
        self.sql = "SELECT %s FROM %s WHERE %s" % (fields , table, where)
    
    def refreshFetch(self, number, curname, table, cursor, fields, where):
        try:
            cursor.execute(self.sql)
            rows = cursor.fetchmany(number)
            return rows
        except Exception:
            print("SQL3Driver:: refreshFetch",  traceback.format_exc())
            
    def useThreads(self):
        return False
    
    def useTimer(self):
        return True
    
    def fetchAll(self, cursor, tablename, where_filter, fields, curname):
        if not curname in self.rowsFetched.keys():
            self.rowsFetched[curname] = 0
            
        try:
            cursor.execute(self.sql)
            rows = cursor.fetchall()
            rowsF = []
            if self.rowsFetched[curname] < len(rows):
                i = 0
                for row in rows:
                    i = i + 1
                    if i > self.rowsFetched[curname]:
                        rowsF.append(row)
                    
                self.rowsFetched[curname] = i
            return rowsF
        except Exception:
            print("SQL3Driver:: fetchAll",  traceback.format_exc())
            return []
            
       
            
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
                    cursor = self.conn_.cursor()
                    #self.transaction()
                    try:
                        cursor.execute("CREATE SEQUENCE %s" % seq)
                    except Exception:
                        print("FLQPSQL::sqlCreateTable:\n", traceback.format_exc())
                    #self.commitTransaction()
                    
                
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
    
    @decorators.NotImplementedWarn
    def mismatchedTable(self, table1, tmd_or_table2, db_):
        return False
        if isinstance(tmd_or_table2, str):
            mtd = db_.manager().metadata(tmd_or_table2, True)
            if not mtd:
                return False
            
            recInfoMtd = self.recordInfo(tmd_or_table2)
            recInfoBD = self.recordInfo2(table1)
            recMtd = recInfoMtd.toRecord()
            recBd = recInfoBD.toRecord()
            fieldBd = None
            mismatch = False
            
        
            for fieldMtd in recMtd:
                fieldBd = recBd.field(fieldMtd.name())
                if fieldBd:
                    if self.notEqualsFields(FieldBd, fieldMtd, recInfoBD.find(fieldMtd.name()), recInfoMtd.find(fieldMtd.name()), mtd.field(fieldMtd.name())):
                        mismatch = True
                        break
                else:
                    mismatch = True
                    break
                
            
            return mismatch    
            
            
            
        
        else:
            return self.mismatchedTable(table1, tmd_or_table2.name(), db_)
    
    def recordInfo2(self, tablename):
        if not self.isOpen():
            return False
        info = []
        stmt = "select pg_attribute.attname, pg_attribute.atttypid, pg_attribute.attnotnull, pg_attribute.attlen, pg_attribute.atttypmod, pg_attrdef.adsrc from pg_class, pg_attribute left join pg_attrdef on (pg_attrdef.adrelid = pg_attribute.attrelid and pg_attrdef.adnum = pg_attribute.attnum) where lower(pg_class.relname) = '%s' and pg_attribute.attnum > 0 and pg_attribute.attrelid = pg_class.oid and pg_attribute.attisdropped = false order by pg_attribute.attnum" % tablename.lower()
        
        query = FLSqlQuery()
        query.setForwardOnly(True)
        query.exec(stmt)
        while query.next():
            len = int(query.value(3))
            precision = int(query.value(4))
            if len == -1 and precision > -1:
                len = precision - 4
                precision = -1
            
            defVal = str(query.value(5))
            if defVal and defVal[0] == "'":
                defVal = defVal[1:len(defVal) - 2]
                info.append([str(query.value(0)), query.value(1), query.value(2), len , precision, defVal, int(query.value(1))])
                 
        
    
    
        return info
    
    
    def tables(self, typeName = None):
        tl = []
        if not self.isOpen():
            return tl
        
        t = FLSqlQuery()
        t.setForwardOnly(True)
        
        if not typeName or typeName == "Tables":
            t.exec_("select relname from pg_class where ( relkind = 'r' ) AND ( relname !~ '^Inv' ) AND relname !~ '^pg_' ) ")
            while t.next():
                tl.append(str(t.value(0)))
        
        if not typeName or typeName == "Views":
            t.exec_("select relname from pg_class where ( relkind = 'v' ) AND ( relname !~ '^Inv' ) AND relname !~ '^pg_' ) ")
            while t.next():
                tl.append(str(t.value(0)))
        if not typeName or typeName == "SystemTables":
            t.exec_("select relname from pg_class where ( relkind = 'r' ) AND relname like 'pg_%' ) ")
            while t.next():
                tl.append(str(t.value(0)))
        
        
        del t
        return tl
    
    def normalizeValue(self, text):
        if text == None:
            return ""
        
        ret = ""
        for c in text:
            if c == "'":
                c = "''"
            ret = ret + c
            
        return ret
    
    
    def queryUpdate(self, name, update, filter):
        return "UPDATE %s SET %s WHERE %s" % (name, update, filter)
        
        