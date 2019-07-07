# -*- coding: utf-8 -*-
import inspect
import weakref
import re
import os
import traceback

from typing import Any, Callable

from PyQt5 import QtCore  # type: ignore
from pineboolib.core.utils.singleton import Singleton
from pineboolib.core.settings import config
from pineboolib.core import decorators
from pineboolib.core.utils.logging import logging
from pineboolib.wiki_error import wiki_error
from pineboolib import project
from pineboolib.fllegacy.flutil import FLUtil


logger = logging.getLogger("PNControlsFactory")

"""
Conjunto de controles usados en Pineboo. Estos son cargados desde el DGI seleccionado en el proyecto
"""

"""
Devuelve un objecto a partir de su nombre
@param name, Nombre del objecto a buscar
@return objecto o None si no existe el objeto buscado
"""


class ObjectNotFoundInCurrentDGI(object):
    pass


class ObjectNotFoundDGINotLoaded(object):
    pass


def resolveObject(name: str) -> Any:
    if not project._DGI:
        return ObjectNotFoundDGINotLoaded
    obj_ = getattr(project._DGI, name, None)
    if obj_:
        return obj_

    logger.warning("resolveObject: class <%s> not found in dgi <%s>", name, project._DGI.alias().lower())
    return ObjectNotFoundInCurrentDGI


