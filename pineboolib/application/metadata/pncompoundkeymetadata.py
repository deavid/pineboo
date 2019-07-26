# -*- coding: utf-8 -*-

from typing import Any, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .pnfieldmetadata import PNFieldMetaData

"""
Clase para definir claves compuestas.

Esta clase sirve para crear objetos que contienen
una lista con los campos que conforman una clave.
En la lista de campos se guardan los metadatos de estos,
es decir objetos FLFieldMetaData.

"""


class PNCompoundKeyMetaData(object):

    """
    Lista de con los metadatos de los campos que componen la clave
    """

    fieldList_: List["PNFieldMetaData"] = []

    def __init__(self, other: "PNCompoundKeyMetaData" = None) -> None:
        super().__init__()
        self.fieldList_ = []
        if other:
            self.copy(other)

    """
    Añade la descripción de un campo a lista  de campos que componen la clave.

    @param f Objeto FLFieldMetaData con la descripción del campo a añadir
    """

    def addFieldMD(self, f: "PNFieldMetaData") -> None:
        self.fieldList_.append(f)

    """
    Obtiene si una campo pertenece a la clave compuesta.

    @param fN Nombre del campo del que se desea saber si pertenece o no a la clave compuesta
    @return TRUE si el campo forma parte de la clave compuesta, FALSE en caso contrario
    """

    def hasField(self, fN) -> bool:
        for i in self.fieldList_:
            if i.name() == str(fN):
                return True

        return False

    """
    Para obtener la lista de definiciones de campos que componen la clave.

    @return Objeto con la lista de deficiones de campos de la clave compuesta
    """

    def fieldList(self) -> Any:
        return self.fieldList_

    def copy(self, other) -> None:
        if self is other:
            return
        self.fieldList_ = other.fieldList_[:]
