from PyQt5.Qt import qWarning, QApplication, QRegExp
from PyQt5.QtXml import QDomDocument
from PyQt5.QtWidgets import QMessageBox, QProgressDialog

from pineboolib.utils import auto_qt_translate_text, checkDependencies
from pineboolib import decorators
from pineboolib.utils import text2bool
from pineboolib.fllegacy.flsqlquery import FLSqlQuery
from pineboolib.fllegacy.flsqlcursor import FLSqlCursor
from pineboolib.fllegacy.flfieldmetadata import FLFieldMetaData

from pineboolib.fllegacy.flutil import FLUtil
import pineboolib



import sys
import traceback

import logging
from PyQt5.QtCore import QTime, QDate, QDateTime

logger = logging.getLogger(__name__)



class FLMYSQL_MYISAM2(object):

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
    cursor_ = None
    db_ = None
    engine_ = None
    session_ = None
    declarative_base_ = None

    def __init__(self):
        self.version_ = "0.6"
        self.conn_ = None
        self.name_ = "FLMYSQL_MyISAM2"
        self.open_ = False
        self.errorList = []
        self.alias_ = "MySQL MyISAM (PyMySQL)"
        self.cursorsArray_ = {}
        self.noInnoDB = True
        self._dbname = None
        self.mobile_ = True
        self.pure_python_ = True
        self.defaultPort_ = 3306
        self.rowsFetched = {}
        self.active_create_index = True
        self.db_ = None
        self.engine_ = None
        self.session_ = None
        self.declarative_base_ = None

    def version(self):
        return self.version_

    def driverName(self):
        return self.name_

    def pure_python(self):
        return self.pure_python_

    def safe_load(self):
        return checkDependencies({"PyMySQL": "PyMySQL", "sqlalchemy":"sqlAlchemy"}, False)

    def mobile(self):
        return self.mobile_

    def isOpen(self):
        return self.open_

    def DBName(self):
        return self._dbname

    def connect(self, db_name, db_host, db_port, db_userName, db_password):
        self._dbname = db_name
        checkDependencies({"PyMySQL": "PyMySQL", "sqlalchemy":"sqlAlchemy"})
        import pymysql
        from sqlalchemy import create_engine

        try:
            self.conn_ = pymysql.connect(host=db_host, user=db_userName, password=db_password, db=db_name, charset="utf8", autocommit=True)
            self.engine_ = create_engine('mysql+mysqldb://%s:%s@%s:%s/%s' % (db_userName, db_password, db_host, db_port, db_name))
        except pymysql.Error as e:
            pineboolib.project._splash.hide()
            if "Unknown database" in str(e):
                ret = QMessageBox.warning(None, "Pineboo",
                                          "La base de datos %s no existe.\n¿Desea crearla?" % db_name,
                                          QMessageBox.Ok | QMessageBox.No)
                if ret == QMessageBox.No:
                    return False
                else:
                    try:
                        tmpConn = pymysql.connect(host=db_host, user=db_userName, password=db_password, charset="utf8", autocommit=True)
                        cursor = tmpConn.cursor()
                        try:
                            cursor.execute("CREATE DATABASE %s" % db_name)
                        except Exception:
                            print("ERROR: FLMYSQL2.connect",traceback.format_exc())
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

        if self.conn_:
            self.open_ = True
            #self.conn_.autocommit(True)
            #self.conn_.set_character_set('utf8')

        return self.conn_
    
    def cursor(self):
        if not self.cursor_:
            self.cursor_ = self.conn_.cursor()
        return self.cursor_
    
    def engine(self):
        return self.engine_
    
    def session(self):
        if self.session_ is None:
            from sqlalchemy.orm import sessionmaker
            #from sqlalchemy import event
            #from pineboolib.pnobjectsfactory import before_commit, after_commit
            Session = sessionmaker(bind=self.engine())
            self.session_ = Session()
            #event.listen(Session, 'before_commit', before_commit, self.session_)
            #event.listen(Session, 'after_commit', after_commit, self.session_)
    
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

        # if v == None:
        #    v = ""
        # TODO: psycopg2.mogrify ???

        if v is None:
            s = "Null"

        elif type_ == "bool" or type_ == "unlock":
            s = text2bool(v)

        elif type_ == "date":
            #val = util.dateDMAtoAMD(v)
            val = v
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
    
    
    def tables(self, type_name=None):
        tl = []
        if not self.isOpen():
            return tl
        
        q_tables = FLSqlQuery()
        q_tables.exec_("show tables")
        while q_tables.next():
            tl.append(q_tables.value(0))
        
        return tl

            
            
    

    def nextSerialVal(self, table, field):
        if not self.isOpen():
            logger.warning("%s::beginTransaction: Database not open", self.name_)
            return None

        self.transaction()
        #    self.setLastError("No se puede iniciar la transacción", "BEGIN WORK")
        #    return None

        res = None
        row = None
        max = 0
        cur_max = 0
        updateQry = False
        ret = None
        
        q = FLSqlQuery()
        q.setSelect("max(%s)" % field)
        q.setFrom(table)
        q.setWhere("1 = 1")
        if not q.exec_():
            logger.warning("not exec sequence")
            return None
        if q.first() and q.value(0) is not None:
            max = q.value(0)

        cursor = self.conn_.cursor()



        #print(1,"max de %s.%s = %s" % (table, field, max))


        strQry = "SELECT seq FROM flseqs WHERE tabla = '%s' AND campo ='%s'" % (table, field)
        try:
            cur_max = cursor.execute(strQry)
        except Exception:
            logger.warning("%s:: La consulta a la base de datos ha fallado" , self.name_, traceback.format_exc())
            self.rollbackTransaction()
            return
        
        
        #print(2,"cur_max de %s.%s = %s" % (table, field , cur_max))
        
        updateQry = cur_max > 0

        strQry = None
        ret = max + 1
        if updateQry:
            if ret > cur_max:
                strQry = "UPDATE flseqs SET seq=%s WHERE tabla = '%s' AND campo = '%s'" % (ret, table, field)
        else:
            strQry = "INSERT INTO flseqs (tabla,campo,seq) VALUES('%s','%s',%s)" % (table, field, ret)
        
        result = None
        
        if strQry is not None:
            try:
                result = cursor.execute(strQry)
            except Exception:
                logger.warning("%s:: La consulta a la base de datos ha fallado\n %s" ,self.name_, traceback.format_exc())
                self.rollbackTransaction()

                return


        self.commitTransaction()
        #    qWarning("%s:: No se puede aceptar la transacción" % self.name_)
        #    return

        return ret
    
    def queryUpdate(self, name, update, filter):
        sql = "UPDATE %s SET %s WHERE %s" % (name, update, filter)
        return sql

    def savePoint(self, n):
        if n == 0:
            return True
        
        if not self.isOpen():
            logger.warning("%s::savePoint: Database not open", self.name_)
            return False

        cursor = self.cursor()
        try:
            cursor.execute("SAVEPOINT sv_%s" % n)
        except Exception:
            self.setLastError(
                "No se pudo crear punto de salvaguarda", "SAVEPOINT sv_%s" % n)
            logger.warning("MySQLDriver:: No se pudo crear punto de salvaguarda SAVEPOINT sv_%s \n %s ", n, traceback.format_exc())
            return False

        return True

    def canSavePoint(self):
        return False
    
    def canTransaction(self):
        return False

    def rollbackSavePoint(self, n):
        if n == 0:
            return True
        
        if not self.isOpen():
            logger.warning("%s::rollbackSavePoint: Database not open", self.name_)
            return False

        cursor = self.cursor()
        try:
            cursor.execute("ROLLBACK TO SAVEPOINT sv_%s" % n)
        except Exception:
            self.setLastError(
                "No se pudo rollback a punto de salvaguarda", "ROLLBACK TO SAVEPOINTt sv_%s" % n)
            logger.warning("%s:: No se pudo rollback a punto de salvaguarda ROLLBACK TO SAVEPOINT sv_%s\n %s", self.name_, n, traceback.format_exc())
            return False

        return True

    def setLastError(self, text, command):
        self.lastError_ = "%s (%s)" % (text, command)

    def lastError(self):
        return self.lastError_

    def commitTransaction(self):
        
        if not self.isOpen():
            logger.warning("%s::commitTransaction: Database not open", self.name_)

        cursor = self.cursor()
        try:
            cursor.execute("COMMIT")
        except Exception:
            self.setLastError("No se pudo aceptar la transacción", "COMMIT")
            logger.warning("%s:: No se pudo aceptar la transacción COMMIT\n %s", self.name_, traceback.format_exc())
            return False

        return True

    def rollbackTransaction(self):
        if not self.isOpen():
            logger.warning("%s::rollbackTransaction: Database not open", self.name_)

        cursor = self.cursor()
        if self.canSavePoint():
            try:
                cursor.execute("ROLLBACK")
            except Exception:
                self.setLastError("No se pudo deshacer la transacción", "ROLLBACK")
                qWarning("%s:: No se pudo deshacer la transacción ROLLBACK\n %s" % (
                    self.name_, traceback.format_exc()))
                return False
        else:
            qWarning("%s:: No se pudo deshacer la transacción ROLLBACK\n %s" % (self.name_, traceback.format_exc()))

        return True

    def transaction(self):
        
        if not self.isOpen():
            logger.warning("%s::transaction: Database not open", self.name_)

        cursor = self.cursor()
        try:
            cursor.execute("START TRANSACTION")
        except Exception:
            self.setLastError("No se pudo crear la transacción", "BEGIN WORK")
            logger.warning("%s:: No se pudo crear la transacción BEGIN\n %s", self.name_, traceback.format_exc())
            return False

        return True

    def releaseSavePoint(self, n):
        if n == 0:
            return True
        
        if not self.isOpen():
            qWarning("%s::releaseSavePoint: Database not open" % self.name_)
            return False

        cursor = self.cursor()
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
        sql = self.fix_query(sql)
        try:
            self.cursorsArray_[curname].execute(sql)
        except Exception:
            qWarning("CursorTableModel.Refresh\n %s" % traceback.format_exc())
    
    def fix_query(self, val):
        ret_ = val.replace("'true'","1")
        ret_ = ret_.replace("'false'", "0")
        ret_ = ret_.replace("\'0\'", "0")
        ret_ = ret_.replace("\'1\'", "1")
        return ret_

    def refreshFetch(self, number, curname, table, cursor, fields, where_filter):
        pass
        #try:
        #    self.cursorsArray_[curname].fetchmany(number)
        #except Exception:
        #    qWarning("%s.refreshFetch\n %s" %(self.name_, traceback.format_exc()))

    def useThreads(self):
        return False

    def useTimer(self):
        return True

    def fetchAll(self, cursor, tablename, where_filter, fields, curname):
        if curname not in self.rowsFetched.keys():
            self.rowsFetched[curname] = 0
        
        rowsF = []
        try:
            rows = list(self.cursorsArray_[curname])
            if self.rowsFetched[curname] < len(rows):
                i = 0
                for row in rows:
                    i += 1
                    if i > self.rowsFetched[curname]:
                        rowsF.append(row)

                self.rowsFetched[curname] = i
        except Exception:
            logger.error("%s:: fetchAll:%s",self.name_, traceback.format_exc())
        
        return rowsF


    def existsTable(self, name):
        if not self.isOpen():
            return False

        t = FLSqlQuery()
        t.setForwardOnly(True)
        ok = t.exec_("SHOW TABLES LIKE '%s'" % name)
        if ok:
            ok = t.next()
            
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
                unlocks += 1

        if unlocks > 1:
            qWarning(u"%s : No se ha podido crear la tabla %s" % (self.name_, tmd.name()))
            qWarning(u"%s : Hay mas de un campo tipo unlock. Solo puede haber uno." % self.name_)
            return None

        i = 1
        for field in fieldList:
            sql = sql + field.name()
            if field.type() == "int":
                sql += " INT"
            elif field.type() in ["uint","serial"]:
                sql += " INT UNSIGNED"
            elif field.type() in ("bool", "unlock"):
                sql += " BOOL"
            elif field.type() == "double":
                sql += " DECIMAL(%s,%s)" % (field.partInteger() + field.partDecimal() +5 , field.partDecimal() + 5)
            elif field.type() == "time":
                sql += " TIME"
            elif field.type() == "date":
                sql += " DATE"
            elif field.type() in ["pixmap","stringlist"]:
                sql += " MEDIUMTEXT"
            elif field.type() == "string":
                if field.length() > 0:
                    if field.length() > 255:
                        sql += " VARCHAR"
                    else:
                        sql += " CHAR"
                    
                    sql += "(%s)" % field.length()
                else:
                    sql += " CHAR(255)"
                    
            elif field.type() == "bytearray":
                sql = sql + " LONGBLOB"


            if field.isPrimaryKey():
                if primaryKey is None:
                    sql += " PRIMARY KEY"
                    primaryKey = field.name()
                else:
                    qWarning(QApplication.tr("FLManager : Tabla-> ") + tmd.name() +
                             QApplication.tr(" . Se ha intentado poner una segunda clave primaria para el campo ") +
                             field.name() + QApplication.tr(" , pero el campo ") + primaryKey +
                             QApplication.tr(" ya es clave primaria. Sólo puede existir una clave primaria en FLTableMetaData,"
                                             " use FLCompoundKey para crear claves compuestas."))
                    return None
            else:
                if field.isUnique():
                    sql += " UNIQUE"
                if not field.allowNull():
                    sql += " NOT NULL"
                else:
                    sql += " NULL"

            if not i == len(fieldList):
                sql += ","
                i = i + 1

        engine = ") ENGINE=INNODB" if not self.noInnoDB else ") ENGINE=MyISAM"
        sql += engine
        
        sql += " DEFAULT CHARACTER SET = utf8 COLLATE = utf8_bin"
        
        qWarning("NOTICE: CREATE TABLE (%s%s)" % (tmd.name(), engine))

        return sql


    def Mr_Proper(self):
        util = FLUtil()
        self.db_.dbAux().transaction()

        qry = FLSqlQuery(None, "dbAux")
        qry2 = FLSqlQuery(None, "dbAux")
        qry3 = FLSqlQuery(None, "dbAux")
        qry4 = FLSqlQuery(None, "dbAux")
        qry5 = FLSqlQuery(None, "dbAux")
        steps = 0
        self.active_create_index = False

        rx = QRegExp("^.*\\d{6,9}$")
        if rx in self.tables() is not False:
            listOldBks = rx in self.tables()
        else:
            listOldBks = []

        qry.exec_("select nombre from flfiles where nombre regexp"
                  "'.*[[:digit:]][[:digit:]][[:digit:]][[:digit:]]-[[:digit:]][[:digit:]].*:[[:digit:]][[:digit:]]$' or nombre regexp"
                  "'.*alteredtable[[:digit:]][[:digit:]][[:digit:]][[:digit:]].*' or (bloqueo=0 and nombre like '%.mtd')")

        util.createProgressDialog(
            util.tr("Borrando backups"), len(listOldBks) + qry.size() + 2)

        while qry.next():
            item = qry.value(0)
            util.setLabelText(util.tr("Borrando registro %s") % item)
            qry2.exec_("DELETE FROM flfiles WHERE nombre ='%s'" % item)
            if item.find("alteredtable") > -1:
                if self.existsTable(item.replace(".mtd", "")):
                    util.setLabelText(util.tr("Borrando tabla %s" % item))
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
        qry3.exec_("SHOW TABLES")
        
        
        
        util.createProgressDialog(util.tr("Comprobando base de datos"), qry3.size())
        while qry3.next():
            item = qry3.value(0)
            #print("Comprobando", item)
            #qry2.exec_("alter table %s convert to character set utf8 collate utf8_bin" % item)
            mustAlter = self.mismatchedTable(item, item)
            if mustAlter:
                conte = self.db_.managerModules().content("%s.mtd" % item)
                if conte:
                    msg = util.tr("La estructura de los metadatos de la tabla '%s' y su "
                                  "estructura interna en la base de datos no coinciden. "
                                  "Intentando regenerarla." % item)

                    logger.warning("%s", msg)
                    self.alterTable2(conte, conte, None, True)

            steps = steps + 1
            util.setProgress(steps)

        self.db_.dbAux().driver().transaction()
        self.active_create_index = True
        steps = 0
        #sqlCursor = FLSqlCursor(None, True, self.db_.dbAux())
        engine = "MyISAM" if self.noInnoDB else "INNODB"
        convert_engine = False
        do_ques = True
        
        
        
        sqlQuery = FLSqlQuery(None, self.db_.dbAux())
        sql_query2 = FLSqlQuery(None, self.db_.dbAux())
        if sqlQuery.exec_("SHOW TABLES"):
            util.setTotalSteps(sqlQuery.size())
            while sqlQuery.next():
                item = sqlQuery.value(0)
                steps = steps + 1
                util.setProgress(steps)
                util.setLabelText(util.tr("Creando índices para %s" % item))
                mtd = self.db_.manager().metadata(item, True)
                if not mtd:
                    continue
                fL = mtd.fieldList()
                if not fL:
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
                sql_query2.exec_("show table status where Engine='%s' and Name='%s'" % (engine, item))
                if (not sql_query2.next()):
                    if do_ques:
                        res = QMessageBox.question(None, util.tr("Mr. Proper"), util.tr("Existen tablas que no son del tipo %s utilizado por el driver de la conexión actual.\n"
                                                                                        "Ahora es posible convertirlas, pero asegurése de tener una COPIA DE SEGURIDAD,\n"
                                                                                        "se pueden peder datos en la conversión de forma definitiva.\n\n"
                                                                                        "¿ Quiere convertirlas ?" % (engine)), QMessageBox.Yes, QMessageBox.No)
                        if res == QMessageBox.Yes:
                            convert_engine = True
                    
                    do_ques = False
                    if convert_engine:
                        conte = self.db_.managerModules().content("%s.mtd" % item)
                        self.alterTable2(conte, conte, None, True)
                
                
                                                                                        
        self.active_create_index = False
        util.destroyProgressDialog()
    
    def alterTable(self, mtd1, mtd2, key):
        return self.alterTable2(mtd1, mtd2, key)
    
    def hasCheckColumn(self, mtd):
        field_list = mtd.fieldList()
        if not field_list:
            return False
        
        for field in field_list:
            if field.isCheck() or field.name().endswith("_check_column"):
                return True
        
        return False

    def alterTable2(self, mtd1, mtd2, key, force=False):
        
        util = FLUtil()

        oldMTD = None
        newMTD = None
        doc = QDomDocument("doc")
        docElem = None

        if not util.domDocumentSetContent(doc, mtd1):
            print("FLManager::alterTable : " + util.tr("Error al cargar los metadatos."))
        else:
            docElem = doc.documentElement()
            oldMTD = self.db_.manager().metadata(docElem, True)

        if oldMTD and oldMTD.isQuery():
            return True
        
        if oldMTD and self.hasCheckColumn(oldMTD):
            return False

        if not util.domDocumentSetContent(doc, mtd2):
            print("FLManager::alterTable : " + util.tr("Error al cargar los metadatos."))
            return False
        else:
            docElem = doc.documentElement()
            newMTD = self.db_.manager().metadata(docElem, True)

        if not oldMTD:
            oldMTD = newMTD

        if not oldMTD.name() == newMTD.name():
            print("FLManager::alterTable : " + util.tr("Los nombres de las tablas nueva y vieja difieren."))
            if oldMTD and not oldMTD == newMTD:
                del oldMTD
            if newMTD:
                del newMTD

            return False

        oldPK = oldMTD.primaryKey()
        newPK = newMTD.primaryKey()

        if not oldPK == newPK:
            print("FLManager::alterTable : " + util.tr("Los nombres de las claves primarias difieren."))
            if oldMTD and not oldMTD == newMTD:
                del oldMTD
            if newMTD:
                del newMTD

            return False

        if not force and self.db_.manager().checkMetaData(oldMTD, newMTD):
            if oldMTD and not oldMTD == newMTD:
                del oldMTD
            if newMTD:
                del newMTD

            return True

        if not self.db_.manager().existsTable(oldMTD.name()):
            print("FLManager::alterTable : " + util.tr("La tabla %1 antigua de donde importar los registros no existe.").arg(oldMTD.name()))
            if oldMTD and not oldMTD == newMTD:
                del oldMTD
            if newMTD:
                del newMTD

            return False

        fieldList = oldMTD.fieldList()
        oldField = None

        if not fieldList:
            print("FLManager::alterTable : " + util.tr("Los antiguos metadatos no tienen campos."))
            if oldMTD and not oldMTD == newMTD:
                del oldMTD
            if newMTD:
                del newMTD

            return False
        
        fieldsNamesOld = []
        if not force:
            for it in fieldList:
                if newMTD.field(it.name()) is not None:
                    fieldsNamesOld.append(it.name())
        
        

        renameOld = "%salteredtable%s" % (oldMTD.name()[0:5], QDateTime().currentDateTime().toString("ddhhssz"))

        if not self.db_.dbAux():
            if oldMTD and not oldMTD == newMTD:
                del oldMTD
            if newMTD:
                del newMTD

            return False

        #self.db_.dbAux().transaction()
        fieldList = newMTD.fieldList()
        
        if not fieldList:
            qWarning("FLManager::alterTable : " + util.tr("Los nuevos metadatos no tienen campos"))
            
            if oldMTD and not oldMTD == newMTD:
                del oldMTD
            if newMTD:
                del newMTD

            return False
        
        q = FLSqlQuery(None, "dbAux")
        in_sql = "ALTER TABLE %s RENAME TO %s" % (oldMTD.name(), renameOld)
        logger.warning(in_sql)
        if not q.exec_(in_sql):
            qWarning("FLManager::alterTable : " + util.tr("No se ha podido renombrar la tabla antigua."))
            
            if oldMTD and not oldMTD == newMTD:
                del oldMTD
            if newMTD:
                del newMTD

            return False
        

        if not self.db_.manager().createTable(newMTD):
            self.db_.dbAux().rollbackTransaction()
            if oldMTD and not oldMTD == newMTD:
                del oldMTD
            if newMTD:
                del newMTD

            return False
        
        
        
        self.db_.dbAux().transaction()
        
        #in_sql = "INSERT INTO flfiles(nombre,contenido,idmodulo,sha) VALUES ('%s.mtd','%s','%s','%s')" % (renameOld, mtd1, self.db_.managerModules().idModuleOfFile("%s.mtd" % oldMTD.name()), key)
        #logger.warning(in_sql)
        #q.exec_(in_sql)    
                
                
        
        ok = False
        if force and fieldsNamesOld:
            sel = fieldsNamesOld.join(",")
            in_sql = "INSERT INTO %s(%s) SELECT %s FROM %s" % (newMTD.name(), sel, sel, renameOld)
            logger.warning(in_sql)
            ok = q.exec_(in_sql)
            if not ok:
                self.db_.dbAux().rollback()
                if oldMTD and not oldMTD == newMTD:
                    del oldMTD
                if newMTD:
                    del newMTD

                return False
            
            return self.alterTable2(mtd1, mtd2, key, True)
        
        if not ok:

            oldCursor = FLSqlCursor(renameOld, True, "dbAux")
            oldCursor.setModeAccess(oldCursor.Browse)
            oldCursor.setForwardOnly(True)
            oldCursor.select()
            totalSteps = oldCursor.size()
            util.createProgressDialog(util.tr("Reestructurando registros para %s..." % newMTD.alias()), totalSteps)
            util.setLabelText(util.tr("Tabla modificada"))

            step = 0
            newBuffer = None
            newField = None
            listRecords = []
            newBufferInfo = self.recordInfo2(newMTD.name())
            vector_fields = {}
            defValues = {}
            v = None
            
            
            for it2 in fieldList:
                oldField = oldMTD.field(it2.name())
                if oldField is None or oldCursor.field(oldField.name()) is None:
                    if oldField is None:
                        oldField = it2
                    if it2.type() != FLFieldMetaData.Serial:
                        v = it2.defaultValue()
                        step += 1
                        defValues[str(step)] = v
                
                step += 1
                vector_fields[str(step)] = it2
                step += 1
                vector_fields[str(step)] = oldField
            
            step2 = 0
            ok = True
            while oldCursor.next():
                newBuffer = newBufferInfo
                
                i = 0
                while i < len(vector_fields):
                    if str(i) in defValues.keys():
                        v = defValues[str(i)]
                        i += 1
                        newField = vector_fields[str(i)]
                        i += 1
                        oldField = vector_fields[str(i)]
                    else:
                        i += 1
                        newField = vector_fields[str(i)]
                        i += 1
                        oldField = vector_fields[str(i)]
                        v = oldCursor.value(newField.name())
                        if (not oldField.allowNull() or not newField.allowNull()) and (v is None) and newField.type != FLFieldMetaData.Serial:
                            defVal = newField.defaultValue()
                            if defVal is not None:
                                v = defVal
                        
                    if v is not None and newField.type() == "string" and newField.length() > 0:
                        v = v[:newField.length()]
                    
                    if (not oldField.allowNull() or not newField.allowNull()) and v is None:
                        if oldField.type() == FLFieldMetadata.Serial:
                            v = int(self.nextSerialVal(newMTD.name(), newField.name()))
                        elif oldField.type() in ["int", "uint", "bool", "unlock"]:
                            v = 0
                        elif oldField.type() == "double":
                            v = 0.0
                        elif oldField.type() == "time":
                            v = QTime.currentTime()
                        elif oldField.type() == "date":
                            v = QDate.currentDate()
                        else:
                            v = str("NULL")[:newField.length()]
                    
                    newBuffer.setValue(newField.name(), v)
                
                listRecords.append(newBuffer)
                if len(listRecords):
                    if not self.insertMulti(newMTD.name(), listRecords):
                        ok = False
                    listRecords.clear()
                
            util.setProgress(totalSteps)
                
                
        
        util.destroyProgressDialog()      
        if ok:
            self.db_.dbAux().commit()
            
            if force:
                q.exec_("DROP TABLE %s CASCADE" % renameOld)
        else:
            self.db_.dbAux().rollback()
                
            q.exec_("DROP TABLE %s CASCADE" % oldMTD.name())
            q.exec_("ALTER TABLE %s RENAME TO %s" % (renameOld, oldMTD.name()))
                
            if oldMTD and oldMTD != newMTD:
                del oldMTD 
            if newMTD:
                del newMTD 
            return False
        
        if oldMTD and oldMTD != newMTD:
            del oldMTD    
        if newMTD:
            del newMTD
                
        return True

    @decorators.NotImplementedWarn
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
        cursor = self.conn_.cursor()
        
        cursor.execute("SHOW FIELDS FROM %s" % tablename)
        #print("Campos", tablename)
        for field in cursor.fetchall():  
            col_name = field[0]
            allow_null = True if field[2] == "NO" else False
            tipo_ = field[1]
            if field[1].find("(") > -1:
                tipo_ = field[1][:field[1].find("(")]
            
                
            
            
            
            #len_
            len_ = "0"
            if field[1].find("(") > -1:
                len_ = field[1][field[1].find("(") + 1:  field[1].find(")")]
            
            precision_ = 0

            
            
            tipo_ = self.decodeSqlType(tipo_)
            
            if tipo_ in ["uint","int","double"]:
                len_ = '0'
                #print("****", tipo_, field)
            else:
                if len_.find(",") > -1:
                    precision_ = len_[len_.find(","):]
                    len_ = len_[:len_.find(",")]
            
            len_ = int(len_)
            
            
            default_value_ = field[4]
            primary_key_ = True if field[3] == "PRI" else False
            #print("***", field)
            #print("Nombre:", col_name)
            #print("Tipo:", tipo_)
            #print("Nulo:", allow_null)
            #print("longitud:", len_)
            #print("Precision:", precision_)
            #print("Defecto:", default_value_)
            info.append([col_name, tipo_, allow_null,len_, precision_, default_value_ , primary_key_])
            #info.append(desc[0], desc[1], not desc[6], , part_decimal, default_value, is_primary_key) 
        
        return info

    def decodeSqlType(self, t):
        
        ret = t
        
        if t in ["char","varchar","text"]:
            ret = "string"
        elif t == "int":
            ret = "uint"
        elif t == "date":
            ret = "date"
        elif t == "mediumtext":
            ret = "stringlist"
        elif t == "tinyint":
            ret = "bool"
        elif t in ["decimal","double"]:
            ret = "double"
        elif t == "longblob":
            ret = "bytearray"
        elif t == "time":
            ret = "time"
        
        else:
            logger.warning("formato desconocido %s", ret)
    
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
        #print("comparando", field1, field1[1], field2, field2[1])
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
        
        
    def normalizeValue(self, text):
        if text is None:
            return None
        
        text = text.replace("'", "''")
        text = text.replace('\\"', '\\\\"')
        text = text.replace("\\n", "\\\\n")
        text = text.replace("\\r", "\\\\r")
        
        
       
        return text

    def cascadeSupport(self):
        return True

    def canDetectLocks(self):
        return True

    def desktopFile(self):
        return False

    def execute_query(self, q):

        if not self.isOpen():
            logger.warning("MySQLDriver::execute_query. DB is closed")
            return False
        cursor = self.cursor()
        try:
            q = self.fix_query(q)
            cursor.execute(q)
        except Exception as exc:           
            self.setLastError("No se puedo ejecutar la siguiente query %s" % q, q)
            logger.warning("MySQLDriver:: No se puedo ejecutar la siguiente query %s\n %s", q, traceback.format_exc())