def reload_from_DGI():
    # Clases Qt
    global QComboBox, QTable, QLayoutWidget, QToolButton, QTabWidget, QLabel, QGroupBox, QListView, QPushButton, QTextEdit
    global QLineEdit, QDateEdit, QTimeEdit, QCheckBox, QWidget, QtWidgets, QColor, QMessageBox, QButtonGroup, QDialog
    global QVBoxLayout, QHBoxLayout, QFrame, QMainWindow, QSignalMapper, QDomDocument, QMenu, QToolBar, QListWidgetItem, QListViewWidget
    global QPixmap, QImage, QIcon, QAction, QActionGroup, QTreeWidget, QTreeWidgetItem, QTreeWidgetItemIterator, QDataView
    global QProcess, QByteArray, QRadioButton, QSpinBox, QInputDialog, QLineEdit, QApplication, qApp, QStyleFactory, QFontDialog
    global QDockWidget, QMdiArea, QMdiSubWindow, QKeySequence, QSize, QSizePolicy, QToolBox, QPainter, QBrush, QProgressDialog, QFileDialog
    # Clases FL
    global FLLineEdit, FLTimeEdit, FLDateEdit, FLPixmapView, FLDomDocument, FLDomElement
    global FLDomNode, FLDomNodeList, FLListViewItem, FLTable, FLDataTable, FLCheckBox, FLTextEditOutput
    global FLSpinBox, FLTableDB, FLFieldDB, FLFormDB, FLFormRecordDB, FLFormSearchDB, FLDoubleValidator
    global FLIntValidator, FLUIntValidator, FLCodBar, FLWidget, FLWorkSpace, FormDBWidget
    # Clases QSA
    global CheckBox, ComboBox, TextEdit, LineEdit, FileDialog, MessageBox, RadioButton, Color, Dialog
    global Label, GroupBox, Process, SpinBox, Line, NumberEdit, DateEdit, TimeEdit
    # Clases AQNext
    global auth
    # Clases Qt
    QComboBox = resolveObject("QComboBox")
    QTable = resolveObject("QTable")
    QLayoutWidget = resolveObject("QWidget")
    QToolButton = resolveObject("QToolButton")
    QTabWidget = resolveObject("QTabWidget")
    QLabel = resolveObject("QLabel")
    QGroupBox = resolveObject("QGroupBox")
    QListView = resolveObject("QListView")
    QPushButton = resolveObject("QPushButton")
    QTextEdit = resolveObject("QTextEdit")
    QLineEdit = resolveObject("QLineEdit")
    QDateEdit = resolveObject("QDateEdit")
    QTimeEdit = resolveObject("QTimeEdit")
    QCheckBox = resolveObject("QCheckBox")
    QWidget = resolveObject("QWidget")
    QtWidgets = resolveObject("QtWidgets")
    QColor = resolveObject("QColor")
    QMessageBox = resolveObject("MessageBox")
    QButtonGroup = resolveObject("QButtonGroup")
    QDialog = resolveObject("QDialog")
    QVBoxLayout = resolveObject("QVBoxLayout")
    QHBoxLayout = resolveObject("QHBoxLayout")
    QFrame = resolveObject("QFrame")
    QMainWindow = resolveObject("QMainWindow")
    QSignalMapper = resolveObject("QSignalMapper")
    QDomDocument = resolveObject("QDomDocument")
    QMenu = resolveObject("QMenu")
    QToolBar = resolveObject("QToolBar")
    QListWidgetItem = resolveObject("QListWidgetItem")
    QListViewWidget = resolveObject("QListWidget")
    QPixmap = resolveObject("QPixmap")
    QImage = resolveObject("QImage")
    QIcon = resolveObject("QIcon")
    QAction = resolveObject("QAction")
    QActionGroup = resolveObject("QActionGroup")
    QTreeWidget = resolveObject("QTreeWidget")
    QTreeWidgetItem = resolveObject("QTreeWidgetItem")
    QTreeWidgetItemIterator = resolveObject("QTreeWidgetItemIterator")
    QDataView = resolveObject("QWidget")
    QProcess = resolveObject("Process")
    QByteArray = resolveObject("QByteArray")
    QRadioButton = resolveObject("QRadioButton")
    QSpinBox = resolveObject("FLSpinBox")
    QInputDialog = resolveObject("QInputDialog")
    QLineEdit = resolveObject("QLineEdit")
    QApplication = resolveObject("QApplication")
    qApp = resolveObject("qApp")
    QStyleFactory = resolveObject("QStyleFactory")
    QFontDialog = resolveObject("QFontDialog")
    QDockWidget = resolveObject("QDockWidget")
    QMdiArea = resolveObject("QMdiArea")
    QMdiSubWindow = resolveObject("QMdiSubWindow")
    QKeySequence = resolveObject("QKeySequence")
    QSize = resolveObject("QSize")
    QSizePolicy = resolveObject("QSizePolicy")
    QToolBox = resolveObject("QToolBox")
    QPainter = resolveObject("QPainter")
    QBrush = resolveObject("QBrush")
    QProgressDialog = resolveObject("QProgressDialog")
    QFileDialog = resolveObject("QFileDialog")

    """
    QIconSet = resolveObject("QIconSet")
    """
    # Clases FL
    FLLineEdit = resolveObject("FLLineEdit")
    FLTimeEdit = resolveObject("FLTimeEdit")
    FLDateEdit = resolveObject("FLDateEdit")
    FLPixmapView = resolveObject("FLPixmapView")
    FLDomDocument = resolveObject("QDomDocument")
    FLDomElement = resolveObject("QDomElement")
    FLDomNode = resolveObject("QDomNode")
    FLDomNodeList = resolveObject("QDomNodeList")
    FLListViewItem = resolveObject("FLListViewItem")
    FLTable = resolveObject("QTable")
    FLDataTable = resolveObject("FLDataTable")
    FLCheckBox = resolveObject("FLCheckBox")
    FLTextEditOutput = resolveObject("FLTextEditOutput")
    FLSpinBox = resolveObject("FLSpinBox")
    FLTableDB = resolveObject("FLTableDB")
    FLFieldDB = resolveObject("FLFieldDB")
    FLFormDB = resolveObject("FLFormDB")
    FLFormRecordDB = resolveObject("FLFormRecordDB")
    FLFormSearchDB = resolveObject("FLFormSearchDB")
    FLDoubleValidator = resolveObject("FLDoubleValidator")
    FLIntValidator = resolveObject("FLIntValidator")
    FLUIntValidator = resolveObject("FLUIntValidator")
    FLCodBar = resolveObject("FLCodBar")
    FLWidget = resolveObject("FLWidget")
    FLWorkSpace = resolveObject("FLWorkSpace")

    FormDBWidget = resolveObject("FormDBWidget")
    # Clases QSA
    CheckBox = resolveObject("CheckBox")
    ComboBox = resolveObject("QComboBox")
    TextEdit = QTextEdit
    LineEdit = resolveObject("LineEdit")
    FileDialog = resolveObject("FileDialog")
    MessageBox = resolveObject("MessageBox")
    RadioButton = resolveObject("RadioButton")
    Color = QColor
    Dialog = resolveObject("Dialog")
    Label = resolveObject("QLabel")
    GroupBox = resolveObject("GroupBox")
    Process = resolveObject("Process")
    SpinBox = resolveObject("FLSpinBox")
    Line = resolveObject("QLine")
    NumberEdit = resolveObject("NumberEdit")
    DateEdit = resolveObject("QDateEdit")
    TimeEdit = resolveObject("QTimeEdit")

    # Clases AQNext
    auth = resolveObject("auth")


