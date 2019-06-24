# -*- coding: utf-8 -*-
"""Módulo base para la ejecución de pineboo.
Librería orientada a emular Eneboo desde python."""
from pineboolib.pnapplication import Project

# project = None
no_python_cache = False


def load_dgi(name):
    """Load a DGI module dynamically."""
    import importlib
    import sys
    import logging

    logger = logging.getLogger("dgi")

    modname = "dgi_%s" % name
    modpath = "pineboolib.plugins.dgi.%s.%s" % (modname, modname)
    try:
        import pineboolib
    except Exception:
        print("Cargando como invitado")
        modpath = "pineboo.%s" % modpath

    try:
        dgi_pymodule = importlib.import_module(modpath)
    except ImportError:
        raise ImportError("No se ha encontrado el módulo DGI %s" % modpath)

    dgi_entrypoint = getattr(dgi_pymodule, modname, None)
    if dgi_entrypoint is None:
        raise ImportError("Fallo al cargar el punto de entrada al módulo DGI %s" % modpath)

    try:
        dgi = dgi_entrypoint()  # FIXME: Necesitamos ejecutar código dinámico tan pronto?
    except Exception:
        logger.exception("Error inesperado al cargar el módulo DGI %s" % modpath)
        sys.exit(32)

    logger.info("DGI loaded: %s", name)

    return dgi


_DGI = load_dgi("qt")
project = Project(_DGI)
