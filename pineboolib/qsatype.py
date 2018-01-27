# -*- coding: utf-8 -*-

import os
import fnmatch
import weakref

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import QTabWidget, QTextEdit

from PyQt5.QtCore import QIODevice, qWarning, QTextStream

from pineboolib.fllegacy import FLFormSearchDB as FLFormSearchDB_legacy
from pineboolib.flcontrols import FLTable
from pineboolib.fllegacy import FLSqlQuery as FLSqlQuery_Legacy
from pineboolib.fllegacy import FLSqlCursor as FLSqlCursor_Legacy
from pineboolib.fllegacy import FLTableDB as FLTableDB_Legacy
from pineboolib.fllegacy import FLFieldDB as FLFieldDB_Legacy
from pineboolib.fllegacy import FLUtil as FLUtil_Legacy
from pineboolib.fllegacy import FLReportViewer as FLReportViewer_Legacy
from pineboolib.fllegacy import AQObjects

from pineboolib.utils import filedir

from pineboolib import decorators
import traceback
from PyQt5.Qt import QWidget

# Cargar toda la API de Qt para que sea visible.
from PyQt5.QtGui import *  # noqa
from PyQt5.QtCore import *  # noqa
from PyQt5.QtXml import QDomDocument


class StructMyDict(dict):

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError as e:
            raise AttributeError(e)

    def __setattr__(self, name, value):
        self[name] = value


def Function(args, source):
    # Leer código QS embebido en Source
    # asumir que es una funcion anónima, tal que:
    #  -> function($args) { source }
    # compilar la funcion y devolver el puntero
    qs_source = """
function anon(%s) {
    %s
} """ % (args, source)
    print("Compilando QS en línea: ", qs_source)
    from pineboolib.flparser import flscriptparse
    from pineboolib.flparser import postparse
    from pineboolib.flparser.pytnyzer import write_python_file, string_template
    import io
    prog = flscriptparse.parse(qs_source)
    tree_data = flscriptparse.calctree(prog, alias_mode=0)
    ast = postparse.post_parse(tree_data)
    tpl = string_template

    f1 = io.StringIO()

    write_python_file(f1, ast, tpl)
    pyprog = f1.getvalue()
    print("Resultado: ", pyprog)
    glob = {}
    loc = {}
    exec(pyprog, glob, loc)
    # ... y lo peor es que funciona. W-T-F.

    return loc["anon"]


def Object(x=None):
    if x is None:
        x = {}
    return StructMyDict(x)

# def Array(x=None):
    # try:
    # if x is None: return {}
    # else: return list(x)
    # except TypeError:
    # return [x]


class Array(object):

    dict_ = None
    key_ = None
    names_ = None

    def __init__(self, *args):
        self.names_ = []
        self.dict_ = {}

        if not len(args):
            return
        elif isinstance(args[0], int) and len(args) == 1:
            return
        elif isinstance(args[0], list):
            for field in args[0]:
                self.names_.append(field)
                self.dict_[field] = field

        elif isinstance(args[0], str):
            for f in args:
                self.__setitem__(f, f)
        else:
            self.dict_ = args

    def __setitem__(self, key, value):
        # if isinstance(key, int):
        #   key = str(key)
        if key not in self.names_:
            self.names_.append(key)

        self.dict_[key] = value

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.dict_[self.names_[key]]
        else:
            # print("QSATYPE.DEBUG: Array.getItem() " ,key,  self.dict_[key])
            return self.dict_[key]

    def __getattr__(self, k):
        if k == 'length':
            return len(self.dict_)
        else:
            return self.dict_[k]

    def __len__(self):
        len_ = 0

        for l in self.dict_:
            len_ = len_ + 1

        return len_


def Boolean(x=False):
    return bool(x)


def FLSqlQuery(*args):
    # if not args: return None
    query_ = FLSqlQuery_Legacy.FLSqlQuery(*args)

    return query_


def FLUtil(*args):
    return FLUtil_Legacy.FLUtil(*args)


def AQUtil(*args):
    return FLUtil_Legacy.FLUtil(*args)


