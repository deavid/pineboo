import logging

from pineboolib.core.utils.utils_base import load2xml
from pineboolib.application.xmlaction import XMLAction

from .module import Module
from .proxy import DelayedObjectProxyLoader


class ModuleActions(object):
    """Genera un arbol con las acciones de los diferentes módulos
    @param name. Nombre del la función buscada
    @return el objecto del XMLAction afectado
    """

    logger = logging.getLogger("main.ModuleActions")

    def __init__(self, module: Module, path: str, modulename: str) -> None:
        """Constructor
        @param module. Identificador del módulo
        @param path. Ruta del módulo
        @param modulename. Nombre del módulo
        """
        self.mod = module
        self.path = path
        self.module_name = modulename
        if not self.path:
            self.logger.error("El módulo no tiene un path válido %s", self.module_name)

    def load(self) -> None:
        """Carga las actions del módulo en el projecto
        """
        # Ojo: Almacena un arbol con los módulos cargados
        from pineboolib import qsa as qsa_dict_modules
        from pineboolib import project

        self.tree = load2xml(self.path)
        self.root = self.tree.getroot()

        action = XMLAction(project=project)
        action.mod = self
        action.name = self.mod.name
        action.alias = self.mod.name
        # action.form = self.mod.name
        action.form = None
        action.table = None
        action.scriptform = self.mod.name
        project.actions[action.name] = action  # FIXME: Actions should be loaded to their parent, not the singleton
        # settings = FLSettings()  # FIXME: Nope
        if hasattr(qsa_dict_modules, action.name):
            if action.name != "sys":
                self.logger.warning("No se sobreescribe variable de entorno %s", action.name)
        else:  # Se crea la action del módulo
            setattr(qsa_dict_modules, action.name, DelayedObjectProxyLoader(action.load, name="QSA.Module.%s" % action.name))

        for xmlaction in self.root:
            action_xml = XMLAction(xmlaction, project=project)
            action_xml.mod = self
            name = action_xml.name
            if name != "unnamed":
                if hasattr(qsa_dict_modules, "form%s" % name):
                    self.logger.warning(
                        "No se sobreescribe variable de entorno %s. Hay una definición previa en %s",
                        "%s.form%s" % (self.module_name, name),
                        self.module_name,
                    )
                else:  # Se crea la action del form
                    project.actions[name] = action_xml  # FIXME: Actions should be loaded to their parent, not the singleton
                    delayed_action = DelayedObjectProxyLoader(action_xml.load, name="QSA.Module.%s.Action.form%s" % (self.mod.name, name))
                    setattr(qsa_dict_modules, "form" + name, delayed_action)

                if hasattr(qsa_dict_modules, "formRecord" + name):
                    self.logger.debug("No se sobreescribe variable de entorno %s", "formRecord" + name)
                else:  # Se crea la action del formRecord
                    delayed_action = DelayedObjectProxyLoader(
                        action_xml.formRecordWidget, name="QSA.Module.%s.Action.formRecord%s" % (self.mod.name, name)
                    )

                    setattr(qsa_dict_modules, "formRecord" + name, delayed_action)

    def __contains__(self, k):
        """Busca si es propietario de una action
        """
        from pineboolib import project

        return k in project.actions  # FIXME: Actions should be loaded to their parent, not the singleton

    def __getitem__(self, name):
        """Recoge una action determinada
        @param name. Nombre de la action
        @return Retorna el XMLAction de la action dada
        """
        from pineboolib import project

        return project.actions[name]  # FIXME: Actions should be loaded to their parent, not the singleton

    """
    Añade una action a propiedad del módulo
    @param name. Nombre de la action
    @param action_. Action a añadir a la propiedad del módulo
    """

    def __setitem__(self, name, action_):
        raise NotImplementedError("Actions are not writable!")
        # pineboolib.project.actions[name] = action_
