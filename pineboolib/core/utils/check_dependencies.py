# -*- coding: utf-8 -*-
"""Check application dependencies."""
import sys
import traceback
from typing import Dict, Tuple

from pineboolib.core.utils import logging
from pineboolib.core.utils.version import VersionNumber

ModuleName = str
ModuleVersion = str
SuggestedPackageNameForInstall = str
ErrorString = str

DependencyCheck = Dict[ModuleName, SuggestedPackageNameForInstall]
DependencyError = Dict[Tuple[ModuleName, SuggestedPackageNameForInstall], ErrorString]

logger = logging.getLogger(__name__)
DEPENDENCIES_CHECKED: Dict[ModuleName, ModuleVersion] = {}

MINIMUM_VERSION = {
    "Python": "3.6",
    "ply": "3.9",
    "Pillow": "5.1.0",
    "fpdf": "1.7.3",
    "PyQt5": "5.11",
}
PYTHON_INCLUDED_BATTERIES = {"Python", "sqlite3"}


def get_dependency_errors(dict_: DependencyCheck) -> DependencyError:
    """
    Check if a package is installed and return the result.

    @param dict_. Dict with the name of the agency and the module to be checked.
    @param exit . Exit if dependence fails.
    """

    global DEPENDENCIES_CHECKED
    from importlib import import_module

    error: DependencyError = {}
    for key, suggested_pkg in dict_.items():
        if key in DEPENDENCIES_CHECKED:
            continue
        version = None
        if key in PYTHON_INCLUDED_BATTERIES:
            version = sys.version[: sys.version.find("(")]
        else:
            try:
                mod_ = import_module(key)
                version = getattr(mod_, "__version__", None)
                if key == "PyQt5.QtCore":
                    version = getattr(mod_, "QT_VERSION_STR", None)
                del mod_
            except ImportError:
                error[(key, suggested_pkg)] = traceback.format_exc()
                continue

        if key == "odf":
            from odf import namespaces  # type: ignore

            version = namespaces.__version__

        if key == "barcode":
            import barcode

            version = barcode.version

        if not isinstance(version, str):
            error[(key, suggested_pkg)] = (
                "Error: version detected should be string, but found %r" % version
            )
            continue

        if key in MINIMUM_VERSION:
            VersionNumber.check(key, version, MINIMUM_VERSION[key])

        DEPENDENCIES_CHECKED[key] = version
        logger.debug("Dependency checked %s: %s", key, version)
    return error


def check_dependencies_cli(dict_: DependencyCheck) -> bool:
    """
    Check if a package is installed and return the result.

    @param dict_. Dict with the name of the agency and the module to be checked.
    @param exit . Exit if dependence fails.
    """
    dep_error: DependencyError = get_dependency_errors(dict_)
    if not dep_error:
        return True

    logger.warning("Unmet dependences:")
    for (dep, suggestedpkg), errormsg in dep_error.items():
        logger.warning("... Error trying to import module %s:\n%s", dep, errormsg)
        logger.warning("... Install package %s for %s", suggestedpkg, dep)

    return False
