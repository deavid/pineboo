# -*- coding: utf-8 -*-

from pineboolib.flcontrols import ProjectClass
from pineboolib import decorators, PNSqlDrivers
from PyQt5 import QtCore,QtWidgets
import psycopg2
import traceback, sys
from pineboolib.fllegacy.FLManager import FLManager
from pineboolib.fllegacy.FLSqlQuery import FLSqlQuery
from pineboolib.fllegacy.FLManagerModules import FLManagerModules
from pineboolib.fllegacy.FLSqlSavePoint import FLSqlSavePoint
from pineboolib.fllegacy.FLSqlCursor import FLSqlCursor
from PyQt5.QtWidgets import QMessageBox



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
    
    def __init__(self, db_name, db_host, db_port, db_userName, db_password, driverAlias):
        super(PNConnection,self).__init__()
        
        self.connAux = {}
        self.db_name = db_name
        self.db_host = db_host
        self.db_port = db_port
        self.db_userName = db_userName
        self.db_password = db_password
        self.driverSql = PNSqlDrivers.PNSqlDrivers()
        self.driverName_ = self.driverSql.aliasToName(driverAlias)
        
        if (self.driverName_ and self.driverSql.loadDriver(self.driverName_)):
            self.conn = self.conectar(self.db_name, self.db_host, self.db_port, self.db_userName, self.db_password)
        else:
            print("PNConnection.ERROR: No se encontro el driver \'%s\'" % driverAlias)
            sys.exit(0)
            
        self._manager = FLManager(self)
        self._managerModules = FLManagerModules(self.conn)
        
        self.transaction_ = 0
        self.stackSavePoints_= []
        self.queueSavePoints_= []
        self.interactiveGUI_ = True
        
    def connectionName(self):
        return self.db_name
    
    """
    Permite seleccionar una conexion que no es la default, Si no existe la crea
    """
    def useConn(self, name = "default"):
        if name == "default":
            return self.conn
        
        if not name in self.connAux:
            print("PNConnection::Creando nueva conexión", name)
            self.connAux[name] = PNConnection(self.db_name, self.db_host, self.db_port, self.db_userName, self.db_password, self.driverSql.nameToAlias(self.driverName()))
        
        return self.connAux[name]
        
    
    def driver(self):
        return self.driverSql.driver()
    
    def cursor(self):
        return self.conn.cursor()
    
    def conectar(self, db_name, db_host, db_port, db_userName, db_password):
        conn = self.driver().connect(db_name, db_host, db_port, db_userName, db_password)
        return conn
    
    def driverName(self):
        return self.driver().driverName()
    
    def lastError(self):
        return self.driver().lastError()
    
    def host(self):
        return self.db_host
    
    def port(self):
        return self.db_port
    
    def database(self):
        return self.db_name
    
    def user(self):
        return self.db_userName
    
    def password(self):
        return self.db_password
    
    def seek(self, offs, whence = 0):
        return self.conn.seek(offs, whence)
    
    def manager(self):
        return self._manager
    
    @decorators.NotImplementedWarn
    def md5TuplesStateTable(self, curname):
        return True
    
    def db(self):
        return self.conn
    
    def dbAux(self):
        return self.useConn("dbAux").conn
    
    def formatValue(self, t, v, upper):
        return self.driverSql.formatValue(t, v, upper)
    
    def nextSerialVal(self, table, field):
        self.driverSql.nextSerialVal(table, field)

    def doTransaction(self, cursor):
        if not cursor or not self.db():
            return False
        
        if self.transaction_ == 0 and self.canTransaction():
            print("Iniciando Transacción...")
            if self.driver().transaction():
                self.lastActiveCursor_ = cursor
                #ProjectClass.emitTransactionBegin(cursor)
            
                if not self.canSavePoint():
                    if self.currentSavePoint_:
                        del self.currentSavePoint_
                        self.currentSavePoint_ = 0
                    
                    self.stackSavePoints_.clear()
                    self.queueSavePoints_.clear()
            
                self.transaction_ = self.transaction_ + 1
                #cursor.d.transactionsOpened_.push(self.transaction_)
                cursor.d.transactionsOpened_.append(self.transaction_)
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
    
    def doRollback(self, cur):
        if not cur or not self.conn:
            return False
        
        cancel = False
        if self.interactiveGUI() and (cur.d.modeAccess_ == FLSqlCursor.Insert or cur.d.modeAccess_ == FLSqlCursor.Edit) and cur.isModifiedBuffer() and cur.d.askForCancelChanges_:
            #res = QMessageBox.information(QtWidgets.QApplication, "Cancelar Cambios", "Todos los cambios se cancelarán.¿Está seguro?", QMessageBox.Yes, [QMessageBox.No, QMessageBox.Default, QMessageBox.Escape])
            res = QtWidgets.QMessageBox.information(QtWidgets.QApplication.focusWidget(),"Cancelar Cambios", "Todos los cambios se cancelarán.¿Está seguro?", QMessageBox.Yes, (QMessageBox.No, QMessageBox.Default, QMessageBox.Escape))
            if res == QMessageBox.No:
                return False
            cancel = True
        
        if self.transaction_ > 0:
            if cur.d.transactionsOpened_:
                trans = cur.d.transactionsOpened_.pop()
                if not trans == self.transaction_:
                    print("FLSqlDatabase : El cursor va a deshacer la transacción %s pero la última que inició es la %s" % (self.transaction_, trans))
            else:
                print("FLSqlDatabaser : El cursor va a deshacer la transacción %s pero no ha iniciado ninguna" % self.transaction_)
                
            self.transaction_ = self.transaction_ - 1
        else:
            return True
        
        if self.transaction_ == 0 and self.canTransaction():
            print("Deshaciendo Transacción...")
            try:
                self.conn.rollback()
                self.lastActiveCursor_ = None
                
                if not self.canSavePoint():
                    if self.currentSavePoint_:
                        del self.currentSavePoint
                        self.currrentSavePoint = None
                    
                    self.stackSavePoints_.clear()
                    self.queueSavepoints_.clear()
                
                cur.d.modeAccess_ = FLSqlCursor.Browse
                if cancel:
                    cur.select()
                
                #aqApp.TransactionRoolback.emit(cur)
                return True
            except:
                print("FLSqlDatabase::doRollback : Fallo al intentar deshacer transacción")
                return False
        
        else:
            print("Restaurando punto de salvaguarda %s..." % self.transaction_)
            if not self.canSavePoint():
                tamQueue = len(self.queueSavePoints_)
                tempId = None
                
                i = 0
                while i < tamQueue:
                    tempSavePoint = self.queueSavePoints_.dequeue()
                    tempId = tempSavePoint.id()
                    if tempId > self.transaction_ or self.transaction_ == 0:
                        tempSavePoint.undo()
                        del tempSavePoint
                    else:
                        self.queueSavePoints_.enqueue(tempSavePoint)
                    
                    i = i + 1
                
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
    
    def doCommit(self, cur, notify):
        if not cur and not self.db():
            return False
        
        if not notify:
            cur.autocommit.emit()
        
        if self.transaction_ > 0:
            if cur.d.transactionsOpened_:
                trans = cur.d.transactionsOpened_.pop()
                if not trans == self.transaction_:
                    print("PNConnect : El cursor va a terminar la transacción %s pero la última que inició es la %s" % (self.transaction_, trans))
            else:
                print("PNConnect : El cursor va a terminar la transacción %s pero no ha iniciado ninguna" % self.transaction_)
                
            self.transaction_ = self.transaction_ - 1
        else:
            return True
        
        if self.transaction_ == 0 and self.canTransaction():
            print("Terminando transacción...")
            try:
                self.conn.commit()
                self.lastActiveCursor_ = None
                
                if not self.canSavePoint():
                    if self.currentSavePoint_:
                        del self.currentSavePoint_
                        self.currentSavePoint_ = None
                    
                    self.stackSavePoints_.clear()
                    self.queueSavePoints_.clear()
                
                if notify:
                    cur.d.modeAccess_ = FLSqlCursor.Browse
                    
                #aqApp.emitTransactionEnd(cur)
                
                return True
            except:
                print("PNConnect::doCommit : Fallo al intentar terminar transacción")
                return False
        else:
            print("Liberando punto de salvaguarda %s..." % self.transaction_)
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
                tamQueue = len(self.queueSavePoints_)
                tempSavePoint = None
                
                i = 0
                while i < tamQueue:
                    tempSavePoint = self.queueSavePoints_.dequeue()
                    tempSavePoint.setId(self.transaction_ -1)
                    self.queueSavePoints_.enqueue(tempSavePoint)
                    
                    i = i + 1
                
                if self.currentSavePoint_:
                    self.currentSavePoint_.undo()
                    del self.currentSavePoint_
                    self.currentSavePoint_ = None
                    if self.stackSavePoints_:
                        self.currentSavePoint_ = self.stackSavePoints_.pop()
                
                if self.transaction_ == 0:
                    self.queueSavePoints_.enqueue(self.currentSavePoint_)
                    self.currentSavePoint_ = None
                    if self.stackSavePoints_:
                        self.currentSavePoint_ = self.stackSavePoints_.pop()
            else:
                self.releaseSavePoint(self.transaction_)
            
            if notity:
                cur.d.modeAccess_ = FLSqlCursor.Browse
                
                    
            return True
                
     
            
                
    
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
    
    
    
