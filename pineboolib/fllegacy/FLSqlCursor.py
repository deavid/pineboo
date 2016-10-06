# -*- coding: utf-8 -*-

from pineboolib.flcontrols import ProjectClass
from pineboolib import decorators, fllegacy
from pineboolib.fllegacy.FLSqlQuery import FLSqlQuery
from pineboolib.utils import DefFun

from PyQt4 import QtCore,QtGui
from PyQt4.QtCore import QString, QVariant

from pineboolib.fllegacy.FLTableMetaData import FLTableMetaData
from pineboolib.fllegacy.FLSqlSavePoint import FLSqlSavePoint

from pineboolib.CursorTableModel import CursorTableModel
from pineboolib.fllegacy.FLFieldMetaData import FLFieldMetaData

import hashlib, traceback

class Struct(object):
    pass





class PNBuffer(ProjectClass):

    fieldList_ = None
    cursor_ = None
    clearValues_ = False
    line_ = None

    def __init__(self, cursor):
        super(PNBuffer,self).__init__()
        self.cursor_ = cursor
        self.fieldList_ = []
        self.md5Sum_ = ""
        campos = self.cursor_.db_.manager().metadata(self.cursor_.curName_).fieldListObject()
        for campo in campos:
            field = Struct()
            field.name = campo.name()
            field.value = None
            field.metadata = campo
            field.type_ = field.metadata.type()
            field.modified = False

            self.line_ = None
            self.fieldList_.append(field)

    def count(self):
        return len(self.fieldList_)

    def primeUpdate(self, row = None):
        if row < 0:
            row = self.cursor_._currentregister
        for field in self.fieldList_:
            field.value = self.cursor_._model.value(row , field.name)


        self.line_ = self.cursor_._currentregister

    def primeDelete(self):
        for field in self.fieldList_:
            field.value = None

    def row(self):
        return self.line_

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
                field.modified = False


    def isEmpty(self):
        if len(self.fieldList_) <= 0:
            return True
        else:
            return False

    def isNull(self, n):
        if isinstance(n , (str, QString)):
            n = str(n)
            for field in  self.fieldList_:
                if field.name == str(n):
                    if not field.value:
                        #print("PNBuffer.isNull(True)")
                        return True
                    else:
                        return False
        else:
            i = 0
            for field in self.fieldList_:
                if i == n:
                    if not field.value:
                        return True
                    else:
                        return False
                i = i + 1


        return True


    def value(self, n):
        if isinstance(n, (str, QString)):
            n = str(n)
            for field in  self.fieldList_:
                if field.name == str(n):
                    #print("PNBuffer.value(%s) = %s" % (name, field.value) )
                    if field.value is None:
                        return None
                    else:
                        return field.value
        else:
            i = 0
            for field in self.fieldList_:
                if i == n:
                    return self.fieldList_[n].value


            return None

    def setValue(self, name, value):
        if value is not None and not isinstance(value, (int, float, str)):
            raise ValueError("No se admite el tipo %r , en setValue %r" % (type(value) ,value))

        for field in  self.fieldList_:
            if field.name == str(name):
                field.value = value
                field.modified = True
                self.setMd5Sum(value)
                return


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

    def setGenerated(self, i, b):
        pos = 0
        for field in self.fieldList_:
            if pos == i:
                field.metadata.d.generated_ = b
                return
            pos = pos + 1

    """
    Calcula el md5 de todos los valores contenidos en el buffer concatenando el md5 de un valor con el nombre del siguiente y calculando el nuevo md5
    """
    def setMd5Sum(self, value):
        value = str(value)
        cadena = "%s_%s" % (self.md5Sum_, value)
        tmp = hashlib.md5(value.encode()).hexdigest()
        self.md5Sum_ = tmp

    def md5Sum(self):
        return self.md5Sum_

    def modifiedFields(self):
        lista = []
        for f in self.fieldList_:
            if f.modified:
                lista.append(f.name)

        return lista


    def pK(self):
        for f in self.fieldList_:
            if f.metadata.isPrimaryKey():
                return f.name

        print("PNBuffer.pk(): No se ha encontrado clave Primaria")

    def indexField(self, name):
        i = 0
        for f in self.fieldList_:
            if f.name == name:
                return i

            i = i + 1



################################################################################
################################################################################
#######                                                                  #######
#######                                                                  #######
#######                      FLSqlCursorPrivate                          #######
#######                                                                  #######
#######                                                                  #######
################################################################################
################################################################################

