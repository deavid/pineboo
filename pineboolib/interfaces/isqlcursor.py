"""
ISqlCursor module.
"""
from typing import Any
from pineboolib.interfaces.cursoraccessmode import CursorAccessMode


class ISqlCursor(object):
    """
    Abstract class for PNSqlCursor.
    """

    Insert = CursorAccessMode.Insert
    Edit = CursorAccessMode.Edit
    Del = CursorAccessMode.Del
    Browse = CursorAccessMode.Browse
    Value = 0
    RegExp = 1
    Function = 2

    def __init__(
        self,
        name: str = None,
        autopopulate: bool = True,
        connectionName_or_db: Any = None,
        cR=None,
        r=None,
        parent=None,
    ):
        """Create cursor."""
        super().__init__()

    def init(self, name: str, autopopulate, cR, r) -> None:
        """Initialize cursor."""
        pass

    def conn(self) -> Any:
        """Retrieve connection object."""
        pass

    def table(self) -> Any:
        """Retrieve table name."""
        pass

    def setName(self, name, autop) -> Any:
        """Set cursor name."""
        pass

    def metadata(self) -> Any:
        """Get table metadata for this cursor table."""
        pass

    def currentRegister(self) -> Any:
        """Get current row number."""
        pass

    def modeAccess(self) -> Any:
        """Get current access mode."""
        pass

    def filter(self) -> str:
        """Get SQL filter as a string."""
        return ""

    def mainFilter(self) -> Any:
        """Get SQL Main filter as a string."""
        pass

    def action(self) -> Any:
        """Get action object."""
        pass

    def actionName(self) -> Any:
        """Get action name."""
        pass

    def setAction(self, a) -> Any:
        """Set Action object."""
        pass

    def setMainFilter(self, f, doRefresh=True) -> Any:
        """Set Main filter for this cursor."""
        pass

    def setModeAccess(self, m) -> Any:
        """Set Access mode for the cursor."""
        pass

    def connectionName(self) -> Any:
        """Get current connection name."""
        pass

    def setValueBuffer(self, fN, v) -> Any:
        """Set Value on the cursor buffer."""
        pass

    def valueBuffer(self, fN) -> Any:
        """Get value from cursor buffer."""
        pass

    def fetchLargeValue(self, value) -> Any:
        """Fetch from fllarge."""
        pass

    def valueBufferCopy(self, fN) -> Any:
        """Get original value on buffer."""
        pass

    def setEdition(self, b, m=None) -> Any:
        """Set edit mode."""
        pass

    def restoreEditionFlag(self, m) -> Any:
        """Restore edit flag."""
        pass

    def setBrowse(self, b, m=None) -> Any:
        """Set browse mode."""
        pass

    def restoreBrowseFlag(self, m) -> Any:
        """Restore browse flag."""
        pass

    def meta_model(self) -> Any:
        """Get sqlAlchemy model."""
        pass

    def setContext(self, c=None) -> Any:
        """Set script execution context."""
        pass

    def context(self) -> Any:
        """Get script execution context."""
        pass

    def fieldDisabled(self, fN) -> Any:
        """Get if field is disabled."""
        pass

    def inTransaction(self) -> Any:
        """Return if transaction is in progress."""
        pass

    def transaction(self, lock=False) -> Any:
        """Open transaction."""
        pass

    def rollback(self) -> Any:
        """Rollback transaction."""
        pass

    def commit(self, notify=True) -> Any:
        """Commit transaction."""
        pass

    def size(self) -> Any:
        """Get current cursor size in rows."""
        pass

    def openFormInMode(self, m, cont=True) -> Any:
        """Open record form in specified mode."""
        pass

    def isNull(self, fN) -> Any:
        """Get if field is null."""
        pass

    def updateBufferCopy(self) -> Any:
        """Refresh buffer copy."""
        pass

    def isModifiedBuffer(self) -> Any:
        """Get if buffer is modified."""
        pass

    def setAskForCancelChanges(self, a) -> Any:
        """Activate dialog for asking before closing."""
        pass

    def setActivatedCheckIntegrity(self, a) -> Any:
        """Activate integrity checks."""
        pass

    def activatedCheckIntegrity(self) -> Any:
        """Get integrity check state."""
        pass

    def setActivatedCommitActions(self, a) -> Any:
        """Activate before/after commit."""
        pass

    def activatedCommitActions(self) -> Any:
        """Get before/after commit status."""
        pass

    def setActivatedBufferChanged(self, activated_bufferchanged) -> Any:
        """Activate Buffer changed."""
        pass

    def activatedBufferChanged(self) -> Any:
        """Get buffer changed status."""
        pass

    def setActivatedBufferCommited(self, activated_buffercommited) -> Any:
        """Activate buffer committed."""
        pass

    def activatedBufferCommited(self) -> Any:
        """Get buffer committed status."""
        pass

    def cursorRelation(self) -> Any:
        """Get cursor relation."""
        pass

    def relation(self) -> Any:
        """Get relation."""
        pass

    def setUnLock(self, fN, v) -> Any:
        """Set unlock field."""
        pass

    def isLocked(self) -> Any:
        """Get if record is locked."""
        pass

    def buffer(self) -> Any:
        """Get buffer object."""
        pass

    def bufferCopy(self) -> Any:
        """Get buffer copy."""
        pass

    def bufferIsNull(self, pos_or_name) -> Any:
        """Get if value is null in buffer."""
        pass

    def bufferSetNull(self, pos_or_name) -> Any:
        """Set null to value in buffer."""
        pass

    def bufferCopyIsNull(self, pos_or_name) -> Any:
        """Get if value is null in original buffer."""
        pass

    def bufferCopySetNull(self, pos_or_name) -> Any:
        """Set to null field in bufferCopy."""
        pass

    def setNull(self, name) -> Any:
        """Set field to null."""
        pass

    def db(self) -> Any:
        """Return database object."""
        pass

    def curName(self) -> Any:
        """Get cursor name."""
        pass

    def filterAssoc(self, fieldName, tableMD=None) -> Any:
        """Retrieve filter for associated field."""
        pass

    def calculateField(self, name) -> Any:
        """Return the result of a field calculation."""
        pass

    def model(self) -> Any:
        """Get sqlAlchemy model."""
        pass

    def selection(self) -> Any:
        """Get selection."""
        pass

    def at(self) -> Any:
        """Get row number."""
        pass

    def isValid(self) -> Any:
        """Return if cursor is valid."""
        pass

    def refresh(self, fN=None) -> Any:
        """Refresh cursor."""
        pass

    def refreshBuffer(self) -> Any:
        """Refresh buffer."""
        pass

    def setEditMode(self) -> Any:
        """Set cursor in edit mode."""
        pass

    def seek(self, i, relative=None, emite=None) -> Any:
        """Move cursor without fetching."""
        pass

    def next(self, emite=True) -> Any:
        """Get next row."""
        pass

    def moveby(self, pos) -> Any:
        """Move cursor down "pos" rows."""
        pass

    def prev(self, emite=True) -> Any:
        """Get previous row."""
        pass

    def move(self, row) -> Any:
        """Move cursor to row number."""
        pass

    def first(self, emite=True) -> Any:
        """Move cursor to first row."""
        pass

    def last(self, emite=True) -> Any:
        """Move cursor to last row."""
        pass

    def select(self, _filter=None, sort=None) -> Any:
        """Perform SQL Select."""
        pass

    def setSort(self, sortO) -> Any:
        """Set sorting order."""
        pass

    def insertRecord(self) -> Any:
        """Open form in insert mode."""
        pass

    def editRecord(self) -> Any:
        """Open form in edit mode."""
        pass

    def browseRecord(self) -> Any:
        """Open form in browse mode."""
        pass

    def deleteRecord(self) -> Any:
        """Delete record."""
        pass

    def copyRecord(self) -> Any:
        """Copy record."""
        pass

    def chooseRecord(self) -> Any:
        """Emit chooseRecord."""
        pass

    def setForwardOnly(self, b) -> Any:
        """Set forward only."""
        pass

    def commitBuffer(self, emite=True, checkLocks=False) -> Any:
        """Commit current buffer to db."""
        pass

    def commitBufferCursorRelation(self) -> Any:
        """Commit buffer from cursor relation."""
        pass

    def transactionLevel(self) -> Any:
        """Get number of nested transactions."""
        pass

    def transactionsOpened(self) -> Any:
        """Return if any transaction is open."""
        pass

    def rollbackOpened(self, count=-1, msg=None) -> Any:
        """Return if in rollback."""
        pass

    def commitOpened(self, count=-1, msg=None) -> Any:
        """Return if in commit."""
        pass
