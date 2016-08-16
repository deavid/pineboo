# -*- coding: utf-8 -*-

from pineboolib.flcontrols import ProjectClass
from pineboolib import decorators
from pineboolib.fllegacy.FLSqlQuery import FLSqlQuery
from pineboolib.utils import DefFun
from pineboolib.fllegacy.FLUtil import FLUtil

from PyQt4 import QtCore,QtGui
from PyQt4.QtCore import QString, QVariant

from pineboolib.fllegacy.FLTableMetaData import FLTableMetaData

from pineboolib.CursorTableModel import CursorTableModel
from pineboolib.fllegacy.FLFieldMetaData import FLFieldMetaData

class Struct(object):
    pass

class PNBuffer(ProjectClass):
    
    fieldList_ = None
    cursor_ = None
    clearValues_ = False
    
    
    def __init__(self, cursor):
        super(PNBuffer,self).__init__()    
        self.cursor_ = cursor
        self.fieldList_ = []
        campos = self.cursor_.db_.manager().metadata(self.cursor_.curName_).fieldListObject()
        for campo in campos:
            field = Struct()
            field.name = campo.name()
            field.value = None
            field.type_ = campo.type()
            self.fieldList_.append(field)
    
    def primeUpdate(self):
        for field in self.fieldList_:
            #field.value = self.convertToType(self.cursor_._model.value(self.cursor_._currentregister, field.name), field.type_)
            field.value = self.cursor_._model.value(self.cursor_._currentregister, field.name)
            
            #print("%s->%s" %(field.name, field.value))
    
    def setNull(self, name):
        for field in  self.fieldList_:
            if field.name == str(name):
                field.value = None
    
    def isGenerated(self, name):
        return self.cursor_.db_.manager().metadata(self.cursor_.curName_).field(name).generated()
    

    def clearValues(self, b):
        if b:
            for field in  self.fieldList_:
                field.value = None
        
    
    def isEmpty(self):
        if len(self.fieldList_) <= 0:
            return True
        else:
            return False
    
    def isNull(self, name):
        for field in  self.fieldList_:
            if field.name == str(name):
                if not field.value:
                    #print("PNBuffer.isNull(True)")
                    return True
                else:
                    return False
        
        return True
    
    def value(self, name):
        for field in  self.fieldList_:
            if field.name == str(name):
                #print("PNBuffer.value(%s) = %s" % (name, field.value) )
                if field.value is None:
                    return None
                else:
                    return field.value
        
        return QVariant()
        
                
    def convertToType(self, value, fltype):
        _type = None
        
        #print("Recogiendo %s tipo(%s) para convertir a fltype %s " % (value, type(value), fltype))
        
        if value is None:
            #print("Retornando %s vacio" % fltype)
            return ""
        """

        if fltype == "int":
            _type = value.toInt()
        elif fltype == "serial" or fltype == "uint":
            _type = value.toUInt()
        elif fltype == "bool" or fltype == "unlock":
            _type = value.toBool()
        elif fltype == "double":
            _type = value.toDouble()
        elif fltype ==  "time":
            _type = value.toTime()
        elif fltype == "date":
            _type = value.toDate()
        elif fltype == "string" or fltype == "pixmap" or fltype == "stringList":
            _type = value.toString()
        elif fltype == "bytearray":
            _type = value.toByteArray()
        """    
        #print("Retornando =", value)
        
        return value
           


class FLSqlCursorPrivate(QtCore.QObject):

    """
    Buffer con un registro del cursor.

    Según el modo de acceso FLSqlCursor::Mode establecido para el cusor, este buffer contendr
    el registro activo de dicho cursor listo para insertar,editar,borrar o navegar.
    """
    buffer_ = None
     
    """
    Copia del buffer.

    Aqui se guarda una copia del FLSqlCursor::buffer_ actual mediante el metodo FLSqlCursor::updateBufferCopy().
    """    
    bufferCopy_ = None
        
    """
    Metadatos de la tabla asociada al cursor.
    """        
    metadata_ = None
        
    """
    Mantiene el modo de acceso actual del cursor, ver FLSqlCursor::Mode.
    """
    modeAccess_ = None
        
    """
    Cursor relacionado con este.
    """
    cursorRelation_ = None
        
    """
    Relación que determina como se relaciona con el cursor relacionado.
    """
    relation_ = None
        
    """
    Esta bandera cuando es TRUE indica que se abra el formulario de edición de regitros en
    modo edición, y cuando es FALSE se consulta la bandera FLSqlCursor::browse. Por defecto esta
    bandera está a TRUE
    """
    edition_ = True
        
    """
    Esta bandera cuando es TRUE y la bandera FLSqlCuror::edition es FALSE, indica que se
    abra el formulario de edición de registro en modo visualización, y cuando es FALSE no hace
    nada. Por defecto esta bandera está a TRUE
    """
    browse_ = True
    browseStates_ = []
        
    """
    Filtro principal para el cursor.

    Este filtro persiste y se aplica al cursor durante toda su existencia,
    los filtros posteriores, siempre se ejecutaran unidos con 'AND' a este.
    """
    mainFilter_ = None
        
    """
    Accion asociada al cursor, esta accion pasa a ser propiedad de FLSqlCursor, que será el
    encargado de destruirla
    """
    action_ = None
        
    """
    Cuando esta propiedad es TRUE siempre se pregunta al usuario si quiere cancelar
    cambios al editar un registro del cursor.
    """
    askForCancelChanges_ = False
        
    """
    Indica si estan o no activos los chequeos de integridad referencial
    """
    activatedCheckIntegrity_ = True
        
    """
    Indica si estan o no activas las acciones a realiar antes y después del Commit
    """
    activatedCommitActions_ = True
        
    """
    Contexto de ejecución de scripts.

    El contexto de ejecución será un objeto formulario el cual tiene asociado un script.
    Ese objeto formulario corresponde a aquel cuyo origen de datos es este cursor.
    El contexto de ejecución es automáticamente establecido por las clases FLFormXXXX.
    """
    ctxt_ = None
        
    """
    Crónometro interno
    """
    timer_ = None
        
    """
    Cuando el cursor proviene de una consulta indica si ya se han agregado al mismo
    la definicón de los campos que lo componen
    """
    populated_ = False
        
    """
    Cuando el cursor proviene de una consulta contiene la sentencia sql
    """
    query_ = None
        
    """
    Cuando el cursor proviene de una consulta contiene la clausula order by
    """
    queryOrderBy_ = None
        
    """
    Base de datos sobre la que trabaja
    """
    db_ = None
        
    """
    Pila de los niveles de transacción que han sido iniciados por este cursor
    """
    transactionsOpened_ = []
        
    """
    Filtro persistente para incluir en el cursor los registros recientemente insertados aunque estos no
    cumplan los filtros principales. Esto es necesario para que dichos registros sean válidos dentro del
    cursor y así poder posicionarse sobre ellos durante los posibles refrescos que puedan producirse en
    el proceso de inserción. Este filtro se agrega a los filtros principales mediante el operador OR.
    """
    persistentFilter_ = None
        
    """
    Cursor propietario
    """
    cursor_ = None
        
    """
    Nombre del cursor
    """
    curName_ = None

    
    """
    Auxiliares para la comprobacion de riesgos de bloqueos
    """
    inLoopRisksLocks_ = False
    inRisksLocks_ = False
    modalRisksLocks_ = None
    timerRisksLocks_ = None
    
    """
    Para el control de acceso dinámico en función del contenido de los registros
    """
    
    acTable_ = None
    acPermTable_ = None
    acPermBackupTable_ = None
    acosTable_ = None
    acosBackupTable_ = None
    acosCondName_ = None
    acosCond_ = None
    acosCondVal_ = None
    lastAt_ = None
    aclDone_ = None
    fieldsNamesUnlock_ = None
    idAc_ = None
    idAcos_ = None
    idCond_ = None
    id_ = None
    
    """ Uso interno """
    isQuery_ = None
    isSysTable_ = None
    mapCalcFields_ = None
    rawValues_ = None
    
    md5Tuples_ = None
    
    countRefCursor = None
    
    _model = None
    
    _currentregister = None
    editionStates_ = None
    
    _current_changed = QtCore.pyqtSignal(int)
    
    def __init__(self):
        super(FLSqlCursorPrivate,self).__init__()
        self.metadata_ = None
        self.countRefCursor = 0
        self.currentRegister = -1
        self.acosCondName_ = QString()
        

        
        
    def __del__(self):
        
        if self.metadata_:
            self.undoAcl()
        
        if self.bufferCopy_:
            del self.bufferCopy_
        
        if self.relation_:
            del self.relation_
        
        if self.acTable_:
            del self.acTable_
        
        if self.editionStates_:
            del self.editionStates_
            print("AQBoolFlagState count", self.count_)
            
        if self.browseStates_:
            del self.browseStates_
            print("AQBoolFlagState count", self.count_)
    
    @decorators.NotImplementedWarn
    def doAcl(self):
        return True
    
    @decorators.NotImplementedWarn
    def undoAcl(self):
        return True
    
    @decorators.NotImplementedWarn
    def needUpdate(self):
        return False
    
        if self.isQuery_:
            return False
        
        md5Str = QString(self.db_.md5TuplesStateTable(self.curName_))
        
        if md5Str.isEmpty():
            return False
        
        if self.md5Tuples_.isEmpty():
            self.md5Tuples_ = md5Str
            return True
        
        need = False
        
        if not md5Str == self.md5Tuples_:
            need = True
            
        self.md5Tuples_ = md5Str
        return need
      

        
