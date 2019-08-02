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
    def save_formrecord(cls, actionname, delayed_action):
        """Store a new formRecord for safe retrieval."""
        cls._formrecord[actionname] = delayed_action

    @classmethod
    def save_mainform(cls, actionname, delayed_action):
        """Store a new main form for safe retrieval."""
        cls._mainform[actionname] = delayed_action

    @classmethod
    def save_root_module(cls, actionname, delayed_action):
        """Store a new root module for safe retrieval."""
        cls._root_module[actionname] = delayed_action
