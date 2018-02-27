# # -*- coding: utf-8 -*-
import os
import os.path
import re
import logging
import sys


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

# Convertir una ruta relativa, a una ruta relativa a este fichero.


def filedir(*path):
    """  filedir(path1[, path2, path3 , ...])

            Filedir devuelve la ruta absoluta resultado de concatenar los paths que se le pasen y aplicarlos desde la ruta del proyecto.
            Es útil para especificar rutas a recursos del programa.
    """
    ruta_ = os.path.dirname(__file__)
    if ruta_.find(":") > -1:
        ruta_ = ruta_.replace(":", ".")
    ruta_ = os.path.realpath(os.path.join(ruta_, *path))
    # if ruta_.find(":/pineboolib/forms") > -1 or ruta_.find(":/pineboolib/plugins") > -1 or ruta_.find(":/pineboolib/..") > -1:

    return ruta_


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
                    from pineboolib.qt3ui import loadProperty

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
                     self.parent.__class__.__name__, self.funname, args)
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
from PyQt5.QtCore import QObject, QFileInfo, QFile, QIODevice, QUrl, QByteArray
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

        #infile = QFile(filename)
        # infile.open(QIODevice.ReadOnly)
        #uncompress = QByteArray(infile.readAll())

        #QtWidgets.QMessageBox.information(None, "AVISO", "%s" % self.result)


def download_files():
    import sysconfig
    from PyQt5.QtWidgets import (QApplication, QLabel, QTreeView, QVBoxLayout,
                                 QWidget, QLineEdit, QPushButton)

    # Try and import the platform-specific modules.
    platform_module = "Not available"

    try:
        import PyQt5.QtAndroidExtras
        platform_module = 'QtAndroidExtras'
    except ImportError:
        pass

    try:
        import PyQt5.QtMacExtras
        platform_module = 'QtMacExtras'
    except ImportError:
        pass

    try:
        import PyQt5.QtWinExtras
        platform_module = 'QtWinExtras'
    except ImportError:
        pass

    try:
        import PyQt5.QtX11Extras
        platform_module = 'QtX11Extras'
    except ImportError:
        pass

    # Try and import the optional products.
    optional_products = []

    # Create the GUI.

    app = QApplication(sys.argv)
    QApplication.setStyle("Android")
    lista = {}
    lista["dlg_connect.ui"] = "pineboolib/forms"
    lista["flareas.mtd"] = "share/pineboo/tables"
    lista["flfiles.mtd"] = "share/pineboo/tables"
    lista["flgroups.mtd"] = "share/pineboo/tables"
    lista["fllarge.mtd"] = "share/pineboo/tables"
    lista["flmetadata.mtd"] = "share/pineboo/tables"
    lista["flmodules.mtd"] = "share/pineboo/tables"
    lista["flseqs.mtd"] = "share/pineboo/tables"
    lista["flserial.mtd"] = "share/pineboo/tables"
    lista["flsettings.mtd"] = "share/pineboo/tables"
    lista["flusers.mtd"] = "share/pineboo/tables"
    lista["flvar.mtd"] = "share/pineboo/tables"
    lista["sys.xpm"] = "share/pineboo"
    lista["flareas.ui"] = "share/pineboo/forms"
    lista["flfiles.ui"] = "share/pineboo/forms"
    lista["flgroups.ui"] = "share/pineboo/forms"
    lista["flmodulos.ui"] = "share/pineboo/forms"
    lista["flusers.ui"] = "share/pineboo/forms"
    lista["FLWidgetMasterTable.ui"] = "share/pineboo/forms"
    lista["mainwindow.ui"] = "share/pineboo/forms"
    lista["master.ui"] = "share/pineboo/forms"
    lista["master_copy.ui"] = "share/pineboo/forms"
    lista["master_print.ui"] = "share/pineboo/forms"
    lista["master_print_copy.ui"] = "share/pineboo/forms"
    lista["sys.ui"] = "share/pineboo/forms"
    lista["flloadmod.qs.py"] = "share/pineboo/scripts"
    lista["flmodules.qs.py"] = "share/pineboo/scripts"
    lista["sys.qs.py"] = "share/pineboo/scripts"
    lista["sys.xml"] = "share/pineboo"
    lista["mainform.ui"] = "pineboolib/plugins/mainform/pineboo"

    shell = QWidget()
    shell_layout = QVBoxLayout()

    header = QLabel("""<h1>PINEBOO</h1>
    <p>Se necesita una descarga adicional
    </p>""")
    header.setWordWrap(True)
    urllineedit = QLineEdit()
    urllineedit.setText("http://192.168.1.106")
    pb = QPushButton()
    pb.setText("Descargar")
    shell_layout.addWidget(header)
    shell_layout.addWidget(urllineedit)
    shell_layout.addWidget(pb)
    shell.setLayout(shell_layout)
    dm = {}
    for l in lista.keys():
        dm[l] = downloadManager()
        dm[l].setLE(l, lista[l], urllineedit)
        pb.clicked.connect(dm[l].doDownload)

    # Show the GUI and interact with it.
    shell.show()
    app.exec()

    # All done.
    sys.exit()
