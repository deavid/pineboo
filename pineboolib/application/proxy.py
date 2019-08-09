"""
Proxy Module.
"""
from typing import Callable
from pineboolib import logging
from typing import Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from pineboolib.fllegacy.flformdb import FLFormDB  # noqa: F401


class DelayedObjectProxyLoader(object):
    """
    Delay load of an object until its first accessed.
    This is used to create entities such "formclientes" or "flfactppal" ahead of time and
    publish them in pineboolib.qsa.qsa so the code can freely call flfactppal.iface.XXX.

    Once the first attribute is called, the object is loaded.

    QSA Code should avoid calling directly "formclientes" and instead use QSADictModules or SafeQSA
    """

    logger = logging.getLogger("application.DelayedObjectProxyLoader")

    def __init__(
        self, obj: Callable[..., "FLFormDB"], name: Optional[str] = None, *args: str, **kwargs: str
    ) -> None:
        """
        Constructor.
        """
        self.logger.trace("obj: %r", obj)
        self._name: str = name or "unnamed-loader"
        self._obj = obj
        self._args = args
        self._kwargs = kwargs
        self.loaded_obj: Optional["FLFormDB"] = None

    def __load(self) -> "FLFormDB":
        """
        Load a new object.

        @return objeto nuevo o si ya existe , cacheado
        """
        if self.loaded_obj is not None:
            return self.loaded_obj
        self.logger.debug(
            "DelayedObjectProxyLoader: loading %s %s( *%s **%s)",
            self._name,
            self._obj,
            self._args,
            self._kwargs,
        )

        self.loaded_obj = self._obj(*self._args, **self._kwargs)
        self.logger.trace("loaded object: %r", self.loaded_obj)
        if self.loaded_obj is None:
            raise Exception("Failed to load object")
        return self.loaded_obj

    def __getattr__(self, name: str) -> Any:  # Solo se lanza si no existe la propiedad.
        """
        Return attribute or method from internal object.

        @param name. Nombre del la función buscada
        @return el objecto del XMLAction afectado
        """
        obj_ = self.__load()
        return getattr(obj_, name, getattr(obj_.widget, name, None))
