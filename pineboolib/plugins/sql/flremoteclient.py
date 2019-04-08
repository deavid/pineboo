
#from PyQt5.QtCore import QTime, QDate, QDateTime
#from PyQt5.Qt import qWarning, QDomDocument, QRegExp
#from PyQt5.QtWidgets import QMessageBox, QProgressDialog 

from pineboolib.utils import checkDependencies
from pineboolib import decorators
#from pineboolib.fllegacy.flutil import FLUtil
#from pineboolib.fllegacy.flsqlquery import FLSqlQuery
#from pineboolib.fllegacy.flsqlcursor import FLSqlCursor

import traceback
import pineboolib
import sys
import logging
import json


logger = logging.getLogger(__name__)

class cursor_class(object):
    driver_ = None
    id_ = None
    data_ = None
    current_ = None
    last_sql = None
    
    def __init__(self, driver, n):
        self.driver_ = driver
        self.id_ =  n
        self.current_ = None
        self.last_sql = None
        self.description = None
    
    def __getattr__(self, name):
        logger.warn("cursor(%s).%s !!", self.id_,name, stack_info = True)
    
    def execute(self, sql):
        self.last_sql = sql
        self.data_ = self.driver_.send_to_server(self.driver_.create_dict("execute", {"cursor_id": self.id_, "sql": sql}))
        self.current_ = 0
    
    def close(self):
        self.driver_.send_to_server(self.driver_.create_dict("close", {"cursor_id": self.id_}))
    
    def fetchone(self):
        ret_ = self.driver_.send_to_server(self.driver_.create_dict("fetchone", {"cursor_id": self.id_}))
        #print(self.id_, "**", self.last_sql, ret_)
        return ret_
    
    def fetchall(self):
        ret_ = self.driver_.send_to_server(self.driver_.create_dict("fetchall", {"cursor_id": self.id_}))
        #print(self.id_, "**", self.last_sql, ret_)
        return ret_
        
        
    def __iter__(self):
        return self

    def __next__(self):
        ret =  self.driver_.send_to_server(self.driver_.create_dict("fetchone", {"cursor_id": self.id_}))
        if ret is None:
            raise StopIteration
        return ret
        


class conn_class(object):
    
    db_name_ = None
    driver_ = None
    list_cursor = None
    
    def __init__(self, db_name, driver):
        self.db_name_ = db_name
        self.driver_ = driver
        self.list_cursor = []
    
    def is_valid(self):
        db_name_server = self.driver_.send_to_server(self.driver_.create_dict("db_name"))
        return self.db_name_ == db_name_server
    
    def cursor(self):
        cur = cursor_class(self.driver_, len(self.list_cursor))
        self.list_cursor.append(cur)
        return cur
    
        
        


class FLREMOTECLIENT(object):

    version_ = None
    conn_ = None
    name_ = None
    alias_ = None
    errorList = None
    lastError_ = None
    db_ = None
    mobile_ = True
    pure_python_ = True
    defaultPort_ = None

    def __init__(self):
        self.version_ = "0.6"
        self.conn_ = None
        self.name_ = "REMOTECLIENT"
        self.open_ = False
        self.errorList = []
        self.alias_ = "Pineboo Server"
        self._dbname = None
        self.mobile_ = False
        self.pure_python_ = False
        self.defaultPort_ = 4000
        self.id_ = 0
        self.url = None
        checkDependencies({"requests": "requests"}, False)
    
    def useThreads(self):
        return False

    def useTimer(self):
        return True
    
    def desktopFile(self):
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
        return True

    def mobile(self):
        return self.mobile_

    def DBName(self):
        return self._dbname
    
    def create_dict(self, fun, data = []): 
        fun = "%s__%s" % (self.id_, fun)
        return pineboolib.utils.create_dict("dbdata", fun, self.id_, data)
    
    def send_to_server(self, js):
        import requests
        headers = {'content-type': 'application/json'}
        
        req = requests.post(self.url, data=json.dumps(js), headers=headers).json()
        res_ = req["result"] if "result" in req.keys() else None
        #if res_ is None:
        #    print("FAIL %s --> %s\n%s" % (js, self.url, req))
        
        if res_ == "Desconocido":
            print("%s -> %s\nresult: %s" % (js, self.url, res_))
        return res_

    def connect(self, db_name, db_host, db_port, db_user_name, db_password):
        self._dbname = db_name
        self.id_ = db_user_name
        self.url = "http://%s:%s/jsonrpc" % (db_host, db_port)
        dict_ = self.create_dict("hello")
        try:
            ret = self.send_to_server(dict_)
        except Exception as exc:
            print(exc)
            return False
            
        server_found = False
        
        
        if ret[0:7] == "Welcome":
            server_found = True
        
        
        if server_found:
            self.conn_ = conn_class(db_name, self)
            
            if not self.conn_.is_valid():
                return False

        return self.conn_
    
    def existsTable(self, name): #Siempre True
        return True
    
    def mismatchedTable(self, *args):
        return False

    def __getattr__(self, name):
        return virtual_function(name, self).virtual
    
    def refreshQuery(self, curname, fields, table, where, cursor, conn):
        self.send_to_server(self.create_dict("refreshQuery", {"cursor_id": cursor.id_, "curname": "%s_%s" % (self.id_, curname), "fields": fields, "table": table, "where": where}))
    
    def refreshFetch(self, number, curname, table, cursor, fields, where_filter):
        self.send_to_server(self.create_dict("refreshFetch", {"cursor_id": cursor.id_, "curname": "%s_%s" % (self.id_, curname), "fields": fields, "table": table, "where_filter": where_filter, "number": number}))
        
    def fetchAll(self, cursor, tablename, where_filter, fields, curname):
        return self.send_to_server(self.create_dict("fetchAll", {"cursor_id": cursor.id_, "tablename": tablename, "where_filter": where_filter, "fields": fields , "curname": "%s_%s" % (self.id_, curname)}))

class virtual_function(object):
    name_ = None
    driver_ = None
    
    def __init__(self, name, driver):
        self.name_ = name
        self.driver_ = driver
        
    def virtual(self, *args):
        #return self.driver_.send_to_server(self.driver_.create_dict("%s_%s" % (self.driver_.conn_.user_name_, self.name_), args))
        return self.driver_.send_to_server(self.driver_.create_dict(self.name_, args))
        
        
        