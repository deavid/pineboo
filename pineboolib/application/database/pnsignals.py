class PNSignals(object):
    notify_begin_transaction_: bool
    notify_end_transaction_: bool
    notify_roll_back_transaction_: bool

    def __init__(self):
        super().__init__()

        self.notify_begin_transaction_ = False
        self.notify_end_transaction_ = False
        self.notify_roll_back_transaction_ = False

    def emitTransactionBegin(self, o) -> None:
        if self.notify_begin_transaction_:
            o.transactionBegin.emit()

    def emitTransactionEnd(self, o) -> None:
        if self.notify_end_transaction_:
            o.transactionEnd.emit()

    def emitTransactionRollback(self, o) -> None:
        if self.notify_roll_back_transaction_:
            o.transsactionRollBack.emit()
