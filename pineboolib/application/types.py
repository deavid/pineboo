import os
import os.path
from typing import Any, Optional, Dict
from pineboolib.core.utils.utils_base import StructMyDict
from pineboolib.core.utils.logging import logging
from .utils import date_conversion

logger = logging.getLogger(__name__)

Date = date_conversion.Date


def Boolean(x=False):
    """
    Retorna Booelan de una cadena de texto
    """
    ret = False
    if x in ["true", "True", True, 1] or isinstance(x, int) > 0 or isinstance(x, float) > 0:
        ret = True

    return ret


class QString(str):
    """
    Clase QString para simular la original que no existe en PyQt5
    """

    def mid(self, start, length=None):
        """
        Recoje una sub cadena a partir de una cadena
        @param start. Posición inicial
        @param length. Longitud de la cadena. Si no se especifica , es hasta el final
        @return sub cadena de texto.
        """
        if length is None:
            return self[start:]
        else:
            return self[start : start + length]


def Function(*args):

    import importlib
    import sys as python_sys

    # Leer código QS embebido en Source
    # asumir que es una funcion anónima, tal que:
    #  -> function($args) { source }
    # compilar la funcion y devolver el puntero
    arguments = args[: len(args) - 1]
    source = args[len(args) - 1]
    qs_source = """

function anon(%s) {
    %s
} """ % (
        ", ".join(arguments),
        source,
    )

    # print("Compilando QS en línea: ", qs_source)
    from pineboolib.flparser import flscriptparse
    from pineboolib.flparser import postparse
    from pineboolib.flparser.pytnyzer import write_python_file

    from . import project

    prog = flscriptparse.parse(qs_source)
    tree_data = flscriptparse.calctree(prog, alias_mode=0)
    ast = postparse.post_parse(tree_data)

    dest_filename = "%s/anon.py" % project.tmpdir
    # f1 = io.StringIO()
    if os.path.exists(dest_filename):
        os.remove(dest_filename)

    f1 = open(dest_filename, "w", encoding="UTF-8")

    write_python_file(f1, ast)
    f1.close()
    mod = None
    module_path = "tempdata.anon"

    if module_path in python_sys.modules:
        mod = importlib.reload(python_sys.modules[module_path])
    else:
        mod = importlib.import_module(module_path)
    forminternalobj = getattr(mod, "FormInternalObj", None)

    return getattr(forminternalobj(), "anon", None)


def Object(x: Optional[Dict[str, Any]] = None) -> StructMyDict:
    """
    Objeto tipo object
    """
    if x is None:
        x = {}

    return StructMyDict(x)


def String(value):
    """
    Devuelve una cadena de texto
    @param value. Valor a convertir
    @return cadena de texto.
    """
    return str(value)


class Array(object):
    """
    Objeto tipo Array
    """

    dict_: Dict[Any, Any] = None
    key_ = None
    names_ = None
    pos_iter = None

    def __init__(self, *args) -> None:
        import collections

        self.dict_ = collections.OrderedDict()

        if not len(args):
            return
        elif isinstance(args[0], int) and len(args) == 1:
            return
        elif isinstance(args[0], list):
            for field in args[0]:

                field_key = field
                while field_key in self.dict_.keys():
                    field_key = "%s_bis" % field_key

                self.dict_[field_key] = field

        elif isinstance(args[0], str):
            for f in args:
                self.__setitem__(f, f)
        else:
            self.dict_ = collections.OrderedDict(enumerate(args))

    def __iter__(self):
        """
        iterable
        """
        self.pos_iter = 0
        return self

    def __next__(self):
        """
        iterable
        """
        ret_ = None
        i = 0
        if self.dict_:
            for k in self.dict_.keys():
                if i == self.pos_iter:
                    ret_ = self.dict_[k]
                    break

                i += 1

        if ret_ is None:
            raise StopIteration
        else:
            self.pos_iter += 1

        return ret_

    def __setitem__(self, key, value):
        """
        Especificamos una nueva entrada
        @param key. Nombre del registro
        @param value. Valor del registro
        """

        self.dict_[key] = value

    def __getitem__(self, key):
        """
        Recogemos el valor de un registro
        @param key. Valor que idenfica el registro a recoger
        @return Valor del registro especificado
        """
        if isinstance(key, int):
            i = 0
            for k in self.dict_.keys():
                if key == i:
                    return self.dict_[k]
                i += 1

        elif isinstance(key, slice):
            logger.warning("FIXME: Array __getitem__%s con slice" % key)
        else:
            return self.dict_[key] if key in self.dict_.keys() else None

        return None

    def __getattr__(self, k):
        if k == "length":
            return len(self.dict_)
        else:
            return self.dict_[k]

    def splice(self, *args):
        if len(args) == 2:  # Delete
            pos_ini = args[0]
            length_ = args[1]
            i = 0
            x = 0
            new = {}
            for m in self.dict_.keys():
                if i >= pos_ini and x <= length_:
                    new[m] = self.dict_[m]
                    x += 1

                i += 1

            self.dict_ = new

        elif len(args) > 2 and args[1] == 0:  # Insertion
            for i in range(2, len(args)):
                self.append(args[i])
        elif len(args) > 2 and args[1] > 0:  # Replacement
            pos_ini = args[0]
            replacement_size = args[1]
            new_values = args[2:]

            i = 0
            x = 0
            new = {}
            for m in self.dict_.keys():
                if i < pos_ini:
                    new[m] = self.dict_[m]
                else:
                    if x < replacement_size:
                        if x == 0:
                            for n in new_values:
                                new[n] = n

                        x += 1
                    else:
                        new[m] = self.dict_[m]

                i += 1

            self.dict_ = new

    def __len__(self):
        return len(self.dict_)

    def __str__(self):
        return " ".join(self.dict_.keys())

    def append(self, val):
        k = repr(val)
        while True:
            if hasattr(self.dict_, k):
                k = "%s_" % k
            else:
                break

        self.dict_[k] = val
