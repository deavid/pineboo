from pineboolib.flcontrols import ProjectClass
from pineboolib import decorators
from PyQt4 import QtGui
from pineboolib.fllegacy.FLTableMetaData import FLTableMetaData
import pineboolib



class FLSqlQuery(ProjectClass):
    
    """
    Maneja consultas con características específicas para AbanQ, hereda de QSqlQuery.

    Ofrece la funcionalidad para manejar consultas de QSqlQuery y además ofrece métodos
    para trabajar con consultas parametrizadas y niveles de agrupamiento.

    @author InfoSiAL S.L.
    """

    def __init__(self, parent = None, connectionName = "default"):
        super(FLSqlQuery, self).__init__()
        
        self.d = FLSqlQueryPrivate()
        self.d.db_ = self._prj.conn
        self.countRefQuery = self.countRefQuery + 1
        self._row = None


    def __del__(self):
        del self.d
        self.countRefQuery = self.countRefQuery - 1
        
    
    """
    Ejecuta la consulta
    """
    
    def exec(self):
        try:
            #print(self.sql())
            micursor=self.__damecursor()
            micursor.execute(self.sql())
            self._cursor=micursor
        except:
            return False
        else:
            return True 
    
    @classmethod
    def __damecursor(self):
        if self.d.db_:
            cursor = self.d.db_.cursor()
        else:
            cursor = pineboolib.project.conn.cursor()
        return cursor
    
    def __cargarDatos(self):
        if self._datos:
            pass
        else:
            self._datos=self._cursor.fetchall()
    
    
    def  exec_(self):
        return self.exec()

    """
    Añade la descripción parámetro al diccionario de parámetros.

    @param p Objeto FLParameterQuery con la descripción del parámetro a añadir
    """
    def addParameter(self, p):
        if not self.d.parameterDict_:
            self.d.parameterDict_ = {}
        
        if p:
            self.d.parameterDict_.insert(p.name(), p)

    """
    Añade la descripción de un grupo al diccionario de grupos.

    @param g Objeto FLGroupByQuery con la descripción del grupo a añadir
    """  
    def addGroup(self, g):
        if not self.d.groupDict_:
            self.d.groupDict_ = {}
        
        if g:
            self.d.groupDict_.insert(float(g.level()), g)

    """
    Tipo de datos diccionario de parametros
    """
    FLParameterQueryDict = {}

    
    """
    Tipo de datos diccionaro de grupos
    """
    FLGroupByQueryDict = {}

    """
    Para establecer el nombre de la consulta.

    @param n Nombre de la consulta
    """
    def setName(self, n):
        self.d.name_ = n
  
    """
    Para obtener el nombre de la consulta
    """
    def name(self):
        return self.d.name_
    """
    Para obtener la parte SELECT de la sentencia SQL de la consulta
    """
    def select(self):
        return self.d.select_
    """
    Para obtener la parte FROM de la sentencia SQL de la consulta
    """
    def from_(self):
        return self.d.from_

    """
    Para obtener la parte WHERE de la sentencia SQL de la consulta
    """
    def where(self):
        return self.d.where_

    """
    Para obtener la parte ORDER BY de la sentencia SQL de la consulta
    """
    def orderBy(self):
        return self.d.orderBy_

    """
    Para establecer la parte SELECT de la sentencia SQL de la consulta.

    @param  s Cadena de texto con la parte SELECT de la sentencia SQL que
            genera la consulta. Esta cadena NO debe incluir la palabra reservada
            SELECT, ni tampoco el caracter '*' como comodín. Solo admite la lista
            de campos que deben aparecer en la consulta separados por la cadena
            indicada en el parámetro 'sep'
    @param  sep Cadena utilizada como separador en la lista de campos. Por defecto
              se utiliza la coma.
    """
    
    def setSelect(self, s, sep = ","):
        
        self.d.select_ = s.strip_whitespace()
        #self.d.select_ = self.d.select_.simplifyWhiteSpace()
        
        if not sep in s and not "*" in s:
            self.d.fieldList_.clear()
            self.d.fieldList_.append(s)
            return
        
        fieldListAux = s.split(sep)
        for f in fieldListAux:
            f = f.strip_whitespace()
            
        
        table = None
        field = None
        self.d.fieldList_.clear()
        
        for f in fieldListAux:
            table = f[:f.index(".")]
            field = f[f.index(".") + 1:]
            if field == "*":
                mtd = self.d.db_.manager().metadata(table, True)
                if mtd:
                    self.d.fieldList_ = mtd.fieldList(True).split(',')
                    if not mtd.inCache():
                        del mtd
                
            else:
                self.d.fieldList_.append(f)
            
        
        self.d.select_ = ",".join(self.d.fieldList_)
        
        

    """
    Para establecer la parte FROM de la sentencia SQL de la consulta.

    @param f Cadena de texto con la parte FROM de la sentencia SQL que
           genera la consulta
    """
    def setFrom(self, f):
        self.d.from_ = f.strip_whitespace()
        #self.d.from_ = self.d.from_.simplifyWhiteSpace()

    """
    Para establecer la parte WHERE de la sentencia SQL de la consulta.

    @param s Cadena de texto con la parte WHERE de la sentencia SQL que
        genera la consulta
    """
    
    def setWhere(self, w):
        self.d.where_ = w.strip_whitespace()
        #self.d.where_ = self.d.where_.simplifyWhiteSpace()

    """
    Para establecer la parte ORDER BY de la sentencia SQL de la consulta.

    @param s Cadena de texto con la parte ORDER BY de la sentencia SQL que
           genera la consulta
    """
    
    def setOrderBy(self, w):
        self.d.orderBy_ = w.strip_whitespace()
        #self.d.orderBy_ = self.d.orderBy_.simplifyWhiteSpace()

    """
    Para obtener la sentencia completa SQL de la consulta.

    Este método une las tres partes de la consulta (SELECT, FROM Y WHERE),
    sustituye los parámetros por el valor que tienen en el diccionario y devuelve
    todo en una cadena de texto.

    @return Cadena de texto con la sentencia completa SQL que genera la consulta
    """
    def sql(self):
        for tableName in self.d.tablesList_:
            if not self.d.db_.existsTable(tableName) and not self.d.db_.createTable(tableName):
                return
        
        res = None
        
        if not self.d.from_:
            res = "SELECT %s" % self.d.select_
        elif not self.d.where_:
            res = "SELECT %s FROM %s" % (self.d.select_, self.d.from_)
        else:
            res = "SELECT %s FROM %s WHERE %s" % (self.d.select_, self.d.from_, self.d.where_)
        
        if self.d.groupDict_ and not self.d.orderBy_:
            res = res + " ORDER BY "
            initGD = None
            for gD in self.d.groupDict_:
                if not initGD:
                    res = res + gD
                    initGD = True
                else:
                    res = res + ", " + gD
            
        
        elif self.d.orderBy_:
           res = res + " ORDER BY " + self.d.orderBy_ 
        
        if self.d.parameterDict_:
            for pD in self.d.parameterDict_:
                v = pD.value()
                
                if not v:
                    ok = True
                    v = QtGui.QInputDialog.getText(QtGui.QApplication, "Entrada de parámetros de la consulta", pD.alias(),None , None)
                
                res = res.replace(pD.key(), self.d.db_.manager().formatValue(pD.type(), v))
        
        return res
                    
            

    """
    Para obtener los parametros de la consulta.

    @return Diccionario de parámetros
    """
    def parameterDict(self):
        return self.d.parameterDict_

    """
    Para obtener los niveles de agrupamiento de la consulta.

    @return Diccionario de niveles de agrupamiento
    """
    def groupDict(self):
        return self.d.groupDict_
  
    """
    Para obtener la lista de nombres de los campos.

    @return Lista de cadenas de texto con los nombres de los campos de la
          consulta
    """
    def fieldList(self):
        return self.d.fieldList_

    """
    Asigna un diccionario de parámetros, al diccionario de parámetros de la consulta.

    El diccionario de parámetros del tipo FLGroupByQueryDict , ya construido,
    es asignado como el nuevo diccionario de grupos de la consulta, en el caso de que
    ya exista un diccionario de grupos, este es destruido y sobreescrito por el nuevo.
    El diccionario pasado a este método pasa a ser propiedad de la consulta, y ella es la
    encargada de borrarlo. Si el diccionario que se pretende asignar es nulo o vacío este
    método no hace nada.

    @param gd Diccionario de parámetros
    """
    
    def setGroupDict(self, gd):
        if not gd:
            return 
        
        self.d.groupDict_ = []
        self.d.groupDict_ = gd

    """
    Asigna un diccionario de grupos, al diccionario de grupos de la consulta.

    El diccionario de grupos del tipo FLParameterQueryDict , ya construido,
    es asignado como el nuevo diccionario de parámetros de la consulta, en el caso de que
    ya exista un diccionario de parámetros, este es destruido y sobreescrito por el nuevo.
    El diccionario pasado a este método pasa a ser propiedad de la consulta, y ella es la
    encargada de borrarlo. Si el diccionario que se pretende asignar es nulo o vacío este
    método no hace nada.

    @param pd Diccionario de parámetros
    """
    
    def setParameterDict(self, pd):
        if not pd:
            return
        
        self.d.parameterDict_ = []
        self.d.parameterDict_ = pd

    """
    Este método muestra el contenido de la consulta, por la sálida estándar.

    Está pensado sólo para tareas de depuración
    """
    @decorators.NotImplementedWarn
    def showDebug(self):
        pass

    """
    Obtiene el valor de un campo de la consulta.

    Dado un nombre de un campo de la consulta, este método devuelve un objeto QVariant
    con el valor de dicho campo. El nombre debe corresponder con el que se coloco en
    la parte SELECT de la sentenica SQL de la consulta.

    @param n Nombre del campo de la consulta
    @param raw Si TRUE y el valor del campo es una referencia a un valor grande
             (ver FLManager::storeLargeValue()) devuelve el valor de esa referencia,
             en vez de contenido al que apunta esa referencia
    """
    def value(self, n, raw = False):
        if isinstance(n, str):
            n=self.__damePosDeCadena(n)
        if raw:
            return self.d.db_.fetchLargeValue(self._row[n])
        else:   
            return self._row[n]
  
  
    """
    Indica si un campo de la consulta es nulo o no

    Dado un nombre de un campo de la consulta, este método devuelve true si el campo de la consulta es nulo.
    El nombre debe corresponder con el que se coloco en
    la parte SELECT de la sentenica SQL de la consulta.

    @param n Nombre del campo de la consulta
    """
    def isNull(self,n):
        i=self.__damePosDeCadena(n)
        return (self._row[i]==None)


    """
    Devuelve el nombre de campo, dada su posicion en la consulta.

    @param p Posicion del campo en la consulta, empieza en cero y de izquierda
       a derecha
    @return Nombre del campo correspondiente. Si no existe el campo devuelve
      QString::null
    """
    def posToFieldName(self, p):
        if p < 0 or p >= len(self.d.fieldList_):
            return None
        
        return self.d.fieldList_[p]

    """
    Devuelve la posición de una campo en la consulta, dado su nombre.

    @param n Nombre del campo
    @return Posicion del campo en la consulta. Si no existe el campo devuelve -1
    """
    @decorators.NotImplementedWarn
    def fieldNameToPos(self, n):
        pass

    """
    Para obtener la lista de nombres de las tablas de la consulta.

    @return Lista de nombres de las tablas que entran a formar parte de la
        consulta
    """
    def tablesList(self):
        return self.d.tablesList_

    """
    Establece la lista de nombres de las tablas de la consulta

    @param tl Cadena de texto con los nombres de las tablas
        separados por comas, p.e. "tabla1,tabla2,tabla3"
    """
    def setTablesList(self, tl):
        self.d.tablesList_ = []
        for tabla in tl.split(","):
            self.d.tablesList_.append(tabla)

    """
    Establece el valor de un parámetro.

    @param name Nombre del parámetro
    @param v Valor para el parámetros
    """
    def setValueParam(self, name, v):
        if self.d.parameterDict_:
            self.d.parameterDict_[name] = v

    """
    Obtiene el valor de un parámetro.

    @param name Nombre del parámetro.
    """
    def valueParam(self, name):
        if self.d.parameterDict_:
            return self.d.parameterDict_[name]
        else:
            return None
  
    """
    Redefinicion del método size() de QSqlQuery
    """
    def size(self):
        self.__cargarDatos()
        if self._datos:
            return len(self._datos)
        else:
            return 0


    """
    Para obtener la lista de definiciones de campos de la consulta

    @return Objeto con la lista de deficiones de campos de la consulta
    """
    def fieldMetaDataList(self):
        if not self.d.fieldMetaDataList_:
            self.d.fieldMetaDataList_ = FLTableMetaData()
        table = None
        field = None
        for f in self.d.fieldList_:
            table = f[:f.index(".")]
            field = f[f.index(".") + 1:]
            mtd = self.d.db_.manager().metadata(table, True)
            if not mtd:
                continue
            fd = mtd.field(field)
            if fd:
                self.d.fieldMetaDataList_.insert(field.lower(), fd)
            
            if not mtd.inCache():
                del mtd
        
        return self.d.fieldMetaDataList_
    

    countRefQuery = 0

    """
    Para obtener la base de datos sobre la que trabaja
    """
    def db(self):
        return self.d.db_


    """
    Privado
    """
    d = None

    @decorators.NotImplementedWarn
    def isValid(self):
        pass
    
    @decorators.NotImplementedWarn
    def isActive(self):
        pass
    
    @decorators.NotImplementedWarn
    def at(self):
        pass
    
    @decorators.NotImplementedWarn
    def lastQuery(self):
        pass

    @decorators.NotImplementedWarn
    def numRowsAffected(self):
        pass

    @decorators.NotImplementedWarn
    def lastError(self):
        pass
    
    @decorators.NotImplementedWarn
    def isSelect(self):
        pass
    
    @decorators.NotImplementedWarn
    def QSqlQuery_size(self):
        pass
    
    @decorators.NotImplementedWarn
    def driver(self):
        pass
    
    @decorators.NotImplementedWarn
    def result(self):
        pass
    
    @decorators.NotImplementedWarn
    def isForwardOnly(self):
        pass
    
    @decorators.NotImplementedWarn
    def setForwardOnly(self, forward):
        pass

    
    @decorators.NotImplementedWarn
    def QSqlQuery_value(self, i):
        pass

    @decorators.NotImplementedWarn
    def seek(self, i, relative = False):
        pass
  
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
    
    def prev(self):
        self._posicion-=1
        if self._datos:
            if self._posicion<0:
                return False
            self._row=self._datos[self._posicion]
            return True 
        else:
            return False 

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

    def last(self):
        if self._datos:
            self._posicion=len(self._datos)-1
            self._row=self._datos[self._posicion]
        else:
            return False
    
    @decorators.NotImplementedWarn
    def prepare(self, query):
        pass

    @decorators.NotImplementedWarn
    def bindValue(self, *args):
        pass

    @decorators.NotImplementedWarn
    def addBindValue(self, *args):
        pass

    @decorators.NotImplementedWarn
    def boundValue(self, *args):
        pass
    
    
    @decorators.NotImplementedWarn
    def boundValues(self):
        pass
    
    @decorators.NotImplementedWarn
    def executedQuery(self):
        pass
    
















