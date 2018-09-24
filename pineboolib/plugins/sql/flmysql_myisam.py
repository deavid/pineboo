import sys
from pineboolib.fllegacy.FLUtil import FLUtil
from pineboolib.utils import text2bool
from pineboolib.fllegacy.FLSqlQuery import FLSqlQuery
from pineboolib.utils import auto_qt_translate_text
import traceback
from PyQt5.Qt import qWarning, QApplication


class FLMYSQL_MYISAM(object):

    version_ = None
    conn_ = None
    name_ = None
    alias_ = None
    errorList = None
    lastError_ = None
    cursorsArray_ = None
    noInnoDB = None
    mobile_ = False
    pure_python_ = False
    defaultPort_ = None

    def __init__(self):
        self.version_ = "0.4"
        self.conn_ = None
        self.name_ = "FLMYSQL_MyISAM"
        self.open_ = False
        self.errorList = []
        self.alias_ = "MySQL_MyISAM (EN OBRAS)"
        self.cursorsArray_ = {}
        self.noInnoDB = True
        self._dbname = None
        self.mobile_ = False
        self.pure_python_ = False
        self.defaultPort_ = 3306

    def version(self):
        return self.version_

    def driverName(self):
        return self.name_

    def pure_python(self):
        return self.pure_python_

    def mobile(self):
        return self.mobile_

    def isOpen(self):
        return self.open_

    def DBName(self):
        return self._dbname

    def connect(self, db_name, db_host, db_port, db_userName, db_password):
        self._dbname = db_name

        try:
            import MySQLdb
        except ImportError:
            print(traceback.format_exc())
            print("HINT: Instale el paquete python3-mysqldb e intente de nuevo")
            sys.exit(0)

        self.conn_ = MySQLdb.connect(
            db_host, db_userName, db_password, db_name)

        if self.conn_:
            self.open_ = True
            self.conn_.autocommit(True)

        return self.conn_

    def formatValueLike(self, type_, v, upper):
        res = "IS NULL"

        if type_ == "bool":
            s = str(v[0]).upper()
            if s == str(QApplication.tr("Sí")[0]).upper():
                res = "=1"
            elif str(QApplication.tr("No")[0]).upper():
                res = "=0"

        elif type_ == "date":
            util = FLUtil()
            res = "LIKE '%%" + util.dateDMAtoAMD(str(v)) + "'"

        elif type_ == "time":
            t = v.toTime()
            res = "LIKE '" + t.toString(QtCore.Qt.ISODate) + "%%'"

        else:
            res = str(v)
            if upper:
                res = "%s" % res.upper()

            res = "LIKE '" + res + "%%'"

        return res

    def formatValue(self, type_, v, upper):

        util = FLUtil()

        s = None

        if v is None:
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
            if upper and type_ == "string":
                v = v.upper()

            s = "'%s'" % v
        # print ("PNSqlDriver(%s).formatValue(%s, %s) = %s" % (self.name_, type_, v, s))
        return s

    def canOverPartition(self):
        return True

    def nextSerialVal(self, table, field):
        """
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
        """
        if not self.isOpen():
            qWarning("%s::beginTransaction: Database not open" % self.name_)
            return None

        if not self.noInnoDB and self.transaction():
            self.setLastError(
                "No se puede iniciar la transacción", "BEGIN WORK")
            return None

        res = None
        row = None
        max = 0
        curMax = 0
        updateQry = False

        strQry = "SELECT MAX(%s) FROM %s" % (field, table)
        cursor = self.conn_.cursor()

        try:
            result = cursor.execute(strQry)
        except Exception:
            qWarning("%s:: No se pudo crear la transacción BEGIN\n %s" %
                     (self.name_, traceback.format_exc()))
            self.rollbackTransaction()
            return

        for max_ in result:
            res = max_

        if res:
            row = cursor._fetch_row(res)
            if row:
                max = int(row[0])

        strQry = "SELECT seq FROM flseqs WHERE tabla = '%s' AND campo ='%s'" % (
            table, field)
        try:
            result = cursor.execute(strQry)
        except Exception:
            qWarning("%s:: La consulta a la base de datos ha fallado" %
                     (self.name_, traceback.format_exc()))
            self.rollbackTransaction()
            return

        for curMax_ in result:
            res = curMax_

        if res:
            updateQry = (len(res) > 0)
            if updateQry:
                row = cursor._fetch_row(res)
                if row:
                    curMax = int(row[0])

        strQry = None
        if updateQry:
            if max > curMax:
                strQry = "UPDATE flseq SET seq=%s WHERE tabla = '%s' AND campo = '%s'" % (
                    max + 1, table, field)
        else:
            strQry = "INSERT INTO flseq (tabla, campo, seq) VALUES('%s','%s',%s)" % (
                table, field, max + 1)

        if strQry:
            try:
                result = cursor.execute(strQry)
            except Exception:
                qWarning("%s:: La consulta a la base de datos ha fallado" %
                         (self.name_, traceback.format_exc()))
                if not self.noInnoDB:
                    self.rollbackTransaction()

                return

        strQry = "UPDATE flseq SET seq= LAST INSERT_ID(seq+1) WHERE tabla = '%s' and campo = '%s'" % (
            table, field)
        try:
            result = cursor.execute(strQry)
        except Exception:
            qWarning("%s:: La consulta a la base de datos ha fallado" %
                     (self.name_, traceback.format_exc()))
            if not self.noInnoDB:
                self.rollbackTransaction()

            return

        strQry = "SELECT LAST_INSERT_ID()"
        try:
            result = cursor.execute(strQry)
        except Exception:
            qWarning("%s:: La consulta a la base de datos ha fallado" %
                     (self.name_, traceback.format_exc()))
            if not self.noInnoDB:
                self.rollbackTransaction()

            return

        for r in result:
            res = r

        if res:
            row = cursor._fetch_row(res)
            if row:
                ret = int(row[0])

        if not self.noInnoDB and self.commitTransaction():
            qWarning("%s:: No se puede aceptar la transacción" % self.name_)
            return

        return ret

    def savePoint(self, n):
        if not self.isOpen():
            qWarning("%s::savePoint: Database not open" % self.name_)
            return False

        cursor = self.conn_.cursor()
        try:
            cursor.execute("SAVEPOINT sv_%s" % n)
        except Exception:
            self.setLastError(
                "No se pudo crear punto de salvaguarda", "SAVEPOINT sv_%s" % n)
            qWarning("MySQLDriver:: No se pudo crear punto de salvaguarda SAVEPOINT sv_%s \n %s " % (
                n, traceback.format_exc()))
            return False

        return True

    def canSavePoint(self):
        return True

    def rollbackSavePoint(self, n):
        if not self.isOpen():
            qWarning("%s::rollbackSavePoint: Database not open" % self.name_)
            return False

        cursor = self.conn_.cursor()
        try:
            cursor.execute("ROLLBACK TO SAVEPOINT sv_%s" % n)
        except Exception:
            self.setLastError(
                "No se pudo rollback a punto de salvaguarda", "ROLLBACK TO SAVEPOINTt sv_%s" % n)
            qWarning("%s:: No se pudo rollback a punto de salvaguarda ROLLBACK TO SAVEPOINT sv_%s\n %s" % (
                self.name_, n, traceback.format_exc()))
            return False

        return True

    def setLastError(self, text, command):
        self.lastError_ = "%s (%s)" % (text, command)

    def lastError(self):
        return self.lastError_

    def commitTransaction(self):
        if not self.isOpen():
            qWarning("%s::commitTransaction: Database not open" % self.name_)

        cursor = self.conn_.cursor()
        try:
            cursor.execute("COMMIT TRANSACTION")
        except Exception:
            self.setLastError("No se pudo aceptar la transacción", "COMMIT")
            qWarning("%s:: No se pudo aceptar la transacción COMMIT\n %s" %
                     (self.name_, traceback.format_exc()))
            return False

        return True

    def rollbackTransaction(self):
        if not self.isOpen():
            qWarning("%s::rollbackTransaction: Database not open" % self.name_)

        cursor = self.conn_.cursor()
        try:
            cursor.execute("ROLLBACK TRANSACTION")
        except Exception:
            self.setLastError("No se pudo deshacer la transacción", "ROLLBACK")
            qWarning("%s:: No se pudo deshacer la transacción ROLLBACK\n %s" % (
                self.name_, traceback.format_exc()))
            return False

        return True

    def transaction(self):
        if not self.isOpen():
            qWarning("%s::transaction: Database not open" % self.name_)

        cursor = self.conn_.cursor()
        try:
            cursor.execute("START TRANSACTION")
        except Exception:
            self.setLastError("No se pudo crear la transacción", "BEGIN WORK")
            qWarning("%s:: No se pudo crear la transacción BEGIN\n %s" %
                     (self.name_, traceback.format_exc()))
            return False

        return True

    def releaseSavePoint(self, n):

        if not self.isOpen():
            qWarning("%s::releaseSavePoint: Database not open" % self.name_)
            return False

        cursor = self.conn_.cursor()
        try:
            cursor.execute("RELEASE SAVEPOINT sv_%s" % n)
        except Exception:
            self.setLastError(
                "No se pudo release a punto de salvaguarda", "RELEASE SAVEPOINT sv_%s" % n)
            qWarning("MySQLDriver:: No se pudo release a punto de salvaguarda RELEASE SAVEPOINT sv_%s\n %s" % (
                n, traceback.format_exc()))

            return False

        return True

    def setType(self, type_, leng=None):
        if leng:
            return "::%s(%s)" % (type_, leng)
        else:
            return "::%s" % type_

    def refreshQuery(self, curname, fields, table, where, cursor, conn):
        if curname not in self.cursorsArray_.keys():
            self.cursorsArray_[curname] = cursor

        sql = "SELECT %s FROM %s WHERE %s " % (fields, table, where)
        try:
            self.cursorsArray_[curname].execute(sql)
        except Exception:
            qWarning("CursorTableModel.Refresh\n %s" % traceback.format_exc())

    def refreshFetch(self, number, curname, table, cursor, fields, where_filter):
        try:
            self.cursorsArray_[curname].fetchmany(number)
        except Exception:
            qWarning("%s.refreshFetch\n %s" %
                     (self.name_, traceback.format_exc()))

    def useThreads(self):
        return True

    def useTimer(self):
        return False

    def fetchAll(self, cursor, tablename, where_filter, fields, curname):
        return list(self.cursorsArray_[curname])

    def existsTable(self, name):
        if not self.isOpen():
            return False

        t = FLSqlQuery()
        t.setForwardOnly(True)
        ok = t.exec_(
            "select relname from pg_class where relname = '%s'" % name)
        if ok:
            ok = t.next()

        del t
        return ok

    def sqlCreateTable(self, tmd):
        # util = FLUtil()
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
            qWarning(u"FLManager : No se ha podido crear la tabla " + tmd.name())
            qWarning(
                u"FLManager : Hay mas de un campo tipo unlock. Solo puede haber uno.")
            return None

        i = 1
        for field in fieldList:
            sql = sql + field.name()
            if field.type() == "int":
                sql = sql + " INT2"
            elif field.type() == "uint":
                sql = sql + " INT4"
            elif field.type() in ("bool", "unlock"):
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
                if primaryKey is None:
                    sql = sql + " PRIMARY KEY"
                else:
                    qWarning(QApplication.tr("FLManager : Tabla-> ") + tmd.name() +
                             QApplication.tr(" . Se ha intentado poner una segunda clave primaria para el campo ") +
                             field.name() + QApplication.tr(" , pero el campo ") + primaryKey +
                             QApplication.tr(" ya es clave primaria. Sólo puede existir una clave primaria en FLTableMetaData,"
                                             " use FLCompoundKey para crear claves compuestas."))
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

    def cascadeSupport(self):
        return True

    def canDetectLocks(self):
        return True

    def desktopFile(self):
        return False

    def execute_query(self, q):

        if not self.isOpen():
            qWarning("MySQLDriver::execute_query. DB is closed")
            return False

        cursor = self.conn_.cursor()
        try:
            cursor.execute(q)
        except Exception:
            self.setLastError(
                "No se puedo ejecutar la siguiente query %s" % q)
            qWarning("MySQLDriver:: No se puedo ejecutar la siguiente query %s % q\n %s" % (
                q, traceback.format_exc()))
