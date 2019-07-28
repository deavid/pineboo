from pineboolib import logging
import os.path
from typing import Optional

logger = logging.getLogger(__name__)


def _dir(*x) -> str:
    """
    Calcula la ruta de una carpeta
    @param x. str o array con la ruta de la carpeta
    @return str con ruta absoluta a una carpeta
    """
    from pineboolib.application import project  # type: ignore

    return os.path.join(project.tmpdir, *x)


def coalesce_path(*filenames) -> Optional[str]:
    """
    Retorna el primer fichero existente de un grupo de ficheros
    @return ruta al primer fichero encontrado
    """
    for filename in filenames:
        if filename is None:
            # When the caller specifies None as the last item means that its OK to return None
            return None
        from pineboolib.application import project

        if filename in project.files:

            return project.files[filename].path()
    logger.error(
        "coalesce_path: Ninguno de los ficheros especificados ha sido encontrado en el proyecto: %s",
        repr(filenames),
        stack_info=False,
    )
    return None


def _path(filename: str, showNotFound: bool = True) -> Optional[str]:
    """
    Retorna el primer fichero existente de un grupo de ficheros
    @return ruta al fichero
    """
    from pineboolib.application import project

    if filename not in project.files:
        if showNotFound:
            logger.error(
                "Fichero %s no encontrado en el proyecto.", filename, stack_info=False
            )
        return None
    return project.files[filename].path()
