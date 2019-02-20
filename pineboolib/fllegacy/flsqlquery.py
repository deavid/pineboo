from pineboolib import decorators
import pineboolib
import traceback
import datetime
import logging

logger = logging.getLogger(__name__)


class FLSqlQuery(object):
    """
    Maneja consultas con características específicas para AbanQ, hereda de QSqlQuery.

    Ofrece la funcionalidad para manejar consultas de QSqlQuery y además ofrece métodos
    para trabajar con consultas parametrizadas y niveles de agrupamiento.

    @author InfoSiAL S.L.
    """

    countRefQuery = 0
    invalidTables = False

    def __init__(self, name=None, connection_name=None):
        # super(FLSqlQuery, self).__init__()

        self.d = FLSqlQueryPrivate(name)
        self.d.db_ = pineboolib.project.conn.useConn(connection_name)

        self.countRefQuery = self.countRefQuery + 1
        self._row = None
        self._posicion = None
        self._datos = None
        self._cursor = None
        self.invalidTablesList = False
        self.d.select_ = None
        self.d.fieldList_ = []
        #self.d.fieldMetaDataList_ = {}

        retornoQry = None
        if name:
            retornoQry = pineboolib.project.conn.manager().query(name, self)

        if retornoQry:
            self.d = retornoQry.d

    def __del__(self):
        try:
            del self.d
            del self._datos
            self._cursor.close()
            del self._cursor
        except Exception:
            pass

        self.countRefQuery = self.countRefQuery - 1

    """
    Ejecuta la consulta
    """

    def exec_(self, sql=None):
        if self.invalidTablesList:
            return False
        if not sql:
            sql = self.sql()
        if not sql:
            return False

        sql = sql.replace(";", "")
        # micursor=self.__damecursor()
        conn = self.__dameConn()
        micursor = conn.cursor()
        try:
            micursor.execute(sql)
            self._cursor = micursor
            self._posicion = None
        except Exception:
            logger.warn("Error en consulta:\n %s", sql, stack_info=True)
            return False
        # conn.commit()

        return True

    # exec = exec_  # FIXME: En python no se puede llamar una variable "exec".

    """
    def exec_(self, sql=None, conn=None):
        if conn:
            self.d.db_ = conn
        return self.exec(sql)
    """

    @classmethod
    def __damecursor(self):
        if getattr(self.d, "db_", None):
            cursor = self.d.db_.cursor()
        else:
            cursor = pineboolib.project.conn.cursor()
        return cursor

    def __dameConn(self):
        from pineboolib.pnconnection import PNConnection
        if getattr(self.d, "db_", None):
            if isinstance(self.d.db_, PNConnection):
                conn = self.d.db_.conn
            else:
                conn = self.d.db_
        else:
            conn = pineboolib.project.conn.conn
        return conn

    def __cargarDatos(self):
        if self._datos:
            pass
        else:
            self._datos = self._cursor.fetchall()

    """
    Añade la descripción parámetro al diccionario de parámetros.

    @param p Objeto FLParameterQuery con la descripción del parámetro a añadir
    """

    def addParameter(self, p=None):
        if p is not None:
            self.d.parameterDict_[p.name()] = p

    """
    Añade la descripción de un grupo al diccionario de grupos.

    @param g Objeto FLGroupByQuery con la descripción del grupo a añadir
    """

    def addGroup(self, g):
        if not self.d.groupDict_:
            self.d.groupDict_ = {}

        if g:
            self.d.groupDict_[g.level()] = g.field()

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

    def setSelect(self, s, sep=","):
        self.d.select_ = s

        if isinstance(s, str) and sep in s:
            #s = s.replace(" ", "")
            s = s.split(sep)

        # self.d.select_ = s.strip_whitespace()
        # self.d.select_ = self.d.select_.simplifyWhiteSpace()

        if not isinstance(s, list) and not "*" == s:
            self.d.fieldList_.clear()
            self.d.fieldList_.append(s)

            return

        # fieldListAux = s.split(sep)
        # for f in s:
        #    f = str(f).strip()

        table = None
        field = None
        self.d.fieldList_.clear()

        for f in s:
            try:
                if f.startswith(" "):
                    f = f[1:]
                table = f[:f.index(".")]
                field = f[f.index(".") + 1:]
            except Exception:
                pass

            if field == "*":
                mtd = self.d.db_.manager().metadata(table, True)
                if mtd:
                    self.d.fieldList_ = mtd.fieldList(True)
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
        self.d.from_ = f
        # self.d.from_ = f.strip_whitespace()
        # self.d.from_ = self.d.from_.simplifyWhiteSpace()

    """
    Para establecer la parte WHERE de la sentencia SQL de la consulta.

    @param s Cadena de texto con la parte WHERE de la sentencia SQL que
        genera la consulta
    """

    def setWhere(self, w):
        self.d.where_ = w
        # self.d.where_ = w.strip_whitespace()
        # self.d.where_ = self.d.where_.simplifyWhiteSpace()

    """
    Para establecer la parte ORDER BY de la sentencia SQL de la consulta.

    @param s Cadena de texto con la parte ORDER BY de la sentencia SQL que
           genera la consulta
    """

    def setOrderBy(self, w):
        self.d.orderBy_ = w
        # self.d.orderBy_ = w.strip_whitespace()
        # self.d.orderBy_ = self.d.orderBy_.simplifyWhiteSpace()

    """
    Para obtener la sentencia completa SQL de la consulta.

    Este método une las tres partes de la consulta (SELECT, FROM Y WHERE),
    sustituye los parámetros por el valor que tienen en el diccionario y devuelve
    todo en una cadena de texto.

    @return Cadena de texto con la sentencia completa SQL que genera la consulta
    """

    def sql(self):
        # for tableName in self.d.tablesList_:
        #    if not self.d.db_.manager().existsTable(tableName) and not self.d.db_.manager().createTable(tableName):
        #        return

        res = None

        if not self.d.select_:
            return False

        if not self.d.from_:
            res = "SELECT %s" % self.d.select_
        elif not self.d.where_:
            res = "SELECT %s FROM %s" % (self.d.select_, self.d.from_)
        else:
            res = "SELECT %s FROM %s WHERE %s" % (
                self.d.select_, self.d.from_, self.d.where_)

        if self.d.groupDict_ and not self.d.orderBy_:
            res = res + " ORDER BY "
            initGD = None
            i = 0
            while i < len(self.d.groupDict_):
                gD = self.d.groupDict_[i]
                if not initGD:
                    res = res + gD
                    initGD = True
                else:
                    res = res + ", " + gD

                i = i + 1

        elif self.d.orderBy_:
            res = res + " ORDER BY " + self.d.orderBy_

        if self.d.parameterDict_:
            for pD in self.d.parameterDict_.keys():
                v = self.d.parameterDict_[pD]

                if not v:
                    from pineboolib.pncontrolsfactory import QInputDialog, QApplication
                    v = QInputDialog.getText(QApplication, "Entrada de parámetros de la consulta", pD, None, None)

                res = res.replace("[%s]" % pD, "\'%s\'" % v)

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

    def value(self, n, raw=None):
        pos = None
        name = None
        table_name = None
        field_name = None

        if isinstance(n, str):
            #n = n.replace(" ", "")
            pos = self.fieldNameToPos(n)
            name = n
        else:
            pos = n
            name = self.posToFieldName(pos)
        
        
        if name:
            if name.find(".") > -1 and name[0:name.find(".")] is self.tablesList():
                table_name = name[0:name.find(".")]
                field_name = name[name.find(".") + 1:]
            else:
                for t in self.tablesList():
                    mtd = self.d.db_.manager().metadata(t, True)
                    f = mtd.field(name)
                    
                    if f is not None:
                        table_name = t
                        field_name = name
                        break
        
        
        if raw is None:
            #Intentamos saber si en un valor para fllarge
            if table_name and field_name:
                field = self.d.db_.manager().metadata(table_name, True).field(field_name)
                raw  = (field.type() is "pixmap") and not self.d.db_.manager().isSystemTable(table_name)
                        
            
            

            
        if raw is True:
            return self.d.db_.manager().fetchLargeValue(self._row[pos])
        else:
            from pineboolib.qsa import Date
            
            
            try:
                retorno = self._row[pos]
            except Exception:
                retorno = None
            
            if table_name and field_name:
                #field = self.d.db_.manager().metadata(table_name, True).field(field_name)
                if field.type() == "date" and isinstance(retorno, str):
                    retorno = Date(retorno)
            
            """ TIME """
            if isinstance(retorno, datetime.time):
                retorno = str(retorno)[:8]
            
            elif isinstance(retorno, str) and retorno is not None and retorno.find(":") < retorno.find(".") and retorno.find(":") > -1:
                retorno = retorno[:retorno.find(".")]
                """ / TIME """
                
            elif isinstance(retorno, datetime.date):
                retorno = Date(str(retorno))
                
            elif retorno is not None and not isinstance(retorno, (str, int, bool, float, Date)):
                retorno = float(retorno)

            if isinstance(retorno, float):
                if retorno == int(retorno):
                    retorno = int(retorno)
                

            return retorno

    """
    Indica si un campo de la consulta es nulo o no

    Dado un nombre de un campo de la consulta, este método devuelve true si el campo de la consulta es nulo.
    El nombre debe corresponder con el que se coloco en
    la parte SELECT de la sentenica SQL de la consulta.

    @param n Nombre del campo de la consulta
    """

    def isNull(self, n):
        i = self.self.fieldNameToPos(n)
        return (self._row[i] is None)

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

    def fieldNameToPos(self, n):
        i = 0
        for field in self.d.fieldList_:
            if field.lower() == n.lower():
                return i
            i = i + 1

        return False

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
            if not pineboolib.project.conn.manager().existsTable(tabla):
                self.invalidTablesList = True

            self.d.tablesList_.append(tabla)

    """
    Establece el valor de un parámetro.

    @param name Nombre del parámetro
    @param v Valor para el parámetros
    """

    def setValueParam(self, name, v):
        self.d.parameterDict_[name] = v

    """
    Obtiene el valor de un parámetro.

    @param name Nombre del parámetro.
    """

    def valueParam(self, name):
        if name in self.d.parameterDict_.keys():
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
            self.d.fieldMetaDataList_ = {}
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
                self.d.fieldMetaDataList_[field.lower()] = fd

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

    _posicion = None

    @decorators.NotImplementedWarn
    def isValid(self):
        return True

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

    def setForwardOnly(self, forward):
        #No sirve para nada , por ahora
        pass

    @decorators.NotImplementedWarn
    def QSqlQuery_value(self, i):
        pass

    @decorators.NotImplementedWarn
    def seek(self, i, relative=False):
        pass

    def next(self):
        if not self._cursor:
            return False

        if self._posicion is None:
            self._posicion = 0
        else:
            self._posicion += 1
        if self._datos:
            if self._posicion >= len(self._datos):
                return False
            self._row = self._datos[self._posicion]
            return True
        else:
            try:
                self._row = self._cursor.fetchone()
                if self._row is None:
                    return False
                else:
                    return True
            except Exception:
                print(traceback.format_exc())
                return False

    def prev(self):
        if not self._cursor:
            return False

        self._posicion -= 1
        if self._datos:
            if self._posicion < 0:
                return False
            self._row = self._datos[self._posicion]
            return True
        else:
            return False

    def first(self):
        if not self._cursor:
            return False

        self._posicion = 0
        if self._datos:
            self._row == self._datos[0]
            return True
        else:
            try:
                self._row = self._cursor.fetchone()
                if self._row is None:
                    return False
                else:
                    return True
            except Exception:
                return False

    def last(self):
        if not self._cursor:
            return False

        if self._datos:
            self._posicion = len(self._datos) - 1
            self._row = self._datos[self._posicion]
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


class FLSqlQueryPrivate(object):
    name_ = None
    select_ = None
    from_ = None
    where_ = None
    orderBy_ = None
    groupDict_ = []

    def __init__(self, name=None):
        self.name_ = name
        self.select_ = None
        self.from_ = None
        self.where_ = None
        self.orderBy_ = None
        self.parameterDict_ = {}
        self.groupDict_ = []
        self.fieldMetaDataList_ = {}
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
    fieldMetaDataList_ = {}

    """
    Base de datos sobre la que trabaja
    """
    db_ = None


class FLGroupByQuery(object):

    level_ = None
    field_ = None

    def __init__(self, n, v):
        self.level_ = n
        self.field_ = v

    def level(self):
        return self.level_

    def field(self):
        return self.field_