class SysType(object, metaclass=Singleton):
    def __init__(self) -> None:
        self._name_user = None
        self.sys_widget = None

    def nameUser(self) -> str:
        ret_ = None
        if aqApp.DGI().use_alternative_credentials():
            ret_ = aqApp.DGI().get_nameuser()
        else:
            ret_ = aqApp.db().user()

        return ret_

    def interactiveGUI(self) -> str:
        return aqApp.DGI().interactiveGUI()

    def isUserBuild(self) -> bool:
        return self.version().upper().find("USER") > -1

    def isDeveloperBuild(self) -> bool:
        return self.version().upper().find("DEVELOPER") > -1

    def isNebulaBuild(self) -> bool:
        return self.version().upper().find("NEBULA") > -1

    def isDebuggerMode(self) -> bool:
        return bool(config.value("application/isDebuggerMode", False))

    @decorators.NotImplementedWarn
    def isCloudMode(self) -> bool:
        return False

    def isDebuggerEnabled(self) -> bool:
        return bool(config.value("application/dbadmin_enabled", False))

    def isQuickBuild(self):
        return not self.isDebuggerEnabled()

    def isLoadedModule(self, modulename: str) -> bool:
        return modulename in aqApp.db().managerModules().listAllIdModules()

    def translate(self, *args) -> str:
        util = FLUtil()

        group = args[0] if len(args) == 2 else "scripts"
        text = args[1] if len(args) == 2 else args[0]

        return util.translate(group, text)

    def osName(self) -> str:
        util = FLUtil()
        return util.getOS()

    def nameBD(self):
        return aqApp.db().DBName()

    def toUnicode(self, val: str, format: str) -> str:
        return val.encode(format).decode("utf-8", "replace")

    def fromUnicode(self, val, format):
        return val.encode("utf-8").decode(format, "replace")

    def Mr_Proper(self):
        aqApp.db().Mr_Proper()

    def installPrefix(self):
        from pineboolib.core.utils.utils_base import filedir

        return filedir("..")

    def __getattr__(self, fun_: str) -> Callable:
        if self.sys_widget is None:
            if "sys" in project.actions:
                self.sys_widget = project.actions["sys"].load().widget
            else:
                logger.warn("No action found for 'sys'")
        return getattr(self.sys_widget, fun_, None)

    def installACL(self, idacl):
        # acl_ = project.acl()
        acl_ = None  # FIXME: Add ACL later
        if acl_:
            acl_.installACL(idacl)

    def version(self) -> str:
        return str(project.version)

    def processEvents(self) -> None:
        return aqApp.DGI().processEvents()

    def write(self, encode_, dir_, contenido):
        import codecs

        f = codecs.open(dir_, encoding=encode_, mode="w+")
        f.write(contenido)
        f.seek(0)
        f.close()

    def cleanupMetaData(self, connName="default"):
        aqApp.db().useConn(connName).manager().cleanupMetaData()

    def updateAreas(self):
        aqApp.initToolBox()

    def reinit(self):
        aqApp.reinit()

    def setCaptionMainWidget(self, t):
        aqApp.setCaptionMainWidget(t)

    def nameDriver(self, connName="default"):
        return aqApp.db().useConn(connName).driverName()

    def nameHost(self, connName="default"):
        return aqApp.db().useConn(connName).host()

    def addDatabase(self, *args):
        # def addDatabase(self, driver_name = None, db_name = None, db_user_name = None,
        #                 db_password = None, db_host = None, db_port = None, connName="default"):
        if len(args) == 1:
            conn_db = aqApp.db().useConn(args[0])
            if not conn_db.isOpen():
                if conn_db.driverName_ and conn_db.driverSql.loadDriver(conn_db.driverName_):
                    conn_db.driver_ = conn_db.driverSql.driver()
                    conn_db.conn = conn_db.conectar(
                        aqApp.db().db_name, aqApp.db().db_host, aqApp.db().db_port, aqApp.db().db_userName, aqApp.db().db_password
                    )
                    if conn_db.conn is False:
                        return False

                    conn_db._isOpen = True

        else:
            conn_db = aqApp.db().useConn(args[6])
            if not conn_db.isOpen():
                conn_db.driverName_ = conn_db.driverSql.aliasToName(args[0])
                if conn_db.driverName_ and conn_db.driverSql.loadDriver(conn_db.driverName_):
                    conn_db.conn = conn_db.conectar(args[1], args[4], args[5], args[2], args[3])

                    if conn_db.conn is False:
                        return False

                    # conn_db.driver().db_ = conn_db
                    conn_db._isOpen = True
                    # conn_db._dbAux = conn_db

        return True

    def removeDatabase(self, connName="default"):
        return aqApp.db().useConn(connName).removeConn(connName)

    def idSession(self):
        return aqApp.timeUser().toString(QtCore.Qt.ISODate)


