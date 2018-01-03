import os, sys
from PyQt5.QtCore import QTime
from pineboolib import decorators 
from pineboolib.dbschema.schemaupdater import text2bool
from pineboolib.fllegacy import FLUtil
from pineboolib.fllegacy.FLSqlQuery import FLSqlQuery
from pineboolib.utils import auto_qt_translate_text
from pineboolib.fllegacy.FLUtil import FLUtil
import traceback
from PyQt5.Qt import QDomDocument





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
    db_ = None
    
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
        q.setSelect("max(%s)" % field)
        q.setFrom(table)
        q.setWhere("1 = 1")
        if not q.exec():
            print("not exec sequence")
            return None
        if q.first():
            return int(q.value(0)) + 1
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
        ok = t.exec_("SELECT * FROM %s WHERE 1 = 1 LIMIT 1" % name)
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
                sql = sql + " INTEGER"
            elif field.type() == "uint":
                sql = sql + " INTEGER"
            elif field.type() in ("bool","unlock"):
                sql = sql + " BOOLEAN"
            elif field.type() == "double":
                sql = sql + " FLOAT"
            elif field.type() == "time":
                sql = sql + " VARCHAR(20)"
            elif field.type() == "date":
                sql = sql + " VARCHAR(20)"
            elif field.type() == "pixmap":
                sql = sql + " TEXT"
            elif field.type() == "string":
                sql = sql + " VARCHAR"
            elif field.type() == "stringlist":
                sql = sql + " TEXT"
            elif field.type() == "bytearray":
                sql = sql + " CLOB"
            elif field.type() == "serial":
                sql = sql + " INTEGER"
                if not field.isPrimaryKey():
                    sql = sql + " PRIMARY KEY"
        
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
        
        createIndex = "CREATE INDEX %s_pkey ON %s (%s)" % (tmd.name(), tmd.name(), tmd.primaryKey())
        
        q = FLSqlQuery()
        q.setForwardOnly(True)
        q.exec_(createIndex)
        
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
            return None
        
        q = FLSqlQuery()
        q.setForwardOnly(True)
        q.exec_("SELECT * FROM %s LIMIT 1" % tablename)
        return self.recordInfo(q)
    
    def recordInfo(self, tablename_or_query):
        if isinstance(tablename_or_query, str):
            tablename = tablename_or_query
            if not self.isOpen():
                return None
            info = []
            
            doc = QDomDocument(tablename)
            stream = self.db_.managerModules().contentCached("%s.mtd" % tablename)
            util = FLUtil()
            if not util.domDocumentSetContent(doc, stream):
                print("FLManager : " + qApp.tr("Error al cargar los metadatos para la tabla %1").arg(tablename))
            
                return self.recordInfo2(tablename)
            
            docElem = doc.documentElement()
            mtd = self.db_.manager().metadata(docElem, True)
            if not mtd:
                return self.recordInfo2(tablename)
            fL = mtd.fieldList()
            if not fl:
                del mtd
                return self.recordInfo2(tablename)
            
            for f in mtd.fieldsNames():
                field = mtd.field(f)
                info.append([field.name(), field.type(), not field.allowNull(), field.length(), field.partDecimal(), field.defaultValue()])
                
            
            del mtd
            return info
        
        #else:
        """
        QSqlRecordInfo SqliteDriver::recordInfo(const QSqlQuery &query) const
        {
          if (query.isActive() && query.driver() == this) {
        QSqlRecordInfo info;
        const SqliteResult *result = static_cast<const SqliteResult *>(query.result());
        Dataset *ds = result->dataSet;
    for (int i = 0; i < ds->fieldCount(); ++i) {
      QString fName(ds->fieldName(i));
      fType type = ds->fv(fName).get_fType();
      info.append(QSqlFieldInfo(fName, qDecodeSqliteType(type)));
    }
    return info;
  }
  return QSqlRecordInfo();
}
        """
            
        
            
                
            
        
    
    
    def tables(self, typeName = None):
        tl = []
        if not self.isOpen():
            return tl
        
        t = FLSqlQuery()
        t.setForwardOnly(True)
        
        if typeName == "Tables" and typeName == "Views":
            t.exec_("SELECT name FROM sqlite_master WHERE type='table' OR type='view'")
        elif not typeName or typeName == "Tables":
            t.exec_("SELECT name FROM sqlite_master WHERE type='table'")
        elif not typeName or typeName == "Views":
            t.exec_("SELECT name FROM sqlite_master WHERE type='view'")
        
        while t.next():
            tl.append(str(t.value(0)))        
        
        if not typeName or typeName == "SystemTables":
            tl.append("sqlite_master")
 

        
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
        sql = "UPDATE %s SET %s WHERE %s" % (name, update, filter)
        return sql
        
        