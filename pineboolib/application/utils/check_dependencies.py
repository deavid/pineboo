# -*- coding: utf-8 -*-
"""Check the application dependencies."""

import sys
from pineboolib.core.utils import logging
import traceback

from pineboolib.core.utils.utils_base import version_check, is_deployed
from pineboolib.application import project
from typing import Dict

logger = logging.getLogger("application.utils.check_dependencies")
DEPENDENCIES_CHECKED: Dict[str, str] = {}


def check_dependencies(dict_: Dict[str, str], exit: bool = True) -> bool:
    """
    Check if a package is installed and return the result.

    @param dict_. Dictated with the name of the agency and the module to be checked.
    @param exit . Exit if dependence fails.
    """

    global DEPENDENCIES_CHECKED
    from importlib import import_module

    dependences = []
    error = []
    mod_ver = None
    mod_ = None
    for key in dict_.keys():

        try:
            if key != "Python":
                mod_ = import_module(key)
                version = getattr(mod_, "__version__", None)
            else:
                mod_ = None
                version = None
                version_check(key, sys.version[: sys.version.find("(")], "3.6")
                mod_ver = sys.version[: sys.version.find("(")]
            if key == "ply":
                version_check(key, version, "3.9")
            elif key == "Pillow":
                version_check(key, version, "5.1.0")
            elif key == "fpdf":
                version_check(key, version, "1.7.3")
            elif key == "odf":
                from odf import namespaces  # type: ignore

                mod_ver = namespaces.__version__
            elif key == "PyQt5.QtCore":
                version = getattr(mod_, "QT_VERSION_STR", None)
                version_check("PyQt5", version, "5.11")
                mod_ver = version

            if mod_ver is None:
                mod_ver = version or getattr(mod_, "version", "???")

            # settings = FLSettings()
            # if settings.readBoolEntry("application/isDebuggerMode", False):
            # if not key in DEPENDENCIES_CHECKED.keys():
            #    logger.warning("Versión de %s: %s", key, mod_ver)
        except ImportError:
            dependences.append(dict_[key])
            # print(traceback.format_exc())
            error.append(traceback.format_exc())

        msg = ""
        if len(dependences) > 0 and key not in DEPENDENCIES_CHECKED.keys():
            logger.warning("HINT: Dependencias incumplidas:")
            for dep in dependences:
                logger.warning("HINT: Instale el paquete %s" % dep)
                msg += "Instale el paquete %s.\n%s" % (dep, error)
                if dep == "pyfpdf":
                    msg += "\n\n\n Use pip3 install -i https://test.pypi.org/simple/ pyfpdf==1.7.3"

            if exit:
                if project.DGI.useDesktop() and project.DGI.localDesktop():
                    from pineboolib import pncontrolsfactory

                    pncontrolsfactory.QMessageBox.warning(
                        None, "Pineboo - Dependencias Incumplidas -", msg, pncontrolsfactory.QMessageBox.Ok
                    )

                if not is_deployed():
                    sys.exit(32)

    return len(dependences) == 0
