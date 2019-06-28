# -*- coding: utf-8 -*-
"""Módulo base para la ejecución de pineboo.
Librería orientada a emular Eneboo desde python."""
from .core.utils.utils_base import is_deployed  # noqa: F401
from .application.project import Project

project = Project()
