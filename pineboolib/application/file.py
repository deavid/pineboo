import os.path
from pineboolib.core.utils import logging
from typing import Optional

from .utils.path import _dir


class File(object):
    """
    Clase que gestiona cada uno de los ficheros de un módulo
    """

    logger = logging.getLogger("application.File")

    def __init__(
        self, module: str, filename: str, sha: Optional[str] = None, basedir: Optional[str] = None, db_name: Optional[str] = None
    ) -> None:
        """
        Constructor
        @param module. Identificador del módulo propietario
        @param filename. Nombre del fichero
        @param sha. Código sha1 del contenido del fichero
        @param basedir. Ruta al fichero en cache
        """
        self.module = module
        self.filename = filename
        self.sha = sha
        if filename.endswith(".qs.py"):
            self.ext = ".qs.py"
            self.name = os.path.splitext(os.path.splitext(filename)[0])[0]
        else:
            self.name, self.ext = os.path.splitext(filename)

        if self.sha:
            self.filekey = "%s/%s/file%s/%s/%s%s" % (db_name, module, self.ext, self.name, sha, self.ext)
        else:
            self.filekey = filename
        self.basedir = basedir

    """
    Devuelve la ruta absoluta del fichero
    @return Ruta absoluta del fichero
    """

    def path(self) -> str:
        if self.basedir:
            # Probablemente porque es local . . .
            return _dir(self.basedir, self.filename)
        else:
            # Probablemente es remoto (DB) y es una caché . . .
            return _dir("cache", *(self.filekey.split("/")))
