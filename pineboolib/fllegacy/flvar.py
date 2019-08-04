# -*- coding: utf-8 -*-
"""
Module for FLVar.

Store user variables in database.

Those variables are per session, so they are not shared even for same user.
"""

from pineboolib.application.database.utils import sqlSelect, sqlDelete, sqlUpdate, sqlInsert
from pineboolib.fllegacy import flapplication

from PyQt5 import QtCore  # type: ignore
from typing import Any


class FLVar(object):
    """Store user variables in database."""

    def set(self, n: str, v: Any) -> bool:
        """Save a variable to database."""
        from pineboolib.application.database.pnsqlquery import PNSqlQuery

        id_sesion = flapplication.aqApp.timeUser().toString(QtCore.Qt.ISODate)
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
        """Get variable from database."""
        id_sesion = flapplication.aqApp.timeUser().toString(QtCore.Qt.ISODate)
        where = "idvar = '%s' AND idsesion ='%s'" % (n, id_sesion)
        return sqlSelect("flvar", "valor", where, "flvar")

    def del_(self, n: str) -> bool:
        """Delete variable from database."""
        id_sesion = flapplication.aqApp.timeUser().toString(QtCore.Qt.ISODate)
        where = "idvar = '%s' AND idsesion ='%s'" % (n, id_sesion)
        return sqlDelete("flvar", where)

    def clean(self) -> bool:
        """Clean variables for this session."""
        id_sesion = flapplication.aqApp.timeUser().toString(QtCore.Qt.ISODate)
        where = "idsesion = '%s'" % id_sesion
        return sqlDelete("flvar", where)
