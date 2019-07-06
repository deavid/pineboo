from PyQt5.Qt import QDomDocument, QDateTime, QProgressDialog, QDate, QRegExp, QApplication  # type: ignore
from PyQt5.QtCore import QTime, Qt  # type: ignore
from pineboolib.core.utils.utils_base import auto_qt_translate_text
from pineboolib.application.utils.check_dependencies import check_dependencies

from pineboolib.fllegacy.flsqlquery import FLSqlQuery
from pineboolib.fllegacy.flsqlcursor import FLSqlCursor
from pineboolib.fllegacy.flutil import FLUtil

from sqlalchemy import create_engine

import traceback
import os
from pineboolib import logging


class FLSQLITE(object):

    version_ = None
    conn_ = None
    name_ = None
    cursor_ = None
    alias_ = None
    errorList = None
    lastError_ = None
    declare = None
    db_filename = None
    sql = None
    rowsFetched = None
    db_ = None
    mobile_ = True
    pure_python_ = False
    # True por defecto, convierte los datos de entrada y salida a UTF-8 desde
    # Latin1
    parseFromLatin = None
    defaultPort_ = None
    engine_ = None
    session_ = None
    declarative_base_ = None

    def __init__(self):
        self.logger = logging.getLogger("FLSqLite")
        self.version_ = "0.6"
        self.conn_ = None
        self.name_ = "FLsqlite"
        self.open_ = False
        self.errorList = []
        self.alias_ = "SQLite3 (SQLITE3)"
        self.declare = []
        self.db_filename = None
        self.sql = None
        self.rowsFetched = {}
        self.db_ = None
        self.parseFromLatin = False
        self.mobile_ = True
        self.pure_python_ = False
        self.defaultPort_ = 0
        self.cursor_ = None
        self.engine_ = None
        self.session_ = None
        self.declarative_base_ = None

    def pure_python(self):
        return self.pure_python_

    def mobile(self):
        return self.mobile_

    def version(self):
        return self.version_

    def driverName(self):
        return self.name_

    def safe_load(self):
        return check_dependencies({"sqlite3": "sqlite3", "sqlalchemy": "sqlAlchemy"}, False)

    def isOpen(self):
        return self.open_

    def cursor(self):
        if not self.cursor_:
            self.cursor_ = self.conn_.cursor()
            # self.cursor_.execute("PRAGMA journal_mode = WAL")
            # self.cursor_.execute("PRAGMA synchronous = NORMAL")
        return self.cursor_

    def useThreads(self):
        return False

    def useTimer(self):
        return True

    def cascadeSupport(self):
        return False

    def canDetectLocks(self):
        return True

    def desktopFile(self):
        return True

    def connect(self, db_name, db_host, db_port, db_userName, db_password):
        import pineboolib

        check_dependencies({"sqlite3": "sqlite3", "sqlalchemy": "sqlAlchemy"})
        self.db_filename = db_name
        db_is_new = not os.path.exists("%s" % self.db_filename)

        import sqlite3

        if self.db_filename == getattr(pineboolib.project.conn, "db_name", None):
            self.conn_ = pineboolib.project.conn.conn
        else:
            self.conn_ = sqlite3.connect("%s" % self.db_filename)
            self.engine_ = create_engine("sqlite:///%s" % self.db_filename)
            self.conn_.isolation_level = None

            if db_is_new:
                self.logger.warning("La base de datos %s no existe", self.db_filename)

        if self.conn_:
            self.open_ = True

        if self.parseFromLatin:
            self.conn_.text_factory = lambda x: str(x, "latin1")

        return self.conn_

    def engine(self):
        return self.engine_

    def session(self):
        if self.session_ is None:
            from sqlalchemy.orm import sessionmaker

            # from sqlalchemy import event
            # from pineboolib.pnobjectsfactory import before_commit, after_commit
            Session = sessionmaker(bind=self.engine())
            self.session_ = Session()
            # event.listen(Session, 'before_commit', before_commit, self.session_)
            # event.listen(Session, 'after_commit', after_commit, self.session_)

    def declarative_base(self):
        if self.declarative_base_ is None:
            from sqlalchemy.ext.declarative import declarative_base

            self.declarative_base_ = declarative_base()

        return self.declarative_base_

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
            res = "LIKE '" + t.toString(Qt.ISODate) + "%%'"

        else:
            res = str(v)
            if upper:
                res = "%s" % res.upper()

            res = "LIKE '" + res + "%%'"

        return res

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
                if v:
                    s = 1
                else:
                    s = 0

        elif type_ == "date":
            s = "'%s'" % util.dateDMAtoAMD(v)

        elif type_ == "time":
            if v:
                s = "'%s'" % v
            else:
                s = ""

        elif type_ in ("uint", "int", "double", "serial"):
            if v is None:
                s = 0
            else:
                s = v

        else:
            if type_ == "string":
                v = auto_qt_translate_text(v)
            if upper and type_ == "string":
                v = v.upper()
                # v = v.encode("UTF-8")
            s = "'%s'" % v
        return s

    def DBName(self):
        return self.db_filename[self.db_filename.rfind("/") + 1 : -8]

    def canOverPartition(self):
        return True

    def nextSerialVal(self, table, field):
        q = FLSqlQuery()
        q.setSelect("max(%s)" % field)
        q.setFrom(table)
        q.setWhere("1 = 1")
        if not q.exec_():  # FIXME: exec es palabra reservada
            self.logger.warning("not exec sequence")
            return None
        if q.first() and q.value(0) is not None:
            return int(q.value(0)) + 1
        else:
            return None

    def savePoint(self, n):
        if n == 0:
            return True

        if not self.isOpen():
            self.logger.warning("%s::savePoint: Database not open", __name__)
            return False

        cursor = self.cursor()
        try:
            self.logger.debug("Creando savepoint sv_%s" % n)
            cursor.execute("SAVEPOINT sv_%s" % n)
        except Exception:
            self.setLastError("No se pudo crear punto de salvaguarda", "SAVEPOINT sv_%s" % n)
            self.logger.error("%s:: No se pudo crear punto de salvaguarda SAVEPOINT sv_%s", __name__, n)
            return False

        return True

    def canSavePoint(self):
        return True

    def canTransaction(self):
        return True

    def rollbackSavePoint(self, n):
        if n == 0:
            return True

        if not self.isOpen():
            self.logger.warning("%s::rollbackSavePoint: Database not open", __name__)
            return False

        cursor = self.cursor()
        try:
            cursor.execute("ROLLBACK TRANSACTION TO SAVEPOINT sv_%s" % n)
        except Exception:
            self.setLastError("No se pudo rollback a punto de salvaguarda", "ROLLBACK TO SAVEPOINTt sv_%s" % n)
            self.logger.error("%s:: No se pudo rollback a punto de salvaguarda ROLLBACK TO SAVEPOINT sv_%s", __name__, n)
            return False

        return True

    def setLastError(self, text, command):
        self.lastError_ = "%s (%s)" % (text, command)

    def lastError(self):
        return self.lastError_

    def commitTransaction(self):
        if not self.isOpen():
            self.logger.warning("%s::commitTransaction: Database not open", __name__)

        cursor = self.cursor()
        try:
            cursor.execute("END TRANSACTION")
        except Exception:
            self.setLastError("No se pudo aceptar la transacción", "COMMIT")
            self.logger.error("%s:: No se pudo aceptar la transacción COMMIT. %s", __name__, traceback.format_exc())
            return False

        return True

    def inTransaction(self):
        return self.conn_.in_transaction

    def fix_query(self, query):
        # ret_ = query.replace(";", "")
        return query

    def execute_query(self, q):
        if not self.isOpen():
            self.logger.warning("%s::execute_query: Database not open", __name__)

        cursor = self.cursor()
        try:
            q = self.fix_query(q)
            cursor.execute(q)
        except Exception:
            self.logger.error("SQL3Driver:: No se pudo ejecutar la query %s" % q, q)
            self.setLastError("%s::No se pudo ejecutar la query.\n%s" % (__name__, q), q)

        return cursor

    def rollbackTransaction(self):
        if not self.isOpen():
            self.logger.warning("SQL3Driver::rollbackTransaction: Database not open")

        cursor = self.cursor()
        try:
            cursor.execute("ROLLBACK TRANSACTION")
        except Exception:
            self.setLastError("No se pudo deshacer la transacción", "ROLLBACK")
            self.logger.error("SQL3Driver:: No se pudo deshacer la transacción ROLLBACK")
            return False

        return True

    def transaction(self):
        if not self.isOpen():
            self.logger.warning("SQL3Driver::transaction: Database not open")
        cursor = self.cursor()
        try:
            cursor.execute("BEGIN TRANSACTION")
        except Exception:
            self.setLastError("No se pudo crear la transacción", "BEGIN")
            self.logger.error("SQL3Driver:: No se pudo crear la transacción BEGIN")
            return False

        return True

    def releaseSavePoint(self, n):
        if n == 0:
            return True
        if not self.isOpen():
            self.logger.debug("SQL3Driver::releaseSavePoint: Database not open")
            return False

        cursor = self.cursor()
        try:
            cursor.execute("RELEASE SAVEPOINT sv_%s" % n)
        except Exception:
            self.setLastError("No se pudo release a punto de salvaguarda", "RELEASE SAVEPOINT sv_%s" % n)
            self.logger.error("SQL3Driver:: No se pudo release a punto de salvaguarda RELEASE SAVEPOINT sv_%s", n)
            return False

        return True

    def setType(self, type_, leng=None):
        return " %s(%s)" % (type_.upper(), leng) if leng else " %s" % type_.upper()

    def refreshQuery(self, curname, fields, table, where, cursor, conn):
        where = self.process_booleans(where)
        self.sql = "SELECT %s FROM %s WHERE %s" % (fields, table, where)

    def refreshFetch(self, number, curname, table, cursor, fields, where):
        try:
            cursor.execute(self.sql)
            rows = cursor.fetchmany(number)
            return rows
        except Exception:
            self.logger.error("SQL3Driver:: refreshFetch")

    def process_booleans(self, where):
        where = where.replace("'true'", str(1))
        return where.replace("'false'", str(0))

    def fetchAll(self, cursor, tablename, where_filter, fields, curname):
        if curname not in self.rowsFetched.keys():
            self.rowsFetched[curname] = 0

        rowsF = []
        try:
            cursor.execute(self.sql)
            rows = cursor.fetchall()
            if self.rowsFetched[curname] < len(rows):
                i = 0
                for row in rows:
                    i += 1
                    if i > self.rowsFetched[curname]:
                        rowsF.append(row)

                self.rowsFetched[curname] = i

        except Exception:
            self.logger.error("SQL3Driver:: fetchAll", traceback.format_exc())

        return rowsF

    def existsTable(self, name):
        if not self.isOpen():
            return False

        t = FLSqlQuery()
        t.setForwardOnly(True)
        ok = t.exec_("SELECT name FROM sqlite_master WHERE type='table' AND name='%s'" % name)
        if ok:
            ok = t.next()

        return ok

    def sqlCreateTable(self, tmd):
        if not tmd:
            return None

        primaryKey = None
        sql = "CREATE TABLE %s (" % tmd.name()

        fieldList = tmd.fieldList()

        unlocks = 0
        for field in fieldList:
            if field.type() == "unlock":
                unlocks = unlocks + 1

        if unlocks > 1:
            self.logger.debug(u"FLManager : No se ha podido crear la tabla " + tmd.name())
            self.loger.debug(u"FLManager : Hay mas de un campo tipo unlock. Solo puede haber uno.")
            return None

        i = 1
        for field in fieldList:
            sql = sql + field.name()
            if field.type() == "int":
                sql = sql + " INTEGER"
            elif field.type() == "uint":
                sql = sql + " INTEGER"
            elif field.type() in ("bool", "unlock"):
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
                if primaryKey is None:
                    sql = sql + " PRIMARY KEY"
                else:
                    self.logger.debug(
                        QApplication.tr("FLManager : Tabla-> ")
                        + tmd.name()
                        + QApplication.tr(" . Se ha intentado poner una segunda clave primaria para el campo ")
                        + field.name()
                        + QApplication.tr(" , pero el campo ")
                        + primaryKey
                        + QApplication.tr(
                            " ya es clave primaria. Sólo puede existir una clave primaria en FLTableMetaData, "
                            "use FLCompoundKey para crear claves compuestas."
                        )
                    )
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

        sql = sql + ");"

        createIndex = "CREATE INDEX %s_pkey ON %s (%s)" % (tmd.name(), tmd.name(), tmd.primaryKey())

        # q = FLSqlQuery()
        # q.setForwardOnly(True)
        # q.exec_(createIndex)
        sql += createIndex

        return sql

    def mismatchedTable(self, table1, tmd_or_table2, db_=None):
        if db_ is None:
            db_ = self.db_

        if isinstance(tmd_or_table2, str):
            mtd = db_.manager().metadata(tmd_or_table2, True)
            if not mtd:
                return False

            mismatch = False
            processed_fields = []
            try:
                recMtd = self.recordInfo(tmd_or_table2)
                recBd = self.recordInfo2(table1)
                # fieldBd = None
                for fieldMtd in recMtd:
                    # fieldBd = None
                    found = False
                    for field in recBd:
                        if field[0] == fieldMtd[0]:
                            processed_fields.append(field[0])
                            found = True
                            if self.notEqualsFields(field, fieldMtd):
                                mismatch = True

                            recBd.remove(field)
                            break

                    if not found:
                        if fieldMtd[0] not in processed_fields:
                            mismatch = True
                            break

                if len(recBd) > 0:
                    mismatch = True

            except Exception:
                print(traceback.format_exc())

            return mismatch

        else:
            return self.mismatchedTable(table1, tmd_or_table2.name(), db_)

    def notEqualsFields(self, field1, field2):
        ret = False
        try:
            if not field1[2] == field2[2] and not field2[6]:
                ret = True

            if field1[1] == "stringlist" and not field2[1] in ("stringlist", "pixmap"):
                ret = True

            elif field1[1] == "string" and (not field2[1] in ("string", "time", "date") or not field1[3] == field2[3]):
                if field2[1] in ("time", "date") and field1[3] == 20:
                    ret = False
                else:
                    ret = True

            elif field1[1] == "uint" and not field2[1] in ("int", "uint", "serial"):
                ret = True
            elif field1[1] == "bool" and not field2[1] in ("bool", "unlock"):
                ret = True
            elif field1[1] == "double" and not field2[1] == "double":
                ret = True

        except Exception:
            self.logger.error("notEqualsFields %s %s", field1, field2)
        return ret

    def recordInfo2(self, tablename):
        if not self.isOpen():
            return None

        sql = "PRAGMA table_info('%s')" % tablename
        conn = self.conn_
        cursor = conn.execute(sql)
        res = cursor.fetchall()
        return self.recordInfo(res)

    def recordInfo(self, tablename_or_query):
        if not self.isOpen():
            return None

        info = []

        if isinstance(tablename_or_query, str):
            tablename = tablename_or_query

            doc = QDomDocument(tablename)
            stream = self.db_.managerModules().contentCached("%s.mtd" % tablename)
            util = FLUtil()
            if not util.domDocumentSetContent(doc, stream):
                self.logger.warning("FLManager : " + QApplication.tr("Error al cargar los metadatos para la tabla %1").arg(tablename))

                return self.recordInfo2(tablename)

            docElem = doc.documentElement()
            mtd = self.db_.manager().metadata(docElem, True)
            if not mtd:
                return self.recordInfo2(tablename)
            fL = mtd.fieldList()
            if not fL:
                del mtd
                return self.recordInfo2(tablename)

            for f in mtd.fieldNames():
                field = mtd.field(f)
                info.append(
                    [
                        field.name(),
                        field.type(),
                        not field.allowNull(),
                        field.length(),
                        field.partDecimal(),
                        field.defaultValue(),
                        field.isPrimaryKey(),
                    ]
                )

            del mtd
            return info

        else:
            for columns in tablename_or_query:
                fName = columns[1]
                fType = columns[2]
                fSize = 0
                fAllowNull = columns[3] == 0
                if fType.find("VARCHAR(") > -1:
                    fSize = int(fType[fType.find("(") + 1 : len(fType) - 1])

                info.append([fName, self.decodeSqlType(fType), not fAllowNull, fSize])

            return info

    def decodeSqlType(self, type):
        ret = None
        if type == "BOOLEAN":  # y unlock
            ret = "bool"
        elif type == "FLOAT":
            ret = "double"
        elif type.find("VARCHAR") > -1:  # Aqui también puede ser time y date
            ret = "string"
        elif type == "TEXT":  # Aquí también puede ser pixmap
            ret = "stringlist"
        elif type == "INTEGER":  # serial
            ret = "uint"

        return ret

    def alterTable(self, mtd1, mtd2, key, force=False):
        util = FLUtil()

        oldMTD = None
        newMTD = None
        doc = QDomDocument("doc")
        docElem = None

        if not util.domDocumentSetContent(doc, mtd1):
            self.logger.warning("FLManager::alterTable : " + util.tr("Error al cargar los metadatos."))
        else:
            docElem = doc.documentElement()
            oldMTD = self.db_.manager().metadata(docElem, True)

        if oldMTD and oldMTD.isQuery():
            return True

        if not util.domDocumentSetContent(doc, mtd2):
            self.logger.warning("FLManager::alterTable : " + util.tr("Error al cargar los metadatos."))
            return False
        else:
            docElem = doc.documentElement()
            newMTD = self.db_.manager().metadata(docElem, True)

        if not oldMTD:
            oldMTD = newMTD

        if not oldMTD.name() == newMTD.name():
            self.logger.warning("FLManager::alterTable : " + util.tr("Los nombres de las tablas nueva y vieja difieren."))
            if oldMTD and not oldMTD == newMTD:
                del oldMTD
            if newMTD:
                del newMTD

            return False

        oldPK = oldMTD.primaryKey()
        newPK = newMTD.primaryKey()

        if not oldPK == newPK:
            self.logger.warning("FLManager::alterTable : " + util.tr("Los nombres de las claves primarias difieren."))
            if oldMTD and not oldMTD == newMTD:
                del oldMTD
            if newMTD:
                del newMTD

            return False

        if not self.db_.manager().checkMetaData(oldMTD, newMTD):
            if oldMTD and not oldMTD == newMTD:
                del oldMTD
            if newMTD:
                del newMTD

            return True

        if not self.db_.manager().existsTable(oldMTD.name()):
            self.logger.warning(
                "FLManager::alterTable : " + util.tr("La tabla %1 antigua de donde importar los registros no existe.").arg(oldMTD.name())
            )
            if oldMTD and not oldMTD == newMTD:
                del oldMTD
            if newMTD:
                del newMTD

            return False

        fieldList = oldMTD.fieldList()
        oldField = None

        if not fieldList:
            self.logger.warning("FLManager::alterTable : " + util.tr("Los antiguos metadatos no tienen campos."))
            if oldMTD and not oldMTD == newMTD:
                del oldMTD
            if newMTD:
                del newMTD

            return False

        renameOld = "%salteredtable%s" % (oldMTD.name()[0:5], QDateTime().currentDateTime().toString("ddhhssz"))

        if not self.db_.dbAux():
            if oldMTD and not oldMTD == newMTD:
                del oldMTD
            if newMTD:
                del newMTD

            return False

        self.db_.dbAux().transaction()

        if key and len(key) == 40:
            c = FLSqlCursor("flfiles", True, self.db_.dbAux())
            c.setForwardOnly(True)
            c.setFilter("nombre = '%s.mtd'" % renameOld)
            c.select()
            if not c.next():
                buffer = c.primeInsert()
                buffer.setValue("nombre", "%s.mtd" % renameOld)
                buffer.setValue("contenido", mtd1)
                buffer.setValue("sha", key)
                c.insert()

        q = FLSqlQuery("", self.db_.dbAux())
        if not q.exec_("CREATE TABLE %s AS SELECT * FROM %s;" % (renameOld, oldMTD.name())) or not q.exec_(
            "DROP TABLE %s;" % oldMTD.name()
        ):
            self.logger.warning("FLManager::alterTable : " + util.tr("No se ha podido renombrar la tabla antigua."))

            self.db_.dbAux().rollback()
            if oldMTD and not oldMTD == newMTD:
                del oldMTD
            if newMTD:
                del newMTD

            return False

        if not self.db_.manager().createTable(newMTD):
            self.db_.dbAux().rollback()
            if oldMTD and not oldMTD == newMTD:
                del oldMTD
            if newMTD:
                del newMTD

            return False

        oldCursor = FLSqlCursor(renameOld, True, self.db_.dbAux())
        oldCursor.setModeAccess(oldCursor.Browse)
        newCursor = FLSqlCursor(newMTD.name(), True, self.db_.dbAux())
        newCursor.setMode(newCursor.Insert)

        oldCursor.select()
        totalSteps = oldCursor.size()
        progress = QProgressDialog(util.tr("Reestructurando registros para %s..." % newMTD.alias()), util.tr("Cancelar"), 0, totalSteps)
        progress.setLabelText(util.tr("Tabla modificada"))

        step = 0
        newBuffer = None
        # sequence = ""
        fieldList = newMTD.fieldList()
        newField = None

        if not fieldList:
            self.logger.warning("FLManager::alterTable : " + util.tr("Los nuevos metadatos no tienen campos."))
            self.db_.dbAux().rollback()
            if oldMTD and not oldMTD == newMTD:
                del oldMTD
            if newMTD:
                del newMTD

            return False

        v = None
        ok = True
        while oldCursor.next():
            v = None
            newBuffer = newCursor.primeInsert()

            for it in fieldList:
                oldField = oldMTD.field(newField.name())
                if not oldField or not oldCursor.field(oldField.name()):
                    if not oldField:
                        oldField = newField

                    v = newField.defaultValue()

                else:
                    v = oldCursor.value(newField.name())
                    if (not oldField.allowNull() or not newField.allowNull()) and (v is None):
                        defVal = newField.defaultValue()
                        if defVal is not None:
                            v = defVal

                    if not newBuffer.field(newField.name()).type() == newField.type():
                        self.logger.warning(
                            "FLManager::alterTable : "
                            + util.tr("Los tipos del campo %s no son compatibles. Se introducirá un valor nulo." % newField.name())
                        )

                if not oldField.allowNull() or not newField.allowNull() and v is not None:
                    if oldField.type() in ("int", "serial", "uint", "bool", "unlock"):
                        v = 0
                    elif oldField.type() == "double":
                        v = 0.0
                    elif oldField.type() == "time":
                        v = QTime().currentTime()
                    elif oldField.type() == "date":
                        v = QDate().currentDate()
                    else:
                        v = "NULL"[0 : newField.length()]

                newBuffer.setValue(newField.name(), v)

            if not newCursor.insert():
                ok = False
                break
            step = step + 1
            progress.setProgress(step)

        progress.setProgress(totalSteps)
        if oldMTD and not oldMTD == newMTD:
            del oldMTD
        if newMTD:
            del newMTD

        if ok:
            self.db_.dbAux().commit()
        else:
            self.db_.dbAux().rollback()
            return False

        return True

    def tables(self, typeName=None):
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
        return None if text is None else str(text).replace("'", "''")

    def queryUpdate(self, name, update, filter):
        sql = "UPDATE %s SET %s WHERE %s" % (name, update, filter)
        return sql

    def Mr_Proper(self):
        self.logger.warning("FLSQLITE: FIXME: Mr_Proper no regenera tablas")
        util = FLUtil()
        self.db_.dbAux().transaction()
        rx = QRegExp("^.*[\\d][\\d][\\d][\\d].[\\d][\\d].*[\\d][\\d]$")
        rx2 = QRegExp("^.*alteredtable[\\d][\\d][\\d][\\d].*$")
        qry = FLSqlQuery(None, "dbAux")
        qry2 = FLSqlQuery(None, "dbAux")
        qry3 = FLSqlQuery(None, "dbAux")
        steps = 0
        item = ""

        rx3 = QRegExp("^.*\\d{6,9}$")
        # listOldBks = self.tables("").grep(rx3)
        listOldBks_prev = self.tables("")

        listOldBks = []

        for l in listOldBks_prev:
            if rx3.indexIn(l) > -1:
                listOldBks.append(l)

        qry.exec_("select nombre from flfiles")
        util.createProgressDialog(util.tr("Borrando backups"), len(listOldBks) + qry.size() + 5)
        while qry.next():
            item = qry.value(0)
            if rx.indexIn(item) > -1 or rx2.indexIn(item) > -1:
                util.setLabelText(util.tr("Borrando regisro %s" % item))
                qry2.exec_("delete from flfiles where nombre = '%s'" % item)
                if item.find("alteredtable") > -1:
                    if item.replace(".mtd", "") in self.tables(""):
                        util.setLabelText(util.tr("Borrando tabla %s" % item))
                        qry2.exec_("drop table %s" % item.replace(".mtd", ""))

            steps = steps + 1
            util.setProgress(steps)

        for item in listOldBks:
            if item in self.tables(""):
                util.tr("Borrando tabla %s" % item)
                util.setLabelText(util.tr("Borrando tabla %s" % item))
                qry2.exec_("drop table %s" % item)

            steps = steps + 1
            util.setProgress(steps)

        util.setLabelText(util.tr("Inicializando cachés"))
        steps = steps + 1
        util.setProgress(steps)

        qry.exec_("delete from flmetadata")
        qry.exec_("delete from flvar")
        self.db_.manager().cleanupMetaData()
        self.db_.dbAux().commit()

        util.setLabelText(util.tr("Vacunando base de datos"))
        steps = steps + 1
        util.setProgress(steps)
        qry3.exec_("vacuum")
        steps = steps + 1
        util.setProgress(steps)
        util.destroyProgressDialog()
