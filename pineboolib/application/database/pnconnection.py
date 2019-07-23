# -*- coding: utf-8 -*-
"""Defines the PNConnection class.

"""
from PyQt5 import QtCore, QtWidgets  # type: ignore

from pineboolib.core.utils import logging
from pineboolib.core.settings import config
from pineboolib.core import decorators
from pineboolib.interfaces.iconnection import IConnection
from pineboolib.interfaces.cursoraccessmode import CursorAccessMode

from .pnsqlsavepoint import PNSqlSavePoint
from . import db_signals
from typing import Dict, List, Optional, Any, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from pineboolib.interfaces.iapicursor import IApiCursor
    from pineboolib.fllegacy import flmanager
    from pineboolib.fllegacy import flmanagermodules
    from .pnsqldrivers import PNSqlDrivers

logger = logging.getLogger(__name__)


class PNConnection(QtCore.QObject, IConnection):
    """Wrapper for database cursors which are used to emulate FLSqlCursor."""

    db_name: str
    db_host: str
    db_port: int
    db_userName: str
    db_password: str
    conn: Any = None  # Connection from the actual driver
    driverSql: "PNSqlDrivers"
    transaction_: int
    _managerModules = None
    _manager = None
    driverName_: str
    currentSavePoint_: Optional[PNSqlSavePoint]
    stackSavePoints_: List[PNSqlSavePoint]
    queueSavePoints_: List[PNSqlSavePoint]
    interactiveGUI_: bool
    _dbAux = None
    _isOpen: bool
    driver_ = None

    def __init__(self, db_name, db_host, db_port, db_userName, db_password, driverAlias, name=None) -> None:
        from .pnsqldrivers import PNSqlDrivers

        super(PNConnection, self).__init__()
        self.currentSavePoint_ = None
        self.driverSql = PNSqlDrivers()
        self.connAux: Dict[str, "IConnection"] = {}
        if name is None:
            self.name = "default"
        else:
            self.name = name

        self.driverName_ = self.driverSql.aliasToName(driverAlias)

        if name and name not in ("dbAux", "Aux"):
            self._isOpen = False
            return

        if self.driverName_ and self.driverSql.loadDriver(self.driverName_):
            self.driver_ = self.driverSql.driver()
            self.conn = self.conectar(db_name, db_host, db_port, db_userName, db_password)
            if self.conn is False:
                return

            self._isOpen = True

        else:
            logger.error("PNConnection.ERROR: No se encontro el driver '%s'", driverAlias)
            import sys

            sys.exit(0)

        self.transaction_ = 0
        self.stackSavePoints_ = []
        self.queueSavePoints_ = []
        self.interactiveGUI_ = True

        self.driver().db_ = self

    @decorators.NotImplementedWarn
    def finish(self):
        pass

    def connectionName(self) -> Any:
        """Get the current connection name for this cursor."""
        return self.name

    def useConn(self, name_or_conn: Union[str, IConnection] = "default") -> IConnection:
        """Select another connection which can be not the default one.

        Permite seleccionar una conexion que no es la default, Si no existe la crea
        """
        name: str
        if isinstance(name_or_conn, IConnection):
            name = str(name_or_conn.connectionName())
        else:
            name = str(name_or_conn)

        if name in ("default", None):
            return self

        connection = self.connAux.get(name, None)

        if connection is None:
            if self.driverSql is None:
                raise Exception("No driver selected")
            connection = PNConnection(
                self.db_name,
                self.db_host,
                self.db_port,
                self.db_userName,
                self.db_password,
                self.driverSql.nameToAlias(self.driverName()),
                name,
            )
            self.connAux[name] = connection
        return connection

    def dictDatabases(self) -> Dict[str, "IConnection"]:
        return self.connAux

    def removeConn(self, name="default") -> bool:
        try:
            conn_ = self.useConn(name).conn
            if conn_ is not None:
                conn_.close()

            del self.connAux[name]
        except Exception:
            pass

        return True

    def isOpen(self) -> bool:
        return self._isOpen

    def tables(self, t_: Optional[str] = None) -> List[str]:
        return self.driver().tables(t_)

    def database(self, name=None) -> "IConnection":
        if name is None:
            return self  # El tipo de retorno debe ser consistente
            # return self.DBName()  # Si no especificamos name, retorna str con el nombre de la BD

        return self.useConn(name)

    def DBName(self) -> str:
        try:
            return self.driver().DBName()
        except Exception as e:
            logger.error("DBName: %s", e)
            return self.db_name

    def driver(self):
        return self.driver_

    def session(self):
        return self.driver().session()

    def engine(self):
        return self.driver().engine()

    def declarative_base(self):
        return self.driver().declarative_base()

    def cursor(self) -> "IApiCursor":
        if self.conn is None:
            raise Exception("cursor. Empty conn!!")

        return self.conn.cursor()

    def conectar(self, db_name, db_host, db_port, db_userName, db_password) -> Any:

        self.db_name = db_name
        self.db_host = db_host
        self.db_port = db_port
        self.db_userName = db_userName
        self.db_password = db_password
        if self.name:
            self.driver().alias_ = self.driverName() + ":" + self.name

        return self.driver().connect(db_name, db_host, db_port, db_userName, db_password)

    def driverName(self) -> Any:
        return self.driver().driverName()

    def driverAlias(self) -> Any:
        return self.driver().alias_

    def driverNameToDriverAlias(self, name) -> Any:
        if self.driverSql is None:
            raise Exception("driverNameoDriverAlias. Sql driver manager is not defined")

        return self.driverSql.nameToAlias(name)

    def lastError(self) -> Any:
        return self.driver().lastError()

    def host(self) -> Any:
        return self.db_host

    def port(self) -> Any:
        return self.db_port

    def user(self) -> Any:
        return self.db_userName

    def password(self) -> Any:
        return self.db_password

    def seek(self, offs, whence=0) -> Any:
        if self.conn is None:
            raise Exception("seek. Empty conn!!")

        return self.conn.seek(offs, whence)

    def manager(self) -> "flmanager.FLManager":
        if not self._manager:
            # FIXME: Should not load from FL*
            from pineboolib.fllegacy.flmanager import FLManager

            self._manager = FLManager(self)

        return self._manager

    @decorators.NotImplementedWarn
    def md5TuplesStateTable(self, curname):
        return True

    @decorators.NotImplementedWarn
    def setInteractiveGUI(self, b):
        pass

    @decorators.NotImplementedWarn
    def setQsaExceptions(self, b):
        pass

    def db(self) -> "IConnection":
        return self

    def dbAux(self) -> "IConnection":
        return self.useConn("dbAux")

    def formatValue(self, t, v, upper) -> Any:
        return self.driver().formatValue(t, v, upper)

    def formatValueLike(self, t, v, upper) -> str:
        return self.driver().formatValueLike(t, v, upper)

    def canSavePoint(self) -> Any:
        return self.dbAux().driver().canSavePoint()

    def canTransaction(self) -> Any:
        return self.driver().canTransaction()

    def lastActiveCursor(self):
        return self.lastActiveCursor_

    def doTransaction(self, cursor) -> bool:
        if not cursor or not self.db():
            return False

        from pineboolib.application import project

        if self.transaction_ == 0 and self.canTransaction():
            if config.value("application/isDebuggerMode", False):
                project.message_manager().send("status_help_msg", "send", ["Iniciando Transacción... %s" % self.transaction_])
            if self.transaction():
                self.lastActiveCursor_ = cursor
                db_signals.emitTransactionBegin(cursor)

                if not self.canSavePoint():
                    if self.currentSavePoint_:
                        del self.currentSavePoint_
                        self.currentSavePoint_ = None

                    self.stackSavePoints_.clear()
                    self.queueSavePoints_.clear()

                self.transaction_ = self.transaction_ + 1
                cursor.d.transactionsOpened_.insert(0, self.transaction_)
                return True
            else:
                logger.warning("doTransaction: Fallo al intentar iniciar la transacción")
                return False

        else:
            if config.value("application/isDebuggerMode", False):
                project.message_manager().send(
                    "status_help_msg", "send", ["Creando punto de salvaguarda %s:%s" % (self.name, self.transaction_)]
                )
            if not self.canSavePoint():
                if self.transaction_ == 0:
                    if self.currentSavePoint_:
                        del self.currentSavePoint_
                        self.currentSavePoint_ = None

                    self.stackSavePoints_.clear()
                    self.queueSavePoints_.clear()

                if self.currentSavePoint_:
                    if self.stackSavePoints_:
                        self.stackSavePoints_.insert(0, self.currentSavePoint_)
                    else:
                        self.stackSavePoints_.append(self.currentSavePoint_)

                self.currentSavePoint_ = PNSqlSavePoint(self.transaction_)
            else:
                self.savePoint(self.transaction_)

            self.transaction_ = self.transaction_ + 1
            if cursor.d.transactionsOpened_:
                cursor.d.transactionsOpened_.insert(0, self.transaction_)  # push
            else:
                cursor.d.transactionsOpened_.append(self.transaction_)
            return True

    def transactionLevel(self) -> int:
        return self.transaction_

    def doRollback(self, cur) -> bool:
        if not cur or not self.conn:
            return False

        from pineboolib.application import project

        cancel = False
        if (
            self.interactiveGUI()
            and cur.d.modeAccess_ in (CursorAccessMode.Insert, CursorAccessMode.Edit)
            and cur.isModifiedBuffer()
            and cur.d.askForCancelChanges_
        ):

            if project.DGI.localDesktop():
                res = QtWidgets.QMessageBox.information(
                    QtWidgets.QApplication.activeWindow(),
                    "Cancelar Cambios",
                    "Todos los cambios se cancelarán.¿Está seguro?",
                    QtWidgets.QMessageBox.Yes,
                    QtWidgets.QMessageBox.No,
                )
                if res == QtWidgets.QMessageBox.No:
                    return False

            cancel = True

        if self.transaction_ > 0:
            if cur.d.transactionsOpened_:
                trans = cur.d.transactionsOpened_.pop()
                if not trans == self.transaction_:
                    logger.info(
                        "FLSqlDatabase: El cursor va a deshacer la transacción %s pero la última que inició es la %s",
                        self.transaction_,
                        trans,
                    )
            else:
                logger.info("FLSqlDatabaser : El cursor va a deshacer la transacción %s pero no ha iniciado ninguna", self.transaction_)

            self.transaction_ = self.transaction_ - 1
        else:
            return True

        if self.transaction_ == 0 and self.canTransaction():
            if config.value("application/isDebuggerMode", False):
                project.message_manager().send("status_help_msg", "send", ["Deshaciendo Transacción... %s" % self.transaction_])
            if self.rollbackTransaction():
                self.lastActiveCursor_ = None

                if not self.canSavePoint():
                    if self.currentSavePoint_:
                        del self.currentSavePoint_
                        self.currentSavePoint_ = None

                    self.stackSavePoints_.clear()
                    self.queueSavePoints_.clear()

                cur.d.modeAccess_ = CursorAccessMode.Browse
                if cancel:
                    cur.select()

                db_signals.emitTransactionRollback(cur)
                return True
            else:
                logger.warning("doRollback: Fallo al intentar deshacer transacción")
                return False

        else:

            project.message_manager().send(
                "status_help_msg", "send", ["Restaurando punto de salvaguarda %s:%s..." % (self.name, self.transaction_)]
            )
            if not self.canSavePoint():
                tam_queue = len(self.queueSavePoints_)
                for i in range(tam_queue):
                    temp_save_point = self.queueSavePoints_.pop()
                    temp_id = temp_save_point.id()

                    if temp_id > self.transaction_ or self.transaction_ == 0:
                        temp_save_point.undo()
                        del temp_save_point
                    else:
                        self.queueSavePoints_.append(temp_save_point)

                if self.currentSavePoint_ is not None:
                    self.currentSavePoint_.undo()
                    self.currentSavePoint_ = None
                    if self.stackSavePoints_:
                        self.currentSavePoint_ = self.stackSavePoints_.pop()

                if self.transaction_ == 0:
                    if self.currentSavePoint_:
                        del self.currentSavePoint_
                        self.currentSavePoint_ = None

                    self.stackSavePoints_.clear()
                    self.queueSavePoints_.clear()

            else:
                self.rollbackSavePoint(self.transaction_)

            cur.d.modeAccess_ = CursorAccessMode.Browse
            return True

    def interactiveGUI(self) -> bool:
        return self.interactiveGUI_

    def doCommit(self, cur, notify=True) -> bool:
        if not cur and not self.db():
            return False

        if not notify:
            cur.autoCommit.emit()

        if self.transaction_ > 0:
            if cur.d.transactionsOpened_:
                trans = cur.d.transactionsOpened_.pop()
                if not trans == self.transaction_:
                    logger.warning("El cursor va a terminar la transacción %s pero la última que inició es la %s", self.transaction_, trans)
            else:
                logger.warning("El cursor va a terminar la transacción %s pero no ha iniciado ninguna", self.transaction_)

            self.transaction_ = self.transaction_ - 1
        else:

            return True

        from pineboolib.application import project

        if self.transaction_ == 0 and self.canTransaction():
            if config.value("application/isDebuggerMode", False):
                project.message_manager().send("status_help_msg", "send", ["Terminando transacción... %s" % self.transaction_])
            try:
                if self.driver().commitTransaction():
                    self.lastActiveCursor_ = None

                    if not self.canSavePoint():
                        if self.currentSavePoint_:
                            del self.currentSavePoint_
                            self.currentSavePoint_ = None

                        self.stackSavePoints_.clear()
                        self.queueSavePoints_.clear()

                    if notify:
                        cur.d.modeAccess_ = CursorAccessMode.Browse

                    db_signals.emitTransactionEnd(cur)
                    return True

                else:
                    logger.error("doCommit: Fallo al intentar terminar transacción: %s" % self.transaction_)
                    return False

            except Exception as e:
                logger.error("doCommit: Fallo al intentar terminar transacción: %s", e)
                return False
        else:
            project.message_manager().send(
                "status_help_msg", "send", ["Liberando punto de salvaguarda %s:%s..." % (self.name, self.transaction_)]
            )
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
                    cur.d.modeAccess_ = CursorAccessMode.Browse

                return True
            if not self.canSavePoint():
                tam_queue = len(self.queueSavePoints_)
                for i in range(tam_queue):
                    temp_save_point = self.queueSavePoints_.pop()
                    temp_save_point.setId(self.transaction_ - 1)
                    self.queueSavePoints_.append(temp_save_point)

                if self.currentSavePoint_:
                    self.queueSavePoints_.append(self.currentSavePoint_)
                    self.currentSavePoint_ = None
                    if self.stackSavePoints_:
                        self.currentSavePoint_ = self.stackSavePoints_.pop()
            else:
                self.releaseSavePoint(self.transaction_)

            if notify:
                cur.d.modeAccess_ = CursorAccessMode.Browse

            return True

    def canDetectLocks(self) -> Any:
        if not self.db():
            return False

        return self.driver().canDetectLocks()

    def commit(self) -> Any:
        if not self.db():
            return False

        return self.driver().commitTransaction()

    def managerModules(self) -> "flmanagermodules.FLManagerModules":
        if not self._managerModules:
            from pineboolib.fllegacy.flmanagermodules import FLManagerModules

            self._managerModules = FLManagerModules(self)

        return self._managerModules

    def canOverPartition(self) -> Any:
        if not self.db():
            return False

        return self.dbAux().driver().canOverPartition()

    def savePoint(self, savePoint) -> Any:
        if not self.db():
            return False

        return self.driver().savePoint(savePoint)

    def releaseSavePoint(self, savePoint) -> Any:
        if not self.db():
            return False

        return self.driver().releaseSavePoint(savePoint)

    def Mr_Proper(self):
        if not self.db():
            return

        self.dbAux().driver().Mr_Proper()

    def rollbackSavePoint(self, savePoint) -> Any:
        if not self.db():
            return False

        return self.driver().rollbackSavePoint(savePoint)

    def transaction(self) -> Any:
        if not self.db():
            return False

        return self.driver().transaction()

    def commitTransaction(self) -> Any:
        if not self.db():
            return False

        return self.driver().commitTransaction()

    def rollbackTransaction(self) -> Any:
        if not self.db():
            return False

        return self.driver().rollbackTransaction()

    def nextSerialVal(self, table, field) -> Any:
        if not self.db():
            return False

        return self.dbAux().driver().nextSerialVal(table, field)

    def existsTable(self, name) -> Any:
        if not self.db():
            return False

        return self.dbAux().driver().existsTable(name)

    def createTable(self, tmd) -> bool:
        if not self.db():
            return False

        sql = self.dbAux().driver().sqlCreateTable(tmd)
        if not sql:
            return False
        if self.transaction_ == 0:
            self.transaction()
            self.transaction_ += 1

        for singleSql in sql.split(";"):
            try:
                self.dbAux().execute_query(singleSql)
            except Exception:
                logger.exception("createTable: Error happened executing sql: %s...", singleSql[:80])
                self.rollbackTransaction()
                return False
        if self.transaction_ > 0:
            self.commitTransaction()
            self.transaction_ -= 1

        return True

    def mismatchedTable(self, tablename, tmd) -> Any:
        if not self.db():
            return None

        return self.dbAux().driver().mismatchedTable(tablename, tmd, self)

    def normalizeValue(self, text) -> Optional[str]:
        if getattr(self.driver(), "normalizeValue", None):
            return self.driver().normalizeValue(text)

        logger.warning("PNConnection: El driver %s no dispone de normalizeValue(text)", self.driverName())
        return text

    def queryUpdate(self, name, update, filter) -> Any:
        if not self.db():
            return None

        return self.driver().queryUpdate(name, update, filter)

    def execute_query(self, q) -> Any:
        if not self.db():
            return None
        return self.driver().execute_query(q)

    def alterTable(self, mtd_1, mtd_2, key, force=False) -> Any:
        if not self.db():
            return None

        return self.dbAux().driver().alterTable(mtd_1, mtd_2, key, force)

    def __str__(self):
        return self.DBName()
