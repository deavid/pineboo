"""
Module for PNSignals class.
"""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pineboolib.application.database.pnsqlcursor import PNSqlCursor


class PNSignals(object):
    """
    Signals for database.

    Used in flapplication.
    Filters out transaction signals.
    """

    notify_begin_transaction_: bool
    notify_end_transaction_: bool
    notify_roll_back_transaction_: bool

    def __init__(self):
        """
        Create new PNSignals.

        It is treated like a singleton. See pineboolib.database.db_signals
        """
        super().__init__()

        self.notify_begin_transaction_ = False
        self.notify_end_transaction_ = False
        self.notify_roll_back_transaction_ = False

    def emitTransactionBegin(self, o: "PNSqlCursor") -> None:
        """Emit transaction begin signal."""
        if self.notify_begin_transaction_:
            o.transactionBegin.emit()

    def emitTransactionEnd(self, o: "PNSqlCursor") -> None:
        """Emit transaction end signal."""
        if self.notify_end_transaction_:
            o.transactionEnd.emit()

    def emitTransactionRollback(self, o: "PNSqlCursor") -> None:
        """Emit transaction begin rollback."""
        if self.notify_roll_back_transaction_:
            o.transsactionRollBack.emit()
