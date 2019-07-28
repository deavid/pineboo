"""Manage load and storage of Eneboo/Pineboo modules.

What are modules?
-------------------

Modules are the declaration of Pineboo source packages where all related functionality
is stored within. Its composed of a name and description; and they contain code, forms, etc.
"""

import os.path
from pineboolib.core.utils import logging

from pineboolib.core.parsetable import parseTable
from .utils.path import _path

from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from .file import File
    from pineboolib.core.utils.struct import TableStruct


class Module(object):
    """Esta clase almacena la información de los módulos cargados
    """

    logger = logging.getLogger("application.Module")

    def __init__(self, areaid: str, name: str, description: str, icon: str) -> None:
        """Constructor
        @param areaid. Identificador de area.
        @param name. Nombre del módulo
        @param description. Descripción del módulo
        @param icon. Icono del módulo
        """

        self.areaid = areaid
        self.name = name
        self.description = description  # En python2 era .decode(UTF-8)
        self.icon = icon
        self.files: Dict[str, "File"] = {}
        self.tables: Dict[str, TableStruct] = {}
        self.loaded = False

    def add_project_file(self, fileobj: "File") -> None:
        """Añade ficheros al array que controla que ficehros tengo.
        @param fileobj. Objeto File con información del fichero
        """
        self.files[fileobj.filename] = fileobj

    def load(self) -> bool:
        """Carga las acciones pertenecientes a este módulo
        @return Boolean. True si ok, False si hay problemas
        """
        from .moduleactions import ModuleActions

        pathxml = _path("%s.xml" % self.name)
        # pathui = _path("%s.ui" % self.name)
        if pathxml is None:
            self.logger.error("módulo %s: fichero XML no existe", self.name)
            return False
        # if pathui is None:
        #    self.logger.error("módulo %s: fichero UI no existe", self.name)
        #    return False
        try:
            self.actions = ModuleActions(self, pathxml, self.name)
            self.actions.load()
        except Exception:
            self.logger.exception("Al cargar módulo %s:", self.name)
            return False

        # TODO: Load Main Script:
        self.mainscript = None
        # /-----------------------

        for tablefile in self.files:
            if not tablefile.endswith(".mtd") or tablefile.find("alteredtable") > -1:
                continue
            name, ext = os.path.splitext(tablefile)
            path = _path(tablefile)
            if path is None:
                raise Exception("Cannot find %s" % tablefile)
            try:
                contenido = str(open(path, "rb").read(), "ISO-8859-15")
            except UnicodeDecodeError as e:
                self.logger.error("Error al leer el fichero %s %s", tablefile, e)
                continue
            try:
                tableObj = parseTable(name, contenido)
            except ValueError as e:
                self.logger.warning("No se pudo procesar. Se ignora tabla %s/%s (%s) ", self.name, name, e)
            self.tables[name] = tableObj

        self.loaded = True
        return True
