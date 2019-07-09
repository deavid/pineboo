"""
Crea una conexión con el interface adecuado del DGI usado para mostrar mensajes
"""
from typing import Any


class Manager(object):

    _dgi = None

    def __init__(self, dgi) -> None:
        self._dgi = dgi

    def send(self, type_: str, function_: str = None, data_=None) -> Any:
        if self._dgi is None:
            return None
        obj_ = getattr(self._dgi, type_, None)
        ret_ = None
        if obj_:
            if function_ is not None:
                attr_ = getattr(obj_, function_, None)
            else:
                attr_ = obj_
            if not data_:
                ret_ = attr_()
            else:
                ret_ = attr_(*data_)
            self._dgi.processEvents()

        if ret_ is not None:
            return ret_
