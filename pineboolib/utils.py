# # -*- coding: utf-8 -*-
import os
import re
import logging
import sys
import traceback
from io import StringIO
from xml import etree

import pineboolib

from pineboolib.fllegacy.FLSettings import FLSettings

logger = logging.getLogger(__name__)


def auto_qt_translate_text(text):
    """ función utilizada para eliminar los QT_TRANSLATE de eneboo. Esta función ahora mismo no traduce nada."""
    if not isinstance(text, str):
        text = str(text)

    if isinstance(text, str):
        if text.find("QT_TRANSLATE") != -1:
            match = re.search(r"""QT_TRANSLATE\w*\(.+,["'](.+)["']\)""", text)
            if match:
                text = match.group(1)
    return text


aqtt = auto_qt_translate_text


"""  
filedir(path1[, path2, path3 , ...])
@param array de carpetas de la ruta
@return devuelve la ruta absoluta resultado de concatenar los paths que se le pasen y aplicarlos desde la ruta del proyecto.
Es útil para especificar rutas a recursos del programa.
"""


def filedir(*path):
    base_dir = getattr(pineboolib, "base_dir", None)
    if not base_dir:
        base_dir = os.path.dirname(__file__)

        if getattr(sys, 'frozen', False):
            if base_dir.startswith(":"):
                base_dir = ".%s" % base_dir[1:]

    ruta_ = os.path.realpath(os.path.join(base_dir, *path))
    return ruta_


"""
Calcula la ruta de una carpeta
@param x. str o array con la ruta de la carpeta
@return str con ruta absoluta a una carpeta
"""


def _dir(*x):
    return os.path.join(pineboolib.project.tmpdir, *x)


"""
Retorna el primer fichero existente de un grupo de ficheros
@return ruta al primer fichero encontrado
"""


def coalesce_path(*filenames):
    for filename in filenames:
        if filename is None:
            return None
        if filename in pineboolib.project.files:
            return pineboolib.project.files[filename].path()
    logger.error("Ninguno de los ficheros especificados ha sido encontrado en el proyecto: %s",
                 repr(filenames), stack_info=False)


"""
Retorna el primer fichero existente de un grupo de ficheros
@return ruta al fichero
"""


def _path(filename, showNotFound=True):
    if filename not in pineboolib.project.files:
        if showNotFound:
            logger.error("Fichero %s no encontrado en el proyecto.", filename, stack_info=False)
        return None
    return pineboolib.project.files[filename].path()


def one(x, default=None):
    """ Se le pasa una lista de elementos (normalmente de un xml) y devuelve el primero o None; sirve para ahorrar try/excepts y limpiar código"""
    try:
        return x[0]
    except IndexError:
        return default


class Struct(object):
    """
        Plantilla básica de objeto. Asigna sus propiedades en el __init__.
        Especialmente útil para bocetar clases al vuelo.
    """

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class XMLStruct(Struct):
    """
        Plantilla de objeto que replica el contenido de un xml. Sirve para tener rápidamente un objeto
        que sea idéntico al xml que se pueda acceder fácilmente por propiedades.
    """

    def __init__(self, xmlobj=None):
        self._attrs = []
        if xmlobj is not None:
            self.__name__ = xmlobj.tag
            for child in xmlobj:
                if child.tag == "property":
                    # Se importa aquí para evitar error de importación cíclica.
                    from pineboolib.pnqt3ui import loadProperty

                    key, text = loadProperty(child)
                else:
                    text = aqtt(child.text)
                    key = child.tag
                if isinstance(text, str):
                    text = text.strip()
                try:
                    setattr(self, key, text)
                    self._attrs.append(key)
                except Exception:
                    print("utils.XMLStruct: Omitiendo",
                          self.__name__, key, text)

    def __str__(self):
        attrs = ["%s=%s" % (k, repr(getattr(self, k))) for k in self._attrs]
        txtattrs = " ".join(attrs)
        return "<%s.%s %s>" % (self.__class__.__name__, self.__name__, txtattrs)

    def _v(self, k, default=None):
        return getattr(self, k, default)


class DefFun:
    """
        Emuladores de funciones por defecto.
        Tiene una doble funcionalidad. Por un lado, permite convertir llamadas a propiedades en llamadas a la función de verdad.
        Por otro, su principal uso, es omitir las llamadas a funciones inexistentes, de forma que nos advierta en consola
        pero que el código se siga ejecutando. (ESTO ES PELIGROSO)
    """

    def __init__(self, parent, funname, realfun=None):
        self.parent = parent
        self.funname = funname
        self.realfun = None

    def __str__(self):
        if self.realfun:
            logger.debug("%r: Redirigiendo Propiedad a función %r",
                         self.parent.__class__.__name__, self.funname)
            return self.realfun()

        logger.debug("WARN: %r: Propiedad no implementada %r",
                     self.parent.__class__.__name__, self.funname)
        return 0

    def __call__(self, *args):
        if self.realfun:
            logger.debug("%r: Redirigiendo Llamada a función %s %s",
                         self.parent.__class__.__name__, self.funname, args)
            return self.realfun(*args)

        logger.debug("%r: Método no implementado %s %s",
                     self.parent.__class__.__name__, self.funname.encode("UTF-8"), args)
        return None


