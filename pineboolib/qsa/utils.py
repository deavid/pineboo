"""
Utility functions for QS files.
"""
import traceback
import re
import math

from PyQt5 import QtCore

from pineboolib.core.utils.utils_base import ustr
from pineboolib.core.utils import logging

from typing import Any, Optional, Union, Match, List, Pattern, Generator

logger = logging.getLogger("qsa.utils")


class switch(object):
    """
    Switch emulation class.

    from: http://code.activestate.com/recipes/410692/
    This class provides the functionality we want. You only need to look at
    this if you want to know how this works. It only needs to be defined
    once, no need to muck around with its internals.
    """

    def __init__(self, value: Any):
        """Construct new witch from initial value."""
        self.value = value
        self.fall = False

    def __iter__(self) -> Generator:
        """Return the match method once, then stop."""
        yield self.match

    def match(self, *args: List[Any]) -> bool:
        """Indicate whether or not to enter a case suite."""
        if self.fall or not args:
            return True
        elif self.value in args:
            self.fall = True
            return True
        else:
            return False


class qsaRegExp(object):
    logger = logging.getLogger("qsaRegExp")
    result_: Optional[Match[str]]

    def __init__(self, strRE: str, is_global: bool = False):
        self.strRE_ = strRE
        self.pattern = re.compile(self.strRE_)
        self.is_global = is_global
        self.result_ = None

    def search(self, text: str) -> Optional[Match[str]]:
        self.result_ = None
        if self.pattern is not None:
            self.result_ = self.pattern.search(text)
        return self.result_

    def replace(self, target: str, new_value: str) -> str:
        count = 1 if not self.is_global else 0
        return self.pattern.sub(new_value, target, count)

    def cap(self, i: int) -> Optional[str]:
        if self.result_ is None:
            return None

        try:
            return self.result_.group(i)
        except Exception:
            self.logger.exception("Error calling cap(%s)" % i)
            return None

    def get_global(self) -> bool:
        return self.is_global

    def set_global(self, b: bool) -> None:
        self.is_global = b

    global_ = property(get_global, set_global)


def RegExp(strRE: str) -> qsaRegExp:
    """
    Regexp
    @param strRE. Cadena de texto
    @return valor procesado
    """
    is_global = False
    if strRE[-2:] == "/g":
        strRE = strRE[:-2]
        is_global = True
    elif strRE[-1:] == "/":
        strRE = strRE[:-1]

    if strRE[:1] == "/":
        strRE = strRE[1:]

    return qsaRegExp(strRE, is_global)


class Math(object):
    @staticmethod
    def abs(x: Union[int, float]) -> Union[int, float]:
        return math.fabs(x)

    @staticmethod
    def ceil(x: float) -> int:
        return math.ceil(x)

    @staticmethod
    def floor(x: float) -> int:
        return math.floor(x)

    @staticmethod
    def pow(x: Union[int, float], y: Union[int, float]) -> Union[int, float]:
        return math.pow(x, y)

    @staticmethod
    def round(x: Union[int, float]) -> float:
        return round(float(x), 2)


class Application:
    """El modulo "Datos" usa Application.formRecorddat_procesos para leer el módulo"""

    def __getattr__(self, name: str) -> Any:
        return from_project(name)


def parseFloat(x: Any) -> Any:
    """
    Convierte a float un valor dado
    @param x. valor a convertir
    @return Valor tipo float, o parametro x , si no es convertible
    """
    orig_ = x
    ret = 0.00
    try:
        if isinstance(x, str) and x.find(":") > -1:
            # Convertimos a horas
            list_ = x.split(":")
            x = float(list_[0])  # Horas
            x += float(list_[1]) / 60  # Minutos a hora
            x += float(list_[2]) / 3600  # Segundos a hora

        if isinstance(x, str):
            try:
                ret = float(x)
            except Exception:
                x = x.replace(".", "")
                x = x.replace(",", ".")
                try:
                    ret = float(x)
                except Exception:
                    return orig_

        else:
            ret = 0 if x in (None, "") else float(x)

        if ret == int(ret):
            ret = int(ret)

        return ret
    except Exception:
        logger.exception("parseFloat: Error converting %s to float", x)
        return x


def parseString(obj: Any) -> str:
    """
    Convierte a str un objeto dado
    @param obj. valor a convertir
    @return str del objeto dado
    """
    return obj.toString() if hasattr(obj, "toString") else str(obj)


def parseInt(x: Union[float, int, str]) -> int:
    """
    Convierte en int un valor dado
    @param x. Valor a convertir
    @return Valor convertido
    """
    ret_ = 0
    if isinstance(x, str) and x.find(",") > -1:
        x = x.replace(",", ".")

    if x is not None:
        x = float(x)
        ret_ = int(x)

    return ret_


def isNaN(x: Any) -> bool:
    """
    Comprueba si un valor dado en numerico
    @param x. Valor numérico
    @return True o False
    """

    if x is None:
        return True

    if isinstance(x, str) and x.find(":"):
        x = x.replace(":", "")
    try:
        float(x)
        return False
    except ValueError:
        return True


def length(obj: Any) -> int:
    """
    Parser para recoger el length de un campo
    @param obj, objeto a obtener longitud
    @return longitud del objeto
    """
    if hasattr(obj, "length"):
        if isinstance(obj.length, int):
            return obj.length
        else:
            return obj.length()

    else:
        if isinstance(obj, dict) and "result" in obj.keys():
            return len(obj) - 1
        else:
            return len(obj)


def text(obj: Any) -> str:
    """
    Parser para recoger valor text de un objeto dado
    @param obj. Objeto a procesar
    @return Valor de text o text()
    """
    try:
        return obj.text()
    except Exception:
        return obj.text


def startTimer(time: int, fun: Any) -> "QtCore.QTimer":
    timer = QtCore.QTimer()
    timer.timeout.connect(fun)
    timer.start(time)
    return timer


def killTimer(t: Optional["QtCore.QTimer"] = None) -> None:
    if t is not None:
        t.stop()
        t = None


def debug(txt: str) -> None:
    """
    Mensajes debug en qsa
    @param txt. Mensaje.
    """
    from pineboolib.application import project

    project.message_manager().send("debug", None, [ustr(txt)])


def from_project(scriptname: str) -> Any:
    """
    Devuelve el objeto de proyecto que coincide con el nombre dado
    """
    from pineboolib import qsa as qsa_dict_modules

    # FIXME: Esto debería estar guardado en Project.
    return getattr(qsa_dict_modules, scriptname, None)


def format_exc(exc: Optional[int] = None) -> str:
    return traceback.format_exc(exc)


def isnan(n: Any) -> bool:
    return math.isnan(n)


def replace(source: str, search: Any, replace: str) -> Union[str, Pattern]:
    """Replace for QSA where detects if "search" is a Regexp"""
    if hasattr(search, "match"):
        return search.replace(source, replace)
    else:
        return source.replace(search, str(replace))
