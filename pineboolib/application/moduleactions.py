"""
Genera un arbol con las acciones de los diferentes módulos
@param name. Nombre del la función buscada
@return el objecto del XMLAction afectado
"""


class ModuleActions(object):
    """
    Constructor
    @param module. Identificador del módulo
    @param path. Ruta del módulo
    @param modulename. Nombre del módulo
    """

    def __init__(self, module: Module, path: str, modulename: str) -> None:
        self.mod = module
        self.path = path
        self.module_name = modulename
        self.logger = logging.getLogger("main.ModuleActions")
        if not self.path:
            self.logger.error("El módulo no tiene un path válido %s", self.module_name)

    """
    Carga las actions del módulo en el projecto
    """

    def load(self) -> None:
        # Ojo: Almacena un arbol con los módulos cargados
        from pineboolib import qsa as qsa_dict_modules

        self.tree = pineboolib.utils.load2xml(self.path)
        self.root = self.tree.getroot()

        action = XMLAction()
        action.mod = self
        action.name = self.mod.name
        action.alias = self.mod.name
        # action.form = self.mod.name
        action.form = None
        action.table = None
        action.scriptform = self.mod.name
        pineboolib.project.actions[action.name] = action
        settings = FLSettings()
        if hasattr(qsa_dict_modules, action.name):
            if action.name != "sys":
                if settings.readBoolEntry("application/isDebuggerMode", False):
                    self.logger.warning("No se sobreescribe variable de entorno %s", action.name)
        else:  # Se crea la action del módulo
            setattr(qsa_dict_modules, action.name, DelayedObjectProxyLoader(action.load, name="QSA.Module.%s" % action.name))

        for xmlaction in self.root:
            action_xml = XMLAction(xmlaction)
            action_xml.mod = self
            name = action_xml.name
            if name != "unnamed":
                if hasattr(qsa_dict_modules, "form%s" % name):
                    if settings.readBoolEntry("application/isDebuggerMode", False):
                        self.logger.warning(
                            "No se sobreescribe variable de entorno %s. Hay una definición previa en %s",
                            "%s.form%s" % (self.module_name, name),
                            pineboolib.project.actions[name].mod.module_name,
                        )
                else:  # Se crea la action del form
                    pineboolib.project.actions[name] = action_xml
                    delayed_action = DelayedObjectProxyLoader(action_xml.load, name="QSA.Module.%s.Action.form%s" % (self.mod.name, name))
                    setattr(qsa_dict_modules, "form" + name, delayed_action)

                if hasattr(qsa_dict_modules, "formRecord" + name):
                    self.logger.debug("No se sobreescribe variable de entorno %s", "formRecord" + name)
                else:  # Se crea la action del formRecord
                    delayed_action = DelayedObjectProxyLoader(action_xml.formRecordWidget, name="QSA.Module.%s.Action.formRecord%s" % (self.mod.name, name))

                    setattr(qsa_dict_modules, "formRecord" + name, delayed_action)

    """
    Busca si es propietario de una action
    """

    def __contains__(self, k):
        return k in pineboolib.project.actions

    """
    Recoge una action determinada
    @param name. Nombre de la action
    @return Retorna el XMLAction de la action dada
    """

    def __getitem__(self, name):
        return pineboolib.project.actions[name]

    """
    Añade una action a propiedad del módulo
    @param name. Nombre de la action
    @param action_. Action a añadir a la propiedad del módulo
    """

    def __setitem__(self, name, action_):
        raise NotImplementedError("Actions are not writable!")
        # pineboolib.project.actions[name] = action_
