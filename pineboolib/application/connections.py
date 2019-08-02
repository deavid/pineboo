"""
Manage Qt Signal-Slot connections.
"""
import inspect
import weakref
import re
import types

from pineboolib.qt3_widgets.qdateedit import QDateEdit
from pineboolib.qt3_widgets.qtable import QTable

from pineboolib.core.utils import logging

from PyQt5 import QtCore

from typing import Callable, Any, List, Dict, Tuple, Optional

logger = logging.getLogger("application.connections")


class ProxySlot:
    """
    Proxies a method so it doesn't need to be resolved on connect.
    """

    PROXY_FUNCTIONS: Dict[str, Callable] = {}

    def __init__(self, remote_fn: types.MethodType, receiver: Any, slot: Any) -> None:
        """Create a proxy for a method."""
        self.key = "%r.%r->%r" % (remote_fn, receiver, slot)
        if self.key not in self.PROXY_FUNCTIONS:
            weak_fn = weakref.WeakMethod(remote_fn)
            weak_receiver = weakref.ref(receiver)
            self.PROXY_FUNCTIONS[self.key] = proxy_fn(weak_fn, weak_receiver, slot)
        self.proxy_function = self.PROXY_FUNCTIONS[self.key]

    def getProxyFn(self) -> Callable:
        """Retrieve internal proxy function."""
        return self.proxy_function


def get_expected_args_num(inspected_function: Callable) -> int:
    """Inspect function to get how many arguments expects."""
    expected_args = inspect.getargspec(inspected_function)[0]
    args_num = len(expected_args)

    if args_num and expected_args[0] == "self":
        args_num -= 1

    return args_num


def get_expected_kwargs(inspected_function: Callable) -> bool:
    """Inspect a function to get if expects keyword args."""
    expected_kwargs = inspect.getfullargspec(inspected_function)[2]
    return True if expected_kwargs else False


def proxy_fn(wf: weakref.WeakMethod, wr: weakref.ref, slot: Any) -> Callable:
    """Create a proxied function, so it does not hold the garbage collector."""

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
    """Create a fake slot for QS connects."""

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
    """Connect signal to slot for QSA."""
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
    """Disconnect signal from slot for QSA."""
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
    """Try hard to guess which is the correct way of connecting signal to slot. For QSA."""
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
