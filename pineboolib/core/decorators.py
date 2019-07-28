# -*- coding: utf-8 -*-
"""
Collection of useful decorators.

These are mainly intended to tell other devs whether a funcitionality is considered unstable or beta
"""
import time
import re
import functools
from .utils import logging
from PyQt5 import QtCore  # type: ignore
from typing import Callable, Any, Dict, TypeVar, cast

T_FN = TypeVar("T_FN", bound=Callable[..., Any])

logger = logging.getLogger(__name__)
MSG_EMITTED: Dict[str, float] = {}
CLEAN_REGEX = re.compile(r"\s*object\s+at\s+0x[0-9a-zA-Z]{6,38}", re.VERBOSE)
MINIMUM_TIME_FOR_REPRINT = 300


def clean_repr(x: Any) -> str:
    """Clean up error texts to make them easier to read on GUI (Internal use only)."""
    return CLEAN_REGEX.sub("", repr(x))


def NotImplementedWarn(fn: T_FN) -> T_FN:
    """
    Mark function as not implemented. Its contents do almost nothing at all. Emits a Warning.

    This one is specific to warn users that when QSA runs the code, it's going to be wrong.
    Adds a Stack/traceback to aid devs locating from where the code was called from.
    """

    @functools.wraps(fn)
    def newfn(*args: Any, **kwargs: Any) -> Any:
        global MSG_EMITTED
        ret = fn(*args, **kwargs)
        x_args = [clean_repr(a) for a in args] + [
            "%s=%s" % (k, clean_repr(v)) for k, v in list(kwargs.items())
        ]
        keyname = fn.__name__ + repr(x_args)
        now = time.time()
        if (
            keyname not in MSG_EMITTED
            or now - MSG_EMITTED[keyname] > MINIMUM_TIME_FOR_REPRINT
        ):
            MSG_EMITTED[keyname] = now
            logger.warning(
                "Not yet impl.: %s(%s) -> %s", fn.__name__, ", ".join(x_args), repr(ret)
            )
            logger.trace(
                "Not yet impl.: %s(%s) -> %s",
                fn.__name__,
                ", ".join(x_args),
                repr(ret),
                stack_info=True,
            )
        return ret

    mock_fn: T_FN = cast(T_FN, newfn)  # type: ignore
    return mock_fn


def NotImplementedDebug(fn: T_FN) -> T_FN:
    """
    Mark function as not implemented. Its contents do almost nothing at all. Emits a Debug.

    In this case, just a Debug, so mainly intended for devs.
    This means the function not doing anything is usually harmless.
    """

    @functools.wraps(fn)
    def newfn(*args: Any, **kwargs: Any) -> Any:
        global MSG_EMITTED
        ret = fn(*args, **kwargs)
        x_args = [clean_repr(a) for a in args] + [
            "%s=%s" % (k, clean_repr(v)) for k, v in list(kwargs.items())
        ]
        keyname = fn.__name__ + repr(x_args)
        now = time.time()
        if (
            keyname not in MSG_EMITTED
            or now - MSG_EMITTED[keyname] > MINIMUM_TIME_FOR_REPRINT
        ):
            MSG_EMITTED[keyname] = now
            logger.debug(
                "Not yet impl.: %s(%s) -> %s", fn.__name__, ", ".join(x_args), repr(ret)
            )
        return ret

    mock_fn: T_FN = cast(T_FN, newfn)  # type: ignore
    return mock_fn


def WorkingOnThis(fn: T_FN) -> T_FN:
    """Emit a message to tell other devs that someone is already working on this function."""

    @functools.wraps(fn)
    def newfn(*args: Any, **kwargs: Any) -> Any:
        global MSG_EMITTED
        ret = fn(*args, **kwargs)
        x_args = [clean_repr(a) for a in args] + [
            "%s=%s" % (k, clean_repr(v)) for k, v in list(kwargs.items())
        ]
        keyname = fn.__name__ + repr(x_args)
        now = time.time()
        if (
            keyname not in MSG_EMITTED
            or now - MSG_EMITTED[keyname] > MINIMUM_TIME_FOR_REPRINT
        ):
            MSG_EMITTED[keyname] = now
            logger.info(
                "WARN: In Progress: %s(%s) -> %s",
                fn.__name__,
                ", ".join(x_args),
                repr(ret),
            )
        return ret

    mock_fn: T_FN = cast(T_FN, newfn)  # type: ignore
    return mock_fn


def BetaImplementation(fn: T_FN) -> T_FN:
    """Mark function as beta. This means that more or less works but it might need more tweaking or errors may arise."""

    @functools.wraps(fn)
    def newfn(*args: Any, **kwargs: Any) -> Any:
        global MSG_EMITTED
        ret = fn(*args, **kwargs)
        x_args = [clean_repr(a) for a in args] + [
            "%s=%s" % (k, clean_repr(v)) for k, v in list(kwargs.items())
        ]
        keyname = fn.__name__ + repr(x_args)
        now = time.time()
        if (
            keyname not in MSG_EMITTED
            or now - MSG_EMITTED[keyname] > MINIMUM_TIME_FOR_REPRINT
        ):
            MSG_EMITTED[keyname] = now
            logger.info(
                "WARN: Beta impl.: %s(%s) -> %s",
                fn.__name__,
                ", ".join(x_args),
                repr(ret),
            )
        return ret

    mock_fn: T_FN = cast(T_FN, newfn)  # type: ignore
    return mock_fn