def traceit(frame, event, arg):
    """Print a trace line for each Python line executed or call.

    This function is intended to be the callback of sys.settrace.
    """
    import linecache
    # if event != "line":
    #    return traceit
    try:
        lineno = frame.f_lineno
        filename = frame.f_globals["__file__"]
        # if "pineboo" not in filename:
        #     return traceit
        if (filename.endswith(".pyc") or
                filename.endswith(".pyo")):
            filename = filename[:-1]
        name = frame.f_globals["__name__"]
        line = linecache.getline(filename, lineno)
        print("%s:%s:%s %s" % (name, lineno, event, line.rstrip()))
    except Exception:
        pass
    return traceit


class TraceBlock():
    def __enter__(self):
        sys.settrace(traceit)
        return traceit

    def __exit__(self, type, value, traceback):
        sys.settrace(None)


def trace_function(f):
    def wrapper(*args):
        with TraceBlock():
            return f(*args)
    return wrapper


from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QObject, QFileInfo, QFile, QIODevice, QUrl, QByteArray,\
    QDir
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkReply,\
    QNetworkRequest


class downloadManager(QObject):
    manager = None
    currentDownload = None
    reply = None
    url = None
    result = None
    filename = None
    dir_ = None
    url_ = None

    def __init__(self):
        super(downloadManager, self).__init__()
        self.manager = QNetworkAccessManager()
        self.currentDownload = []
        self.manager.finished.connect(self.downloadFinished)

    def setLE(self, filename, dir_, urllineedit):
        self.filename = filename
        self.dir_ = dir_
        self.url_ = urllineedit

    def doDownload(self):
        request = QNetworkRequest(QUrl("%s/%s/%s" % (self.url_.text(), self.dir_, self.filename)))
        self.reply = self.manager.get(request)
        # self.reply.sslErrors.connect(self.sslErrors)
        self.currentDownload.append(self.reply)

    def saveFileName(self, url):
        path = url.path()
        basename = QFileInfo(path).fileName()

        if not basename:
            basename = "download"

        if QFile.exists(basename):
            i = 0
            basename = basename + "."
            while QFile.exists("%s%s" % (basename, i)):
                i = i + 1

            basename = "%s%s" % (basename, i)

        return basename

    def saveToDisk(self, filename, data):
        fi = "%s/%s" % (self.dir_, filename)
        if not os.path.exists(self.dir_):
            os.makedirs(self.dir_)
        file = QFile(fi)
        if not file.open(QIODevice.WriteOnly):
            return False

        file.write(data.readAll())
        file.close()

        return True

    def isHttpRedirect(self, reply):
        statusCode = reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)
        return statusCode in [301, 302, 303, 305, 307, 308]

    @QtCore.pyqtSlot(QNetworkReply)
    def downloadFinished(self, reply):
        url = reply.url()
        if not reply.error():
            if not self.isHttpRedirect(reply):
                filename = self.saveFileName(url)
                filename = filename.replace(":", "")
                self.saveToDisk(filename, reply)
                self.result = "%s ---> %s/%s" % (url, self.dir_, filename)
            else:
                self.result = "Redireccionado ... :("
        else:
            self.result = reply.errorString()


def download_files():
    import sysconfig
    from PyQt5.QtWidgets import (QApplication, QLabel, QTreeView, QVBoxLayout,
                                 QWidget)

    dir_ = filedir("forms")
    if os.path.exists(dir_):
        return

    copy_dir_recursive(":/pineboolib", filedir("../pineboolib"))
    copy_dir_recursive(":/share", filedir("../share"))


def copy_dir_recursive(from_dir, to_dir, replace_on_conflict=False):
    dir = QDir()
    dir.setPath(from_dir)

    from_dir += QDir.separator()
    to_dir += QDir.separator()

    if not os.path.exists(to_dir):
        os.makedirs(to_dir)

    for file_ in dir.entryList(QDir.Files):
        from_ = from_dir + file_
        to_ = to_dir + file_
        if str(to_).endswith(".src"):
            to_ = str(to_).replace(".src", "")

        if os.path.exists(to_):
            if replace_on_conflict:
                if not QFile.remove(to_):
                    return False
            else:
                continue

        if not QFile.copy(from_, to_):
            return False

    for dir_ in dir.entryList(QDir.Dirs | QDir.NoDotAndDotDot):
        from_ = from_dir + dir_
        to_ = to_dir + dir_

        if not os.path.exists(to_):
            os.makedirs(to_)

        if not copy_dir_recursive(from_, to_, replace_on_conflict):
            return False

    return True


def clearXPM(text):
    v = text
    if v.find("{"):
        v = v[v.find("{") + 3:]
        v = v[:v.find("};") + 1]
        v = v.replace("\n", "")
        v = v.replace("\t", "    ")
    v = v.split('","')
    return v


