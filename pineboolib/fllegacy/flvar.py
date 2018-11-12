# -*- coding: utf-8 -*-
from pineboolib.pncontrolsfactory import aqApp
from pineboolib.fllegacy.flsqlquery import FLSqlQuery
from pineboolib.fllegacy.flutil import FLUtil

from PyQt5 import QtCore


class FLVar(object):
    
    
    def set(self, n, v):
        id_sesion = aqApp.timeUser().toString(QtCore.Qt.ISODate)
        where = "idvar = '%s' AND idsesion ='%s'" % (n, id_sesion)

        q = FLSqlQuery()
        q.setTablesList("flvar")
        q.setSelect("id")
        q.setFrom("flvar")
        q.setWhere(where)
        q.setForwardOnly(True)
        
        if not q.exec_():
            return False
        if q.next():
            return FLUtil().sqlUpdate("flvar", "valor", str(v), "id='%s'" % str(q.value(0)))
        
        values = "%s,%s,%s" % (n, id_sesion, str(v))
        FLUtil().sqlInsert("flvar", "idvar,idsesion,idvalor", values)
        
    def get(self, n):
        id_sesion = aqApp.timeUser().toString(QtCore.Qt.ISODate)
        where = "idvar = '%s' AND idsesion ='%s'" % (n, id_sesion)
        return FLUtil().sqlSelect("flvar","valor", where, "flvar")
    
    def del_(self, n ):
        id_sesion = aqApp.timeUser().toString(QtCore.Qt.ISODate)
        where = "idvar = '%s' AND idsesion ='%s'" % (n, id_sesion)
        return FLUtil().sqlDelete("flvar", where)
    
    def clean(self):
        id_sesion = aqApp.timeUser().toString(QtCore.Qt.ISODate)
        where = "idsesion = '%s'" % id_sesion 
        return FLUtil().sqlDelete("flvar", where)
        