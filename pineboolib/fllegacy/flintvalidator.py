# -*- coding: utf-8 -*-
from PyQt5 import QtGui  # type: ignore
from typing import Any, Tuple


class FLIntValidator(QtGui.QIntValidator):
    _formatting = None

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args[0], args[1], args[2])
        self._formatting = False

    def validate(self, input_, pos_cursor) -> Tuple[Any, Any, Any]:

        if not input_ or self._formatting:
            return (self.Acceptable, input_, pos_cursor)

        state = super().validate(input_, pos_cursor)

        ret_0 = None
        ret_1 = state[1]
        ret_2 = state[2]

        if state[0] in (self.Invalid, self.Intermediate) and len(input_) > 0:
            s = input_[1:]
            if (
                input_[0] == "-"
                and super().validate(s, pos_cursor)[0] == self.Acceptable
                or s == ""
            ):
                ret_0 = self.Acceptable
            else:
                ret_0 = self.Invalid
        else:
            ret_0 = self.Acceptable

        # FIXME:Salir formateado
        return (ret_0, ret_1, ret_2)
