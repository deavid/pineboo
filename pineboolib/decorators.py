# -*- coding: utf-8 -*-
import time
import re
import traceback

class Options:
    DEBUG_LEVEL = 100


MSG_EMITTED = {}
CLEAN_REGEX = re.compile(r'\s*object\s+at\s+0x[0-9a-zA-Z]{6,38}', re.VERBOSE)
MINIMUM_TIME_FOR_REPRINT = 300
def print_stack(maxsize=1):
    for tb in traceback.format_list(traceback.extract_stack())[1:-2][-maxsize:]:
        print(tb.rstrip())

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
            if Options.DEBUG_LEVEL > 50: print("WARN: Not yet impl.: %s(%s) -> %s" % (fn.__name__,", ".join(x_args),repr(ret)))
            if Options.DEBUG_LEVEL > 90: print_stack()
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
            if Options.DEBUG_LEVEL > 10: print("WARN: In Progress: %s(%s) -> %s" % (fn.__name__,", ".join(x_args),repr(ret)))
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
            if Options.DEBUG_LEVEL > 5: print("WARN: Beta impl.: %s(%s) -> %s" % (fn.__name__,", ".join(x_args),repr(ret)))
        return ret
    return newfn

def Empty(fn): # Similar a NotImplemented, pero sin traceback. Para funciones que de momento no necesitamos (clonadas del motor C++ por ejemplo)
    def newfn(*args,**kwargs):
        global MSG_EMITTED
        ret = fn(*args,**kwargs)
        x_args = [ clean_repr(a) for a in args] + [ "%s=%s" % (k,clean_repr(v)) for k,v in list(kwargs.items())]
        keyname = fn.__name__
        now = time.time()
        if keyname not in MSG_EMITTED or now - MSG_EMITTED[keyname] > MINIMUM_TIME_FOR_REPRINT:
            MSG_EMITTED[keyname] = now
            if Options.DEBUG_LEVEL > 50: print("WARN: Empty: %s(%s) -> %s" % (fn.__name__,", ".join(x_args),repr(ret)))
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
            if Options.DEBUG_LEVEL > 5: print("WARN: Incomplete: %s(%s) -> %s" % (fn.__name__,", ".join(x_args),repr(ret)))
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
            if Options.DEBUG_LEVEL > 10: print("WARN: Needs help: %s(%s) -> %s" % (fn.__name__,", ".join(x_args),repr(ret)))
        return ret
    return newfn
