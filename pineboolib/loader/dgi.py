"""DGI Module."""

from pineboolib import logging

from typing import Callable, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from pineboolib.interfaces.dgi_schema import dgi_schema
    from pineboolib.plugins.dgi.dgi_qt.dgi_qt import dgi_qt
    from pineboolib.plugins.dgi.dgi_aqnext.dgi_aqnext import dgi_aqnext
    from pineboolib.plugins.dgi.dgi_fcgi.dgi_fcgi import dgi_fcgi
    from pineboolib.plugins.dgi.dgi_jsonrpc.dgi_jsonrpc import dgi_jsonrpc
    from pineboolib.plugins.dgi.dgi_server.dgi_server import dgi_server


logger = logging.getLogger(__name__)


def load_dgi(name: str, param: Any) -> "dgi_schema":
    """Load a DGI module dynamically."""

    dgi_entrypoint = DGILoader.load_dgi(name)

    try:
        dgi = dgi_entrypoint()  # FIXME: Necesitamos ejecutar código dinámico tan pronto?
    except Exception:
        logger.exception("Error inesperado al cargar el módulo DGI %s" % name)
        raise

    if param:
        dgi.setParameter(param)

    logger.info("DGI loaded: %s", name)

    return dgi


class DGILoader(object):
    """DGILoader Class."""

    @staticmethod
    def load_dgi_qt() -> "dgi_qt":
        """Load dgi qt."""

        from pineboolib.plugins.dgi.dgi_qt import dgi_qt as dgi

        return dgi.dgi_qt()

    @staticmethod
    def load_dgi_aqnext() -> "dgi_aqnext":
        """Load dgi aqnext."""

        from pineboolib.plugins.dgi.dgi_aqnext import dgi_aqnext as dgi

        return dgi.dgi_aqnext()

    @staticmethod
    def load_dgi_fcgi() -> "dgi_fcgi":
        """Load dgi fcgi."""

        from pineboolib.plugins.dgi.dgi_fcgi import dgi_fcgi as dgi

        return dgi.dgi_fcgi()

    @staticmethod
    def load_dgi_jsonrpc() -> "dgi_jsonrpc":
        """Load dgi jsonrpc."""

        from pineboolib.plugins.dgi.dgi_jsonrpc import dgi_jsonrpc as dgi

        return dgi.dgi_jsonrpc()

    @staticmethod
    def load_dgi_server() -> "dgi_server":
        """Load dgi server."""

        from pineboolib.plugins.dgi.dgi_server import dgi_server as dgi

        return dgi.dgi_server()

    @classmethod
    def load_dgi(cls, name: str) -> Callable:
        """Load dgi specified by name."""

        loader = getattr(cls, "load_dgi_%s" % name, None)
        if not loader:
            raise ValueError("Unknown DGI %s" % name)
        return loader
