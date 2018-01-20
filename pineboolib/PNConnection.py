# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QMessageBox
from PyQt5.Qt import qWarning
from PyQt5 import QtCore, QtWidgets

from pineboolib import decorators, PNSqlDrivers
from pineboolib.flcontrols import ProjectClass

from pineboolib.fllegacy.FLManager import FLManager
from pineboolib.fllegacy.FLSqlQuery import FLSqlQuery
from pineboolib.fllegacy.FLManagerModules import FLManagerModules
from pineboolib.fllegacy.FLSqlSavePoint import FLSqlSavePoint
from pineboolib.fllegacy.FLSqlCursor import FLSqlCursor

import traceback
import sys


class PNConnection(QtCore.QObject):

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
    
    def __init__(self, db_name, db_host, db_port, db_userName, db_password, driverAlias, name = None):
        super(PNConnection,self).__init__()
        
        self.connAux = {}
        self.name = name
        self.db_name = db_name
        self.db_host = db_host
        self.db_port = db_port
        self.db_userName = db_userName
        self.db_password = db_password
        self.driverSql = PNSqlDrivers.PNSqlDrivers()

        self.driverName_ = self.driverSql.aliasToName(driverAlias)

        if (self.driverName_ and self.driverSql.loadDriver(self.driverName_)):
            self.conn = self.conectar(
                self.db_name, self.db_host, self.db_port, self.db_userName, self.db_password)
            if self.conn == False:
                return

            self._dbAux = self

        else:
            print("PNConnection.ERROR: No se encontro el driver \'%s\'" %
                  driverAlias)
            sys.exit(0)

        self.transaction_ = 0
        self.stackSavePoints_ = []
        self.queueSavePoints_ = []
        self.interactiveGUI_ = True

        self.driver().db_ = self

    def connectionName(self):
        return self.name

    """
    Permite seleccionar una conexion que no es la default, Si no existe la crea
    """

    def useConn(self, name="default"):
        if name == "default":
            return self

        for k in self.connAux.keys():
            if k == name:
                return self.connAux[name]

        print("PNConnection::Creando nueva conexión", name)
        
        self.connAux[name] = PNConnection(self.db_name, self.db_host, self.db_port, self.db_userName, self.db_password, self.driverSql.nameToAlias(self.driverName()), name)
        
        return self.connAux[name]

    @decorators.NotImplementedWarn
    def removeConn(self, name = "default"):
        return True

    def isOpen(self):
        return self.driver().isOpen()
        
    def tables(self):
        return self.driver().tables()

    def database(self, name=None):
        if name == None:
            return self.DBName()

        return self.useConn(name)

    def DBName(self):
        try:
            return self.driver().DBName()
        except:
            return self.db_name

    def driver(self):
        return self.driverSql.driver()

    def cursor(self):
        return self.conn.cursor()

    def conectar(self, db_name, db_host, db_port, db_userName, db_password):
        return self.driver().connect(db_name, db_host, db_port, db_userName, db_password)

    def driverName(self):
        return self.driver().driverName()

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
            self._manager = FLManager(self)

        return self._manager

    @decorators.NotImplementedWarn
    def md5TuplesStateTable(self, curname):
        return True

    def db(self):
        return self.conn

    def dbAux(self):
        return self._dbAux

    def formatValue(self, t, v, upper):
        return self.driverSql.formatValue(t, v, upper)

    def nextSerialVal(self, table, field):
        self.driverSql.nextSerialVal(table, field)

    def canSavePoint(self):
        return True

    def doTransaction(self, cursor):
        if not cursor or not self.db():
            return False

        if self.transaction_ == 0:
            print("Iniciando Transacción...")
            if self.transaction():
                self.savePoint(self.transaction_)
                self.lastActiveCursor_ = cursor
                self.transaction_ = self.transaction_ + 1
                # cursor.d.transactionsOpened_.push(self.transaction_)
                cursor.d.transactionsOpened_.append(self.transaction_)
                return True
            else:
                print(
                    "PNConnection::doTransaction : Fallo al intentar iniciar la transacción")
                return False
        else:
            print("Creando punto de salvaguarda %s" % self.transaction_)
            self.savePoint(self.transaction_)

            self.transaction_ = self.transaction_ + 1
            cursor.d.transactionsOpened_.append(self.transaction_)  # push

    def transactionLevel(self):
        return self.transaction_

    def doRollback(self, cur):
        if not cur or not self.conn:
            return False

        cancel = False
        if self.interactiveGUI() and (cur.d.modeAccess_ == FLSqlCursor.Insert or cur.d.modeAccess_ == FLSqlCursor.Edit) and cur.isModifiedBuffer() and cur.d.askForCancelChanges_:
            #res = QMessageBox.information(QtWidgets.QApplication, "Cancelar Cambios", "Todos los cambios se cancelarán.¿Está seguro?", QMessageBox.Yes, [QMessageBox.No, QMessageBox.Default, QMessageBox.Escape])
            res = QtWidgets.QMessageBox.information(QtWidgets.QApplication.focusWidget(
            ), "Cancelar Cambios", "Todos los cambios se cancelarán.¿Está seguro?", QMessageBox.Yes, QMessageBox.No)
            if res == QMessageBox.No:
                return False
            cancel = True

        if self.transaction_ > 0:
            if cur.d.transactionsOpened_:
                trans = cur.d.transactionsOpened_.pop()
                if not trans == self.transaction_:
                    print("FLSqlDatabase : El cursor va a deshacer la transacción %s pero la última que inició es la %s" % (
                        self.transaction_, trans))
            else:
                print(
                    "FLSqlDatabaser : El cursor va a deshacer la transacción %s pero no ha iniciado ninguna" % self.transaction_)

            self.transaction_ = self.transaction_ - 1
        else:
            return True

        if self.transaction_ == 0:
            print("Deshaciendo Transacción...")
            try:
                self.rollbackSavePoint(self.transaction_)
                self.rollbackTransaction()
                self.lastActiveCursor_ = None
                cur.d.modeAccess_ = FLSqlCursor.Browse
                if cancel:
                    cur.select()

                return True
            except:
                print(
                    "FLSqlDatabase::doRollback : Fallo al intentar deshacer transacción")
                return False

        else:
            print("Restaurando punto de salvaguarda %s..." % self.transaction_)
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
                    print("PNConnect : El cursor va a terminar la transacción %s pero la última que inició es la %s" % (
                        self.transaction_, trans))
            else:
                print(
                    "PNConnect : El cursor va a terminar la transacción %s pero no ha iniciado ninguna" % self.transaction_)

            self.transaction_ = self.transaction_ - 1
        else:

            return True

        if self.transaction_ == 0:
            print("Terminando transacción...")
            try:
                # self.conn.commit()
                self.releaseSavePoint(self.transaction_)
                self.commitTransaction()
                self.lastActiveCursor_ = None

                if notify:
                    cur.d.modeAccess_ = FLSqlCursor.Browse

                # aqApp.emitTransactionEnd(cur)

                return True
            except:
                print("PNConnect::doCommit : Fallo al intentar terminar transacción")
                return False
        else:
            print("Liberando punto de salvaguarda %s..." % self.transaction_)
            if self.transaction_ == 1:
                self.releaseSavePoint(self.transaction_)
                if notify:
                    cur.d.modeAccess_ = FLSqlCursor.Browse

                return True
            self.releaseSavePoint(self.transaction_)

            if notify:
                cur.d.modeAccess_ = FLSqlCursor.Browse

            return True

    @decorators.NotImplementedWarn
    def canDetectLocks(self):
        return True

    def managerModules(self):
        if not self._managerModules:
            self._managerModules = FLManagerModules(self.conn)

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
        self.transaction()
        q = self.cursor()
        try:
            q.execute(sql)
        except:
            qWarning(traceback.format_exc())
            self.rollbackTransaction()
            return False
        self.commitTransaction()
        return True

    def mismatchedTable(self, tablename, tmd):
        if not self.db():
            return None

        return self.driver().mismatchedTable(tablename, tmd, self)

    def normalizeValue(self, text):
        if getattr(self.driver(), "normalizeValue", None):
            return self.driver().normalizeValue(text)

        qWarning("PNConnection: El driver %s no dispone de normalizeValue(text)" %
                 self.driverName())
        return text

    def queryUpdate(self, name, update, filter):
        if not self.db():
            return None

        return self.driver().queryUpdate(name, update, filter)
