# -*- coding: utf-8 -*-
"""
Module for PNSqlCursor class.
"""
import weakref
import importlib
import traceback
from typing import Any, Optional, List, Union, TYPE_CHECKING

from PyQt5 import QtCore  # type: ignore
from pineboolib.core.error_manager import error_manager
from pineboolib.core.decorators import pyqtSlot
from pineboolib.core.utils import logging
from pineboolib.core import decorators
from pineboolib.core.utils.struct import TableStruct

from pineboolib.interfaces.cursoraccessmode import CursorAccessMode
from pineboolib.application.database.pnsqlquery import PNSqlQuery
from pineboolib.application import project
from pineboolib.application.utils.xpm import cacheXPM


from .pnbuffer import PNBuffer

# FIXME: Removde dependency: Should not import from fllegacy.*
from pineboolib.fllegacy.flaccesscontrolfactory import FLAccessControlFactory  # FIXME: Removde dependency
from pineboolib.fllegacy.aqsobjects.aqboolflagstate import AQBoolFlagStateList, AQBoolFlagState  # FIXME: Should not depend on AQS

if TYPE_CHECKING:
    from .pncursortablemodel import PNCursorTableModel  # noqa: F401
    from pineboolib.application.metadata.pntablemetadata import PNTableMetaData  # noqa: F401
    from pineboolib.application.metadata.pnrelationmetadata import PNRelationMetaData  # noqa: F401
    from pineboolib.fllegacy.flformdb import FLFormDB  # noqa: F401
    from pineboolib.interfaces.iconnection import IConnection  # noqa: F401
    from pineboolib.fllegacy.flaction import FLAction  # noqa: F401
    from pineboolib.application.database.pnbuffer import FieldStruct  # noqa: F401


