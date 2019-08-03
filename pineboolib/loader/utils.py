"""
Utilities for loading pineboo.
"""
import traceback
from pineboolib import logging
from typing import Dict, Any, Callable

logger = logging.getLogger(__name__)


def monkey_patch_connect() -> None:
    """
    Patch Qt5 signal/event functions for tracing them.

    This is not stable and should be used with care
    """
    from PyQt5 import QtCore  # type: ignore

    logger.warning("--trace-signals es experimental. Tiene problemas de memoria y falla en llamadas con un argumento (False)")
    logger.warning("... se desaconseja su uso excepto para depurar. Puede cambiar el comportamiento del programa.")

    class BoundSignal:
        _CONNECT = QtCore.pyqtBoundSignal.connect  # type: ignore
        _EMIT = QtCore.pyqtBoundSignal.emit
        _LAST_EMITTED_SIGNAL: Dict[str, Any] = {}

        def slot_decorator(self: Any, slot: Callable, connect_stack: Any) -> Callable:
            selfid = repr(self)

            def decorated_slot(*args: Any) -> Any:
                ret = None
                if len(args) == 1 and args[0] is False:
                    args = tuple()
                try:
                    # print("Calling slot: %r %r" % (slot, args))
                    ret = slot(*args)
                except Exception:
                    logger.error("Unhandled exception in slot %r (%r): %r" % (slot, self, args))
                    logger.error("-- Connection --")
                    logger.error(traceback.format_list(connect_stack)[-2].rstrip())
                    last_emit_stack = BoundSignal._LAST_EMITTED_SIGNAL.get(selfid, None)
                    if last_emit_stack:
                        logger.error("-- Last signal emmitted --")
                        logger.error(traceback.format_list(last_emit_stack)[-2].rstrip())
                    logger.error("-- Slot traceback --")
                    logger.error(traceback.format_exc())
                return ret

            return decorated_slot

        def connect(self: Any, slot: Any, type_: int = 0, no_receiver_check: bool = False) -> Any:
            """
            Proxy a connection to the original connect in the Qt library.

            This function wraps on top of the original Qt.connect so everything
            is logged.

            slot is either a Python callable or another signal.
            type is a Qt.ConnectionType. (default Qt.AutoConnection = 0)
            no_receiver_check is True to disable the check that the receiver's C++
            instance still exists when the signal is emitted.
            """
            clname = getattr(getattr(slot, "__class__", {}), "__name__", "not a class")
            # print("Connect: %s -> %s" % (type(self), slot))
            if clname == "method":
                stack = traceback.extract_stack()
                newslot = BoundSignal.slot_decorator(self, slot, stack)
            else:
                newslot = slot
            return BoundSignal._CONNECT(self, newslot, type_, no_receiver_check)

        def emit(self: Any, *args: Any) -> Any:
            """Proxy original Qt Emit function for tracing signal emits."""
            # print("Emit: %s :: %r" % (self, args))
            stack = traceback.extract_stack()
            # print(traceback.format_list(stack)[-2].rstrip())
            BoundSignal._LAST_EMITTED_SIGNAL[repr(self)] = stack
            return BoundSignal._EMIT(self, *args)

    QtCore.pyqtBoundSignal.connect = BoundSignal.connect  # type: ignore
    QtCore.pyqtBoundSignal.emit = BoundSignal.emit  # type: ignore
