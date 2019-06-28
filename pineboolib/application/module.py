import os.path
import logging

from pineboolib.core.parsetable import parseTable
from .utils.path import _path

# FIXME: parseTable is something too specific to be in utils.py

# For types only:
from .file import File


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
        self.files = {}
        self.tables = {}
        self.loaded = False
        # self.path = pineboolib.project.path  # FIXME: nope.

    def add_project_file(self, fileobj: File) -> None:
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
            try:
                contenido = str(open(_path(tablefile), "rb").read(), "ISO-8859-15")
            except UnicodeDecodeError as e:
                self.logger.error("Error al leer el fichero %s %s", tablefile, e)
                continue
            tableObj = parseTable(name, contenido)
            if tableObj is None:
                self.logger.warning("No se pudo procesar. Se ignora tabla %s/%s ", self.name, name)
                continue
            self.tables[name] = tableObj
            # pineboolib.project.tables[name] = tableObj  # FIXME: nope

        self.loaded = True
        return True
