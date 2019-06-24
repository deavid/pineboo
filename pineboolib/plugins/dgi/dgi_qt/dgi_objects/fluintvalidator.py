# -*- coding: utf-8 -*-
from PyQt5 import QtGui


class FLUIntValidator(QtGui.QIntValidator):
    _formatting = None

    def __init__(self, *args, **kwargs):
        if len(args) == 3:
            super().__init__(args[0], args[1], args[2])

        self._formatting = False

    def validate(self, input_, pos_cursor):

        if not input_ or self._formatting:
            return (self.Acceptable, input_, pos_cursor)

        i_v = QtGui.QIntValidator(0, 1000000000, self)
        state = i_v.validate(input_, pos_cursor)

        ret_0 = self.Invalid if state[0] is self.Intermediate else state[0]
        ret_1 = state[1]
        ret_2 = state[2]

        # FIXME: Salir formateado
        return (ret_0, ret_1, ret_2)
