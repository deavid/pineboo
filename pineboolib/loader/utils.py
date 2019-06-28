import traceback
import logging

logger = logging.getLogger(__name__)


def addLoggingLevel(levelName, levelNum, methodName=None):
    """
    Comprehensively adds a new logging level to the `logging` module and the
    currently configured logging class.

    `levelName` becomes an attribute of the `logging` module with the value
    `levelNum`. `methodName` becomes a convenience method for both `logging`
    itself and the class returned by `logging.getLoggerClass()` (usually just
    `logging.Logger`). If `methodName` is not specified, `levelName.lower()` is
    used.

    To avoid accidental clobberings of existing attributes, this method will
    raise an `AttributeError` if the level name is already an attribute of the
    `logging` module or if the method name is already present

    Example
    -------
    >>> addLoggingLevel('TRACE', logging.DEBUG - 5)
    >>> logging.getLogger(__name__).setLevel("TRACE")
    >>> logging.getLogger(__name__).trace('that worked')
    >>> logging.trace('so did this')
    >>> logging.TRACE
    5

    """
    if not methodName:
        methodName = levelName.lower()

    if hasattr(logging, levelName):
        raise AttributeError("{} already defined in logging module".format(levelName))
    if hasattr(logging, methodName):
        raise AttributeError("{} already defined in logging module".format(methodName))
    if hasattr(logging.getLoggerClass(), methodName):
        raise AttributeError("{} already defined in logger class".format(methodName))

    # This method was inspired by the answers to Stack Overflow post
    # http://stackoverflow.com/q/2183233/2988730, especially
    # http://stackoverflow.com/a/13638084/2988730
    def logForLevel(self, message, *args, **kwargs):
        if self.isEnabledFor(levelNum):
            self._log(levelNum, message, args, **kwargs)

    def logToRoot(message, *args, **kwargs):
        logging.log(levelNum, message, *args, **kwargs)

    logging.addLevelName(levelNum, levelName)
    setattr(logging, levelName, levelNum)
    setattr(logging.getLoggerClass(), methodName, logForLevel)
    setattr(logging, methodName, logToRoot)


def monkey_patch_connect():
    """Patch Qt5 signal/event functions for tracing them.

    This is not stable and should be used with care
    """
    from PyQt5 import QtCore

    logger.warning("--trace-signals es experimental. Tiene problemas de memoria y falla en llamadas con un argumento (False)")
    logger.warning("... se desaconseja su uso excepto para depurar. Puede cambiar el comportamiento del programa.")

    class BoundSignal:
        _CONNECT = QtCore.pyqtBoundSignal.connect
        _EMIT = QtCore.pyqtBoundSignal.emit
        _LAST_EMITTED_SIGNAL = {}

        def slot_decorator(self, slot, connect_stack):
            selfid = repr(self)

            def decorated_slot(*args):
                ret = None
                if len(args) == 1 and args[0] is False:
                    args = []
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

        def connect(self, slot, type_=0, no_receiver_check=False):
            """Proxy a connection to the original connect in the Qt library.

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

        def emit(self, *args):
            """Proxy original Qt Emit function for tracing signal emits."""
            # print("Emit: %s :: %r" % (self, args))
            stack = traceback.extract_stack()
            # print(traceback.format_list(stack)[-2].rstrip())
            BoundSignal._LAST_EMITTED_SIGNAL[repr(self)] = stack
            return BoundSignal._EMIT(self, *args)

    QtCore.pyqtBoundSignal.connect = BoundSignal.connect
    QtCore.pyqtBoundSignal.emit = BoundSignal.emit
