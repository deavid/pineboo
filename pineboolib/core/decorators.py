# -*- coding: utf-8 -*-
import time
import re
import functools
from .utils import logging
from PyQt5 import QtCore  # type: ignore

"""
Esta libreria se usa para especificar estados de una función que no son final
"""
from typing import Callable, Any, Dict, TypeVar, cast

T_FN = TypeVar("T_FN", bound=Callable[..., Any])

logger = logging.getLogger(__name__)
MSG_EMITTED: Dict[str, float] = {}
CLEAN_REGEX = re.compile(r"\s*object\s+at\s+0x[0-9a-zA-Z]{6,38}", re.VERBOSE)
MINIMUM_TIME_FOR_REPRINT = 300


def clean_repr(x: Any) -> str:
    return CLEAN_REGEX.sub("", repr(x))


"""
Aviso no implementado
"""


def NotImplementedWarn(fn: T_FN) -> T_FN:
    @functools.wraps(fn)
    def newfn(*args, **kwargs):
        global MSG_EMITTED
        ret = fn(*args, **kwargs)
        x_args = [clean_repr(a) for a in args] + ["%s=%s" % (k, clean_repr(v)) for k, v in list(kwargs.items())]
        keyname = fn.__name__ + repr(x_args)
        now = time.time()
        if keyname not in MSG_EMITTED or now - MSG_EMITTED[keyname] > MINIMUM_TIME_FOR_REPRINT:
            MSG_EMITTED[keyname] = now
            logger.warning("Not yet impl.: %s(%s) -> %s", fn.__name__, ", ".join(x_args), repr(ret))
            logger.trace("Not yet impl.: %s(%s) -> %s", fn.__name__, ", ".join(x_args), repr(ret), stack_info=True)
        return ret

    mock_fn: T_FN = cast(T_FN, newfn)  # type: ignore
    return mock_fn


"""
Aviso no implementado. Igual que la anterior, pero solo informa en caso de debug
"""


def NotImplementedDebug(fn: T_FN) -> T_FN:
    @functools.wraps(fn)
    def newfn(*args, **kwargs):
        global MSG_EMITTED
        ret = fn(*args, **kwargs)
        x_args = [clean_repr(a) for a in args] + ["%s=%s" % (k, clean_repr(v)) for k, v in list(kwargs.items())]
        keyname = fn.__name__ + repr(x_args)
        now = time.time()
        if keyname not in MSG_EMITTED or now - MSG_EMITTED[keyname] > MINIMUM_TIME_FOR_REPRINT:
            MSG_EMITTED[keyname] = now
            logger.debug("Not yet impl.: %s(%s) -> %s", fn.__name__, ", ".join(x_args), repr(ret))
        return ret

    mock_fn: T_FN = cast(T_FN, newfn)  # type: ignore
    return mock_fn


"""
Avisa que hay otro desarollador trabajando en una función
"""


def WorkingOnThis(fn: T_FN) -> T_FN:
    @functools.wraps(fn)
    def newfn(*args, **kwargs):
        global MSG_EMITTED
        ret = fn(*args, **kwargs)
        x_args = [clean_repr(a) for a in args] + ["%s=%s" % (k, clean_repr(v)) for k, v in list(kwargs.items())]
        keyname = fn.__name__ + repr(x_args)
        now = time.time()
        if keyname not in MSG_EMITTED or now - MSG_EMITTED[keyname] > MINIMUM_TIME_FOR_REPRINT:
            MSG_EMITTED[keyname] = now
            logger.info("WARN: In Progress: %s(%s) -> %s", fn.__name__, ", ".join(x_args), repr(ret))
        return ret

    mock_fn: T_FN = cast(T_FN, newfn)  # type: ignore
    return mock_fn


"""
Aviso de implementación de una función en pruebas
"""


def BetaImplementation(fn: T_FN) -> T_FN:
    @functools.wraps(fn)
    def newfn(*args, **kwargs):
        global MSG_EMITTED
        ret = fn(*args, **kwargs)
        x_args = [clean_repr(a) for a in args] + ["%s=%s" % (k, clean_repr(v)) for k, v in list(kwargs.items())]
        keyname = fn.__name__ + repr(x_args)
        now = time.time()
        if keyname not in MSG_EMITTED or now - MSG_EMITTED[keyname] > MINIMUM_TIME_FOR_REPRINT:
            MSG_EMITTED[keyname] = now
            logger.info("WARN: Beta impl.: %s(%s) -> %s", fn.__name__, ", ".join(x_args), repr(ret))
        return ret

    mock_fn: T_FN = cast(T_FN, newfn)  # type: ignore
    return mock_fn