class FLSqlCursor(ProjectClass):
    
    """ 
    Insertar, en este modo el buffer se prepara para crear un nuevo registro 
    """    
    Insert = 0
    
    """ 
    Edición, en este modo el buffer se prepara para editar el registro activo 
    """
    Edit = 1
    
    """ 
    Borrar, en este modo el buffer se prepara para borrar el registro activo 
    """
    Del = 2
    
    """ 
    Navegacion, en este modo solo se puede visualizar el buffer 
    """
    Browse = 3
    
    """ 
    evalua un valor fijo 
    """
    Value = 0
    
    """ 
    evalua una expresion regular 
    """
    RegExp = 1
     
    """ 
    evalua el valor devuelto por una funcion de script 
    """
    Function = 2
    
    _selection = None
    
    
    
    
    def __init__(self, name , autopopulate = True, connectionName_or_db = None, cR = QString(), r = None , parent = None):
        super(FLSqlCursor,self).__init__()
        self._valid = False 
        self.d = FLSqlCursorPrivate()
        nameCursor = name + QtCore.QDateTime.currentDateTime().toString("ddMMyyyyhhmmsszzz") + "-K"
        
        if connectionName_or_db is None:
            #print("Init1") # si soy texto y estoy vacio
            self.d.db_ = self._prj.conn
        elif isinstance(connectionName_or_db, QString) or isinstance(connectionName_or_db, str):
            #print("Init2 ")
            self.d.db_ = self._prj.conn
        else:
            #print("Init3", connectionName_or_db)
            self.d.db_ = connectionName_or_db
        
        self.init(name, autopopulate, cR, r)
        
            
        
    
    """
    Código de inicialización común para los constructores
    """
    def init(self, name, autopopulate, cR, r):
        #print("FLSqlCursor(%s): Init()" % name)
        
        #if self.d.metadata_ and not self.d.metadata_.aqWasDeleted() and not self.d.metadata_.inCache():
        
        self.d.curName_ = name
        if self.setAction(self.d.curName_):
            self.d.countRefCursor = self.d.countRefCursor + 1
        else:
            print("FLSqlCursor(%s).init(): ¿La tabla no existe?" % name)
            return None
            
       
        #if not name.isEmpty():
        #    if not self.d.db_.manager().existsTable(name):
        #        self.d.metadata_ = self.d.db_.manager().createTable(name)
        #    else:
        #        self.d.metadata_ = self.d.db_.manager().metadata(name)
        self.d.cursorRelation_ = cR
        if r: # FLRelationMetaData
            if self.d.relation_ and self.d.relation_.deref():
                del self.d.relation_
            
            #r.ref()
            self.d.relation_ = r
        else:
            self.d.relation_ = None
            
        if not self.metadata():
            return
        
        #self.d.fieldsNamesUnlock_ = self.d.metadata_.fieldsNamesUnlock()
        self.d.isQuery_ = self.metadata().isQuery()
        if (name[len(name)-3:]) == "sys" or self.db().manager().isSystemTable(name):
            self.d.isSysTable_ = True
        else:
            self.d.isSysTable_ = False
        
        if self.d.isQuery_: 
            qry = self.d.db_.manager().query(self.d.metadata_.query(), self)
            self.d.query_ = qry.sql()
            if qry and not self.d.query_.isEmpty():
                self.exec(self.d.query_)
            if qry:
                self.qry.deleteLater()
        else:
            self.setName(self.metadata().name(), autopopulate)
        
        if self.d.modeAccess_ == self.Browse:
            if cR and r:
                try:
                    cR.bufferChanged.disconnect(self.refresh)
                except:
                    a = 1
                    
                cR.bufferChanged.connect(self.refresh)
                try:
                    cR.newBuffer.disconnect(self.clearPersistentFilter)
                except:
                    a = 1
                cR.newBuffer.connect(self.clearPersistentFilter)
        else:
            self.seek(None)
        
        if self.d.timer_:
            del self.d.timer_
        
        self.d.timer_ = QtCore.QTimer(self)
        self.d.timer_.timeout.connect(self.refreshDelayed)
        self.d.md5Tuples_ = self.db().md5TuplesStateTable(self.d.curName_)
        
               
            
            
    def __getattr__(self, name): return DefFun(self, name)    
        
    
    def setName(self, name, autop):
        self.name = name
        #autop = autopopulate para que??
    
    """
    Para obtener los metadatos de la tabla.

    @return Objeto FLTableMetaData con los metadatos de la tabla asociada al cursor
    """
    def metadata(self): 
        if not self.d.metadata_:
            print("FLSqlCursor(%s) Esta devolviendo un metadata vacio" % self.d.curName_)
        return self.d.metadata_

    """
    Para obtener el modo de acceso actual del cursor.

    @return Constante FLSqlCursor::Mode que define en que modo de acceso esta preparado
        el buffer del cursor
    """
    def modeAccess(self): 
        return self.d.modeAccess_
    
    """
    Para obtener el filtro principal del cursor.

    @return Cadena de texto con el filtro principal
    """
    def mainFilter(self):
        return self.d.mainFilter_
    

    """
    Para obtener la accion asociada al cursor.

    @return  Objeto FLAction
    """
    def action(self):
        return self._action
    
    def actionName(self):
        return self.d.curName_

    """
    Establece la accion asociada al cursor.

    @param a Objeto FLAction
    """
    def setAction(self, a):
        if isinstance(a, str) or isinstance(a, QString):
            #print("FLSqlCursor(%s): setAction(%s)" % (self.d.curName_, a)) 
            try:
                self._action = self._prj.actions[str(a)]
            except KeyError:
                #print("FLSqlCursor.setAction(): Action no encontrada : %s en %s actions. Es posible que la tabla no exista" % (a, len(self._prj.actions)))
                return False
            #self._action = self._prj.actions["articulos"]

            if self._action.table:
                self.d._model = CursorTableModel(self._action, self._prj)
                self._selection = QtGui.QItemSelectionModel(self.d._model)
                self._selection.currentRowChanged.connect(self.selection_currentRowChanged)
                self._currentregister = self._selection.currentIndex().row()
                self.d.metadata_ = self.db().manager().metadata(self._action.table)
            else:
                return False
            self.d.activatedCheckIntegrity_ = True
            self.d.activatedCommitActions_ = True
            return True
        else:
            self.d.action_ = a

    """
    Establece el filtro principal del cursor.

    @param f Cadena con el filtro, corresponde con una clausura WHERE
    @param doRefresh Si TRUE tambien refresca el cursor
    """
    def setMainFilter(self, f, doRefresh = True):
        self.d.mainFilter_ = f
        if doRefresh:
            self.refresh()
        

    """
    Establece el modo de acceso para el cursor.

    @param m Constante FLSqlCursor::Mode que indica en que modo de acceso
    se quiere establecer el cursor
    """
    def setModeAccess(self, m):
        self.d.modeAccess_ = m
        

    """
    Devuelve el nombre de la conexión que el cursor usa

    @return Nombre de la conexión
    """
    
    def connectionName(self):
        return self.d.db_.connectionName()
        

    """
    Establece el valor de un campo del buffer de forma atómica y fuera de transacción.

    Invoca a la función, cuyo nombre se pasa como parámetro, del script del contexto del cursor
    (ver FLSqlCursor::ctxt_) para obtener el valor del campo. El valor es establecido en el campo de forma
    atómica, bloqueando la fila durante la actualización. Esta actualización se hace fuera de la transacción
    actual, dentro de una transacción propia, lo que implica que el nuevo valor del campo está inmediatamente
    disponible para las siguientes transacciones.

    @param fN Nombre del campo
    @param functionName Nombre de la función a invocar del script
    """
    @decorators.NotImplementedWarn
    def setAtomicValueBuffer(self, fN, functionName):
        return True
    
    """
    Establece el valor de un campo del buffer con un valor.

    @param fN Nombre del campo
    @param v Valor a establecer para el campo
    """
    @decorators.NotImplementedWarn
    def setValueBuffer(self, fN, v):
        return True

    """
    Devuelve el valor de un campo del buffer.

    @param fN Nombre del campo
    """

    def valueBuffer(self, fN):
        fN = str(fN)
        if self.d.rawValues_:
            return self.valueBufferRaw(fN)
        
        if not self.d.buffer_ or self.d.buffer_.isEmpty() or not self.metadata():
            return QVariant()
        
        field = self.metadata().field(fN)
        if not field:
            print("FLSqlCursor::valueBuffer() : No existe el campo %s:%s" % (self.metadata().name(), fN))
            return QVariant()
        
        type_ = field.type()
        fltype = field.flDecodeType(type_)
        if self.d.buffer_.isNull(fN):
            if type_ == "double" or type_ == "int" or type_ == "uint":
                return 0
        
        v = QVariant()    
        if field.outTransaction() and self.d.db_.dbAux() and not self.d.db_.db() == self.d.db_.dbAux() and not self.d.modeAccess_ == self.Insert: 
            pK = self.d.metadata_.primaryKey()
            if pK:
                print("valueBuffer:soy PK")
                pKV = self.d.buffer_.value(pK)
                q = FLSqlQuery()
                sql_query = "SELECT %s FROM %s WHERE %s" % (fN, self.d.metadata.name() , self.d.db_.manager().formatAssignValue(self.d.metadata_.field(pK), pKV))
                q.setSql(sql_query)
                q.exec_(self.d.db_.dbAux())
                if q.next():
                    v = q.value(0)
            else:
                print("FLSqlCursor : No se puede obtener el campo fuera de transaccion, porque no existe clave primaria")
            
        else:
            v = self.d.buffer_.value(fN)    
            #print("FLSqlCursor.valueBuffer(%s) = %s" % (fN, v))        
        #if v.isValid():
            #v.cast(fltype)
        
        if not v is None and type_ == "pixmap":
            vLarge = QVariant(self.d.db_.manager().fetchLargeValue(v.toString()))
            if vLarge.isValid():
                return vLarge
        
        return v
        
            
            
         
        

    """
    Devuelve el valor de un campo del buffer copiado antes de sufrir cambios.

    @param fN Nombre del campo
    """
    @decorators.NotImplementedWarn
    def valueBufferCopy(self, fN):
        return True

    """
    Establece el valor de FLSqlCursor::edition.

    @param b TRUE o FALSE
    """
    @decorators.NotImplementedWarn
    def setEdition(self, b, m = None):
        return True
    
    @decorators.NotImplementedWarn   
    def restoreEditionFlag(self, m):
        return True

    """
    Establece el valor de FLSqlCursor::browse.

    @param b TRUE o FALSE
    """
    @decorators.NotImplementedWarn 
    def setBrowse(self, b,m = None):
        return True
    
    @decorators.NotImplementedWarn 
    def restoreBrowseFlag(self, m):
        return True

    """
    Establece el contexto de ejecución de scripts

    Ver FLSqlCursor::ctxt_.

    @param c Contexto de ejecucion
    """
    @decorators.NotImplementedWarn
    def setContext(self, c):
        return True

    """
    Para obtener el contexto de ejecución de scripts.

    Ver FLSqlCursor::ctxt_.

    @return Contexto de ejecución
    """
    def context(self):
        return self.d.ctxt_
    

    """
    Dice si un campo está deshabilitado.

    Un campo estará deshabilitado, porque esta clase le dará un valor automáticamente.
    Estos campos son los que están en una relación con otro cursor, por lo que
    su valor lo toman del campo foráneo con el que se relacionan.

    @param fN Nombre del campo a comprobar
    @return TRUE si está deshabilitado y FALSE en caso contrario
    """
    
    def fieldDisabled(self, fN):
        if self.d.modeAccess_ == self.Insert or self.d.modeAccess_ == self.Edit:
            if self.d.cursorRelation_ and self.d.relation_:
                if not self.d.cursorRelation_.metadata():
                    return False
                    if str(self.d.relation_.field()).lower() == str(fN).lower():
                        return True
                    else:
                        return False
            else:
                return False
        else:
            return False

    """
    Indica si hay una transaccion en curso.

    @return TRUE si hay una transaccion en curso, FALSE en caso contrario
    """
    @decorators.NotImplementedWarn
    def inTransaction(self):
        return True

    """
    Inicia un nuevo nivel de transacción.

    Si ya hay una transacción en curso simula un nuevo nivel de anidamiento de
    transacción mediante un punto de salvaguarda.

    @param  lock Actualmente no se usa y no tiene ningún efecto. Se mantiene por compatibilidad hacia atrás
    @return TRUE si la operación tuvo exito
    """
    @decorators.BetaImplementation
    def transaction(self, lock = False):
        if not self.d.db_ and not self.d.db_.db():
            print("FLSqlCursor::transaction() : No hay conexión con la base de datos")
            return False
        
        return self.d.db_.doTransaction(self)
            

    """
    Deshace las operaciones de una transacción y la acaba.

    @return TRUE si la operación tuvo exito
    """
    @decorators.NotImplementedWarn
    def rollback(self):
        return True

    """
    Hace efectiva la transacción y la acaba.

    @param notify Si TRUE emite la señal cursorUpdated y pone el cursor en modo BROWSE,
          si FALSE no hace ninguna de estas dos cosas y emite la señal de autoCommit
    @return TRUE si la operación tuvo exito
    """
    @decorators.NotImplementedWarn
    def commit(self, notify = True):
        return True
    
    def size(self):
        return self.d._model.rowCount()

    """
    Abre el formulario asociado a la tabla origen en el modo indicado.

    @param m Modo de apertura (FLSqlCursor::Mode)
    @param cont Indica que se abra el formulario de edición de registros con el botón de
         aceptar y continuar
    """

    def openFormInMode(self, m, cont = True):
        if not self.d.metadata_:
            return 

        
        if (not self.isValid() or self.size() <= 0) and not m == self.Insert:
            QtGui.QMessageBox.Warning(QtGui.qApp.focusWidget(), "Aviso","No hay ningún registro seleccionado",QtGui.QMessageBox.Ok,0,0)
            return
        
        if m == self.Del:
            res = QtGui.QMessageBox.Warning(QtGui.qApp.focusWidget(), "Aviso","El registro activo será borrado. ¿ Está seguro ?",QtGui.QMessageBox.Ok,(QtGui.QMessageBox.No, QtGui.QMessageBox.Default, QtGui.QMessageBox.Escape))
            if res == QtGui.QMessageBox.No:
                return
            
            self.transaction()
            self.modeAccess(self.Del)
            if not self.refreshBuffer():
                self.commit()
            else:
                if not self.commitBuffer():
                    self.rollback()
                else:
                    self.commit()
            return
        
        
        self.d.modeAccess_ = m 
        if self.d.buffer_:
            self.d.buffer_.clearValues(True)
        
        #if not self.d._action:
            #self.d.action_ = self.d.db_.manager().action(self.metadata().name())
            
        if not self._action:
            print("FLSqlCursor : Para poder abrir un registro de edición se necesita una acción asociada al cursor, o una acción definida con el mismo nombre que la tabla de la que procede el cursor.")
            return
        
        if not self._action.formRecord():
            QtGui.QMessageBox.Warning(QtGui.qApp.focusWidget(), "Aviso","No hay definido ningún formulario para manejar "
         "registros de esta tabla : %s" % str(self.d.curName()) ,QtGui.QMessageBox.Ok,0,0)
            return
        
        if self.refreshBuffer() or 1 == 1:
            
            self._action.openDefaultFormRecord(self)
            self.updateBufferCopy()
        else:
            print("AUCHHH")

            
               
        
        

    
        
        

    """
    Copia el contenido del FLSqlCursor::buffer_ actual en FLSqlCursor::bufferCopy_.

    Al realizar esta copia se podra comprobar posteriormente si el buffer actual y la copia realizada
    difieren mediante el metodo FLSqlCursor::isModifiedBuffer().
    """
    @decorators.NotImplementedWarn
    def updateBufferCopy(self):
        return True

    """
    Indica si el contenido actual del buffer difiere de la copia guardada.

    Ver FLSqlCursor::bufferCopy_ .

    @return TRUE si el buffer y la copia son distintas, FALSE en caso contrario
    """
    @decorators.NotImplementedWarn
    def isModifiedBuffer(self):
        return True

    """
    Establece el valor de FLSqlCursor::askForCancelChanges_ .

    @param a Valor a establecer (TRUE o FALSE)
    """
    def setAskForCancelChanges(self, a):
        self.d.askForCancelChanges_ = a

    """
    Activa o desactiva los chequeos de integridad referencial.

    @param a TRUE los activa y FALSE los desactiva
    """
    def setActivatedCheckIntegrity(self, a):
        self.d.activatedCheckIntegrity_ = a
    
    def activatedCheckIntegrity(self):
        return self.d.activatedCheckIntegrity_

    """
    Activa o desactiva las acciones a realizar antes y después de un commit

    @param a TRUE las activa y FALSE las desactiva
    """
    def setActivatedCommitActions(self, a):
        self.d.activatedCommitActions_ = a
  
    def activatedCommitActions(self):
        return self.d.activatedCommitActions_

    """
    Se comprueba la integridad referencial al intentar borrar, tambien se comprueba la no duplicidad de
    claves primarias y si hay nulos en campos que no lo permiten cuando se inserta o se edita.
    Si alguna comprobacion falla devuelve un mensaje describiendo el fallo.
    """
    @decorators.NotImplementedWarn
    def msgCheckIntegrity(self):
        return True

    """
    Realiza comprobaciones de intregidad.

    Se comprueba la integridad referencial al intentar borrar, tambien se comprueba la no duplicidad de
    claves primarias y si hay nulos en campos que no lo permiten cuando se inserta o se edita.
    Si alguna comprobacion falla muestra un cuadro de diálogo con el tipo de fallo encontrado y el metodo
    devuelve FALSE.

    @param showError Si es TRUE muestra el cuadro de dialogo con el error que se produce al no
           pasar las comprobaciones de integridad
    @return TRUE si se ha podido entregar el buffer al cursor, y FALSE si ha fallado alguna comprobacion
      de integridad
    """
    @decorators.NotImplementedWarn
    def checkIntegrity(self, showError = True):
        return True

    """
    Devuelve el cursor relacionado con este.
    """
    def cursorRelation(self):
        return self.d.cursorRelation_
  
    def relation(self):
        return self.d.relation_

    """
    Desbloquea el registro actual del cursor.

    @param fN Nombre del campo
    @param v Valor para el campo unlock
    """
    @decorators.NotImplementedWarn
    def setUnLock(self, fN, v):
        return True
        

    """
    Para comprobar si el registro actual del cursor está bloqueado.

    @return TRUE si está bloqueado, FALSE en caso contrario.
    """
    @decorators.NotImplementedWarn
    def isLocked(self):
        return False
    
    """
    Devuelve si el contenido de un campo en el buffer es nulo.

    @param pos_or_name Nombre o pos del campo en el buffer
    """

    def bufferIsNull(self, pos_or_name):
        
        if self.d.buffer_:
            return self.d.buffer_.isNull(pos_or_name)
        return True
            
    

    """
    Establece que el contenido de un campo en el buffer sea nulo.

    @param pos_or_name Nombre o pos del campo en el buffer
    """
    @decorators.NotImplementedWarn
    def bufferSetNull(self, pos_or_name):
        return True

    """
    Devuelve si el contenido de un campo en el bufferCopy en nulo.

    @param pos_or_name Nombre o pos del campo en el bufferCopy
    """
    @decorators.NotImplementedWarn
    def bufferCopyIsNull(self, pos_or_name):
        return True

  
    """
    Establece que el contenido de un campo en el bufferCopy sea nulo.

    @param pos_or_name Nombre o pos del campo en el bufferCopy
    """
    @decorators.NotImplementedWarn
    def bufferCopySetNull(self, pos_or_name):
        return True


    """
    Obtiene la posición del registro actual, según la clave primaria contenida en el buffer.

    La posición del registro actual dentro del cursor se calcula teniendo en cuenta el
    filtro actual ( FLSqlCursor::curFilter() ) y el campo o campos de ordenamiento
    del mismo ( QSqlCursor::sort() ).
    Este método es útil, por ejemplo, para saber en que posición dentro del cursor
    se ha insertado un registro.

    @return Posición del registro dentro del cursor, o 0 si no encuentra coincidencia.
    """
    @decorators.NotImplementedWarn
    def atFrom(self):
        return True

    """
    Obtiene la posición dentro del cursor del primer registro que en el campo indicado
    empieze con el valor solicitado. Supone que los registros están ordenados por dicho
    campo, para realizar una búsqueda binaria.

    La posición del registro actual dentro del cursor se calcula teniendo en cuenta el
    filtro actual ( FLSqlCursor::curFilter() ) y el campo o campos de ordenamiento
    del mismo ( QSqlCursor::sort() ).
    Este método es útil, por ejemplo, para saber en que posición dentro del cursor
    se encuentra un registro con un cierto valor en un campo.

    @param  fN  Nombre del campo en el que buscar el valor
    @param  v   Valor a buscar ( mediante like 'v%' )
    @param  orderAsc TRUE (por defecto) si el orden es ascendente, FALSE si es descendente
    @return Posición del registro dentro del cursor, o 0 si no encuentra coincidencia.
    """
    @decorators.NotImplementedWarn
    def atFromBinarySearch(self, fN, v, orderAsc = True):
        return True

    """
    Redefinido por conveniencia
    """
    @decorators.NotImplementedWarn
    def exec(self, query):
        return True


    """
    Para obtener la base de datos sobre la que trabaja
    """
    def db(self):
        return self.d.db_

    """
    Para obtener el nombre del cursor (generalmente el nombre de la tabla)
    """
    def curName(self):
        return self.d.curName_

    """
    Para obtener el filtro por defecto en campos asociados

    @param  fieldName Nombre del campo que tiene campos asociados.
                    Debe ser el nombre de un campo de este cursor.
    @param  tableMD   Metadatos a utilizar como tabla foránea.
                    Si es cero usa la tabla foránea definida por la relación M1 de 'fieldName'
    """
    
    def filterAssoc(self, fieldName, tableMD = None):
        fieldName = fieldName
        
        mtd = self.d.metadata_
        if not mtd:
            return None
        
        field = mtd.field(fieldName)
        if not field:
            return None
        
        ownTMD = False
        
        if not tableMD:
            ownTMD = True
            tableMD = self.d.db_.manager().metadata(field.relationM1().foreignTable())
        
        if not tableMD:
            return None
        
        fieldAc = field.associatedField()
        if not fieldAc:
            #if ownTMD and not tableMD.inCache():
                #del tableMD
            
            return None
        
        fieldBy = field.associatedFieldTo()
        if not tableMD.field(fieldBy) or self.d.buffer_.isNull(fieldAc.name()):
            #if ownTMD and not tableMD.inCache():
                #del tableMD
            return None
        
        vv = self.d.buffer_.value(fieldAc.name())
        if vv:
            #if ownTMD and not tableMD.inCache():
                #del tableMD
            return self.d.db_.manager().fomatAssignValue(fieldBy, fieldAc, vv, True)
        
        #if ownTMD and not tableMD.inCache():
            #del rableMD
        
        return None
            
        
        
            
        
        

    """
    Redefinida
    """
    @decorators.NotImplementedWarn
    def calculateField(self, name):
        return True

    """
    Redefinicion del método afterSeek() de QSqlCursor.
    """
    def afterSeek(self):
        return True
    
    def model(self):
        return self.d._model
    
    def selection(self):
        return self._selection
    
    def selection_currentRowChanged(self, current, previous):
        if self.d._currentregister == current.row(): return False
        self.d._currentregister = current.row()
        self.d._current_changed.emit(self.at())
        print("cursor:%s , row:%d" %(self._action.table, self.d._currentregister ))
    
    
    def at(self):
        row = self.d._currentregister
        print("Row", self.d._currentregister)
        if row < 0: return -1
        if row >= self.model().rows: return -2
        return row
    
    def isValid(self):
        if self.at() >= 0:
            return True
        else:
            return False
    
    """
    public slots:
    """
    
    """
    Refresca el contenido del cursor.

    Si no se ha indicado cursor relacionado obtiene el cursor completo, segun la consulta
    por defecto. Si se ha indicado que depende de otro cursor con el que se relaciona,
    el contenido del cursor dependerá del valor del campo que determina la relación.
    Si se indica el nombre de un campo se considera que el buffer sólo ha cambiado en ese
    campo y así evitar repeticiones en el refresco.

    @param fN Nombre del campo de buffer que ha cambiado
    """
    @QtCore.pyqtSlot()
    @QtCore.pyqtSlot(QString)
    def refresh(self, fN = None):
        if not self.d.metadata_:
            return
        
        if self.d.cursorRelation_ and self.d.relation_:
            self.d.persistentFilter_ = QString.null
            if not self.d.cursorRelation_.metadata():
                return 
            if str(self.d.cursorRelation_.metadata().primaryKey()) == str(fN) and self.d.cursorRelation_.modeAccess() == self.Insert:
                return
            if not fN or self.d.relation_.foreignField() == str(fN):
                self.d.buffer_ = None
                self.refreshDelayed(500)
        else:
            self.d._model.refresh()
            #print("FLCursor.refresh()")
            self.newBuffer.emit()
            

    """
    Actualiza el conjunto de registros con un retraso.

    Acepta un lapsus de tiempo en milisegundos, activando el cronómetro interno para
    que realize el refresh definitivo al cumplirse dicho lapsus.

    @param msec Cantidad de tiempo del lapsus, en milisegundos.
    """
    @QtCore.pyqtSlot()
    @decorators.NotImplementedWarn
    def refreshDelayed(self, msec = 50):
        return True



    def primeInsert(self):
         return PNBuffer(self.d)
    
    def primeUpdate(self):
        if not self.d.buffer_:
            self.d.buffer_ = PNBuffer(self.d)
        self.d.buffer_.primeUpdate()
        return self.d.buffer_
    
    @decorators.NotImplementedWarn
    def editBuffer(self, b):
        return True
        
    """
    Refresca el buffer segun el modo de acceso establecido.

    Lleva informacion del cursor al buffer para editar o navegar, o prepara el buffer para
    insertar o borrar.

    Si existe un campo contador se invoca a la función "calculateCounter" del script del
    contexto (ver FLSqlCursor::ctxt_) establecido para el cursor. A esta función se le pasa
    como argumento el nombre del campo contador y debe devolver el valor que debe contener
    ese campo.

    @return TRUE si se ha podido realizar el refresco, FALSE en caso contrario
    """
    @QtCore.pyqtSlot()
    @decorators.BetaImplementation
    def refreshBuffer(self):
        if not self.d.metadata_:
            return False
        
        if not self.isValid() and not self.d.modeAccess_ == self.Insert:
            return False
        
        if self.d.modeAccess_ == self.Insert:
            if not self.commitBufferCursorRelation():
                return False
            
            self.d.buffer_ = self.primeInsert()
            self.setNotGenerateds()
            
            fieldList = self.metadata().fieldListObject()
            if fieldList:
                for field in fieldList:
                    fiName = field.name()
                    self.d.buffer_.setNull(fiName)
                    if not self.d.buffer_.isGenerated(fiName):
                        continue
                    type_ = field.type()
                    fltype = FLFieldMetaData.flDecodeType(type_) 
                    defVal = field.defaultValue()
                    if defVal.isValid():
                        defVal.cast(fltype)
                        self.d.buffer_.setValue(fiName, defVal)
                    
                    if type_ == "serial":
                        self.d.buffer_.setValue(fiName, self.d.db_.nextSerialVal(self.d.metadata_.name(), fiName).toUInt())
                    
                    if field.isCounter():
                        siguiente = self.calculateCounter(fiName)
                        if siguiente.isValid():
                            self.d.buffer_.setValue(fiName, siguiente)
                        else:
                            siguiente = FLUtil.nextCounter(fiName, self)
                            if siguiente.isValid():
                                self.d.buffer_.setValue(fiName, siguiente)
                            
            if self.d.cursorRelation_ and self.d.relation_ and self.d.cursorRelation_.metadata():
                self.setValueBuffer(self.d.relation_.field(), self.d.cursorRelation_.valueBuffer(self.d.relation_.foreignField()))
            
            self.d.undoAcl()
            self.updateBufferCopy()
            self.newBuffer.emit()
        
        elif self.d.modeAccess_ == self.Edit:
            print("FLCursor.refeshBuffer 1")
            if not self.commitBufferCursorRelation():
                return False
            
            print("FLCursor.refeshBuffer 2")
            if self.isLocked() and self.d.acosCondName_.isEmpty():
                self.d.modeAccess_ = self.Browse
            
            print("FLCursor.refeshBuffer 3")
            self.d.buffer_ = self.primeUpdate()
            self.setNotGenerateds()
            self.updateBufferCopy()
            self.newBuffer.emit()
        
        elif self.d.modeAccess_ == self.Del:
            if self.isLocked():
                self.d.msgboxWarning("Registro bloqueado, no se puede eliminar")
                self.d.modeAccess_ = self.Browse
                return False
            
            self.d.buffer_.primeDelete()
            self.setNoGenerateds()
            self.updateBufferCopy()
            
        elif self.d.modeAccess_ == self.Browse:
            self.d.buffer_ = self.editBuffer(True)
            self.setNoGenerateds()
            self.newBuffer.emit()
        
        return True
            
        
        
     
        

    """
    Pasa el cursor a modo Edit

    @return True si el cursor está en modo Edit o estaba en modo Insert y ha pasado con éxito a modo Edit
    """
    @QtCore.pyqtSlot()
    def setEditMode(self):
        if self.d.modeAccess_ == self.Insert:
            if not self.commitBuffer():
                return False
            self.refresh()
            self.setModeAccess(self.Edit)
        elif self.d.modeAccess_ == self.Edit:
            return True
        
        return False
            
    
    """
    Redefinicion del método seek() de QSqlCursor.

    Este método simplemente invoca al método seek() original de QSqlCursor() y refresca
    el buffer con el metodo FLSqlCursor::refreshBuffer().

    @param emit Si TRUE emite la señal FLSqlCursor::currentChanged()
    """
    @QtCore.pyqtSlot()
    @decorators.NotImplementedWarn
    def seek(self, i, relative = False, emite = False):
        return True

    """
    Redefinicion del método next() de QSqlCursor.

    Este método simplemente invoca al método next() original de QSqlCursor() y refresca el
    buffer con el metodo FLSqlCursor::refreshBuffer().

    @param emit Si TRUE emite la señal FLSqlCursor::currentChanged()
    """
    @QtCore.pyqtSlot()
    @decorators.BetaImplementation
    def next(self,  emite = True):
        if self.d.modeAccess_ == self.Del:
            return False
        self.moveby(1)
        
    
        
    def moveby(self, pos):
        return self.move(pos+self.d._currentregister)
    
    """
    Redefinicion del método prev() de QSqlCursor.

    Este método simplemente invoca al método prev() original de QSqlCursor() y refresca
    el buffer con el metodo FLSqlCursor::refreshBuffer().

    @param emit Si TRUE emite la señal FLSqlCursor::currentChanged()
    """
    @QtCore.pyqtSlot()
    @decorators.NotImplementedWarn
    def prev(self, emite = True):
        return self.moveby(-1)
        

    """
    Redefinicion del método first() de QSqlCursor.

    Este método simplemente invoca al método first() original de QSqlCursor() y refresca el
    buffer con el metodo FLSqlCursor::refreshBuffer().

    @param emit Si TRUE emite la señal FLSqlCursor::currentChanged()
    """
    @QtCore.pyqtSlot()
    @decorators.NotImplementedWarn
    def first(self,  emite = True):
        return self.move(0)

    """
    Redefinicion del método last() de QSqlCursor.

    Este método simplemente invoca al método last() original de QSqlCursor() y refresca el
    buffer con el metodo FLSqlCursor::refreshBuffer().

    @param emit Si TRUE emite la señal FLSqlCursor::currentChanged()
    """
    @QtCore.pyqtSlot()
    @decorators.NotImplementedWarn
    def last(self, emite = True):
        return True

    """
    Redefinicion del método del() de QSqlCursor.

    Este método invoca al método del() original de QSqlCursor() y comprueba si hay borrado
    en cascada, en caso afirmativo borrar también los registros relacionados en cardinalidad 1M.
    """
    @QtCore.pyqtSlot()
    @decorators.NotImplementedWarn
    def __del__(self, invalidate = True):
        return True

    """
    Redefinicion del método select() de QSqlCursor
    """
    @QtCore.pyqtSlot()
    @decorators.NotImplementedWarn
    def select(self, filter_, sort = None ): #sort = QtCore.QSqlIndex()
        return True

    """
    Redefinicion del método sort() de QSqlCursor
    """
    @QtCore.pyqtSlot()
    @decorators.NotImplementedWarn
    def setSort(self, sort):
        return True

    """
    Obtiene el filtro base
    """
    @QtCore.pyqtSlot()
    @decorators.NotImplementedWarn
    def baseFilter(self):
        return True

    """
    Obtiene el filtro actual
    """
    @QtCore.pyqtSlot()
    @decorators.NotImplementedWarn
    def curFilter(self):
        return True
    
    """
    Redefinicion del método setFilter() de QSqlCursor
    """
    @QtCore.pyqtSlot()
    @decorators.BetaImplementation
    def setFilter(self, filter_):
        
        finalFilter = filter_
        bFilter = self.baseFilter()
        
        if not bFilter.isEmpty():
            if finalFilter.isEmpty() or bFilter.contains(finalFilter):
                finalFilter = bFilter
            elif not finalFilter.contains(bFilter):
                finalFilter = bFilter + " AND " + finalFilter
        
        if not finalFilter.isEmpty() and not self.d.persistentFilter_.isEmpty() and not finalFilter.contains(self.d.persistentFilter_):
            finalFilter = finalFilter + " OR " + self.d.persistentFilter_
        
        self.d.filter_ = finalFilter
            
        

  
    """
    Abre el formulario de edicion de registro definido en los metadatos (FLTableMetaData) listo
    para insertar un nuevo registro en el cursor.
    """
    @QtCore.pyqtSlot()
    def insertRecord(self):
        print("Insert a row ", self._action.name)
        self.openFormInMode(self.Insert)

    """
    Abre el formulario de edicion de registro definido en los metadatos (FLTableMetaData) listo
    para editar el registro activo del cursor.
    """
    @QtCore.pyqtSlot()
    @decorators.BetaImplementation
    def editRecord(self):
        print("Edit the row!", self.actionName())
        if self.d.needUpdate():
            pKN = self.d.metadata_.primaryKey()
            pKValue = self.valueBuffer(pKN)
            self.refresh()
            pos = self.atFromBinarySearch(pKN, pKValue.toString())
            if not pos == self.at(): 
                self.seek(pos, False, False)
                
        self.openFormInMode(self.Edit)

    """
    Abre el formulario de edicion de registro definido en los metadatos (FLTableMetaData) listo
    para sólo visualizar el registro activo del cursor.
    """
    @QtCore.pyqtSlot()
    @decorators.BetaImplementation
    def browseRecord(self):
        print("Inspect, inspect!", self.actionName())
        if self.d.needUpdate():
            pKN = self.d.metadata_.primaryKey()
            pKValue = self.valueBuffer(pKN)
            self.refresh()
            pos = self.atFromBinarySearch(pKN, pKValue.toString())
            if not pos == self.at(): 
                self.seek(pos, False, False)
        
        self.openFormInMode(self.Browse)


    """
    Borra, pidiendo confirmacion, el registro activo del cursor.
    """
    @QtCore.pyqtSlot()
    def deleteRecord(self):
        print("Drop the row!", self.actionName())
        self.openFormInMode(self.Del)
        #self.d._action.openDefaultFormRecord(self)

    """
    Realiza la accion de insertar un nuevo registro, y copia el valor de los campos del registro
    actual.
    """
    def copyRecord(self):
        return True

    """
    Realiza la acción asociada a elegir un registro del cursor, por defecto se abre el formulario de
    edición de registro,llamando al método FLSqlCursor::editRecord(), si la bandera FLSqlCursor::edition
    indica TRUE, si indica FALSE este método no hace nada
    """
    @QtCore.pyqtSlot()
    @decorators.NotImplementedWarn
    def chooseRecord(self):
        return True

    """
    Manda el contenido del buffer al cursor, o realiza la acción oportuna para el cursor.

    Todos los cambios realizados en el buffer se hacen efectivos en el cursor al invocar este método.
    La manera de efectuar estos cambios viene determinada por el modo de acceso establecido para
    el cursor, ver FLSqlCursor::Mode, si el modo es editar o insertar actualiza con los nuevos valores de
    los campos del registro, si el modo es borrar borra el registro, y si el modo es navegacion no hace nada.
    Antes de nada tambien comprueba la integridad referencial invocando al método FLSqlCursor::checkIntegrity().

    Si existe un campo calculado se invoca a la función "calculateField" del script del
    contexto (ver FLSqlCursor::ctxt_) establecido para el cursor. A esta función se le pasa
    como argumento el nombre del campo calculado y debe devolver el valor que debe contener
    ese campo, p.e. si el campo es el total de una factura y de tipo calculado la función
    "calculateField" debe devolver la suma de lineas de las facturas mas/menos impuestos y
    descuentos.

    @param  emite       True para emitir señal cursorUpdated
    @param  checkLocks  True para comprobar riesgos de bloqueos para esta tabla y el registro actual
    @return TRUE si se ha podido entregar el buffer al cursor, y FALSE si ha fallado la entrega
    """
    
    @QtCore.pyqtSlot()
    @decorators.NotImplementedWarn
    def commitBuffer(self, emite = True, checkLocks = False):
        return True

    """
    Manda el contenido del buffer del cursor relacionado a dicho cursor.

    Hace efectivos todos los cambios en el buffer del cursor relacionado posiconándose en el registro
    correspondiente que recibe los cambios.
    """
    @QtCore.pyqtSlot()
    @decorators.NotImplementedWarn
    def commitBufferCursorRelation(self):
        return True

    """
    @return El nivel actual de anidamiento de transacciones, 0 no hay transaccion
    """
    @QtCore.pyqtSlot()
    @decorators.NotImplementedWarn
    def transactionLevel(self):
        return True

    """
    @return La lista con los niveles de las transacciones que ha iniciado este cursor y continuan abiertas
    """
    @QtCore.pyqtSlot()
    @decorators.NotImplementedWarn
    def transactionsOpened(self):
        return True

    """
    Deshace transacciones abiertas por este cursor.

    @param count  Cantidad de transacciones a deshacer, -1 todas.
    @param msg    Cadena de texto que se muestra en un cuadro de diálogo antes de deshacer las transacciones.
                Si es vacía no muestra nada.
    """
    @QtCore.pyqtSlot()
    @decorators.NotImplementedWarn
    def rollbackOpened(self, count = -1, msg = QString()):
        return True

    """
    Termina transacciones abiertas por este cursor.

    @param count  Cantidad de transacciones a terminar, -1 todas.
    @param msg    Cadena de texto que se muestra en un cuadro de diálogo antes de terminar las transacciones.
                Si es vacía no muestra nada.
    """
    @QtCore.pyqtSlot()
    @decorators.NotImplementedWarn
    def commitOpened(self, count = -1, msg = QString()):
        return True

    """
    Entra en un bucle de comprobacion de riesgos de bloqueos para esta tabla y el registro actual

    El bucle continua mientras existan bloqueos, hasta que se vuelva a llamar a este método con
    'terminate' activado o cuando el usuario cancele la operación.

    @param  terminate True terminará el bucle de comprobaciones si está activo
    """
    @QtCore.pyqtSlot()
    @decorators.NotImplementedWarn
    def checkRisksLocks(self, terminate = False):
        return True

    
    """
    Establece el acceso global para la tabla, ver FLSqlCursor::setAcosCondition().

    Este será el permiso a aplicar a todos los campos por defecto

    @param  ac Permiso global; p.e.: "r-", "-w"
    """
    @QtCore.pyqtSlot()
    @decorators.NotImplementedWarn
    def setAcTable(self, ac):
        return True

    """
    Establece la lista de control de acceso (ACOs) para los campos de la tabla, , ver FLSqlCursor::setAcosCondition().

    Esta lista de textos deberá tener en sus componentes de orden par los nombres de los campos,
    y en los componentes de orden impar el permiso a aplicar a ese campo,
    p.e.: "nombre", "r-", "descripcion", "--", "telefono", "rw",...

    Los permisos definidos aqui sobreescriben al global.

    @param acos Lista de cadenas de texto con los nombre de campos y permisos.
    """
    @QtCore.pyqtSlot()
    @decorators.NotImplementedWarn
    def setAcosTable(self, acos):
        return True

    """
    Establece la condicion que se debe cumplir para aplicar el control de acceso.

    Para cada registro se evalua esta condicion y si se cumple, aplica la regla
    de control de acceso establecida con FLSqlCursor::setAcTable y FLSqlCursor::setAcosTable.

    Ejemplos:

    setAcosCondition( "nombre", VALUE, "pepe" ); // valueBuffer( "nombre" ) == "pepe"
    setAcosCondition( "nombre", REGEXP, "pe*" ); // QRegExp( "pe*" ).exactMatch( valueBuffer( "nombre" ).toString() )
    setAcosCondition( "sys.checkAcos", FUNCTION, true ); // call( "sys.checkAcos" ) == true

    @param  cond      Tipo de evaluacion;
                    VALUE compara con un valor fijo
                    REGEXP compara con una expresion regular
                    FUNCTION compara con el valor devuelto por una funcion de script

    @param  condName  Si es vacio no se evalua la condicion y la regla no se aplica nunca.
                    Para VALUE y REGEXP nombre de un campo.
                    Para FUNCTION nombre de una funcion de script.  A la función se le pasa como
                    argumento el objeto cursor.

    @param  condVal   Valor que hace que la condicion sea cierta
    """
    @QtCore.pyqtSlot()
    @decorators.NotImplementedWarn
    def setAcosCondition(self, condName, cond, condVal):
        return True

    """
    Comprueba si hay una colisión de campos editados por dos sesiones simultáneamente.

    @return Lista con los nombres de los campos que colisionan
    """
    @QtCore.pyqtSlot()
    @decorators.NotImplementedWarn
    def concurrencyFields(self):
        return True

    """
    Cambia el cursor a otra conexión de base de datos
    """
    @QtCore.pyqtSlot()
    @decorators.NotImplementedWarn
    def changeConnection(self, connName):
        return True

    



    """
    Si el cursor viene de una consulta, realiza el proceso de agregar la defición
    de los campos al mismo
    """
    @decorators.NotImplementedWarn
    def populateCursor(self):
        return True

    """
    Cuando el cursor viene de una consulta, realiza el proceso que marca como
    no generados (no se tienen en cuenta en INSERT, EDIT, DEL) los campos del buffer
    que no pertenecen a la tabla principal
    """
    @decorators.NotImplementedWarn
    def setNotGenerateds(self):
        return True

    """
    Uso interno
    """
    @decorators.NotImplementedWarn
    def setExtraFieldAttributes(self):
        return True
    
    @decorators.NotImplementedWarn
    def clearMapCalcFields(self):
        return True
    
    @decorators.NotImplementedWarn
    def valueBufferRaw(self, fN):
        return True
    
    """
    signals:
    """

    """
    Indica que se ha cargado un nuevo buffer
    """
    newBuffer = QtCore.pyqtSignal()

    """
    Indica ha cambiado un campo del buffer, junto con la señal se envía el nombre del campo que
    ha cambiado.
    """
    bufferChanged = QtCore.pyqtSignal(QString)

    """
    Indica que se ha actualizado el cursor
    """
    cursorUpdated = QtCore.pyqtSignal()

    """
    Indica que se ha elegido un registro, mediante doble clic sobre él o bien pulsando la tecla Enter
    """
    recordChoosed = QtCore.pyqtSignal()

    """
    Indica que la posicion del registro activo dentro del cursor ha cambiado
    """
    currentChanged = QtCore.pyqtSignal(int)

    """
    Indica que se ha realizado un commit automático para evitar bloqueos
    """
    autoCommit = QtCore.pyqtSignal()

    """
    Indica que se ha realizado un commitBuffer
    """
    bufferCommited = QtCore.pyqtSignal()

    """
    Indica que se ha cambiado la conexión de base de datos del cursor. Ver changeConnection
    """
    connectionChanged = QtCore.pyqtSignal()

    """
    Indica que se ha realizado un commit
    """
    commited = QtCore.pyqtSignal()

    """
    private slots:
    """
    
    """ Uso interno """
    clearPersistentFilter = QtCore.pyqtSignal()

#endif 