# -*- coding: utf-8 -*-
from PyQt5 import QtCore

class FLSqlCursor(QtCore.QObject):
    
    parent_cursor = None
    _buffer_changed = None
    _before_commit = None
    _after_commit = None
    _buffer_commited = None
    _inicia_valores_cursor = None
    _buffer_changed_label = None
    _validate_cursor = None
    _validate_transaction = None
    _cursor_accepted = None
    
    def __init__(self, cursor, stabla):
        super().__init__()
        self.parent_cursor = cursor
        self.parent_cursor.setActivatedBufferChanged(False)
        self.parent_cursor.setActivatedBufferCommited(False)
        
        
        if stabla:
            (self._model, self._buffer_changed, self._before_commit, self._after_commit, self._buffer_commited, self._inicia_valores_cursor, self._buffer_changed_label, self._validate_cursor, self._validate_transaction, self._cursor_accepted) = self.obtener_modelo(stabla)
            self._stabla = self._model._meta.db_table
    
    
    def buffer_changed_signal(self, scampo):
        if self._buffer_changed is None:
            return True

        return self._buffer_changed(scampo, self.parent_cursor)

    def buffer_commited_signal(self):
        if not self._activatedBufferCommited:
            return True

        if self._buffer_commited is None:
            return True

        try:
            return self._buffer_commited(self.parent_cursor)
        except Exception as exc:
            print("Error inesperado", exc)

    def before_commit_signal(self):
        if not self._activatedCommitActions:
            return True

        if self._before_commit is None:
            return True

        return self._before_commit(self.parent_cursor)

    def after_commit_signal(self):
        if not self._activatedCommitActions:
            return True

        if self._after_commit is None:
            return True

        return self._after_commit(self.parent_cursor)

    def inicia_valores_cursor_signal(self):
        if self._inicia_valores_cursor is None:
            return True

        return self._inicia_valores_cursor(self.parent_cursor)

    def buffer_changed_label_signal(self, scampo):
        if self._buffer_changed_label is None:
            return {}

        import inspect
        expected_args = inspect.getargspec(self._buffer_changed_label)[0]
        if len(expected_args) == 3:
            return self._buffer_changed_label(self._model, scampo, self.parent_cursor)
        else:
            return self._buffer_changed_label(scampo, self.parent_cursor)

    def validate_cursor_signal(self):
        if self._validate_cursor is None:
            return True

        return self._validate_cursor(self.parent_cursor)

    def validate_transaction_signal(self):
        if self._validate_transaction is None:
            return True

        return self._validate_transaction(self.parent_cursor)

    def cursor_accepted_signal(self):
        if self._cursor_accepted is None:
            return True

        return self._cursor_accepted(self.parent_cursor)
    
    def obtener_modelo(self, stabla):
        from YBLEGACY.FLAux import FLAux
        return FLAux.obtener_modelo(stabla)   