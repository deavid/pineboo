# -*- coding: utf-8 -*-

# Completada Si
from PyQt4 import QtCore, QtGui
# from pineboolib.fllegacy.FLUtil import FLUtil
from pineboolib.fllegacy.FLSqlSavePoint import FLSqlSavePoint
from pineboolib.fllegacy.FLSqlQuery import FLSqlQuery
from pineboolib.fllegacy.FLSqlCursor import FLSqlCursor
from pineboolib.fllegacy.FLManager import FLManager
from pineboolib.fllegacy.FLManagerModules import FLManagerModules
from pineboolib.fllegacy.FLUtil import FLUtil
from pineboolib import decorators


class FLSqlDatabase():

    """
    Gestión de bases de datos.

    Proporciona una capa de abstracción para manejar distintos tipos de bases de datos.
    A través de controladores internos (drivers) específicos se gestiona el acceso a cada
    uno de los tipos de la bases de datos, ver FLSqlDriver.

    Ofrece métodos para cargar controladores, conectar a la base de datos y realizar operaciones
    específicas de forma unificada.

    El sistemas de persistencia utiliza esta clase para poder trabajar de forma homogénea sobre cualquier
    tipo de base de datos de la que exista un controlador.

    @author InfoSiAL S.L.
    """

    """
    Enumeración de opciones de conexión
    """
    """ Usuario   """
    USER = 0
    """ Contraseña   """
    PASSWORD = 1
    """ Puerto   """
    PORT = 2
    """ Servidor   """
    HOST = 3

    """
    constructor
    """
    """ Conexión principal a la base de datos actual   """
    db_ = None

    """ Usuario utilizado para conectar a la base de datos actual   """
    dbAux_ = None

    """ Nombre de la base de datos actual   """
    database_ = None

    """ Usuario utilizado para conectar a la base de datos actual   """
    user_ = None

    """ Contraseña utilizada para conectar a la base de datos actual   """
    password_ = None

    """ Dirección del servidor donde se encuentra la base de datos actual   """
    host_ = None

    """ Puerto TCP utlizado para conectar al servidor de la base de datos actual   """
    port_ = None

    """  Nombre interno del driver utilizado para conectar a la base de datos actual   """
    driverName_ = None

    """ Nombre de la conexion, ver FLSqlConnections   """
    connectionName_ = None

    """ Manejador general   """
    manager_ = None

    """ Manejador de módulos   """
    managerModules_ = None

    """ Indica si el driver de la base de datos puede interactuar con el GUI, por defecto activado   """
    interactiveGUI_ = None

    """ Indica si el driver puede lanzar excepciones a los scripts QSA, por defecto activado   """
    qsaExceptions_ = None
    
    cursorsOpened = None
    
    transaction_ = 0
    
    stackSavePoints_ = []
    queueSavePoints_ = []
    currentSavePoint_ = None
    lastActiveCursor_ = None
    
    @decorators.BetaImplementation   
    def __init__(self, *args, **kwargs):
        self.connectionName_ = "Default"
        self.setInteractiveGUI()
        self.setQsaExceptions()

        
        
        

    """
    destructor
    """
    @decorators.BetaImplementation   
    def __del__(self):
        if self.manager_:
            self.manager_.finish()
            del self.manager_
            self.manager_ = None
        
        if self.managerModules_:
            self.managerModules_.finish()
            del self.managerModules_
            self.managerModules_ = None
        
        self.closeDB()
    

    """
    @return Lista de los alias de los controladores actualmente disponibles.
    """
    @decorators.BetaImplementation   
    def driverAliases(self):
        ret = []
        list_ = ['PostgreSQL'] # FIXME a mejorar ...
        for drv in list_:
            ret.append(self.driverNameToDriverAlias(drv))
        
        return ret

    """
    @return Alias establecido por defecto
    """
    @decorators.BetaImplementation   
    def defaultAlias(self):
        return str('PostgreSQL')

    """
    @param alias Alias de un controlador
    @return Alias el nombre interno de un controlador a partir de su alias
    """
    @decorators.BetaImplementation   
    def driverAliasToDriverName(self, alias):
        return alias

    """
    @param name Nombre interno de un controlador
    @return Alias de un controlador a partir de su nombre interno
    """
    @decorators.BetaImplementation   
    def driverNameToDriverAlias(self, name):
        return name

    """
    Obtiene si un controlador necesita una opción de conexión, a partir de su alias.

    @param alias Alias del controlador
    @param connOption Tipo de opción a comprobar, del tipo enumeración FLSqlDatabase::ConnOptions
    @return True si la opción es necesaria para que el controlador pueda establecer la conexión, false en caso contrario
    """
    @decorators.BetaImplementation   
    def needConnOption(self, alias, connOption):
            return True

    """
    Obtiene el puerto de conexión usado habitualmente por un controlador

    @param alias Alias del controlador
    @return Numero de puerto
    """
    @decorators.BetaImplementation   
    def defaultPort(self, alias):
        if alias == 'PostgreSQL':
            return "5432"
        
        return None

    """
    Carga un controlador.

    @param driverName Nombre interno del controlador que se desa cargar
    @param connName Nombre de la conexion
    @return True si la carga tuvo éxito, false en caso contrario
    """
    @decorators.BetaImplementation   
    def loadDriver(self, driverName, connName = "default"):
        self.db_.addDatabase(driverName, connName + QtCore.QDateTime.currentDateTime().toString('ddMMyyyyhhmmsszzz'))
        
        self.dbAux_ = self.db_
        
        if self.db_.isOpen():
            self.db_.close()
        
        self.dbAux_.addDatabase(driverName, connName + "Aux" + QtCore.QDateTime.currentDateTime().toString('ddMMyyyyhhmmsszzz'))
        
        if self.dbAux_.isOpen():
            self.db_.close()
        
        #dr = None # FLSqlDriver        
        dr = self.db_.driver()
        dr.setFLSqlDatabase(self)
        
        dr = self.dbAux_.driver()
        dr.setFLSqlDatabase(self)
        self.driverName_ = driverName
        return True     
    

    """
  Conecta con una base de datos.

  Para poder conectar con una base de datos es imprescindible haber cargado con anterioridad el driver
  correspondiente utilizando FLSqlDatabase::loadDriver().

  A partir de la llamada a este método la base de datos actual para a ser a la que conectamos. Internamente,
  si es posible, crea dos conexiones paralelas a la misma base de datos; FLSqlDatabase::db() y FLSqlDatabase::dbAux().

  @param database Nombre de la base de datos a la que conectar
  @param user  Usuario
  @param password Contraseña
  @param host  Servidor de la base de datos
  @param port  Puerto TCP de conexión
  @param connName Nombre de la conexion
  @param connectOptions Contiene opciones auxiliares de conexión a la base de datos.
                        El formato de la cadena de opciones es una lista separada por punto y coma
                        de nombres de opción o la opción = valor. Las opciones dependen del uso del
                        driver de base de datos.
                        Si a las opciones se añade 'nogui' desactiva interactiveGUI_
                        Si a las opciones se añade 'noexceptions' desactiva qsaExceptions_
  @return True si la conexión tuvo éxito, false en caso contrario
    """
    @decorators.BetaImplementation   
    def connectDB(self, *args, **kwargs):
        if len(args) > 0:
            self.connectDB1(args)
        else:
            self.connectDB2()
    
    @decorators.BetaImplementation   
    def connectDB1(self, database, user = None, password = None, host = None, port = -1, connName = "default", connectOptions = None):
        
        if self.driverName_ is None:
            return False
        
        self.finishInternal()
        dr = self.dbAux_.driver()
        self.database_ = dr.formatDatabaseName(database)
        self.user_ = user 
        self.password_ =  password 
        self.host_ = host 
        self.port_ = port
        connOpts = self.parseConnOpts(connectOptions, self)
        self.db_.setConnectOptions(connOpts)
        self.dbAux_.setConnectOptions(connOpts)
        if dr.tryConnect(self.database_, self.user_, self.password_, self.host_, self.port_):
            self.db_.setDataBaseName(self.database_)
            self.db_.setUserName(self.user_)
            self.db_.setPassword(self.password_)
            self.db_.setHostName(self.host_)
            self.db_.setPort(self.port_)
            if not self.db_.open():
                return False

            self.dbAux_.setDataBaseName(self.database_)
            self.dbAux_.setUserName(self.user_)
            self.dbAux_.setPassword(self.password_)
            self.dbAux_.setHostName(self.host_)
            self.dbAux_.setPort(self.port_)
            if not self.dbAux_.open():
                return False  
            
            self.connectionName_ = connName
            self.initInternal()
            return True
        
        return False              
        
        

    """
  Conecta con una base de datos utilizando los datos de conexión actuales
    """
    @decorators.BetaImplementation   
    def connectDB2(self):
        if self.driverName_ is None:
            return False
      
        self.finishInternal()
        dr = self.dbAux_.driver()
        if dr.tryConnect(self.database_, self.user_, self.password_, self.host_, self.port_):
            self.db_.setDataBaseName(self.database_)
            self.db_.setUserName(self.user_)
            self.db_.setPassword(self.password_)
            self.db_.setHostName(self.host_)
            self.db_.setPort(self.port_)
            if not self.db_.open():
                return False

            self.dbAux_.setDataBaseName(self.database_)
            self.dbAux_.setUserName(self.user_)
            self.dbAux_.setPassword(self.password_)
            self.dbAux_.setHostName(self.host_)
            self.dbAux_.setPort(self.port_)
            if not self.dbAux_.open():
                return False  
            
            self.initInternal()
            return True
        
        return False     
        

    """
    Crea una tabla en la base de datos actual.

    @param tmd Metadatos con la descripción de la tabla a crear
    @return True si se pudo crear la tabla, false en caso contrario
    """
    @decorators.BetaImplementation   
    def createTable(self, *tmd):
        if self.driverName_ is None or not self.tmd or not self.dbAux_:
            return False
        
        dr = self.dbAux_.driver()
        sql = dr.createTable(tmd)
        
        if sql is None:
            return False
        
        q = FLSqlQuery() 
        if q.exec_(sql):
            print("FLManager: SQL - %s" % sql)
        
        

    """
    @return True si la base de datos actual es capaz de regenerar tablas de forma dinámica
    """
    @decorators.BetaImplementation   
    def canRegenTables(self):
        if not self.driverName_ is None or not self.dbAux_:
            return False
        
        dr = self.dbAux_.driver()
        return dr.canRegenTables()

    """
    Devuelve el contenido del valor de de un campo formateado para ser reconocido
    por la base de datos actual en condiciones LIKE, dentro de la clausura WHERE de SQL.

    Este método toma como parametros los metadatos del campo definidos con
    FLFieldMetaData. Además de TRUE y FALSE como posibles valores de un campo
    lógico también acepta los valores Sí y No (o su traducción al idioma correspondiente).
    Las fechas son adaptadas al forma AAAA-MM-DD, que es el formato reconocido por PostgreSQL .

    @param t Tipo de datos del valor
    @param v Valor que se quiere formatear para el campo indicado
    @param upper Si TRUE convierte a mayúsculas el valor (si es de tipo cadena)
    @return Valor del campo debidamente formateado
    """
    @decorators.BetaImplementation   
    def formatValueLike(self, t, v, upper = False):
        if not self.db_:
            return str(v)
        
        dr = self.db_.driver()
        return dr.formatValueLike(t,v, upper)

    """
    Devuelve el contenido del valor de de un campo formateado para ser reconocido
    por la base de datos actual, dentro de la clausura WHERE de SQL.

    Este método toma como parametros los metadatos del campo definidos con
    FLFieldMetaData. Además de TRUE y FALSE como posibles valores de un campo
    lógico también acepta los valores Sí y No (o su traducción al idioma correspondiente).
    Las fechas son adaptadas al forma AAAA-MM-DD, que es el formato reconocido por PostgreSQL .

    @param t Tipo de datos del valor
    @param v Valor que se quiere formatear para el campo indicado
    @param upper Si TRUE convierte a mayúsculas el valor (si es de tipo cadena)
    @return Valor del campo debidamente formateado
    """
    @decorators.BetaImplementation   
    def formatValue(self, t, v,upper = False):
        if not self.db_:
            return str(v)
        
        dr = self.dbAux_.driver()
        return dr.formatValue(t, v, upper)
    
    

    """
    Obtiene el siguiente valor de la secuencia para campos del tipo serial.

    @param table Nombre la tabla del campo serial
    @param field Nombre del campo serial
    @return Siguiente valor de la secuencia
    """
    @decorators.BetaImplementation   
    def nextSerialVal(self, table, field):
        if not self.db_:
            return None
        
        dr = self.dbAux_.driver()
        return dr.nextSerialVal(table, field)
    

    """
    Obtiene la posición del registro actual.

    La posición del registro actual dentro del cursor se calcula teniendo en cuenta el
    filtro actual ( FLSqlCursor::curFilter() ) y el campo o campos de ordenamiento
    del mismo ( QSqlCursor::sort() ).
    Este método es útil, por ejemplo, para saber en que posición dentro del cursor
    se ha insertado un registro.

    @param cur Cursor sobre el que calcular la posición del registro.
    @return Posición del registro dentro del cursor.
    """
    @decorators.BetaImplementation
    def atFrom(self, *cur):
        if not self.db_ or not cur:
            return None

        dr = cur.driver()

        return dr.atForm(cur)

    """
    @return Conexión principal a la base de datos actual
    """
    @decorators.BetaImplementation
    def db(self):
        return self.db_

    """
    @return Conexión auxiliar a la base de datos actual
    """
    @decorators.BetaImplementation
    def dbAux(self):
        return self.dbAux_

    """
    @return Nombre de la base de datos actual
    """
    @decorators.BetaImplementation
    def database(self):
        return self.database_

    """
    @return Usuario utilizado para conectar a la base de datos actual
    """
    @decorators.BetaImplementation
    def user(self):
        return self.user_

    """
    @return Contraseña utilizada para conectar a la base de datos actual
    """
    @decorators.BetaImplementation
    def password(self):
        return self.password_

    """
    @return Dirección del servidor donde se encuentra la base de datos actual
    """
    @decorators.BetaImplementation
    def host(self):
        return self.host_

    """
    @return Puerto TCP utlizado para conectar al servidor de la base de datos actual
    """
    @decorators.BetaImplementation
    def port(self):
        return self.port_

    """
    @return Nombre interno del driver utilizado para conectar a la base de datos actual
    """
    @decorators.BetaImplementation
    def driverName(self):
        return self.driverName_

    """
    Modifica la estructura de una tabla dada, preservando los datos. La nueva
    estructura y la vieja se pasan en cadenas de caracteres con la descripcion XML.

    @param n Nombre de la tabla a reconstruir
    @param mtd1 Descripcion en XML de la vieja estructura
    @param mtd2 Descripcion en XML de la nueva estructura
    @param key Clave sha1 de la vieja estructura
    @return TRUE si la modificación tuvo éxito
    """
    @decorators.BetaImplementation   
    def alterTable(self, mtd1, mtd2, key = None):
        if not self.db_:
            return False
        
        dr = self.dbAux_.driver()
        return dr.alterTable(mtd1, mtd2, key)
         

    """
    @return Manejador general
    """
    @decorators.BetaImplementation   
    def manager(self):
        if not self.manager_:
            self.manager_ = FLManager(self)
            self.manager_.init()
        
        return self.manager_
    """
    @return Manejador de módulos
    """
    @decorators.BetaImplementation   
    def managerModules(self):
        if not self.manager_:
            self.manager_ = FLManager(self)
            self.manager_.init()
        
        if not self.managerModules_:
            self.managerModules_ = FLManagerModules(self)
            self.managerModules_.init()
        
        return self.managerModules_

    """
    @return Nombre de la conexión
    """
    @decorators.BetaImplementation   
    def connectionName(self):
        return self.connectionName_
    

    """
    @return Si tiene capacidad para crear puntos de salvaguarda
    """
    @decorators.BetaImplementation   
    def canSavePoint(self):
        if not self.db_:
            return False
        
        dr = self.dbAux_.driver()
        return dr.canSavePoint()

    """
      Crea un punto de salvaguarda

    @param n Nombre que se le asignará al punto de salvaguarda
    @return TRUE si la acción tuvo éxito
    """
    @decorators.BetaImplementation   
    def savePoint(self, n):
        if not self.db_:
            return False
        
        dr = self.db_.driver()
        return dr.savePoint()

    """
    Libera un punto de salvaguarda

    @param n Nombre del punto de salvaguarda a liberar
    @return TRUE si la acción tuvo éxito
    """
    @decorators.BetaImplementation   
    def releaseSavePoint(self, n):
        if not self.db_:
            return False
        
        dr = self.db_.driver()
        return dr.releaseSavePoint(n)

    """
    Deshace operaciones hasta el punto de salvaguarda

    @param n Nombre del punto de salvaguarda
    @return TRUE si la acción tuvo éxito
    """
    @decorators.BetaImplementation   
    def rollbackSavePoint(self, n):
        if not self.db_:
            return False
        
        dr = self.db_.driver()
        dr.roolbackSavePint(n)

    """
    @return Si soporta transacciones
    """
    @decorators.BetaImplementation   
    def canTransaction(self):
        if not self.db_:
            return False
        
        return self.db_.driver().hasFeature("Transactions")

    """
    @return True si la base de datos soporta la sentencia OVER
    """
    @decorators.BetaImplementation   
    def canOverPartition(self):        
        if not self.db_:
            return False
        
        dr = self.dbAux_.driver()
        return dr.canOverPartition()


    """
    Ejecuta tareas de limpieza y optimización de la base de datos
    """
    @decorators.BetaImplementation   
    def Mr_Proper(self):
        if self.db_:
            dr = self.dbAux_.driver()
            dr.Mr_Proper()       

    """
    @return True si la base de datos actual puede detectar si sus transacciones están bloqueando a las de otra conexión
    """
    @decorators.BetaImplementation   
    def canDetectLocks(self):
        if not self.db_:
            return False
        
        dr = self.dbAux_.driver()
        return dr.canDetectLocks()
        

    """
    Para obtener información sobre el estado de los bloqueos existentes en la base de datos.

    Si hay bloqueos devuelve una lista de cadenas de texto en forma de registros de información. En esta lista
    la primera cadena de texto contiene los nombres de los campos de información incluidos y separados con "@",
    las siguientes cadenas son una por cada bloqueo con la información correspondiente.
    Si hay registros bloqueados produciendo situaciones de espera, se incluye información de los mismos cuando
    la cadena empieza por "##", indicando el nombre del campo clave primaria y el valor para el registro bloqueado.

    Ejemplo:

    "relation@locktype@pid"
    "stocks@RowExclusiveLock@8229"
    "##idstock=203"
    "secuencias@ExclusiveLock@8393"

    @return Lista con información de los bloqueos, si es vacia no hay bloqueos.
    """
    @decorators.BetaImplementation   
    def locksStatus(self):
        return self.detectLocks()

    """
    Comprueba si las transacciones de la base de datos actual están bloqueando a otras conexiones.

    Si hay bloqueos devuelve una lista de los mismos con el formato descrito en FLSqlDatabase::locksStatus()

    @return Lista con información de los bloqueos, si es vacia no hay bloqueos.
    """
    @decorators.BetaImplementation   
    def detectLocks(self):
        if not self.db_:
            return []
        
        dr = self.db_.driver()
        return dr.detectLocks()


    """
    Comprueba si hay riesgo de caer en un bloqueo en espera con otras conexiones.

    Si hay riesgo devuelve una lista de los bloqueos candidatos con el mismo formato descrito en FLSqlDatabase::locksStatus()

    @param  table           El nombre de una tabla para solo comprobar los riesgos sobre ella, o vacio
                          para comprobarlos en todas las tablas.
    @param  primaryKeyValue El valor de la clave primaria de un registro para solo comprobar los riesgos sobre el,
                          o vacio para comprobarlos en todos. ( No funciona con claves compuestas ).
    @return Lista con información de los bloqueos, si es vacia no hay bloqueos.
    """
    @decorators.BetaImplementation   
    def detectRisksLocks(self, table = None,primaryKeyValue = None):
        if not self.db_:
            return []
        
        dr = self.db_.driver()
        return dr.detectRiskLocks(table, primaryKeyValue)        

    """
    Regenera una tabla si su estructura actual en la base de datos difiere de la estructura definida en los metadatos
    pasados como parámetro.

    @param  n   Nombre de la tabla de la base de datos
    @param  tmd Metadatos con la descripción de la tabla
    @return True si se necesitaba regenerar la tabla y la regenación tuvo éxito
    """
    @decorators.BetaImplementation   
    def regenTable(self, n, *tmd):
        if self.driverName_ is None or not self.tmd or not self.dbAux_:
            return False
        
        dr = self.dbAux_.driver()
        return dr.regenTable(n, tmd)

    """
    Devuelve la suma md5 con el total de registros insertados, borrados y modificados en la base de datos hasta ahora

    Util para saber si la base de datos ha sido modificada desde un momento dado
    """
    @decorators.BetaImplementation   
    def md5TuplesState(self):
        if self.driverName_ is None or not self.dbAux_:
            return None
        
        dr = self.dbAux_.driver()
        return dr.md5TuplesState()

    """
    Devuelve la suma md5 con el total de registros insertados, borrados y modificados en una tabla hasta ahora

    Util para saber si una tabla ha sido modificada desde un momento dado
    """
    @decorators.BetaImplementation   
    def md5TuplesStateTable(self, table):
        if self.driverName_ is None or not self.dbAux_:
            return None
        
        dr = self.dbAux_.driver()
        return dr.md5TuplesStateTable(table)
        

    """ Ver propiedad interactiveGUI_   """
    @decorators.BetaImplementation   
    def interactiveGUI(self):
        #return interactiveGUI_ && qApp && !qApp->aqWasDeleted();
        return self.interactiveGUI_

    @decorators.BetaImplementation
    def setInteractiveGUI(self, on=True):
        self.interactiveGui_ = on
        # if self.globalAQSInterpreter:
        #     self.globalAQSInterpreter.setInteractiveGUI(self.interactiveGUI_)

    """ Ver propiedad qsaExceptions_   """
    @decorators.BetaImplementation   
    def qsaExceptions(self):
        return self.qsaExceptions_
    
    @decorators.BetaImplementation   
    def setQsaExceptions(self, on = True):
        self.qsaExceptions_ = on

    """
    Indica si la estructura de los metadatos de una tabla no coincide con la estructura de la tabla
    en la base de datos
    """
    @decorators.BetaImplementation   
    def mismatchedTable(self, table, tmd):
        if self.driverName_ is None or not self.dbAux_:
            return None
        
        dr = self.dbAux_.driver()
        return dr.mismatchedTable(table, tmd)
        

    """
    Indica si existe la tabla
    """
    @decorators.BetaImplementation   
    def existsTable(self, n):
        if self.driverName_ is None or not self.dbAux_:
            return self.tables().contains(n)
        
        dr = self.dbAux_.driver()
        return dr.existTable(n)

    """
    @return El nivel actual de anidamiento de transacciones, 0 no hay transaccion
    """
    @decorators.BetaImplementation   
    def transactionLevel(self):
        return self.transaction_

    """
    @return El último cursor activo en esta base de datos con una transacción abierta
    """
    @decorators.BetaImplementation   
    def lastActiveCursor(self):
        return self.lastActiveCursor_
    
    @decorators.BetaImplementation   
    def isOpen(self):
        if self.db_:
            return self.db_.isOpen()
        else:
            return False
    
    @decorators.BetaImplementation   
    def isOpenError(self):
        if self.db_:
            return self.db_.isopenError()
        else:
            return True
    
    @decorators.BetaImplementation   
    def tables(self, *args, **kwargs):
        if len(args) > 0:
            self.tables2(args[0])
        else:
            self.tables1()
    
    @decorators.BetaImplementation          
    def tables1(self):
        if self.db_:
            return self.db_.tables()
        else:
            return []
    
    @decorators.BetaImplementation   
    def tables2(self, type_):
        if self.db_:
            return self.db_.tables(type_)
        else:
            return []
        
    @decorators.BetaImplementation      
    def lastError(self):
        if self.db_:
            return self.db_.lastError()
        else:
            return None
    
    @decorators.BetaImplementation   
    def connectOptions(self):
        if self.db_:
            return self.db_.connecOptions()
        else:
            return None
  

    """
  Cierra la conexión actual de la base de datos
    """
    @decorators.BetaImplementation   
    def closeDB(self):
        self.finishInternal()
        if self.driverName_ is None:
            return
        
        if self.dbAux_:
            self.dbAux_.close()
        
        if self.db_:
            self.db_.close()



    @decorators.BetaImplementation   
    def doTransaction(self, cur):
        #if not cur or not self.db_ or not aqApp or not qApp: #FIXME
        if not cur:
            return False
        
        if self.transaction_ == 0  and self.canTransaction():
            #aqApp.statusHelpMsg(FLUtil.translate("app", "Iniciando transacción")) #FIXME
            if self.db_.transaction():
                self.lastActiveCursor_ = cur
                #aqApp.emitTransactionBegin(cur) #FIXME
                if not self.canSavePoint():
                    if self.currentSavePoint_:
                        del self.currentSavePoint_
                        self.currentSavePoint_ = None
                    
                    self.stackSavePoints_ = []
                    self.queueSavePoints_ = []
                
                ++self.transaction_
                cur.d.transactionsOpened_.append(self.transaction_)
                return True
            else:
                print("FLSqlDatabase::doTransaction : Fallo al intentar iniciar transacción")
                return False
        
        else:
            #aqApp.statusHelpMsg(FLUtil.translate("app", Creando punto de salvaguarda %s..." % self.transaction_))
            if not self.canSavePoint():
                if self.transaction_ == 0:
                    if self.currentSavePoint_:
                        del self.currentSavePoint_
                        self.currentSavePoint_ = 0
                    
                    self.stackSavePoints_ = []
                    self.queueSavePoints_ = []
                
                if self.currentSavePoint_:
                    self.stackSavePoints_.append(self.currentSavePoint_)
                self.currentSavePoint_ = FLSqlSavePoint(self.transaction_)
            else:
                self.savePoint(int(self.transaction_))
            ++self.transaction_
            cur.d.transactionsOpened_.append(self.transaction_)
            return True
                
                
                

    @decorators.BetaImplementation       
    def doCommit(self, cur,notify = True):
        #if not cur or not aqApp or not qApp: #FIXMME
        if not cur:
        
            return False
        
        if not notify:
            self.emit(cur.autocommit())
        
        if self.transaction_ > 0:
            if not cur.d.transactionsOpened_ == []:
                trans = cur.d.transactionsOpened_.pop()
                if not trans == self.transaction_:
                    print(FLUtil.translate("app","FLSqlDatabase : El cursor va a terminar la transacción %s pero la última que inició es la %s" % (self.transaction_, trans)))
            
            else:
                print(FLUtil.translate("app","FLSqlDatabase : El cursor va a terminar la transacción %s pero no ha iniciado ninguna" % self.transaction_))
            
            self.transaction_ = self.transaction_ -1
        else:
            return True
        
        if self.transaction_ == 0 and self.canTransaction():
            #aqApp->statusHelpMsg(qApp->tr("Terminando transacción...")); #FIXME
            if self.db_.commit():
                self.lastActiveCursor_ = None
                if not self.canSavePoint():
                    if self.currentSavePoint_:
                        del self.currentSavePoint_
                        self.currentSavePoint_ = None
                    self.stackSavePoints_.clear()
                    self.queueSavePoints_.clear()
                
                if notify:
                    cur.d.modeAccess_ = FLSqlCursor.BROWSE 
                
                #aqApp.emitTransactionEnd(cur)
                cur.d.md5Tuples_ = self.db_.md5TuplesStateTable(cur.d.curName_)
                return True
            else:
                print(FLUtil.translate("app","FLSqlDatabase::doCommit : Fallo al intentar terminar transacción"))
                return False
        else:
            #aqApp->statusHelpMsg(qApp->tr("Liberando punto de salvaguarda %1...").arg(transaction_)); 
            if (self.transaction_ == 1 and self.canTransaction()) or (self.transaction_ == 0 and not self.canTransaction()):
                if not self.canSavePoint():
                    if self.currentSavePoint_:
                        del self.currentSavePoint_
                        self.currentSavePoint_ = None
                    self.stackSavePoints_.clear()
                    self.queueSavePoints_.clear()
                else:
                    self.releaseSavePoint(self.transaction_)
                if notify:
                    cur.d.modeAccess_ = FLSqlCursor.BROWSE
                return True
            
            if not self.canSavePoint():
                for tempSavePoint in self.queueSavePoints_:
                    tempSavePoint.setId(self.transaction_ - 1)
                
                if self.currentSavePoint_:
                    self.queueSavePoints_.append(self.currentSavePoint_)
                    self.currentSavePoint_ = None
                    if not self.stackSavePoints_ == []:
                        self.currentSavePoint_ = self.stackSavePoints_.pop()
                
                else:
                    self.releaseSavePoint(self.transaction_)
                if notify:
                    cur.d.modeAccess_ = FLSqlCursor.BROWSE
                return True

    @decorators.BetaImplementation   
    def doRollback(self, cur):
        #if not cur or not self.db_ or not aqApp or not qApp: #FIXME
        if not cur:
            return False
        
        cancel = False
        if self.interactiveGUI() and (cur.d.modeAccess() == FLSqlCursor.INSERT or cur.d.modeAccess_ == FLSqlCursor.EDIT) and cur.isModifiedBuffer() and cur.d.askForCancelChanges_:
            res = QtGui.QMessageBox.information(self,FLUtil.translate("app","Cancelar cambios"),FLUtil.translate("app","Todos los cambios efectuados se cancelarán.¿Está seguro?"),
                                           QtGui.QMessageBox.Yes, QtGui.QMessageBox.No | QtGui.QMessageBox.Default | QtGui.QMessageBox.Escape)
            if res == QtGui.QMessageBox.No:
                return False
            cancel = True
        
        if self.transaction_ > 0:
            if not cur.d.transactionsOpened_ == []:
                trans = cur.d.transactionsOpened_.pop()
                if not trans == self.transaction_:
                    print(FLUtil.translate("app","FLSqlDatabase : El cursor va a deshacer la transacción %s pero la última que inició es la %s" % (self.transaction_, trans)))
            else:
                print(FLUtil.translate("app","FLSqlDatabase : El cursor va a deshacer la transacción %1 pero no ha iniciado ninguna" % self.transaction_))
            self.transaction_ = self.transaction_ -1
        else:
            return True
            
        
        if self.transaction_ == 0 and self.canTransaction():
            #aqApp->statusHelpMsg(qApp->tr("Deshaciendo transacción...")); #FIXME
            if self.db_.rollback():
                self.lastActiveCursor_ = None
            
                if not self.canSavePoint():
                    if self.currentSavePoint_:
                        del self.currentSavePoint_
                        self.currentSavePoint_ = None
                
                    self.stackSavePoints_.clear()
                    self.queueSavePoints_.clear()
            
                cur.d.modeAccess_ = FLSqlCursor.BROWSE 
                if cancel:
                    cur.select()
            
                #aqApp->emitTransactionRollback(cur);
                return True
        
            else:
                print(FLUtil.translate("app","FLSqlDatabase::doRollback : Fallo al intentar deshacer transacción"))
                return False
        
        else:
            #aqApp->statusHelpMsg(qApp->tr("Restaurando punto de salvaguarda %1...").arg(transaction_));
            if not self.canSavePoint():
                for tempSavePoint in self.queueSavePoints_:
                    tempId = tempSavePoint.id()
                    if tempId > self.transaction_ or self.transaction_ == 0:
                        tempSavePoint.undo()
                        del tempSavePoint
                    else:
                        self.queueSavePoints_
                    
                if self.currentSavePoint_:
                    self.currentSavePoint_.undo()
                    del self.currentSavePoint_
                    self.currentSavePoint_ = None
                    if not self.stackSavePoints_ == []:
                        self.currentSavePoint_ = self.stackSavePoints_.pop()
                
                if self.transaction_ == 0:
                    if self.currentSavePoint_:
                        del self.currentSavePoint_
                        self.currentSavePoint_ = None
                    self.stackSavePoints_.clear()
                    self.queueSavePoints_.clear()
            else:
                self.rollbackSavePoint(self.transaction_)
            cur.d.modeAccess_ = FLSqlCursor.BROWSE
            return True
        
    @decorators.BetaImplementation   
    def initInternal(self):
        self.currentSavePoint_ = None
        self.lastActiveCursor_ = None
        if self.stackSavePoints_ and not self.canSavePoint():
            self.stackSavePoints_ = FLSqlSavePoint()
            self.stackSavePoints_.setAutoDelete(True)
        
        if not self.queueSavePoints_ and not self.canSavePoint():
            self.queueSavePoints_ = FLSqlSavePoint()
            self.queueSavePoints_.setAutoDelete(True)

    @decorators.BetaImplementation       
    def finishInternal(self):
        if self.transaction_ > 0:
            if self.lastActiveCursor_:
                text = "Se han detectado transacciones no finalizadas en la última operación.\nSe van a cancelar las transacciones pendientes.\nLos últimos datos introducidos no han sido guardados, por favor\nrevise sus últimas acciones y repita las operaciones que no\nse han guardado.\nSqlDatabase::finishInternal: %s\n" % self.lastActiveCursor_.d.curName_
                self.lastActiveCursor_.rollbackOpened(-1,text)
            
            if self.db_ and self.transaction_ > 0:
                self.db_.rollback()
            
            self.transaction_ = 0
        
        if self.stackSavePoints_:
            self.stackSavePoints_ = []
        
        if self.queueSavePoints_:
            self.queueSavePoints_ = []
        
        self.currentSavePoint_ = None
        self.lastActiveCursor_ = None