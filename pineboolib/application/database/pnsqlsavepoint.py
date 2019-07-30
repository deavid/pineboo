# -*- coding: utf-8 -*-
"""
Module for PNSqlSavePoint class.
"""

from pineboolib.core import decorators
from typing import Any, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .pnsqlcursor import PNSqlCursor
    from .pnbuffer import PNBuffer


class OpInfo:
    """
    OpInfo Class.

    Information about an operation.

    The information of an operation is; the primary key,
    operation performed (0 = insert, 1 = edit, 2 = delete),
    buffer with the contents of the record affected by the operation,
    position of the current cursor record,
    cursor order, cursor filter, cursor name (from the table),
    associated cursor.
    """

    primaryKey: str
    op: int
    buffer: "PNBuffer"
    at: int
    sort: str
    filter: str
    name: str
    cursor: "PNSqlCursor"
    autoDelete_: bool

    def __init__(self, *args, **kwargs) -> None:
        """Initialize a virtual save point."""
        if len(args) > 0:

            self.opInfo(*args)

        self.setAutoDelete(False)

    def opInfo(self, pK: str, o: Any, b: "PNBuffer", a: int, s: str, f: str, n: str, c: "PNSqlCursor") -> None:
        """
        Save initialization values.

        @param pK. primaryKey.
        @param o. option (1,2,3)
        @param b. PNBuffer
        @param a. cursor postition.
        @param s. sort.
        @param f. filter.
        @param n. cursor name.
        @param c. cursor object.
        """

        self.primaryKey = pK
        self.op = o
        self.buffer = b
        self.at = a
        self.sort = s
        self.filter = f
        self.name = n
        self.cursor = c

    def setAutoDelete(self, b: bool) -> None:
        """I specify if I do autoDelete when closing."""
        self.autoDelete_ = b


