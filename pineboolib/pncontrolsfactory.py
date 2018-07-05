# -*- coding: utf-8 -*-
import re
from PyQt5 import QtCore
from PyQt5.QtWidgets import qApp

import pineboolib
import logging
import weakref
from pineboolib import decorators


logger = logging.getLogger("PNControlsFactory")

"""
Conjunto de controles usados en Pineboo. Estos son cargados desde el DGI seleccionado en el proyecto
"""

"""
Devuelve un objecto a partir de su nombre
@param name, Nombre del objecto a buscar
@return objecto o None si no existe el objeto buscado
"""


def resolveObject(name):
    ret_ = pineboolib.project.resolveDGIObject(name)
    return ret_


QComboBox = resolveObject("QComboBox")
QTable = resolveObject("QTable")
QLayoutWidget = resolveObject("QLayoutWidget")
QTabWidget = resolveObject("QTabWidget")
QLabel = resolveObject("QLabel")
QGroupBox = resolveObject("QGroupBox")
QListView = resolveObject("QListView")
QPushButton = resolveObject("QPushButton")
QTextEdit = resolveObject("QTextEdit")
QLineEdit = resolveObject("QLineEdit")
QDateEdit = resolveObject("QDateEdit")
QCheckBox = resolveObject("QCheckBox")
FLLineEdit = resolveObject("FLLineEdit")
FLTimeEdit = resolveObject("FLTimeEdit")
FLDateEdit = resolveObject("FLDateEdit")
FLPixmapView = resolveObject("FLPixmapView")


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


def proxy_fn(wf, wr, slot):
    def fn(*args, **kwargs):
        f = wf()
        if not f:
            return None
        r = wr()
        if not r:
            return None

        # Apaño para conectar los clicked()
        if args == (False,):
            return f()

        return f(*args, **kwargs)
    return fn


def connect(sender, signal, receiver, slot, caller=None):
    if caller is not None:
        logger.debug("* * * Connect::", caller, sender, signal, receiver, slot)
    else:
        logger.debug("? ? ? Connect::", sender, signal, receiver, slot)
    signal_slot = solve_connection(sender, signal, receiver, slot)
    if not signal_slot:
        return False
    # http://pyqt.sourceforge.net/Docs/PyQt4/qt.html#ConnectionType-enum
    conntype = QtCore.Qt.QueuedConnection | QtCore.Qt.UniqueConnection
    signal, slot = signal_slot

    try:
        signal.connect(slot, type=conntype)
    except Exception:
        logger.exception("ERROR Connecting: %s %s %s %s", sender, signal, receiver, slot)
        return False

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

    if receiver.__class__.__name__ == "FormInternalObj" and slot == "accept":
        receiver = receiver.parent()

    remote_fn = getattr(receiver, slot, None)

    sg_name = re.sub(' *\(.*\)', '', signal)
    oSignal = getattr(sender, sg_name, None)
    if not oSignal and sender.__class__.__name__ == "FormInternalObj":
        oSignal = getattr(sender.parent(), sg_name, None)
    if not oSignal:
        logger.error("ERROR: No existe la señal %s para la clase %s", signal, sender.__class__.__name__)
        return

    if remote_fn:
        if receiver.__class__.__name__ == "FLFormSearchDB" and slot == "accept":
            return oSignal, remote_fn

        pS = ProxySlot(remote_fn, receiver, slot)
        proxyfn = pS.getProxyFn()
        return oSignal, proxyfn
    elif m:
        remote_obj = getattr(receiver, m.group(1), None)
        if remote_obj is None:
            raise AttributeError("Object %s not found on %s" %
                                 (remote_obj, str(receiver)))
        remote_fn = getattr(remote_obj, m.group(2), None)
        if remote_fn is None:
            raise AttributeError("Object %s not found on %s" %
                                 (remote_fn, remote_obj))
        return oSignal, remote_fn

    elif isinstance(receiver, QtCore.QObject):
        if isinstance(slot, str):
            oSlot = getattr(receiver, slot, None)
            if not oSlot:
                return False
        return oSignal, oSlot
    else:
        logger.error(
            "Al realizar connect %s:%s -> %s:%s ; "
            "el slot no se reconoce y el receptor no es QObject.",
            sender, signal, receiver, slot)
    return False
