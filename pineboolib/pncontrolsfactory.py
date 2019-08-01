# -*- coding: utf-8 -*-
import inspect
import weakref
import re
import os
import traceback

from PyQt5 import QtCore  # type: ignore
from pineboolib.core.utils import logging
from pineboolib.application import project
from pineboolib.fllegacy.systype import SysType
import types
from typing import Callable, Any, List, Tuple, Optional, Dict


logger = logging.getLogger("PNControlsFactory")

"""
Conjunto de controles usados en Pineboo. Estos son cargados desde el DGI seleccionado en el proyecto
"""


class ObjectNotFoundInCurrentDGI(object):
    pass


class ObjectNotFoundDGINotLoaded(object):
    def __init__(self, *args: List[Any]):
        pass


aqApp: Any = ObjectNotFoundDGINotLoaded

# --- create empty objects first:
QComboBox: Any = ObjectNotFoundDGINotLoaded
QTable: Any = ObjectNotFoundDGINotLoaded
QLayoutWidget: Any = ObjectNotFoundDGINotLoaded
QToolButton: Any = ObjectNotFoundDGINotLoaded
QTabWidget: Any = ObjectNotFoundDGINotLoaded
QLabel: Any = ObjectNotFoundDGINotLoaded
QGroupBox: Any = ObjectNotFoundDGINotLoaded
QListView: Any = ObjectNotFoundDGINotLoaded
QPushButton: Any = ObjectNotFoundDGINotLoaded
QTextEdit: Any = ObjectNotFoundDGINotLoaded
QLineEdit: Any = ObjectNotFoundDGINotLoaded
QDateEdit: Any = ObjectNotFoundDGINotLoaded
QTimeEdit: Any = ObjectNotFoundDGINotLoaded
QCheckBox: Any = ObjectNotFoundDGINotLoaded
QWidget: Any = ObjectNotFoundDGINotLoaded
QtWidgets: Any = ObjectNotFoundDGINotLoaded
QColor: Any = ObjectNotFoundDGINotLoaded
QMessageBox: Any = ObjectNotFoundDGINotLoaded
QButtonGroup: Any = ObjectNotFoundDGINotLoaded
QDialog: Any = ObjectNotFoundDGINotLoaded
QVBoxLayout: Any = ObjectNotFoundDGINotLoaded
QHBoxLayout: Any = ObjectNotFoundDGINotLoaded
QFrame: Any = ObjectNotFoundDGINotLoaded
QMainWindow: Any = ObjectNotFoundDGINotLoaded
QSignalMapper: Any = ObjectNotFoundDGINotLoaded
QDomDocument: Any = ObjectNotFoundDGINotLoaded
QMenu: Any = ObjectNotFoundDGINotLoaded
QToolBar: Any = ObjectNotFoundDGINotLoaded
QListWidgetItem: Any = ObjectNotFoundDGINotLoaded
QListViewWidget: Any = ObjectNotFoundDGINotLoaded
QPixmap: Any = ObjectNotFoundDGINotLoaded
QImage: Any = ObjectNotFoundDGINotLoaded
QIcon: Any = ObjectNotFoundDGINotLoaded
QAction: Any = ObjectNotFoundDGINotLoaded
QActionGroup: Any = ObjectNotFoundDGINotLoaded
QTreeWidget: Any = ObjectNotFoundDGINotLoaded
QTreeWidgetItem: Any = ObjectNotFoundDGINotLoaded
QTreeWidgetItemIterator: Any = ObjectNotFoundDGINotLoaded
QDataView: Any = ObjectNotFoundDGINotLoaded
QProcess: Any = ObjectNotFoundDGINotLoaded
QByteArray: Any = ObjectNotFoundDGINotLoaded
QRadioButton: Any = ObjectNotFoundDGINotLoaded
QSpinBox: Any = ObjectNotFoundDGINotLoaded
QInputDialog: Any = ObjectNotFoundDGINotLoaded
QApplication: Any = ObjectNotFoundDGINotLoaded
qApp: Any = ObjectNotFoundDGINotLoaded
QStyleFactory: Any = ObjectNotFoundDGINotLoaded
QFontDialog: Any = ObjectNotFoundDGINotLoaded
QDockWidget: Any = ObjectNotFoundDGINotLoaded
QMdiArea: Any = ObjectNotFoundDGINotLoaded
QMdiSubWindow: Any = ObjectNotFoundDGINotLoaded
QKeySequence: Any = ObjectNotFoundDGINotLoaded
QSize: Any = ObjectNotFoundDGINotLoaded
QSizePolicy: Any = ObjectNotFoundDGINotLoaded
QToolBox: Any = ObjectNotFoundDGINotLoaded
QPainter: Any = ObjectNotFoundDGINotLoaded
QBrush: Any = ObjectNotFoundDGINotLoaded
QProgressDialog: Any = ObjectNotFoundDGINotLoaded
QFileDialog: Any = ObjectNotFoundDGINotLoaded