"""
Similar a NotImplemented, pero sin traceback. Para funciones que de momento no necesitamos (clonadas del motor C++ por ejemplo)
"""


def Empty(fn: T_FN) -> T_FN:
    @functools.wraps(fn)
    def newfn(*args, **kwargs):
        global MSG_EMITTED
        ret = fn(*args, **kwargs)
        x_args = [clean_repr(a) for a in args] + ["%s=%s" % (k, clean_repr(v)) for k, v in list(kwargs.items())]
        keyname = fn.__name__
        now = time.time()
        if keyname not in MSG_EMITTED or now - MSG_EMITTED[keyname] > MINIMUM_TIME_FOR_REPRINT:
            MSG_EMITTED[keyname] = now
            logger.info("WARN: Empty: %s(%s) -> %s", fn.__name__, ", ".join(x_args), repr(ret))
        return ret

    mock_fn: T_FN = cast(T_FN, newfn)  # type: ignore
    return mock_fn


"""
Avisa de que la funcionalidad está incompleta de desarrollo
"""


def Incomplete(fn: T_FN) -> T_FN:
    @functools.wraps(fn)
    def newfn(*args, **kwargs):
        global MSG_EMITTED
        ret = fn(*args, **kwargs)
        x_args = [clean_repr(a) for a in args] + ["%s=%s" % (k, clean_repr(v)) for k, v in list(kwargs.items())]
        keyname = fn.__name__ + repr(x_args)
        now = time.time()
        if keyname not in MSG_EMITTED or now - MSG_EMITTED[keyname] > MINIMUM_TIME_FOR_REPRINT:
            MSG_EMITTED[keyname] = now
            logger.info("WARN: Incomplete: %s(%s) -> %s", fn.__name__, ", ".join(x_args), repr(ret))
        return ret

    mock_fn: T_FN = cast(T_FN, newfn)  # type: ignore
    return mock_fn


"""
Avisa de que la funcionalidad tiene que ser revisada
"""


def needRevision(fn: T_FN) -> T_FN:
    def newfn(*args, **kwargs):
        global MSG_EMITTED
        ret = fn(*args, **kwargs)
        x_args = [clean_repr(a) for a in args] + ["%s=%s" % (k, clean_repr(v)) for k, v in list(kwargs.items())]
        keyname = fn.__name__ + repr(x_args)
        now = time.time()
        if keyname not in MSG_EMITTED or now - MSG_EMITTED[keyname] > MINIMUM_TIME_FOR_REPRINT:
            MSG_EMITTED[keyname] = now
            logger.info("WARN: Needs help: %s(%s) -> %s", fn.__name__, ", ".join(x_args), repr(ret))
        return ret

    mock_fn: T_FN = cast(T_FN, newfn)  # type: ignore
    return mock_fn


"""
Avisa de que la funcionalidad está dejando de ser usada, en pro de otra
"""


def Deprecated(fn: T_FN) -> T_FN:
    @functools.wraps(fn)
    def newfn(*args, **kwargs):
        global MSG_EMITTED
        ret = fn(*args, **kwargs)
        x_args = [clean_repr(a) for a in args] + ["%s=%s" % (k, clean_repr(v)) for k, v in list(kwargs.items())]
        keyname = fn.__name__ + repr(x_args)
        now = time.time()
        if keyname not in MSG_EMITTED or now - MSG_EMITTED[keyname] > MINIMUM_TIME_FOR_REPRINT:
            MSG_EMITTED[keyname] = now
            logger.info("WARN: Deprecated: %s(%s) -> %s", fn.__name__, ", ".join(x_args), repr(ret), stack_info=False)
        return ret

    mock_fn: T_FN = cast(T_FN, newfn)  # type: ignore
    return mock_fn


def pyqtSlot(*args) -> Callable[[T_FN], T_FN]:
    def _pyqtSlot(fn: T_FN) -> T_FN:
        return QtCore.pyqtSlot(*args)(fn)

    return _pyqtSlot
