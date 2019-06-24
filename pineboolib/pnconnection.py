# -*- coding: utf-8 -*-
"""Defines the PNConnection class.

"""
from PyQt5 import QtCore, QtWidgets

from pineboolib.fllegacy.flsqlcursor import FLSqlCursor
from pineboolib.fllegacy.flsettings import FLSettings
from pineboolib.fllegacy.flsqlsavepoint import FLSqlSavePoint
from pineboolib import decorators
from pineboolib.pncontrolsfactory import aqApp
from pineboolib.pnsqldrivers import PNSqlDrivers


import logging

logger = logging.getLogger(__name__)


class PNConnection(QtCore.QObject):
    """Wrapper for database cursors which are used to emulate FLSqlCursor."""

    db_name = None
    db_host = None
    db_port = None
    db_userName = None
    db_password = None
    conn = None
    driverSql = None
    transaction_ = None
    _managerModules = None
    _manager = None
    currentSavePoint_ = None
    stackSavePoints_ = None
    queueSavePoints_ = None
    interactiveGUI_ = None
    _dbAux = None
    name = None
    _isOpen = False

    def __init__(self, db_name, db_host, db_port, db_userName, db_password, driverAlias, name=None):
        super(PNConnection, self).__init__()

        self.driverSql = PNSqlDrivers()

        if name:
            self._isOpen = False
            self.name = name
            return
        else:
            self.name = "default"

        self.driverName_ = self.driverSql.aliasToName(driverAlias)

        if self.driverName_ and self.driverSql.loadDriver(self.driverName_):

            self.conn = self.conectar(db_name, db_host, db_port, db_userName, db_password)
            if self.conn is False:
                return

            self._isOpen = True

        else:
            logger.error("PNConnection.ERROR: No se encontro el driver '%s'", driverAlias)
            import sys

            sys.exit(0)

        self.transaction_ = 0
        self.stackSavePoints_ = []
        self.queueSavePoints_ = []
        self.interactiveGUI_ = True

        self.driver().db_ = self

    @decorators.NotImplementedWarn
    def finish(self):
        pass

    def connectionName(self):
        """Get the current connection name for this cursor."""
        return self.name

    def useConn(self, name="default"):
        """Select another connection which can be not the default one.

        Permite seleccionar una conexion que no es la default, Si no existe la crea
        """
        if isinstance(name, PNConnection):
            name = name.connectionName()

        if name in ("default", None):
            return self

        if name in self.connAux.keys():
            return self.connAux[name]

        name_conn = name
        if name == "dbAux":
            name_conn = None

        self.connAux[name] = PNConnection(
            self.db_name, self.db_host, self.db_port, self.db_userName, self.db_password, self.driverSql.nameToAlias(self.driverName()), name_conn
        )
        return self.connAux[name]

    def removeConn(self, name="default"):
        try:
            self.useConn(name).conn.close()
            self.connAux[name] = None
            del self.connAux[name]
        except Exception:
            pass

        return True

    def isOpen(self):
        return self._isOpen

    def tables(self):
        return self.driver().tables()

    def database(self, name=None):
        if name is None:
            return self.DBName()

        return self.useConn(name)

    def DBName(self):
        try:
            return self.driver().DBName()
        except Exception as e:
            logger.error("DBName: %s", e)
            return self.db_name

    def driver(self):
        return self.driverSql.driver()

    def session(self):
        return self.driver().session()

    def engine(self):
        return self.driver().engine()

    def declarative_base(self):
        return self.driver().declarative_base()

    def cursor(self):
        return self.conn.cursor()

    def conectar(self, db_name, db_host, db_port, db_userName, db_password):

        self.connAux = {}
        self.db_name = db_name
        self.db_host = db_host
        self.db_port = db_port
        self.db_userName = db_userName
        self.db_password = db_password

        return self.driver().connect(db_name, db_host, db_port, db_userName, db_password)

    def driverName(self):
        return self.driver().driverName()

    def driverAlias(self):
        return self.driver().alias_

    def driverNameToDriverAlias(self, name):
        return self.driverSql.nameToAlias(name)

    def lastError(self):
        return self.driver().lastError()

    def host(self):
        return self.db_host

    def port(self):
        return self.db_port

    def user(self):
        return self.db_userName

    def password(self):
        return self.db_password

    def seek(self, offs, whence=0):
        return self.conn.seek(offs, whence)

    def manager(self):
        if not self._manager:
            from pineboolib.fllegacy.flmanager import FLManager

            self._manager = FLManager(self)

        return self._manager

    @decorators.NotImplementedWarn
    def md5TuplesStateTable(self, curname):
        return True

    @decorators.NotImplementedWarn
    def setInteractiveGUI(self, b):
        pass

    @decorators.NotImplementedWarn
    def setQsaExceptions(self, b):
        pass

    def db(self):
        return self.conn

    def dbAux(self):
        return self.useConn("dbAux")

    def formatValue(self, t, v, upper):
        return self.driver().formatValue(t, v, upper)

    def formatValueLike(self, t, v, upper):
        return self.driver().formatValueLike(t, v, upper)

    def canSavePoint(self):
        return self.driver().canSavePoint()

    def canTransaction(self):
        return self.driver().canTransaction()

    def doTransaction(self, cursor):
        if not cursor or not self.db():
            return False

        settings = FLSettings()
        if self.transaction_ == 0 and self.canTransaction():
            if settings.readBoolEntry("application/isDebuggerMode", False):
                aqApp.statusHelpMsg("Iniciando Transacción... %s" % self.transaction_)
            if self.transaction():
                self.lastActiveCursor_ = cursor
                aqApp.emitTransactionBegin(cursor)

                if not self.canSavePoint():
                    if self.currentSavePoint_:
                        del self.currentSavePoint_
                        self.currentSavePoint_ = None

                    self.stackSavePoints_.clear()
                    self.queueSavePoints_.clear()

                self.transaction_ = self.transaction_ + 1
                cursor.d.transactionsOpened_.insert(0, self.transaction_)
                return True
            else:
                logger.warning("doTransaction: Fallo al intentar iniciar la transacción")
                return False

        else:
            if settings.readBoolEntry("application/isDebuggerMode", False):
                aqApp.statusHelpMsg("Creando punto de salvaguarda %s" % self.transaction_)
                if not self.canSavePoint():
                    if self.transaction_ == 0:
                        if self.currentSavePoint_:
                            del self.currentSavePoint_
                            self.currentSavePoint_ = None

                        self.stackSavePoints_.clear()
                        self.queueSavePoints_.clear()

                    if self.currentSavePoint_:
                        if self.stackSavePoints_:
                            self.stackSavePoints_.insert(0, self.currentSavePoint_)
                        else:
                            self.stackSavePoints_.append(self.currentSavePoint_)

                    self.currentSavePoint_ = FLSqlSavePoint(self.transaction_)
                else:
                    self.savePoint(self.transaction_)

            self.transaction_ = self.transaction_ + 1
            if cursor.d.transactionsOpened_:
                cursor.d.transactionsOpened_.insert(0, self.transaction_)  # push
            else:
                cursor.d.transactionsOpened_.append(self.transaction_)
            return True

    def transactionLevel(self):
        return self.transaction_

    def doRollback(self, cur):
        if not cur or not self.conn:
            return False

        cancel = False
        if self.interactiveGUI() and cur.d.modeAccess_ in (FLSqlCursor.Insert, FLSqlCursor.Edit) and cur.isModifiedBuffer() and cur.d.askForCancelChanges_:
            import pineboolib

            if pineboolib.project._DGI.localDesktop():
                res = QtWidgets.QMessageBox.information(
                    QtWidgets.QApplication.activeWindow(),
                    "Cancelar Cambios",
                    "Todos los cambios se cancelarán.¿Está seguro?",
                    QtWidgets.QMessageBox.Yes,
                    QtWidgets.QMessageBox.No,
                )
                if res == QtWidgets.QMessageBox.No:
                    return False

            cancel = True

        if self.transaction_ > 0:
            if cur.d.transactionsOpened_:
                trans = cur.d.transactionsOpened_.pop()
                if not trans == self.transaction_:
                    logger.info("FLSqlDatabase: El cursor va a deshacer la transacción %s pero la última que inició es la %s", self.transaction_, trans)
            else:
                logger.info("FLSqlDatabaser : El cursor va a deshacer la transacción %s pero no ha iniciado ninguna", self.transaction_)

            self.transaction_ = self.transaction_ - 1
        else:
            return True

        if self.transaction_ == 0 and self.canTransaction():
            aqApp.statusHelpMsg("Deshaciendo Transacción...")
            if self.rollbackTransaction():
                self.lastActiveCursor_ = None

                if not self.canSavePoint():
                    if self.currentSavePoint_:
                        del self.currentSavePoint_
                        self.currentSavePoint_ = None

                    self.stackSavePoints_.clear()
                    self.queueSavePoints_.clear()

                cur.d.modeAccess_ = FLSqlCursor.Browse
                if cancel:
                    cur.select()

                aqApp.emitTransactionRollback(cur)
                return True
            else:
                logger.warning("doRollback: Fallo al intentar deshacer transacción")
                return False

        else:
            aqApp.statusHelpMsg("Restaurando punto de salvaguarda %s..." % self.transaction_)
            if not self.canSavePoint():
                tam_queue = len(self.queueSavePoints_)
                for i in range(tam_queue):
                    temp_save_point = self.queueSavePoints_.dequeue()
                    temp_id = temp_save_point.id()

                    if temp_id > self.transaction_ or self.transaction_ == 0:
                        temp_save_point.undo()
                        del temp_save_point
                    else:
                        self.queueSavePoints_.append(temp_save_point)

                if self.currentSavePoint_:
                    self.currentSavePoint_.undo()
                    del self.currentSavePoint_
                    self.currentSavePoint_ = None
                    if self.stackSavePoints_:
                        self.currentSavePoint_ = self.stackSavePoints_.pop()

                if self.transaction_ == 0:
                    if self.currentSavePoint_:
                        del self.currentSavePoint_
                        self.currentSavePoint_ = None

                    self.stackSavePoints_.clear()
                    self.queueSavePoints_.clear()

            else:
                self.rollbackSavePoint(self.transaction_)

            cur.d.modeAccess_ = FLSqlCursor.Browse
            return True

    def interactiveGUI(self):
        return self.interactiveGUI_

    def doCommit(self, cur, notify=True):
        if not cur and not self.db():
            return False

        if not notify:
            cur.autocommit.emit()

        if self.transaction_ > 0:
            if cur.d.transactionsOpened_:
                trans = cur.d.transactionsOpened_.pop()
                if not trans == self.transaction_:
                    logger.warning("El cursor va a terminar la transacción %s pero la última que inició es la %s", self.transaction_, trans)
            else:
                logger.warning("El cursor va a terminar la transacción %s pero no ha iniciado ninguna", self.transaction_)

            self.transaction_ = self.transaction_ - 1
        else:

            return True

        if self.transaction_ == 0 and self.canTransaction():
            settings = FLSettings()
            if settings.readBoolEntry("application/isDebuggerMode", False):
                aqApp.statusHelpMsg("Terminando transacción... %s" % self.transaction_)
            try:
                if self.driver().commitTransaction():
                    self.lastActiveCursor_ = None

                    if not self.canSavePoint():
                        if self.currentSavePoint_:
                            del self.currentSavePoint_
                            self.currentSavePoint_ = None

                        self.stackSavePoints_.clear()
                        self.queueSavePoints_.clear()

                    if notify:
                        cur.d.modeAccess_ = FLSqlCursor.Browse

                    aqApp.emitTransactionEnd(cur)
                    return True

                else:
                    logger.error("doCommit: Fallo al intentar terminar transacción: %s" % self.transaction_)
                    return False

            except Exception as e:
                logger.error("doCommit: Fallo al intentar terminar transacción: %s", e)
                return False
        else:
            aqApp.statusHelpMsg("Liberando punto de salvaguarda %s..." % self.transaction_)
            if (self.transaction_ == 1 and self.canTransaction()) or (self.transaction_ == 0 and not self.canTransaction()):
                if not self.canSavePoint():
                    if self.currentSavePoint_:
                        del self.currentSavePoint_
                        self.currentSavePoint_ = None

                    self.stackSavePoints_.clear()
                    self.queueSavePoints_.clear()
                else:
                    self.releaseSavePoint(self.transaction_)
                if notify:
                    cur.d.modeAccess_ = FLSqlCursor.Browse

                return True
            if not self.canSavePoint():
                tam_queue = len(self.queueSavePoints_)
                for i in range(tam_queue):
                    temp_save_point = self.queueSavePoints_.dequeue()
                    temp_save_point.setId(self.transaction_ - 1)
                    self.queueSavePoints_.append(temp_save_point)

                if self.currentSavePoint_:
                    self.queueSavePoints_.append(self.currentSavePoint_)
                    self.currentSavePoint_ = None
                    if self.stackSavePoints_:
                        self.currentSavePoint_ = self.stackSavePoints_.pop()
            else:
                self.releaseSavePoint(self.transaction_)

            if notify:
                cur.d.modeAccess_ = FLSqlCursor.Browse

            return True

    def canDetectLocks(self):
        if not self.db():
            return False

        return self.driver().canDetectLocks()

    def commit(self):
        if not self.db():
            return False

        return self.driver().commitTransaction()

    def managerModules(self):
        if not self._managerModules:
            from pineboolib.fllegacy.flmanagermodules import FLManagerModules

            self._managerModules = FLManagerModules(self)

        return self._managerModules

    def canOverPartition(self):
        if not self.db():
            return False

        return self.driver().canOverPartition()

    def savePoint(self, savePoint):
        if not self.db():
            return False

        return self.driver().savePoint(savePoint)

    def releaseSavePoint(self, savePoint):
        if not self.db():
            return False

        return self.driver().releaseSavePoint(savePoint)

    def Mr_Proper(self):
        if not self.db():
            return

        self.driver().Mr_Proper()

    def rollbackSavePoint(self, savePoint):
        if not self.db():
            return False

        return self.driver().rollbackSavePoint(savePoint)

    def transaction(self):
        if not self.db():
            return False

        return self.driver().transaction()

    def commitTransaction(self):
        if not self.db():
            return False

        return self.driver().commitTransaction()

    def rollbackTransaction(self):
        if not self.db():
            return False

        return self.driver().rollbackTransaction()

    def nextSerialVal(self, table, field):
        if not self.db():
            return False

        return self.driver().nextSerialVal(table, field)

    def existsTable(self, name):
        if not self.db():
            return False

        return self.driver().existsTable(name)

    def createTable(self, tmd):
        if not self.db():
            return False

        sql = self.driver().sqlCreateTable(tmd)
        if not sql:
            return False
        if self.transaction_ == 0:
            self.transaction()
            self.transaction_ += 1

        for singleSql in sql.split(";"):
            try:
                self.driver().execute_query(singleSql)
            except Exception:
                logger.exception("createTable: Error happened executing sql: %s...", singleSql[:80])
                self.rollbackTransaction()
                return False
        if self.transaction_ > 0:
            self.commitTransaction()
            self.transaction_ -= 1

        return True

    def mismatchedTable(self, tablename, tmd):
        if not self.db():
            return None

        return self.driver().mismatchedTable(tablename, tmd, self)

    def normalizeValue(self, text):
        if getattr(self.driver(), "normalizeValue", None):
            return self.driver().normalizeValue(text)

        logger.warning("PNConnection: El driver %s no dispone de normalizeValue(text)", self.driverName())
        return text

    def queryUpdate(self, name, update, filter):
        if not self.db():
            return None

        return self.driver().queryUpdate(name, update, filter)

    def execute_query(self, q):
        if not self.db():
            return None

        return self.driver().execute_query(q)

    def alterTable(self, mtd_1, mtd_2, key, force=False):
        if not self.db():
            return None

        return self.driver().alterTable(mtd_1, mtd_2, key, force)