logger = logging.getLogger(__name__)


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
    Database Cursor class.
    """

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

    _selection: Optional[QtCore.QItemSelectionModel] = None

    _iter_current: Optional[int]

    _action: Optional["FLAction"] = None

    ext_cursor = None
    _activatedBufferChanged: bool
    _activatedBufferCommited: bool
    _meta_model: Any

    def __init__(
        self,
        name: Union[str, TableStruct] = None,
        conn_or_autopopulate: Union[bool, str] = True,
        connectionName_or_db: Optional[Union[str, "IConnection"]] = None,
        cR: Optional["PNSqlCursor"] = None,
        r: Optional["PNRelationMetaData"] = None,
        parent=None,
    ) -> None:
        """Create a new cursor."""
        super().__init__()
        if name is None:
            logger.warning("Se está iniciando un cursor Huerfano (%s). Posiblemente sea una declaración en un qsa parseado", self)
            return

        if isinstance(conn_or_autopopulate, str):
            connectionName_or_db = conn_or_autopopulate
            autopopulate = True
        elif isinstance(conn_or_autopopulate, bool):
            autopopulate = conn_or_autopopulate
        self._meta_model = None
        name_action = None
        self.setActivatedBufferChanged(True)
        self.setActivatedBufferCommited(True)
        ext_cursor = getattr(project.DGI, "FLSqlCursor", None)
        if ext_cursor is not None:
            self.ext_cursor = ext_cursor(self, name)
        else:
            self.ext_cursor = None

        if isinstance(name, TableStruct):
            logger.trace("FIXME::__init__ TableStruct %s", name.name, stack_info=True)
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

    def init(self, name: str, autopopulate: bool, cR: Optional["PNSqlCursor"], r: Optional["PNRelationMetaData"]) -> None:
        """
        Initialize class.

        Common init code for constructors.
        """
        # logger.warning("FLSqlCursor(%s): Init() %s (%s, %s)" , name, self, cR, r, stack_info=True)

        # if self.d.metadata_ and not self.d.metadata_.aqWasDeleted() and not
        # self.d.metadata_.inCache():

        self.d.curName_ = name
        if self.setAction(name):
            self.d.countRefCursor = self.d.countRefCursor + 1
        else:
            # logger.trace("FLSqlCursor(%s).init(): ¿La tabla no existe?" % name)
            return None

        self.d.modeAccess_ = PNSqlCursor.Browse

        self.d.cursorRelation_ = cR
        if r:  # FLRelationMetaData
            if self.relation():
                del self.d.relation_

            # r.ref()
            self.d.relation_ = r
        else:
            self.d.relation_ = None

        if not self.d.metadata_:
            return

        # if project.DGI.use_model():
        #    self.build_cursor_tree_dict()

        self.d.isQuery_ = self.d.metadata_.isQuery()
        if (name[len(name) - 3 :]) == "sys" or self.db().manager().isSystemTable(name):
            self.d.isSysTable_ = True
        else:
            self.d.isSysTable_ = False

        # if self.d.isQuery_:
        #     qry = self.db().manager().query(self.d.metadata_.query(), self)
        #     self.d.query_ = qry.sql()
        #     if qry and self.d.query_:
        #         self.exec_(self.d.query_)
        #     if qry:
        #         self.qry.deleteLater()
        # else:
        #     self.setName(self.d.metadata_.name(), autopopulate)
        self.setName(self.d.metadata_.name(), autopopulate)

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
                project.DGI.use_model() and cR.meta_model()
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

    def conn(self) -> "IConnection":
        """Get current connection for this cursor."""
        return self.db()

    def table(self) -> str:
        """Get current table or empty string."""
        m = self.d.metadata_
        if m:
            return m.name()
        else:
            return ""

    # def __getattr__(self, name):
    #    return DefFun(self, name)

    def setName(self, name: str, autop: bool) -> None:
        """Set cursor name."""
        self.name = name
        # FIXME: autopop probably means it should do a refresh upon construction.
        # autop = autopopulate para que??

    def metadata(self) -> "PNTableMetaData":
        """
        Retrieve PNTableMetaData for current table.

        @return PNTableMetaData object with metadata related to cursor table.
        """
        if self.d.metadata_ is None:
            raise Exception("metadata is empty!")

        return self.d.metadata_

    def currentRegister(self) -> int:
        """
        Get current row number selected by the cursor.

        @return Integer cotining record number.
        """
        return self.d._currentregister

    def modeAccess(self) -> int:
        """
        Get current access mode for cursor.

        @return PNSqlCursor::Mode constant defining mode access prepared
        """
        return self.d.modeAccess_

    def mainFilter(self) -> str:
        """
        Retrieve main filter for cursor.

        @return String containing the WHERE clause part that will be appended on select.
        """
        ret_ = None
        if hasattr(self.d._model, "where_filters"):
            ret_ = self.d._model.where_filters["main-filter"]

        if ret_ is None:
            ret_ = ""

        return ret_

    def action(self) -> Optional["FLAction"]:
        """
        Get FLAction related to this cursor.

        @return FLAction object.
        """
        return self._action if self._action else None

    def actionName(self) -> str:
        """Get action name from FLAction related to the cursor. Returns empty string if none is set."""
        return self._action.name() if self._action else ""

    def setAction(self, a: Union[str, "FLAction"]) -> bool:
        """
        Set action to be related to this cursor.

        @param FLAction object
        @return True if success, otherwise False.
        """
        action = None

        if isinstance(a, str):
            action = self.db().manager().action(a.lower())

            if action.table() == "":
                action.setTable(a)
        else:
            action = a

        if self._action is None:
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
                return True

            if self.action() is not None:  # La action previa existe y no es la misma tabla
                self._action = action
                self.d.buffer_ = None
                self.d.metadata_ = None

        if self._action is None:
            raise Exception("Unexpected: Action is still None")

        if not self._action.table():
            return False

        if not self.d.metadata_:
            self.d.metadata_ = self.db().manager().metadata(self._action.table())

        self.d.doAcl()

        from .pncursortablemodel import PNCursorTableModel

        self.d._model = PNCursorTableModel(self.conn(), self)
        if not self.d._model:
            return False

        # if not self.d.buffer_:
        #    self.primeInsert()

        self._selection = QtCore.QItemSelectionModel(self.d._model)
        self.selection().currentRowChanged.connect(self.selection_currentRowChanged)
        self._currentregister = self.selection().currentIndex().row()
        self.d.metadata_ = self.db().manager().metadata(self._action.table())
        self.d.activatedCheckIntegrity_ = True
        self.d.activatedCommitActions_ = True
        return True

    def setMainFilter(self, f: str, doRefresh: bool = True) -> None:
        """
        Set main cursor filter.

        @param f String containing the filter in SQL WHERE format (excluding WHERE)
        @param doRefresh By default, refresh the cursor afterwards. Set to False to avoid this.
        """
        # if f == "":
        #    f = "1 = 1"

        # logger.trace("--------------------->Añadiendo filtro",  f)
        none_f: Optional[str] = f
        if none_f is None:
            logger.warning("setMainFilter: f does not accept 'None'. Use empty string instead.")
            f = ""
        if self.d._model and getattr(self.d._model, "where_filters", None):
            self.d._model.where_filters["main-filter"] = f
            if doRefresh:
                self.refresh()

    def setModeAccess(self, m: int) -> None:
        """
        Set cursor access mode.

        @param m PNSqlCursor::Mode constant which inidicates access mode.
        """
        self.d.modeAccess_ = m

    def connectionName(self) -> str:
        """
        Get database connection alias name.

        @return String containing the connection name.
        """
        return self.db().connectionName()

    def setAtomicValueBuffer(self, fN: str, functionName: str) -> None:
        """
        Set a buffer field value in atomic fashion and outside transaction.

        Invoca a la función, cuyo nombre se pasa como parámetro, del script del contexto del cursor
        (ver PNSqlCursor::ctxt_) para obtener el valor del campo. El valor es establecido en el campo de forma
        atómica, bloqueando la fila durante la actualización. Esta actualización se hace fuera de la transacción
        actual, dentro de una transacción propia, lo que implica que el nuevo valor del campo está inmediatamente
        disponible para las siguientes transacciones.

        @param fN Nombre del campo
        @param functionName Nombre de la función a invocar del script
        """
        if not self.d.buffer_ or not fN or not self.d.metadata_:
            return

        field = self.d.metadata_.field(fN)

        if field is None:
            logger.warning("setAtomicValueBuffer(): No existe el campo %s:%s", self.d.metadata_.name(), fN)
            return

        if not self.db().dbAux():
            return

        type = field.type()
        # fltype = FLFieldself.d.metadata_.FlDecodeType(type)
        pK = self.d.metadata_.primaryKey()
        v: Any

        if self.d.cursorRelation_ and self.modeAccess() == self.Browse:
            self.self.d.cursorRelation_.commit(False)

        if pK and self.db().db() is not self.db().dbAux():
            pKV = self.d.buffer_.value(pK)
            self.db().dbAux().transaction()

            arglist: List[Any] = []
            arglist.append(fN)
            arglist.append(self.d.buffer_.value(fN))
            v = project.call(functionName, arglist, self.context())

            q = PNSqlQuery(None, self.db().dbAux())
            ret = q.exec_(
                "UPDATE  %s SET %s = %s WHERE %s"
                % (
                    self.d.metadata_.name(),
                    fN,
                    self.db().manager().formatValue(type, v),
                    self.db().manager().formatAssignValue(self.d.metadata_.field(pK), pKV),
                )
            )
            if ret:
                self.db().dbAux().commit()
            else:
                self.db().dbAux().rollbackTransaction()
        else:
            logger.warning("No se puede actualizar el campo de forma atómica, porque no existe clave primaria")

        self.d.buffer_.setValue(fN, v)
        if self.activatedBufferChanged():
            if project.DGI.use_model() and self.meta_model():
                bch_model = getattr(self.meta_model(), "bChCursor", None)
                if bch_model and bch_model(fN, self) is False:
                    return

                from pineboolib import qsa  # FIXME: Should not import QSA at all

                script = getattr(qsa, "formRecord%s" % self.action(), None)
                if script is not None:
                    bChCursor = getattr(script.iface, "bChCursor", None)
                    if bChCursor:
                        bChCursor(fN, self)

            self.bufferChanged.emit(fN)

            project.app.processEvents()

    def setValueBuffer(self, fN: str, v: Any) -> None:
        """
        Set buffer value for a particular field.

        @param fN field name
        @param v Value to be set to the buffer field.
        """

        if not self.buffer():
            return

        if not fN or not self.d.metadata_:
            logger.warning("setValueBuffer(): No fieldName, or no metadata found")
            return

        if not self.d.buffer_:
            logger.warning("setValueBuffer(): No buffer")
            return

        field = self.d.metadata_.field(fN)
        if field is None:
            logger.warning("setValueBuffer(): No existe el campo %s:%s", self.curName(), fN)
            return
        db = self.db()
        manager = db.manager()
        if manager is None:
            raise Exception("no manager")

        type_ = field.type()
        buff_field = self.d.buffer_.field(fN)
        if buff_field and not buff_field.has_changed(v):
            return

        # if not self.buffer():  # Si no lo pongo malo....
        #    self.primeUpdate()

        # if not fN or not self.d.metadata_:
        #    return

        # field = self.d.metadata_.field(fN)
        # if field is None:
        #    logger.warning("PNSqlCursor::setValueBuffer() : No existe el campo %s:%s", self.d.metadata_.name(), fN)
        #    return

        # fltype = field.flDecodeType(type_)
        vv = v

        if vv and type_ == "pixmap" and not manager.isSystemTable(self.table()):
            vv = db.normalizeValue(vv)
            largeValue = manager.storeLargeValue(self.d.metadata_, vv)
            if largeValue:
                vv = largeValue

        if field.outTransaction() and db.db() is not db.dbAux() and self.modeAccess() != self.Insert:
            pK = self.d.metadata_.primaryKey()

            if self.d.cursorRelation_ is not None and self.modeAccess() != self.Browse:
                self.d.cursorRelation_.commit(False)

            if pK:
                pKV = self.d.buffer_.value(pK)
                q = PNSqlQuery(None, "dbAux")
                q.exec_(
                    "UPDATE %s SET %s = %s WHERE %s;"
                    % (
                        self.d.metadata_.name(),
                        fN,
                        manager.formatValue(type_, vv),
                        manager.formatAssignValue(self.d.metadata_.field(pK), pKV),
                    )
                )
            else:
                logger.warning("FLSqlCursor : No se puede actualizar el campo fuera de transaccion, porque no existe clave primaria")

        else:
            self.d.buffer_.setValue(fN, vv)

        # logger.trace("(%s)bufferChanged.emit(%s)" % (self.curName(),fN))
        if self.activatedBufferChanged():

            if project.DGI.use_model() and self.meta_model():
                bch_model = getattr(self.meta_model(), "bChCursor", None)
                if bch_model and bch_model(fN, self) is False:
                    return

                from pineboolib import qsa  # FIXME: Should not import QSA at all

                script = getattr(qsa, "formRecord%s" % self.action(), None)
                if script is not None:
                    bChCursor = getattr(script.iface, "bChCursor", None)
                    if bChCursor:
                        bChCursor(fN, self)

            self.bufferChanged.emit(fN)
        project.app.processEvents()

    def valueBuffer(self, fN: str) -> Any:
        """
        Retrieve a value from a field buffer (self.d.buffer_).

        @param fN field name
        """
        fN = str(fN)

        if project.DGI.use_model():
            if fN == "pk":
                # logger.warning("¡¡¡¡ OJO Cambiado fieldname PK!!", stack_info = True)
                pk_name = self.primaryKey()
                if pk_name is None:
                    raise Exception("primary key is not defined!")

                fN = pk_name

        if self.d.rawValues_:
            return self.valueBufferRaw(fN)

        if not self.d.metadata_:
            return None

        if (self.d._model.rows > 0 and not self.modeAccess() == PNSqlCursor.Insert) or not self.buffer():
            if not self.buffer():
                self.refreshBuffer()

            if not self.buffer():
                return None

        field = self.d.metadata_.field(fN)
        if field is None:
            logger.warning("valueBuffer(): No existe el campo %s:%s en la tabla %s", self.curName(), fN, self.d.metadata_.name())
            return None

        type_ = field.type()

        v = None
        if field.outTransaction() and self.db().db() is not self.db().dbAux() and self.modeAccess() != self.Insert:
            pK = self.d.metadata_.primaryKey()

            if self.d.buffer_ is None:
                return None
            if pK:

                pKV = self.d.buffer_.value(pK)
                q = PNSqlQuery(None, "dbAux")
                sql_query = "SELECT %s FROM %s WHERE %s" % (
                    fN,
                    self.d.metadata_.name(),
                    self.db().manager().formatAssignValue(self.d.metadata_.field(pK), pKV),
                )
                # q.exec_(self.db().dbAux(), sql_query)
                q.exec_(sql_query)
                if q.next():
                    v = q.value(0)
            else:
                logger.warning("No se puede obtener el campo fuera de transacción porque no existe clave primaria")

        else:

            if self.d.buffer_ is None:
                return None
            v = self.d.buffer_.value(fN)

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

    def fetchLargeValue(self, value: str) -> Any:
        """Retrieve large value from database."""
        return self.db().manager().fetchLargeValue(value)

    def valueBufferCopy(self, fN: str) -> Any:
        """
        Retrieve original value for a field before it was changed.

        @param fN field name
        """
        if not self.bufferCopy() or not self.d.metadata_:
            return None

        field = self.d.metadata_.field(fN)
        if field is None:
            logger.warning("FLSqlCursor::valueBufferCopy() : No existe el campo " + self.d.metadata_.name() + ":" + fN)
            return None

        type_ = field.type()
        bufferCopy = self.bufferCopy()
        if bufferCopy is None:
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

    def setEdition(self, b: bool, m: Optional[str] = None) -> None:
        """
        Put cursor into "edition" mode.

        @param b TRUE or FALSE
        """
        # FIXME: What is "edition" ??
        if m is None:
            self.d.edition_ = b
            return

        state_changes = b != self.d.edition_

        if state_changes and not self.d.edition_states_:
            self.d.edition_states_ = AQBoolFlagStateList()

        # if self.d.edition_states_ is None:
        #     return

        i = self.d.edition_states_.find(m)
        if not i and state_changes:
            i = AQBoolFlagState()
            i.modifier_ = m
            i.prevValue_ = self.d.edition_
            self.d.edition_states_.append(i)
        elif i:
            if state_changes:
                self.d.edition_states_.pushOnTop(i)
                i.prevValue_ = self.d.edition_
            else:
                self.d.edition_states_.erase(i)

        if state_changes:
            self.d.edition_ = b

    def restoreEditionFlag(self, m: str) -> None:
        """Restore Edition flag to its previous value."""
        if not self.d.edition_states_:
            return

        i = self.d.edition_states_.find(m)

        if i and i == self.d.edition_states_.current():
            self.d.edition_ = i.prevValue_

        if i:
            self.d.edition_states_.erase(i)

    def setBrowse(self, b: bool, m: Optional[str] = None) -> None:
        """
        Put cursor into browse mode.

        @param b TRUE or FALSE
        """
        if not m:
            self.d.browse_ = b
            return

        state_changes = b != self.d.browse_

        if state_changes and not self.d.browse_states_:
            self.d.browse_states_ = AQBoolFlagStateList()

        if not self.d.browse_states_:
            return

        i = self.d.browse_states_.find(m)
        if not i and state_changes:
            i = AQBoolFlagState()
            i.modifier_ = m
            i.prevValue_ = self.d.browse_
            self.d.browse_states_.append(i)
        elif i:
            if state_changes:
                self.d.browse_states_.pushOnTop(i)
                i.prevValue_ = self.d.browse_
            else:
                self.d.browse_states_.erase(i)

        if state_changes:
            self.d.browse_ = b

    def restoreBrowseFlag(self, m: str) -> None:
        """Restores browse flag to its previous state."""
        if not self.d.browse_states_:
            return

        i = self.d.browse_states_.find(m)

        if i and i == self.d.browse_states_.current():
            self.d.browse_ = i.prevValue_

        if i:
            self.d.browse_states_.erase(i)

    def meta_model(self) -> bool:
        """
        Check if DGI requires models (SqlAlchemy?).
        """
        return self._meta_model if project.DGI.use_model() else False

    def setContext(self, c: Any = None) -> None:
        """
        Set cursor context for script execution.

        This can be for master or formRecord.

        See FLSqlCursor::ctxt_.

        @param c Execution Context
        """
        if c:
            self.d.ctxt_ = weakref.ref(c)

    def context(self) -> Any:
        """
        Retrieve current context of execution of scripts for this cursor.

        See FLSqlCursor::ctxt_.

        @return Execution context
        """
        if self.d.ctxt_:
            return self.d.ctxt_()
        else:
            logger.debug("%s.context(). No hay contexto" % self.curName())
            return None

    def fieldDisabled(self, fN: str) -> bool:
        """
        Check if a field is disabled.

        Un campo estará deshabilitado, porque esta clase le dará un valor automáticamente.
        Estos campos son los que están en una relación con otro cursor, por lo que
        su valor lo toman del campo foráneo con el que se relacionan.

        @param fN Nombre del campo a comprobar
        @return TRUE si está deshabilitado y FALSE en caso contrario
        """
        if self.modeAccess() in (self.Insert, self.Edit):

            if self.d.cursorRelation_ is not None and self.d.relation_ is not None:
                if not self.d.cursorRelation_.metadata():
                    return False
                field = self.d.relation_.field()
                if field.lower() == fN.lower():
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def inTransaction(self) -> bool:
        """
        Check if there is a transaction in progress.

        @return TRUE if there is one.
        """
        if self.db():
            if self.db().transaction_ > 0:
                return True

        return False

    def transaction(self, lock: bool = False) -> bool:
        """
        Start a new transaction.

        Si ya hay una transacción en curso simula un nuevo nivel de anidamiento de
        transacción mediante un punto de salvaguarda.

        @param  lock Actualmente no se usa y no tiene ningún efecto. Se mantiene por compatibilidad hacia atrás
        @return TRUE si la operación tuvo exito
        """
        if not self.db() and not self.db().db():
            logger.warning("transaction(): No hay conexión con la base de datos")
            return False

        return self.db().doTransaction(self)

    def rollback(self) -> bool:
        """
        Undo operations from a transaction and cleans up.

        @return TRUE if success.
        """
        if not self.db() and not self.db().db():
            logger.warning("rollback(): No hay conexión con la base de datos")
            return False

        return self.db().doRollback(self)

    def commit(self, notify: bool = True) -> bool:
        """
        Finishes and commits transaction.

        @param notify If TRUE emits signal cursorUpdated and sets cursor on BROWSE,
              If FALSE skips and emits autoCommit signal.
        @return TRUE if success.
        """
        if not self.db() and not self.db().db():
            logger.warning("commit(): No hay conexión con la base de datos")
            return False

        r = self.db().doCommit(self, notify)
        if r:
            self.commited.emit()

        return r

    def size(self) -> int:
        """Get number of records in the cursor."""
        return self.d._model.size()

    def openFormInMode(self, m: int, wait: bool = True, cont: bool = True) -> None:
        """
        Open form associated with the table in the specified mode.

        @param m Opening mode. (FLSqlCursor::Mode)
        @param wait Indica que se espera a que el formulario cierre para continuar
        @param cont Indica que se abra el formulario de edición de registros con el botón de
        aceptar y continuar
        """
        if not self.d.metadata_:
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

        if self.d.buffer_:
            self.d.buffer_.clearValues(True)

        # if not self.d._action:
        # self.d.action_ = self.db().manager().action(self.d.metadata_.name())

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

    def isNull(self, fN: str) -> bool:
        """Get if a field is null."""
        if not self.d.buffer_:
            raise Exception("No buffer set")
        return self.d.buffer_.isNull(fN)

    def isCopyNull(self, fN: str) -> bool:
        """Get if a field was null before changing."""
        if not self.d.bufferCopy_:
            raise Exception("No buffer_copy set")
        return self.d.bufferCopy_.isNull(fN)

    def updateBufferCopy(self) -> None:
        """
        Copy contents of FLSqlCursor::buffer_ into FLSqlCursor::bufferCopy_.

        This copy allows later to check if the buffer was changed using
        FLSqlCursor::isModifiedBuffer().
        """
        if not self.buffer():
            return None

        if self.d.bufferCopy_:
            del self.d.bufferCopy_

        self.d.bufferCopy_ = PNBuffer(self)
        bufferCopy = self.bufferCopy()
        if bufferCopy is None:
            raise Exception("No buffercopy")

        if self.d.buffer_ is not None:
            for field in self.d.buffer_.fieldsList():
                bufferCopy.setValue(field.name, self.d.buffer_.value(field.name), False)

    def isModifiedBuffer(self) -> bool:
        """
        Check if current buffer contents are different from the original copy.

        See FLSqlCursor::bufferCopy_ .

        @return True if different. False if equal.
        """

        if self.d.buffer_ is None:
            return False

        modifiedFields = self.d.buffer_.modifiedFields()
        if modifiedFields:
            return True
        else:
            return False

    def setAskForCancelChanges(self, a: bool) -> None:
        """
        Set value for FLSqlCursor::askForCancelChanges_ .

        @param a If True, a popup will appear warning the user for unsaved changes on cancel.
        """
        self.d.askForCancelChanges_ = a

    def setActivatedCheckIntegrity(self, a: bool) -> None:
        """
        Enable or disable integrity checks.

        @param a TRUE los activa y FALSE los desactiva
        """
        self.d.activatedCheckIntegrity_ = a

    def activatedCheckIntegrity(self) -> bool:
        """Retrieve if integrity checks are enabled."""
        return self.d.activatedCheckIntegrity_

    def setActivatedCommitActions(self, a: bool) -> None:
        """
        Enable or disable before/after commit actions.

        @param a True to enable, False to disable.
        """
        self.d.activatedCommitActions_ = a

    def activatedCommitActions(self) -> bool:
        """
        Retrieve wether before/after commits are enabled.
        """
        return self.d.activatedCommitActions_

    def setActivatedBufferChanged(self, activated_bufferchanged: bool) -> None:
        """Enable or disable bufferChanged signals."""
        self._activatedBufferChanged = activated_bufferchanged

    def activatedBufferChanged(self) -> bool:
        """Retrieve if bufferChanged signals are enabled."""
        return self._activatedBufferChanged

    def setActivatedBufferCommited(self, activated_buffercommited: bool) -> None:
        """Enable or disable bufferCommited signals."""
        self._activatedBufferCommited = activated_buffercommited

    def activatedBufferCommited(self) -> bool:
        """Retrieve wether bufferCommited signals are enabled."""
        return self._activatedBufferCommited

    def msgCheckIntegrity(self) -> str:
        """
        Get message for integrity checks.

        The referential integrity is checked when trying to delete, the non-duplication of
        primary keys and if there are nulls in fields that do not allow it when inserted or edited.
        If any verification fails, it returns a message describing the fault.

        @return Error message
        """
        msg = ""

        if self.d.buffer_ is None or self.d.metadata_ is None:
            msg = "\nBuffer vacío o no hay metadatos"
            return msg

        if self.d.modeAccess_ in [self.Insert, self.Edit]:
            if not self.isModifiedBuffer() and self.d.modeAccess_ == self.Edit:
                return msg
            fieldList = self.d.metadata_.fieldList()
            checkedCK = False

            if not fieldList:
                return msg

            for field in fieldList:

                fiName = field.name()
                if not self.d.buffer_.isGenerated(fiName):
                    continue

                s = None
                if not self.d.buffer_.isNull(fiName):
                    s = self.d.buffer_.value(fiName)

                fMD = field.associatedField()
                if fMD and s is not None:
                    if not field.relationM1():
                        msg = (
                            msg + "\n" + "FLSqlCursor : Error en metadatos, el campo %s tiene un campo asociado pero no existe "
                            "relación muchos a uno:%s" % (self.d.metadata_.name(), fiName)
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
                    if not self.d.buffer_.isNull(fmdName):
                        ss = self.d.buffer_.value(fmdName)
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
                            msg = msg + "\n" + self.d.metadata_.name() + ":" + field.alias() + " : %s no pertenece a %s" % (s, ss)
                        else:
                            self.d.buffer_.setValue(fmdName, q.value(0))

                    else:
                        msg = msg + "\n" + self.d.metadata_.name() + ":" + field.alias() + " : %s no se puede asociar a un valor NULO" % s
                    if not tMD.inCache():
                        del tMD

                if self.d.modeAccess_ == self.Edit:
                    if self.d.buffer_ and self.d.bufferCopy_:
                        if self.d.buffer_.value(fiName) == self.d.bufferCopy_.value(fiName):
                            continue

                if self.d.buffer_.isNull(fiName) and not field.allowNull() and not field.type() == "serial":
                    msg = msg + "\n" + self.d.metadata_.name() + ":" + field.alias() + " : No puede ser nulo"

                if field.isUnique():
                    pK = self.d.metadata_.primaryKey()
                    if not self.d.buffer_.isNull(pK) and s is not None:
                        pKV = self.d.buffer_.value(pK)
                        field_mtd = self.d.metadata_.field(pK)
                        if field_mtd is None:
                            raise Exception("pk field is not found!")
                        q = PNSqlQuery(None, self.db().connectionName())
                        q.setTablesList(self.d.metadata_.name())
                        q.setSelect(fiName)
                        q.setFrom(self.d.metadata_.name())
                        q.setWhere(
                            "%s AND %s <> %s"
                            % (
                                self.db().manager().formatAssignValue(field, s, True),
                                self.d.metadata_.primaryKey(self.d.isQuery_),
                                self.db().manager().formatValue(field_mtd.type(), pKV),
                            )
                        )
                        q.setForwardOnly(True)
                        q.exec_()
                        if q.next():
                            msg = (
                                msg
                                + "\n"
                                + self.d.metadata_.name()
                                + ":"
                                + field.alias()
                                + " : Requiere valores únicos, y ya hay otro registro con el valor %s en este campo" % s
                            )

                if field.isPrimaryKey() and self.d.modeAccess_ == self.Insert and s is not None:
                    q = PNSqlQuery(None, self.db().connectionName())
                    q.setTablesList(self.d.metadata_.name())
                    q.setSelect(fiName)
                    q.setFrom(self.d.metadata_.name())
                    q.setWhere(self.db().manager().formatAssignValue(field, s, True))
                    q.setForwardOnly(True)
                    q.exec_()
                    if q.next():
                        msg = (
                            msg
                            + "\n"
                            + self.d.metadata_.name()
                            + ":"
                            + field.alias()
                            + " : Es clave primaria y requiere valores únicos, y ya hay otro registro con el valor %s en este campo" % s
                        )

                if field.relationM1() and s:
                    if field.relationM1().checkIn() and not field.relationM1().foreignTable() == self.d.metadata_.name():
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
                                + self.d.metadata_.name()
                                + ":"
                                + field.alias()
                                + " : El valor %s no existe en la tabla %s" % (s, r.foreignTable())
                            )
                        else:
                            self.d.buffer_.setValue(fiName, q.value(0))

                        if not tMD.inCache():
                            del tMD

                fieldListCK = self.d.metadata_.fieldListOfCompoundKey(fiName)
                if fieldListCK and not checkedCK and self.d.modeAccess_ == self.Insert:
                    if fieldListCK:
                        filterCK: Optional[str] = None
                        field_1: Optional[str] = None
                        valuesFields: Optional[str] = None
                        for fieldCK in fieldListCK:
                            sCK = self.d.buffer_.value(fieldCK.name())
                            if filterCK is None:
                                filterCK = self.db().manager().formatAssignValue(fieldCK, sCK, True)
                            else:
                                filterCK = "%s AND %s" % (filterCK, self.db().manager().formatAssignValue(fieldCK, sCK, True))
                            if field_1 is None:
                                field_1 = fieldCK.alias()
                            else:
                                field_1 = "%s+%s" % (field_1, fieldCK.alias())
                            if valuesFields is None:
                                valuesFields = str(sCK)
                            else:
                                valuesFields = "%s+%s" % (valuesFields, str(sCK))

                        q = PNSqlQuery(None, self.db().connectionName())
                        q.setTablesList(self.d.metadata_.name())
                        q.setSelect(fiName)
                        q.setFrom(self.d.metadata_.name())
                        if filterCK is not None:
                            q.setWhere(filterCK)
                        q.setForwardOnly(True)
                        q.exec_()
                        if q.next():
                            msg = msg + "\n%s : Requiere valor único, y ya hay otro registro con el valor %s en la tabla %s" % (
                                field_1,
                                valuesFields,
                                self.d.metadata_.name(),
                            )

                        checkedCK = True

        elif self.d.modeAccess_ == self.Del:
            fieldList = self.d.metadata_.fieldList()
            fiName = None
            s = None

            for field in fieldList:
                # fiName = field.name()
                if not self.d.buffer_.isGenerated(field.name()):
                    continue

                s = None

                if not self.d.buffer_.isNull(field.name()):
                    s = self.d.buffer_.value(field.name())
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
                                % (mtd.name(), r.foreignField(), self.d.metadata_.name(), field.name())
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
                                + self.d.metadata_.name()
                                + ":"
                                + field.alias()
                                + " : Con el valor %s hay registros en la tabla %s:%s" % (s, mtd.name(), mtd.alias())
                            )

                        if not mtd.inCache():
                            del mtd

        return msg

    def checkIntegrity(self, showError: bool = True) -> bool:
        """
        Perform integrity checks.

        The referential integrity is checked when trying to delete, the non-duplication of
        primary keys and if there are nulls in fields that do not allow it when inserted or edited.
        If any check fails it displays a dialog box with the type of fault found and the method
        returns FALSE.

        @param showError If TRUE shows the dialog box with the error that occurs when the pass integrity checks
        @return TRUE if the buffer could be delivered to the cursor, and FALSE if any verification failed of integrity
        """
        if not self.buffer() or not self.d.metadata_:
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

    def cursorRelation(self) -> Optional["PNSqlCursor"]:
        """
        Return the cursor relationed.

        @return PNSqlCursor relationed or None
        """
        return self.d.cursorRelation_

    def relation(self) -> Optional["PNRelationMetaData"]:
        """
        Return the relation metadata.

        @return PNRelationMetaData relationed or None.
        """
        return self.d.relation_

    def setUnLock(self, fN: str, v: bool) -> None:
        """
        Unlock the current cursor record.

        @param fN Field name.
        @param v Value for the unlock field.
        """

        if not self.d.metadata_ or not self.modeAccess() == self.Browse:
            return

        field_mtd = self.d.metadata_.field(fN)
        if field_mtd is None:
            raise Exception("Field %s is empty!" % fN)

        if not field_mtd.type() == "unlock":
            logger.warning("setUnLock sólo permite modificar campos del tipo Unlock")
            return

        if not self.d.buffer_:
            self.primeUpdate()

        if not self.d.buffer_:
            raise Exception("Unexpected null buffer")

        self.setModeAccess(self.Edit)
        self.d.buffer_.setValue(fN, v)
        self.update()
        self.refreshBuffer()

    def isLocked(self) -> bool:
        """
        To check if the current cursor record is locked.

        @return TRUE if blocked, FALSE otherwise.
        """
        if not self.d.metadata_:
            return False

        ret_ = False
        if self.d.modeAccess_ is not self.Insert:
            row = self.currentRegister()

            for field in self.d.metadata_.fieldNamesUnlock():
                if row > -1:
                    if self.d._model.value(row, field) not in ("True", True, 1, "1"):
                        ret_ = True
                        break

        if not ret_ and self.d.cursorRelation_ is not None:
            ret_ = self.d.cursorRelation_.isLocked()

        return ret_

    def buffer(self) -> Optional[PNBuffer]:
        """
        Return the content of the buffer.

        @return PNBuffer or None.
        """
        return self.d.buffer_

    def bufferCopy(self) -> Optional[PNBuffer]:
        """
        Return the contents of the bufferCopy.

        @return PNBuffer or None.
        """
        return self.d.bufferCopy_

    def bufferIsNull(self, pos_or_name: Union[int, str]) -> bool:
        """
        Return if the content of a field in the buffer is null.

        @param pos_or_name Name or pos of the field in the buffer.
        @return True or False
        """

        if self.d.buffer_ is not None:
            return self.d.buffer_.isNull(pos_or_name)

        return True

    def bufferSetNull(self, pos_or_name: Union[int, str]) -> None:
        """
        Set the content of a field in the buffer to be null.

        @param pos_or_name Name or pos of the field in the buffer.
        """

        if self.d.buffer_ is not None:
            self.d.buffer_.setNull(pos_or_name)

    def bufferCopyIsNull(self, pos_or_name: Union[int, str]) -> bool:
        """
        Return if the content of a field in the bufferCopy is null.

        @param pos_or_name Name or pos of the field in the bufferCopy
        """

        if self.d.bufferCopy_ is not None:
            return self.d.bufferCopy_.isNull(pos_or_name)
        return True

    def bufferCopySetNull(self, pos_or_name: Union[int, str]) -> None:
        """
        Set the content of a field in the bufferCopy to be null.

        @param pos_or_name Name or pos of the field in the bufferCopy
        """

        if self.d.bufferCopy_ is not None:
            self.d.bufferCopy_.setNull(pos_or_name)

    def atFrom(self) -> int:
        """
        Get the position of the current record, according to the primary key contained in the self.d.buffer_.

        The position of the current record within the cursor is calculated taking into account the
        Current filter (FLSqlCursor :: curFilter ()) and the field or sort fields of it (QSqlCursor :: sort ()).
        This method is useful, for example, to know at what position within the cursor
        A record has been inserted.

        @return Position of the record within the cursor, or 0 if it does not match.
        """

        if not self.buffer() or not self.d.metadata_:
            return 0
        # Faster version for this function::
        if self.isValid():
            pos = self.at()
        else:
            pos = 0
        return pos

    def atFromBinarySearch(self, fN: str, v: Any, orderAsc: bool = True) -> int:
        """
        Get the position within the cursor of the first record in the indicated field start with the requested value.

        It assumes that the records are ordered by that field, to perform a binary search.
        The position of the current record within the cursor is calculated taking into account the
        Current filter (FLSqlCursor :: curFilter ()) and the field or sort fields
        of it (QSqlCursor :: sort ()).
        This method is useful, for example, to know at what position within the cursor
        a record with a certain value is found in a field.

        @param fN Name of the field in which to look for the value
        @param v Value to look for (using like 'v%')
        @param orderAsc TRUE (default) if the order is ascending, FALSE if it is descending
        @return Position of the record within the cursor, or 0 if it does not match.
        """

        ret = -1
        ini = 0
        fin = self.size() - 1
        mid = None
        comp = None
        midVal = None

        if not self.d.metadata_:
            raise Exception("Metadata is not set")

        if fN in self.d.metadata_.fieldNames():
            while ini <= fin:
                mid = int((ini + fin) / 2)
                midVal = str(self.d._model.value(mid, fN))
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

    # """
    # Redefinido por conveniencia
    # """

    # @decorators.NotImplementedWarn
    # def exec_(self, query: str) -> bool:
    # if query:
    #    logger.debug("ejecutando consulta " + query)
    #    QSqlQuery.exec(self, query)

    #    return True

    def setNull(self, name: str) -> None:
        """Specify a field as Null."""

        self.setValueBuffer(name, None)

    def db(self) -> "IConnection":
        """
        To get the database you work on.

        @return PNConnection used by the cursor.
        """

        if not self.d.db_:
            raise Exception("db_ is not defined!")

        return self.d.db_

    def curName(self) -> str:
        """
        To get the cursor name (usually the table name).

        @return cursor Name
        """
        return self.d.curName_

    """
    Para obtener el filtro por defecto en campos asociados

    @param  fieldName Nombre del campo que tiene campos asociados.
                    Debe ser el nombre de un campo de este cursor.
    @param  tableMD   Metadatos a utilizar como tabla foránea.
                    Si es cero usa la tabla foránea definida por la relación M1 de 'fieldName'
    """

    def filterAssoc(self, fieldName: str, tableMD: Optional["PNTableMetaData"] = None) -> Optional[str]:
        """
        To get the default filter in associated fields.

        @param fieldName Name of the field that has associated fields. It must be the name of a field of this cursor.
        @param tableMD Metadata to use as a foreign table. If it is zero use the foreign table defined by the relation M1 of 'fieldName'.
        """
        fieldName = fieldName

        mtd = self.d.metadata_
        if not mtd:
            return None

        field = mtd.field(fieldName)
        if field is None:
            return None

        # ownTMD = False

        if not tableMD:
            # ownTMD = True
            rel_m1 = field.relationM1()
            if rel_m1 is None:
                raise Exception("relation is empty!")
            tableMD = self.db().manager().metadata(rel_m1.foreignTable())

        if not tableMD:
            return None

        fieldAc = field.associatedField()
        if fieldAc is None:
            # if ownTMD and not tableMD.inCache():
            # del tableMD
            return None

        fieldBy = field.associatedFieldFilterTo()

        if self.d.buffer_ is None:
            return None

        if not tableMD.field(fieldBy) or self.d.buffer_.isNull(fieldAc.name()):
            # if ownTMD and not tableMD.inCache():
            # del tableMD
            return None

        vv = self.d.buffer_.value(fieldAc.name())
        if vv:
            # if ownTMD and not tableMD.inCache():
            # del tableMD
            return self.db().manager().formatAssignValue(fieldBy, fieldAc, vv, True)

        # if ownTMD and not tableMD.inCache():
        # del rableMD

        return None

    @decorators.BetaImplementation
    def aqWasDeleted(self) -> bool:
        """
        Indicate if the cursor has been deleted.

        @return True or False.
        """
        return False

    @decorators.NotImplementedWarn
    def calculateField(self, name: str) -> bool:
        """
        Indicate if the field is calculated.

        @return True or False.
        """
        return True

    def model(self) -> "PNCursorTableModel":
        """
        Return the tablemodel used by the cursor.

        @return PNCursorTableModel used.
        """
        return self.d._model

    def selection(self) -> Any:
        """
        Return the item pointed to in the tablemodel.

        @return selected Item.
        """
        return self._selection

    @pyqtSlot(QtCore.QModelIndex, QtCore.QModelIndex)
    @pyqtSlot(int, int)
    @pyqtSlot(int)
    def selection_currentRowChanged(self, current: Any, previous: Any = None) -> None:
        """
        Update the current record pointed to by the tablemodel.

        @param current. new item selected.
        @param previous. old item selected.
        """

        if self.currentRegister() == current.row():
            self.d.doAcl()
            return None

        self.d._currentregister = current.row()
        self.d._current_changed.emit(self.at())
        # agregado para que FLTableDB actualice el buffer al pulsar.
        self.refreshBuffer()
        self.d.doAcl()
        if self._action:
            logger.debug("cursor:%s , row:%s:: %s", self._action.table(), self.currentRegister(), self)

    def selection_pk(self, value: str) -> bool:
        """
        Move the cursor position to the one that matches the primaryKey value.

        @param value. primaryKey value to search.
        @return True if seek the position else False.
        """

        # if value is None:
        #     return False

        i = 0

        if not self.d.buffer_:
            raise Exception("Buffer not set")
        while i <= self.d._model.rowCount():
            pk_value = self.d.buffer_.pK()
            if pk_value is None:
                raise ValueError("pk_value is empty!")

            if self.d._model.value(i, pk_value) == value:
                return self.move(i)

            i = i + 1

        return False

    def at(self) -> int:
        """
        Return the current position to which the cursor points.

        @return Index position.
        """

        if not self.currentRegister():
            row = 0
        else:
            row = self.currentRegister()

        if row < 0:
            return -1

        if row >= self.d._model.rows:
            return -2
        # logger.debug("%s.Row %s ----> %s" % (self.curName(), row, self))
        return row

    def isValid(self) -> bool:
        """
        Specify whether the position to which the cursor points is valid.

        @return True if ok else False.
        """

        if self.at() >= 0:
            return True
        else:
            return False

    @pyqtSlot()
    @pyqtSlot(str)
    def refresh(self, fN: Optional[str] = None) -> None:
        """
        Refresh the cursor content.

        If no related cursor has been indicated, get the complete cursor, according to the query
        default. If it has been indicated that it depends on another cursor with which it relates,
        The content of the cursor will depend on the value of the field that determines the relationship.
        If the name of a field is indicated, it is considered that the buffer has only changed in that
        field and thus avoid repetitions in the soda.

        @param fN Name of the buffer field that has changed
        """
        if not self.d.metadata_:
            return

        if self.d.cursorRelation_ is not None and self.d.relation_ is not None:
            self.clearPersistentFilter()
            if not self.d.cursorRelation_.metadata():
                return
            if self.d.cursorRelation_.metadata().primaryKey() == fN and self.d.cursorRelation_.modeAccess() == self.Insert:
                return

            if not fN or self.d.relation_.foreignField() == fN:
                if self.d.buffer_:
                    self.d.buffer_.clear_buffer()
                self.refreshDelayed()
                return
        else:
            self.d._model.refresh()  # Hay que hacer refresh previo pq si no no recoge valores de un commitBuffer paralelo
            # self.select()
            pos = self.atFrom()
            if pos > self.size():
                pos = self.size() - 1

            if not self.seek(pos, False, True):

                if self.d.buffer_:
                    self.d.buffer_.clear_buffer()
                self.newBuffer.emit()

    @pyqtSlot()
    def refreshDelayed(self, msec: int = 20) -> None:
        """
        Update the recordset with a delay.

        Accept a lapse of time in milliseconds, activating the internal timer for
        to perform the final refresh upon completion of said lapse.

        @param msec Amount of lapsus time, in milliseconds.
        """
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

            if self.d.cursorRelation_ and self.d.relation_ and self.d.cursorRelation_.metadata():
                v = self.valueBuffer(self.d.relation_.field())
                foreignFieldValueBuffer = self.d.cursorRelation_.valueBuffer(self.d.relation_.foreignField())

                if foreignFieldValueBuffer != v and foreignFieldValueBuffer is not None:
                    self.d.cursorRelation_.setValueBuffer(self.d.relation_.foreignField(), v)

    def primeInsert(self) -> None:
        """
        Refill the buffer for the first time.
        """

        if not self.d.buffer_:
            self.d.buffer_ = PNBuffer(self)

        self.d.buffer_.primeInsert()

    def primeUpdate(self) -> PNBuffer:
        """
        Update the buffer.

        @return buffer refresh.
        """

        if self.d.buffer_ is None:
            self.d.buffer_ = PNBuffer(self)
        # logger.warning("Realizando primeUpdate en pos %s y estado %s , filtro %s", self.at(), self.modeAccess(), self.filter())
        self.d.buffer_.primeUpdate(self.at())
        return self.d.buffer_

    @pyqtSlot()
    def refreshBuffer(self) -> bool:
        """
        Refresh the buffer according to the established access mode.

        Bring cursor information to the buffer to edit or navigate, or prepare the buffer to
        insert or delete

        If there is a counter field, the "calculateCounter" function of the script of the
        context (see FLSqlCursor :: ctxt_) set for the cursor. This function is passed
        as an argument the name of the counter field and must return the value it must contain
        that field

        @return TRUE if the refreshment could be performed, FALSE otherwise
        """
        from pineboolib import qsa as qsa_tree

        if not self.d.metadata_:
            raise Exception("Not initialized")
        if not self._action:
            raise Exception("Not initialized")

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

            fieldList = self.d.metadata_.fieldList()
            if fieldList:
                for field in fieldList:
                    field_name = field.name()

                    if self.d.buffer_ is None:
                        raise Exception("buffer is empty!")

                    self.d.buffer_.setNull(field_name)
                    if not self.d.buffer_.isGenerated(field_name):
                        continue
                    type_ = field.type()
                    # fltype = FLFieldself.d.metadata_.flDecodeType(type_)
                    # fltype = self.d.metadata_.field(fiName).flDecodeType(type_)
                    defVal = field.defaultValue()
                    if defVal is not None:
                        # defVal.cast(fltype)
                        self.d.buffer_.setValue(field_name, defVal)

                    if type_ == "serial":
                        val = self.db().nextSerialVal(self.d.metadata_.name(), field_name)
                        if val is None:
                            val = 0
                        self.d.buffer_.setValue(field_name, val)

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
                            self.d.buffer_.setValue(field_name, siguiente)

            if self.d.cursorRelation_ is not None and self.d.relation_ is not None and self.d.cursorRelation_.metadata():
                self.setValueBuffer(self.d.relation_.field(), self.d.cursorRelation_.valueBuffer(self.d.relation_.foreignField()))

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

            self.primeUpdate()
            self.setNotGenerateds()
            self.updateBufferCopy()

        elif self.d.modeAccess_ == self.Browse:

            self.primeUpdate()
            self.setNotGenerateds()
            self.newBuffer.emit()

        else:
            logger.error("refreshBuffer(). No hay definido modeAccess()")

        # if project.DGI.use_model() and self.meta_model():
        #    self.populate_meta_model()

        return True

    @pyqtSlot()
    def setEditMode(self) -> bool:
        """
        Change the cursor to Edit mode.

        @return True if the cursor is in Edit mode or was in Insert mode and has successfully switched to Edit mode
        """
        if self.d.modeAccess_ == self.Insert:
            if not self.commitBuffer():
                return False
            self.refresh()
            self.setModeAccess(self.Edit)
        elif self.d.modeAccess_ == self.Edit:
            return True

        return False

    @pyqtSlot()
    def seek(self, i, relative: Optional[bool] = False, emite: bool = False) -> bool:
        """
        Simply refreshes the buffer with the FLSqlCursor :: refreshBuffer () method.

        @param i. Not used.
        @param relative. Not used.
        @param emite If TRUE emits the FLSqlCursor :: currentChanged () signal.

        @return True if ok or False.
        """
        ret_ = False

        if self.buffer():
            if emite:
                self.currentChanged.emit(self.at())

            ret_ = self.refreshBuffer()

        return ret_

    @pyqtSlot()
    @pyqtSlot(bool)
    def next(self, emite: bool = True) -> bool:
        """
        Move the position to which the +1 position and execute refreshBuffer.

        @param emits If TRUE emits the FLSqlCursor :: currentChanged () signal
        """
        # if self.d.modeAccess_ == self.Del:
        #    return False

        b = self.moveby(1)
        if b:
            if emite:
                self.d._current_changed.emit(self.at())

            return self.refreshBuffer()

        return b

    def moveby(self, pos: int) -> bool:
        """
        Move the cursor to the specified position.

        @param i. index position to seek.
        @return True if ok else False.
        """

        if self.currentRegister():
            pos += self.currentRegister()

        return self.move(pos)

    @pyqtSlot()
    @pyqtSlot(bool)
    def prev(self, emite: bool = True) -> bool:
        """
        Move the position to which the -1 position and execute refreshBuffer.

        @param emits If TRUE emits the FLSqlCursor :: currentChanged () signal
        """
        # if self.d.modeAccess_ == self.Del:
        #    return False

        b = self.moveby(-1)

        if b:
            if emite:
                self.d._current_changed.emit(self.at())

            return self.refreshBuffer()

        return b

    def move(self, row: int = -1) -> bool:
        """
        Move the cursor across the table.

        @return True if ok else False.
        """
        # if row is None:
        #     row = -1

        if not self.d._model:
            return False

        if row < 0:
            row = -1
        if row >= self.d._model.rows:
            row = self.d._model.rows
        if self.currentRegister() == row:
            return False
        topLeft = self.d._model.index(row, 0)
        bottomRight = self.d._model.index(row, self.d._model.cols - 1)
        new_selection = QtCore.QItemSelection(topLeft, bottomRight)
        if self._selection is None:
            raise Exception("Call setAction first.")
        self._selection.select(new_selection, QtCore.QItemSelectionModel.ClearAndSelect)
        self.d._currentregister = row
        # self.d._current_changed.emit(self.at())
        if row < self.d._model.rows and row >= 0:
            return True
        else:
            return False

    @pyqtSlot()
    @pyqtSlot(bool)
    def first(self, emite: bool = True) -> bool:
        """
        Move the position to which the first position and execute refreshBuffer.

        @param emits If TRUE emits the FLSqlCursor :: currentChanged () signal
        """
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

    @pyqtSlot()
    @pyqtSlot(bool)
    def last(self, emite: bool = True) -> bool:
        """
        Move the position to which the last position and execute refreshBuffer.

        @param emits If TRUE emits the FLSqlCursor :: currentChanged () signal
        """
        # if self.d.modeAccess_ == self.Del:
        #    return False

        b = self.move(self.d._model.rows - 1)

        if b:
            if emite:
                self.d._current_changed.emit(self.at())

            return self.refreshBuffer()

        return b

    @pyqtSlot()
    def __del__(self, invalidate: bool = True) -> None:
        """
        Check if it is deleted in cascade, if so, also delete related records in 1M cardinality.

        @param invalidate. Not used.
        """
        # logger.trace("FLSqlCursor(%s). Eliminando cursor" % self.curName(), self)
        # delMtd = None
        # if self.d.metadata_:
        #     if not self.d.metadata_.inCache():
        #         delMtd = True

        msg = None
        mtd = self.d.metadata_

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
        # self.destroyed.emit()
        # self.d.countRefCursor = self.d.countRefCursor - 1     FIXME

    @pyqtSlot()
    def select(self, _filter: Optional[str] = None, sort: Optional[str] = None) -> bool:  # sort = QtCore.QSqlIndex()
        """
        Execute the filter specified in the cursor and refresh the information of the affected records.

        @param _filter. Optional filter.
        @param sort. Optional sort order.

        @return True if ok or False.
        """
        # _filter = _filter if _filter is not None else self.filter()
        if not self.d.metadata_:
            return False

        finalFilter = _filter or ""
        # bFilter = self.baseFilter()
        # finalFilter = bFilter
        # if _filter:
        #    if bFilter:
        #        if _filter not in bFilter:
        #            finalFilter = "%s AND %s" % (bFilter, _filter)
        #        else:
        #            finalFilter = bFilter
        #
        #    else:
        #        finalFilter = _filter

        if self.d.cursorRelation_ and self.d.cursorRelation_.modeAccess() == self.Insert and not self.curFilter():
            finalFilter = "1 = 0"

        self.setFilter(finalFilter)

        if sort:
            self.d._model.setSortOrder(sort)

        self.d._model.refresh()

        self.d._currentregister = -1

        if self.d.cursorRelation_ and self.modeAccess() == self.Browse:
            self.d._currentregister = self.atFrom()

        self.refreshBuffer()
        # if self.modeAccess() == self.Browse:
        #    self.d._currentregister = -1
        self.newBuffer.emit()

        return True

    @pyqtSlot()
    def setSort(self, sortO: str) -> None:
        """
        Specify the sort order in the tablemodel.

        @param str. new sort order.
        """
        if not sortO:
            return

        self.d._model.setSortOrder(sortO)

    @pyqtSlot()
    def baseFilter(self) -> str:
        """
        Return the base filter.

        @return base filter.
        """

        relationFilter = None
        finalFilter = ""

        if self.d.cursorRelation_ and self.d.relation_ and self.d.metadata_ and self.d.cursorRelation_.metadata():
            fgValue = self.d.cursorRelation_.valueBuffer(self.d.relation_.foreignField())
            field = self.d.metadata_.field(self.d.relation_.field())

            if field is not None and fgValue is not None:

                relationFilter = self.db().manager().formatAssignValue(field, fgValue, True)
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
                if relationFilter not in finalFilter:
                    finalFilter = "%s AND %s" % (finalFilter, relationFilter)

        # if self.filter():
        #    if finalFilter and self.filter() not in finalFilter:
        #        finalFilter = "%s AND %s" % (finalFilter, self.filter())
        #    else:
        #        finalFilter = self.filter()

        return finalFilter

    @pyqtSlot()
    def curFilter(self) -> str:
        """
        Return the actual filter.

        @return actual filter.
        """

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

    @pyqtSlot()
    def setFilter(self, _filter: str) -> None:
        """
        Specify the cursor filter.

        @param _filter. Text string with the filter to apply.
        """

        _filter_none: Optional[str] = _filter
        if _filter_none is None:
            logger.warning("setFilter: None is not allowed, use empty string", stack_info=True)
            _filter = ""
        # self.d.filter_ = None

        finalFilter = _filter

        bFilter = self.baseFilter()
        if bFilter not in [None, ""]:
            if finalFilter in [None, ""]:
                finalFilter = bFilter
            elif finalFilter in bFilter:
                finalFilter = bFilter
            elif bFilter not in finalFilter:
                finalFilter = bFilter + " AND " + finalFilter

        if finalFilter and self.d.persistentFilter_ and self.d.persistentFilter_ not in finalFilter:
            finalFilter = finalFilter + " OR " + self.d.persistentFilter_

        self.d._model.where_filters["filter"] = finalFilter

    @pyqtSlot()
    def insertRecord(self, wait: bool = True) -> None:
        """
        Open the form record in insert mode.

        @param wait. wait to form record close.
        """

        logger.trace("insertRecord %s", self._action and self._action.name())
        self.openFormInMode(self.Insert, wait)

    @pyqtSlot()
    def editRecord(self, wait: bool = True) -> None:
        """
        Open the form record in edit mode.

        @param wait. wait to form record close.
        """

        logger.trace("editRecord %s", self.actionName())
        if self.d.needUpdate():
            if not self.d.metadata_:
                raise Exception("self.d.metadata_ is not defined!")

            pKN = self.d.metadata_.primaryKey()
            pKValue = self.valueBuffer(pKN)
            self.refresh()
            pos = self.atFromBinarySearch(pKN, pKValue)
            if not pos == self.at():
                self.seek(pos, False, False)

        self.openFormInMode(self.Edit, wait)

    @pyqtSlot()
    def browseRecord(self, wait: bool = True) -> None:
        """
        Open the form record in browse mode.

        @param wait. wait to form record close.
        """

        logger.trace("browseRecord %s", self.actionName())
        if self.d.needUpdate():
            if not self.d.metadata_:
                raise Exception("self.d.metadata_ is not defined!")
            pKN = self.d.metadata_.primaryKey()
            pKValue = self.valueBuffer(pKN)
            self.refresh()
            pos = self.atFromBinarySearch(pKN, pKValue)
            if not pos == self.at():
                self.seek(pos, False, False)
        self.openFormInMode(self.Browse, wait)

    @pyqtSlot()
    def deleteRecord(self, wait: bool = True) -> None:
        """
        Open the form record in insert mode.Ask for confirmation to delete the record.

        @param wait. wait to record delete to continue.
        """

        logger.trace("deleteRecord %s", self.actionName())
        self.openFormInMode(self.Del, wait)
        # self.d._action.openDefaultFormRecord(self)

    def copyRecord(self) -> None:
        """
        Perform the action of inserting a new record, and copy the value of the record fields current.
        """

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

    @pyqtSlot()
    def chooseRecord(self) -> None:
        """
        Perform the action associated with choosing a cursor record.

        By default the form of record edition, calling the PNSqlCursor :: editRecord () method, if the PNSqlCursor :: edition flag
        indicates TRUE, if it indicates FALSE this method does nothing
        """

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

    def setForwardOnly(self, b: bool) -> None:
        """
        Avoid refreshing the associated model.
        """

        if not self.d._model:
            return

        self.d._model.disable_refresh(b)

    @pyqtSlot()
    def commitBuffer(self, emite: bool = True, checkLocks: bool = False) -> bool:
        """
        Send the contents of the buffer to the cursor, or perform the appropriate action for the cursor.

        All changes made to the buffer become effective at the cursor when invoking this method.
        The way to make these changes is determined by the access mode established for
        the cursor, see FLSqlCursor :: Mode, if the mode is edit or insert update with the new values ​​of
        the fields of the record, if the mode is delete deletes the record, and if the mode is navigation it does nothing.
        First of all it also checks referential integrity by invoking the FLSqlCursor :: checkIntegrity () method.

        If a calculated field exists, the "calculateField" function of the script of the
        context (see FLSqlCursor :: ctxt_) set for the cursor. This function is passed
        as an argument the name of the calculated field and must return the value it must contain
        that field, e.g. if the field is the total of an invoice and of type calculated the function
        "calculateField" must return the sum of lines of invoices plus / minus taxes and
        discounts

        @param issues True to emit cursorUpdated signal
        @param checkLocks True to check block risks for this table and the current record
        @return TRUE if the buffer could be delivered to the cursor, and FALSE if the delivery failed
        """

        if not self.d.buffer_ or not self.d.metadata_:
            return False

        if not self.activatedBufferCommited():
            return True

        from pineboolib import pncontrolsfactory

        if self.db().interactiveGUI() and self.db().canDetectLocks() and (checkLocks or self.d.metadata_.detectLocks()):
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

        if self.modeAccess() in [self.Edit, self.Insert]:
            fieldList = self.d.metadata_.fieldList()

            for field in fieldList:
                if field.isCheck():
                    fieldNameCheck = field.name()
                    self.d.buffer_.setGenerated(field, False)

                    if self.d.bufferCopy_:
                        self.d.bufferCopy_.setGenerated(field, False)
                    continue

                if not self.d.buffer_.isGenerated(field.name()):
                    continue

                if self.context() and hasattr(self.context(), "calculateField") and field.calculated():
                    v = project.call("calculateField", [field.name()], self.context(), False)

                    if v not in (True, False, None):
                        self.setValueBuffer(field.name(), v)

        functionBefore = None
        functionAfter = None
        model_module: Any = None

        idMod = self.db().managerModules().idModuleOfFile("%s.mtd" % self.d.metadata_.name())

        module_script: "FLFormDB" = project.actions[idMod].load() if idMod in project.actions.keys() else project.actions["sys"].load()

        if project.DGI.use_model():
            model_name = "models.%s.%s_def" % (idMod, idMod)
            try:
                model_module = importlib.import_module(model_name)
            except Exception:
                logger.exception("Error trying to import module %s", model_name)

        if not self.modeAccess() == PNSqlCursor.Browse and self.activatedCommitActions():

            functionBefore = "beforeCommit_%s" % (self.d.metadata_.name())
            functionAfter = "afterCommit_%s" % (self.d.metadata_.name())

            if model_module is not None:
                function_model_before = getattr(model_module.iface, "beforeCommit_%s" % self.d.metadata_.name(), None)
                if function_model_before:
                    ret = function_model_before(self)
                    if not ret:
                        return ret

            if functionBefore:
                fn = getattr(module_script.iface, functionBefore, None)
                v = None
                if fn is not None:
                    try:
                        v = fn(self)
                    except Exception:
                        pncontrolsfactory.aqApp.msgBoxWarning(error_manager(traceback.format_exc(limit=-6, chain=False)), project._DGI)
                    if v and not isinstance(v, bool) or v is False:
                        return False

        pKN = self.d.metadata_.primaryKey()
        updated = False
        savePoint = None

        if self.modeAccess() == self.Insert:
            if self.d.cursorRelation_ and self.d.relation_:
                if self.d.cursorRelation_.metadata() and self.d.cursorRelation_.valueBuffer(self.d.relation_.foreignField()):
                    self.setValueBuffer(self.d.relation_.field(), self.d.cursorRelation_.valueBuffer(self.d.relation_.foreignField()))
                    self.d.cursorRelation_.setAskForCancelChanges(True)

            pk_name = self.d.buffer_.pK()
            if pk_name is None:
                raise ValueError("primery key is not defined!")
            pk_value = self.d.buffer_.value(pk_name)

            self.d._model.Insert(self)
            self.d._model.refresh()
            pk_row = self.d._model.findPKRow((pk_value,))
            if pk_row is None:
                raise Exception("pk_row not found after insert!")
            self.move(pk_row)

            updated = True

        elif self.modeAccess() == self.Edit:
            db = self.db()
            if db is None:
                raise Exception("db is not defined!")

            if not db.canSavePoint():
                if db.currentSavePoint_:
                    db.currentSavePoint_.saveEdit(pKN, self.bufferCopy(), self)

            if functionAfter and self.d.activatedCommitActions_:
                if not savePoint:
                    from . import pnsqlsavepoint

                    savePoint = pnsqlsavepoint.PNSqlSavePoint(None)
                savePoint.saveEdit(pKN, self.bufferCopy(), self)

            if self.d.cursorRelation_ and self.d.relation_:
                if self.d.cursorRelation_.metadata():
                    self.d.cursorRelation_.setAskForCancelChanges(True)
            logger.trace("commitBuffer -- Edit . 20 . ")
            if self.isModifiedBuffer():

                logger.trace("commitBuffer -- Edit . 22 . ")
                self.update(False)

                logger.trace("commitBuffer -- Edit . 25 . ")

                updated = True
                self.setNotGenerateds()
            logger.trace("commitBuffer -- Edit . 30 . ")

        elif self.modeAccess() == self.Del:

            if self.d.cursorRelation_ and self.d.relation_:
                if self.d.cursorRelation_.metadata():
                    self.d.cursorRelation_.setAskForCancelChanges(True)

            recordDelBefore = "recordDelBefore%s" % self.d.metadata_.name()
            v = project.call(recordDelBefore, [self], self.context(), False)
            if v and not isinstance(v, bool):
                return False

            if not self.d.buffer_:
                self.primeUpdate()

            fieldList = self.d.metadata_.fieldList()

            for field in fieldList:

                fiName = field.name()
                if not self.d.buffer_.isGenerated(fiName):
                    continue

                s = None
                if not self.d.buffer_.isNull(fiName):
                    s = self.d.buffer_.value(fiName)

                if s is None:
                    continue

                relationList = field.relationList()
                if not relationList:
                    continue
                else:
                    for r in relationList:
                        c = PNSqlCursor(r.foreignTable())
                        if not c.d.metadata_:
                            continue
                        f = c.d.metadata_.field(r.foreignField())
                        if f is None:
                            continue

                        relation_m1 = f.relationM1()

                        if relation_m1 and relation_m1.deleteCascade():
                            c.setForwardOnly(True)
                            c.select(self.conn().manager().formatAssignValue(r.foreignField(), f, s, True))
                            while c.next():
                                c.setModeAccess(self.Del)
                                c.refreshBuffer()
                                if not c.commitBuffer(False):
                                    return False

            self.d._model.Delete(self)

            recordDelAfter = "recordDelAfter%s" % self.d.metadata_.name()
            v = project.call(recordDelAfter, [self], self.context(), False)

            updated = True

        if updated and self.lastError():
            return False

        if not self.modeAccess() == self.Browse and self.activatedCommitActions():

            if model_module is not None:
                function_model_after = getattr(model_module.iface, "afterCommit_%s" % self.d.metadata_.name(), None)
                if function_model_after:
                    ret = function_model_after(self)
                    if not ret:
                        return ret

            if functionAfter:
                fn = getattr(module_script.iface, functionAfter, None)
                if fn is not None:
                    v = None
                    try:
                        v = fn(self)
                    except Exception:
                        pncontrolsfactory.aqApp.msgBoxWarning(error_manager(traceback.format_exc(limit=-6, chain=False)), project._DGI)
                    if v and not isinstance(v, bool) or v is False:
                        return False

        if self.modeAccess() in (self.Del, self.Edit):
            self.setModeAccess(self.Browse)

        if self.modeAccess() == self.Insert:
            self.setModeAccess(self.Edit)

        if updated:
            if fieldNameCheck:
                self.d.buffer_.setGenerated(fieldNameCheck, True)

                if self.d.bufferCopy_:
                    self.d.bufferCopy_.setGenerated(fieldNameCheck, True)

            self.setFilter("")
            # self.clearMapCalcFields()

            if emite:
                self.cursorUpdated.emit()

        if model_module is not None:
            function_model_buffer_commited = getattr(model_module.iface, "bufferCommited_%s" % self.d.metadata_.name(), None)
            if function_model_buffer_commited:
                ret = function_model_buffer_commited(self)
                if not ret:
                    return ret

        self.bufferCommited.emit()
        return True

    @pyqtSlot()
    def commitBufferCursorRelation(self) -> bool:
        """
        Send the contents of the cursor buffer related to that cursor.

        It makes all changes in the related cursor buffer effective by placing itself in the registry corresponding receiving changes.
        """

        ok = True
        activeWidEnabled = False
        activeWid = None

        if self.d.cursorRelation_ is None or self.relation() is None:
            return ok

        if project.DGI.localDesktop():
            from pineboolib import pncontrolsfactory

            activeWid = pncontrolsfactory.QApplication.activeModalWidget()
            if not activeWid:
                activeWid = pncontrolsfactory.QApplication.activePopupWidget()
            if not activeWid:
                activeWid = pncontrolsfactory.QApplication.activeWindow()

            if activeWid:
                activeWidEnabled = activeWid.isEnabled()

        if self.d.modeAccess_ == self.Insert:
            if self.d.cursorRelation_.metadata() and self.d.cursorRelation_.modeAccess() == self.Insert:

                if activeWid and activeWidEnabled:
                    activeWid.setEnabled(False)

                if not self.d.cursorRelation_.commitBuffer():
                    self.d.modeAccess_ = self.Browse
                    ok = False
                else:
                    self.setFilter("")
                    self.d.cursorRelation_.refresh()
                    self.d.cursorRelation_.setModeAccess(self.Edit)
                    self.d.cursorRelation_.refreshBuffer()

                if activeWid and activeWidEnabled:
                    activeWid.setEnabled(True)

        elif self.d.modeAccess_ in [self.Browse, self.Edit]:
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

    @pyqtSlot()
    def transactionLevel(self) -> int:
        """
        Transaction level.

        @return The current level of transaction nesting, 0 there is no transaction.
        """

        if self.db():
            return self.db().transactionLevel()
        else:
            return 0

    @pyqtSlot()
    def transactionsOpened(self) -> List[str]:
        """
        Transactions opened by this cursor.

        @return The list with the levels of transactions that this cursor has initiated and remain open
        """
        lista = []
        for it in self.d.transactionsOpened_:
            lista.append(str(it))

        return lista

    @pyqtSlot()
    @decorators.BetaImplementation
    def rollbackOpened(self, count: int = -1, msg: str = None) -> None:
        """
        Undo transactions opened by this cursor.

        @param count Number of transactions to be undone, -1 all.
        @param msg Text string that is displayed in a dialog box before undoing transactions. If it is empty it shows nothing.
        """

        ct: int = len(self.d.transactionsOpened_) if count < 0 else count

        if ct > 0 and msg:
            t: str = self.d.metadata_.name() if self.d.metadata_ else self.curName()
            m = "%sSqLCursor::rollbackOpened: %s %s" % (msg, count, t)
            self.d.msgBoxWarning(m, False)
        elif ct > 0:
            logger.trace("rollbackOpened: %s %s", count, self.curName())

        i = 0
        while i < ct:
            logger.trace("Deshaciendo transacción abierta", self.transactionLevel())
            self.rollback()
            i = i + 1

    @pyqtSlot()
    def commitOpened(self, count: int = -1, msg: str = None) -> None:
        """
        Complete transactions opened by this cursor.

        @param count Number of transactions to finish, -1 all.
        @param msg A text string that is displayed in a dialog box before completing transactions. If it is empty it shows nothing.
        """

        ct: int = len(self.d.transactionsOpened_) if count < 0 else count
        t: str = self.d.metadata_.name() if self.d.metadata_ else self.curName()

        if ct and msg:
            m = "%sSqlCursor::commitOpened: %s %s" % (msg, str(count), t)
            self.d.msgBoxWarning(m, False)
            logger.warning(m)
        elif ct > 0:
            logger.warning("SqlCursor::commitOpened: %d %s" % (count, self.curName()))

        i = 0
        while i < ct:
            logger.warning("Terminando transacción abierta %s", self.transactionLevel())
            self.commit()
            i = i + 1

    @pyqtSlot()
    @decorators.NotImplementedWarn
    def checkRisksLocks(self, terminate: bool = False) -> bool:
        """
        Enter a lockout risk loop for this table and the current record.

        The loop continues as long as there are locks, until this method is called again with 'terminate'
        activated or when the user cancels the operation.

        @param terminate True will end the check loop if it is active
        """

        return True

    @pyqtSlot()
    def setAcTable(self, ac):
        """
        Set the global access for the table, see FLSqlCursor :: setAcosCondition ().

        This will be the permission to apply to all default fields.

        @param ac Global permission; eg: "r-", "-w"
        """

        self.d.idAc_ = self.d.idAc_ + 1
        self.d.id_ = "%s%s%s" % (self.d.idAc_, self.d.idAcos_, self.d.idCond_)
        self.d.acPermTable_ = ac

    @pyqtSlot()
    def setAcosTable(self, acos):
        """
        Set the access control list (ACOs) for the fields in the table, see FLSqlCursor :: setAcosCondition ().

        This list of texts should have in their order components the names of the fields,
        and in the odd order components the permission to apply to that field,
        eg: "name", "r-", "description", "-", "telephone", "rw", ...

        The permissions defined here overwrite the global.

        @param acos List of text strings with the names of fields and permissions.
        """

        self.d.idAcos_ = self.d.idAcos_ + 1
        self.d.id_ = "%s%s%s" % (self.d.idAc_, self.d.idAcos_, self.d.idCond_)
        self.d.acosTable_ = acos

    @pyqtSlot()
    def setAcosCondition(self, condName, cond, condVal):
        """
        Set the condition that must be met to apply access control.

        For each record this condition is evaluated and if it is met, the rule applies
        of access control set with FLSqlCursor :: setAcTable and FLSqlCursor :: setAcosTable.

        setAcosCondition ("name", VALUE, "pepe"); // valueBuffer ("name") == "pepe"
        setAcosCondition ("name", REGEXP, "pe *"); // QRegExp ("pe *") .exactMatch (valueBuffer ("name") .toString ())
        setAcosCondition ("sys.checkAcos", FUNCTION, true); // call ("sys.checkAcos") == true



        @param cond Type of evaluation;
                    VALUE compares with a fixed value
                    REGEXP compares with a regular expression
                    FUNCTION compares with the value returned by a script function

        @param condName If it is empty, the condition is not evaluated and the rule is never applied.
                    For VALUE and REGEXP name of a field.
                    For FUNCTION name of a script function. The function is passed as
                    argument the cursor object.

        @param condVal Value that makes the condition true
        """

        self.d.idCond_ = self.d.idCond_ + 1
        self.d.id_ = "%s%s%s" % (self.d.idAc_, self.d.idAcos_, self.d.idCond_)
        self.d.acosCondName_ = condName
        self.d.acosCond_ = cond
        self.d.acosCondVal_ = condVal

    @pyqtSlot()
    @decorators.NotImplementedWarn
    def concurrencyFields(self) -> List[str]:
        """
        Check if there is a collision of fields edited by two sessions simultaneously.

        @return List with the names of the colliding fields
        """

        return []

    @pyqtSlot()
    def changeConnection(self, connName: str) -> None:
        """
        Change the cursor to another database connection.

        @param connName. connection name.
        """

        curConnName = self.connectionName()
        if curConnName == connName:
            return

        newDB = project.conn.database(connName)
        if curConnName == newDB.connectionName():
            return

        if self.d.transactionsOpened_:
            mtd = self.d.metadata_
            t = None
            if mtd:
                t = mtd.name()
            else:
                t = self.curName()

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

    @decorators.NotImplementedWarn
    def populateCursor(self) -> None:
        """
        If the cursor comes from a query, perform the process of adding the deficit from the fields to it.
        """
        return

    def setNotGenerateds(self) -> None:
        """
        Mark as no generated.

        When the cursor comes from a query, it performs the process that marks as
        not generated (the fields of the buffer are not taken into account in INSERT, EDIT, DEL)
        that do not belong to the main table.
        """

        if self.d.metadata_ and self.d.isQuery_ and self.d.buffer_:
            for f in self.d.metadata_.fieldList():
                self.d.buffer_.setGenerated(f, False)

    @decorators.NotImplementedWarn
    def setExtraFieldAttributes(self):
        """Deprecated."""

        return True

    # def clearMapCalcFields(self):
    #    self.d.mapCalcFields_ = []

    @decorators.NotImplementedWarn
    def valueBufferRaw(self, fN: str) -> Any:
        """Deprecated."""

        return True

    def sort(self) -> str:
        """
        Choose the order of the main columns.

        @return sort order.
        """

        return self.d._model.getSortOrder()

    # @decorators.NotImplementedWarn
    # def list(self):
    #    return None

    def filter(self) -> str:
        """
        Return the cursor filter.

        @return current filter.
        """

        return self.d._model.where_filters["filter"] if "filter" in self.d._model.where_filters else ""

    def field(self, name: str) -> Optional["FieldStruct"]:
        """
        Return a specified FieldStruct of the buffer.
        """

        if not self.d.buffer_:
            raise Exception("self.d.buffer_ is not defined!")
        return self.d.buffer_.field(name)

    def update(self, notify: bool = True) -> None:
        """
        Update tableModel with the buffer.

        @param notify. emit bufferCommited signal after update if True else None.
        """

        logger.trace("PNSqlCursor.update --- BEGIN:")
        if self.modeAccess() == PNSqlCursor.Edit:

            if not self.d.buffer_:
                raise Exception("Buffer is not set. Cannot update")
            # solo los campos modified
            lista = self.d.buffer_.modifiedFields()
            self.d.buffer_.setNoModifiedFields()
            # TODO: pKVaue debe ser el valueBufferCopy, es decir, el antiguo. Para
            # .. soportar updates de PKey, que, aunque inapropiados deberían funcionar.
            pk_name = self.d.buffer_.pK()
            if pk_name is None:
                raise Exception("PrimaryKey is not defined!")

            pKValue = self.d.buffer_.value(pk_name)

            dict_update = {fieldName: self.d.buffer_.value(fieldName) for fieldName in lista}
            try:
                update_successful = self.d._model.updateValuesDB(pKValue, dict_update)
            except Exception:
                logger.exception("PNSqlCursor.update:: Unhandled error on model updateRowDB:: ")
                update_successful = False
            # TODO: En el futuro, si no se puede conseguir un update, hay que
            # "tirar atrás" todo.
            if update_successful:
                row = self.d._model.findPKRow([pKValue])
                if row is not None:
                    if self.d._model.value(row, self.d._model.pK()) != pKValue:
                        raise AssertionError(
                            "Los indices del CursorTableModel devolvieron un registro erroneo: %r != %r"
                            % (self.d._model.value(row, self.d._model.pK()), pKValue)
                        )
                    self.d._model.setValuesDict(row, dict_update)

                else:
                    # Método clásico
                    logger.warning("update :: WARN :: Los indices del CursorTableModel no funcionan o el PKey no existe.")
                    row = 0
                    while row < self.d._model.rowCount():
                        if self.d._model.value(row, self.d._model.pK()) == pKValue:
                            for fieldName in lista:
                                self.d._model.setValue(row, fieldName, self.d.buffer_.value(fieldName))

                            break

                        row = row + 1

            if notify:
                self.bufferCommited.emit()

        logger.trace("PNSqlCursor.update --- END")

    def lastError(self) -> str:
        """
        Return the last error reported by the database connection.

        @return last error reported.
        """

        return self.db().lastError()

    def __iter__(self) -> "PNSqlCursor":
        """
        Make the cursor iterable.
        """

        self._iter_current = None
        return self

    def __next__(self) -> str:
        """
        Make the cursor iterable.

        @return function name.
        """
        self._iter_current = 0 if self._iter_current is None else self._iter_current + 1

        list_ = [attr for attr in dir(self) if not attr[0] == "_"]
        if self._iter_current >= len(list_):
            raise StopIteration

        return list_[self._iter_current]

    def primaryKey(self) -> Optional[str]:
        """
        Return the primary cursor key.

        @return primary key field name.
        """

        if self.d.metadata_:
            return self.d.metadata_.primaryKey()
        else:
            return None

    def fieldType(self, field_name: str = None) -> Optional[int]:
        """
        Return the field type.

        @param field_name. Specify the field to return type.
        @return int identifier.
        """

        if field_name and self.d.metadata_:
            return self.d.metadata_.fieldType(field_name)
        else:
            return None

    def __getattr__(self, name: str) -> Any:
        """
        Return the attribute of the associated DGI.

        @param name. attribute name to search.
        @return atribute or None.
        """

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
    # clearPersistentFilter = QtCore.pyqtSignal()

    # destroyed = QtCore.pyqtSignal()

    @pyqtSlot()
    def clearPersistentFilter(self):
        """
        Clear persistent filters.
        """

        self.d.persistentFilter_ = None


