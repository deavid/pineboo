# -*- coding: utf-8 -*-

from pineboolib.flcontrols import ProjectClass
from pineboolib import decorators
import pineboolib
class FLSqlQuery(ProjectClass):
    """
    Implementacion de FlSqlquery de Abanq para compatibilidad con python
    """
    def __init__(self):
        self._sSELECT=""
        self._columns=[]
        self._sWHERE=""
        self._sFROM=""
        self._sORDER=""
        self.__tables=[]
        self._sTablas=""
        self._cursor=None
        self._datos=None
        self._posicion=None
        self._row=None
    
    #Establecimiento de valores
    def setSelect(self,sSELECT):
        self._sSELECT=sSELECT
        self._columns=[]
        for scolumna in self._sSELECT.split(","):
            self._columns.append(str(scolumna).strip().upper())

    def select(self):
        return self._sSELECT

    def setFrom(self,sFROM):
        self._sFROM=sFROM

    def From(self):
        return self._sFROM

    def setWhere(self,swhere):
        self._sWHERE=swhere

    def where(self):
        return self._sWHERE

    def setOrderBy(self,orderBy):
        self._sORDER=orderBy

    def orderBy(self):
        return self._sORDER

    def setTablesList(self,tablas):
        self._sTablas=tablas
        self._tables=[]
        for stable in self._sTablas.split(","):
            self._tables.append(str(stable).strip().upper())

    def sql(self):
        sSQL= "SELECT " + self._sSELECT
        if self._sFROM : 
            sSQL=sSQL + " FROM " +self._sFROM
        if self._sWHERE : 
            sSQL=sSQL + " WHERE " +self._sWHERE
        if self._sORDER : 
            sSQL=sSQL + " ORDER BY " +self._sORDER
        return str(sSQL)


    def setForwardOnly(self,valor):
        #De principio nada
        pass
    #ejecucion de consulta y scroll
    def exec(self,connection=None):
        try:
            #print(self.sql())
            micursor=self.__damecursor(connection)
            micursor.execute(self.sql())
            self._cursor=micursor
        except:
            return False
        else:
            return True 

    def exec_(self,connection=None):
        return self.exec(connection)

    def first(self):
        self._posicion=0
        if self._datos:
            self._row==self._datos[0]
            return True 
        else:
            try:
                self._row=self._cursor.fetchone()
                if self._row==None:
                    return False
                else:
                    return  True
            except:
                return False 
        
    def next(self):        
        if self._posicion is None:
            self._posicion=0            
        else:
            self._posicion+=1
        if self._datos:
            if self._posicion>=len(self._datos):
                return False
            self._row=self._datos[self._posicion]
            return True 
        else:
            try:
                self._row=self._cursor.fetchone()
                if self._row==None:
                    return False
                else:
                    return  True
            except:
                return False 
    
    def last(self):
        __cargarDatos
        if self._datos:
            self._posicion=len(self._datos)-1
            self._row=self._datos[self._posicion]
        else:
            return False

    def prev(self):
        self._posicion-=1
        if self._datos:
            if self._posicion<0:
                return False
            self._row=self._datos[self._posicion]
            return True 
        else:
            return False 


    def size(self):
        self.__cargarDatos()
        if self._datos:
            return len(self._datos)
        else:
            return 0
    #acceso valores
    def value(self,sCampo):
        i=self.__damePosDeCadena(sCampo)
        return self._row[i]

    def isNull(self,sCampo):
        i=self.__damePosDeCadena(sCampo)
        return (self._row[i]==None)



    #PRIVADAS
    def __del__(self):
        try:                        
            del self._datos
            self._cursor.close()
            del self._cursor
        except:
            pass
    
    def __cargarDatos(self):
        if self._datos:
            pass
        else:
            self._datos=self._cursor.fetchall()


    @classmethod
    def __damecursor(self ,miconnection=None):
        if miconnection:
            cursor = miconnection.cursor()
        else:
            cursor = pineboolib.project.conn.cursor()
        return cursor

    def __damePosDeCadena(self,sCampo):
        if isinstance(sCampo, int):
            return sCampo
        else:
            try:
                return self._columns.index(sCampo.strip().upper())
            except:
                try:
                    sAux=sCampo.split(".")[-1]
                except:
                    sAux=sCampo
                i=0                
                for x in self._cursor.description:
                    if x.name==sAux: 
                        return i
                    i+=1
                raise NameError("Error columna " +sCampo)