def AQSql(*args):
    return AQObjects.AQSql(*args)


def FLSqlCursor(action=None, cN=None):
    if action is None:
        return None
    return FLSqlCursor_Legacy.FLSqlCursor(action, True, cN)


def FLTableDB(*args):
    if not args:
        return None
    return FLTableDB_Legacy.FLTableDB(*args)


FLListViewItem = QtWidgets.QListView
FLDomDocument = QDomDocument
QTable = FLTable
Color = QtGui.QColor
QColor = QtGui.QColor
QDateEdit = QtWidgets.QDateEdit


@decorators.NotImplementedWarn
def FLPosPrinter(*args, **kwargs):
    class flposprinter:
        pass
    return flposprinter()


@decorators.BetaImplementation
def FLReportViewer():
    return FLReportViewer_Legacy.FLReportViewer()


"""
class FLDomDocument(object):

    parser = None
    tree = None
    root_ = None
    string_ = None

    def __init__(self):
        self.parser = etree.XMLParser(recover=True, encoding='utf-8')
        self.string_ = None


    def setContent(self, value):
        try:
            self.string_ = value
            if value.startswith('<?'):
                value = re.sub(r'^\<\?.*?\?\>','', value, flags=re.DOTALL)
            self.tree = etree.fromstring(value, self.parser)
            #self.root_ = self.tree.getroot()
            return True
        except:
            return False

    def namedItem(self, name):
        return u"<%s" % name in self.string_

    def toString(self, value = None):
        return self.string_
"""


@decorators.NotImplementedWarn
def FLCodBar(*args, **kwargs):
    class flcodbar:
        def nameToType(self, name):
            return name

        def pixmapError(self):
            return QtGui.QPixmap()

        def pixmap(self):
            return QtGui.QPixmap()

        def validBarcode(self):
            return None
    return flcodbar()


def print_stack(maxsize=1):
    for tb in traceback.format_list(traceback.extract_stack())[1:-2][-maxsize:]:
        print(tb.rstrip())


def check_gc_referrers(typename, w_obj, name):
    import threading
    import time

    def checkfn():
        import gc
        time.sleep(2)
        gc.collect()
        obj = w_obj()
        if not obj:
            return
        # TODO: Si ves el mensaje a continuación significa que "algo" ha dejado
        # ..... alguna referencia a un formulario (o similar) que impide que se destruya
        # ..... cuando se deja de usar. Causando que los connects no se destruyan tampoco
        # ..... y que se llamen referenciando al código antiguo y fallando.
        print("HINT: Objetos referenciando %r::%r (%r) :" %
              (typename, obj, name))
        for ref in gc.get_referrers(obj):
            if isinstance(ref, dict):
                x = []
                for k, v in ref.items():
                    if v is obj:
                        k = "(**)" + k
                        x.insert(0, k)
                    else:
                        x.append(k)
                print(" - ", repr(x[:48]))
            else:
                if "<frame" in str(repr(ref)):
                    continue
                print(" - ", repr(ref))

    threading.Thread(target=checkfn).start()


