# # -*- coding: utf-8 -*-
import os
import re
import logging
import sys
import traceback
from io import StringIO
from xml import etree

import pineboolib

from pineboolib.fllegacy.flsettings import FLSettings

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
    if not os.path.exists(filedir("../tempdata")):
        os.mkdir(filedir("../tempdata"))


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


def cacheXPM(value):
    file_name = None
    if value:
        xpm_name = value[:value.find("[]")]
        xpm_name = xpm_name[xpm_name.rfind(" ") + 1:]
        from pineboolib.pncontrolsfactory import aqApp

        cache_dir = filedir("../tempdata/cache/%s/cacheXPM" % aqApp.db().DBName())
        if not os.path.exists(cache_dir):
            os.mkdir(cache_dir)

        file_name = "%s/%s.xpm" % (cache_dir, xpm_name)
        if not os.path.exists(file_name):
            f = open(file_name, "w")
            f.write(value)
            f.close()

    return file_name


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

    obj_name = root.find("name")
    query = root.find("query")
    if query is not None:
        if query.text != nombre:
            logger.warn("WARN: Nombre de query %s no coincide con el nombre declarado en el XML %s (se prioriza el nombre de query)" % (
                obj_name.text, nombre))
            query.text = nombre
    elif obj_name.text != nombre:
        logger.warn("WARN: Nombre de tabla %s no coincide con el nombre declarado en el XML %s (se prioriza el nombre de tabla)" % (
            obj_name.text, nombre))
        obj_name.text = nombre
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
        return "%s" % t
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


DEPENDECIE_CHECKED = []


def checkDependencies(dict_, exit=True):

    from importlib import import_module

    dependences = []
    error = []
    for key in dict_.keys():
        if not key in DEPENDECIE_CHECKED:
            try:
                mod_ = import_module(key)
                mod_ver = None
                if key == "ply":
                    version_check("ply", mod_.__version__, '3.9')
                elif key == "Pillow":
                    version_check("Pillow", mod_.__version__, '5.1.0')
                elif key == "PyQt5.QtCore":
                    version_check("PyQt5", mod_.QT_VERSION_STR, '5.9')
                    mod_ver = mod_.QT_VERSION_STR

                if not mod_ver:
                    mod_ver = getattr(mod_, "__version__", None) or getattr(mod_, "version", "???")

                settings = FLSettings()
                if settings.readBoolEntry("application/isDebuggerMode", False):
                    logger.warn("Versión de %s: %s", key, mod_ver)
            except ImportError:
                dependences.append(dict_[key])
                error.append(traceback.format_exc())

            DEPENDECIE_CHECKED.append(key)

    msg = ""
    if len(dependences) > 0:
        logger.warn("HINT: Dependencias incumplidas:")
        for dep in dependences:
            logger.warn("HINT: Instale el paquete %s" % dep)
            msg += "Instale el paquete %s.\n%s" % (dep, error)

        if exit:
            if getattr(pineboolib.project, "_DGI", None):
                if pineboolib.project._DGI.useDesktop() and pineboolib.project._DGI.localDesktop():
                    try:
                        ret = QtWidgets.QMessageBox.warning(None, "Pineboo - Dependencias Incumplidas -", msg, QtWidgets.QMessageBox.Ok)
                    except Exception:
                        logger.error("No se puede mostrar el diálogo de dependecias incumplidas")

            if not getattr(sys, 'frozen', False):
                sys.exit(32)

    return len(dependences) == 0


def version_check(mod_name, mod_ver, min_ver):
    """Compare two version numbers and raise a warning if "minver" is not met."""
    if version_normalize(mod_ver) < version_normalize(min_ver):
        logger.warn("La version de <%s> es %s. La mínima recomendada es %s.", mod_name, mod_ver, min_ver)


def version_normalize(v):
    """Normalize version string numbers like 3.10.1 so they can be compared."""
    return [int(x) for x in re.sub(r'(\.0+)*$', '', v).split(".")]


def convertFLAction(action):
    if action.name() in pineboolib.project.actions.keys():
        return pineboolib.project.actions[action.name()]
    else:
        return None


def convert2FLAction(action):
    name = None
    if isinstance(action, str):
        name = str
    else:
        name = action.name

    from pineboolib.pncontrolsfactory import aqApp
    return aqApp.db().manager().action(name)


