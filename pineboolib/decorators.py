# -*- coding: utf-8 -*-
import time
import re

MSG_EMITTED = {}
CLEAN_REGEX = re.compile(r'\s*object\s+at\s+0x[0-9a-zA-Z]{6,38}', re.VERBOSE)
MINIMUM_TIME_FOR_REPRINT = 300

def clean_repr(x):
    x = repr(x)
    return CLEAN_REGEX.sub('', x)

def NotImplementedWarn(fn):
    def newfn(*args,**kwargs):
        global MSG_EMITTED
        ret = fn(*args,**kwargs)
        x_args = [ clean_repr(a) for a in args] + [ "%s=%s" % (k,clean_repr(v)) for k,v in list(kwargs.items())]
        keyname = fn.__name__+repr(x_args)
        now = time.time()
        if keyname not in MSG_EMITTED or now - MSG_EMITTED[keyname] > MINIMUM_TIME_FOR_REPRINT:
            MSG_EMITTED[keyname] = now
            print("WARN: Not yet impl.: %s(%s) -> %s" % (fn.__name__,", ".join(x_args),repr(ret)))
        return ret
    return newfn

def WorkingOnThis(fn):
    def newfn(*args,**kwargs):
        global MSG_EMITTED
        ret = fn(*args,**kwargs)
        x_args = [ clean_repr(a) for a in args] + [ "%s=%s" % (k,clean_repr(v)) for k,v in list(kwargs.items())]
        keyname = fn.__name__+repr(x_args)
        now = time.time()
        if keyname not in MSG_EMITTED or now - MSG_EMITTED[keyname] > MINIMUM_TIME_FOR_REPRINT:
            MSG_EMITTED[keyname] = now
            print("WARN: In Progress: %s(%s) -> %s" % (fn.__name__,", ".join(x_args),repr(ret)))
        return ret
    return newfn

def BetaImplementation(fn):
    def newfn(*args,**kwargs):
        global MSG_EMITTED
        ret = fn(*args,**kwargs)
        x_args = [ clean_repr(a) for a in args] + [ "%s=%s" % (k,clean_repr(v)) for k,v in list(kwargs.items())]
        keyname = fn.__name__+repr(x_args)
        now = time.time()
        if keyname not in MSG_EMITTED or now - MSG_EMITTED[keyname] > MINIMUM_TIME_FOR_REPRINT:
            MSG_EMITTED[keyname] = now
            print("WARN: Beta impl.: %s(%s) -> %s" % (fn.__name__,", ".join(x_args),repr(ret)))
        return ret
    return newfn

def Incomplete(fn):
    def newfn(*args,**kwargs):
        global MSG_EMITTED
        ret = fn(*args,**kwargs)
        x_args = [ clean_repr(a) for a in args] + [ "%s=%s" % (k,clean_repr(v)) for k,v in list(kwargs.items())]
        keyname = fn.__name__+repr(x_args)
        now = time.time()
        if keyname not in MSG_EMITTED or now - MSG_EMITTED[keyname] > MINIMUM_TIME_FOR_REPRINT:
            MSG_EMITTED[keyname] = now
            print("WARN: Incomplete: %s(%s) -> %s" % (fn.__name__,", ".join(x_args),repr(ret)))
        return ret
    return newfn


def needRevision(fn):
    def newfn(*args,**kwargs):
        global MSG_EMITTED
        ret = fn(*args,**kwargs)
        x_args = [ clean_repr(a) for a in args] + [ "%s=%s" % (k,clean_repr(v)) for k,v in list(kwargs.items())]
        keyname = fn.__name__+repr(x_args)
        now = time.time()
        if keyname not in MSG_EMITTED or now - MSG_EMITTED[keyname] > MINIMUM_TIME_FOR_REPRINT:
            MSG_EMITTED[keyname] = now
            print("WARN: Needs help: %s(%s) -> %s" % (fn.__name__,", ".join(x_args),repr(ret)))
        return ret
    return newfn
