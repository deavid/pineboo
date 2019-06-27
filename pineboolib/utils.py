# -*- coding: utf-8 -*-
import os
import logging
import sys
import traceback

from .utils_base import (  # noqa: F401  # FIXME: Code should import from utils_base when needed.
    auto_qt_translate_text,
    aqtt,
    one,
    Struct,
    XMLStruct,
    DefFun,
    traceit,
    TraceBlock,
    trace_function,
    downloadManager,
    copy_dir_recursive,
    text2bool,
    getTableObj,
    ustr,
    ustr1,
    StructMyDict,
    version_check,
    version_normalize,
    convert2FLAction,
    load2xml,
    parse_for_duplicates,
    indent,
    format_double,
    format_int,
    unformat_number,
    convert_to_qdate,
    resolve_pagination,
    resolve_query,
    resolve_order_params,
    resolve_where_params,
    get_tipo_aqnext,
    create_dict,
    is_deployed,
    filedir,
    download_files,
    parseTable,  # FIXME: parseTable is something too specific to be in utils.py
)
import pineboolib
from pineboolib.fllegacy.flsettings import FLSettings

logger = logging.getLogger(__name__)


def _dir(*x):
    """
    Calcula la ruta de una carpeta
    @param x. str o array con la ruta de la carpeta
    @return str con ruta absoluta a una carpeta
    """
    return os.path.join(pineboolib.project.tmpdir, *x)


def coalesce_path(*filenames):
    """
    Retorna el primer fichero existente de un grupo de ficheros
    @return ruta al primer fichero encontrado
    """
    for filename in filenames:
        if filename is None:
            return None
        if filename in pineboolib.project.files:
            return pineboolib.project.files[filename].path()
    logger.error("Ninguno de los ficheros especificados ha sido encontrado en el proyecto: %s", repr(filenames), stack_info=False)


def _path(filename, showNotFound=True):
    """
    Retorna el primer fichero existente de un grupo de ficheros
    @return ruta al fichero
    """
    if filename not in pineboolib.project.files:
        if showNotFound:
            logger.error("Fichero %s no encontrado en el proyecto.", filename, stack_info=False)
        return None
    return pineboolib.project.files[filename].path()


def cacheXPM(value):
    file_name = None
    if value:
        xpm_name = value[: value.find("[]")]
        xpm_name = xpm_name[xpm_name.rfind(" ") + 1 :]
        from pineboolib.pncontrolsfactory import aqApp

        cache_dir = "%s/cache/%s/cacheXPM" % (aqApp.tmp_dir(), aqApp.db().DBName())
        if not os.path.exists(cache_dir):
            os.mkdir(cache_dir)

        if value.find("cacheXPM") > -1:
            file_name = value
        else:
            file_name = "%s/%s.xpm" % (cache_dir, xpm_name)

        if not os.path.exists(file_name) or FLSettings().readBoolEntry("ebcomportamiento/no_img_cached", False):
            f = open(file_name, "w")
            f.write(value)
            f.close()

    return file_name


def saveGeometryForm(name, geo):
    """
    Guarda la geometría de una ventana
    @param name, Nombre de la ventana
    @param geo, QSize con los valores de la ventana
    """
    from pineboolib.pncontrolsfactory import aqApp

    name = "geo/%s/%s" % (aqApp.db().DBName(), name)
    FLSettings().writeEntry(name, geo)


def loadGeometryForm(name):
    """
    Carga la geometría de una ventana
    @param name, Nombre de la ventana
    @return QSize con los datos de la geometríca de la ventana guardados.
    """
    from pineboolib.pncontrolsfactory import aqApp

    name = "geo/%s/%s" % (aqApp.db().DBName(), name)
    return FLSettings().readEntry(name, None)


DEPENDENCIES_CHECKED = {}


def checkDependencies(dict_, exit=True):

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


def convertFLAction(action):
    if action.name() in pineboolib.project.actions.keys():
        return pineboolib.project.actions[action.name()]
    else:
        return None
