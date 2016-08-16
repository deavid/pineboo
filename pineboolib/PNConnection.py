# -*- coding: utf-8 -*-

#from pineboolib.flcontrols import ProjectClass
from pineboolib import decorators, PNSqlDrivers
from PyQt4 import QtCore
import psycopg2
import traceback
from pineboolib.fllegacy.FLManager import FLManager



class PNConnection(QtCore.QObject):
    
    db_name = None
    db_host = None
    db_port = None
    db_userName = None
    db_password = None
    conn = None
    driverSql = None
    
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

    
    
    
    
    
    
    
    