def load2xml(form_path_or_str):
    from xml.etree import ElementTree as ET

    class xml_parser():

        builder_ = None

        def __init__(self):
            self.builder_ = ET.TreeBuilder()

        def start(self, tag, attrs):
            #print("iniciando", tag, attrs)
            ret = self.builder_.start(tag, attrs)

            # for at in ret.items():
            #    print("****", at)
            # print(ret)

            return ret

        def end(self, tag):
            #print("Terminando", tag)
            return self.builder_.end(tag)

        def data(self, data):
            #print("data!!", repr(data))
            self.builder_.data(data)

        def close(self):
            return self.builder_.close()

    try:
        parser = ET.XMLParser(html=0, target=xml_parser())
        if form_path_or_str.find("KugarTemplate") > -1 or form_path_or_str.find("DOCTYPE QUERY_DATA") > -1:
            print(form_path_or_str)
            ret = ET.fromstring(form_path_or_str, parser)
        else:
            ret = ET.parse(form_path_or_str, parser)
    except Exception:
        try:
            parser = ET.XMLParser(html=0, encoding="ISO-8859-15", target=xml_parser())
            if form_path_or_str.find("KugarTemplate") > -1 or form_path_or_str.find("DOCTYPE QUERY_DATA") > -1:
                ret = ET.fromstring(form_path_or_str, parser)
            else:
                ret = ET.parse(form_path_or_str, parser)
            #logger.exception("Formulario %r se cargó con codificación ISO (UTF8 falló)", form_path)
        except Exception:
            logger.exception("Error cargando UI después de intentar con UTF8 y ISO", form_path_or_str)
            ret = None

    return ret


def imFrozen():
    return getattr(sys, 'frozen', False)


"""
copy and paste from http://effbot.org/zone/element-lib.htm#prettyprint
it basically walks your tree and adds spaces and newlines so the tree is
printed in a nice way
"""


def indent(elem, level=0):
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def format_double(d, part_integer, part_decimal):
    from PyQt5 import QtCore
    from pineboolib.pncontrolsfactory import aqApp
    
    if d is "":
        return d
    #import locale
    #p_int = field_meta.partInteger()
    #p_decimal = field_meta.partDecimal()
    comma_ = "."
    d = str(d)
    found_comma = True if d.find(comma_) > -1 else False
    #if aqApp.commaSeparator() == comma_:
    #    d = d.replace(",", "")
    #else:
    #    d = d.replace(".","")
    #    d = d.replace(",",".")

    d = round(float(d), part_decimal)

    str_d = str(d)
    str_integer = str_d[0:str_d.find(comma_)] if str_d.find(comma_) > -1 else str_d
    str_decimal = "" if str_d.find(comma_) == -1 else str_d[str_d.find(comma_) + 1:]

    if part_decimal > 0:
        while part_decimal > len(str_decimal):
            str_decimal += "0"

    
    str_integer = format_int(str_integer, part_integer)
  
    # Fixme: Que pasa cuando la parte entera sobrepasa el limite, se coge el maximo valor o
    ret_ = "%s%s%s" % (str_integer,aqApp.commaSeparator() if found_comma else "", str_decimal if part_decimal > 0 else "")
    return ret_


def format_int(value, part_intenger = None):
    from pineboolib.pncontrolsfactory import aqApp
    str_integer = value
    if value is not None:
        str_integer = "{:,d}".format(int(value))

        if aqApp.commaSeparator() == ",":
            str_integer = str_integer.replace(",",".")
        else:
            str_integer = str_integer.replace(".",",")
    
    return str_integer

def unformat_number(new_str, old_str, type_):
    ret_ = new_str
    if old_str is not None:
    
        if type_ in ("int","uint"):
            new_str = new_str.replace(",","")
            new_str = new_str.replace(".", "")
    
            ret_ = new_str
        
        else:
            end_comma = False
            if new_str.endswith(",") or new_str.endswith("."):
                #Si acaba en coma, lo guardo
                end_comma = True
                
            ret_ = new_str.replace(",","")
            ret_ = ret_.replace(".", "")
            if end_comma:
                ret_ = ret_ + "."
            #else:
            #    comma_pos = old_str.find(".")
            #    if comma_pos > -1:   
            print("Desformateando", new_str, ret_)       
 
        #else:
            #pos_comma = old_str.find(".")
    
            #if pos_comma > -1:
            #    if pos_comma > new_str.find("."):
            #        new_str = new_str.replace(".", "")
                            
            #        ret_ = new_str[0:pos_comma] + "." + new_str[pos_comma:] 
    
    #print("l2", ret_)
    return ret_
    
"""
Convierte diferentes formatos de fecha a QDate
@param date: Fecha a convertir
@return QDate con el valor de la fecha dada 
"""


def convert_to_qdate(date):
    from pineboolib.qsa import Date
    from pineboolib.fllegacy.flutil import FLUtil
    import datetime

    if isinstance(date, Date):
        date = date.date_  # str
    elif isinstance(date, datetime.date):
        date = str(date)

    if isinstance(date, str):
        if "T" in date:
            date = date[:date.find("T")]

        util = FLUtil()
        date = util.dateAMDtoDMA(date) if len(date.split("-")[0]) == 4 else date
        date = QtCore.QDate.fromString(date, "dd-MM-yyyy")

    return date
