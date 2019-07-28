# -*- coding: utf-8 -*-
import re
from .utils import logging

logger = logging.getLogger(__name__)


def translate(mod: str, txt: str) -> str:
    # FIXME: qsa_sys is not something we should import here
    return txt


def error_manager(e: str) -> str:
    from .utils.utils_base import filedir

    tmpdir = filedir("../tempdata")
    e = e.replace(tmpdir, "...")
    e = re.sub(r"/[0-9a-f]{35,60}\.qs\.py", ".qs.py", e)

    text = translate("scripts", "Error ejecutando un script")
    text += ":\n%s" % e
    text += process_error(e)
    logger.error(text)
    return text


def process_error(error_str: str) -> str:
    ret = "\n=========== Error Manager =============\n\n"

    if "AttributeError: 'dict' object has no attribute" in error_str:
        error = "AttributeError: 'dict' object has no attribute"
        var = error_str[error_str.find(error) + len(error) + 1 :]
        var = var.replace("\n", "")
        ret += translate("scripts", "La forma correcta de acceder a .%s es [%s].") % (
            var,
            var,
        )

    elif "'builtin_function_or_method' object has no attribute" in error_str:
        error = "'builtin_function_or_method' object has no attribute"
        var = error_str[error_str.find(error) + len(error) + 1 :]
        var = var.replace("\n", "")
        var = var.replace("'", "")
        ret += translate("scripts", "La forma correcta de acceder a .%s es ().%s.") % (
            var,
            var,
        )

    elif "AttributeError: 'ifaceCtx' object has no attribute" in error_str:
        error = "AttributeError: 'ifaceCtx' object has no attribute"
        var = error_str[error_str.find(error) + len(error) + 1 :]
        var = var.replace("\n", "")
        var = var.replace("'", "")
        ret += translate(
            "scripts", "No se ha traducido el script o el script está vacio."
        )
    elif "object is not callable" in error_str:
        error = "object is not callable"
        var = error_str[error_str.find("TypeError") + 10 : error_str.find(error)]
        ret += translate(
            "scripts",
            "Estas llamando a un objeto %s .Los parentesis finales hay que quitarlos."
            % var,
        )
    elif "unsupported operand type(s) for" in error_str:
        error = "unsupported operand type(s) for"
        ret += translate(
            "scripts",
            "No puedes hacer operaciones entre dos 'Nones' o dos tipos diferentes. Revisa el script y controla esto.",
        )
    elif "'QDomElement' object has no attribute 'toString'" in error_str:
        error = "'QDomElement' object has no attribute 'toString'"
        ret += translate(
            "scripts", "toString() ya no está disponible , usa otro método"
        )
    elif "can only concatenate" in error_str:
        error = "can only concatenate"
        ret += translate(
            "scripts",
            "Estas intentado añadir a una cadena de texto un tipo de dato no str.",
        )

    else:
        ret += translate("scripts", "Información no disponible.")

    return ret