class FLSqlCursorPrivate(QtCore.QObject):

    """
    Buffer con un registro del cursor.

    Según el modo de acceso FLSqlCursor::Mode establecido para el cusor, este buffer contendrá
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
    #self.d._model.where_filters["main-filter"] = None

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
    Cronómetro interno
    """
    timer_ = None

    """
    Cuando el cursor proviene de una consulta indica si ya se han agregado al mismo
    la definición de los campos que lo componen
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
    mapCalcFields_ = []
    rawValues_ = None

    md5Tuples_ = None

    countRefCursor = None

    _model = None

    _currentregister = None
    editionStates_ = None

    filter_ = None


    _current_changed = QtCore.pyqtSignal(int)

    def __init__(self):
        super(FLSqlCursorPrivate,self).__init__()
        self.metadata_ = None
        self.countRefCursor = 0
        self._currentRegister = -1
        self.acosCondName_ = QString()
        self.buffer_ = None




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
            #print("AQBoolFlagState count", self.count_)

        if self.browseStates_:
            del self.browseStates_
            #print("AQBoolFlagState count", self.count_)

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










################################################################################
################################################################################
#######                                                                  #######
#######                                                                  #######
#######                         FLSqlCursor                              #######
#######                                                                  #######
#######                                                                  #######
################################################################################
################################################################################


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

    _refreshDelayedTimer = None


    def __init__(self, name , autopopulate = True, connectionName_or_db = None, cR = None, r = None , parent = None):
        super(FLSqlCursor,self).__init__()
        self._valid = False
        self.d = FLSqlCursorPrivate()
        self.d.nameCursor_ = "%s%s" % (name, QtCore.QDateTime.currentDateTime())

        if connectionName_or_db is None:
            #print("Init1") # si soy texto y estoy vacio
            self.d.db_ = self._prj.conn
        elif isinstance(connectionName_or_db, QString) or isinstance(connectionName_or_db, str):
            #print("Init2 ")
            self.d.db_ = self._prj.conn
        else:
            #print("Init3", connectionName_or_db)
            self.d.db_ = connectionName_or_db

        #for module in self._prj.modules:
        #    for action in module.actions:
        #        if action.name == name:
        #            self.d.action_ = action
        #            break
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

        self.d.modeAccess_ = FLSqlCursor.Browse

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

        self.fieldsNamesUnlock_ = self.metadata().fieldsNamesUnlock()

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
                    pass

                cR.bufferChanged.connect(self.refresh)
                try:
                    cR.newBuffer.disconnect(self.clearPersistentFilter)
                except:
                    pass
                cR.newBuffer.connect(self.clearPersistentFilter)
        else:
            self.seek(None)

        if self.d.timer_:
            del self.d.timer_


        self.refreshDelayed()
        #self.d.md5Tuples_ = self.db().md5TuplesStateTable(self.d.curName_)
        #self.first()

    def table(self):
        return self.metadata().name()


    def __getattr__(self, name): return DefFun(self, name)


    def setName(self, name, autop):
        self.name = name
        #autop = autopopulate para que??

    """
    Para obtener los metadatos de la tabla.

    @return Objeto FLTableMetaData con los metadatos de la tabla asociada al cursor
    """
    def metadata(self):
        #if not self.d.metadata_:
            #print("FLSqlCursor(%s) Esta devolviendo un metadata vacio" % self.d.curName_)
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
        return getattr(self.d._model,'where_filters["main-filter"]',None)


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

            if getattr(self._action,"table",None):
                self.d._model = CursorTableModel(self._action, self._prj)
                self._selection = QtGui.QItemSelectionModel(self.model())
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
        #print("New main filter:", f)
        if self.d._model:
            self.d._model.where_filters["main-filter"] = f
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
    @decorators.Incomplete
    def setValueBuffer(self, fN, v):
        self.d.buffer_.setValue(fN, v)
        self.bufferChanged.emit(fN)

    """
    Devuelve el valor de un campo del buffer.

    @param fN Nombre del campo
    """

    def valueBuffer(self, fN):
        fN = str(fN)
        if self.d.rawValues_:
            return self.valueBufferRaw(fN)

        if not self.metadata():
            return None

        #if not self.d.buffer_ or self.d.buffer_.isEmpty() or not self.metadata():
        if self.model().rows > 0 and not self.modeAccess() == FLSqlCursor.Insert:
            if not self.d.buffer_:
                self.refreshBuffer()

            if not self.d.buffer_:
                print("ERROR: FLSqlCursor: aún después de refresh, no tengo buffer.", self.curName())
                return None
        else:
            return None

        field = self.metadata().field(fN)
        if not field:
            #print("FLSqlCursor::valueBuffer() : No existe el campo %s:%s" % (self.metadata().name(), fN))
            return None

        type_ = field.type()
        fltype = field.flDecodeType(type_)
        if self.d.buffer_.isNull(fN):
            if type_ == "double" or type_ == "int" or type_ == "uint":
                return 0

        v = None
        if field.outTransaction() and self.d.db_.dbAux() and not self.d.db_.db() == self.d.db_.dbAux() and not self.d.modeAccess_ == self.Insert:
            pK = self.d.metadata_.primaryKey()
            if pK:
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

        if v and type_ == "pixmap":
            vLarge = self.d.db_.manager().fetchLargeValue(v)
            if vLarge:
                return vLarge

        return v


    def fetchLargeValue(self, value):
        return self.d.db_.manager().fetchLargeValue(value)



    """
    Devuelve el valor de un campo del buffer copiado antes de sufrir cambios.

    @param fN Nombre del campo
    """
    def valueBufferCopy(self, fN):
        if not self.d.bufferCopy_ and fN.isEmpty() or not self.d.metadata_:
            return QVariant()

        field = self.d.metadata_.field(fN)
        if not field:
            print("FLSqlCursor::valueBufferCopy() : No existe el campo %s:%s" % (self.d.metadata_.name(), fN))
            return QVariant()

        type_ = field.type()
        if self.d.bufferCopy_.isNull(fN):
            if type_ == "double" or type_ == "int" or type_ == "uint":
                return 0

        v = self.d.bufferCopy_.value(fN)

        #v.cast(fltype)

        if not v.isNull() and type_ == "pixmap":
            vl = self.d.db_.manager().fetchLargeValue(v)
            if vl.isValid():
                return vl

        return v





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
    def setContext(self, c):
        self.d.ctxt_ = c

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
    def inTransaction(self):
        if self.d.db_:
            if self.d.db_.transaction_ > 0:
                return True
            else:
                return False

    """
    Inicia un nuevo nivel de transacción.

    Si ya hay una transacción en curso simula un nuevo nivel de anidamiento de
    transacción mediante un punto de salvaguarda.

    @param  lock Actualmente no se usa y no tiene ningún efecto. Se mantiene por compatibilidad hacia atrás
    @return TRUE si la operación tuvo exito
    """

    def transaction(self, lock = False):
        if not self.d.db_ and not self.d.db_.db():
            print("FLSqlCursor::transaction() : No hay conexión con la base de datos")
            return False

        return self.d.db_.doTransaction(self)


    """
    Deshace las operaciones de una transacción y la acaba.

    @return TRUE si la operación tuvo exito
    """
    def rollback(self):
        if not self.d.db_ and not self.d.db_.db():
            print("FLSqlCursor::rollback() : No hay conexión con la base de datos")
            return False

        return self.d.db_.doRollback(self)




    """
    Hace efectiva la transacción y la acaba.

    @param notify Si TRUE emite la señal cursorUpdated y pone el cursor en modo BROWSE,
          si FALSE no hace ninguna de estas dos cosas y emite la señal de autoCommit
    @return TRUE si la operación tuvo exito
    """
    def commit(self, notify = True):
        if not self.d.db_ and not self.d.db_.db():
            print("FLSqlCursor::commit() : No hay conexión con la base de datos")
            return False

        r = self.d.db_.doCommit(self, notify)
        if r:
            self.commited.emit()

        return r



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
            QtGui.QMessageBox.warning(QtGui.qApp.focusWidget(), "Aviso","No hay ningún registro seleccionado",QtGui.QMessageBox.Ok,0,0)
            return

        if m == self.Del:
            res = QtGui.QMessageBox.warning(QtGui.qApp.focusWidget(), "Aviso","El registro activo será borrado. ¿ Está seguro ?",QtGui.QMessageBox.Ok, QtGui.QMessageBox.No | QtGui.QMessageBox.Default| QtGui.QMessageBox.Escape)
            if res == QtGui.QMessageBox.No:
                return

            self.transaction()
            self.d.modeAccess_ = self.Del
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

        if self.refreshBuffer():
            self._action.openDefaultFormRecord(self)
            self.updateBufferCopy()










    """
    Copia el contenido del FLSqlCursor::buffer_ actual en FLSqlCursor::bufferCopy_.

    Al realizar esta copia se podra comprobar posteriormente si el buffer actual y la copia realizada
    difieren mediante el metodo FLSqlCursor::isModifiedBuffer().
    """
    def updateBufferCopy(self):
        if not self.d.buffer_:
            return None

        self.d.bufferCopy_ = self.d.buffer_

    """
    Indica si el contenido actual del buffer difiere de la copia guardada.

    Ver FLSqlCursor::bufferCopy_ .

    @return TRUE si el buffer y la copia son distintas, FALSE en caso contrario
    """
    def isModifiedBuffer(self):
        modifiedFields = self.d.buffer_.modifiedFields()
        if modifiedFields:
            return True
        else:
            return False

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
    @decorators.BetaImplementation
    def isLocked(self):
        if not self.d.modeAccess_ == self.Insert and self.fieldsNamesUnlock_ and self.d.buffer_ and self.d.buffer_.value(self.d.metadata_.primaryKey()):
            for field in self.fieldsNamesUnlock_:
                if not self.d.buffer_.value(field):
                    return True
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
    def atFrom(self):
        if not self.d.buffer_ or not self.d.metadata_:
            return 0

        pKN = self.d.metadata_.primaryKey()
        pKValue = self.valueBuffer(pKN)

        pos = -99

        if pos == -99:
            #q = FLSqlQuery(None, self.d.db_.db()) FIXME
            q = FLSqlQuery()
            sql = self.curFilter()
            sqlIn = self.curFilter()
            cFilter = self.curFilter()
            field = self.d.metadata_.field(pKN)

            sqlPriKey = None
            sqlFrom = None
            sqlWhere = None
            sqlPriKeyValue = None
            sqlOrderBy = None

            if not self.d.isQuery_ or "." in pKN:
                sqlPriKey = pKN
                sqlFrom = self.d.metadata_.name()
                sql = "SELECT %s FROM %s" % (sqlPriKey, sqlFrom)
            else:
                qry = self.d.db_.manager().query(self.d.metadata_.query(), self)
                if qry:
                    sqlPriKey = "%s.%s" % (self.d.metadata_.name(), pKN)
                    sqlFrom = qry.From()
                    sql = "SELECT %s FROM %s" % (sqlPriKey, sqlFrom)
                    qry.deleteLater()
                else:
                    print("FLSqlCursor::atFrom Error al crear la consulta")
                    self.seek(self.at())
                    if self.isValid():
                        pos = self.at()
                    else:
                        pos = 0
                    return pos

            if cFilter:
                sqlWhere = cFilter
                sql = "%s WHERE %s" % (sql, sqlWhere)
            else:
                sqlWhere = "1=1"

            if field:
                sqlPriKeyValue = self.d.db_.manager().formatAssignValue(field, pKValue)
                if cFilter:
                    sqlIn = "%s AND %s" % (sql, sqlPriKeyValue)
                else:
                    sqlIn = "%s WHERE %s" % (sql, sqlPriKeyValue)
                q.exec_(sqlIn)
                if not q.next():
                    self.seek(self.at())
                    if self.isValid():
                        pos = self.at()
                    else:
                        pos = 0
                    return pos

            if self.d.isQuery_ and self.d.queryOrderBy_:
                sqlOrderBy = self.d.queryOrderBy_
                sql = "%s ORDERBY %s" % (sql, sqlOrderBy)
            elif len(self.sort()) > 0:
                sqlOrderBy = self.sort()
                sql = "%s ORDERBY %s" % (sql, sqlOrderBy)

            if sqlPriKeyValue and self.d.db_.canOverPartition():
                posEqual = sqlPriKeyValue.index("=")
                leftSqlPriKey = sqlPriKeyValue[0:posEqual]
                sqlRowNum = "SELECT rownum FROM (SELECT row_number() OVER (ORDER BY %s) as rownum, %s as %s FROM %s WHERE %s ORDER BY %s) as subnumrow where" % (sqlOrderBy, sqlPriKey,leftSqlPriKey, sqlFrom, sqlWhere, sqlOrderBy)
                if q.exec_(sqlRowNum) and q.next():
                    pos = int(q.value(0)) -1
                    if pos >= 0:
                        return pos


            found = False
            q.exec_(sql)

            pos = 0
            if q.first():
                if not q.value(0) == pKValue:
                    pos = q.size()
                    if q.last() and pos > 1:
                        pos = pos -1
                        if not q.value(0) == pKValue:
                            while q.prev() and pos > 1:
                                pos = pos -1
                                if q.value(0) == pKValue:
                                    found = True
                                    break

                        else:
                            found = True

                    else:
                        found = True

            if not found:
                    self.seek(self.at())
                    if self.isValid():
                        pos = self.at()
                    else:
                        pos = 0

        return pos




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

    @decorators.BetaImplementation
    def setNull(self, name):
        self.d.buffer_.setNull(name)

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



    @decorators.NotImplementedWarn
    def aqWasDeleted(self):
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

    @QtCore.pyqtSlot(int, int)
    @QtCore.pyqtSlot(int)
    def selection_currentRowChanged(self, current, previous = None):
        if self.d._currentregister == current.row(): return False
        self.d._currentregister = current.row()
        self.d._current_changed.emit(self.at())
        print("cursor:%s , row:%d" %(self._action.table, self.d._currentregister ))


    def at(self):
        if not self.d._currentregister:
            row = 0
        else:
            row = self.d._currentregister

        if row < 0: return -1
        if row >= self.model().rows: return -2
        #print("%s.Row %s ----> %s" % (self.curName(), row, self))
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
            self.d.persistentFilter_ = None
            if not self.d.cursorRelation_.metadata():
                return
            if self.d.cursorRelation_.metadata().primaryKey() == fN and self.d.cursorRelation_.modeAccess() == self.Insert:
                return
            if not fN or self.d.relation_.foreignField() == fN:
                self.d.buffer_ = None
                self.refreshDelayed(500)
        else:
            self.select()
            pos = self.atFrom()
            if pos > self.size():
                pos = self.size() - 1

            if not self.seek(pos, False, True):
                self.d.buffer_ = None
                self.newBuffer.emit()


    """
    Actualiza el conjunto de registros con un retraso.

    Acepta un lapsus de tiempo en milisegundos, activando el cronómetro interno para
    que realize el refresh definitivo al cumplirse dicho lapsus.

    @param msec Cantidad de tiempo del lapsus, en milisegundos.
    """
    @QtCore.pyqtSlot()
    def refreshDelayed(self, msec = 50):

        if not self._refreshDelayedTimer:
            time = QtCore.QTimer()
            time.singleShot(msec, self.refreshDelayed)
            self._refreshDelayedTimer = True
            return

        self._refreshDelayedTimer = False

        #if not self.d.timer_:
        #    return
        #self.d.timer_.start(msec)
        #cFilter = self.filter()
        #self.setFilter(None)
        #if cFilter == self.filter() and self.isValid():
        #    return

        self.select()
        pos = self.atFrom()
        if not self.seek(pos, False, True):
            self.newBuffer.emit()
        else:
            if self.d.cursorRelation_ and self.d.relation_ and self.d.cursorRelation_.metadata():
                v = self.valueBuffer(self.d.relation_.field())
                if not self.d.cursorRelation_.valueBuffer(self.d.relation_.foreignField()) == v:
                    self.d.cursorRelation_.setValueBuffer(self.d.relation_.foreignField(), v)





    def primeInsert(self):
         return PNBuffer(self.d)

    def primeUpdate(self):
        self.d.buffer_.primeUpdate(self.at())


    def editBuffer(self, b = None):

        if not self.d.buffer_:
            self.d.buffer_ = PNBuffer(self.d)
        self.primeUpdate()



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
    def refreshBuffer(self):
        if not self.d.metadata_:
            return False

        if not self.isValid() and not self.d.modeAccess_ == self.Insert:
            return False

        if self.d.modeAccess_ == self.Insert:
            if not self.commitBufferCursorRelation():
                return False

            if not self.d.buffer_:
                self.d.buffer_ = PNBuffer(self.d)
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
            if not self.commitBufferCursorRelation():
                return False

            if self.isLocked() and self.d.acosCondName_.isEmpty():
                self.d.modeAccess_ = self.Browse

            if not self.d.buffer_:
                self.d.buffer_ = PNBuffer(self.d)

            self.d.buffer_.primeUpdate(self.at())
            self.setNotGenerateds()
            self.updateBufferCopy()
            self.newBuffer.emit()

        elif self.d.modeAccess_ == self.Del:
            if self.isLocked():
                self.d.msgboxWarning("Registro bloqueado, no se puede eliminar")
                self.d.modeAccess_ = self.Browse
                return False

            if self.d.buffer_:
                self.d.buffer_.primeDelete()
                self.setNoGenerateds()
                self.updateBufferCopy()

        elif self.d.modeAccess_ == self.Browse:
            self.editBuffer(True)
            self.setNoGenerateds()
            self.newBuffer.emit()



        return True


    @decorators.NotImplementedWarn
    def setNoGenerateds(self):
        pass


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
    def seek(self, i, relative = None, emite = None):
        return False
    """
        if self.d.modeAccess_ == self.Del:
            return False

        b = False

        if not self.d.buffer_:
            b = True


        if b and emite:
            self.currentChanged(self.at())

        if b:
            return self.refreshBuffer()

        else:
            print("FLSqlCursor.seek(): buffer principal =", self.d.buffer_.md5Sum())

        return False


    """

    """
    Redefinicion del método next() de QSqlCursor.

    Este método simplemente invoca al método next() original de QSqlCursor() y refresca el
    buffer con el metodo FLSqlCursor::refreshBuffer().

    @param emit Si TRUE emite la señal FLSqlCursor::currentChanged()
    """
    @QtCore.pyqtSlot()
    @QtCore.pyqtSlot(bool)
    def next(self,  emite = True):
        if self.d.modeAccess_ == self.Del:
            return False

        b = self.moveby(1)

        if b and emite:
            self.d._current_changed.emit(self.at())

        if b:
            return self.refreshBuffer()

        return b

    def moveby(self, pos):
        if self.d._currentregister:
            pos += self.d._currentregister
        return self.move(pos)

    """
    Redefinicion del método prev() de QSqlCursor.

    Este método simplemente invoca al método prev() original de QSqlCursor() y refresca
    el buffer con el metodo FLSqlCursor::refreshBuffer().

    @param emit Si TRUE emite la señal FLSqlCursor::currentChanged()
    """
    @QtCore.pyqtSlot()
    @QtCore.pyqtSlot(bool)
    def prev(self, emite = True):
        if self.d.modeAccess_ == self.Del:
            return False

        b = self.moveby(-1)

        if b and emite:
            self.d._current_changed.emit(self.at())

        if b:
            return self.refreshBuffer()

        return b


    """
    Mueve el cursor por la tabla:
    """

    def move(self, row):
        if row < 0: row = -1
        if row >= self.d._model.rows: row = self.d._model.rows
        if self.d._currentregister == row: return False
        topLeft = self.d._model.index(row,0)
        bottomRight = self.d._model.index(row,self.d._model.cols-1)
        new_selection = QtGui.QItemSelection(topLeft, bottomRight)
        self._selection.select(new_selection, QtGui.QItemSelectionModel.ClearAndSelect)
        self.d._currentregister = row
        #self.d._current_changed.emit(self.at())
        if row < self.d._model.rows and row >= 0: return True
        else: return False

    """
    Redefinicion del método first() de QSqlCursor.

    Este método simplemente invoca al método first() original de QSqlCursor() y refresca el
    buffer con el metodo FLSqlCursor::refreshBuffer().

    @param emit Si TRUE emite la señal FLSqlCursor::currentChanged()
    """

    @QtCore.pyqtSlot()
    @QtCore.pyqtSlot(bool)
    def first(self,  emite = True):
        if self.d.modeAccess_ == self.Del:
            return False

        b = self.move(0)

        if b and emite:
            self.d._current_changed.emit(self.at())

        if b:
            return self.refreshBuffer()

        return b



    """
    Redefinicion del método last() de QSqlCursor.

    Este método simplemente invoca al método last() original de QSqlCursor() y refresca el
    buffer con el metodo FLSqlCursor::refreshBuffer().

    @param emit Si TRUE emite la señal FLSqlCursor::currentChanged()
    """
    @QtCore.pyqtSlot()
    @QtCore.pyqtSlot(bool)
    def last(self, emite = True):
        if self.d.modeAccess_ == self.Del:
            return False

        b = self.move(self.d._model.rows-1)

        if b and emite:
            self.d._current_changed.emit(self.at())

        if b:
            return self.refreshBuffer()

        return b


    """
    Redefinicion del método del() de QSqlCursor.

    Este método invoca al método del() original de QSqlCursor() y comprueba si hay borrado
    en cascada, en caso afirmativo borrar también los registros relacionados en cardinalidad 1M.
    """
    @QtCore.pyqtSlot()
    def __del__(self, invalidate = True):
        delMtd = None
        if self.d.metadata_ and not self.d.metadata_.inCache():
            delMtd = True

        mtd = self.d.metadata_
        if self.d.transactionsOpened_:
            t = self.name()
            if self.d.metadata_:
                t = self.d.metadata_.name()
                msg = "Se han detectado transacciones no finalizadas en la última operación.\nSe van a cancelar las transacciones pendientes.\nLos últimos datos introducidos no han sido guardados, por favor\nrevise sus últimas acciones y repita las operaciones que no\nse han guardado.\nSqlCursor::~SqlCursor: %s\n" % t
            self.rollbackOpened(-1, msg)

        del self.d
        if delMtd:
            del mtd

        #self.d.countRefCursor = self.d.countRefCursor - 1     FIXME




    """
    Redefinicion del método select() de QSqlCursor
    """
    @QtCore.pyqtSlot()
    @decorators.Incomplete
    def select(self, _filter = None, sort = None ): #sort = QtCore.QSqlIndex()

        if not self.d.metadata_:
            return False

        bFilter = self.baseFilter()
        finalFilter = bFilter
        if _filter:
            if bFilter:
                if not _filter in bFilter:
                    finalFilter = "%s AND %s" % (bFilter, _filter)
                else:
                    finalFilter = bFilter

            else:
                finalFilter = _filter

        self.setMainFilter(finalFilter , False)
        self.d._model.refresh()

        self.newBuffer.emit()







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
    def baseFilter(self):
        relationFilter = None
        finalFilter = "1 = 1"

        if self.d.cursorRelation_ and self.drelation_ and self.d.metadata_ and self.d.cursorRelation_.metadata():

            fgValue = self.d.cursorRelation_.valueBuffer(self.d.relation_.foreignField())
            field = self.d.metadata_.field(self.d.relation_.field())

            if field and fgValue:
                relationFilter = self.d.db_.manager().formatAssignValue(field, fgValue, True)
                filterAc = self.d.cursorRelation_.filterAssoc(self.d.relation_.foreignField(), self.d.metadata_)

                if filterAc:
                    if not relationFilter:
                        relationFilter = filterAc
                    else:
                        relationFilter = "%s AND %s" % (relationFilter, filterAc)

        if self.mainFilter():
            finalFilter = self.mainFilter()

        if relationFilter:
            if not finalFilter:
                finalFilter = relationFilter
            else:
                if not relationFilter in finalFilter:
                    finalFilter = "%s AND %s" % (finalFilter, relationFilter)

        return finalFilter





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
        if bFilter:
            if not finalFilter:
                finalFilter = bFilter
            elif finalFilter in bFilter:
                finalFilter = bFilter
            elif not bFilter in finalFilter:
                finalFilter = bFilter + " AND " + finalFilter

        if finalFilter and self.d.persistentFilter_ and not self.d.persistentFilter_ in finalFilter:
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
    def editRecord(self):
        print("Edit the row!", self.actionName())
        if self.d.needUpdate():
            pKN = self.d.metadata_.primaryKey()
            pKValue = self.valueBuffer(pKN)
            self.refresh()
            pos = self.atFromBinarySearch(pKN, pKValue)
            if not pos == self.at():
                self.seek(pos, False, False)

        self.openFormInMode(self.Edit)

    """
    Abre el formulario de edicion de registro definido en los metadatos (FLTableMetaData) listo
    para sólo visualizar el registro activo del cursor.
    """
    @QtCore.pyqtSlot()
    def browseRecord(self):
        print("Inspect, inspect!", self.actionName())
        if self.d.needUpdate():
            pKN = self.d.metadata_.primaryKey()
            pKValue = self.valueBuffer(pKN)
            self.refresh()
            pos = self.atFromBinarySearch(pKN, pKValue)
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
    @decorators.BetaImplementation
    def commitBuffer(self, emite = True, checkLocks = False):
        if not self.d.buffer_ or not self.d.metadata_:
            return False

        if self.d.db_.interactiveGUI() and self.d.db_.canDetectLocks() and (checkLocks or self.d.metadata_.detectLocks()):
            self.checkRisksLocks()
            if self.d.inRisksLocks_ and QtGui.QMessageBox.No == QtGui.QMessageBox.warning(None, "Bloqueo inminente", "Los registros que va a modificar están bloqueados actualmente,\nsi continua hay riesgo de que su conexión quede congelada hasta finalizar el bloqueo.\n\n¿ Desa continuar aunque exista riesgo de bloqueo ?", QtGui.QMessageBox.Ok, QtGui.QMessageBox.No | QtGui.QMessageBox.Default | QtGui.QMessageBox.Escape):
                return False

        if not self.checkIntegrity():
            return False


        fieldNameCheck = None

        if self.d.modeAccess_ == self.Edit or self.d.modeAccess_ == self.Insert:
            fieldList = self.d.metadata_.fieldListObject()

            for field in fieldList:
                if field.isCheck():
                    fieldNameCheck = field.name()
                    self.d.buffer_.setGenerated(fieldNameCheck, False)
                    if self.d.bufferCopy_:
                        self.d.bufferCopy_.setGenerated(fieldNameCheck, False)
                    continue

                if not self.d.buffer_.isGenerated(field.name()):
                    continue

                if self.d.ctxt_ and field.calculated():
                    v = None
                    try:
                        v = self.d.ctxt_.calculateField(field.name())
                    except Exception:
                        print("FLSqlCursor.commitBuffer(): EL campo %s es calculado, pero no se ha calculado nada" % field.name())

                    if v:
                        self.setValueBuffer(field.name(), v)


        functionBefore = None
        functionAfter = None
        if not self.d.modeAccess_ == FLSqlCursor.Browse and self.d.activatedCommitActions_:
            idMod = self.d.db_.managerModules().idModuleOfFile("%s.%s" % (self.d.metadata_.name(),"mtd"))

            if idMod:
                functionBefore = "%s.iface.beforeCommit_%s" % (idMod, self.d.metadata_.name())
                functionAfter = "%s.iface.afterCommit_%s" % (idMod, self.d.metadata_.name())
            else:
                functionBefore = "sys.iface.beforeCommit_%s" % self.d.metadata_.name()
                functionAfter = "sys.iface.afterCommit_%s" % self.d.metadata_.name()

            if functionBefore:
                cI = self.d.ctxt_
                v = self._prj.call(functionBefore, [self], cI)
                if v and not isinstance(v ,bool):
                    return False

        if not self.checkIntegrity():
            return

        pKN = self.d.metadata_.primaryKey()
        updated = False
        savePoint = None

        if self.d.modeAccess_ == self.Insert:
            if self.d.cursorRelation_ and self.d.relation_:
                if self.d.cursorRelation_.metadata():
                    self.setValueBuffer(self.d.relation_.field(), self.d.cursorRelation_.valueBuffer(self.d.relation_.foreignField()))
                    self.d.cursorRelation_.setAskForCancelChanges(True)

            pkWhere = self.d.db_.manager().formatAssignValue(self.d.metadata_.field(pKN), self.valueBuffer(pKN))
            #self.insert(False)
            self.update(False) # NOTE: la funcion insert no está implementada. Tampoco tiene porqué tener dos funciones distintas.
            if not self.d.db_.canSavePoint():
                if self.d.db_.currentSavePoint_:
                    self.d.db_.currentSavePoint_.saveInsert(pKN, self.d.buffer_, self)


            if not functionAfter and self.d.activatedCommitActions_:
                if not savePoint:
                    savePoint = FLSqlSavePoint(None)
                savePoint.saveInsert(pKN, self.d.buffer_, self)


                if not self.d.persistentFilter_:
                    self.d.persistentFilter_ = pkWhere
                else:
                    if not pkWhere in self.d.persistentFilter_:
                        self.dl.persistentFilter_ = "%s OR %s" % (self.d.persistentFilter_, pkWhere)

            updated = True

        elif self.d.modeAccess_ == self.Edit:
            if not self.d.db_.canSavePoint():
                if self.d.db_.currentSavePoint_:
                    self.d.db_.currentSavePoint_.saveEdit(pKN, self.d.bufferCopy_, self)

            if functionAfter and self.d.activatedCommitActions_:
                if not savePoint:
                    savePoint = FLSqlSavePoint(None)
                savePoint.saveEdit(pKN, self.d.bufferCopy_, self)

            if self.d.cursorRelation_ and self.d.relation_:
                if self.d.cursorRelation_.metadata():
                    self.d.cursorRelation_.setAskForCancelChanges(True)
            print("FLSqlCursor -- commitBuffer -- Edit . 20 . ")
            if self.isModifiedBuffer():
                #i = 0
                #while i < self.d.buffer_.count():
                #    if self.d.buffer_.value(i) == self.d.bufferCopy_.value(i) and self.d.buffer_.isNull(i) and self.d.bufferCopy_.isNull(i):
                #        self.d.buffer_.setGenerated(i, False)

                #    i = i +1

                print("FLSqlCursor -- commitBuffer -- Edit . 22 . ")
                self.update(False)
                #i = 0
                #while i < self.d.buffer_.count():
                #    self.d.buffer_.setGenerated(i, True)
                #    i = i + 1

                print("FLSqlCursor -- commitBuffer -- Edit . 25 . ")

                updated = True
                self.setNotGenerateds()
            print("FLSqlCursor -- commitBuffer -- Edit . 30 . ")


        elif self.d.modeAccess_ == self.Del:
            if not self.d.db_.canSavePoint():
                if self.d.db_.currentSavePoint_:
                    self.d.db_.currentSavePoint_.saveDel(pKN, self.d.bufferCopy_, self)

            if functionAfter and self.d.activatedCommitActions_:
                if not savePoint:
                    savePoint = fllegacy.FLSqlSavePoint.FLSqlSavePoint(None)
                savePoint.saveDel(pKN, self.d.bufferCopy_, self)

            if self.d.cursorRelation_ and self.d.relation_:
                if self.d.cursorRelation_.metadata():
                    self.d.cursorRelation_.setAskForCancelChanges(True)
                #self.del(False) FIXME?
                updated = True


        if updated and self.lastError():
            if savePoint == True:
                del savePoint
            return False

        if not self.d.modeAccess_ == self.Browse and functionAfter and self.d.activatedCommitActions_:
            #cI = FLSqlCursorInterface::sqlCursorInterface(this) FIXME
            cI = self.d.ctxt_
            v = self._prj.call(functionAfter, [self], cI)
            if v and not isinstance(v ,bool):
                print(21)
                if savePoint == True:
                    savePoint.undo()
                    del savePoint

                return False

        if savePoint == True:
            del savePoint

        self.d.modeAccess_ = self.Browse
        if updated == True:
            if fieldNameCheck:
                self.d.buffer_.setGenerated(fieldNameCheck, True)
                if self.d.bufferCopy_:
                    self.d.bufferCopy_.setGenerated(fieldNameCheck, True)

            self.setFilter(None)
            self.clearMapCalcFields()

        if updated == True and emite == True:
            self.cursorUpdated.emit()

        self.bufferCommited.emit()

        return True

    """
    Manda el contenido del buffer del cursor relacionado a dicho cursor.

    Hace efectivos todos los cambios en el buffer del cursor relacionado posiconándose en el registro
    correspondiente que recibe los cambios.
    """
    @QtCore.pyqtSlot()
    def commitBufferCursorRelation(self):
        ok = True
        activeWid = QtGui.qApp.activeModalWidget()
        if not activeWid:
            activeWid = QtGui.qApp.activePopupWidget()
        if not activeWid:
            activeWid = QtGui.qApp.activeWindow()

        activeWidEnabled = False
        if activeWid:
            activeWidEnabled = activeWid.isEnabled()

        if self.d.modeAccess_ == self.Insert:
            if self.d.cursorRelation_ and self.d.relation_:
                if self.d.cursorRelation_.metadata() and self.d.cursorRelation_.modeAccess() == self.Insert:


                    if activeWid and activeWidEnabled:
                        activeWid.setEnabled(False)

                    if not self.d.cursorRelation_.commitBuffer():
                        self.d.modeAccess_ = self.Browse
                        ok = False
                    else:
                        self.setFilter(None)
                        self.d.cursorRelation_.refresh()
                        self.d.cursorRelation_.setModeAccess(self.Edit)
                        self.d.cursorRelation_.refreshBuffer()

                    if activeWid and activeWidEnabled:
                        activeWid.setEnabled(True)

        if self.d.modeAccess_ == self.Browse or self.d.modeAccess_ == self.Edit:
            if self.d.cursorRelation_ and self.d.relation_:
                if self.d.cursorRelation_.metadata() and self.d.cursorRelation_.modeAccess() == self.Insert:
                    if activeWid and activeWidEnabled:
                        activeWid.setEnabled(False)

                    if not self.d.cursorRelation_.commitBuffer():
                        self.d.modeAccess_ = self.Browse
                        ok = False
                    else:
                        self.d.cursorRelation_.refresh()
                        self.d.cursorRelation_.setModeAccess(self.Edit)
                        self.d.cursorRelation_.refreshBuffer()

                    if activeWid and activeWidEnabled:
                        activeWid.setEnabled(True)

        return ok





    """
    @return El nivel actual de anidamiento de transacciones, 0 no hay transaccion
    """
    @QtCore.pyqtSlot()
    def transactionLevel(self):
        if self.d.db_:
            return self.d.db_.transaction_
        else:
            return 0


    """
    @return La lista con los niveles de las transacciones que ha iniciado este cursor y continuan abiertas
    """
    @QtCore.pyqtSlot()
    def transactionsOpened(self):
        lista = []
        for it in self.d.transactionsOpened_:
            lista.append(str(it))

        return lista


    """
    Deshace transacciones abiertas por este cursor.

    @param count  Cantidad de transacciones a deshacer, -1 todas.
    @param msg    Cadena de texto que se muestra en un cuadro de diálogo antes de deshacer las transacciones.
                Si es vacía no muestra nada.
    """
    @QtCore.pyqtSlot()
    def rollbackOpened(self, count = -1, msg = None):
        ct = None
        if count < 0:
            ct = self.d.transactionsOpened_.count()
        else:
            ct = count

        if ct > 0 and msg:
            t = None
            if self.d.metadata_:
                t = self.d.metadata_.name()
            else:
                t = self.name()

            m = "%sSqLCursor::rollbackOpened: %s %s" % (msg, count, t)
            self.d.msgBoxWarning(m, False)
        elif ct > 0:
            print("SqLCursor::rollbackOpened: %s %s" % (count, self.name))

        i = 0
        while i < ct:
            print("FLSqlCursor : Deshaciendo transacción abierta", self.transactionLevel())
            self.rollback()





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


    def clearMapCalcFields(self):
        self.d.mapCalcFields_ = []

    @decorators.NotImplementedWarn
    def valueBufferRaw(self, fN):
        return True

    @decorators.NotImplementedWarn
    def sort(self):
        return None

    @decorators.NotImplementedWarn
    def list(self):
        return None

    def filter(self):
        return self.d.filter_

    """
    Actualiza tableModel con el buffer
    """
    def update(self, notify):
        print("FLSqlCursor.update --- BEGIN")
        if self.modeAccess() == FLSqlCursor.Edit:
            # solo los campos modified
            lista = self.d.buffer_.modifiedFields()
            # TODO: pKVaue debe ser el valueBufferCopy, es decir, el antiguo. Para
            # .. soportar updates de PKey, que, aunque inapropiados deberían funcionar.
            pKValue = self.d.buffer_.value(self.d.buffer_.pK())

            dict_update = dict([(fieldName, self.d.buffer_.value(fieldName)) for fieldName in lista])

            try:
                update_successful = self.model().updateValuesDB(pKValue, dict_update)
            except Exception:
                print("FLSqlCursor.update:: Unhandled error on model updateRowDB:: ", traceback.format_exc())
                update_successful = False
            # TODO: En el futuro, si no se puede conseguir un update, hay que "tirar atrás" todo.
            if update_successful:
                row = self.model().findPKRow([pKValue])
                if row is not None:
                    if self.model().value(row, self.model().pK()) != pKValue:
                        raise AssertionError("Los indices del CursorTableModel devolvieron un registro erroneo: %r != %r" % (self.model().value(row, self.model().pK()), pKValue))
                    self.model().setValuesDict(row, dict_update)

                else:
                    # Método clásico
                    print("FLSqlCursor.update :: WARN :: Los indices del CursorTableModel no funcionan o el PKey no existe.")
                    row = 0
                    while row < self.model().rowCount():
                        if self.model().value(row, self.model().pK()) == pKValue:
                            for fieldName in lista:
                                self.model().setValue(row, fieldName, self.d.buffer_.value(fieldName))

                            break

                        row = row + 1

            if notify:
                self.bufferCommited.emit()


        elif self.modeAccess() == FLSqlCursor.Insert:
            self.model().newRowFromBuffer(self.d.buffer_)

            if notify:
                self.bufferCommited.emit()
        print("FLSqlCursor.update --- END")

    """
    Indica el último error
    """
    @decorators.NotImplementedWarn
    def lastError(self):
        return None
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
from pineboolib.fllegacy.FLUtil import FLUtil
