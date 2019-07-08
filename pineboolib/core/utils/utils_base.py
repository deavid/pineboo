# # -*- coding: utf-8 -*-
import os
import re
import sys
import io
from PyQt5 import QtCore  # type: ignore
from PyQt5.QtGui import QPixmap  # type: ignore
from PyQt5.QtCore import QObject, QFileInfo, QFile, QIODevice, QUrl, QDir  # type: ignore
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest  # type: ignore

from typing import Optional, Union, Any, List
from xml.etree.ElementTree import ElementTree
from . import logging

from typing import Callable, Dict, Iterable, Sized, TypeVar

_T0 = TypeVar("_T0")
_T1 = TypeVar("_T1")
_T2 = TypeVar("_T2")
_T3 = TypeVar("_T3")

logger = logging.getLogger(__name__)

# FIXME: Move commaSeparator to Pineboo internals, not aqApp
decimal_separator = ","  # FIXME: Locale dependent. ES: "," EN: "."


def auto_qt_translate_text(text: Optional[str]) -> str:
    """ función utilizada para eliminar los QT_TRANSLATE de eneboo. Esta función ahora mismo no traduce nada."""
    if not isinstance(text, str):
        text = str(text)

    if isinstance(text, str):
        if text.find("QT_TRANSLATE") != -1:
            match = re.search(r"""QT_TRANSLATE\w*\(.+,["'](.+)["']\)""", text)
            text = match.group(1) if match else ""

    return text


aqtt = auto_qt_translate_text


def one(x: List[Any], default=None):
    """ Se le pasa una lista de elementos (normalmente de un xml) y devuelve el primero o None;
    sirve para ahorrar try/excepts y limpiar código"""
    try:
        return x[0]
    except IndexError:
        return default


class DefFun:
    """
        Emuladores de funciones por defecto.
        Tiene una doble funcionalidad. Por un lado, permite convertir llamadas a propiedades en llamadas a la función de verdad.
        Por otro, su principal uso, es omitir las llamadas a funciones inexistentes, de forma que nos advierta en consola
        pero que el código se siga ejecutando. (ESTO ES PELIGROSO)
    """

    def __init__(self, parent: Any, funname: str, realfun: None = None) -> None:
        self.parent = parent
        self.funname = funname
        self.realfun = None

    def __str__(self) -> Any:
        if self.realfun:
            logger.debug("%r: Redirigiendo Propiedad a función %r", self.parent.__class__.__name__, self.funname)
            return self.realfun()

        logger.debug("WARN: %r: Propiedad no implementada %r", self.parent.__class__.__name__, self.funname)
        return 0

    def __call__(self, *args) -> Any:
        if self.realfun:
            logger.debug("%r: Redirigiendo Llamada a función %s %s", self.parent.__class__.__name__, self.funname, args)
            return self.realfun(*args)

        logger.debug("%r: Método no implementado %s %s", self.parent.__class__.__name__, self.funname.encode("UTF-8"), args)
        return None


def traceit(frame, event, arg) -> Callable[[Any, Any, Any], Any]:
    """Print a trace line for each Python line executed or call.

    This function is intended to be the callback of sys.settrace.
    """

    # if event != "line":
    #    return traceit
    try:
        import linecache

        lineno = frame.f_lineno
        filename = frame.f_globals["__file__"]
        # if "pineboo" not in filename:
        #     return traceit
        if filename.endswith(".pyc") or filename.endswith(".pyo"):
            filename = filename[:-1]
        name = frame.f_globals["__name__"]
        line = linecache.getline(filename, lineno)
        print("%s:%s:%s %s" % (name, lineno, event, line.rstrip()))
    except Exception:
        pass
    return traceit


class TraceBlock:
    def __enter__(self) -> Callable[[Any, Any, Any], Any]:
        sys.settrace(traceit)
        return traceit

    def __exit__(self, type, value, traceback) -> None:
        sys.settrace(None)


def trace_function(f: Callable) -> Callable:
    def wrapper(*args):
        with TraceBlock():
            return f(*args)

    return wrapper


class downloadManager(QObject):  # FIXME: PLZ follow python naming PEP8
    manager = None
    currentDownload = None
    reply = None
    url = None
    result = None
    filename = None
    dir_ = None
    url_ = None

    def __init__(self) -> None:
        super(downloadManager, self).__init__()
        self.manager = QNetworkAccessManager()
        self.currentDownload = []
        self.manager.finished.connect(self.downloadFinished)

    def setLE(self, filename, dir_, urllineedit) -> None:
        self.filename = filename
        self.dir_ = dir_
        self.url_ = urllineedit

    def doDownload(self) -> None:
        request = QNetworkRequest(QUrl("%s/%s/%s" % (self.url_.text(), self.dir_, self.filename)))
        self.reply = self.manager.get(request)
        # self.reply.sslErrors.connect(self.sslErrors)
        self.currentDownload.append(self.reply)

    def saveFileName(self, url) -> Any:
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

    def saveToDisk(self, filename, data) -> bool:
        fi = "%s/%s" % (self.dir_, filename)
        if not os.path.exists(self.dir_):
            os.makedirs(self.dir_)
        file = QFile(fi)
        if not file.open(QIODevice.WriteOnly):
            return False

        file.write(data.readAll())
        file.close()

        return True

    def isHttpRedirect(self, reply) -> bool:
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


