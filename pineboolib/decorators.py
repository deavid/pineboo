# -*- coding: utf-8 -*-
import time
import re
import logging


logger = logging.getLogger(__name__)
MSG_EMITTED = {}
CLEAN_REGEX = re.compile(r'\s*object\s+at\s+0x[0-9a-zA-Z]{6,38}', re.VERBOSE)
MINIMUM_TIME_FOR_REPRINT = 300


def clean_repr(x):
    x = repr(x)
    return CLEAN_REGEX.sub('', x)


def NotImplementedWarn(fn):
    def newfn(*args, **kwargs):
        global MSG_EMITTED
        ret = fn(*args, **kwargs)
        x_args = [clean_repr(a) for a in args] + ["%s=%s" %
                                                  (k, clean_repr(v)) for k, v in list(kwargs.items())]
        keyname = fn.__name__ + repr(x_args)
        now = time.time()
        if keyname not in MSG_EMITTED or now - MSG_EMITTED[keyname] > MINIMUM_TIME_FOR_REPRINT:
            MSG_EMITTED[keyname] = now
            logger.warn("Not yet impl.: %s(%s) -> %s", fn.__name__, ", ".join(x_args), repr(ret))
            logger.trace("Not yet impl.: %s(%s) -> %s", fn.__name__, ", ".join(x_args), repr(ret), stack_info=True)
        return ret
    return newfn


def NotImplementedDebug(fn):
    def newfn(*args, **kwargs):
        global MSG_EMITTED
        ret = fn(*args, **kwargs)
        x_args = [clean_repr(a) for a in args] + ["%s=%s" %
                                                  (k, clean_repr(v)) for k, v in list(kwargs.items())]
        keyname = fn.__name__ + repr(x_args)
        now = time.time()
        if keyname not in MSG_EMITTED or now - MSG_EMITTED[keyname] > MINIMUM_TIME_FOR_REPRINT:
            MSG_EMITTED[keyname] = now
            logger.debug("Not yet impl.: %s(%s) -> %s", fn.__name__, ", ".join(x_args), repr(ret))
        return ret
    return newfn


def WorkingOnThis(fn):
    def newfn(*args, **kwargs):
        global MSG_EMITTED
        ret = fn(*args, **kwargs)
        x_args = [clean_repr(a) for a in args] + ["%s=%s" %
                                                  (k, clean_repr(v)) for k, v in list(kwargs.items())]
        keyname = fn.__name__ + repr(x_args)
        now = time.time()
        if keyname not in MSG_EMITTED or now - MSG_EMITTED[keyname] > MINIMUM_TIME_FOR_REPRINT:
            MSG_EMITTED[keyname] = now
            logger.info("WARN: In Progress: %s(%s) -> %s", fn.__name__, ", ".join(x_args), repr(ret))
        return ret
    return newfn


def BetaImplementation(fn):
    def newfn(*args, **kwargs):
        global MSG_EMITTED
        ret = fn(*args, **kwargs)
        x_args = [clean_repr(a) for a in args] + ["%s=%s" %
                                                  (k, clean_repr(v)) for k, v in list(kwargs.items())]
        keyname = fn.__name__ + repr(x_args)
        now = time.time()
        if keyname not in MSG_EMITTED or now - MSG_EMITTED[keyname] > MINIMUM_TIME_FOR_REPRINT:
            MSG_EMITTED[keyname] = now
            logger.info("WARN: Beta impl.: %s(%s) -> %s", fn.__name__, ", ".join(x_args), repr(ret))
        return ret
    return newfn


def Empty(fn):  # Similar a NotImplemented, pero sin traceback. Para funciones que de momento no necesitamos (clonadas del motor C++ por ejemplo)
    def newfn(*args, **kwargs):
        global MSG_EMITTED
        ret = fn(*args, **kwargs)
        x_args = [clean_repr(a) for a in args] + ["%s=%s" %
                                                  (k, clean_repr(v)) for k, v in list(kwargs.items())]
        keyname = fn.__name__
        now = time.time()
        if keyname not in MSG_EMITTED or now - MSG_EMITTED[keyname] > MINIMUM_TIME_FOR_REPRINT:
            MSG_EMITTED[keyname] = now
            logger.info("WARN: Empty: %s(%s) -> %s", fn.__name__, ", ".join(x_args), repr(ret))
        return ret
    return newfn


def Incomplete(fn):
    def newfn(*args, **kwargs):
        global MSG_EMITTED
        ret = fn(*args, **kwargs)
        x_args = [clean_repr(a) for a in args] + ["%s=%s" %
                                                  (k, clean_repr(v)) for k, v in list(kwargs.items())]
        keyname = fn.__name__ + repr(x_args)
        now = time.time()
        if keyname not in MSG_EMITTED or now - MSG_EMITTED[keyname] > MINIMUM_TIME_FOR_REPRINT:
            MSG_EMITTED[keyname] = now
            logger.info("WARN: Incomplete: %s(%s) -> %s", fn.__name__, ", ".join(x_args), repr(ret))
        return ret
    return newfn


def needRevision(fn):
    def newfn(*args, **kwargs):
        global MSG_EMITTED
        ret = fn(*args, **kwargs)
        x_args = [clean_repr(a) for a in args] + ["%s=%s" %
                                                  (k, clean_repr(v)) for k, v in list(kwargs.items())]
        keyname = fn.__name__ + repr(x_args)
        now = time.time()
        if keyname not in MSG_EMITTED or now - MSG_EMITTED[keyname] > MINIMUM_TIME_FOR_REPRINT:
            MSG_EMITTED[keyname] = now
            logger.info("WARN: Needs help: %s(%s) -> %s", fn.__name__, ", ".join(x_args), repr(ret))
        return ret
    return newfn


def Deprecated(fn):
    def newfn(*args, **kwargs):
        global MSG_EMITTED
        ret = fn(*args, **kwargs)
        x_args = [clean_repr(a) for a in args] + ["%s=%s" %
                                                  (k, clean_repr(v)) for k, v in list(kwargs.items())]
        keyname = fn.__name__ + repr(x_args)
        now = time.time()
        if keyname not in MSG_EMITTED or now - MSG_EMITTED[keyname] > MINIMUM_TIME_FOR_REPRINT:
            MSG_EMITTED[keyname] = now
            logger.info("WARN: Deprecated: %s(%s) -> %s", fn.__name__, ", ".join(x_args), repr(ret), stack_info=True)
        return ret
    return newfn
