"""
SafeQSA Module.

Stores methods for safe and typed retrieval of project actions.

"""
from pineboolib.application.proxy import DelayedObjectProxyLoader
from typing import Dict, Optional


class SafeQSA:
    """Store safely project elements for internal Pineboo load."""

    _root_module: Dict[str, DelayedObjectProxyLoader] = {}
    _mainform: Dict[str, DelayedObjectProxyLoader] = {}
    _formrecord: Dict[str, DelayedObjectProxyLoader] = {}

    @classmethod
    def clean_all(cls):
        """Clear all values from internal storage for Pineboo soft-restart."""
        cls._root_module.clear()
        cls._mainform.clear()
        cls._formrecord.clear()

    @classmethod
    def save_formrecord(cls, actionname: str, delayed_action: DelayedObjectProxyLoader) -> None:
        """Store a new formRecord for safe retrieval."""
        cls._formrecord[actionname] = delayed_action

    @classmethod
    def save_mainform(cls, actionname: str, delayed_action: DelayedObjectProxyLoader) -> None:
        """Store a new main form for safe retrieval."""
        cls._mainform[actionname] = delayed_action

    @classmethod
    def save_root_module(cls, actionname: str, delayed_action: DelayedObjectProxyLoader) -> None:
        """Store a new root module for safe retrieval."""
        cls._root_module[actionname] = delayed_action

    @classmethod
    def get_root_module(cls, actionname: str) -> Optional[DelayedObjectProxyLoader]:
        """Get a root module."""
        return cls._root_module.get(actionname, None)

    @classmethod
    def get_mainform(cls, actionname: str) -> Optional[DelayedObjectProxyLoader]:
        """Get a main form."""
        return cls._mainform.get(actionname, None)

    @classmethod
    def get_formrecord(cls, actionname: str) -> Optional[DelayedObjectProxyLoader]:
        """Get a form record."""
        return cls._formrecord.get(actionname, None)

    @classmethod
    def get_any(cls, actionname: str) -> Optional[DelayedObjectProxyLoader]:
        """
        Get an action of any type.

        Avoid using this method unless it is truly needed.
        """
        formrecord = cls._formrecord.get(actionname, None)
        mainform = cls._mainform.get(actionname, None)
        root_module = cls._root_module.get(actionname, None)
        return_value = root_module or mainform or formrecord
        return return_value

    @classmethod
    def root_module(cls, actionname: str) -> DelayedObjectProxyLoader:
        """Get a root module or error out."""
        return cls._root_module[actionname]

    @classmethod
    def mainform(cls, actionname: str) -> DelayedObjectProxyLoader:
        """Get a main form or error out."""
        return cls._mainform[actionname]

    @classmethod
    def formrecord(cls, actionname: str) -> DelayedObjectProxyLoader:
        """Get a form record or error out."""
        return cls._formrecord[actionname]

    @classmethod
    def any(cls, actionname: str) -> DelayedObjectProxyLoader:
        """
        Get an action of any type or error out.

        Avoid using this method unless it is truly needed.
        """
        return_value = cls.get_any(actionname)
        if return_value is None:
            raise ValueError("Action %r does not exist" % actionname)
        return return_value
