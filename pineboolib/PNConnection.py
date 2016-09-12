# -*- coding: utf-8 -*-

#from pineboolib.flcontrols import ProjectClass
from pineboolib import decorators, PNSqlDrivers
from PyQt4 import QtCore
import psycopg2
import traceback
from pineboolib.fllegacy.FLManager import FLManager
from pineboolib.fllegacy.FLSqlQuery import FLSqlQuery
from pineboolib.fllegacy.FLManagerModules import FLManagerModules



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
    
    def __init__(self, db_name, db_host, db_port, db_userName, db_password):
        super(PNConnection,self).__init__()
        
        
        self.db_name = db_name
        self.db_host = db_host
        self.db_port = db_port
        self.db_userName = db_userName
        self.db_password = db_password
        self.driverSql = PNSqlDrivers.PNSqlDrivers()
        
        
        
        
        conninfostr = "dbname=%s host=%s port=%s user=%s password=%s connect_timeout=5" % (
                        self.db_name, self.db_host, self.db_port,
                        self.db_userName, self.db_password)
        
        self.conn = self.conectar(conninfostr)
        self._manager = FLManager(self)
        self._managerModules = FLManagerModules(self.conn)
        
    def connectionName(self):
        return self.db_name
    
    def cursor(self):
        return self.conn.cursor()
    
    def conectar(self, conninfostr):
        conn = psycopg2.connect(conninfostr)
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

    @decorators.NotImplementedWarn
    def doTransaction(self, cursor):
        return True
    
    @decorators.NotImplementedWarn
    def doRollback(self, cursor):
        return True
    
    @decorators.NotImplementedWarn
    def interactiveGUI(self):
        return True
    
    @decorators.NotImplementedWarn
    def doCommit(self, cursor, notify):
        return True
    
    @decorators.NotImplementedWarn
    def canDetectLocks(self):
        return True
    
    def managerModules(self):
        return self._managerModules
    
    @decorators.NotImplementedWarn
    def canSavePoint(self):
        return False
    
    
    