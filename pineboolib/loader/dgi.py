import importlib
import logging

logger = logging.getLogger(__name__)


def load_dgi(name, param):
    """Load a DGI module dynamically."""

    modname = "dgi_%s" % name
    modpath = "pineboolib.plugins.dgi.%s.%s" % (modname, modname)

    # FIXME: No se puede importar el proyecto si aún ni lo hemos cargado.
    # try:
    #     import pineboolib  # noqa: F401
    # except Exception:
    #     print("Cargando como invitado")
    #     modpath = "pineboo.%s" % modpath

    try:
        dgi_pymodule = importlib.import_module(modpath)
    except ImportError:
        print("No se ha encontrado el módulo DGI %s" % (modpath))
        raise

    dgi_entrypoint = getattr(dgi_pymodule, modname, None)
    if dgi_entrypoint is None:
        raise ImportError("Fallo al cargar el punto de entrada al módulo DGI %s" % modpath)

    try:
        dgi = dgi_entrypoint()  # FIXME: Necesitamos ejecutar código dinámico tan pronto?
    except Exception:
        logger.exception("Error inesperado al cargar el módulo DGI %s" % modpath)
        raise

    if param:
        dgi.setParameter(param)

    logger.info("DGI loaded: %s", name)

    return dgi