# Clases FL
FLLineEdit: Any = ObjectNotFoundDGINotLoaded
FLTimeEdit: Any = ObjectNotFoundDGINotLoaded
FLDateEdit: Any = ObjectNotFoundDGINotLoaded
FLPixmapView: Any = ObjectNotFoundDGINotLoaded
FLDomDocument: Any = ObjectNotFoundDGINotLoaded
FLDomElement: Any = ObjectNotFoundDGINotLoaded
FLDomNode: Any = ObjectNotFoundDGINotLoaded
FLDomNodeList: Any = ObjectNotFoundDGINotLoaded
FLListViewItem: Any = ObjectNotFoundDGINotLoaded
FLTable: Any = ObjectNotFoundDGINotLoaded
FLDataTable: Any = ObjectNotFoundDGINotLoaded
FLCheckBox: Any = ObjectNotFoundDGINotLoaded
FLTextEditOutput: Any = ObjectNotFoundDGINotLoaded
FLSpinBox: Any = ObjectNotFoundDGINotLoaded
FLTableDB: Any = ObjectNotFoundDGINotLoaded
FLFieldDB: Any = ObjectNotFoundDGINotLoaded
FLFormDB: Any = ObjectNotFoundDGINotLoaded
FLFormRecordDB: Any = ObjectNotFoundDGINotLoaded
FLFormSearchDB: Any = ObjectNotFoundDGINotLoaded
FLDoubleValidator: Any = ObjectNotFoundDGINotLoaded
FLIntValidator: Any = ObjectNotFoundDGINotLoaded
FLUIntValidator: Any = ObjectNotFoundDGINotLoaded
FLCodBar: Any = ObjectNotFoundDGINotLoaded
FLWidget: Any = ObjectNotFoundDGINotLoaded
FLWorkSpace: Any = ObjectNotFoundDGINotLoaded

FormDBWidget: Any = ObjectNotFoundDGINotLoaded

# Clases QSA
CheckBox: Any = ObjectNotFoundDGINotLoaded
ComboBox: Any = ObjectNotFoundDGINotLoaded
TextEdit: Any = ObjectNotFoundDGINotLoaded
LineEdit: Any = ObjectNotFoundDGINotLoaded
FileDialog: Any = ObjectNotFoundDGINotLoaded
MessageBox: Any = ObjectNotFoundDGINotLoaded
RadioButton: Any = ObjectNotFoundDGINotLoaded
Color = QColor
Dialog: Any = ObjectNotFoundDGINotLoaded
Label: Any = ObjectNotFoundDGINotLoaded
GroupBox: Any = ObjectNotFoundDGINotLoaded
Process: Any = ObjectNotFoundDGINotLoaded
SpinBox: Any = ObjectNotFoundDGINotLoaded
Line: Any = ObjectNotFoundDGINotLoaded
NumberEdit: Any = ObjectNotFoundDGINotLoaded
DateEdit: Any = ObjectNotFoundDGINotLoaded
TimeEdit: Any = ObjectNotFoundDGINotLoaded

# Clases AQNext
auth: Any = ObjectNotFoundDGINotLoaded


