
from PyQt5.QtCore import QTime, QDate, QDateTime
from PyQt5.Qt import qWarning, QApplication, qApp, QDomDocument, QRegExp
from PyQt5.QtWidgets import QMessageBox, QProgressDialog 

from pineboolib.utils import text2bool, auto_qt_translate_text, checkDependencies

from pineboolib.fllegacy.flutil import FLUtil
from pineboolib.fllegacy.flsqlquery import FLSqlQuery
from pineboolib.fllegacy.flsqlcursor import FLSqlCursor

import traceback
import pineboolib
import sys
import logging


logger = logging.getLogger(__name__)


class FLQPSQL(object):

    version_ = None
    conn_ = None
    name_ = None
    alias_ = None
    errorList = None
    lastError_ = None
    db_ = None
    mobile_ = False
    pure_python_ = False
    defaultPort_ = None

    def __init__(self):
        self.version_ = "0.5"
        self.conn_ = None
        self.name_ = "FLQPSQL"
        self.open_ = False
        self.errorList = []
        self.alias_ = "PostgreSQL (PSYCOPG2)"
        self._dbname = None
        self.mobile_ = False
        self.pure_python_ = False
        self.defaultPort_ = 5432
    
    def useThreads(self):
        return True

    def useTimer(self):
        return False

    def version(self):
        return self.version_

    def driverName(self):
        return self.name_

    def isOpen(self):
        return self.open_

    def pure_python(self):
        return self.pure_python_

    def safe_load(self):
        return checkDependencies({"psycopg2": "python3-psycopg2"}, False)

    def mobile(self):
        return self.mobile_

    def DBName(self):
        return self._dbname

    def connect(self, db_name, db_host, db_port, db_userName, db_password):
        self._dbname = db_name
        checkDependencies({"psycopg2": "python3-psycopg2"})
        import psycopg2

        conninfostr = "dbname=%s host=%s port=%s user=%s password=%s connect_timeout=5" % (
            db_name, db_host, db_port,
            db_userName, db_password)

        try:
            self.conn_ = psycopg2.connect(conninfostr)
        except psycopg2.OperationalError as e:
            pineboolib.project._splash.hide()
            if "does not exist" in str(e) or "no existe" in str(e):
                ret = QMessageBox.warning(None, "Pineboo",
                                          "La base de datos %s no existe.\n¿Desea crearla?" % db_name,
                                          QMessageBox.Ok | QMessageBox.No)
                if ret == QMessageBox.No:
                    return False
                else:
                    conninfostr2 = "dbname=postgres host=%s port=%s user=%s password=%s connect_timeout=5" % (
                        db_host, db_port,
                        db_userName, db_password)
                    try:
                        tmpConn = psycopg2.connect(conninfostr2)
                        tmpConn.set_isolation_level(
                            psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

                        cursor = tmpConn.cursor()
                        try:
                            cursor.execute("CREATE DATABASE %s" % db_name)
                        except Exception:
                            print("ERROR: FLPSQL.connect",
                                  traceback.format_exc())
                            cursor.execute("ROLLBACK")
                            cursor.close()
                            return False
                        cursor.close()
                        return self.connect(db_name, db_host, db_port, db_userName, db_password)
                    except Exception:
                        qWarning(traceback.format_exc())
                        QMessageBox.information(
                            None, "Pineboo", "ERROR: No se ha podido crear la Base de Datos %s" % db_name, QMessageBox.Ok)
                        print(
                            "ERROR: No se ha podido crear la Base de Datos %s" % db_name)
                        return False
            else:
                QMessageBox.information(
                    None, "Pineboo", "Error de conexión\n%s" % str(e), QMessageBox.Ok)
                return False

        # self.conn_.autocommit = True #Posiblemente tengamos que ponerlo a
        # false para que las transacciones funcionen
        self.conn_.set_isolation_level(
            psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

        if self.conn_:
            self.open_ = True

        try:
            self.conn_.set_client_encoding("UTF8")
        except Exception:
            qWarning(traceback.format_exc())

        return self.conn_

    def formatValueLike(self, type_, v, upper):
        res = "IS NULL"

        if type_ == "bool":
            s = str(v[0]).upper()
            if s == str(QApplication.tr("Sí")[0]).upper():
                res = "='t'"
            elif str(QApplication.tr("No")[0]).upper():
                res = "='f'"

        elif type_ == "date":
            util = FLUtil()
            res = "::text LIKE '%%" + util.dateDMAtoAMD(str(v)) + "'"

        elif type_ == "time":
            t = v.toTime()
            res = "::text LIKE '" + t.toString(QtCore.Qt.ISODate) + "%%'"

        else:
            res = str(v)
            if upper:
                res = "%s" % res.upper()

            res = "::text LIKE '" + res + "%%'"

        return res

    def formatValue(self, type_, v, upper):

        util = FLUtil()

        s = None

        # if v == None:
        #    v = ""
        # TODO: psycopg2.mogrify ???

        if v is None:
            s = "Null"

        elif type_ == "bool" or type_ == "unlock":
            s = text2bool(v)

        elif type_ == "date":
            val = util.dateDMAtoAMD(v)
            if val is None:
                s = "Null"
            else:
                s = "'%s'" % val

        elif type_ == "time":
            s = "'%s'" % v

        elif type_ in ("uint", "int", "double", "serial"):
            s = v

        elif type_ in ("string", "stringlist"):
            if v == "":
                s = "Null"
            else:
                if type_ == "string":
                    v = auto_qt_translate_text(v)
                if upper and type_ == "string":
                    v = v.upper()

                s = "'%s'" % v

        elif type_ == "pixmap":
            if v.find("'") > -1:
                v = self.normalizeValue(v)
            s = "'%s'" % v

        else:
            s = v
        # print ("PNSqlDriver(%s).formatValue(%s, %s) = %s" % (self.name_, type_, v, s))
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
            self.setLastError(
                "No se pudo crear punto de salvaguarda", "SAVEPOINT sv_%s" % n)
            qWarning("PSQLDriver:: No se pudo crear punto de salvaguarda SAVEPOINT sv_%s \n %s " % (
                n, traceback.format_exc()))
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
            self.setLastError(
                "No se pudo rollback a punto de salvaguarda", "ROLLBACK TO SAVEPOINTt sv_%s" % n)
            qWarning("PSQLDriver:: No se pudo rollback a punto de salvaguarda ROLLBACK TO SAVEPOINT sv_%s\n %s" % (
                n, traceback.format_exc()))
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
            qWarning("PSQLDriver:: No se pudo aceptar la transacción COMMIT\n %s" %
                     traceback.format_exc())
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
            qWarning("PSQLDriver:: No se pudo deshacer la transacción ROLLBACK\n %s" %
                     traceback.format_exc())
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
            qWarning("PSQLDriver:: No se pudo crear la transacción BEGIN\n %s" %
                     traceback.format_exc())
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
            self.setLastError(
                "No se pudo release a punto de salvaguarda", "RELEASE SAVEPOINT sv_%s" % n)
            qWarning("PSQLDriver:: No se pudo release a punto de salvaguarda RELEASE SAVEPOINT sv_%s\n %s" % (
                n, traceback.format_exc()))

            return False

        return True

    def setType(self, type_, leng=None):
        if leng:
            return "::%s(%s)" % (type_, leng)
        else:
            return "::%s" % type_

    def refreshQuery(self, curname, fields, table, where, cursor, conn):
        sql = "DECLARE %s NO SCROLL CURSOR WITH HOLD FOR SELECT %s FROM %s WHERE %s " % (
            curname, fields, table, where)
        try:
            cursor.execute(sql)
        except Exception:
            logger.warn("Error en consulta %s", sql, stack_info=True)
            return
            qWarning("CursorTableModel.Refresh\n %s" % traceback.format_exc())

    def refreshFetch(self, number, curname, table, cursor, fields, where_filter):
        sql = "FETCH %d FROM %s" % (number, curname)
        try:
            cursor.execute(sql)
        except Exception:
            qWarning("PSQLDriver.refreshFetch\n %s" % traceback.format_exc())

    def fetchAll(self, cursor, tablename, where_filter, fields, curname):
        ret_ = []
        try:
            ret_ = cursor.fetchall()
        except Exception:
            qWarning("PSQLDriver.fetchAll\n %s" % traceback.format_exc())

        return ret_

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
                    cursor = self.conn_.cursor()
                    # self.transaction()
                    try:
                        cursor.execute("CREATE SEQUENCE %s" % seq)
                    except Exception:
                        print("FLQPSQL::sqlCreateTable:\n",
                              traceback.format_exc())
                    # self.commitTransaction()

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
                             QApplication.tr(" ya es clave primaria. Sólo puede existir una clave primaria en FLTableMetaData, "
                                             "use FLCompoundKey para crear claves compuestas."))
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

    def mismatchedTable(self, table1, tmd_or_table2, db_=None):

        if db_ is None:
            db_ = self.db_

        if isinstance(tmd_or_table2, str):
            mtd = db_.manager().metadata(tmd_or_table2, True)
            if not mtd:
                return False

            mismatch = False
            try:
                recMtd = self.recordInfo(tmd_or_table2)
                recBd = self.recordInfo2(table1)
                # fieldBd = None
                for fieldMtd in recMtd:
                    # fieldBd = None
                    found = False
                    for field in recBd:
                        if field[0] == fieldMtd[0]:
                            found = True
                            if self.notEqualsFields(field, fieldMtd):
                                mismatch = True
                            
                            recBd.remove(field)
                            break
                            

                    if not found:
                        mismatch = True
                        break

            except Exception:
                print(traceback.format_exc())

            return mismatch

        else:
            return self.mismatchedTable(table1, tmd_or_table2.name(), db_)

    def recordInfo2(self, tablename):
        if not self.isOpen():
            return False
        info = []
        stmt = (
            "select pg_attribute.attname, pg_attribute.atttypid, pg_attribute.attnotnull, pg_attribute.attlen, pg_attribute.atttypmod, "
            "pg_attrdef.adsrc from pg_class, pg_attribute "
            "left join pg_attrdef on (pg_attrdef.adrelid = pg_attribute.attrelid and pg_attrdef.adnum = pg_attribute.attnum)"
            " where lower(pg_class.relname) = '%s' and pg_attribute.attnum > 0 and pg_attribute.attrelid = pg_class.oid "
            "and pg_attribute.attisdropped = false order by pg_attribute.attnum" % tablename.lower())
        cursor = self.conn_.cursor()
        cursor.execute(stmt)
        rows = cursor.fetchall()
        for row in rows:
            len_ = row[3]
            precision = row[4]
            name = row[0]
            type_ = row[1]
            allowNull = row[2]
            defVal = row[5]

            if len_ == -1 and precision and precision > -1:
                len_ = precision - 4
                precision = -1

            if len_ == -1:
                len_ = 0

            if precision == -1:
                precision = 0

            if defVal and defVal[0] == "'":
                defVal = defVal[1:len(defVal) - 2]

            info.append([name, self.decodeSqlType(type_),
                         allowNull, len_, precision, defVal])

        return info

    def decodeSqlType(self, type_):
        ret = type_

        if type_ == 16:
            ret = "bool"
        elif type_ == 23:
            ret = "uint"
        elif type_ == 25:
            ret = "stringlist"
        elif type_ == 701:
            ret = "double"
        elif type_ == 1082:
            ret = "date"
        elif type_ == 1083:
            ret = "time"
        elif type_ == 1043:
            ret = "string"

        return ret

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
                print("FLManager : " + qApp.tr("Error al cargar los metadatos para la tabla") + tablename)

                return self.recordInfo2(tablename)

            #docElem = doc.documentElement()
            mtd = self.db_.manager().metadata(tablename, True)
            if not mtd:
                return self.recordInfo2(tablename)
            fL = mtd.fieldList()
            if not fL:
                del mtd
                return self.recordInfo2(tablename)

            for f in mtd.fieldsNames():
                field = mtd.field(f)
                info.append([field.name(), field.type(), not field.allowNull(), field.length(
                ), field.partDecimal(), field.defaultValue(), field.isPrimaryKey()])

            del mtd

        return info

    def notEqualsFields(self, field1, field2):
        ret = False
        try:
            if not field1[2] == field2[2] and not field2[6]:
                ret = True

            if field1[1] == "stringlist" and not field2[1] in ("stringlist", "pixmap"):
                ret = True

            elif field1[1] == "string" and (not field2[1] in ("string", "time", "date") or not field1[3] == field2[3]):
                ret = True
            elif field1[1] == "uint" and not field2[1] in ("int", "uint", "serial"):
                ret = True
            elif field1[1] == "bool" and not field2[1] in ("bool", "unlock"):
                ret = True
            elif field1[1] == "double" and not field2[1] == "double":
                ret = True

        except Exception:
            print(traceback.format_exc())

        return ret

    def tables(self, typeName=None):
        tl = []
        if not self.isOpen():
            return tl

        t = FLSqlQuery()
        t.setForwardOnly(True)

        if not typeName or typeName == "Tables":
            t.exec_(
                "select relname from pg_class where ( relkind = 'r' ) AND ( relname !~ '^Inv' ) AND ( relname !~ '^pg_' ) ")
            while t.next():
                tl.append(str(t.value(0)))

        if not typeName or typeName == "Views":
            t.exec_(
                "select relname from pg_class where ( relkind = 'v' ) AND ( relname !~ '^Inv' ) AND ( relname !~ '^pg_' ) ")
            while t.next():
                tl.append(str(t.value(0)))
        if not typeName or typeName == "SystemTables":
            t.exec_(
                "select relname from pg_class where ( relkind = 'r' ) AND ( relname like 'pg_%' ) ")
            while t.next():
                tl.append(str(t.value(0)))

        del t
        return tl

    def normalizeValue(self, text):
        return None if text is None else str(text).replace("'", "''")

    def hasCheckColumn(self, mtd):
        fieldList = mtd.fieldList()
        if not fieldList:
            return False

        for field in fieldList:
            if field.isCheck() or field.name().endswith("_check_column"):
                return True

        return False

    def constraintExists(self, name):
        sql = "SELECT constraint_name FROM information_schema.table_constraints where constraint_name='%s'" % name

        q = FLSqlQuery(None, self.db_.dbAux())

        return (q.exec_(sql) and q.size() > 0)

    def queryUpdate(self, name, update, filter):
        return """UPDATE %s SET %s WHERE %s RETURNING *""" % (name, update, filter)

    def alterTable(self, mtd1, mtd2=None, key=None):

        if mtd2 is None:
            return self.alterTable3(mtd1)
        else:
            return self.alterTable2(mtd1, mtd2, key)

    def alterTable3(self, newMTD):
        if self.hasCheckColumn(newMTD):
            return False

        oldMTD = newMTD
        fieldList = oldMTD.fieldList()

        renameOld = "%salteredtable%s" % (
            oldMTD.name()[0:5], QDateTime().currentDateTime().toString("ddhhssz"))

        self.db_.dbAux().transaction()

        q = FLSqlQuery(None, self.db_.dbAux())

        constraintName = "%s_key" % oldMTD.name()

        if self.constraintExists(constraintName) and not q.exec_("ALTER TABLE %s DROP CONSTRAINT %s" % (oldMTD.name(), constraintName)):
            self.db_.dbAux().rollback()
            return False

        for oldField in fieldList:
            if oldField.isCheck():
                return False
            if oldField.isUnique():
                constraintName = "%s_%s_key" % (oldMTD.name(), oldField.name())
                if self.constraintExists(constraintName) and not q.exec_("ALTER TABLE %s DROP CONSTRAINT %s" % (oldMTD.name(), constraintName)):
                    self.db_.dbAux().rollback()
                    return False

        if not q.exec_("ALTER TABLE %s RENAME TO %s" % (oldMTD.name(), renameOld)):
            self.db_.dbAux().rollback()
            return False

        if not self.db_.manager().createTable(newMTD):
            self.db_.dbAux().rollback()
            return False

        oldCursor = FLSqlCursor(renameOld, True, self.db_.dbAux())
        oldCursor.setModeAccess(oldCursor.Browse)
        oldCursor.select()

        fieldList = newMTD.fieldList()

        if not fieldList:
            self.db_.dbAux().rollback()
            return False

        oldCursor.select()
        totalSteps = oldCursor.size()
        progress = QProgressDialog(qApp.tr("Reestructurando registros para %1...").arg(
            newMTD.alias()), qApp.tr("Cancelar"), 0, totalSteps)
        progress.setLabelText(qApp.tr("Tabla modificada"))

        step = 0
        newBuffer = None
        newField = None
        listRecords = []
        newBufferInfo = self.recordInfo2(newMTD.name())
        oldFieldsList = {}
        newFieldsList = {}
        defValues = {}
        v = None

        for newField in fieldList:
            oldField = oldMTD.field(newField.name())
            defValues[str(step)] = None
            if not oldField or not oldCursor.field(oldField.name()):
                if not oldField:
                    oldField = newField
                if not newField.type() == "serial":
                    v = newField.defaultValue()
                    defValues[str(step)] = v

            newFieldsList[str(step)] = newField
            oldFieldsList[str(step)] = oldField
            step = step + 1

        ok = True
        while oldCursor.next():
            newBuffer = newBufferInfo

            for reg in defValues.keys():
                newField = newFieldsList[reg]
                oldField = oldFieldsList[reg]
                if defValues[reg]:
                    v = defValues[reg]
                else:
                    v = oldCursor.value(newField.name())
                    if (not oldField.allowNull or not newField.allowNull()) and not v and not newField.type() == "serial":
                        defVal = newField.defaultValue()
                        if defVal is not None:
                            v = defVal

                    if v is not None and not newBuffer.field(newField.name()).type() == newField.type():
                        print("FLManager::alterTable : " + qApp.tr(
                            "Los tipos del campo %1 no son compatibles. Se introducirá un valor nulo.").arg(newField.name()))

                    if v is not None and newField.type() == "string" and newField.length() > 0:
                        v = str(v)[0:newField.length()]

                    if (not oldField.allowNull() or not newField.allowNull()) and v is None:
                        if oldField.type() == "serial":
                            v = int(self.nextSerialVal(
                                newMTD.name(), newField.name()))
                        elif oldField.type() in ("int", "uint", "bool", "unlock"):
                            v = 0
                        elif oldField.type() == "double":
                            v = 0.0
                        elif oldField.type() == "time":
                            v = QTime().currentTime()
                        elif oldField.type() == "date":
                            v = QDate().currentDate()
                        else:
                            v = "NULL"[0:newField.length()]

                    newBuffer.setValue(newField.name(), v)

                listRecords.append(newBuffer)

            # if not self.insertMulti(newMTD.name(), listRecords):
            #    ok = False
            #    listRecords.clear()
            #    break

            # listRecords.clear()

        if len(listRecords) > 0:
            if not self.insertMulti(newMTD.name(), listRecords):
                ok = False
            listRecords.clear()

        if ok:
            self.db_.dbAux().commit()
        else:
            self.db_.dbAux().rollback()
            return False

        force = False  # FIXME
        if force and ok:
            q.exec_("DROP TABLE %s CASCADE" % renameOld)
        return True

    def alterTable2(self, mtd1, mtd2, key, force=False):

        util = FLUtil()

        oldMTD = None
        newMTD = None
        doc = QDomDocument("doc")
        docElem = None

        if not util.docDocumentSetContect(doc, mtd1):
            print("FLManager::alterTable : " +
                  qApp.tr("Error al cargar los metadatos."))
        else:
            docElem = doc.documentElement()
            oldMTD = self.db_.manager().metadata(docElem, True)

        if oldMTD and oldMTD.isQuery():
            return True

        if not util.docDocumentSetContect(doc, mtd2):
            print("FLManager::alterTable : " +
                  qApp.tr("Error al cargar los metadatos."))
            return False
        else:
            docElem = doc.documentElement()
            newMTD = self.db_.manager().metadata(docElem, True)

        if not oldMTD:
            oldMTD = newMTD

        if not oldMTD.name() == newMTD.name():
            print("FLManager::alterTable : " +
                  qApp.tr("Los nombres de las tablas nueva y vieja difieren."))
            if oldMTD and not oldMTD == newMTD:
                del oldMTD
            if newMTD:
                del newMTD

            return False

        oldPK = oldMTD.primaryKey()
        newPK = newMTD.primaryKey()

        if not oldPK == newPK:
            print("FLManager::alterTable : " +
                  qApp.tr("Los nombres de las claves primarias difieren."))
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
            print("FLManager::alterTable : " + qApp.tr(
                "La tabla %1 antigua de donde importar los registros no existe.").arg(oldMTD.name()))
            if oldMTD and not oldMTD == newMTD:
                del oldMTD
            if newMTD:
                del newMTD

            return False

        fieldList = oldMTD.fieldList()
        oldField = None

        if not fieldList:
            print("FLManager::alterTable : " +
                  qApp.tr("Los antiguos metadatos no tienen campos."))
            if oldMTD and not oldMTD == newMTD:
                del oldMTD
            if newMTD:
                del newMTD

            return False

        renameOld = "%salteredtable%s" % (
            oldMTD.name()[0:5], QDateTime().currentDateTime().toString("ddhhssz"))

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
        constraintName = "%s_pkey" % oldMTD.name()

        if self.constraintExists(constraintName) and not q.exec_("ALTER TABLE %s DROP CONSTRAINT %s" % (oldMTD.name(), constraintName)):
            print("FLManager : " + qApp.tr("En método alterTable, no se ha podido borrar el índice %1_pkey de la tabla antigua.").arg(oldMTD.name()))
            self.db_.dbAux().rollback()
            if oldMTD and not oldMTD == newMTD:
                del oldMTD
            if newMTD:
                del newMTD

            return False

        fieldsNamesOld = []
        for it in fieldList:
            if newMTD.field(it.name()):
                fieldsNamesOld.append(it.name())

            if it.isUnique():
                constraintName = "%s_%s_key" % (oldMTD.name(), it.name())
                if self.constraintExists(constraintName) and not q.exec_("ALTER TABLE %s DROP CONSTRAINT %s" % (oldMTD.name(), constraintName)):
                    print("FLManager : " + qApp.tr("En método alterTable, no se ha podido borrar el índice %1_%2_key de la tabla antigua.")
                          .arg(oldMTD.name(), oldField.name()))
                    self.db_.dbAux().rollback()
                    if oldMTD and not oldMTD == newMTD:
                        del oldMTD
                    if newMTD:
                        del newMTD

                    return False

        if not q.exec_("ALTER TABLE %s RENAME TO %s" % (oldMTD.name(), renameOld)):
            print("FLManager::alterTable : " +
                  qApp.tr("No se ha podido renombrar la tabla antigua."))

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

        v = None
        ok = False

        if not force and not fieldsNamesOld:
            self.db_.dbAux().rollback()
            if oldMTD and not oldMTD == newMTD:
                del oldMTD
            if newMTD:
                del newMTD

            return self.alterTable2(mtd1, mtd2, key, True)

        oldCursor = FLSqlCursor(renameOld, True, self.db_.dbAux())
        oldCursor.setModeAccess(oldCursor.Browse)
        newCursor = FLSqlCursor(newMTD.name(), True, self.db_.dbAux())
        newCursor.setMode(newCursor.Insert)

        oldCursor.select()
        totalSteps = oldCursor.size()
        progress = QProgressDialog(qApp.tr("Reestructurando registros para %1...").arg(
            newMTD.alias()), qApp.tr("Cancelar"), 0, totalSteps)
        progress.setLabelText(qApp.tr("Tabla modificada"))

        step = 0
        newBuffer = None
        newField = None
        listRecords = []
        newBufferInfo = self.recordInfo2(newMTD.name())
        oldFieldsList = {}
        newFieldsList = {}
        defValues = {}
        v = None

        for newField in fieldList:
            oldField = oldMTD.field(newField.name())
            defValues[str(step)] = None
            if not oldField or not oldCursor.field(oldField.name()):
                if not oldField:
                    oldField = newField
                if not newField.type() == "serial":
                    v = newField.defaultValue()
                    defValues[str(step)] = v

            newFieldsList[str(step)] = newField
            oldFieldsList[str(step)] = oldField
            step = step + 1

        step = 0
        ok = True
        while oldCursor.next():
            newBuffer = newBufferInfo

            for reg in defValues.keys():
                newField = newFieldsList[reg]
                oldField = oldFieldsList[reg]
                if defValues[reg]:
                    v = defValues[reg]
                else:
                    v = oldCursor.value(newField.name())
                    if (not oldField.allowNull or not newField.allowNull()) and not v and not newField.type() == "serial":
                        defVal = newField.defaultValue()
                        if defVal is not None:
                            v = defVal

                    if v is not None and not newBuffer.field(newField.name()).type() == newField.type():
                        print("FLManager::alterTable : " + qApp.tr(
                            "Los tipos del campo %1 no son compatibles. Se introducirá un valor nulo.").arg(newField.name()))

                if v is not None and newField.type() == "string" and newField.length() > 0:
                    v = str(v)[0:newField.length()]

                if (not oldField.allowNull() or not newField.allowNull()) and v is None:
                    if oldField.type() == "serial":
                        v = int(self.nextSerialVal(
                            newMTD.name(), newField.name()))
                    elif oldField.type() in ("int", "uint", "bool", "unlock"):
                        v = 0
                    elif oldField.type() == "double":
                        v = 0.0
                    elif oldField.type() == "time":
                        v = QTime().currentTime()
                    elif oldField.type() == "date":
                        v = QDate().currentDate()
                    else:
                        v = "NULL"[0:newField.length()]

                newBuffer.setValue(newField.name(), v)

            listRecords.append(newBuffer)

            if not self.insertMulti(newMTD.name(), listRecords):
                ok = False
                listRecords.clear()
                break

            listRecords.clear()

        if len(listRecords) > 0:
            if not self.insertMulti(newMTD.name(), listRecords):
                ok = False
            listRecords.clear()

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

        if force and ok:
            q.exec_("DROP TABLE %s CASCADE" % renameOld)

        return True

    def insertMulti(self, tableName, records):
        k = len(records)

        if k == 0:
            return None

        fList = []
        vList = []
        for rec in records:
            for f in rec.fieldsList():
                field = rec.field(f)
                if rec.isGenerated(field):
                    fList.append(field.name)
                    vList.append(self.formatvalue(
                        field.type_, field.value, False))

        sql = "INSERT INTO (%s) values (%s)" % (
            fList.split(","), vList.split(","))
        return sql  # FIXME

    def Mr_Proper(self):
        util = FLUtil()
        self.db_.dbAux().transaction()

        qry = FLSqlQuery(None, "dbAux")
        qry2 = FLSqlQuery(None, "dbAux")
        qry3 = FLSqlQuery(None, "dbAux")
        qry4 = FLSqlQuery(None, "dbAux")
        qry5 = FLSqlQuery(None, "dbAux")
        steps = 0

        rx = QRegExp("^.*\\d{6,9}$")
        if rx in self.tables() is not False:
            listOldBks = rx in self.tables()
        else:
            listOldBks = []

        qry.exec_("select nombre from flfiles where nombre similar to"
                  "'%[[:digit:]][[:digit:]][[:digit:]][[:digit:]]-[[:digit:]][[:digit:]]%:[[:digit:]][[:digit:]]%' or nombre similar to"
                  "'%alteredtable[[:digit:]][[:digit:]][[:digit:]][[:digit:]]%' or (bloqueo='f' and nombre like '%.mtd')")

        util.createProgressDialog(
            util.tr("Borrando backups"), len(listOldBks) + qry.size() + 2)

        while qry.next():
            item = qry.value(0)
            util.setLabelText(util.tr("Borrando registro %s") % item)
            qry2.exec_("DELETE FROM flfiles WHERE nombre ='%s'" % item)
            if item.find("alteredtable") > -1:
                if self.existsTable(item.replace(".mtd", "")):
                    util.setLabelText(util.tr("Borrando tabla %1").arg(item))
                    qry2.exec_("DROP TABLE %s CASCADE" %
                               item.replace(".mtd", ""))

            steps = steps + 1
            util.setProgress(steps)

        for item in listOldBks:
            if self.existsTable(item):
                util.setLabelText(util.tr("Borrando tabla %s" % item))
                qry2.exec_("DROP TABLE %s CASCADE" % item)

            steps = steps + 1
            util.setProgress(steps)

        util.setLabelText(util.tr("Inicializando cachés"))
        steps = steps + 1
        util.setProgress(steps)
        qry.exec_("DELETE FROM flmetadata")
        qry.exec_("DELETE FROM flvar")
        self.db_.manager().cleanupMetaData()
        # self.db_.driver().commit()
        util.destroyProgressDialog()

        steps = 0
        qry3.exec_("select tablename from pg_tables where schemaname='public'")
        util.createProgressDialog(
            util.tr("Comprobando base de datos"), qry3.size())
        while qry3.next():
            item = qry3.value(0)
            util.setLabelText(util.tr("Comprobando tabla %s" % item))
            mustAlter = self.mismatchedTable(item, item)
            if mustAlter:
                conte = self.db_.managerModules().content("%s.mtd" % item)
                if conte:
                    msg = util.tr("La estructura de los metadatos de la tabla '%s' y su "
                                  "estructura interna en la base de datos no coinciden. "
                                  "Intentando regenerarla." % item)

                    print(msg)
                    self.alterTable2(conte, conte, None, True)

            steps = steps + 1
            util.setProgress(steps)

        self.db_.dbAux().driver().transaction()
        steps = 0
        #sqlCursor = FLSqlCursor(None, True, self.db_.dbAux())
        sqlQuery = FLSqlQuery(None, self.db_.dbAux())
        if sqlQuery.exec_("select relname from pg_class where ( relkind = 'r' ) "
                          "and ( relname !~ '^Inv' ) " "and ( relname !~ '^pg_' ) and ( relname !~ '^sql_' )"):

            util.setTotalSteps(sqlQuery.size())
            while sqlQuery.next():
                item = sqlQuery.value(0)
                steps = steps + 1
                util.setProgress(steps)
                util.setLabelText(util.tr("Creando índices para %s" % item))
                mtd = self.db_.manager().metadata(item)
                fL = mtd.fieldList()
                if not mtd or not fL:
                    continue
                for it in fL:
                    if not it or not it.type() == "pixmap":
                        continue
                    cur = FLSqlCursor(item, True, self.db_.dbAux())
                    cur.select(it.name() + " not like 'RK@%'")
                    while cur.next():
                        v = cur.value(it.name())
                        if v is None:
                            continue

                        v = self.db_.manager().storeLargeValue(mtd, v)
                        if v:
                            buf = cur.primeUpdate()
                            buf.setValue(it.name(), v)
                            cur.update(False)

                #sqlCursor.setName(item, True)

        # self.db_.dbAux().driver().commit()

        steps = 0
        qry4.exec_("select tablename from pg_tables where schemaname='public'")
        util.createProgressDialog(
            util.tr("Analizando base de datos"), qry4.size())
        while qry4.next():
            item = qry4.value(0)
            util.setLabelText(util.tr("Analizando tabla %s" % item))
            qry5.exec_("vacuum analyze %s" % item)
            steps = steps + 1
            util.setProgress(steps)

        util.destroyProgressDialog()

    def cascadeSupport(self):
        return True

    def canDetectLocks(self):
        return True

    def desktopFile(self):
        return False

    def execute_query(self, q):

        if not self.isOpen():
            qWarning("PSQLDriver::execute_query. DB is closed")
            return False

        cursor = self.conn_.cursor()
        try:
            cursor.execute(q)
        except Exception:
            self.setLastError(
                "No se puedo ejecutar la siguiente query %s" % q)
            qWarning("PSQLDriver:: No se puedo ejecutar la siguiente query %s % q\n %s" % (
                q, traceback.format_exc()))