def copy_dir_recursive(from_dir, to_dir, replace_on_conflict=False) -> bool:
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


def text2bool(text: str) -> bool:
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


def ustr(*t1) -> str:

    return "".join([ustr1(t) for t in t1])


def ustr1(t: Union[str, int]) -> str:

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
        if t is None:
            t = ""

        return "%s" % t
    except Exception:
        logger.exception("ERROR Coercing to string: %s", repr(t))
        return None


class StructMyDict(dict):
    def __getattr__(self, name) -> Any:
        try:
            return self[name]
        except KeyError as e:
            raise AttributeError(e)

    def __setattr__(self, name, value):
        self[name] = value


def version_check(mod_name, mod_ver, min_ver) -> None:
    """Compare two version numbers and raise a warning if "minver" is not met."""
    if version_normalize(mod_ver) < version_normalize(min_ver):
        logger.warning("La version de <%s> es %s. La mínima recomendada es %s.", mod_name, mod_ver, min_ver)


def version_normalize(v) -> List[int]:
    """Normalize version string numbers like 3.10.1 so they can be compared."""
    return [int(x) for x in re.sub(r"(\.0+)*$", "", v).split(".")]


def load2xml(form_path_or_str: str) -> ElementTree:
    from xml.etree import ElementTree as ET

    """
    class xml_parser(ET.TreeBuilder):


        def start(self, tag, attrs):
            return super(xml_parser, self).start(tag, attrs)

        def end(self, tag):
            return super(xml_parser, self).end(tag)

        def data(self, data):
            super(xml_parser, self).data(data)

        def close(self):
            return super(xml_parser, self).close()
    """

    file_ptr: io.StringIO = None
    if (
        form_path_or_str.find("KugarTemplate") > -1
        or form_path_or_str.find("DOCTYPE KugarData") > -1
        or form_path_or_str.find("DOCTYPE svg") > -1
    ):
        form_path_or_str = parse_for_duplicates(form_path_or_str)
        file_ptr = io.StringIO(form_path_or_str)
    elif not os.path.exists(form_path_or_str):
        raise Exception("File %s not found" % form_path_or_str[:200])

    try:
        parser = ET.XMLParser(html=0)
        return ET.parse(file_ptr or form_path_or_str, parser)
    except Exception:
        try:
            parser = ET.XMLParser(html=0, encoding="ISO-8859-15")
            return ET.parse(file_ptr or form_path_or_str, parser)
        except Exception:
            logger.exception("Error cargando UI después de intentar con UTF8 e ISO \n%s", form_path_or_str)
            raise


def parse_for_duplicates(text: str) -> str:
    ret_ = ""
    text = text.replace("+", "__PLUS__")
    text = text.replace("(", "__LPAREN__")
    text = text.replace(")", "__RPAREN__")
    text = text.replace("*", "__ASTERISK__")

    for section_orig in text.split(">"):
        # print("section", section)
        duplicate_ = False
        attr_list: List[str] = []

        # print("--->", section_orig)
        ret2_ = ""
        section = ""
        for a in section_orig.split(" "):

            c = a.count("=")
            if c > 1:
                # part_ = ""
                text_to_process = a
                for m in range(c):
                    pos_ini = text_to_process.find('"')
                    pos_fin = text_to_process[pos_ini + 1 :].find('"')
                    # print("Duplicado", m, pos_ini, pos_fin, text_to_process, "***" , text_to_process[0:pos_ini + 2 + pos_fin])
                    ret2_ += " %s " % text_to_process[0 : pos_ini + 2 + pos_fin]
                    text_to_process = text_to_process[pos_ini + 2 + pos_fin :]

            else:
                ret2_ += "%s " % a

        section += ret2_
        if section.endswith(" "):
            section = section[0 : len(section) - 1]

        if section_orig.endswith("/") and not section.endswith("/"):
            section += "/"

        # print("***", section)
        section = section.replace(" =", "=")
        section = section.replace('= "', '="')

        for attribute_ in section.split(" "):

            # print("attribute", attribute_)
            if attribute_.find("=") > -1:
                attr_name = attribute_[0 : attribute_.find("=")]
                if attr_name not in attr_list:
                    attr_list.append(attr_name)
                else:
                    if attr_name != "":
                        # print("Eliminado attributo duplicado", attr_name)
                        duplicate_ = True

            if not duplicate_:
                if not section.endswith(attribute_):
                    ret_ += "%s " % attribute_
                else:
                    ret_ += "%s" % attribute_
            else:
                if attribute_.endswith("/"):
                    ret_ += "/"

            duplicate_ = False

        if (section.find(">") == -1 and section.find("<") > -1) or section.endswith("--"):
            ret_ += ">"

    # print(ret_)
    return ret_


