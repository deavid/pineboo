# -*- coding: utf-8 -*-

from pineboolib.fllegacy.FLTableMetaData import FLTableMetaData
from PyQt4 import QtCore
from pineboolib import decorators
from pineboolib.fllegacy.FLSqlQuery import FLSqlQuery, FLGroupByQuery
from pineboolib.fllegacy.FLFieldMetaData import FLFieldMetaData
from pineboolib.fllegacy.FLAction import FLAction
from pineboolib.utils import filedir
from lxml import etree
import os


"""
Esta clase sirve como administrador de la base de datos.

Encargada de abrir los formularios u obtener sus definiciones (ficheros .ui).
Tambien mantiene los metadatos de todas la tablas de la base de
datos, ofreciendo la posibilidad de recuperar los metadatos
mediante objetos FLTableMetaData de una tabla dada.

@author InfoSiAL S.L.
"""
class FLManager(QtCore.QObject):
    
    listTables_ = [] #Lista de las tablas de la base de datos, para optimizar lecturas
    dictKeyMetaData_ =None #Diccionario de claves de metadatos, para optimizar lecturas
    cacheMetaData_ = None #Caché de metadatos, para optimizar lecturas
    cacheAction_ = None #Caché de definiciones de acciones, para optimizar lecturas
    cacheMetaDataSys_ = None #Caché de metadatos de talblas del sistema para optimizar lecturas
    db_ = None #Base de datos a utilizar por el manejador
    initCount_ = 0 #Indica el número de veces que se ha llamado a FLManager::init()
    buffer_ = None


    
    """
    constructor
    """
    def __init__(self, db):
        super(FLManager,self).__init__()
        self.db_ = db
        self.cacheMetaData_ = []
        self.cacheAction_ = []
        self.cacheMetaDataSys_ = None
        self.listTables_ = None
        self.dictKeyMetaData_ = None
        self.initCount_ = 0
        
    """
    destructor
    """
    def __del__(self):
        self.finish()
        

    """
    Acciones de inicialización.
    """
    def init(self):
        self.initCount_ = self.initCount_ + 1
        tmpTMD = self.createSystemTable('flmetadata')
        tmpTMD = self.createSystemTable('flseqs')
        tmpTMP = self.createSystemTable('flsettings')
        
        if not self.dictKeyMetaData_:
            self.dictKeyMetaData_ = []
        
        if not self.db_.dbAux():
            return
        
        q = FLSqlQuery
        q.setSql("SELECT tabla,xml FROM flmetadata")
        if q.exec_(self.db_.dbAux()):
            while q.next():
                self.dictKeyMetaData_[q.value(0)] = q.value(1)
                
        if not self.cacheMetaData_:
            self.cacheMetaData_ = []
        
        if not self.cacheAction_:
            self.cacheAction_ = []
        
        if not self.cacheMetaDataSys_:
            self.cacheMetaDataSys_ = []
            
        
        
        
        
                
    
        
        
        
            
            
            

    """
    Acciones de finalización.
    """
    @decorators.NotImplementedWarn
    def finish(self):
        return True
    
    """
    Para obtener definicion de una tabla de la base de datos, a partir de un fichero XML.

    El nombre de la tabla corresponde con el nombre del fichero mas la extensión ".mtd"
    que contiene en XML la descripción de la tablas. Este método escanea el fichero
    y construye/devuelve el objeto FLTableMetaData correspondiente, además
    realiza una copia de estos metadatos en una tabla de la misma base de datos
    para poder determinar cuando ha sido modificados y así, si es necesario, reconstruir
    la tabla para que se adapte a la nuevos metadatos. NO SE HACEN
    CHEQUEOS DE ERRORES SINTÁCTICOS EN EL XML.

    IMPORTANTE :Para que estos métodos funcionen correctamente, es estrictamente
        necesario haber creado la base de datos en PostgreSQL con codificación
        UNICODE; "createdb -E UNICODE abanq".

    @param n Nombre de la tabla de la base de datos de la que obtener los metadatos
    @param quick Si TRUE no realiza chequeos, usar con cuidado
    @return Un objeto FLTableMetaData con los metadatos de la tabla solicitada
    """

    def metadata(self, n, quick = False):
        
        if not n:
            return None

        name = "%s" % n

         
        for metadata in self.cacheMetaData_:
            if metadata.name() ==name:
                return metadata
        
        
        self.cacheMetaData_.append(FLTableMetaData(name))
        for metadataN in self.cacheMetaData_:
            if metadataN.name() == name:
                return metadataN
            
        
                
            

    
    @decorators.NotImplementedWarn   
    def metadataDev(self, n, quick = None):
        return True

    """
    Para obtener una consulta de la base de datos, a partir de un fichero XML.

    El nombre de la consulta corresponde con el nombre del fichero mas la extensión ".qry"
    que contiene en XML la descripción de la consulta. Este método escanea el fichero
    y construye/devuelve el objeto FLSqlQuery. NO SE HACEN
    CHEQUEOS DE ERRORES SINTÁCTICOS EN EL XML.

    @param n Nombre de la consulta de la base de datos que se quiere obtener
    @return Un objeto FLSqlQuery que representa a la consulta que se quiere obtener
    """
    def query(self, n, parent = None):
        qryName = "%s.qry" % n
        qry_ = self.db_.managerModules().contentCached(qryName)
        
        if not qry_:
            return None
        
        parser_ = etree.XMLParser(
            ns_clean=True,
            encoding="UTF-8",
            remove_blank_text=True,
            )
        
        
        root_ = etree.fromstring(qry_, parser_)
        parent.setSelect(root_.xpath("select/text()")[0].strip(' \t\n\r'))
        parent.setFrom(root_.xpath("from/text()")[0].strip(' \t\n\r'))
        parent.setWhere(root_.xpath("where/text()")[0].strip(' \t\n\r'))
        orderBy_ = None
        try:
            orderBy_ = root_.xpath("order/text()")[0].strip(' \t\n\r')
            parent.setOrderBy(orderBy_)
        except:
            a = 1
            
        
        groupXml_ = root_.xpath("group")
        group_ = []
        i = 0
        while i < len(groupXml_):
            gr = groupXml_[i]
            if float(gr.xpath("level/text()")[0].strip(' \t\n\r')) == i:
                #print("LEVEL %s -> %s" % (i,gr.xpath("field/text()")[0].strip(' \t\n\r')))
                parent.addGroup(FLGroupByQuery(i,gr.xpath("field/text()")[0].strip(' \t\n\r')))
                i = i + 1
        
        
        return parent
    
    """
    Obtiene la definición de una acción a partir de su nombre.

    Este método busca en los [id_modulo].xml la acción que se le pasa
    como nombre y construye y devuelve el objeto FLAction correspondiente.
    NO SE HACEN CHEQUEOS DE ERRORES SINTÁCTICOS EN EL XML.

    @param n Nombre de la accion
    @return Un objeto FLAction con la descripcion de la accion
    """
    @decorators.Incomplete
    def action(self, n):
        if not n:
            return None
        
        name = str(n)
         
        for action in self.cacheAction_:
            if action.name() ==name:
                return action
        
        actionN = FLAction()   
        actionN.setName(name)
        actionN.setTable(name)
        self.cacheAction_.append(actionN)
        return actionN
    
    """
    Comprueba si existe la tabla especificada en la base de datos.

    @param n      Nombre de la tabla que se quiere comprobar si existe
    @param cache  Si cierto consulta primero la cache de tablas, en caso contrario
                realiza una consulta a la base para obtener las tablas existentes
    @return TRUE si existe la tabla, FALSE en caso contrario
    """
    def existsTable(self,  n, cache = True):
        
        if cache:
            modId = self.db_.managerModules().idModuleOfFile(n +".mtd")
            return os.path.exists(filedir("../tempdata/cache/%s/%s/file.mtd/%s" %(self.db_.db_name, modId, n)))
        
        
        q = FLSqlQuery()
        sql_query = "SELECT * FROM %s WHERE 1 = 1" % n
        q.setTablesList(n)
        q.setSelect("*")
        q.setFrom(n)
        q.setWhere("1 = 1 LIMIT 1")
        return q.exec_()
    
    """
    Esta función es esencialmente igual a la anterior, se proporciona por conveniencia.

    Compara los metadatos de dos tablas,  la definición en XML de esas dos tablas se
    pasan como dos cadenas de caracteres.

    @param mtd1 Cadena de caracteres con XML que describe la primera tabla
    @param mtd2 Cadena de caracteres con XML que describe la primera tabla
    @return TRUE si las dos descripciones son iguales, y FALSE en caso contrario
    """

    def checkMetaData(self, mtd1, mtd2):
        if mtd1 == mtd2:
            return True
        return False
    
    """
    Modifica la estructura o metadatos de una tabla, preservando los posibles datos
    que pueda contener.

    Según la definición existente en un momento dado de los metadatos en el fichero .mtd, este
    método reconstruye la tabla con esos metadatos sin la pérdida de información o datos,
    que pudieran existir en ese momento en la tabla.

    @param n Nombre de la tabla a reconstruir
    @param mtd1 Descripcion en XML de la vieja estructura
    @param mtd2 Descripcion en XML de la nueva estructura
    @param key Clave sha1 de la vieja estructura
    @return TRUE si la modificación tuvo éxito
    """
    @decorators.NotImplementedWarn
    def alterTable(self, mtd1 = None, mtd2 = None, key = None):
        return True
    
    """
    Crea una tabla en la base de datos.

    @param n_tmd Nombre o metadatos de la tabla que se quiere crear
    @return Un objeto FLTableMetaData con los metadatos de la tabla que se ha creado, o
      0 si no se pudo crear la tabla o ya existía
    """
    @decorators.NotImplementedWarn
    def createTable(self, n_or_tmd):
        return True
    

    
    """
    Devuelve el contenido del valor de de un campo formateado para ser reconocido
    por la base de datos actual en condiciones LIKE, dentro de la clausura WHERE de SQL.

    Este método toma como parametros los metadatos del campo definidos con
    FLFieldMetaData. Además de TRUE y FALSE como posibles valores de un campo
    lógico también acepta los valores Sí y No (o su traducción al idioma correspondiente).
    Las fechas son adaptadas al forma AAAA-MM-DD, que es el formato reconocido por PostgreSQL .

    @param fMD Objeto FLFieldMetaData que describre los metadatos para el campo
    @param v Valor que se quiere formatear para el campo indicado
    @param upper Si TRUE convierte a mayúsculas el valor (si es de tipo cadena)
    """
    @decorators.NotImplementedWarn
    def formatValueLike(self, *args, **kwargs):
        return True
    
    @decorators.NotImplementedWarn
    def formatAssignValueLike(self, *args, **kwargs):
        return True   

    
    
    """
    Devuelve el contenido del valor de de un campo formateado para ser reconocido
    por la base de datos actual, dentro de la clausura WHERE de SQL.

    Este método toma como parametros los metadatos del campo definidos con
    FLFieldMetaData. Además de TRUE y FALSE como posibles valores de un campo
    lógico también acepta los valores Sí y No (o su traducción al idioma correspondiente).
    Las fechas son adaptadas al forma AAAA-MM-DD, que es el formato reconocido por PostgreSQL .

    @param fMD Objeto FLFieldMetaData que describre los metadatos para el campo
    @param v Valor que se quiere formatear para el campo indicado
    @param upper Si TRUE convierte a mayúsculas el valor (si es de tipo cadena)
    """
    def formatValue(self, *args, **kwargs):
        if not args[0]:
            return None
        
        if len(args) == 3:
            return self.db_.formatValue(args[0], args[1], args[2])
        else:
            return self.formatValue(args[0].field(), args[1], args[2])
            
        
    
    
    def formatAssignValue(self, *args, **kwargs):
        
        
        if not args[0]:
            #print("FLManager.formatAssignValue(). Primer argumento vacio %s" % args[0])
            return "1 = 1"
        
        #print("tipo 0", type(args[0]))
        #print("tipo 1", type(args[1]))
        #print("tipo 2", type(args[2]))]
        
        if isinstance(args[0], FLFieldMetaData) and len(args) == 3:
            fMD = args[0]
            mtd = fMD.metadata()
            if not mtd:
                return self.formatAssignValue(fMD.name(), fMD.type(), args[1], args[2]) 
            
            if fMD.isPrimaryKey():
                return self.formatAssignValue(mtd.primaryKey(True), fMD.type(), args[1], args[2])
                
            fieldName = fMD.name()
            if mtd.isQuery() and not "." in fieldName:
                prefixTable = mtd.name()
                qry = self.query(mtd.query())
                    
                if qry:
                    fL = qry.fieldList()
                    
                    for f in fL:
                        prefixTable = f.section('.', 0, 0)
                        if f.section('.', 1, 1) == fieldName:
                            break
                    
                    qry.deleteLater()
                    
                fieldName.prepend(prefixTable + ".")
                      
            return self.formatAssignValue(fieldName, args[0].type(), args[1], args[2])    
                
        elif isinstance(args[1], FLFieldMetaData) and ( isinstance(args[0], str) or isinstance(args[0], QString)):
            return self.formatAssignValue(args[0], args[1].type(), args[2], args[3])
        
        elif isinstance(args[0], FLFieldMetaData) and len(args) == 2:
            return self.formatAssignValue(args[0].name(), args[0], args[1], False)
        else:
            if args[1] == None:
                return "1 = 1"

            
            formatV = self.formatValue(args[1], args[2], args[3])
            if not formatV:
                return "1 = 1"
            
            if  len(args) == 4 and args[1] == "string":
                fName = "upper(%s)" % args[0]
            else:
                fName = args[0]
            
            #print("%s=%s" % (fName, formatV))
            retorno = "%s = %s" % (fName, formatV)
            return retorno              
            
        
                              
    
    
    
    """
    Crea un objeto FLFieldMetaData a partir de un elemento XML.

    Dado un elemento XML, que contiene la descripción de un
    campo de una tabla construye y agrega a una lista de descripciones
    de campos el objeto FLFieldMetaData correspondiente, que contiene
    dicha definición del campo. Tambien lo agrega a una lista de claves
    compuesta, si el campo construido pertenece a una clave compuesta.
    NO SE HACEN CHEQUEOS DE ERRORES SINTÁCTICOS EN EL XML.

    @param field Elemento XML con la descripción del campo
    @param v Valor utilizado por defecto para la propiedad visible
    @param ed Valor utilizado por defecto para la propiedad editable
    @return Objeto FLFieldMetaData que contiene la descripción del campo
    """
    @decorators.NotImplementedWarn
    def metadataField(self, field, v = True, ed = True):
        return True
    
    """
    Crea un objeto FLRelationMetaData a partir de un elemento XML.

    Dado un elemento XML, que contiene la descripción de una
    relación entre tablas, construye y devuelve el objeto FLRelationMetaData
    correspondiente, que contiene dicha definición de la relación.
    NO SE HACEN CHEQUEOS DE ERRORES SINTÁCTICOS EN EL XML.

    @param relation Elemento XML con la descripción de la relación
    @return Objeto FLRelationMetaData que contiene la descripción de la relación
    """
    @decorators.NotImplementedWarn
    def metadataRelation(self, relation):
        return True
    
    """
    Crea un objeto FLParameterQuery a partir de un elemento XML.

    Dado un elemento XML, que contiene la descripción de una
    parámetro de una consulta, construye y devuelve el objeto FLParameterQuery
    correspondiente.
    NO SE HACEN CHEQUEOS DE ERRORES SINTÁCTICOS EN EL XML.

    @param parameter Elemento XML con la descripción del parámetro de una consulta
    @return Objeto FLParameterQuery que contiene la descrición del parámetro
    """
    @decorators.NotImplementedWarn
    def queryParameter(self, parameter):
        return True
    
    """
    Crea un objeto FLGroupByQuery a partir de un elemento XML.

    Dado un elemento XML, que contiene la descripción de un nivel de agrupamiento
    de una consulta, construye y devuelve el objeto FLGroupByQuery correspondiente.
    NO SE HACEN CHEQUEOS DE ERRORES SINTÁCTICOS EN EL XML.

    @param group Elemento XML con la descripción del nivel de agrupamiento de una consulta.
    @return Objeto FLGroupByQuery que contiene la descrición del nivel de agrupamiento
    """
    @decorators.NotImplementedWarn
    def queryGroup(self, group):
        return True
    
    """
    Crea una tabla del sistema.

    Este método lee directamente de disco el fichero con la descripción de una tabla
    del sistema y la crea en la base de datos. Su uso normal es para inicializar
    el sistema con tablas iniciales.

    @param n Nombre de la tabla.
    @return Un objeto FLTableMetaData con los metadatos de la tabla que se ha creado, o
      0 si no se pudo crear la tabla o ya existía
    """
    @decorators.NotImplementedWarn
    def createSystemTable(self, n):
        return True
    
    """
    Carga en la lista de tablas los nombres de las tablas de la base de datos
    """
    @decorators.NotImplementedWarn
    def loadTables(self):
        return True
    
    """
    Limpieza la tabla flmetadata, actualiza el cotenido xml con el de los fichero .mtd
    actualmente cargados
    """
    @decorators.NotImplementedWarn
    def cleanupMetaData(self):
        return True
    
    """
    Para saber si la tabla dada es una tabla de sistema.

    @param n Nombre de la tabla.
    @return TRUE si es una tabla de sistema
    """
    def isSystemTable(self, n):
        if not n[2:] == "fl":
            return False
        
        if n == ("flfiles","flmetadata","flmodules","flareas","flserial","flvar","flsettings","flseqs","flupdates"):
            return True
        
        return False
    
    
    """
    Utilizado para almacenar valores grandes de campos en tablas separadas indexadas
    por claves SHA del contenido del valor.

    Se utiliza para optimizar consultas que incluyen campos con valores grandes,
    como por ejemplo imágenes, para manejar en las consulta SQL la referencia al valor
    que es de tamaño constante en vez del valor en sí. Esto disminuye el tráfico al
    reducir considerablemente el tamaño de los registros obtenidos.

    Las consultas pueden utilizar una referencia y obtener su valor sólo cuando se
    necesita mediante FLManager::fetchLargeValue().


    @param mtd Metadatos de la tabla que contiene el campo
    @param largeValue Valor de gran tamaño del campo
    @return Clave de referencia al valor
    """
    @decorators.NotImplementedWarn
    def storeLargeValue(self, mtd, largeValue):
        return True
    
    """
    Obtiene el valor de gran tamaño segun su clave de referencia.

    @param refKey Clave de referencia. Esta clave se suele obtener mediante FLManager::storeLargeValue
    @return Valor de gran tamaño almacenado
    """
    def fetchLargeValue(self, refKey):
        if not refKey[0:3] == "RK@":
            return None
        q = FLSqlQuery()
        q.setSelect("contenido")
        q.setFrom("fllarge")
        q.setWhere(" refkey = '%s'" % refKey)
        if q.exec_() and q.first():
            v = q.value(0)
            del q
            return v
        
        return None
    
    """
    Uso interno. Indica el número de veces que se ha llamado a FLManager::init().
    """
    def initCount(self):
        return self.initCount_
    



    
    