class System_class(object):
    def setenv(name, val):
        os.environ[name] = val

    def getenv(self, name):
        ret_ = ""
        if name in os.environ.keys():
            ret_ = os.environ[name]

        return ret_


System = System_class()


class ProxySlot:
    PROXY_FUNCTIONS = {}

    def __init__(self, remote_fn, receiver, slot):
        self.key = "%r.%r->%r" % (remote_fn, receiver, slot)
        if self.key not in self.PROXY_FUNCTIONS:
            weak_fn = weakref.WeakMethod(remote_fn)
            weak_receiver = weakref.ref(receiver)
            self.PROXY_FUNCTIONS[self.key] = proxy_fn(weak_fn, weak_receiver, slot)
        self.proxy_function = self.PROXY_FUNCTIONS[self.key]

    def getProxyFn(self):
        return self.proxy_function


def get_expected_args_num(inspected_function):
    expected_args = inspect.getargspec(inspected_function)[0]
    args_num = len(expected_args)

    if args_num and expected_args[0] == "self":
        args_num -= 1

    return args_num


def get_expected_kwargs(inspected_function):
    expected_kwargs = inspect.getargspec(inspected_function)[2]
    return True if expected_kwargs else False


def proxy_fn(wf, wr, slot):
    def fn(*args, **kwargs):
        f = wf()
        if not f:
            return None
        r = wr()
        if not r:
            return None

        args_num = get_expected_args_num(f)

        if args_num:
            return f(*args[0:args_num], **kwargs)
        else:
            return f()

    return fn


def slot_done(fn, signal, sender, caller):
    def new_fn(*args, **kwargs):

        res = False

        # Este parche es para evitar que las conexiones de un clicked de error de cantidad de argumentos.
        # En Eneboo se esperaba que signal no contenga argumentos
        if signal.signal == "2clicked(bool)":
            args = []

        args_num = get_expected_args_num(fn)
        try:
            if get_expected_kwargs(fn):
                res = fn(*args[0:args_num], **kwargs)
            else:
                res = fn(*args[0:args_num])
        except Exception:
            # script_name = caller.__module__ if caller is not None else "????"
            aqApp.msgBoxWarning(wiki_error(traceback.format_exc(limit=-6, chain=False)), project._DGI)

        if caller is not None:
            try:
                if signal.signal != caller.signal_test.signal:
                    signal_name = signal.signal[1 : signal.signal.find("(")]  # Quitamos el caracter "2" inicial y parámetros
                    logger.debug("Emitir evento test: %s, args:%s kwargs:%s", signal_name, args if args else "", kwargs if kwargs else "")
                    caller.signal_test.emit(signal_name, sender)
            except Exception:
                pass

        return res

    return new_fn


