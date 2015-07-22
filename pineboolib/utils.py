import os, os.path

# Convertir una ruta relativa, a una ruta relativa a este fichero.
def filedir(*path): return os.path.realpath(os.path.join(os.path.dirname(__file__), *path))


def one(x, default = None):
    try:
        return x[0]
    except IndexError:
        return default

class Struct(object):
    "Dummy"
    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)


class DefFun:
    def __init__(self, parent, funname, realfun = None):
        self.parent = parent
        self.funname = funname
        self.realfun = None
    def __str__(self):
        if self.realfun:
            print("%r: Redirigiendo Propiedad a función %r" % (self.parent.__class__, self.funname))
            return self.realfun()
        print("WARN: %r: Propiedad no implementada %r" % (self.parent.__class__, self.funname))
        return 0

    def __call__(self, *args):

        if self.realfun:
            print("%r: Redirigiendo Llamada a función %r %r" % (self.parent.__class__, self.funname, args))
            return self.realfun(*args)

        print("WARN: %r: Método no implementado %r %r" % (self.parent.__class__, self.funname, args))
        return None


def bind(objectName, propertyName, type):

    def getter(self):
        return type(self.findChild(QObject, objectName).property(propertyName).toPyObject())

    def setter(self, value):
        self.findChild(QObject, objectName).setProperty(propertyName, QVariant(value))

    return property(getter, setter)
