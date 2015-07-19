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