def text2bool(text):
    text = str(text).strip().lower()
    if text.startswith("t"):
        return True
    if text.startswith("f"):
        return False

    if text.startswith("y"):
        return True
    if text.startswith("n"):
        return False

    if text.startswith("1"):
        return True
    if text.startswith("0"):
        return False

    if text == "on":
        return True
    if text == "off":
        return False

    if text.startswith("s"):
        return True
    raise ValueError("Valor booleano no comprendido '%s'" % text)


def parseTable(nombre, contenido, encoding="UTF-8", remove_blank_text=True):
    file_alike = StringIO(contenido)

    # parser = etree.XMLParser(
    #    ns_clean=True,
    #    encoding=encoding,
    #    recover=False,
    #    remove_blank_text=remove_blank_text,
    #)
    try:
        #tree = etree.parse(file_alike, parser)
        tree = etree.ElementTree.parse(file_alike)
    except Exception as e:
        print("Error al procesar tabla:", nombre)
        print(traceback.format_exc())
        return None
    root = tree.getroot()

    objname = root.find("name")
    query = root.find("query")
    if query:
        if query[-1].text != nombre:
            print("WARN: Nombre de query %s no coincide con el nombre declarado en el XML %s (se prioriza el nombre de query)" % (
                objname.text, nombre))
            query[-1].text = nombre
    elif objname.text != nombre:
        print("WARN: Nombre de tabla %s no coincide con el nombre declarado en el XML %s (se prioriza el nombre de tabla)" % (
            objname.text, nombre))
        objname.text = nombre
    return getTableObj(tree, root)


def getTableObj(tree, root):
    table = Struct()
    table.xmltree = tree
    table.xmlroot = root
    query_name = None
    if table.xmlroot.find("query"):
        query_name = one(table.xmlroot.find("query").text, None)
    name = table.xmlroot.find("name").text
    table.tablename = name
    if query_name:
        table.name = query_name
        table.query_table = name
    else:
        table.name = name
        table.query_table = None
    table.fields = []
    table.pk = []
    table.fields_idx = {}
    return table


"""
Guarda la geometría de una ventana
@param name, Nombre de la ventana
@param geo, QSize con los valores de la ventana
"""


def saveGeometryForm(name, geo):
    name = "geo/%s" % name
    FLSettings().writeEntry(name, geo)


"""
Carga la geometría de una ventana
@param name, Nombre de la ventana
@return QSize con los datos de la geometríca de la ventana guardados.
"""


def loadGeometryForm(name):
    name = "geo/%s" % name
    return FLSettings().readEntry(name, None)


def ustr(*t1):

    return "".join([ustr1(t) for t in t1])


def ustr1(t):
    if isinstance(t, str):
        return t

    if isinstance(t, float):
        try:
            t = int(t)
        except Exception:
            pass

    # if isinstance(t, QtCore.QString): return str(t)
    if isinstance(t, str):
        return str(t, "UTF-8")
    try:
        return str(t)
    except Exception as e:
        logger.exception("ERROR Coercing to string: %s", repr(t))
        return None


class StructMyDict(dict):

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError as e:
            raise AttributeError(e)

    def __setattr__(self, name, value):
        self[name] = value


def checkDependencies(dict_):

    from importlib import import_module

    dependences = []
    error = []
    for key in dict_.keys():
        try:
            mod_ = import_module(key)
            if key == "PIL":
                v = mod_.__version__

            if key == "ply":
                version_check("ply", mod_.__version__, '3.9')

            if key == "Pillow":
                version_check("Pillow", mod_.__version__, '5.1.0')
            if key == "PyQt5.QtCore":
                version_check("PyQt5", mod_.QT_VERSION_STR, '5.9')

        except ImportError:
            dependences.append(dict_[key])
            error.append(traceback.format_exc())

    msg = ""
    if len(dependences) > 0:
        logger.warn("HINT: Dependencias incumplidas:")
        for dep in dependences:
            logger.warn("HINT: Instale el paquete %s e intente de nuevo" % dep)
            msg += "Instale el paquete %s.\n%s" % (dep, error)

        if getattr(pineboolib.project, "_DGI", None):
            if not getattr(sys, 'frozen', False):
                msg += "\nEl programa se cerrará ahora."
            if pineboolib.project._DGI.useDesktop() and pineboolib.project._DGI.localDesktop():
                ret = QtWidgets.QMessageBox.warning(
                    QtWidgets.QWidget(), "Pineboo - Dependencias Incumplidas -", msg, QtWidgets.QMessageBox.Ok)

        if not getattr(sys, 'frozen', False):
            sys.exit(32)


def version_check(modname, modver, minver):
    """Compare two version numbers and raise a warning if "minver" is not met."""
    if version_normalize(modver) < version_normalize(minver):
        logger.warn(
            "La version de <%s> es %s. La mínima recomendada es %s.", modname, modver, minver)


def version_normalize(v):
    """Normalize version string numbers like 3.10.1 so they can be compared."""
    return [int(x) for x in re.sub(r'(\.0+)*$', '', v).split(".")]


def convertFLAction(action):
    if action.name() in pineboolib.project.actions.keys():
        return pineboolib.project.actions[action.name()]
    else:
        return None
