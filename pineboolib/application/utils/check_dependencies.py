import pineboolib
import sys
import logging
import traceback

from pineboolib.core.utils.utils_base import version_check, is_deployed

from typing import Dict

logger = logging.getLogger("application.utils.check_dependencies")
DEPENDENCIES_CHECKED = {}


def check_dependencies(dict_: Dict[str, str], exit: bool = True) -> bool:
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
            if key == "ply":
                version_check(key, mod_.__version__, "3.9")
            if key == "Python":
                version_check(key, sys.version[: sys.version.find("(")], "3.6")
                mod_ver = sys.version[: sys.version.find("(")]
            elif key == "Pillow":
                version_check(key, mod_.__version__, "5.1.0")
            elif key == "fpdf":
                version_check(key, mod_.__version__, "1.7.3")
            elif key == "odf":
                from odf import namespaces

                mod_ver = namespaces.__version__
            elif key == "PyQt5.QtCore":
                version_check("PyQt5", mod_.QT_VERSION_STR, "5.11")
                mod_ver = mod_.QT_VERSION_STR

            if mod_ver is None:
                mod_ver = getattr(mod_, "__version__", None) or getattr(mod_, "version", "???")

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
            if getattr(pineboolib.project, "_DGI", None):
                if pineboolib.project._DGI.useDesktop() and pineboolib.project._DGI.localDesktop():
                    from pineboolib.pncontrolsfactory import QMessageBox

                    QMessageBox.warning(None, "Pineboo - Dependencias Incumplidas -", msg, QMessageBox.Ok)

            if not is_deployed():
                sys.exit(32)

    if key not in DEPENDENCIES_CHECKED.keys():
        DEPENDENCIES_CHECKED[key] = mod_ver

    return len(dependences) == 0
