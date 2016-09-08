# -*- coding: utf-8 -*-

def NotImplementedWarn(fn):
    def newfn(*args,**kwargs):
        ret = fn(*args,**kwargs)
        x_args = [ repr(a) for a in args] + [ "%s=%s" % (k,repr(v)) for k,v in list(kwargs.items())]
        print("WARN: Function not yet implemented: %s(%s) -> %s" % (fn.__name__,", ".join(x_args),repr(ret)))
        return ret
    return newfn

def WorkingOnThis(fn):
    def newfn(*args,**kwargs):
        ret = fn(*args,**kwargs)
        x_args = [ repr(a) for a in args] + [ "%s=%s" % (k,repr(v)) for k,v in list(kwargs.items())]
        print("WARN: A developer is working on this function : %s(%s) -> %s" % (fn.__name__,", ".join(x_args),repr(ret)))
        return ret
    return newfn

def BetaImplementation(fn):
    def newfn(*args,**kwargs):
        ret = fn(*args,**kwargs)
        x_args = [ repr(a) for a in args] + [ "%s=%s" % (k,repr(v)) for k,v in list(kwargs.items())]
        print("WARN: This implementation is a beta : %s(%s) -> %s" % (fn.__name__,", ".join(x_args),repr(ret)))
        return ret
    return newfn

def Incomplete(fn):
    def newfn(*args,**kwargs):
        ret = fn(*args,**kwargs)
        x_args = [ repr(a) for a in args] + [ "%s=%s" % (k,repr(v)) for k,v in list(kwargs.items())]
        print("WARN: This implementation is incomplete : %s(%s) -> %s" % (fn.__name__,", ".join(x_args),repr(ret)))
        return ret
    return newfn
    
