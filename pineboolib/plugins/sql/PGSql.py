
from PyQt5.QtCore import QTime
from pineboolib.flcontrols import ProjectClass
from pineboolib import decorators 
from pineboolib.dbschema.schemaupdater import text2bool
from pineboolib.fllegacy import FLUtil
from pineboolib.fllegacy.FLSqlQuery import FLSqlQuery


try:
    import psycopg2
except ImportError:
    print(traceback.format_exc())
    print("HINT: Instale el paquete python3-psycopg2 e intente de nuevo")


class PGSql(object):
    
    version_ = None
    conn_ = None
    name_ = None
    
    def __init__(self):
        self.version_ = "0.1"
        self.conn_ = None
        self.name_ = "postGreSQL"
    
    def version(self):
        return self.version_
    
    def name(self):
        return self.name_
    
    def connect(self, db_name, db_host, db_port, db_userName, db_password):
        
        
        conninfostr = "dbname=%s host=%s port=%s user=%s password=%s connect_timeout=5" % (
                        db_name, db_host, db_port,
                        db_userName, db_password)
        self.conn_ = psycopg2.connect(conninfostr)
        return self.conn_
     
    
    
    def formatValue(self, type_, v, upper):
            
            util = FLUtil.FLUtil()
        
            s = None
            # TODO: psycopg2.mogrify ???

            if type_ == "bool" or type_ == "unlock":
                s = text2bool(v)

            elif type_ == "date":
                s = "'%s'" % util.dateDMAtoAMD(v)
                
            elif type_ == "time":
                time = QTime(s)
                s = "'%s'" % time

            elif type_ == "uint" or type_ == "int" or type_ == "double" or type_ == "serial":
                s = v

            else:
                if upper == True and type_ == "string":
                    v = v.upper()

                s = "'%s'" % v
            #print ("PNSqlDriver.formatValue(%s, %s) = %s" % (type_, v, s))
            return s

    def canOverPartition(self):
        return True
    
    @decorators.NotImplementedWarn
    def hasFeature(self, value):
        if getattr(self.conn_, value, None):
            return True
        else:
            return False
    
    
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
    def savePoint(self, number):
        pass
    
    def canSavePoint(self):
        return True
        