from typing import Any, List, Optional, Dict
from xml.etree.ElementTree import Element
from .utils_base import aqtt


class Struct(object):
    """
        Plantilla básica de objeto. Asigna sus propiedades en el __init__.
        Especialmente útil para bocetar clases al vuelo.
    """

    fields: List[str]
    pk: List[str]
    fields_idx: Dict[str, int]

    def __init__(self, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


class XMLStruct(Struct):
    """
        Plantilla de objeto que replica el contenido de un xml. Sirve para tener rápidamente un objeto
        que sea idéntico al xml que se pueda acceder fácilmente por propiedades.
    """

    def __init__(self, xmlobj: Optional[Element] = None) -> None:
        self._attrs: List[str] = []
        if xmlobj is not None:
            self.__name__ = xmlobj.tag
            for child in xmlobj:
                if child.tag == "property":
                    # Se importa aquí para evitar error de importación cíclica.
                    raise Exception("FIXME: No property support")
                    # FIXME: Esto es del DGI QT:
                    # from pineboolib.pnqt3ui import loadProperty
                    # key, text = loadProperty(child)
                else:
                    text = aqtt(child.text)
                    key = child.tag
                if isinstance(text, str):
                    text = text.strip()
                try:
                    setattr(self, key, text)
                    self._attrs.append(key)
                except Exception:
                    print("utils.XMLStruct: Omitiendo", self.__name__, key, text)

    def __str__(self) -> str:
        attrs = ["%s=%s" % (k, repr(getattr(self, k))) for k in self._attrs]
        txtattrs = " ".join(attrs)
        return "<%s.%s %s>" % (self.__class__.__name__, self.__name__, txtattrs)

    def _v(self, k: str, default: None = None) -> Optional[str]:
        return getattr(self, k, default)

    def _rv(self, k: str) -> str:
        ret = getattr(self, k, None)
        if not isinstance(ret, str):
            raise ValueError(
                "Retrieving value for %s, found %r which is not a string" % (k, ret)
            )
        return ret


class AreaStruct(Struct):
    idarea: str
    descripcion: str


class TableStruct(Struct):
    xmltree: Any
    xmlroot: Any
    tablename: str
    name: str
    query_table: Optional[str]
    fields: List[str]
    pk: List[str]
    fields_idx: Dict[str, int]
