# -*- coding: utf-8 -*-

from pineboolib.fllegacy.FLFormDB import FLFormDB
from pineboolib.fllegacy.FLSqlCursor import FLSqlCursor
from pineboolib import decorators
from pineboolib.utils import DefFun
from pineboolib import project

class FLFormSearchDB( FLFormDB ):
    _accepted = None
    _cursor = None

    def __init__(self,name):
        self._cursor= FLSqlCursor(name)
        super(FLFormSearchDB,self).__init__(None,self._cursor.action())
        self._accepted = False
        

    def __getattr__(self, name): return DefFun(self, name)

    def setCursor(self, cursor):
        print("Definiendo cursor")
        self._cursor = cursor


    def setMainWidget(self):
        print("Creamos la ventana")
        

    def exec_(self, valor):
        print("Ejecutamos la ventana y esperamos respuesta, introducimos desde y hasta en cursor")

    def setFilter(self):
        print("configuramos Filtro")

    def accepted(self):
        return self._accepted

    def cursor(self):
        return self._cursor