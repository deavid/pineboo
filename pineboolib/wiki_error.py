# -*- coding: utf-8 -*-
from pineboolib.core.utils.logging import logging
import re

logger = logging.getLogger(__name__)


def wiki_error(e: str) -> str:
    # FIXME: No hay un nombre mejor? Crea entradas de la wikipedia?
    from pineboolib import pncontrolsfactory
    from pineboolib.application import project

    qsa_sys = pncontrolsfactory.SysType()
    e = e.replace(project.tmpdir, "...")
    e = re.sub(r"/[0-9a-f]{35,60}\.qs\.py", ".qs.py", e)

    text = qsa_sys.translate("scripts", "Error ejecutando un script")
    text += ":\n%s" % e
    text += process_error(e)
    logger.error(text)
    return text


def process_error(error_str: str) -> str:
    from pineboolib import pncontrolsfactory

    qsa_sys = pncontrolsfactory.SysType()
    ret = "\n=========== Wiki error =============\n\n"

    if "AttributeError: 'dict' object has no attribute" in error_str:
        error = "AttributeError: 'dict' object has no attribute"
        var = error_str[error_str.find(error) + len(error) + 1 :]
        var = var.replace("\n", "")
        ret += qsa_sys.translate("scripts", "La forma correcta de acceder a .%s es [%s].") % (var, var)

    elif "'builtin_function_or_method' object has no attribute" in error_str:
        error = "'builtin_function_or_method' object has no attribute"
        var = error_str[error_str.find(error) + len(error) + 1 :]
        var = var.replace("\n", "")
        var = var.replace("'", "")
        ret += qsa_sys.translate("scripts", "La forma correcta de acceder a .%s es ().%s.") % (var, var)

    elif "AttributeError: 'ifaceCtx' object has no attribute" in error_str:
        error = "AttributeError: 'ifaceCtx' object has no attribute"
        var = error_str[error_str.find(error) + len(error) + 1 :]
        var = var.replace("\n", "")
        var = var.replace("'", "")
        ret += qsa_sys.translate("scripts", "No se ha traducido el script o el script está vacio.")
    elif "object is not callable" in error_str:
        error = "object is not callable"
        var = error_str[error_str.find("TypeError") + 10 : error_str.find(error)]
        ret += qsa_sys.translate("scripts", "Estas llamando a un objeto %s .Los parentesis finales hay que quitarlos." % var)
    elif "unsupported operand type(s) for" in error_str:
        error = "unsupported operand type(s) for"
        ret += qsa_sys.translate(
            "scripts", "No puedes hacer operaciones entre dos 'Nones' o dos tipos diferentes. Revisa el script y controla esto."
        )
    elif "'QDomElement' object has no attribute 'toString'" in error_str:
        error = "'QDomElement' object has no attribute 'toString'"
        ret += qsa_sys.translate("scripts", "toString() ya no está disponible , usa otro método")

    else:
        ret += qsa_sys.translate("scripts", "Información no disponible.")

    return ret