def connect(sender, signal, receiver, slot, caller=None):
    if caller is not None:
        logger.debug("* * * Connect:: %s %s %s %s %s", caller, sender, signal, receiver, slot)
    else:
        logger.debug("? ? ? Connect:: %s %s %s %s", sender, signal, receiver, slot)
    signal_slot = solve_connection(sender, signal, receiver, slot)

    if not signal_slot:
        return False
    # http://pyqt.sourceforge.net/Docs/PyQt4/qt.html#ConnectionType-enum
    conntype = QtCore.Qt.QueuedConnection | QtCore.Qt.UniqueConnection
    new_signal, new_slot = signal_slot

    # if caller:
    #    for sl in caller._formconnections:
    #        if sl[0].signal == signal_slot[0].signal and sl[1].__name__ == signal_slot[1].__name__:
    #            return False

    try:
        slot_done_fn = slot_done(new_slot, new_signal, sender, caller)
        new_signal.connect(slot_done_fn, type=conntype)
        # new_signal.connect(new_slot, type=conntype)

    except Exception:
        # logger.exception("ERROR Connecting: %s %s %s %s", sender, signal, receiver, slot)
        return False

    signal_slot = new_signal, slot_done_fn
    return signal_slot


def disconnect(sender, signal, receiver, slot, caller=None):
    signal_slot = solve_connection(sender, signal, receiver, slot)
    if not signal_slot:
        return False
    signal, slot = signal_slot
    try:
        signal.disconnect(slot)
    except Exception:
        pass

    return signal_slot


def solve_connection(sender, signal, receiver, slot):
    if sender is None:
        logger.error("Connect Error:: %s %s %s %s", sender, signal, receiver, slot)
        return False

    m = re.search(r"^(\w+)\.(\w+)(\(.*\))?", slot)
    if slot.endswith("()"):
        slot = slot[:-2]

    if isinstance(sender, QDateEdit):
        if "valueChanged" in signal:
            signal = signal.replace("valueChanged", "dateChanged")

    if isinstance(sender, QTable):
        if "currentChanged" in signal:
            signal = signal.replace("currentChanged", "CurrentChanged")

    # if receiver.__class__.__name__ == "FormInternalObj" and slot == "accept":
    #    receiver = receiver.parent()

    remote_fn = getattr(receiver, slot, None)

    sg_name = re.sub(r" *\(.*\)", "", signal)
    oSignal = getattr(sender, sg_name, None)
    # if not oSignal and sender.__class__.__name__ == "FormInternalObj":
    #    oSignal = getattr(sender.parent(), sg_name, None)

    if not oSignal:
        logger.error("ERROR: No existe la señal %s para la clase %s", signal, sender.__class__.__name__)
        return

    if remote_fn:
        # if receiver.__class__.__name__ in ("FLFormSearchDB", "QDialog") and slot in ("accept", "reject"):
        #    return oSignal, remote_fn

        pS = ProxySlot(remote_fn, receiver, slot)
        proxyfn = pS.getProxyFn()
        return oSignal, proxyfn
    elif m:
        remote_obj = getattr(receiver, m.group(1), None)
        if remote_obj is None:
            raise AttributeError("Object %s not found on %s" % (remote_obj, str(receiver)))
        remote_fn = getattr(remote_obj, m.group(2), None)
        if remote_fn is None:
            raise AttributeError("Object %s not found on %s" % (remote_fn, remote_obj))
        return oSignal, remote_fn

    elif isinstance(receiver, QtCore.QObject):
        if isinstance(slot, str):
            oSlot = getattr(receiver, slot, None)
            if not oSlot:
                return False
        return oSignal, oSlot
    else:
        logger.error(
            "Al realizar connect %s:%s -> %s:%s ; " "el slot no se reconoce y el receptor no es QObject.", sender, signal, receiver, slot
        )
    return False