class PNCursorPrivate(QtCore.QObject):
    """
    Buffer with a cursor record.

    According to the FLSqlCursor :: Mode access mode set for the cusor, this buffer will contain
    the active record of said cursor ready to insert, edit, delete or navigate.
    """

    buffer_: Optional[PNBuffer] = None

    """
    Copia del buffer.

    Aqui se guarda una copia del FLSqlCursor::buffer_ actual mediante el metodo FLSqlCursor::updateBufferCopy().
    """
    bufferCopy_: Optional[PNBuffer] = None

    """
    Metadatos de la tabla asociada al cursor.
    """
    metadata_: Optional["PNTableMetaData"]

    """
    Mantiene el modo de acceso actual del cursor, ver FLSqlCursor::Mode.
    """
    modeAccess_ = -1

    """
    Cursor relacionado con este.
    """
    cursorRelation_: Optional["PNSqlCursor"]

    """
    Relación que determina como se relaciona con el cursor relacionado.
    """
    relation_: Optional["PNRelationMetaData"]

    """
    Esta bandera cuando es TRUE indica que se abra el formulario de edición de regitros en
    modo edición, y cuando es FALSE se consulta la bandera FLSqlCursor::browse. Por defecto esta
    bandera está a TRUE
    """
    edition_: bool

    """
    Esta bandera cuando es TRUE y la bandera FLSqlCuror::edition es FALSE, indica que se
    abra el formulario de edición de registro en modo visualización, y cuando es FALSE no hace
    nada. Por defecto esta bandera está a TRUE
    """
    browse_: bool
    browse_states_: "AQBoolFlagStateList"

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
    action_: "FLAction"

    """
    Cuando esta propiedad es TRUE siempre se pregunta al usuario si quiere cancelar
    cambios al editar un registro del cursor.
    """
    askForCancelChanges_: bool

    """
    Indica si estan o no activos los chequeos de integridad referencial
    """
    activatedCheckIntegrity_: bool

    """
    Indica si estan o no activas las acciones a realiar antes y después del Commit
    """
    activatedCommitActions_: bool

    """
    Contexto de ejecución de scripts.

    El contexto de ejecución será un objeto formulario el cual tiene asociado un script.
    Ese objeto formulario corresponde a aquel cuyo origen de datos es este cursor.
    El contexto de ejecución es automáticamente establecido por las clases FLFormXXXX.
    """
    ctxt_: Any

    """
    Cronómetro interno
    """
    timer_: Optional[QtCore.QTimer]

    """
    Cuando el cursor proviene de una consulta indica si ya se han agregado al mismo
    la definición de los campos que lo componen
    """
    populated_: bool

    """
    Cuando el cursor proviene de una consulta contiene la sentencia sql
    """
    isQuery_: bool

    """
    Cuando el cursor proviene de una consulta contiene la clausula order by
    """
    queryOrderBy_: str

    """
    Base de datos sobre la que trabaja
    """
    db_: Optional["IConnection"]

    """
    Pila de los niveles de transacción que han sido iniciados por este cursor
    """
    transactionsOpened_: List[int]

    """
    Filtro persistente para incluir en el cursor los registros recientemente insertados aunque estos no
    cumplan los filtros principales. Esto es necesario para que dichos registros sean válidos dentro del
    cursor y así poder posicionarse sobre ellos durante los posibles refrescos que puedan producirse en
    el proceso de inserción. Este filtro se agrega a los filtros principales mediante el operador OR.
    """
    persistentFilter_: Optional[str]

    """
    Cursor propietario
    """
    cursor_: Optional["PNSqlCursor"]

    """
    Nombre del cursor
    """
    curName_: str

    """
    Orden actual
    """
    sort_: str
    """
    Auxiliares para la comprobacion de riesgos de bloqueos
    """
    inLoopRisksLocks_: bool
    inRisksLocks_: bool

    """
    Para el control de acceso dinámico en función del contenido de los registros
    """

    acTable_: Any
    acPermTable_ = None
    acPermBackupTable_ = None
    acosTable_ = None
    acosBackupTable_ = None
    acosCondName_: Optional[str] = None
    acosCond_ = None
    acosCondVal_ = None
    lastAt_ = None
    aclDone_ = False
    idAc_ = 0
    idAcos_ = 0
    idCond_ = 0
    id_ = "000"

    """ Uso interno """
    isSysTable_: bool
    rawValues_: bool

    md5Tuples_: str

    countRefCursor: int

    _model: "PNCursorTableModel"

    edition_states_: AQBoolFlagStateList
    _current_changed = QtCore.pyqtSignal(int)

    def __init__(self) -> None:
        """
        Initialize the private part of the cursor.
        """

        super().__init__()
        self.metadata_ = None
        self.countRefCursor = 0
        self._currentregister = -1
        self.acosCondName_ = None
        self.buffer_ = None
        self.edition_states_ = AQBoolFlagStateList()
        self.browse_states_ = AQBoolFlagStateList()
        self.activatedCheckIntegrity_ = True
        self.activatedCommitActions_ = True
        self.askForCancelChanges_ = True
        self.populated_ = False
        self.transactionsOpened_ = []
        self.idAc_ = 0
        self.idAcos_ = 0
        self.idCond_ = 0
        self.id_ = "000"
        self.aclDone_ = False
        self.edition_ = True
        self.browse_ = True
        self.cursor_ = None
        self.cursorRelation_ = None
        self.relation_ = None
        self.acTable_ = None
        self.timer_ = None
        self.ctxt_ = None
        self.rawValues_ = False
        self.persistentFilter_ = None

    def __del__(self) -> None:
        """
        Delete instance values.
        """

        if self.metadata_:
            self.undoAcl()

        if self.bufferCopy_:
            del self.bufferCopy_
            self.bufferCopy_ = None

        if self.relation_:
            del self.relation_
            self.relation_ = None

        if self.acTable_:
            del self.acTable_
            self.acTable_ = None

        if self.edition_states_:
            del self.edition_states_
            self.edition_states_ = AQBoolFlagStateList()
            # logger.trace("AQBoolFlagState count %s", self.count_)

        if self.browse_states_:
            del self.browse_states_
            self.browse_states_ = AQBoolFlagStateList()
            # logger.trace("AQBoolFlagState count %s", self.count_)
        if self.transactionsOpened_:
            del self.transactionsOpened_
            self.transactionsOpened_ = []

    def doAcl(self) -> None:
        """
        Create restrictions according to access control list.
        """

        if not self.acTable_:
            self.acTable_ = FLAccessControlFactory().create("table")
            self.acTable_.setFromObject(self.metadata_)
            self.acosBackupTable_ = self.acTable_.getAcos()
            self.acPermBackupTable_ = self.acTable_.perm()
            self.acTable_.clear()
        cursor = self.cursor_
        if cursor is None:
            raise Exception("Cursor not created yet")
        if self.modeAccess_ == PNSqlCursor.Insert or (not self.lastAt_ == -1 and self.lastAt_ == cursor.at()):
            return

        if self.acosCondName_ is not None:
            condTrue_ = False

            if self.acosCond_ == PNSqlCursor.Value:
                condTrue_ = cursor.valueBuffer(self.acosCondName_) == self.acosCondVal_
            elif self.acosCond_ == PNSqlCursor.RegExp:
                from PyQt5.Qt import QRegExp  # type: ignore

                # FIXME: What is happenning here? bool(str(Regexp)) ??
                condTrue_ = bool(str(QRegExp(str(self.acosCondVal_)).exactMatch(str(cursor.value(self.acosCondName_)))))
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

        elif cursor.isLocked() or (self.cursorRelation_ and self.cursorRelation_.isLocked()):

            if not self.acTable_.name() == self.id_:
                self.acTable_.clear()
                self.acTable_.setName(self.id_)
                self.acTable_.setPerm("r-")
                self.acTable_.processObject(self.metadata_)
                self.aclDone_ = True

            return

        self.undoAcl()

    def undoAcl(self) -> None:
        """
        Delete restrictions according to access control list.
        """

        if self.acTable_ and self.aclDone_:
            self.aclDone_ = False
            self.acTable_.clear()
            self.acTable_.setPerm(self.acPermBackupTable_)
            self.acTable_.setAcos(self.acosBackupTable_)
            self.acTable_.processObject(self.metadata_)

    def needUpdate(self) -> bool:
        """
        Indicate if the cursor needs to be updated.

        @return True or False.
        """

        if self.isQuery_:
            return False

        need = self._model.need_update
        return need

    def msgBoxWarning(self, msg: str, throwException: bool = False) -> None:
        """
        Error message associated with the DGI.

        @param msg.Error message.
        @param throwException. No used.
        """
        logger.warning(msg)
        if project._DGI and project.DGI.localDesktop():
            if not throwException:
                from pineboolib import pncontrolsfactory

                pncontrolsfactory.QMessageBox.warning(pncontrolsfactory.QApplication.activeWindow(), "Pineboo", msg)
