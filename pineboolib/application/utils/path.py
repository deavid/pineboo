import logging
import os.path

import pineboolib

logger = logging.getLogger(__name__)


def _dir(*x):
    """
    Calcula la ruta de una carpeta
    @param x. str o array con la ruta de la carpeta
    @return str con ruta absoluta a una carpeta
    """
    return os.path.join(pineboolib.project.tmpdir, *x)


def coalesce_path(*filenames):
    """
    Retorna el primer fichero existente de un grupo de ficheros
    @return ruta al primer fichero encontrado
    """
    for filename in filenames:
        if filename is None:
            return None
        if filename in pineboolib.project.files:
            return pineboolib.project.files[filename].path()
    logger.error("Ninguno de los ficheros especificados ha sido encontrado en el proyecto: %s", repr(filenames), stack_info=False)


def _path(filename, showNotFound=True):
    """
    Retorna el primer fichero existente de un grupo de ficheros
    @return ruta al fichero
    """
    if filename not in pineboolib.project.files:
        if showNotFound:
            logger.error("Fichero %s no encontrado en el proyecto.", filename, stack_info=False)
        return None
    return pineboolib.project.files[filename].path()