"""
copy and paste from http://effbot.org/zone/element-lib.htm#prettyprint
it basically walks your tree and adds spaces and newlines so the tree is
printed in a nice way
"""


def indent(elem: Union[Iterable, Sized], level=0) -> None:
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


def format_double(d: _T0, part_integer, part_decimal) -> Union[str, _T0]:
    if d == "":
        return d
    # import locale
    # p_int = field_meta.partInteger()
    # p_decimal = field_meta.partDecimal()
    comma_ = "."
    d = str(d)
    found_comma = True if d.find(comma_) > -1 else False
    # if aqApp.commaSeparator() == comma_:
    #    d = d.replace(",", "")
    # else:
    #    d = d.replace(".","")
    #    d = d.replace(",",".")

    d = round(float(d), part_decimal)

    str_d = str(d)
    str_integer = str_d[0 : str_d.find(comma_)] if str_d.find(comma_) > -1 else str_d
    str_decimal = "" if str_d.find(comma_) == -1 else str_d[str_d.find(comma_) + 1 :]

    if part_decimal > 0:
        while part_decimal > len(str_decimal):
            str_decimal += "0"

    str_integer = format_int(str_integer, part_integer)

    # Fixme: Que pasa cuando la parte entera sobrepasa el limite, se coge el maximo valor o
    ret_ = "%s%s%s" % (str_integer, decimal_separator if found_comma else "", str_decimal if part_decimal > 0 else "")
    return ret_


def format_int(value: _T0, part_intenger=None) -> Union[str, _T0]:
    str_integer = value
    if value is not None:
        str_integer = "{:,d}".format(int(value))

        if decimal_separator == ",":
            str_integer = str_integer.replace(",", ".")
        else:
            str_integer = str_integer.replace(".", ",")

    return str_integer


def unformat_number(new_str: Union[str, str], old_str, type_) -> Any:
    ret_ = new_str
    if old_str is not None:

        if type_ in ("int", "uint"):
            new_str = new_str.replace(",", "")
            new_str = new_str.replace(".", "")

            ret_ = new_str

        else:
            end_comma = False
            if new_str.endswith(",") or new_str.endswith("."):
                # Si acaba en coma, lo guardo
                end_comma = True

            ret_ = new_str.replace(",", "")
            ret_ = ret_.replace(".", "")
            if end_comma:
                ret_ = ret_ + "."
            # else:
            #    comma_pos = old_str.find(".")
            #    if comma_pos > -1:
            print("Desformateando", new_str, ret_)

        # else:
        # pos_comma = old_str.find(".")

        # if pos_comma > -1:
        #    if pos_comma > new_str.find("."):
        #        new_str = new_str.replace(".", "")

        #        ret_ = new_str[0:pos_comma] + "." + new_str[pos_comma:]

    # print("l2", ret_)
    return ret_


def create_dict(
    method: _T0, fun: _T1, id: _T2, arguments: _T3 = []
) -> Dict[str, Union[str, List[Dict[str, Union[_T1, _T2, _T3]]], _T0, _T2]]:
    data = [{"function": fun, "arguments": arguments, "id": id}]
    return {"method": method, "params": data, "jsonrpc": "2.0", "id": id}


def is_deployed() -> bool:
    """Returns True only if the code is running inside a PyInstaller bundle"""
    return getattr(sys, "frozen", False)


def get_base_dir() -> str:
    base_dir = os.path.dirname(__file__)
    base_dir = "%s/../.." % base_dir

    if is_deployed():
        if base_dir.startswith(":"):
            base_dir = ".%s" % base_dir[1:]

    return os.path.realpath(base_dir)


def filedir(*path) -> str:
    """
    filedir(path1[, path2, path3 , ...])
    @param array de carpetas de la ruta
    @return devuelve la ruta absoluta resultado de concatenar los paths que se le pasen y aplicarlos desde la ruta del proyecto.
    Es útil para especificar rutas a recursos del programa.
    """
    ruta_ = os.path.realpath(os.path.join(get_base_dir(), *path))
    return ruta_


def download_files() -> None:
    if os.path.exists(filedir("forms")):
        return

    copy_dir_recursive(":/pineboolib", filedir("../pineboolib"))
    copy_dir_recursive(":/share", filedir("../share"))
    if not os.path.exists(filedir("../tempdata")):
        os.mkdir(filedir("../tempdata"))


def pixmap_fromMimeSource(name) -> Any:

    file_name = filedir("../share/icons", name)
    return QPixmap(file_name) if os.path.exists(file_name) else None