def resolveObject(name: str) -> Any:
    if not project._DGI:
        return ObjectNotFoundDGINotLoaded
    obj_ = getattr(project._DGI, name, None)
    if obj_:
        return obj_

    logger.warning("resolveObject: class <%s> not found in dgi <%s>", name, project.DGI.alias().lower())
    return ObjectNotFoundInCurrentDGI


def reload_from_DGI() -> None:
    # Clases Qt
    global QComboBox, QTable, QLayoutWidget, QToolButton, QTabWidget, QLabel, QGroupBox, QListView, QPushButton, QTextEdit
    global QLineEdit, QDateEdit, QTimeEdit, QCheckBox, QWidget, QtWidgets, QColor, QMessageBox, QButtonGroup, QDialog
    global QVBoxLayout, QHBoxLayout, QFrame, QMainWindow, QSignalMapper, QDomDocument, QMenu, QToolBar, QListWidgetItem, QListViewWidget
    global QPixmap, QImage, QIcon, QAction, QActionGroup, QTreeWidget, QTreeWidgetItem, QTreeWidgetItemIterator, QDataView
    global QProcess, QByteArray, QRadioButton, QSpinBox, QInputDialog, QApplication, qApp, QStyleFactory, QFontDialog
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


class System_class(object):
    @staticmethod
    def setenv(name: str, val: str) -> None:
        os.environ[name] = val

    @staticmethod
    def getenv(name: str) -> str:
        ret_ = ""
        if name in os.environ.keys():
            ret_ = os.environ[name]

        return ret_


class ProxySlot:
    PROXY_FUNCTIONS: Dict[str, Callable] = {}

    def __init__(self, remote_fn: types.MethodType, receiver: Any, slot: Any) -> None:
        self.key = "%r.%r->%r" % (remote_fn, receiver, slot)
        if self.key not in self.PROXY_FUNCTIONS:
            weak_fn = weakref.WeakMethod(remote_fn)
            weak_receiver = weakref.ref(receiver)
            self.PROXY_FUNCTIONS[self.key] = proxy_fn(weak_fn, weak_receiver, slot)
        self.proxy_function = self.PROXY_FUNCTIONS[self.key]

    def getProxyFn(self) -> Callable:
        return self.proxy_function


def get_expected_args_num(inspected_function: Callable) -> int:
    expected_args = inspect.getargspec(inspected_function)[0]
    args_num = len(expected_args)

    if args_num and expected_args[0] == "self":
        args_num -= 1

    return args_num


def get_expected_kwargs(inspected_function: Callable) -> bool:
    expected_kwargs = inspect.getfullargspec(inspected_function)[2]
    return True if expected_kwargs else False


def proxy_fn(wf: weakref.WeakMethod, wr: weakref.ref, slot: Any) -> Callable:
    def fn(*args: List[Any], **kwargs: Dict[str, Any]) -> Optional[Any]:
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


def slot_done(fn: Callable, signal: Any, sender: Any, caller: Any) -> Callable:
    def new_fn(*args: List[Any], **kwargs: Dict[str, Any]) -> Any:

        res = False

        # Este parche es para evitar que las conexiones de un clicked de error de cantidad de argumentos.
        # En Eneboo se esperaba que signal no contenga argumentos
        if signal.signal == "2clicked(bool)":
            args = tuple()
        # args_num = get_expected_args_num(fn)
        try:
            if get_expected_kwargs(fn):
                # res = fn(*args[0:args_num], **kwargs)
                res = fn(*args, **kwargs)
            else:
                # res = fn(*args[0:args_num])
                res = fn(*args)

        except Exception:
            logger.exception("Error trying to create a connection")

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


def connect(sender: Any, signal: Any, receiver: Any, slot: str, caller: Any = None) -> Optional[Tuple[Any, Any]]:
    if caller is not None:
        logger.trace("* * * Connect:: %s %s %s %s %s", caller, sender, signal, receiver, slot)
    else:
        logger.trace("? ? ? Connect:: %s %s %s %s", sender, signal, receiver, slot)
    signal_slot = solve_connection(sender, signal, receiver, slot)

    if not signal_slot:
        return None
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
        logger.warning("ERROR Connecting: %s %s %s %s", sender, signal, receiver, slot)
        return None

    signal_slot = new_signal, slot_done_fn
    return signal_slot