class FormDBWidget(QtWidgets.QWidget):

    closed = QtCore.pyqtSignal()
    cursor_ = None
    parent_ = None
    
    def __init__(self, action, project, parent = None):
        if not action.prj._DGI.useDesktop():
            self._class_init()
            return

        super(FormDBWidget, self).__init__(parent)
        self._action = action
        self.cursor_ = None
        self.parent_ = parent
        self._prj = project
        try:
            self._class_init()
            # timer = QtCore.QTimer(self)
            # timer.singleShot(250, self.init)
            self.init()
        except Exception as e:
            print("FormDBWidget.__init__:", e)

    def __del__(self):
        print("FormDBWidget: Borrando form para accion %r" % self._action.name)

    def parent(self):
        return self.parent_

    def _class_init(self):
        pass

    def closeEvent(self, event):
        can_exit = True
        print("FormDBWidget: closeEvent para accion %r" % self._action.name)
        check_gc_referrers("FormDBWidget:" + self.__class__.__name__,
                           weakref.ref(self), self._action.name)
        if can_exit:
            self.closed.emit()
            event.accept()  # let the window close
        else:
            event.ignore()

        if hasattr(self, 'iface'):
            check_gc_referrers("FormDBWidget.iface:" + self.iface.__class__.__name__,
                               weakref.ref(self.iface), self._action.name)
            del self.iface.ctx
            del self.iface

    def child(self, childName):
        try:
            parent = self
            ret = None
            while parent and not ret:
                ret = parent.findChild(QtWidgets.QWidget, childName)
                if not ret:
                    parent = parent.parentWidget()

        except RuntimeError as rte:
            # FIXME: A veces intentan buscar un control que ya está siendo eliminado.
            # ... por lo que parece, al hacer el close del formulario no se desconectan sus señales.
            print("ERROR: Al buscar el control %r encontramos el error %r" %
                  (childName, rte))
            print_stack(8)
            import gc
            gc.collect()
            print("HINT: Objetos referenciando FormDBWidget::%r (%r) : %r" %
                  (self, self._action.name, gc.get_referrers(self)))
            if hasattr(self, 'iface'):
                print("HINT: Objetos referenciando FormDBWidget.iface::%r : %r" % (
                    self.iface, gc.get_referrers(self.iface)))
            ret = None
        else:
            if ret is None:
                qWarning("WARN: No se encontro el control %s" % childName)

        # Para inicializar los controles si se llaman desde qsa antes de mostrar el formulario.
        if isinstance(ret, FLFieldDB_Legacy.FLFieldDB):
            if not ret.cursor():
                ret.initCursor()
            if not ret.editor_ and not ret.editorImg_:
                ret.initEditor()

        if isinstance(ret, FLTableDB_Legacy.FLTableDB):
            if not ret.tableRecords_:
                ret.tableRecords()
                ret.setTableRecordsCursor()

        # else:
        #    print("DEBUG: Encontrado el control %r: %r" % (childName, ret))
        return ret

    def cursor(self):

        # if self.cursor_:
        #    return self.cursor_

        cursor = None
        parent = self

        while not cursor and parent:
            parent = parent.parent()
            cursor = getattr(parent, "cursor_", None)

        if cursor:
            self.cursor_ = cursor
        else:
            if not self.cursor_:
                self.cursor_ = FLSqlCursor(self._action.name)

        return self.cursor_

    """
    FIX: Cuando usamos this como cursor
    """

    def valueBuffer(self, name):
        return self.cursor().valueBuffer(name)

    def isNull(self, name):
        return self.cursor().isNull(name)

    def table(self):
        return self.cursor().table()

    def cursorRelation(self):
        return self.cursor().cursorRelation()


def FLFormSearchDB(name):
    widget = FLFormSearchDB_legacy.FLFormSearchDB(name)
    widget.setWindowModality(QtCore.Qt.ApplicationModal)
    widget.load()
    widget.cursor_.setContext(widget.iface)
    return widget


class Date(object):

    date_ = None
    time_ = None

    def __init__(self, date_=None):
        super(Date, self).__init__()
        if not date_:
            self.date_ = QtCore.QDate.currentDate()
            self.time_ = QtCore.QTime.currentTime()
        else:
            self.date_ = QtCore.QDate(date_)
            self.time_ = QtCore.QTime("00:00:00")

    def toString(self, *args, **kwargs):
        texto = "%s-%s-%sT%s:%s:%s" % (self.date_.toString("dd"), self.date_.toString("MM"), self.date_.toString(
            "yyyy"), self.time_.toString("hh"), self.time_.toString("mm"), self.time_.toString("ss"))
        return texto

    def getYear(self):
        return self.date_.year()

    def getMonth(self):
        return self.date_.month()

    def getDay(self):
        return self.date_.day()

    def getHours(self):
        return self.time_.hour()

    def getMinutes(self):
        return self.time_.minute()

    def getSeconds(self):
        return self.time_.second()

    def getMilliseconds(self):
        return self.time_.msec()