def Empty(fn: T_FN) -> T_FN:
    """
    Mark function as Empty, not doing anything. Similar to NotImplemented* but does no add traceback.

    This functions are those that we don't think we will need
    """

    @functools.wraps(fn)
    def newfn(*args: Any, **kwargs: Any) -> Any:
        global MSG_EMITTED
        ret = fn(*args, **kwargs)
        x_args = [clean_repr(a) for a in args] + [
            "%s=%s" % (k, clean_repr(v)) for k, v in list(kwargs.items())
        ]
        keyname = fn.__name__
        now = time.time()
        if (
            keyname not in MSG_EMITTED
            or now - MSG_EMITTED[keyname] > MINIMUM_TIME_FOR_REPRINT
        ):
            MSG_EMITTED[keyname] = now
            logger.info(
                "WARN: Empty: %s(%s) -> %s", fn.__name__, ", ".join(x_args), repr(ret)
            )
        return ret

    mock_fn: T_FN = cast(T_FN, newfn)  # type: ignore
    return mock_fn


def Incomplete(fn: T_FN) -> T_FN:
    """Mark the function as Incomplete, meaning that functionaility is still missing."""

    @functools.wraps(fn)
    def newfn(*args: Any, **kwargs: Any) -> Any:
        global MSG_EMITTED
        ret = fn(*args, **kwargs)
        x_args = [clean_repr(a) for a in args] + [
            "%s=%s" % (k, clean_repr(v)) for k, v in list(kwargs.items())
        ]
        keyname = fn.__name__ + repr(x_args)
        now = time.time()
        if (
            keyname not in MSG_EMITTED
            or now - MSG_EMITTED[keyname] > MINIMUM_TIME_FOR_REPRINT
        ):
            MSG_EMITTED[keyname] = now
            logger.info(
                "WARN: Incomplete: %s(%s) -> %s",
                fn.__name__,
                ", ".join(x_args),
                repr(ret),
            )
        return ret

    mock_fn: T_FN = cast(T_FN, newfn)  # type: ignore
    return mock_fn


def needRevision(fn: T_FN) -> T_FN:
    """Mark the function as needs to be revised. Some bug might have been found and needs help from other devs."""

    def newfn(*args: Any, **kwargs: Any) -> Any:
        global MSG_EMITTED
        ret = fn(*args, **kwargs)
        x_args = [clean_repr(a) for a in args] + [
            "%s=%s" % (k, clean_repr(v)) for k, v in list(kwargs.items())
        ]
        keyname = fn.__name__ + repr(x_args)
        now = time.time()
        if (
            keyname not in MSG_EMITTED
            or now - MSG_EMITTED[keyname] > MINIMUM_TIME_FOR_REPRINT
        ):
            MSG_EMITTED[keyname] = now
            logger.info(
                "WARN: Needs help: %s(%s) -> %s",
                fn.__name__,
                ", ".join(x_args),
                repr(ret),
            )
        return ret

    mock_fn: T_FN = cast(T_FN, newfn)  # type: ignore
    return mock_fn


def Deprecated(fn: T_FN) -> T_FN:
    """Mark functionality as deprecated in favor of other one."""

    @functools.wraps(fn)
    def newfn(*args: Any, **kwargs: Any) -> Any:
        global MSG_EMITTED
        ret = fn(*args, **kwargs)
        x_args = [clean_repr(a) for a in args] + [
            "%s=%s" % (k, clean_repr(v)) for k, v in list(kwargs.items())
        ]
        keyname = fn.__name__ + repr(x_args)
        now = time.time()
        if (
            keyname not in MSG_EMITTED
            or now - MSG_EMITTED[keyname] > MINIMUM_TIME_FOR_REPRINT
        ):
            MSG_EMITTED[keyname] = now
            logger.info(
                "WARN: Deprecated: %s(%s) -> %s",
                fn.__name__,
                ", ".join(x_args),
                repr(ret),
                stack_info=False,
            )
        return ret

    mock_fn: T_FN = cast(T_FN, newfn)  # type: ignore
    return mock_fn


def pyqtSlot(*args: Any) -> Callable[[T_FN], T_FN]:
    """
    Create Qt Slot from classm method.

    Same as QtCore.pyQtSlot but with Typing information for mypy.
    Please use this one instead of QtCore.pyQtSlot().
    """

    def _pyqtSlot(fn: T_FN) -> T_FN:
        return cast(T_FN, QtCore.pyqtSlot(*args)(fn))

    return _pyqtSlot
