from typing import Any
from pineboolib.interfaces.cursoraccessmode import CursorAccessMode


class ISqlCursor(object):
    Insert = CursorAccessMode.Insert
    Edit = CursorAccessMode.Edit
    Del = CursorAccessMode.Del
    Browse = CursorAccessMode.Browse
    Value = 0
    RegExp = 1
    Function = 2

    def __init__(self, name: str = None, autopopulate: bool = True, connectionName_or_db: Any = None, cR=None, r=None, parent=None):
        super().__init__()

    def init(self, name: str, autopopulate, cR, r) -> None:
        pass

    def conn(self) -> Any:
        pass

    def table(self) -> Any:
        pass

    def setName(self, name, autop) -> Any:
        pass

    def metadata(self) -> Any:
        pass

    def currentRegister(self) -> Any:
        pass

    def modeAccess(self) -> Any:
        pass

    def filter(self) -> str:
        return ""

    def mainFilter(self) -> Any:
        pass

    def action(self) -> Any:
        pass

    def actionName(self) -> Any:
        pass

    def setAction(self, a) -> Any:
        pass

    def setMainFilter(self, f, doRefresh=True) -> Any:
        pass

    def setModeAccess(self, m) -> Any:
        pass

    def connectionName(self) -> Any:
        pass

    def setValueBuffer(self, fN, v) -> Any:
        pass

    def valueBuffer(self, fN) -> Any:
        pass

    def fetchLargeValue(self, value) -> Any:
        pass

    def valueBufferCopy(self, fN) -> Any:
        pass

    def setEdition(self, b, m=None) -> Any:
        pass

    def restoreEditionFlag(self, m) -> Any:
        pass

    def setBrowse(self, b, m=None) -> Any:
        pass

    def restoreBrowseFlag(self, m) -> Any:
        pass

    def meta_model(self) -> Any:
        pass

    def setContext(self, c=None) -> Any:
        pass

    def context(self) -> Any:
        pass

    def fieldDisabled(self, fN) -> Any:
        pass

    def inTransaction(self) -> Any:
        pass

    def transaction(self, lock=False) -> Any:
        pass

    def rollback(self) -> Any:
        pass

    def commit(self, notify=True) -> Any:
        pass

    def size(self) -> Any:
        pass

    def openFormInMode(self, m, cont=True) -> Any:
        pass

    def isNull(self, fN) -> Any:
        pass

    def updateBufferCopy(self) -> Any:
        pass

    def isModifiedBuffer(self) -> Any:
        pass

    def setAskForCancelChanges(self, a) -> Any:
        pass

    def setActivatedCheckIntegrity(self, a) -> Any:
        pass

    def activatedCheckIntegrity(self) -> Any:
        pass

    def setActivatedCommitActions(self, a) -> Any:
        pass

    def activatedCommitActions(self) -> Any:
        pass

    def setActivatedBufferChanged(self, activated_bufferchanged) -> Any:
        pass

    def activatedBufferChanged(self) -> Any:
        pass

    def setActivatedBufferCommited(self, activated_buffercommited) -> Any:
        pass

    def activatedBufferCommited(self) -> Any:
        pass

    def cursorRelation(self) -> Any:
        pass

    def relation(self) -> Any:
        pass

    def setUnLock(self, fN, v) -> Any:
        pass

    def isLocked(self) -> Any:
        pass

    def buffer(self) -> Any:
        pass

    def bufferCopy(self) -> Any:
        pass

    def bufferIsNull(self, pos_or_name) -> Any:
        pass

    def bufferSetNull(self, pos_or_name) -> Any:
        pass

    def bufferCopyIsNull(self, pos_or_name) -> Any:
        pass

    def bufferCopySetNull(self, pos_or_name) -> Any:
        pass

    def atFrom(self) -> Any:
        pass

    def atFromBinarySearch(self, fN, v, orderAsc=True) -> Any:
        pass

    def setNull(self, name) -> Any:
        pass

    def db(self) -> Any:
        pass

    def curName(self) -> Any:
        pass

    def filterAssoc(self, fieldName, tableMD=None) -> Any:
        pass

    def calculateField(self, name) -> Any:
        pass

    def model(self) -> Any:
        pass

    def selection(self) -> Any:
        pass

    def at(self) -> Any:
        pass

    def isValid(self) -> Any:
        pass

    def refresh(self, fN=None) -> Any:
        pass

    def refreshBuffer(self) -> Any:
        pass

    def setEditMode(self) -> Any:
        pass

    def seek(self, i, relative=None, emite=None) -> Any:
        pass

    def next(self, emite=True) -> Any:
        pass

    def moveby(self, pos) -> Any:
        pass

    def prev(self, emite=True) -> Any:
        pass

    def move(self, row) -> Any:
        pass

    def first(self, emite=True) -> Any:
        pass

    def last(self, emite=True) -> Any:
        pass

    def select(self, _filter=None, sort=None) -> Any:
        pass

    def setSort(self, sortO) -> Any:
        pass

    def insertRecord(self) -> Any:
        pass

    def editRecord(self) -> Any:
        pass

    def browseRecord(self) -> Any:
        pass

    def deleteRecord(self) -> Any:
        pass

    def copyRecord(self) -> Any:
        pass

    def chooseRecord(self) -> Any:
        pass

    def setForwardOnly(self, b) -> Any:
        pass

    def commitBuffer(self, emite=True, checkLocks=False) -> Any:
        pass

    def commitBufferCursorRelation(self) -> Any:
        pass

    def transactionLevel(self) -> Any:
        pass

    def transactionsOpened(self) -> Any:
        pass

    def rollbackOpened(self, count=-1, msg=None) -> Any:
        pass

    def commitOpened(self, count=-1, msg=None) -> Any:
        pass