class Process(QtCore.QProcess):

    running = None
    stderr = None
    stdout = None

    def __init__(self, *args):
        super(Process, self).__init__()
        self.readyReadStandardOutput.connect(self.stdoutReady)
        self.readyReadStandardError.connect(self.stderrReady)
        self.stderr = None
        if args:
            self.runing = False
            self.setProgram(args[0])
            argumentos = args[1:]
            self.setArguments(argumentos)

    def start(self):
        self.running = True
        super(Process, self).start()

    def stop(self):
        self.running = False
        super(Process, self).stop()

    def writeToStdin(self, stdin_):
        stdin_as_bytes = stdin_.encode('utf-8')
        self.writeData(stdin_as_bytes)
        # self.closeWriteChannel()

    def stdoutReady(self):
        self.stdout = str(self.readAllStandardOutput())

    def stderrReady(self):
        self.stderr = str(self.readAllStandardError())

    def __setattr__(self, name, value):
        if name == "workingDirectory":
            self.setWorkingDirectory(value)
        else:
            super(Process, self).__setattr__(name, value)

    def execute(comando):

        pro = QtCore.QProcess()
        array = comando.split(" ")
        programa = array[0]
        argumentos = array[1:]
        pro.setProgram(programa)
        pro.setArguments(argumentos)
        pro.start()
        pro.waitForFinished(30000)
        Process.stdout = pro.readAllStandardOutput()
        Process.stderr = pro.readAllStandardError()


class RadioButton(QtWidgets.QRadioButton):

    def __ini__(self):
        super(RadioButton, self).__init__()
        self.setChecked(False)

    def __setattr__(self, name, value):
        if name == "text":
            self.setText(value)
        elif name == "checked":
            self.setChecked(value)
        else:
            super(RadioButton, self).__setattr__(name, value)

    def __getattr__(self, name):
        if name == "checked":
            return self.isChecked()


class Dialog(QtWidgets.QDialog):
    _layout = None
    buttonBox = None
    okButtonText = None
    cancelButtonText = None
    okButton = None
    cancelButton = None
    _tab = None

    def __init__(self, title=None, f=None, desc=None):
        # FIXME: f no lo uso , es qt.windowsflg
        super(Dialog, self).__init__()
        if title:
            self.setWindowTitle(str(title))

        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self._layout = QtWidgets.QVBoxLayout()
        self.setLayout(self._layout)
        self.buttonBox = QtWidgets.QDialogButtonBox()
        self.okButton = QtWidgets.QPushButton("&Aceptar")
        self.cancelButton = QtWidgets.QPushButton("&Cancelar")
        self.buttonBox.addButton(
            self.okButton, QtWidgets.QDialogButtonBox.AcceptRole)
        self.buttonBox.addButton(
            self.cancelButton, QtWidgets.QDialogButtonBox.RejectRole)
        self.okButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)
        self._tab = QTabWidget()
        self._layout.addWidget(self._tab)
        self.oKButtonText = None
        self.cancelButtonText = None

    def add(self, _object):
        self._layout.addWidget(_object)

    def exec_(self):
        if self.okButtonText:
            self.okButton.setText(str(self.okButtonText))
        if (self.cancelButtonText):
            self.cancelButton.setText(str(self.cancelButtonText))
        self._layout.addWidget(self.buttonBox)

        return super(Dialog, self).exec_()

    def newTab(self, name):
        self._tab.addTab(QtWidgets.QWidget(), str(name))

    def __getattr__(self, name):
        if name == "caption":
            name = self.setWindowTitle

        return getattr(super(Dialog, self), name)


class GroupBox(QtWidgets.QGroupBox):
    def __init__(self):
        super(GroupBox, self).__init__()
        self._layout = QtWidgets.QVBoxLayout()
        self.setLayout(self._layout)

    def add(self, _object):
        self._layout.addWidget(_object)

    def __setattr__(self, name, value):
        if name == "title":
            self.setTitle(str(value))
        else:
            super(GroupBox, self).__setattr__(name, value)