class PNSqlSavePoint:
    """
    PNSqlSavePoint Class.

    Safeguard point of a set of basic operations about cursors (insert, edit and delete).

    Through this class you can save a group of basic operations
    about cursors (insert, edit and delete).
    Undo a safeguard point, means that all operations
    stored are canceled by performing the necessary actions so that
    They have no effect.

    For proper operation you must keep the buffer's (QSqlRecord)
    with the content of the records to be modified or modified by an operation,
    indicating the name of the primary key and the cursor to which it belongs.
    """

    """
    Pila para almacenar informacion de las operaciones.
    """

    opInfos: List[OpInfo] = []

    """
    Identificador del punto de salvaguarda
    """
    id_: int
    countRefSavePoint = 0

    def __init__(self, _id=None) -> None:
        """
        Initialize the safeguard point.

        @param id SavePoint identifier.
        """

        self.opInfos.append(OpInfo())
        self.opInfos[0].setAutoDelete(True)

        self.id_ = _id
        self.countRefSavePoint = self.countRefSavePoint + 1

    def __del__(self) -> None:
        """Process when the savePoint point is destroyed."""

        if self.opInfos:
            self.opInfos = []

        self.countRefSavePoint = self.countRefSavePoint - 1

    def setId(self, id_: int) -> None:
        """
        Set the SavePoint identifier.

        @param id_. Identifier
        """
        self.id_ = id_

    def id(self) -> int:
        """
        Return the identifier.

        @return identifier.
        """

        return self.id_

    def clear(self) -> None:
        """
        Clean the safeguard point.

        All stored operations are deleted, therefore, after invoke this method can no longer be undone.
        """

        self.opInfos.clear()

    @decorators.BetaImplementation
    def undo(self) -> None:
        """
        Undo the SavePoint.
        """

        while self.opInfos:
            opInf = self.opInfos.pop()
            if opInf.op == 0:
                self.undoInsert(opInf)
            if opInf.op == 1:
                self.undoEdit(opInf)
            if opInf.op == 2:
                self.undoDel(opInf)
            del opInf
        self.clear()

    @decorators.BetaImplementation
    def saveInsert(self, primaryKey: str, buffer: Optional["PNBuffer"], cursor: Optional["PNSqlCursor"]) -> None:
        """
        Save the buffer with the contents of the inserted record.

        @param primaryKey Name of the field that is primary key.
        @param buffer buffer with the contents of the record.
        @param cursor Cursor associated.
        """
        if not cursor or not buffer:
            return
        self.opInfos.append(OpInfo(primaryKey, 0, buffer, cursor.at(), cursor.sort(), cursor.filter(), cursor.name, cursor))

    def saveEdit(self, primaryKey: str, buffer: Optional["PNBuffer"], cursor: Optional["PNSqlCursor"]) -> None:
        """
        Save the buffer with the contents of the record to be edited.

        @param primaryKey Name of the field that is primary key.
        @param buffer buffer with the contents of the record.
        @param cursor Cursor associated.

        """
        if not cursor or not buffer:
            return

        self.opInfos.append(OpInfo(primaryKey, 1, buffer, cursor.at(), cursor.sort(), cursor.filter(), cursor.name, cursor))

    @decorators.BetaImplementation
    def saveDel(self, primaryKey: str, buffer: Optional["PNBuffer"], cursor: Optional["PNSqlCursor"]) -> None:
        """
        Save the buffer with the contents of the record to be deleted.

        @param primaryKey Name of the field that is primary key.
        @param buffer buffer with the contents of the record.
        @param cursor Cursor associated.

        """
        if not cursor or not buffer:
            return
        self.opInfos.append(OpInfo(primaryKey, 2, buffer, cursor.at(), cursor.sort(), cursor.filter(), cursor.name, cursor))

    @decorators.BetaImplementation
    def undoInsert(self, opInf: OpInfo) -> None:
        """
        Undo an insert operation.

        @param opInf Operation information.
        """

        cursor_ = opInf.cursor
        owner = False
        if not cursor_:
            from . import pnsqlcursor

            cursor_ = pnsqlcursor.PNSqlCursor(opInf.name)
            cursor_.setForwardOnly(True)
            owner = True

        if not cursor_:
            return

        if opInf.buffer.indexField(opInf.primaryKey) and not opInf.buffer.isNull(opInf.primaryKey):
            valuePrimaryKey = str(opInf.buffer.value(opInf.primaryKey))  # FIXME: (deavid) plz add notes on what needs to be fixed here.
            ok = cursor_.select(opInf.primaryKey + "='" + valuePrimaryKey + "'")
            if ok and cursor_.next():
                cursor_.primeDelete()

        if not owner:
            cursor_.select(opInf.filter, opInf.sort)
            cursor_.seek(opInf.at)

    @decorators.BetaImplementation
    def undoEdit(self, opInf: OpInfo) -> None:
        """
        Undo an edit operation.

        @param opInf Operation information.
        """
        cursor_ = opInf.cursor
        owner = False

        if not cursor_:
            from . import pnsqlcursor

            cursor_ = pnsqlcursor.PNSqlCursor(opInf.name)
            cursor_.setForwardOnly(True)
            owner = True

        if not cursor_:
            return
        valuePrimaryKey = str(opInf.buffer.value(opInf.primaryKey))
        ok = cursor_.select(opInf.primaryKey + "='" + valuePrimaryKey + "'")
        if ok and cursor_.next():
            # buf = cursor_.primeUpdate()
            # buf = opInf.buffer
            cursor_.primeUpdate()
            cursor_.update()

        if not owner:
            cursor_.select(opInf.filter, opInf.sort)
            cursor_.seek(opInf.at)
        else:
            del cursor_

    @decorators.BetaImplementation
    def undoDel(self, opInf: OpInfo) -> None:
        """
        Undo an delete operation.

        @param opInf Operation information.
        """
        cursor_ = opInf.cursor
        owner = False
        if not cursor_:
            from . import pnsqlcursor

            cursor_ = pnsqlcursor.PNSqlCursor(opInf.name)
            cursor_.setForwardOnly(True)
            owner = True

        if not cursor_:
            return

        # buf = cursor_.primeInsert()
        # buf = opInf.buffer
        cursor_.primeInsert()
        cursor_.insert()

        if not owner:
            cursor_.select(opInf.filter, opInf.sort)
            cursor_.seek(opInf.at)
        else:
            del cursor_
