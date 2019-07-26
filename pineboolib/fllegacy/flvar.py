# -*- coding: utf-8 -*-
from pineboolib.application.database.utils import sqlSelect, sqlDelete, sqlUpdate, sqlInsert
from pineboolib.fllegacy.flapplication import aqApp

from PyQt5 import QtCore  # type: ignore
from typing import Any


class FLVar(object):
    def set(self, n: str, v: Any) -> bool:
        from pineboolib.application.database.pnsqlquery import PNSqlQuery

        id_sesion = aqApp.timeUser().toString(QtCore.Qt.ISODate)
        where = "idvar = '%s' AND idsesion ='%s'" % (n, id_sesion)

        q = PNSqlQuery()
        q.setTablesList("flvar")
        q.setSelect("id")
        q.setFrom("flvar")
        q.setWhere(where)
        q.setForwardOnly(True)

        if not q.exec_():
            return False
        if q.next():
            return sqlUpdate("flvar", "valor", str(v), "id='%s'" % str(q.value(0)))

        values = "%s,%s,%s" % (n, id_sesion, str(v))
        return sqlInsert("flvar", "idvar,idsesion,idvalor", values)

    def get(self, n: str) -> Any:
        id_sesion = aqApp.timeUser().toString(QtCore.Qt.ISODate)
        where = "idvar = '%s' AND idsesion ='%s'" % (n, id_sesion)
        return sqlSelect("flvar", "valor", where, "flvar")

    def del_(self, n: str) -> bool:
        id_sesion = aqApp.timeUser().toString(QtCore.Qt.ISODate)
        where = "idvar = '%s' AND idsesion ='%s'" % (n, id_sesion)
        return sqlDelete("flvar", where)

    def clean(self) -> bool:
        id_sesion = aqApp.timeUser().toString(QtCore.Qt.ISODate)
        where = "idsesion = '%s'" % id_sesion
        return sqlDelete("flvar", where)
