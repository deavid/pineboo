"""
SafeQSA Module.

Stores methods for safe and typed retrieval of project actions.

"""
from pineboolib.application.proxy import DelayedObjectProxyLoader
from typing import Dict


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
    def get_root_module(cls, actionname: str) -> DelayedObjectProxyLoader:
        """Get a root module."""
        return cls._root_module[actionname]

    @classmethod
    def get_mainform(cls, actionname: str) -> DelayedObjectProxyLoader:
        """Get a main form."""
        return cls._mainform[actionname]

    @classmethod
    def get_formrecord(cls, actionname: str) -> DelayedObjectProxyLoader:
        """Get a form record."""
        return cls._formrecord[actionname]
