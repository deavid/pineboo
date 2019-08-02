"""
ModuleActions module.
"""
from pineboolib.core.utils import logging

from pineboolib.core.exceptions import ForbiddenError
from pineboolib.core.utils.utils_base import load2xml
from pineboolib.application.xmlaction import XMLAction
from pineboolib.application.qsadictmodules import QSADictModules

from typing import Any, TYPE_CHECKING, NoReturn


class ModuleActions(object):
    """
    Generate tree with actions from modules.
    """

    logger = logging.getLogger("application.ModuleActions")

    def __init__(self, module: Any, path: str, modulename: str) -> None:
        """
        Constructor.

        @param module. Identificador del módulo
        @param path. Ruta del módulo
        @param modulename. Nombre del módulo
        """
        if TYPE_CHECKING:
            # To avoid circular dependency on pytype
            self.project = module
        else:
            from pineboolib.application import project  # FIXME?

            self.project = project
        self.mod = module  # application.Module
        self.path = path
        self.module_name = modulename
        if not self.path:
            self.logger.error("El módulo no tiene un path válido %s", self.module_name)

    def load(self) -> None:
        """Load module actions into project."""
        # Ojo: Almacena un arbol con los módulos cargados

        self.tree = load2xml(self.path)
        self.root = self.tree.getroot()

        action = XMLAction(project=self.project, name=self.mod.name)
        if action is None:
            raise Exception("action is empty!")

        action.mod = self
        action.alias = self.mod.name
        # action.form = self.mod.name
        action.form = None
        action.table = None
        action.scriptform = self.mod.name
        self.project.actions[action.name] = action  # FIXME: Actions should be loaded to their parent, not the singleton
        QSADictModules.save_action_for_root_module(action)

        for xmlaction in self.root:
            action_xml = XMLAction(xmlaction, project=self.project)
            action_xml.mod = self
            name = action_xml.name
            if not name or name == "unnamed":
                continue

            if QSADictModules.save_action_for_mainform(action_xml):
                self.project.actions[name] = action_xml  # FIXME: Actions should be loaded to their parent, not the singleton

            QSADictModules.save_action_for_formrecord(action_xml)

    def __contains__(self, k) -> bool:
        """Determine if it is the owner of an action."""
        return k in self.project.actions  # FIXME: Actions should be loaded to their parent, not the singleton

    def __getitem__(self, name) -> Any:
        """
        Retrieve particular action by name.

        @param name. Nombre de la action
        @return Retorna el XMLAction de la action dada
        """
        return self.project.actions[name]  # FIXME: Actions should be loaded to their parent, not the singleton

    def __setitem__(self, name, action_) -> NoReturn:
        """
        Add action to a module property.

        @param name. Nombre de la action
        @param action_. Action a añadir a la propiedad del módulo
        """
        raise ForbiddenError("Actions are not writable!")
        # self.project.actions[name] = action_