def disconnect(sender: Any, signal: Any, receiver: Any, slot: str, caller: Any = None) -> Optional[Tuple[Any, Any]]:
    signal_slot = solve_connection(sender, signal, receiver, slot)
    if not signal_slot:
        return None
    signal, slot = signal_slot
    try:
        signal.disconnect(slot)
    except Exception:
        pass

    return signal_slot


def solve_connection(sender: Any, signal: str, receiver: Any, slot: str) -> Optional[Tuple[Any, Any]]:
    if sender is None:
        logger.error("Connect Error:: %s %s %s %s", sender, signal, receiver, slot)
        return None

    m = re.search(r"^(\w+)\.(\w+)(\(.*\))?", slot)
    if slot.endswith("()"):
        slot = slot[:-2]

    if isinstance(sender, QDateEdit):
        if "valueChanged" in signal:
            signal = signal.replace("valueChanged", "dateChanged")

    if isinstance(sender, QTable):
        if "CurrentChanged" in signal:
            signal = signal.replace("CurrentChanged", "currentChanged")

    # if receiver.__class__.__name__ == "FormInternalObj" and slot == "accept":
    #    receiver = receiver.parent()
    remote_fn = None
    if slot.find(".") > -1:
        slot_list = slot.split(".")
        remote_fn = receiver
        for slot_ in slot_list:
            remote_fn = getattr(remote_fn, slot_, None)

            if remote_fn is None:
                break

    else:
        remote_fn = getattr(receiver, slot, None)

    sg_name = re.sub(r" *\(.*\)", "", signal)
    oSignal = getattr(sender, sg_name, None)
    # if not oSignal and sender.__class__.__name__ == "FormInternalObj":
    #    oSignal = getattr(sender.parent(), sg_name, None)
    if not oSignal:
        logger.error("ERROR: No existe la señal %s para la clase %s", signal, sender.__class__.__name__)
        return None

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
                if hasattr(receiver, "iface"):
                    oSlot = getattr(receiver.iface, slot, None)
            if not oSlot:
                logger.error("Al realizar connect %s:%s -> %s:%s ; " "el es QObject pero no tiene slot", sender, signal, receiver, slot)
                return None
            return oSignal, oSlot
    else:
        logger.error(
            "Al realizar connect %s:%s -> %s:%s ; " "el slot no se reconoce y el receptor no es QObject.", sender, signal, receiver, slot
        )
    return None


# FIXME: Belongs to RPC drivers
# def GET(function_name, arguments=[], conn=None) -> Any:
#     if conn is None:
#         conn = project.conn
#     if hasattr(conn.driver(), "send_to_server"):
#         return conn.driver().send_to_server(create_dict("call_function", function_name, conn.driver().id_, arguments))
#     else:
#         return "Funcionalidad no soportada"


def check_gc_referrers(typename: Any, w_obj: Callable, name: str) -> None:
    import threading
    import time

    def checkfn() -> None:
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
                x: List[str] = []
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
    def exitLoop(self) -> None:
        super().exit()

    def enterLoop(self) -> None:
        super().exec_()


def print_stack(maxsize: int = 1) -> None:
    for tb in traceback.format_list(traceback.extract_stack())[1:-2][-maxsize:]:
        print(tb.rstrip())


# Usadas solo por import *
# FIXME: No se debe usar import * !!!
from pineboolib.application.packager.aqunpacker import AQUnpacker  # noqa:

from pineboolib.fllegacy.aqsobjects.aqsobjectfactory import *  # noqa:

# aqApp -- imported from loader.main after reload_from_DGI() call, as it is a cyclic dependency

# System = System_class()
# qsa_sys = SysType()
qsa_sys: SysType
System: System_class