class FLSqlQueryPrivate():
    
    def __init__(self):
        self.name_ = None
        self.select_ = None
        self.from_ = None
        self.where_ = None
        self.orderBy_ = None
        self.parameterDict_ = []
        self.groupDict_ = []
        self.fieldMetaDataList_ = []
        self.db_ = None
    
    def __del__(self):
        self.parameterDict_ = None
        self.groupDict_ = None
        self.fieldMetaDataList_ = None

    """
    Nombre de la consulta
    """
    name_ = None

    """
    Parte SELECT de la consulta
    """
    select_ = None

    """
    Parte FROM de la consulta
    """
    from_ = None

    """
    Parte WHERE de la consulta
    """
    where_ = None

    """
    Parte ORDER BY de la consulta
    """
    orderBy_ = None

    """
    Lista de nombres de los campos
    """
    fieldList_ = []

    """
    Lista de parámetros
    """
    parameterDict_ = {}

    """
    Lista de grupos
    """
    groupDict_ = {}

    """
    Lista de nombres de las tablas que entran a formar
    parte en la consulta
    """
    tablesList_ = []

    """
    Lista de con los metadatos de los campos de la consulta
    """
    fieldMetaDataList_ = []

    """
    Base de datos sobre la que trabaja
    """
    db_ = None