def GET(function_name, arguments=[], conn=None):
    if conn is None:
        conn = aqApp.db()
    if hasattr(conn.driver(), "send_to_server"):
        return conn.driver().send_to_server(pineboolib.utils.create_dict("call_function", function_name, conn.driver().id_, arguments))
    else:
        return "Funcionalidad no soportada"


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
        # print("HINT: Objetos referenciando %r::%r (%r) :" % (typename, obj, name))
        for ref in gc.get_referrers(obj):
            if isinstance(ref, dict):
                x = []
                for k, v in ref.items():
                    if v is obj:
                        k = "(**)" + k
                        x.insert(0, k)
                # print(" - dict:", repr(x), gc.get_referrers(ref))
            else:
                if "<frame" in str(repr(ref)):
                    continue
                # print(" - obj:", repr(ref), [x for x in dir(ref) if getattr(ref, x) is obj])

    threading.Thread(target=checkfn).start()


class QEventLoop(QtCore.QEventLoop):
    def exitLoop(self):
        super().exit()

    def enterLoop(self):
        super().exec_()


def print_stack(maxsize=1):
    for tb in traceback.format_list(traceback.extract_stack())[1:-2][-maxsize:]:
        print(tb.rstrip())


# Usadas solo por import *
# FIXME: No se debe usar import * !!!
from pineboolib.packager.aqunpacker import AQUnpacker  # noqa:
from pineboolib.fllegacy.flrelationmetadata import FLRelationMetaData  # noqa:
from pineboolib.fllegacy.aqsobjects.aqsobjectfactory import *  # noqa:
from pineboolib.fllegacy.flapplication import aqApp  # noqa:  # FIXME: Circular dependency

qsa_sys = SysType()

# --- create empty objects first:

QComboBox = ObjectNotFoundDGINotLoaded
QTable = ObjectNotFoundDGINotLoaded
QLayoutWidget = ObjectNotFoundDGINotLoaded
QToolButton = ObjectNotFoundDGINotLoaded
QTabWidget = ObjectNotFoundDGINotLoaded
QLabel = ObjectNotFoundDGINotLoaded
QGroupBox = ObjectNotFoundDGINotLoaded
QListView = ObjectNotFoundDGINotLoaded
QPushButton = ObjectNotFoundDGINotLoaded
QTextEdit = ObjectNotFoundDGINotLoaded
QLineEdit = ObjectNotFoundDGINotLoaded
QDateEdit = ObjectNotFoundDGINotLoaded
QTimeEdit = ObjectNotFoundDGINotLoaded
QCheckBox = ObjectNotFoundDGINotLoaded
QWidget = ObjectNotFoundDGINotLoaded
QtWidgets = ObjectNotFoundDGINotLoaded
QColor = ObjectNotFoundDGINotLoaded
QMessageBox = ObjectNotFoundDGINotLoaded
QButtonGroup = ObjectNotFoundDGINotLoaded
QDialog = ObjectNotFoundDGINotLoaded
QVBoxLayout = ObjectNotFoundDGINotLoaded
QHBoxLayout = ObjectNotFoundDGINotLoaded
QFrame = ObjectNotFoundDGINotLoaded
QMainWindow = ObjectNotFoundDGINotLoaded
QSignalMapper = ObjectNotFoundDGINotLoaded
QDomDocument = ObjectNotFoundDGINotLoaded
QMenu = ObjectNotFoundDGINotLoaded
QToolBar = ObjectNotFoundDGINotLoaded
QListWidgetItem = ObjectNotFoundDGINotLoaded
QListViewWidget = ObjectNotFoundDGINotLoaded
QPixmap = ObjectNotFoundDGINotLoaded
QImage = ObjectNotFoundDGINotLoaded
QIcon = ObjectNotFoundDGINotLoaded
QAction = ObjectNotFoundDGINotLoaded
QActionGroup = ObjectNotFoundDGINotLoaded
QTreeWidget = ObjectNotFoundDGINotLoaded
QTreeWidgetItem = ObjectNotFoundDGINotLoaded
QTreeWidgetItemIterator = ObjectNotFoundDGINotLoaded
QDataView = ObjectNotFoundDGINotLoaded
QProcess = ObjectNotFoundDGINotLoaded
QByteArray = ObjectNotFoundDGINotLoaded
QRadioButton = ObjectNotFoundDGINotLoaded
QSpinBox = ObjectNotFoundDGINotLoaded
QInputDialog = ObjectNotFoundDGINotLoaded
QLineEdit = ObjectNotFoundDGINotLoaded
QApplication = ObjectNotFoundDGINotLoaded
qApp = ObjectNotFoundDGINotLoaded
QStyleFactory = ObjectNotFoundDGINotLoaded
QFontDialog = ObjectNotFoundDGINotLoaded
QDockWidget = ObjectNotFoundDGINotLoaded
QMdiArea = ObjectNotFoundDGINotLoaded
QMdiSubWindow = ObjectNotFoundDGINotLoaded
QKeySequence = ObjectNotFoundDGINotLoaded
QSize = ObjectNotFoundDGINotLoaded
QSizePolicy = ObjectNotFoundDGINotLoaded
QToolBox = ObjectNotFoundDGINotLoaded
QPainter = ObjectNotFoundDGINotLoaded
QBrush = ObjectNotFoundDGINotLoaded
QProgressDialog = ObjectNotFoundDGINotLoaded
QFileDialog = ObjectNotFoundDGINotLoaded

