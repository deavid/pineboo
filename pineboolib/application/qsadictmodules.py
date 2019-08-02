"""
QSADictModules.

Manages read and writting QSA dynamic properties that are loaded during project startup.
"""
from typing import Any
from pineboolib.core.utils import logging
from pineboolib.application.xmlaction import XMLAction
from pineboolib.application.proxy import DelayedObjectProxyLoader

logger = logging.getLogger("qsadictmodules")


class QSADictModules:
    """
    Manage read and write dynamic properties for QSA.
    """

    @classmethod
    def from_project(cls, scriptname: str) -> Any:
        """
        Return project object for given name.
        """
        from pineboolib.qsa import qsa as qsa_dict_modules

        # FIXME: Esto debería estar guardado en Project.
        return getattr(qsa_dict_modules, scriptname, None)

    @classmethod
    def action_exists(cls, scriptname: str) -> bool:
        """
        Check if action is already loaded.
        """
        from pineboolib.qsa import qsa as qsa_dict_modules

        return hasattr(qsa_dict_modules, scriptname)

    @classmethod
    def save_action(cls, scriptname: str, delayed_action: DelayedObjectProxyLoader) -> None:
        """
        Save Action into project for QSA.
        """
        from pineboolib.qsa import qsa as qsa_dict_modules

        setattr(qsa_dict_modules, scriptname, delayed_action)

    @classmethod
    def save_other(cls, scriptname: str, other: Any) -> None:
        """
        Save other objects for QSA.
        """
        from pineboolib.qsa import qsa as qsa_dict_modules

        setattr(qsa_dict_modules, scriptname, other)

    @classmethod
    def save_action_for_root_module(cls, action: XMLAction) -> bool:
        """Save a new module as an action."""

        from pineboolib.qsa import qsa as qsa_dict_modules

        if hasattr(qsa_dict_modules, action.name):
            if action.name != "sys":
                logger.warning("Module found twice, will not be overriden: %s", action.name)
                return False

        # Se crea la action del módulo
        proxy = DelayedObjectProxyLoader(action.load, name="QSA.Module.%s" % action.name)
        cls.save_action(action.name, proxy)
        return True

    @classmethod
    def save_action_for_mainform(cls, action: XMLAction):
        from pineboolib.qsa import qsa as qsa_dict_modules

        name = action.name
        module = action.mod
        if module is None:
            raise ValueError("Action.module must be set before calling")

        if hasattr(qsa_dict_modules, "form%s" % name):
            logger.debug(
                "No se sobreescribe variable de entorno %s. Hay una definición previa en %s",
                "%s.form%s" % (module.module_name, name),
                module.module_name,
            )
            return False
        # Se crea la action del form
        delayed_action = DelayedObjectProxyLoader(action.load, name="QSA.Module.%s.Action.form%s" % (module.module.name, name))
        setattr(qsa_dict_modules, "form" + name, delayed_action)
        return True

    @classmethod
    def save_action_for_formrecord(cls, action: XMLAction):
        from pineboolib.qsa import qsa as qsa_dict_modules

        name = action.name
        module = action.mod
        if module is None:
            raise ValueError("Action.module must be set before calling")

        if hasattr(qsa_dict_modules, "formRecord" + name):
            logger.debug("No se sobreescribe variable de entorno %s", "formRecord" + name)
            return False
        # Se crea la action del formRecord
        delayed_action = DelayedObjectProxyLoader(
            action.formRecordWidget, name="QSA.Module.%s.Action.formRecord%s" % (module.mod.name, name)
        )

        setattr(qsa_dict_modules, "formRecord" + name, delayed_action)
        return True

    @classmethod
    def clean_all(cls):
        from pineboolib.qsa import qsa as qsa_dict_modules

        list_ = [attr for attr in dir(qsa_dict_modules) if not attr[0] == "_"]
        for name in list_:
            att = getattr(qsa_dict_modules, name)
            if isinstance(att, DelayedObjectProxyLoader):
                delattr(qsa_dict_modules, name)
