"""
Application package for resources.

This package holds all functions and classes that are like side resources.
"""
from typing import TYPE_CHECKING, Any

if not TYPE_CHECKING:
    from .projectmodule import Project

    project = Project()
else:
    project: Any  # FIXME: bad idea. Can we move Project() from this file to its own? Or create proper singleton...