# Clases FL
FLLineEdit = ObjectNotFoundDGINotLoaded
FLTimeEdit = ObjectNotFoundDGINotLoaded
FLDateEdit = ObjectNotFoundDGINotLoaded
FLPixmapView = ObjectNotFoundDGINotLoaded
FLDomDocument = ObjectNotFoundDGINotLoaded
FLDomElement = ObjectNotFoundDGINotLoaded
FLDomNode = ObjectNotFoundDGINotLoaded
FLDomNodeList = ObjectNotFoundDGINotLoaded
FLListViewItem = ObjectNotFoundDGINotLoaded
FLTable = ObjectNotFoundDGINotLoaded
FLDataTable = ObjectNotFoundDGINotLoaded
FLCheckBox = ObjectNotFoundDGINotLoaded
FLTextEditOutput = ObjectNotFoundDGINotLoaded
FLSpinBox = ObjectNotFoundDGINotLoaded
FLTableDB = ObjectNotFoundDGINotLoaded
FLFieldDB = ObjectNotFoundDGINotLoaded
FLFormDB = ObjectNotFoundDGINotLoaded
FLFormRecordDB = ObjectNotFoundDGINotLoaded
FLFormSearchDB = ObjectNotFoundDGINotLoaded
FLDoubleValidator = ObjectNotFoundDGINotLoaded
FLIntValidator = ObjectNotFoundDGINotLoaded
FLUIntValidator = ObjectNotFoundDGINotLoaded
FLCodBar = ObjectNotFoundDGINotLoaded
FLWidget = ObjectNotFoundDGINotLoaded
FLWorkSpace = ObjectNotFoundDGINotLoaded

FormDBWidget = ObjectNotFoundDGINotLoaded

# Clases QSA
CheckBox = ObjectNotFoundDGINotLoaded
ComboBox = ObjectNotFoundDGINotLoaded
TextEdit = ObjectNotFoundDGINotLoaded
LineEdit = ObjectNotFoundDGINotLoaded
FileDialog = ObjectNotFoundDGINotLoaded
MessageBox = ObjectNotFoundDGINotLoaded
RadioButton = ObjectNotFoundDGINotLoaded
Color = QColor
Dialog = ObjectNotFoundDGINotLoaded
Label = ObjectNotFoundDGINotLoaded
GroupBox = ObjectNotFoundDGINotLoaded
Process = ObjectNotFoundDGINotLoaded
SpinBox = ObjectNotFoundDGINotLoaded
Line = ObjectNotFoundDGINotLoaded
NumberEdit = ObjectNotFoundDGINotLoaded
DateEdit = ObjectNotFoundDGINotLoaded
TimeEdit = ObjectNotFoundDGINotLoaded

# Clases AQNext
auth = ObjectNotFoundDGINotLoaded