class CheckBox(QWidget):
    _label = None
    _cb = None

    def __init__(self):
        super(CheckBox, self).__init__()

        self._label = QtWidgets.QLabel(self)
        self._cb = QtWidgets.QCheckBox(self)
        spacer = QtWidgets.QSpacerItem(
            1, 1, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        _lay = QtWidgets.QHBoxLayout()
        _lay.addWidget(self._cb)
        _lay.addWidget(self._label)
        _lay.addSpacerItem(spacer)
        self.setLayout(_lay)

    def __setattr__(self, name, value):
        if name == "text":
            self._label.setText(str(value))
        elif name == "checked":
            self._cb.setChecked(value)
        else:
            super(CheckBox, self).__setattr__(name, value)

    def __getattr__(self, name):
        if name == "checked":
            return self._cb.isChecked()
        else:
            return super(CheckBox, self).__getattr__(name)


class ComboBox(QWidget):

    _label = None
    _combo = None

    def __init__(self):
        super(ComboBox, self).__init__()

        self._label = QtWidgets.QLabel(self)
        self._combo = QtWidgets.QComboBox(self)
        self._combo.setMinimumHeight(25)
        _lay = QtWidgets.QHBoxLayout()
        _lay.addWidget(self._label)
        _lay.addWidget(self._combo)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(True)
        self._combo.setSizePolicy(sizePolicy)

        self.setLayout(_lay)

    def __setattr__(self, name, value):
        if name == "label":
            self._label.setText(str(value))
        elif name == "itemList":
            self._combo.insertItems(len(value), value)
        elif name == "currentItem":
            self._combo.setCurrentText(str(value))
        else:
            super(ComboBox, self).__setattr__(name, value)

    def __getattr__(self, name):
        if name == "currentItem":
            return self._combo.currentText()
        else:
            return super(ComboBox, self).__getattr__(name)


class LineEdit(QWidget):
    _label = None
    _line = None

    def __init__(self):
        super(LineEdit, self).__init__()

        self._label = QtWidgets.QLabel(self)
        self._line = QtWidgets.QLineEdit(self)
        _lay = QtWidgets.QHBoxLayout()
        _lay.addWidget(self._label)
        _lay.addWidget(self._line)
        self.setLayout(_lay)

    def __setattr__(self, name, value):
        if name == "label":
            self._label.setText(str(value))
        elif name == "text":
            self._line.setText(str(value))
        else:
            super(LineEdit, self).__setattr__(name, value)

    def __getattr__(self, name):
        if name == "text":
            return self._line.text()
        else:
            return super(LineEdit, self).__getattr__(name)


class Dir_Class(object):
    path_ = None
    home = None
    Files = "*.*"

    def __init__(self, path=None):
        self.path_ = path
        self.home = filedir("..")

    def entryList(self, patron, type_=None):
        # p = os.walk(self.path_)
        retorno = []
        try:
            for file in os.listdir(self.path_):
                if fnmatch.fnmatch(file, patron):
                    retorno.append(file)
        except Exception as e:
            print("Dir_Class.entryList:", e)

        return retorno

    def fileExists(self, name):
        return os.path.exists(name)

    def cleanDirPath(name):
        return str(name)


Dir = Dir_Class


class TextEdit(QTextEdit):
    pass


class File(QtCore.QFile):
    fichero = None
    mode = None
    path = None

    ReadOnly = QIODevice.ReadOnly
    WriteOnly = QIODevice.WriteOnly
    ReadWrite = QIODevice.ReadWrite

    def __init__(self, rutaFichero):
        if isinstance(rutaFichero, tuple):
            rutaFichero = rutaFichero[0]
        self.fichero = str(rutaFichero)
        super(File, self).__init__(rutaFichero)
        self.path = os.path.dirname(self.fichero)

    # def open(self, mode):
    #    super(File, self).open(self.fichero, mode)

    def read(self):
        if isinstance(self, str):
            f = File(self)
            f.open(File.ReadOnly)
            return f.read()

        in_ = QTextStream(self)
        return in_.readAll()

    def write(self, text):
        raise NotImplementedError(
            "File:: out_ << text not a valid Python operator")
        # encoding = text.property("encoding")
        # out_ = QTextStream(self)
        # out_ << text


class QString(str):
    def mid(self, start, length=None):
        if length is not None:
            return self[start:]
        else:
            return self[start:start + length]
