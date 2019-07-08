class PNSignals(object):
    notify_begin_transaction_ = None
    notify_end_transaction_ = None
    notify_roll_back_transaction_ = None

    def __init__(self):
        super().__init__()

        self.notify_begin_transaction_ = False
        self.notify_end_transaction_ = False
        self.notify_roll_back_transaction_ = False

    def emitTransactionBegin(self, o):
        if self.notify_begin_transaction_:
            o.transactionBegin.emit()

    def emitTransactionEnd(self, o):
        if self.notify_end_transaction_:
            o.transactionEnd.emit()

    def emitTransactionRollback(self, o):
        if self.notify_roll_back_transaction_:
            o.transsactionRollBack.emit()
