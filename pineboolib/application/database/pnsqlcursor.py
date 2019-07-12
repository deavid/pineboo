# -*- coding: utf-8 -*-
import weakref
import importlib
from typing import Any, Optional, TYPE_CHECKING

from PyQt5 import QtCore  # type: ignore
from pineboolib.interfaces.cursoraccessmode import CursorAccessMode
from pineboolib.application.database.pnsqlquery import PNSqlQuery
from pineboolib.application import project
from pineboolib.application.utils.xpm import cacheXPM

from pineboolib.core import decorators
from pineboolib.core.utils import logging
from pineboolib.fllegacy.flapplication import aqApp

from .pnbuffer import PNBuffer

# FIXME: Removde dependency: Should not import from fllegacy.*
from pineboolib.fllegacy.flaccesscontrolfactory import FLAccessControlFactory  # FIXME: Removde dependency

from pineboolib.fllegacy import fltablemetadata

if TYPE_CHECKING:
    from .pncursortablemodel import PNCursorTableModel


logger = logging.getLogger(__name__)


class PNCursorPrivate(QtCore.QObject):

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
    metadata_: "fltablemetadata.FLTableMetaData" = None

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
    browse_states_ = []

    """
    Filtro principal para el cursor.

    Este filtro persiste y se aplica al cursor durante toda su existencia,
    los filtros posteriores, siempre se ejecutaran unidos con 'AND' a este.
    """
    # self.d._model.where_filters["main-filter"] = None

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
    Orden actual
    """
    sort_ = None
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
    aclDone_ = False
    idAc_ = 0
    idAcos_ = 0
    idCond_ = 0
    id_ = "000"

    """ Uso interno """
    isQuery_ = None
    isSysTable_ = None
    mapCalcFields_ = []
    rawValues_ = None

    md5Tuples_ = None

    countRefCursor = None

    _model: "PNCursorTableModel" = None

    _currentregister = None
    edition_states_ = None

    # filter_ = None

    _current_changed = QtCore.pyqtSignal(int)

    FlagStateList = None
    FlagState = None

    def __init__(self):
        super().__init__()
        self.metadata_ = None
        self.countRefCursor = 0
        self._currentregister = -1
        self.acosCondName_ = None
        self.buffer_ = None
        self.edition_states_ = None
        self.activatedCheckIntegrity_ = True
        self.askForCancelChanges_ = True
        self.transactionsOpened_ = []
        self.cursorRelation_ = None
        self.idAc_ = 0
        self.idAcos_ = 0
        self.idCond_ = 0
        self.id_ = "000"
        self.aclDone_ = False

    def __del__(self):

        if self.metadata_:
            self.undoAcl()

        if self.bufferCopy_:
            del self.bufferCopy_

        if self.relation_:
            del self.relation_

        if self.acTable_:
            del self.acTable_

        if self.edition_states_:
            del self.edition_states_
            # logger.trace("AQBoolFlagState count %s", self.count_)

        if self.browse_states_:
            del self.browse_states_
            # logger.trace("AQBoolFlagState count %s", self.count_)
        if self.transactionsOpened_:
            del self.transactionsOpened_

    def doAcl(self):
        if not self.acTable_:
            self.acTable_ = FLAccessControlFactory().create("table")
            self.acTable_.setFromObject(self.metadata_)
            self.acosBackupTable_ = self.acTable_.getAcos()
            self.acPermBackupTable_ = self.acTable_.perm()
            self.acTable_.clear()

        if self.modeAccess_ == PNSqlCursor.Insert or (not self.lastAt_ == -1 and self.lastAt_ == self.cursor_.at()):
            return

        if self.acosCondName_ is not None:
            condTrue_ = False

            if self.acosCond_ == PNSqlCursor.Value:
                condTrue_ = self.cursor_.valueBuffer(self.acosCondName_) == self.acosCondVal_
            elif self.acosCond_ == PNSqlCursor.RegExp:
                from PyQt5.Qt import QRegExp  # type: ignore

                # FIXME: What is happenning here? bool(str(Regexp)) ??
                condTrue_ = bool(str(QRegExp(str(self.acosCondVal_)).exactMatch(str(self.cursor_.value(self.acosCondName_)))))
            elif self.acosCond_ == PNSqlCursor.Function:
                condTrue_ = project.call(self.acosCondName_, [self.cursor_]) == self.acosCondVal_

            if condTrue_:
                if self.acTable_.name() != self.id_:
                    self.acTable_.clear()
                    self.acTable_.setName(self.id_)
                    self.acTable_.setPerm(self.acPermTable_)
                    self.acTable_.setAcos(self.acosTable_)
                    self.acTable_.processObject(self.metadata_)
                    self.aclDone_ = True

                return

        elif self.cursor_.isLocked() or (self.cursorRelation_ and self.cursorRelation_.isLocked()):
            if not self.acTable_.name() == self.id_:
                self.acTable_.clear()
                self.acTable_.setName(self.id_)
                self.acTable_.setPerm("r-")
                self.acTable_.processObject(self.metadata_)
                self.aclDone_ = True

            return

        self.undoAcl()

    def undoAcl(self):
        if self.acTable_ and self.aclDone_:
            self.aclDone_ = False
            self.acTable_.clear()
            self.acTable_.setPerm(self.acPermBackupTable_)
            self.acTable_.setAcos(self.acosBackupTable_)
            self.acTable_.processObject(self.metadata_)

    def needUpdate(self):
        return False

        if self.isQuery_:
            return False

        need = self._model.need_update
        return need

    def msgBoxWarning(self, msg, throwException=False):
        if project._DGI.localDesktop():
            from pineboolib import pncontrolsfactory

            logger.warning(msg)
            if not throwException:
                pncontrolsfactory.QMessageBox.warning(pncontrolsfactory.QApplication.activeWindow(), "Pineboo", msg)
        else:
            logger.warning(msg)


# ###############################################################################
# ###############################################################################
# ######
# ######
# ######                         PNSqlCursor
# ######
# ######
# ###############################################################################
# ###############################################################################


class PNSqlCursor(QtCore.QObject):

    """
    Insertar, en este modo el buffer se prepara para crear un nuevo registro
    """

    Insert = CursorAccessMode.Insert

    """
    Edición, en este modo el buffer se prepara para editar el registro activo
    """
    Edit = CursorAccessMode.Edit

    """
    Borrar, en este modo el buffer se prepara para borrar el registro activo
    """
    Del = CursorAccessMode.Del

    """
    Navegacion, en este modo solo se puede visualizar el buffer
    """
    Browse = CursorAccessMode.Browse

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

    _iter_current = None

    _refreshDelayedTimer = None
    _action = None

    ext_cursor = None
    _activatedBufferChanged = None
    _activatedBufferCommited = None
    _meta_model = None

    def __init__(self, name=None, autopopulate=True, connectionName_or_db=None, cR=None, r=None, parent=None):

        super().__init__()
        if name is None:
            logger.warning("Se está iniciando un cursor Huerfano (%s). Posiblemente sea una declaración en un qsa parseado", self)
            return

        if isinstance(autopopulate, str):
            connectionName_or_db = autopopulate
            autopopulate = True

        self._meta_model = None
        name_action = None
        self.setActivatedBufferChanged(True)
        self.setActivatedBufferCommited(True)
        ext_cursor = getattr(project._DGI, "FLSqlCursor", None)
        if ext_cursor is not None:
            self.ext_cursor = ext_cursor(self, name)
        else:
            self.ext_cursor = None

        from pineboolib.core.utils.struct import XMLStruct

        if isinstance(name, XMLStruct):
            logger.trace("FIXME::__init__ XMLSTRUCT %s", name.name, stack_info=True)
            name_action = name.name
        else:
            name_action = name

        act_ = project.conn.manager().action(name_action)
        # self.actionName_ = name.name
        # name = name.table
        # else:
        # self.actionName_ = name

        self._valid = False
        self.d = PNCursorPrivate()
        self.d.cursor_ = self
        self.d.nameCursor_ = "%s_%s" % (act_.name(), QtCore.QDateTime.currentDateTime().toString("dd.MM.yyyyThh:mm:ss.zzz"))

        if connectionName_or_db is None:
            self.d.db_ = project.conn
        # elif isinstance(connectionName_or_db, QString) or
        # isinstance(connectionName_or_db, str):
        elif isinstance(connectionName_or_db, str):
            self.d.db_ = project.conn.useConn(connectionName_or_db)
        else:
            self.d.db_ = connectionName_or_db

        # for module in project.modules:
        #    for action in module.actions:
        #        if action.name == name:
        #            self.d.action_ = action
        #            break
        self.init(act_.name(), autopopulate, cR, r)

    """
    Código de inicialización común para los constructores
    """

    def init(self, name, autopopulate, cR, r):
        # logger.warning("FLSqlCursor(%s): Init() %s (%s, %s)" , name, self, cR, r, stack_info=True)

        # if self.metadata() and not self.metadata().aqWasDeleted() and not
        # self.metadata().inCache():

        self.d.curName_ = name
        if self.setAction(name):
            self.d.countRefCursor = self.d.countRefCursor + 1
        else:
            # logger.trace("FLSqlCursor(%s).init(): ¿La tabla no existe?" % name)
            return None

        self.d.modeAccess_ = PNSqlCursor.Browse

        self.d.cursorRelation_ = cR
        if r:  # FLRelationMetaData
            if self.relation() and self.relation().deref():
                del self.d.relation_

            # r.ref()
            self.d.relation_ = r
        else:
            self.d.relation_ = None
        metadata = self.metadata()
        if not metadata:
            return

        # if project._DGI.use_model():
        #    self.build_cursor_tree_dict()

        self.d.isQuery_ = metadata.isQuery()
        if (name[len(name) - 3 :]) == "sys" or self.db().manager().isSystemTable(name):
            self.d.isSysTable_ = True
        else:
            self.d.isSysTable_ = False

        # if self.d.isQuery_:
        #     qry = self.db().manager().query(self.metadata().query(), self)
        #     self.d.query_ = qry.sql()
        #     if qry and self.d.query_:
        #         self.exec_(self.d.query_)
        #     if qry:
        #         self.qry.deleteLater()
        # else:
        #     self.setName(self.metadata().name(), autopopulate)
        self.setName(metadata.name(), autopopulate)

        self.d.modeAccess_ = self.Browse
        if cR and r:
            try:
                cR.bufferChanged.disconnect(self.refresh)
                cR.newBuffer.disconnect(self.refresh)
                # cR.d._current_changed.disconnect(self.refresh)
            except Exception:
                pass
            cR.bufferChanged.connect(self.refresh)
            cR.newBuffer.connect(self.refresh)
            # cR.d._current_changed.connect(self.refresh)
            try:
                cR.newBuffer.disconnect(self.clearPersistentFilter)

            except Exception:
                pass
            cR.newBuffer.connect(self.clearPersistentFilter)
            if (
                project._DGI.use_model() and cR.meta_model()
            ):  # Si el cursor_relation tiene un model asociado , este cursor carga el propio también
                self.assoc_model()

        else:
            self.seek(None)

        if self.d.timer_:
            del self.d.timer_

        self.d.timer_ = QtCore.QTimer(self)
        self.d.timer_.timeout.connect(self.refreshDelayed)

        # if cR:
        #    self.refreshDelayed()
        # self.d.md5Tuples_ = self.db().md5TuplesStateTable(self.d.curName_)
        # self.first()

    def conn(self):
        return self.db()

    def table(self):
        m = self.metadata()
        if m:
            return m.name()
        else:
            return None

    # def __getattr__(self, name):
    #    return DefFun(self, name)

    def setName(self, name, autop):
        self.name = name
        # autop = autopopulate para que??

    """
    Para obtener los metadatos de la tabla.

    @return Objeto FLTableMetaData con los metadatos de la tabla asociada al cursor
    """

    def metadata(self):
        if not getattr(self.d, "metadata_", None):
            logger.trace("PNSqlCursor(%s) Esta devolviendo un metadata vacio", getattr(self, "curName()", None))
            return None
        return self.d.metadata_

    """
    Informa del registro seleccionado actualmente por el cursor
    @retunr int con el número de registro
    """

    def currentRegister(self):
        return self.d._currentregister

    """
    Para obtener el modo de acceso actual del cursor.

    @return Constante PNSqlCursor::Mode que define en que modo de acceso esta preparado
        el buffer del cursor
    """

    def modeAccess(self):
        return self.d.modeAccess_

    """
    Para obtener el filtro principal del cursor.

    @return Cadena de texto con el filtro principal
    """

    def mainFilter(self):
        ret_ = None
        if hasattr(self.model(), "where_filters"):
            ret_ = self.model().where_filters["main-filter"]

        if ret_ is None:
            ret_ = ""

        return ret_

    """
    Para obtener la accion asociada al cursor.

    @return  Objeto FLAction
    """

    def action(self):
        return self._action.name() if self._action else None

    def actionName(self):
        return self._action.name()

    """
    Establece la accion asociada al cursor.

    @param a Objeto FLAction
    """

    def setAction(self, a):
        action = None

        if isinstance(a, str):
            action = self.db().manager().action(a.lower())

            if action.table() == "":
                action.setTable(a)
        else:
            action = a

        if not self._action:
            self._action = action
        else:

            if (
                self._action.table() == action.table()
            ):  # Esto es para evitar que se setee en un FLTableDB con metadata inválido un action sobre un cursor del parentWidget.
                from pineboolib.core.settings import config

                if config.value("application/isDebuggerMode", False):
                    logger.warning(
                        "Se hace setAction sobre un cursor con la misma table %s\nAction anterior: %s\nAction nueva: %s",
                        action.table(),
                        self._action.name(),
                        action.name(),
                    )
                self._action = action
                return

            if self.action() is not None:
                self._action = None
                self.d.buffer_ = None
                self.d.metadata_ = None

                self._action = action

        if not self._action.table():
            return None

        if not self.d.metadata_:
            self.d.metadata_ = self.db().manager().metadata(self._action.table())

        self.d.doAcl()

        from .pncursortablemodel import PNCursorTableModel

        self.d._model = PNCursorTableModel(self.conn(), self)
        if not self.model():
            return None

        if not self.d.buffer_:
            self.primeInsert()

        self._selection = QtCore.QItemSelectionModel(self.model())
        self.selection().currentRowChanged.connect(self.selection_currentRowChanged)
        self._currentregister = self.selection().currentIndex().row()
        self.d.metadata_ = self.db().manager().metadata(self._action.table())
        self.d.activatedCheckIntegrity_ = True
        self.d.activatedCommitActions_ = True
        return True

    """
    Establece el filtro principal del cursor.

    @param f Cadena con el filtro, corresponde con una clausura WHERE
    @param doRefresh Si TRUE tambien refresca el cursor
    """

    def setMainFilter(self, f, doRefresh=True):
        # if f == "":
        #    f = "1 = 1"

        # logger.trace("--------------------->Añadiendo filtro",  f)
        if self.model() and getattr(self.model(), "where_filters", None):
            self.model().where_filters["main-filter"] = f
            if doRefresh:
                self.refresh()

    """
    Establece el modo de acceso para el cursor.

    @param m Constante PNSqlCursor::Mode que indica en que modo de acceso
    se quiere establecer el cursor
    """

    def setModeAccess(self, m):
        self.d.modeAccess_ = m

    """
    Devuelve el nombre de la conexión que el cursor usa

    @return Nombre de la conexión
    """

    def connectionName(self):
        return self.db().connectionName()

    """
    Establece el valor de un campo del buffer de forma atómica y fuera de transacción.

    Invoca a la función, cuyo nombre se pasa como parámetro, del script del contexto del cursor
    (ver PNSqlCursor::ctxt_) para obtener el valor del campo. El valor es establecido en el campo de forma
    atómica, bloqueando la fila durante la actualización. Esta actualización se hace fuera de la transacción
    actual, dentro de una transacción propia, lo que implica que el nuevo valor del campo está inmediatamente
    disponible para las siguientes transacciones.

    @param fN Nombre del campo
    @param functionName Nombre de la función a invocar del script
    """

    def setAtomicValueBuffer(self, fN, functionName) -> None:
        from pineboolib import pncontrolsfactory
        from pineboolib import qsa  # FIXME: Should not import QSA at all

        metadata = self.metadata()
        buffer = self.buffer()
        if not buffer or not fN or not metadata:
            return

        field = metadata.field(fN)

        if field is None:
            logger.warning("setAtomicValueBuffer(): No existe el campo %s:%s", metadata.name(), fN)
            return

        if not self.db().dbAux():
            return

        type = field.type()
        # fltype = FLFieldMetaData.FlDecodeType(type)
        pK = metadata.primaryKey()
        v = None

        if self.cursorRelation() and self.modeAccess() == self.Browse:
            self.cursorRelation().commit(False)

        if pK and self.db().db() is not self.db().dbAux():
            pKV = buffer.value(pK)
            self.db().dbAux().transaction()

            arglist = []
            arglist.append(fN)
            arglist.append(buffer.value(fN))
            v = aqApp.call(functionName, arglist, self.context())

            q = PNSqlQuery(None, self.db().dbAux())
            ret = q.exec_(
                "UPDATE  %s SET %s = %s WHERE %s"
                % (
                    metadata.name(),
                    fN,
                    self.db().manager().formatValue(type, v),
                    self.db().manager().formatAssignValue(metadata.field(pK), pKV),
                )
            )
            if ret:
                self.db().dbAux().commit()
            else:
                self.db().dbAux().rollback()
        else:
            logger.warning("No se puede actualizar el campo de forma atómica, porque no existe clave primaria")

        buffer.setValue(fN, v)
        if self.activatedBufferChanged():
            if project._DGI.use_model() and self.meta_model():
                bch_model = getattr(self.meta_model(), "bChCursor", None)
                if bch_model and bch_model(fN, self) is False:
                    return

                script = getattr(qsa, "formRecord%s" % self.action(), None)
                if script is not None:
                    bChCursor = getattr(script.iface, "bChCursor", None)
                    if bChCursor:
                        bChCursor(fN, self)

            self.bufferChanged.emit(fN)

            pncontrolsfactory.SysType.processEvents(self)

    """
    Establece el valor de un campo del buffer con un valor.

    @param fN Nombre del campo
    @param v Valor a establecer para el campo
    """

    def setValueBuffer(self, fN, v):
        from pineboolib import pncontrolsfactory
        from pineboolib import qsa  # FIXME: Should not import QSA at all

        buffer, metadata = self.buffer(), self.metadata()
        if not buffer or not fN or not metadata:
            logger.warning("setValueBuffer(): No buffer, or no fieldName, or no metadata found")
            return

        field = metadata.field(fN)
        if field is None:
            logger.warning("setValueBuffer(): No existe el campo %s:%s", self.curName(), fN)
            return
        db = self.db()
        manager = db and db.manager()
        if db is None or manager is None:
            raise Exception("no db or no manager")

        type_ = field.type()

        if not buffer.field(fN).has_changed(v):
            return

        # if not self.buffer():  # Si no lo pongo malo....
        #    self.primeUpdate()

        # if not fN or not self.metadata():
        #    return

        # field = self.metadata().field(fN)
        # if field is None:
        #    logger.warning("PNSqlCursor::setValueBuffer() : No existe el campo %s:%s", self.metadata().name(), fN)
        #    return

        # fltype = field.flDecodeType(type_)
        vv = v

        if vv and type_ == "pixmap" and not manager.isSystemTable(self.table()):
            vv = db.normalizeValue(vv)
            largeValue = manager.storeLargeValue(self.metadata(), vv)
            if largeValue:
                vv = largeValue

        if field.outTransaction() and db.db() is not db.dbAux() and self.modeAccess() != self.Insert:
            pK = metadata.primaryKey()

            if self.cursorRelation() and self.modeAccess() != self.Browse:
                self.cursorRelation().commit(False)

            if pK:
                pKV = buffer.value(pK)
                q = PNSqlQuery(None, "dbAux")
                q.exec_(
                    "UPDATE %s SET %s = %s WHERE %s;"
                    % (metadata.name(), fN, manager.formatValue(type_, vv), manager.formatAssignValue(metadata.field(pK), pKV))
                )
            else:
                logger.warning("FLSqlCursor : No se puede actualizar el campo fuera de transaccion, porque no existe clave primaria")

        else:
            buffer.setValue(fN, vv)

        # logger.trace("(%s)bufferChanged.emit(%s)" % (self.curName(),fN))
        if self.activatedBufferChanged():

            if project._DGI.use_model() and self.meta_model():
                bch_model = getattr(self.meta_model(), "bChCursor", None)
                if bch_model and bch_model(fN, self) is False:
                    return

                script = getattr(qsa, "formRecord%s" % self.action(), None)
                if script is not None:
                    bChCursor = getattr(script.iface, "bChCursor", None)
                    if bChCursor:
                        bChCursor(fN, self)

            self.bufferChanged.emit(fN)
        pncontrolsfactory.SysType.processEvents(self)

    """
    Devuelve el valor de un campo del buffer.

    @param fN Nombre del campo
    """

    def valueBuffer(self, fN):
        fN = str(fN)

        if project._DGI.use_model():
            if fN == "pk":
                # logger.warning("¡¡¡¡ OJO Cambiado fieldname PK!!", stack_info = True)
                fN = self.primaryKey()

        if self.d.rawValues_:
            return self.valueBufferRaw(fN)

        if not self.metadata():
            return None

        if (self.model().rows > 0 and not self.modeAccess() == PNSqlCursor.Insert) or not self.buffer():
            if not self.buffer():
                self.refreshBuffer()

            if not self.buffer():
                return None

        field = self.metadata().field(fN)
        if field is None:
            logger.warning("valueBuffer(): No existe el campo %s:%s en la tabla %s", self.curName(), fN, self.metadata().name())
            return None

        type_ = field.type()

        v = None
        if field.outTransaction() and self.db().db() is not self.db().dbAux() and self.modeAccess() != self.Insert:
            pK = self.metadata().primaryKey()
            if not self.buffer():
                return None
            if pK:
                pKV = self.buffer().value(pK)
                q = PNSqlQuery(None, "dbAux")
                sql_query = "SELECT %s FROM %s WHERE %s" % (
                    fN,
                    self.metadata().name(),
                    self.db().manager().formatAssignValue(self.metadata().field(pK), pKV),
                )
                # q.exec_(self.db().dbAux(), sql_query)
                q.exec_(sql_query)
                if q.next():
                    v = q.value(0)
            else:
                logger.warning("No se puede obtener el campo fuera de transacción porque no existe clave primaria")

        else:
            if not self.buffer():
                return None
            v = self.buffer().value(fN)

        if v is not None:
            if type_ in ("date"):
                from pineboolib.application.types import Date

                v = Date(v)
            elif type_ == "pixmap":
                v_large = None
                if not self.db().manager().isSystemTable(self.table()):

                    v_large = self.db().manager().fetchLargeValue(v)

                else:
                    from pineboolib.application.utils.xpm import cacheXPM

                    v_large = cacheXPM(v)

                if v_large:
                    v = v_large
        else:
            if type_ in ("string", "stringlist", "date"):
                v = ""
            elif type_ in ("double", "int", "uint"):
                v = 0

        return v

    def fetchLargeValue(self, value):
        return self.db().manager().fetchLargeValue(value)

    """
    Devuelve el valor de un campo del buffer copiado antes de sufrir cambios.

    @param fN Nombre del campo
    """

    def valueBufferCopy(self, fN):
        if not self.bufferCopy() and fN is None or not self.metadata():
            return None

        field = self.metadata().field(fN)
        if field is None:
            logger.warning("FLSqlCursor::valueBufferCopy() : No existe el campo ") + self.metadata().name() + ":" + fN
            return None

        type_ = field.type()
        bufferCopy = self.bufferCopy()
        if not bufferCopy:
            raise Exception("no bufferCopy")
        v: Any = None
        if bufferCopy.isNull(fN):
            if type_ in ("double", "int", "uint"):
                v = 0
            elif type_ == "string":
                v = ""
        else:
            v = bufferCopy.value(fN)

        if v is not None:
            if type_ in ("date"):
                from pineboolib.application.types import Date

                v = Date(v)

            elif type_ == "pixmap":
                v_large = None
                if not self.db().manager().isSystemTable(self.table()):
                    v_large = self.db().manager().fetchLargeValue(v)
                else:
                    v_large = cacheXPM(v)

                if v_large:
                    v = v_large
        else:
            if type_ in ("string", "stringlist", "date"):
                v = ""
            elif type_ in ("double", "int", "uint"):
                v = 0

        return v

    """
    Establece el valor de FLSqlCursor::edition.

    @param b TRUE o FALSE
    """

    def setEdition(self, b, m: bool = None):
        from pineboolib.fllegacy.aqsobjects.aqsobjectfactory import AQBoolFlagStateList, AQBoolFlagState  # FIXME: Should not depend on AQS

        if m is None:
            self.d.edition_ = b
            return

        state_changes = b is not self.d.edition_

        if state_changes is not None and not self.d.edition_states_:
            self.d.edition_states_ = AQBoolFlagStateList()

        if self.d.edition_states_ is None:
            return

        i = self.d.edition_states_.find(m)
        if not i and state_changes is not None:
            i = AQBoolFlagState()
            i.modifier_ = m
            i.prevValue_ = self.d.edition_
            self.d.edition_states_.append(i)
        elif i:
            if state_changes is not None:
                self.d.edition_states_.pushOnTop(i)
                i.prevValue_ = self.d.edition_
            else:
                self.d.edition_states_.erase(i)

        if state_changes is not None:
            self.d.edition_ = b

    def restoreEditionFlag(self, m):

        if not self.d.edition_states_:
            return

        i = self.d.edition_states_.find(m)

        if i and i == self.d.edition_states_.current():
            self.d.edition_ = i.prevValue_

        if i:
            self.d.edition_states_.erase(i)

    """
    Establece el valor de FLSqlCursor::browse.

    @param b TRUE o FALSE
    """

    def setBrowse(self, b, m=None):
        from pineboolib.fllegacy.aqsobjects.aqsobjectfactory import AQBoolFlagStateList, AQBoolFlagState  # FIXME: Should not depend on AQS

        if not m:
            self.d.browse_ = b
            return

        state_changes = not b == self.d.browse_

        if state_changes is not None and not self.d.browse_states_:
            self.d.browse_states_ = AQBoolFlagStateList()

        if not self.d.browse_states_:
            return

        i = self.d.browse_states_.find(m)
        if not i and state_changes is not None:
            i = AQBoolFlagState()
            i.modifier_ = m
            i.prevValue_ = self.d.browse_
            self.d.browse_states_.append(i)
        elif i:
            if state_changes is not None:
                self.d.browse_states_.pushOnTop(i)
                i.prevValue_ = self.d.browse_
            else:
                self.d.browse_states_.erase(i)

        if state_changes is not None:
            self.d.browse_ = b

    def restoreBrowseFlag(self, m):
        if not self.d.browse_states_:
            return

        i = self.d.browse_states_.find(m)

        if i and i == self.d.browse_states_.current():
            self.d.browse_ = i.prevValue_

        if i:
            self.d.browse_states_.erase(i)

    def meta_model(self):
        return self._meta_model if project._DGI.use_model() else None

    """
    Establece el contexto de ejecución de scripts, este puede ser del master o del form_record

    Ver FLSqlCursor::ctxt_.

    @param c Contexto de ejecucion
    """

    def setContext(self, c=None):
        if c:
            self.d.ctxt_ = weakref.ref(c)

    """
    Para obtener el contexto de ejecución de scripts.

    Ver FLSqlCursor::ctxt_.

    @return Contexto de ejecución
    """

    def context(self):
        if self.d.ctxt_:
            return self.d.ctxt_()
        else:
            logger.debug("%s.context(). No hay contexto" % self.curName())
            return None

    """
    Dice si un campo está deshabilitado.

    Un campo estará deshabilitado, porque esta clase le dará un valor automáticamente.
    Estos campos son los que están en una relación con otro cursor, por lo que
    su valor lo toman del campo foráneo con el que se relacionan.

    @param fN Nombre del campo a comprobar
    @return TRUE si está deshabilitado y FALSE en caso contrario
    """

    def fieldDisabled(self, fN):
        if self.modeAccess() in (self.Insert, self.Edit):
            if self.cursorRelation() and self.relation():
                if not self.cursorRelation().metadata():
                    return False
                if str(self.relation().field()).lower() == str(fN).lower():
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
        if self.db():
            if self.db().transaction_ > 0:
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

    def transaction(self, lock=False):
        if not self.db() and not self.db().db():
            logger.warning("transaction(): No hay conexión con la base de datos")
            return False

        return self.db().doTransaction(self)

    """
    Deshace las operaciones de una transacción y la acaba.

    @return TRUE si la operación tuvo exito
    """

    def rollback(self):
        if not self.db() and not self.db().db():
            logger.warning("rollback(): No hay conexión con la base de datos")
            return False

        return self.db().doRollback(self)

    """
    Hace efectiva la transacción y la acaba.

    @param notify Si TRUE emite la señal cursorUpdated y pone el cursor en modo BROWSE,
          si FALSE no hace ninguna de estas dos cosas y emite la señal de autoCommit
    @return TRUE si la operación tuvo exito
    """

    def commit(self, notify=True):
        if not self.db() and not self.db().db():
            logger.warning("commit(): No hay conexión con la base de datos")
            return False

        r = self.db().doCommit(self, notify)
        if r:
            self.commited.emit()

        return r

    def size(self):
        return self.model().size()

    """
    Abre el formulario asociado a la tabla origen en el modo indicado.

    @param m Modo de apertura (FLSqlCursor::Mode)
    @param wait Indica que se espera a que el formulario cierre para continuar
    @param cont Indica que se abra el formulario de edición de registros con el botón de
         aceptar y continuar
    """

    def openFormInMode(self, m: int, wait: bool = True, cont: bool = True):
        if not self.metadata():
            return
        from pineboolib import pncontrolsfactory

        if (not self.isValid() or self.size() <= 0) and not m == self.Insert:
            if not self.size():
                pncontrolsfactory.QMessageBox.warning(
                    pncontrolsfactory.QApplication.focusWidget(), self.tr("Aviso"), self.tr("No hay ningún registro seleccionado")
                )
                return
            self.first()

        if m == self.Del:
            res = pncontrolsfactory.QMessageBox.warning(
                pncontrolsfactory.QApplication.focusWidget(),
                self.tr("Aviso"),
                self.tr("El registro activo será borrado. ¿ Está seguro ?"),
                pncontrolsfactory.QMessageBox.Ok,
                pncontrolsfactory.QMessageBox.No,
            )
            if res == pncontrolsfactory.QMessageBox.No:
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
        if self.buffer():
            self.buffer().clearValues(True)

        # if not self.d._action:
        # self.d.action_ = self.db().manager().action(self.metadata().name())

        if not self._action:
            logger.warning(
                "Para poder abrir un registro de edición se necesita una acción asociada al cursor, "
                "o una acción definida con el mismo nombre que la tabla de la que procede el cursor."
            )
            return

        if not self._action.formRecord():
            pncontrolsfactory.QMessageBox.warning(
                pncontrolsfactory.QApplication.focusWidget(),
                self.tr("Aviso"),
                self.tr("No hay definido ningún formulario para manejar\nregistros de esta tabla : %s" % self.curName()),
            )
            return

        if self.refreshBuffer():  # Hace doTransaction antes de abrir formulario y crear savepoint
            if m != self.Insert:
                self.updateBufferCopy()

            project.actions[self._action.name()].openDefaultFormRecord(self, wait)

            # if m != self.Insert and self.refreshBuffer():
            #     self.updateBufferCopy()

    def isNull(self, fN):
        buffer = self.buffer()
        if not buffer:
            raise Exception("No buffer set")
        return buffer.isNull(fN)

    def isCopyNull(self, fN):
        buffer_copy = self.bufferCopy()
        if not buffer_copy:
            raise Exception("No buffer_copy set")
        return buffer_copy.isNull(fN)

    """
    Copia el contenido del FLSqlCursor::buffer_ actual en FLSqlCursor::bufferCopy_.

    Al realizar esta copia se podra comprobar posteriormente si el buffer actual y la copia realizada
    difieren mediante el metodo FLSqlCursor::isModifiedBuffer().
    """

    def updateBufferCopy(self):
        if not self.buffer():
            return None

        if self.d.bufferCopy_:
            del self.d.bufferCopy_

        self.d.bufferCopy_ = PNBuffer(self)
        bufferCopy = self.bufferCopy()
        if bufferCopy is None:
            raise Exception("No buffercopy")

        for field in self.d.buffer_.fieldsList():
            bufferCopy.setValue(field.name, self.d.buffer_.value(field.name), False)

    """
    Indica si el contenido actual del buffer difiere de la copia guardada.

    Ver FLSqlCursor::bufferCopy_ .

    @return TRUE si el buffer y la copia son distintas, FALSE en caso contrario
    """

    def isModifiedBuffer(self):
        if not self.buffer():
            return False

        modifiedFields = self.buffer().modifiedFields()
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

    def setActivatedBufferChanged(self, activated_bufferchanged):
        self._activatedBufferChanged = activated_bufferchanged

    def activatedBufferChanged(self):
        return self._activatedBufferChanged

    def setActivatedBufferCommited(self, activated_buffercommited):
        self._activatedBufferCommited = activated_buffercommited

    def activatedBufferCommited(self):
        return self._activatedBufferCommited

    """
    Se comprueba la integridad referencial al intentar borrar, tambien se comprueba la no duplicidad de
    claves primarias y si hay nulos en campos que no lo permiten cuando se inserta o se edita.
    Si alguna comprobacion falla devuelve un mensaje describiendo el fallo.
    """

    def msgCheckIntegrity(self):
        msg = ""
        if not self.buffer() or not self.metadata():
            msg = "\nBuffer vacío o no hay metadatos"
            return msg

        if self.d.modeAccess_ == self.Insert or self.d.modeAccess_ == self.Edit:
            if not self.isModifiedBuffer() and self.d.modeAccess_ == self.Edit:
                return msg
            fieldList = self.metadata().fieldList()
            checkedCK = False

            if not fieldList:
                return msg

            for field in fieldList:

                fiName = field.name()
                if not self.buffer().isGenerated(fiName):
                    continue

                s = None
                if not self.buffer().isNull(fiName):
                    s = self.buffer().value(fiName)

                fMD = field.associatedField()
                if fMD and s is not None:
                    if not field.relationM1():
                        msg = (
                            msg + "\n" + "FLSqlCursor : Error en metadatos, el campo %s tiene un campo asociado pero no existe "
                            "relación muchos a uno:%s" % (self.metadata().name(), fiName)
                        )
                        continue

                    r = field.relationM1()
                    if not r.checkIn():
                        continue
                    tMD = self.db().manager().metadata(field.relationM1().foreignTable())
                    if not tMD:
                        continue
                    fmdName = fMD.name()
                    ss = None
                    if not self.buffer().isNull(fmdName):
                        ss = self.buffer().value(fmdName)
                        # if not ss:
                        #     ss = None
                    if ss:
                        filter = "%s AND %s" % (
                            self.db().manager().formatAssignValue(field.associatedFieldFilterTo(), fMD, ss, True),
                            self.db().manager().formatAssignValue(field.relationM1().foreignField(), field, s, True),
                        )
                        q = PNSqlQuery(None, self.db().connectionName())
                        q.setTablesList(tMD.name())
                        q.setSelect(field.associatedFieldFilterTo())
                        q.setFrom(tMD.name())
                        q.setWhere(filter)
                        q.setForwardOnly(True)
                        q.exec_()
                        if not q.next():
                            msg = msg + "\n" + self.metadata().name() + ":" + field.alias() + " : %s no pertenece a %s" % (s, ss)
                        else:
                            self.buffer().setValue(fmdName, q.value(0))

                    else:
                        msg = msg + "\n" + self.metadata().name() + ":" + field.alias() + " : %s no se puede asociar a un valor NULO" % s
                    if not tMD.inCache():
                        del tMD

                if self.d.modeAccess_ == self.Edit:
                    if self.buffer() and self.bufferCopy():
                        if self.buffer().value(fiName) == self.bufferCopy().value(fiName):
                            continue

                if self.buffer().isNull(fiName) and not field.allowNull() and not field.type() == "serial":
                    msg = msg + "\n" + self.metadata().name() + ":" + field.alias() + " : No puede ser nulo"

                if field.isUnique():
                    pK = self.metadata().primaryKey()
                    if not self.buffer().isNull(pK) and s is not None:
                        pKV = self.buffer().value(pK)
                        q = PNSqlQuery(None, self.db().connectionName())
                        q.setTablesList(self.metadata().name())
                        q.setSelect(fiName)
                        q.setFrom(self.metadata().name())
                        q.setWhere(
                            "%s AND %s <> %s"
                            % (
                                self.db().manager().formatAssignValue(field, s, True),
                                self.metadata().primaryKey(self.d.isQuery_),
                                self.db().manager().formatValue(self.metadata().field(pK).type(), pKV),
                            )
                        )
                        q.setForwardOnly(True)
                        q.exec_()
                        if q.next():
                            msg = (
                                msg
                                + "\n"
                                + self.metadata().name()
                                + ":"
                                + field.alias()
                                + " : Requiere valores únicos, y ya hay otro registro con el valor %s en este campo" % s
                            )

                if field.isPrimaryKey() and self.d.modeAccess_ == self.Insert and s is not None:
                    q = PNSqlQuery(None, self.db().connectionName())
                    q.setTablesList(self.metadata().name())
                    q.setSelect(fiName)
                    q.setFrom(self.metadata().name())
                    q.setWhere(self.db().manager().formatAssignValue(field, s, True))
                    q.setForwardOnly(True)
                    q.exec_()
                    if q.next():
                        msg = (
                            msg
                            + "\n"
                            + self.metadata().name()
                            + ":"
                            + field.alias()
                            + " : Es clave primaria y requiere valores únicos, y ya hay otro registro con el valor %s en este campo" % s
                        )

                if field.relationM1() and s:
                    if field.relationM1().checkIn() and not field.relationM1().foreignTable() == self.metadata().name():
                        r = field.relationM1()
                        tMD = self.db().manager().metadata(r.foreignTable())
                        if not tMD:
                            continue
                        q = PNSqlQuery(None, self.db().connectionName())
                        q.setTablesList(tMD.name())
                        q.setSelect(r.foreignField())
                        q.setFrom(tMD.name())
                        q.setWhere(self.db().manager().formatAssignValue(r.foreignField(), field, s, True))
                        q.setForwardOnly(True)
                        logger.debug("SQL linea = %s conn name = %s", q.sql(), str(project.conn.connectionName()))
                        q.exec_()
                        if not q.next():
                            msg = (
                                msg
                                + "\n"
                                + self.metadata().name()
                                + ":"
                                + field.alias()
                                + " : El valor %s no existe en la tabla %s" % (s, r.foreignTable())
                            )
                        else:
                            self.buffer().setValue(fiName, q.value(0))

                        if not tMD.inCache():
                            del tMD

                fieldListCK = self.metadata().fieldListOfCompoundKey(fiName)
                if fieldListCK and not checkedCK and self.d.modeAccess_ == self.Insert:
                    if fieldListCK:
                        filter = None
                        field = None
                        valuesFields = None
                        for fieldCK in fieldListCK:
                            sCK = self.buffer().value(fieldCK.name())
                            if filter is None:
                                filter = self.db().manager().formatAssignValue(fieldCK, sCK, True)
                            else:
                                filter = "%s AND %s" % (filter, self.db().manager().formatAssignValue(fieldCK, sCK, True))
                            if field is None:
                                field = fieldCK.alias()
                            else:
                                field = "%s+%s" % (field, fieldCK.alias())
                            if valuesFields is None:
                                valuesFields = str(sCK)
                            else:
                                valuesFields = "%s+%s" % (valuesFields, str(sCK))

                        q = PNSqlQuery(None, self.db().connectionName())
                        q.setTablesList(self.metadata().name())
                        q.setSelect(fiName)
                        q.setFrom(self.metadata().name())
                        q.setWhere(filter)
                        q.setForwardOnly(True)
                        q.exec_()
                        if q.next():
                            msg = msg + "\n%s : Requiere valor único, y ya hay otro registro con el valor %s en la tabla %s" % (
                                field,
                                valuesFields,
                                self.metadata().name(),
                            )

                        checkedCK = True

        elif self.d.modeAccess_ == self.Del:
            fieldList = self.metadata().fieldList()
            fiName = None
            s = None

            for field in fieldList:
                # fiName = field.name()
                if not self.buffer().isGenerated(field.name()):
                    continue

                s = None

                if not self.buffer().isNull(field.name()):
                    s = self.buffer().value(field.name())
                    # if s:
                    #    s = None

                if s is None:
                    continue

                relationList = field.relationList()
                if relationList:
                    for r in relationList:
                        if not r.checkIn():
                            continue
                        mtd = self.db().manager().metadata(r.foreignTable())
                        if not mtd:
                            continue
                        f = mtd.field(r.foreignField())
                        if f is not None:
                            if f.relationM1():
                                if f.relationM1().deleteCascade():
                                    if not mtd.inCache():
                                        del mtd
                                    continue
                                if not f.relationM1().checkIn():
                                    if not mtd.inCache():
                                        del mtd
                                    continue
                            else:
                                if not mtd.inCache():
                                    del mtd
                                continue

                        else:
                            msg = (
                                msg
                                + "\n"
                                + "FLSqlCursor : Error en metadatos, %s.%s no es válido.\nCampo relacionado con %s.%s."
                                % (mtd.name(), r.foreignField(), self.metadata().name(), field.name())
                            )
                            if not mtd.inCache():
                                del mtd
                            continue

                        q = PNSqlQuery(None, self.db().connectionName())
                        q.setTablesList(mtd.name())
                        q.setSelect(r.foreignField())
                        q.setFrom(mtd.name())
                        q.setWhere(self.db().manager().formatAssignValue(r.foreignField(), field, s, True))
                        q.setForwardOnly(True)
                        q.exec_()
                        if q.next():
                            msg = (
                                msg
                                + "\n"
                                + self.metadata().name()
                                + ":"
                                + field.alias()
                                + " : Con el valor %s hay registros en la tabla %s:%s" % (s, mtd.name(), mtd.alias())
                            )

                        if not mtd.inCache():
                            del mtd

        return msg

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

    def checkIntegrity(self, showError=True):
        if not self.buffer() or not self.metadata():
            return False
        if not self.d.activatedCheckIntegrity_:
            return True
        msg = self.msgCheckIntegrity()
        if msg:
            if showError:
                if self.d.modeAccess_ == self.Insert or self.d.modeAccess_ == self.Edit:
                    self.d.msgBoxWarning("No se puede validad el registro actual:\n" + msg)
                elif self.d.modeAccess_ == self.Del:
                    self.d.msgBoxWarning("No se puede borrar registro:\n" + msg)
            return False
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

    def setUnLock(self, fN, v):
        metadata = self.metadata()
        if not metadata or not self.modeAccess() == self.Browse:
            return
        if not metadata.field(fN).type() == "unlock":
            logger.warning("setUnLock sólo permite modificar campos del tipo Unlock")
            return
        buffer = self.d.buffer_ = self.primeUpdate()
        self.setModeAccess(self.Edit)
        buffer.setValue(fN, v)
        self.update()
        self.refreshBuffer()

    """
    Para comprobar si el registro actual del cursor está bloqueado.

    @return TRUE si está bloqueado, FALSE en caso contrario.
    """

    def isLocked(self):

        if not self.metadata():
            return False

        ret_ = False
        if self.d.modeAccess_ is not self.Insert:
            row = self.currentRegister()

            for field in self.metadata().fieldNamesUnlock():
                if row > -1:
                    if self.model().value(row, field) not in ("True", True, 1, "1"):
                        ret_ = True
                        break

        if not ret_ and self.cursorRelation():
            ret_ = self.cursorRelation().isLocked()

        return ret_

    def buffer(self) -> Optional[PNBuffer]:
        """
        Devuelve el contenido del buffer
        """
        if self.d.buffer_:
            return self.d.buffer_
        else:
            return None

    """
    Devuelve el contenido del bufferCopy
    """

    def bufferCopy(self):
        if self.d.bufferCopy_:
            return self.d.bufferCopy_
        else:
            return None

    """
    Devuelve si el contenido de un campo en el buffer es nulo.

    @param pos_or_name Nombre o pos del campo en el buffer
    """

    def bufferIsNull(self, pos_or_name):

        if self.buffer():
            return self.buffer().isNull(pos_or_name)
        return True

    """
    Establece que el contenido de un campo en el buffer sea nulo.

    @param pos_or_name Nombre o pos del campo en el buffer
    """

    def bufferSetNull(self, pos_or_name):

        if self.buffer():
            self.buffer().setNull(pos_or_name)

    """
    Devuelve si el contenido de un campo en el bufferCopy en nulo.

    @param pos_or_name Nombre o pos del campo en el bufferCopy
    """

    def bufferCopyIsNull(self, pos_or_name):

        if self.bufferCopy():
            return self.bufferCopy().isNull(pos_or_name)
        return True

    """
    Establece que el contenido de un campo en el bufferCopy sea nulo.

    @param pos_or_name Nombre o pos del campo en el bufferCopy
    """

    def bufferCopySetNull(self, pos_or_name):

        if self.bufferCopy():
            self.bufferCopy().setNull(pos_or_name)

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
        if not self.buffer() or not self.metadata():
            return 0
        # Faster version for this function::
        if self.isValid():
            pos = self.at()
        else:
            pos = 0
        return pos
        # --- the following function is awfully slow when there is a lot of data
        # ... why we do need to do this, exactly?

        pKN = self.metadata().primaryKey()
        pKValue = self.valueBuffer(pKN)

        pos = -99
        if pos == -99:
            # q = PNSqlQuery(None, self.db().db()) FIXME
            # q = PNSqlQuery()
            q = PNSqlQuery(None, self.db().connectionName())
            sql = self.curFilter()
            sqlIn = self.curFilter()
            cFilter = self.curFilter()
            field = None

            sqlPriKey = None
            sqlFrom = None
            # sqlWhere = None
            sqlPriKeyValue = None
            sqlOrderBy = None

            if not self.d.isQuery_ or "." in pKN:
                sqlPriKey = pKN
                sqlFrom = self.metadata().name()
                field = self.metadata().field(pKN)
                sql = "SELECT %s FROM %s" % (sqlPriKey, sqlFrom)
            else:
                qry = self.db().manager().query(self.metadata().query(), self)
                if qry:
                    # Buscamos la tabla que contiene el campo:
                    for t in qry.tablesList():
                        mtd = self.db().manager().metadata(t)
                        field = mtd.field(pKN)
                        if field is not None:
                            break

                    sqlPriKey = "%s.%s" % (field.metadata().name(), pKN)
                    sqlFrom = qry.from_()
                    sql = "SELECT %s FROM %s" % (sqlPriKey, sqlFrom)
                    del qry
                else:
                    logger.error("atFrom Error al crear la consulta")
                    self.seek(self.at())
                    if self.isValid():
                        pos = self.at()
                    else:
                        pos = 0
                    return pos

            sqlWhere = "1=1"
            if field is not None:
                sqlPriKeyValue = self.db().manager().formatAssignValue(field, pKValue, True)
                sqlWhere = sqlPriKeyValue
                if cFilter:
                    sqlWhere += " AND %s" % cFilter
                sqlIn = "%s WHERE %s" % (sql, sqlPriKeyValue)
                # q.exec_(self.db(), sqlIn)
                q.exec_(sqlIn)
                if not q.next():
                    self.seek(self.at())
                    if self.isValid():
                        pos = self.at()
                    else:
                        pos = 0
                    return pos
            else:
                if cFilter:
                    sqlWhere = cFilter
                    sql = "%s WHERE %s" % (sql, cFilter)
                else:
                    sql = "%s WHERE 1=1" % sql

            if self.d.isQuery_ and self.d.queryOrderBy_:
                sqlOrderBy = self.d.queryOrderBy_
                sql = "%s ORDER BY %s" % (sql, sqlOrderBy)
            elif self.sort() and len(self.sort()) > 0:
                sqlOrderBy = self.sort()
                sql = "%s ORDER BY %s" % (sql, sqlOrderBy)

            # FIXME: solo compatible con PostgreSQL!
            if sqlPriKeyValue and self.db().canOverPartition():
                # posEqual = sqlPriKeyValue.index("=")
                # leftSqlPriKey = sqlPriKeyValue[0:posEqual]
                sqlRowNum = (
                    "SELECT rownum FROM ("
                    "SELECT row_number() OVER (ORDER BY %s) as rownum FROM %s WHERE %s ORDER BY %s) as subnumrow"
                    % (sqlOrderBy or "1", sqlFrom, sqlWhere, sqlOrderBy or "1")
                )
                if q.exec_(sqlRowNum) and q.next():
                    pos = int(q.value(0)) - 1
                    if pos >= 0:
                        return pos

            found = False
            q.exec_(sql)

            pos = 0
            if q.first():
                if not q.value(0) == pKValue:
                    pos = q.size()
                    if q.last() and pos > 1:
                        pos = pos - 1
                        if not q.value(0) == pKValue:
                            while q.prev() and pos > 1:
                                pos = pos - 1
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

    def atFromBinarySearch(self, fN, v, orderAsc=True):

        ret = -1
        ini = 0
        fin = self.size() - 1
        mid = None
        comp = None
        midVal = None
        metadata = self.metadata()
        if not metadata:
            raise Exception("Metadata is not set")

        if fN in metadata.fieldNames():
            while ini <= fin:
                mid = int((ini + fin) / 2)
                midVal = str(self.model().value(mid, fN))
                if v == midVal:
                    ret = mid
                    break

                if orderAsc:
                    comp = v < midVal
                else:
                    comp = v > midVal

                if not comp:
                    ini = mid + 1
                else:
                    fin = mid - 1
                ret = ini

        return ret

    """
    Redefinido por conveniencia
    """

    @decorators.NotImplementedWarn
    def exec_(self, query):
        # if query:
        #    logger.debug("ejecutando consulta " + query)
        #    QSqlQuery.exec(self, query)

        return True

    def setNull(self, name):
        self.setValueBuffer(name, None)

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

    def filterAssoc(self, fieldName, tableMD=None):
        fieldName = fieldName

        mtd = self.metadata()
        if not mtd:
            return None

        field = mtd.field(fieldName)
        if field is None:
            return None

        # ownTMD = False

        if not tableMD:
            # ownTMD = True
            tableMD = self.db().manager().metadata(field.relationM1().foreignTable())

        if not tableMD:
            return None

        fieldAc = field.associatedField()
        if fieldAc is None:
            # if ownTMD and not tableMD.inCache():
            # del tableMD
            return None

        fieldBy = field.associatedFieldFilterTo()

        if not self.buffer():
            return

        if not tableMD.field(fieldBy) or self.buffer().isNull(fieldAc.name()):
            # if ownTMD and not tableMD.inCache():
            # del tableMD
            return None

        vv = self.buffer().value(fieldAc.name())
        if vv:
            # if ownTMD and not tableMD.inCache():
            # del tableMD
            return self.db().manager().formatAssignValue(fieldBy, fieldAc, vv, True)

        # if ownTMD and not tableMD.inCache():
        # del rableMD

        return None

    @decorators.BetaImplementation
    def aqWasDeleted(self):
        return False

    """
    Redefinida
    """

    @decorators.NotImplementedWarn
    def calculateField(self, name):
        return True

    def model(self) -> "PNCursorTableModel":
        return self.d._model

    def selection(self):
        return self._selection

    @QtCore.pyqtSlot(QtCore.QModelIndex, QtCore.QModelIndex)
    @QtCore.pyqtSlot(int, int)
    @QtCore.pyqtSlot(int)
    def selection_currentRowChanged(self, current, previous=None):
        if self.currentRegister() == current.row():
            self.d.doAcl()
            return False
        self.d._currentregister = current.row()
        self.d._current_changed.emit(self.at())
        # agregado para que FLTableDB actualice el buffer al pulsar.
        self.refreshBuffer()
        self.d.doAcl()
        logger.debug("cursor:%s , row:%s:: %s", self._action.table(), self.currentRegister(), self)

    def selection_pk(self, value):

        if value is None:
            return False

        i = 0
        buffer = self.buffer()
        if not buffer:
            raise Exception("Buffer not set")
        while i <= self.model().rowCount():
            if self.model().value(i, buffer.pK()) == value:
                return self.move(i)

            i = i + 1

        return False

    def at(self):
        if not self.currentRegister():
            row = 0
        else:
            row = self.currentRegister()

        if row < 0:
            return -1

        if row >= self.model().rows:
            return -2
        # logger.debug("%s.Row %s ----> %s" % (self.curName(), row, self))
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
    @QtCore.pyqtSlot(str)
    def refresh(self, fN=None):
        if not self.metadata():
            return

        if self.cursorRelation() and self.relation():
            self.d.persistentFilter_ = None
            if not self.cursorRelation().metadata():
                return
            if self.cursorRelation().metadata().primaryKey() == fN and self.cursorRelation().modeAccess() == self.Insert:
                return

            if not fN or self.relation().foreignField() == fN:
                self.d.buffer_ = None
                self.refreshDelayed()
                return
        else:
            self.model().refresh()  # Hay que hacer refresh previo pq si no no recoge valores de un commitBuffer paralelo
            # self.select()
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
    def refreshDelayed(self, msec=50):
        # if self.buffer():
        #    return
        if not self.d.timer_:
            return

        obj = self.sender()

        if not obj or not obj.inherits("QTimer"):
            self.d.timer_.start(msec)
            return
        else:
            self.d.timer_.stop()

        """
        if not self._refreshDelayedTimer:
            time = QtCore.QTimer()
            time.singleShot(msec, self.refreshDelayed)
            self._refreshDelayedTimer = True
            return

        self._refreshDelayedTimer = False
        """

        # self.d.timer_.start(msec)
        # cFilter = self.filter()
        # self.setFilter(None)
        # if cFilter == self.filter() and self.isValid():
        #    return
        self.select()
        pos = self.atFrom()
        if not self.seek(pos, False, True):
            self.newBuffer.emit()
        else:
            if self.cursorRelation() and self.relation() and self.cursorRelation().metadata():
                v = self.valueBuffer(self.relation().field())
                foreignFieldValueBuffer = self.cursorRelation().valueBuffer(self.relation().foreignField())

                if foreignFieldValueBuffer != v and foreignFieldValueBuffer is not None:
                    self.cursorRelation().setValueBuffer(self.relation().foreignField(), v)

    def primeInsert(self):
        buffer = self.buffer()
        if not buffer:
            buffer = self.d.buffer_ = PNBuffer(self)

        buffer.primeInsert()

    def primeUpdate(self):
        buffer = self.buffer()
        if not buffer:
            buffer = self.d.buffer_ = PNBuffer(self)

        buffer.primeUpdate(self.at())
        return buffer

    def editBuffer(self, b=None):
        # if not self.buffer():
        # self.d.buffer_ = PNBuffer(self.d)
        return self.primeUpdate()

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
        from pineboolib import qsa as qsa_tree

        if not self.metadata():
            return False

        if isinstance(self.sender(), QtCore.QTimer) and self.d.modeAccess_ != self.Browse:
            return False

        if not self.isValid() and self.d.modeAccess_ != self.Insert:
            return False

        if self.d.modeAccess_ == self.Insert:
            if not self.commitBufferCursorRelation():
                return False

            if not self.buffer():
                self.d.buffer_ = PNBuffer(self)
            self.setNotGenerateds()

            fieldList = self.metadata().fieldList()
            if fieldList:
                for field in fieldList:
                    field_name = field.name()
                    self.buffer().setNull(field_name)
                    if not self.buffer().isGenerated(field_name):
                        continue
                    type_ = field.type()
                    # fltype = FLFieldMetaData.flDecodeType(type_)
                    # fltype = self.metadata().field(fiName).flDecodeType(type_)
                    defVal = field.defaultValue()
                    if defVal is not None:
                        # defVal.cast(fltype)
                        self.buffer().setValue(field_name, defVal)

                    if type_ == "serial":
                        val = self.db().nextSerialVal(self.metadata().name(), field_name)
                        if val is None:
                            val = 0
                        self.buffer().setValue(field_name, val)

                    if field.isCounter():
                        from pineboolib.application.database.utils import nextCounter

                        siguiente = None
                        if self._action.scriptFormRecord():
                            context_ = getattr(qsa_tree, "formRecord%s" % self._action.scriptFormRecord()[:-3]).iface
                            function_counter = getattr(context_, "calculateCounter", None)
                            if function_counter is None:
                                siguiente = nextCounter(field_name, self)
                            else:
                                siguiente = function_counter()
                        else:
                            siguiente = nextCounter(field_name, self)

                        if siguiente:
                            self.buffer().setValue(field_name, siguiente)

            if self.cursorRelation() and self.relation() and self.cursorRelation().metadata():
                self.setValueBuffer(self.relation().field(), self.cursorRelation().valueBuffer(self.relation().foreignField()))

            self.d.undoAcl()
            self.updateBufferCopy()
            self.newBuffer.emit()

        elif self.d.modeAccess_ == self.Edit:
            if not self.commitBufferCursorRelation():
                return False

            self.primeUpdate()

            if self.isLocked() and not self.d.acosCondName_:
                self.d.modeAccess_ = self.Browse

            self.setNotGenerateds()
            self.updateBufferCopy()
            self.newBuffer.emit()

        elif self.d.modeAccess_ == self.Del:

            if self.isLocked():
                self.d.msgBoxWarning("Registro bloqueado, no se puede eliminar")
                self.d.modeAccess_ = self.Browse
                return False

            if not self.buffer():
                self.d.buffer_ = PNBuffer(self)

            if self.buffer():

                # self.buffer().primeDelete()
                self.setNotGenerateds()
                self.updateBufferCopy()

        elif self.d.modeAccess_ == self.Browse:
            self.editBuffer(True)
            self.setNotGenerateds()
            self.newBuffer.emit()

        else:
            logger.error("refreshBuffer(). No hay definido modeAccess()")

        # if project._DGI.use_model() and self.meta_model():
        #    self.populate_meta_model()

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
    def seek(self, i, relative=None, emite=None):

        ret_ = False

        if self.buffer():
            if emite:
                self.currentChanged.emit(self.at())

            ret_ = self.refreshBuffer()

        return ret_

    """
    Redefinicion del método next() de QSqlCursor.

    Este método simplemente invoca al método next() original de QSqlCursor() y refresca el
    buffer con el metodo FLSqlCursor::refreshBuffer().

    @param emit Si TRUE emite la señal FLSqlCursor::currentChanged()
    """

    @QtCore.pyqtSlot()
    @QtCore.pyqtSlot(bool)
    def next(self, emite=True):
        # if self.d.modeAccess_ == self.Del:
        #    return False

        b = self.moveby(1)
        if b:
            if emite:
                self.d._current_changed.emit(self.at())

            return self.refreshBuffer()

        return b

    def moveby(self, pos):
        if self.currentRegister():
            pos += self.currentRegister()

        return self.move(pos)

    """
    Redefinicion del método prev() de QSqlCursor.

    Este método simplemente invoca al método prev() original de QSqlCursor() y refresca
    el buffer con el metodo FLSqlCursor::refreshBuffer().

    @param emit Si TRUE emite la señal FLSqlCursor::currentChanged()
    """

    @QtCore.pyqtSlot()
    @QtCore.pyqtSlot(bool)
    def prev(self, emite=True):
        # if self.d.modeAccess_ == self.Del:
        #    return False

        b = self.moveby(-1)

        if b:
            if emite:
                self.d._current_changed.emit(self.at())

            return self.refreshBuffer()

        return b

    """
    Mueve el cursor por la tabla:
    """

    def move(self, row):
        if row is None:
            row = -1

        if not self.model():
            return False

        if row < 0:
            row = -1
        if row >= self.model().rows:
            row = self.model().rows
        if self.currentRegister() == row:
            return False
        topLeft = self.model().index(row, 0)
        bottomRight = self.model().index(row, self.model().cols - 1)
        new_selection = QtCore.QItemSelection(topLeft, bottomRight)
        self._selection.select(new_selection, QtCore.QItemSelectionModel.ClearAndSelect)
        self.d._currentregister = row
        # self.d._current_changed.emit(self.at())
        if row < self.model().rows and row >= 0:
            return True
        else:
            return False

    """
    Redefinicion del método first() de QSqlCursor.

    Este método simplemente invoca al método first() original de QSqlCursor() y refresca el
    buffer con el metodo FLSqlCursor::refreshBuffer().

    @param emit Si TRUE emite la señal FLSqlCursor::currentChanged()
    """

    @QtCore.pyqtSlot()
    @QtCore.pyqtSlot(bool)
    def first(self, emite=True):
        # if self.d.modeAccess_ == self.Del:
        #    return False
        if not self.currentRegister() == 0:
            b = self.move(0)
        else:
            b = True

        if b:
            if emite:
                self.d._current_changed.emit(self.at())

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
    def last(self, emite=True):
        # if self.d.modeAccess_ == self.Del:
        #    return False

        b = self.move(self.d._model.rows - 1)

        if b:
            if emite:
                self.d._current_changed.emit(self.at())

            return self.refreshBuffer()

        return b

    """
    Redefinicion del método del() de QSqlCursor.

    Este método invoca al método del() original de QSqlCursor() y comprueba si hay borrado
    en cascada, en caso afirmativo borrar también los registros relacionados en cardinalidad 1M.
    """

    @QtCore.pyqtSlot()
    def __del__(self, invalidate=True):
        # logger.trace("FLSqlCursor(%s). Eliminando cursor" % self.curName(), self)
        # delMtd = None
        # if self.metadata():
        #     if not self.metadata().inCache():
        #         delMtd = True

        if self.d is not None:
            msg = None
            mtd = self.metadata()

            # FIXME: Pongo que tiene que haber mas de una trasaccion abierta
            if len(self.d.transactionsOpened_) > 0:
                logger.notice("FLSqlCursor(%s).Transacciones abiertas!! %s", self.curName(), self.d.transactionsOpened_)
                t = self.curName()
                if mtd:
                    t = mtd.name()
                msg = (
                    "Se han detectado transacciones no finalizadas en la última operación.\n"
                    "Se van a cancelar las transacciones pendientes.\n"
                    "Los últimos datos introducidos no han sido guardados, por favor\n"
                    "revise sus últimas acciones y repita las operaciones que no\n"
                    "se han guardado.\nSqlCursor::~SqlCursor: %s\n" % t
                )
                self.rollbackOpened(-1, msg)
        else:

            if not project._DGI.use_model():
                logger.warning("Se está eliminando un cursor Huerfano (%s)", self)

        self.destroyed.emit()

        # self.d.countRefCursor = self.d.countRefCursor - 1     FIXME

    """
    Redefinicion del método select() de QSqlCursor
    """

    @QtCore.pyqtSlot()
    def select(self, _filter=None, sort=None):  # sort = QtCore.QSqlIndex()
        _filter = _filter if not None else self.filter()
        if not self.metadata():
            return False

        bFilter = self.baseFilter()
        finalFilter = bFilter
        if _filter:
            if bFilter:
                if _filter not in bFilter:
                    finalFilter = "%s AND %s" % (bFilter, _filter)
                else:
                    finalFilter = bFilter

            else:
                finalFilter = _filter

        if self.cursorRelation() and self.cursorRelation().modeAccess() == self.Insert and not self.curFilter():
            finalFilter = "1 = 0"

        if finalFilter:
            self.setFilter(finalFilter)

        if sort:
            self.model().setSortOrder(sort)

        self.model().refresh()

        self.d._currentregister = -1

        if self.cursorRelation() and self.modeAccess() == self.Browse:
            self.d._currentregister = self.atFrom()

        self.refreshBuffer()
        # if self.modeAccess() == self.Browse:
        #    self.d._currentregister = -1
        self.newBuffer.emit()

        return True

    """
    Redefinicion del método sort() de QSqlCursor
    """

    @QtCore.pyqtSlot()
    def setSort(self, sortO):
        if not sortO:
            return

        self.model().setSortOrder(sortO)

    """
    Obtiene el filtro base
    """

    @QtCore.pyqtSlot()
    def baseFilter(self):
        relationFilter = None
        finalFilter = ""

        if self.cursorRelation() and self.relation() and self.metadata() and self.cursorRelation().metadata():
            fgValue = self.cursorRelation().valueBuffer(self.relation().foreignField())
            field = self.metadata().field(self.relation().field())

            if field is not None and fgValue is not None:

                relationFilter = self.db().manager().formatAssignValue(field, fgValue, True)
                filterAc = self.cursorRelation().filterAssoc(self.relation().foreignField(), self.metadata())
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
                if relationFilter not in finalFilter:
                    finalFilter = "%s AND %s" % (finalFilter, relationFilter)

        # if self.filter():
        #    if finalFilter and self.filter() not in finalFilter:
        #        finalFilter = "%s AND %s" % (finalFilter, self.filter())
        #    else:
        #        finalFilter = self.filter()

        return finalFilter

    """
    Obtiene el filtro actual
    """

    @QtCore.pyqtSlot()
    def curFilter(self):
        f = self.filter()
        bFilter = self.baseFilter()
        if f:
            while f.endswith(";"):
                f = f[0 : len(f) - 1]

        if not bFilter:
            return f
        else:
            if not f or f in bFilter:
                return bFilter
            else:
                if bFilter in f:
                    return f
                else:
                    return "%s AND %s" % (bFilter, f)

    """
    Redefinicion del método setFilter() de QSqlCursor
    """

    @QtCore.pyqtSlot()
    def setFilter(self, _filter):

        # self.d.filter_ = None

        finalFilter = _filter

        bFilter = self.baseFilter()
        if bFilter:
            if not finalFilter:
                finalFilter = bFilter
            elif finalFilter in bFilter:
                finalFilter = bFilter
            elif bFilter not in finalFilter:
                finalFilter = bFilter + " AND " + finalFilter

        if finalFilter and self.d.persistentFilter_ and self.d.persistentFilter_ not in finalFilter:
            finalFilter = finalFilter + " OR " + self.d.persistentFilter_

        self.d._model.where_filters["filter"] = finalFilter

    """
    Abre el formulario de edicion de registro definido en los metadatos (FLTableMetaData) listo
    para insertar un nuevo registro en el cursor.
    """

    @QtCore.pyqtSlot()
    def insertRecord(self, wait: bool = True):
        logger.trace("insertRecord %s", self._action.name())
        self.openFormInMode(self.Insert, wait)

    """
    Abre el formulario de edicion de registro definido en los metadatos (FLTableMetaData) listo
    para editar el registro activo del cursor.
    """

    @QtCore.pyqtSlot()
    def editRecord(self, wait: bool = True):
        logger.trace("editRecord %s", self.actionName())
        if self.d.needUpdate():
            pKN = self.metadata().primaryKey()
            pKValue = self.valueBuffer(pKN)
            self.refresh()
            pos = self.atFromBinarySearch(pKN, pKValue)
            if not pos == self.at():
                self.seek(pos, False, False)

        self.openFormInMode(self.Edit, wait)

    """
    Abre el formulario de edicion de registro definido en los metadatos (FLTableMetaData) listo
    para sólo visualizar el registro activo del cursor.
    """

    @QtCore.pyqtSlot()
    def browseRecord(self, wait: bool = True):
        logger.trace("browseRecord %s", self.actionName())
        if self.d.needUpdate():
            pKN = self.metadata().primaryKey()
            pKValue = self.valueBuffer(pKN)
            self.refresh()
            pos = self.atFromBinarySearch(pKN, pKValue)
            if not pos == self.at():
                self.seek(pos, False, False)
        self.openFormInMode(self.Browse, wait)

    """
    Borra, pidiendo confirmacion, el registro activo del cursor.
    """

    @QtCore.pyqtSlot()
    def deleteRecord(self, wait: bool = True):
        logger.trace("deleteRecord %s", self.actionName())
        self.openFormInMode(self.Del, wait)
        # self.d._action.openDefaultFormRecord(self)

    """
    Realiza la accion de insertar un nuevo registro, y copia el valor de los campos del registro
    actual.
    """

    def copyRecord(self):
        if not self.d.metadata_ or not self.d.buffer_:
            return

        from pineboolib import pncontrolsfactory

        if not self.isValid() or self.size() <= 0:
            pncontrolsfactory.QMessageBox.warning(
                pncontrolsfactory.QApplication.focusWidget(),
                self.tr("Aviso"),
                self.tr("No hay ningún registro seleccionado"),
                pncontrolsfactory.QMessageBox.Ok,
            )
            return

        field_list = self.d.metadata_.fieldList()
        if not field_list:
            return

        # ifdef AQ_MD5_CHECK
        if self.d.needUpdate():
            pkn = self.d.metadata_.primaryKey()
            pk_value = self.valueBuffer(pkn)
            self.refresh()
            pos = self.atFromBinarySearch(pkn, str(pk_value))
            if pos != self.at():
                self.seek(pos, False, True)
        # endif

        buffer_aux = self.d.buffer_
        self.insertRecord()

        for it in field_list:
            if it is None:
                continue

            if (
                self.d.buffer_.isNull(it.name())
                and not it.isPrimaryKey()
                and not self.d.metadata_.fieldListOfCompoundKey(it.name())
                and not it.calculated()
            ):
                self.d.buffer_.setValue(it.name(), buffer_aux.value(it.name()))

            del buffer_aux
            self.newBuffer.emit()

    """
    Realiza la acción asociada a elegir un registro del cursor, por defecto se abre el formulario de
    edición de registro,llamando al método FLSqlCursor::editRecord(), si la bandera FLSqlCursor::edition
    indica TRUE, si indica FALSE este método no hace nada
    """

    @QtCore.pyqtSlot()
    def chooseRecord(self):
        from pineboolib.core.settings import config

        if not config.value("ebcomportamiento/FLTableDoubleClick", False):
            if self.d.edition_:
                self.editRecord()
            else:
                if self.d.browse_:
                    self.browseRecord()
        else:
            if self.d.browse_:
                self.browseRecord()

        self.recordChoosed.emit()

    """
    Evita el refresco del model() asociado.
    """

    def setForwardOnly(self, b):
        if not self.model():
            return

        self.model().disable_refresh(b)

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
    def commitBuffer(self, emite=True, checkLocks=False):

        if not self.buffer() or not self.metadata():
            return False

        if not self.activatedBufferCommited():
            return True

        from pineboolib import pncontrolsfactory

        if self.db().interactiveGUI() and self.db().canDetectLocks() and (checkLocks or self.metadata().detectLocks()):
            self.checkRisksLocks()
            if self.d.inRisksLocks_:
                ret = pncontrolsfactory.QMessageBox.warning(
                    None,
                    "Bloqueo inminente",
                    "Los registros que va a modificar están bloqueados actualmente.\n"
                    "Si continua hay riesgo de que su conexión quede congelada hasta finalizar el bloqueo.\n"
                    "\n¿ Desa continuar aunque exista riesgo de bloqueo ?",
                    pncontrolsfactory.QMessageBox.Ok,
                    pncontrolsfactory.QMessageBox.No | pncontrolsfactory.QMessageBox.Default | pncontrolsfactory.QMessageBox.Escape,
                )
                if ret == pncontrolsfactory.QMessageBox.No:
                    return False

        if not self.checkIntegrity():
            return False

        fieldNameCheck = None

        if self.modeAccess() == self.Edit or self.modeAccess() == self.Insert:
            fieldList = self.metadata().fieldList()

            for field in fieldList:
                if field.isCheck():
                    fieldNameCheck = field.name()
                    self.buffer().setGenerated(field, False)
                    if self.bufferCopy():
                        self.bufferCopy().setGenerated(field, False)
                    continue

                if not self.buffer().isGenerated(field.name()):
                    continue

                if self.context() and hasattr(self.context(), "calculateField") and field.calculated():
                    v = project.call("calculateField", [field.name()], self.context(), False)

                    if v not in (True, False, None):
                        self.setValueBuffer(field.name(), v)

        functionBefore = None
        functionAfter = None
        model_module: Any = None

        idMod = self.db().managerModules().idModuleOfFile("%s.mtd" % self.metadata().name())

        if project._DGI.use_model():
            model_name = "models.%s.%s_def" % (idMod, idMod)
            try:
                model_module = importlib.import_module(model_name)
            except Exception:
                logger.exception("Error trying to import module %s", model_name)

        if not self.modeAccess() == PNSqlCursor.Browse and self.activatedCommitActions():

            if idMod:
                functionBefore = "%s.iface.beforeCommit_%s" % (idMod, self.metadata().name())
                functionAfter = "%s.iface.afterCommit_%s" % (idMod, self.metadata().name())
            else:
                functionBefore = "sys.iface.beforeCommit_%s" % self.metadata().name()
                functionAfter = "sys.iface.afterCommit_%s" % self.metadata().name()

            if model_module is not None:
                function_model_before = getattr(model_module.iface, "beforeCommit_%s" % self.metadata().name(), None)
                if function_model_before:
                    ret = function_model_before(self)
                    if not ret:
                        return ret

            if functionBefore:
                v = project.call(functionBefore, [self], None, False)
                if v and not isinstance(v, bool) or v is False:
                    return False

        pKN = self.metadata().primaryKey()
        updated = False
        savePoint = None
        if self.modeAccess() == self.Insert:
            if self.cursorRelation() and self.relation():
                if self.cursorRelation().metadata() and self.cursorRelation().valueBuffer(self.relation().foreignField()):
                    self.setValueBuffer(self.relation().field(), self.cursorRelation().valueBuffer(self.relation().foreignField()))
                    self.cursorRelation().setAskForCancelChanges(True)

            self.model().Insert(self)
            self.model().refresh()
            self.move(self.model().findPKRow((self.buffer().value(self.buffer().pK()),)))

            updated = True

        elif self.modeAccess() == self.Edit:
            if not self.db().canSavePoint():
                if self.db().currentSavePoint_:
                    self.db().currentSavePoint_.saveEdit(pKN, self.bufferCopy(), self)

            if functionAfter and self.d.activatedCommitActions_:
                if not savePoint:
                    from . import pnsqlsavepoint

                    savePoint = pnsqlsavepoint.PNSqlSavePoint(None)
                savePoint.saveEdit(pKN, self.bufferCopy(), self)

            if self.cursorRelation() and self.relation():
                if self.cursorRelation().metadata():
                    self.cursorRelation().setAskForCancelChanges(True)
            logger.trace("commitBuffer -- Edit . 20 . ")
            if self.isModifiedBuffer():

                logger.trace("commitBuffer -- Edit . 22 . ")
                self.update(False)

                logger.trace("commitBuffer -- Edit . 25 . ")

                updated = True
                self.setNotGenerateds()
            logger.trace("commitBuffer -- Edit . 30 . ")

        elif self.modeAccess() == self.Del:

            if self.cursorRelation() and self.relation():
                if self.cursorRelation().metadata():
                    self.cursorRelation().setAskForCancelChanges(True)

            recordDelBefore = "recordDelBefore%s" % self.metadata().name()
            v = project.call(recordDelBefore, [self], self.context(), False)
            if v and not isinstance(v, bool):
                return False

            if not self.buffer():
                self.d.buffer_ = self.primeUpdate()

            fieldList = self.metadata().fieldList()

            for field in fieldList:

                fiName = field.name()
                if not self.buffer().isGenerated(fiName):
                    continue

                s = None
                if not self.buffer().isNull(fiName):
                    s = self.buffer().value(fiName)

                if s is None:
                    continue

                relationList = field.relationList()
                if not relationList:
                    continue
                else:
                    for r in relationList:
                        c = PNSqlCursor(r.foreignTable())
                        if not c.metadata():
                            continue
                        f = c.metadata().field(r.foreignField())
                        if f is None:
                            continue
                        if f.relationM1() and f.relationM1().deleteCascade():
                            c.setForwardOnly(True)
                            c.select(self.conn().manager().formatAssignValue(r.foreignField(), f, s, True))
                            while c.next():
                                c.setModeAccess(self.Del)
                                c.refreshBuffer()
                                if not c.commitBuffer(False):
                                    return False

            self.model().Delete(self)

            recordDelAfter = "recordDelAfter%s" % self.metadata().name()
            v = project.call(recordDelAfter, [self], self.context(), False)

            updated = True

        if updated and self.lastError():
            return False

        if not self.modeAccess() == self.Browse and self.activatedCommitActions():

            if model_module is not None:
                function_model_after = getattr(model_module.iface, "afterCommit_%s" % self.metadata().name(), None)
                if function_model_after:
                    ret = function_model_after(self)
                    if not ret:
                        return ret

            if functionAfter:
                v = project.call(functionAfter, [self], None, False)
                if v and not isinstance(v, bool) or v is False:
                    return False

        if self.modeAccess() in (self.Del, self.Edit):
            self.setModeAccess(self.Browse)

        if self.modeAccess() == self.Insert:
            self.setModeAccess(self.Edit)

        if updated:
            if fieldNameCheck:
                self.buffer().setGenerated(fieldNameCheck, True)
                if self.bufferCopy():
                    self.bufferCopy().setGenerated(fieldNameCheck, True)

            self.setFilter(None)
            self.clearMapCalcFields()

            if emite:
                self.cursorUpdated.emit()

        if model_module is not None:
            function_model_buffer_commited = getattr(model_module.iface, "bufferCommited_%s" % self.metadata().name(), None)
            if function_model_buffer_commited:
                ret = function_model_buffer_commited(self)
                if not ret:
                    return ret

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
        activeWidEnabled = False
        activeWid = None

        if project._DGI.localDesktop():
            from pineboolib import pncontrolsfactory

            activeWid = pncontrolsfactory.QApplication.activeModalWidget()
            if not activeWid:
                activeWid = pncontrolsfactory.QApplication.activePopupWidget()
            if not activeWid:
                activeWid = pncontrolsfactory.QApplication.activeWindow()

            if activeWid:
                activeWidEnabled = activeWid.isEnabled()

        if self.d.modeAccess_ == self.Insert:
            if self.cursorRelation() and self.relation():
                if self.cursorRelation().metadata() and self.cursorRelation().modeAccess() == self.Insert:

                    if activeWid and activeWidEnabled:
                        activeWid.setEnabled(False)

                    if not self.cursorRelation().commitBuffer():
                        self.d.modeAccess_ = self.Browse
                        ok = False
                    else:
                        self.setFilter(None)
                        self.cursorRelation().refresh()
                        self.cursorRelation().setModeAccess(self.Edit)
                        self.cursorRelation().refreshBuffer()

                    if activeWid and activeWidEnabled:
                        activeWid.setEnabled(True)

        elif self.d.modeAccess_ == self.Browse or self.d.modeAccess_ == self.Edit:
            if self.cursorRelation() and self.relation():
                if self.cursorRelation().metadata() and self.cursorRelation().modeAccess() == self.Insert:
                    if activeWid and activeWidEnabled:
                        activeWid.setEnabled(False)

                    if not self.cursorRelation().commitBuffer():
                        self.d.modeAccess_ = self.Browse
                        ok = False
                    else:
                        self.cursorRelation().refresh()
                        self.cursorRelation().setModeAccess(self.Edit)
                        self.cursorRelation().refreshBuffer()

                    if activeWid and activeWidEnabled:
                        activeWid.setEnabled(True)

        return ok

    """
    @return El nivel actual de anidamiento de transacciones, 0 no hay transaccion
    """

    @QtCore.pyqtSlot()
    def transactionLevel(self):
        if self.db():
            return self.db().transactionLevel()
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
    @decorators.BetaImplementation
    def rollbackOpened(self, count=-1, msg=None):
        ct = None
        if count < 0:
            ct = len(self.d.transactionsOpened_)
        else:
            ct = count

        if ct > 0 and msg:
            t = None
            if self.metadata():
                t = self.metadata().name()
            else:
                t = self.name()

            m = "%sSqLCursor::rollbackOpened: %s %s" % (msg, count, t)
            self.d.msgBoxWarning(m, False)
        elif ct > 0:
            logger.trace("rollbackOpened: %s %s", count, self.name())

        i = 0
        while i < ct:
            logger.trace("Deshaciendo transacción abierta", self.transactionLevel())
            self.rollback()
            i = i + 1

    """
    Termina transacciones abiertas por este cursor.

    @param count  Cantidad de transacciones a terminar, -1 todas.
    @param msg    Cadena de texto que se muestra en un cuadro de diálogo antes de terminar las transacciones.
                Si es vacía no muestra nada.
    """

    @QtCore.pyqtSlot()
    def commitOpened(self, count=-1, msg=None):
        ct = None
        t = None
        if count < 0:
            ct = len(self.d.transactionsOpened_)
        else:
            ct = count

        if self.metadata():
            t = self.metadata().name()
        else:
            t = self.name()

        if ct and msg:
            m = "%sSqlCursor::commitOpened: %s %s" % (msg, str(count), t)
            self.d.msgBoxWarning(m, False)
            logger.warning(m)
        elif ct > 0:
            logger.warning("SqlCursor::commitOpened: %d %s" % (count, self.name()))

        i = 0
        while i < ct:
            logger.warning("Terminando transacción abierta %s", self.transactionLevel())
            self.commit()
            i = i + 1

    """
    Entra en un bucle de comprobacion de riesgos de bloqueos para esta tabla y el registro actual

    El bucle continua mientras existan bloqueos, hasta que se vuelva a llamar a este método con
    'terminate' activado o cuando el usuario cancele la operación.

    @param  terminate True terminará el bucle de comprobaciones si está activo
    """

    @QtCore.pyqtSlot()
    @decorators.NotImplementedWarn
    def checkRisksLocks(self, terminate=False):
        return True

    """
    Establece el acceso global para la tabla, ver FLSqlCursor::setAcosCondition().

    Este será el permiso a aplicar a todos los campos por defecto

    @param  ac Permiso global; p.e.: "r-", "-w"
    """

    @QtCore.pyqtSlot()
    def setAcTable(self, ac):
        self.d.idAc_ = self.d.idAc_ + 1
        self.d.id_ = "%s%s%s" % (self.d.idAc_, self.d.idAcos_, self.d.idCond_)
        self.d.acPermTable_ = ac

    """
    Establece la lista de control de acceso (ACOs) para los campos de la tabla, , ver FLSqlCursor::setAcosCondition().

    Esta lista de textos deberá tener en sus componentes de orden par los nombres de los campos,
    y en los componentes de orden impar el permiso a aplicar a ese campo,
    p.e.: "nombre", "r-", "descripcion", "--", "telefono", "rw",...

    Los permisos definidos aqui sobreescriben al global.

    @param acos Lista de cadenas de texto con los nombre de campos y permisos.
    """

    @QtCore.pyqtSlot()
    def setAcosTable(self, acos):
        self.d.idAcos_ = self.d.idAcos_ + 1
        self.d.id_ = "%s%s%s" % (self.d.idAc_, self.d.idAcos_, self.d.idCond_)
        self.d.acosTable_ = acos

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
    def setAcosCondition(self, condName, cond, condVal):
        self.d.idCond_ = self.d.idCond_ + 1
        self.d.id_ = "%s%s%s" % (self.d.idAc_, self.d.idAcos_, self.d.idCond_)
        self.d.acosCondName_ = condName
        self.d.acosCond_ = cond
        self.d.acosCondVal_ = condVal

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
    def changeConnection(self, connName):
        curConnName = self.connectionName()
        if curConnName == connName:
            return

        newDB = project.conn.database(connName)
        if curConnName == newDB.connectionName():
            return

        if self.d.transactionsOpened_:
            mtd = self.metadata()
            t = None
            if mtd:
                t = mtd.name()
            else:
                t = self.name()

            msg = (
                "Se han detectado transacciones no finalizadas en la última operación.\n"
                "Se van a cancelar las transacciones pendientes.\n"
                "Los últimos datos introducidos no han sido guardados, por favor\n"
                "revise sus últimas acciones y repita las operaciones que no\n"
                "se han guardado.\n" + "SqlCursor::changeConnection: %s\n" % t
            )
            self.rollbackOpened(-1, msg)

        bufferNoEmpty = self.buffer() is not None

        bufferBackup = None
        if bufferNoEmpty:
            bufferBackup = self.buffer()
            self.d.buffer_ = None

        # c = FLSqlCursor(None, True, newDB.db())
        self.d.db_ = newDB
        self.init(self.d.curName_, True, self.cursorRelation(), self.relation())

        if bufferNoEmpty:
            # self.buffer() QSqlCursor::edtiBuffer()
            self.d.buffer_ = bufferBackup

        self.connectionChanged.emit()

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

    def setNotGenerateds(self):
        buffer = self.buffer()
        if self.metadata() and self.d.isQuery_ and buffer:
            for f in self.metadata().fieldList():
                buffer.setGenerated(f, False)

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

    def sort(self):
        return self.model().getSortOrder()

    @decorators.NotImplementedWarn
    def list(self):
        return None

    def filter(self):
        return self.model().where_filters["filter"] if "filter" in self.model().where_filters else ""

    def field(self, name):
        return self.buffer().field(name) if self.buffer() else None

    """
    Actualiza tableModel con el buffer
    """

    def update(self, notify=True):
        logger.trace("PNSqlCursor.update --- BEGIN:")
        if self.modeAccess() == PNSqlCursor.Edit:
            buffer = self.buffer()
            if not buffer:
                raise Exception("Buffer is not set. Cannot update")
            # solo los campos modified
            lista = buffer.modifiedFields()
            buffer.setNoModifiedFields()
            # TODO: pKVaue debe ser el valueBufferCopy, es decir, el antiguo. Para
            # .. soportar updates de PKey, que, aunque inapropiados deberían funcionar.
            pKValue = buffer.value(self.buffer().pK())

            dict_update = {fieldName: buffer.value(fieldName) for fieldName in lista}
            try:
                update_successful = self.model().updateValuesDB(pKValue, dict_update)
            except Exception:
                logger.exception("PNSqlCursor.update:: Unhandled error on model updateRowDB:: ")
                update_successful = False
            # TODO: En el futuro, si no se puede conseguir un update, hay que
            # "tirar atrás" todo.
            if update_successful:
                row = self.model().findPKRow([pKValue])
                if row is not None:
                    if self.model().value(row, self.model().pK()) != pKValue:
                        raise AssertionError(
                            "Los indices del CursorTableModel devolvieron un registro erroneo: %r != %r"
                            % (self.model().value(row, self.model().pK()), pKValue)
                        )
                    self.model().setValuesDict(row, dict_update)

                else:
                    # Método clásico
                    logger.warning("update :: WARN :: Los indices del CursorTableModel no funcionan o el PKey no existe.")
                    row = 0
                    while row < self.model().rowCount():
                        if self.model().value(row, self.model().pK()) == pKValue:
                            for fieldName in lista:
                                self.model().setValue(row, fieldName, self.buffer().value(fieldName))

                            break

                        row = row + 1

            if notify:
                self.bufferCommited.emit()

        logger.trace("PNSqlCursor.update --- END")

    """
    Indica el último error
    """

    def lastError(self):
        return self.db().lastError()

    def __iter__(self):
        self._iter_current = None
        return self

    def __next__(self):
        self._iter_current = 0 if self._iter_current is None else self._iter_current + 1

        list_ = [attr for attr in dir(self) if not attr[0] == "_"]
        if self._iter_current >= len(list_):
            raise StopIteration

        return list_[self._iter_current]

    def primaryKey(self):
        if self.metadata():
            return self.metadata().primaryKey()

    def fieldType(self, field_name=None):
        metadata = self.metadata()
        if field_name and metadata:
            return metadata.fieldType(field_name)
        else:
            return None

    def __getattr__(self, name):
        """Busca en el DGI, si procede"""
        _attr = None
        if self.ext_cursor:
            _attr = getattr(self.ext_cursor, name)

        return _attr

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
    bufferChanged = QtCore.pyqtSignal(str)

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

    destroyed = QtCore.pyqtSignal()
    # def clearPersistentFilter(self):
    #     self.d.persistentFilter_ = None
