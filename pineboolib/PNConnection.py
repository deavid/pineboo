# -*- coding: utf-8 -*-

from pineboolib.flcontrols import ProjectClass
from pineboolib import decorators, PNSqlDrivers
from PyQt5 import QtCore
import psycopg2
import traceback
from pineboolib.fllegacy.FLManager import FLManager
from pineboolib.fllegacy.FLSqlQuery import FLSqlQuery
from pineboolib.fllegacy.FLManagerModules import FLManagerModules
from pineboolib.fllegacy.FLSqlSavePoint import FLSqlSavePoint



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
    
    def __init__(self, db_name, db_host, db_port, db_userName, db_password):
        super(PNConnection,self).__init__()
        
        
        self.db_name = db_name
        self.db_host = db_host
        self.db_port = db_port
        self.db_userName = db_userName
        self.db_password = db_password
        self.driverSql = PNSqlDrivers.PNSqlDrivers()
        
        self.conn = self.conectar(self.db_name, self.db_host, self.db_port, self.db_userName, self.db_password)
        self._manager = FLManager(self)
        self._managerModules = FLManagerModules(self.conn)
        
        self.transaction_ = 0
        self.stackSavePoints_= []
        self.queueSavePoints_= []
        
    def connectionName(self):
        return self.db_name
    
    def driver(self):
        return self.driverSql.driver()
    
    def cursor(self):
        return self.conn.cursor()
    
    def conectar(self, db_name, db_host, db_port, db_userName, db_password):
        conn = self.driver().connect(db_name, db_host, db_port, db_userName, db_password)
        try:
            conn.set_client_encoding("UTF8")
        except Exception:
            print(traceback.format_exc())
        return conn
    
    def seek(self, offs, whence = 0):
        return self.conn.seek(offs, whence)
        
    def database(self, databaseName):
        conninfostr = "dbname=%s host=%s port=%s user=%s password=%s connect_timeout=5" % (
                        databaseName, self.db_host, self.db_port,
                        self.db_userName, self.db_password
                    )
        return self.conectar(conninfostr)
    
    
    def manager(self):
        return self._manager
    
    @decorators.NotImplementedWarn
    def md5TuplesStateTable(self, curname):
        return True
    
    def db(self):
        return self.conn
    
    def formatValue(self, t, v, upper):
        return self.driverSql.formatValue(t, v, upper)
    
    def nextSerialVal(self, table, field):
        self.driverSql.nextSerialVal(table, field)

    def doTransaction(self, cursor):
        if not cursor or not self.db():
            return False
        
        if self.transaction_ == 0 and self.canTransaction():
            print("Iniciando Transacción...")
            if self.db().transaction():
                self.lastActiveCursor_ = cursor
                ProjectClass.emitTransactionBegin(cursor)
            
                if not self.canSavePoint():
                    if self.currentSavePoint_:
                        del self.currentSavePoint_
                        self.currentSavePoint_ = 0
                    
                    self.stackSavePoints_.clear()
                    self.queueSavePoints_.clear()
            
                self.transaction_ = self.transaction_ + 1
                cursor.d.transactionsOpened_.push(self.transaction_)
                return True
            else:
                print("PNConnection::doTransaction : Fallo al intentar iniciar la transacción")
                return False
        else:
            print("Creando punto de salvaguarda %s" % self.transaction_)
            if not self.canSavePoint():
                if self.transaction_ == 0:
                    if self.currentSavePoint_:
                        del self.currentSavePoint_
                        self.currentSavePoint_ = 0
                    
                    self.stackSavePoints_.clear()
                    self.queueSavePoints_.clear()
                

                    self.stackSavePoints_.append(self.currentSavePoint_) #push
                        
                self.currentSavePoint_ = FLSqlSavePoint(self.transaction_)
            
                self.savePoint(int(self.transaction_))
            
            self.transaction_ = self.transaction_ + 1
            cursor.d.transactionsOpened_.append(self.transaction_) #push
        
    
    def transactionLevel(self):
        return self.transaction_
    
    @decorators.BetaImplementation
    def doRollback(self, cursor):
        return self.conn.rollback()
    
    @decorators.NotImplementedWarn
    def interactiveGUI(self):
        return True
    
    @decorators.BetaImplementation
    def doCommit(self, cursor, notify):
        return self.conn.commit()
    
    @decorators.NotImplementedWarn
    def canDetectLocks(self):
        return True
    
    def managerModules(self):
        return self._managerModules
    
    def canSavePoint(self):
        return self.driver().canSavePoint()
    
    def canOverPartition(self):
        if not self.db():
            return False
        
        return self.driver().canOverPartition()
    
    def releaseSavePoint(self, savePoint):
        if not self.db():
            return False
        
        return self.driver().releaseSavePoint(savePoint)
    
    def rollbackSavePoint(self, savePoint):
        if not self.db():
            return False
        
        return self.driver().rollbackSavePoint(savePoint)
        
    
    def canTransaction(self):
        if not self.db():
            return False
        
        return self.driver().hasFeature("Transactions")
        
    
    def nextSerialVal(self, table, field):
        if not self.db():
            return False
        
        return self.driver().nextSerialVal(table, field)    
    
    def savePoint(self, number):
        if not self.db():
            return False
        
        self.driver().savePoint(number)
    
    
    
