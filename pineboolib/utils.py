# # -*- coding: utf-8 -*-

import os, os.path, re

DEBUG = False

def auto_qt_translate_text(text):
    """ función utilizada para eliminar los QT_TRANSLATE de eneboo. Esta función ahora mismo no traduce nada."""
    if not isinstance(text,str): text=str(text)

    if isinstance(text,str):
        if text.find("QT_TRANSLATE") != -1:
            match = re.search(r"""QT_TRANSLATE\w*\(.+,["'](.+)["']\)""", text)
            if match: text = match.group(1)
    return text

aqtt = auto_qt_translate_text

# Convertir una ruta relativa, a una ruta relativa a este fichero.
def filedir(*path):
    """  filedir(path1[, path2, path3 , ...])

            Filedir devuelve la ruta absoluta resultado de concatenar los paths que se le pasen y aplicarlos desde la ruta del proyecto.
            Es útil para especificar rutas a recursos del programa.
    """
    return os.path.realpath(os.path.join(os.path.dirname(__file__), *path))


def one(x, default = None):
    """ Se le pasa una lista de elementos (normalmente de un xml) y devuelve el primero o None; sirve para ahorrar try/excepts y limpiar código"""
    try:
        return x[0]
    except IndexError:
        return default

class Struct(object):
    """
        Plantilla básica de objeto. Asigna sus propiedades en el __init__.
        Especialmente útil para bocetar clases al vuelo.
    """
    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)


class XMLStruct(Struct):
    """
        Plantilla de objeto que replica el contenido de un xml. Sirve para tener rápidamente un objeto
        que sea idéntico al xml que se pueda acceder fácilmente por propiedades.
    """
    def __init__(self, xmlobj=None):
        self._attrs = []
        if xmlobj is not None:
            self.__name__ = xmlobj.tag
            for child in xmlobj:
                if child.tag == "property":
                    # Se importa aquí para evitar error de importación cíclica.
                    from pineboolib.qt3ui import loadProperty

                    key, text = loadProperty(child)
                else:
                    text = aqtt(child.text)
                    key = child.tag
                if isinstance(text, str): text = text.strip()
                setattr(self, key, text)
                self._attrs.append(key)
                # print self.__name__, key, text
    def __str__(self):
        attrs = [ "%s=%s" % (k,repr(getattr(self,k))) for k in self._attrs ]
        txtattrs = " ".join(attrs)
        return "<%s.%s %s>" % (self.__class__.__name__, self.__name__, txtattrs)

    def _v(self, k, default=None):
        return getattr(self, k, default)



class DefFun:
    """
        Emuladores de funciones por defecto.
        Tiene una doble funcionalidad. Por un lado, permite convertir llamadas a propiedades en llamadas a la función de verdad.
        Por otro, su principal uso, es omitir las llamadas a funciones inexistentes, de forma que nos advierta en consola
        pero que el código se siga ejecutando. (ESTO ES PELIGROSO)
    """
    def __init__(self, parent, funname, realfun = None):
        self.parent = parent
        self.funname = funname
        self.realfun = None
    def __str__(self):
        if self.realfun:
            if DEBUG: print("%r: Redirigiendo Propiedad a función %r" % (self.parent.__class__, self.funname))
            return self.realfun()
        if DEBUG: print("WARN: %r: Propiedad no implementada %r" % (self.parent.__class__, self.funname))
        return 0

    def __call__(self, *args):

        if self.realfun:
            if DEBUG: print("%r: Redirigiendo Llamada a función %r %r" % (self.parent.__class__, self.funname, args))
            return self.realfun(*args)

        if DEBUG: print("WARN: %r: Método no implementado %r %r" % (self.parent.__class__, self.funname, args))
        return None


def bind(objectName, propertyName, type):
    """
        Utilidad para crear propiedades de estilo Qt fácilmente.
        Actualmente en desuso. Python tiene su propio sistema de propiedades y funciona bien.
    """
    def getter(self):
        return type(self.findChild(QObject, objectName).property(propertyName).toPyObject())

    def setter(self, value):
        self.findChild(QObject, objectName).setProperty(propertyName, QVariant(value))

    return property(getter, setter)
