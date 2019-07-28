# -*- coding: utf-8 -*-
import importlib
import sys
from typing import Dict

from pineboolib.core.utils import logging
from pineboolib.core.utils.singleton import Singleton

logger = logging.getLogger(__name__)


class PNSqlDrivers(object, metaclass=Singleton):
    """
    Esta clase gestiona los diferentes controladores de BD.
    """

    driver_ = None
    only_pure_python_ = None

    def __init__(self, _DGI=None):
        """
        Constructor
        """
        from pineboolib.core.utils.utils_base import filedir
        import os

        self.only_pure_python_ = getattr(sys, "frozen", False)

        self.driversdict: Dict[str, str] = {}
        self.driversDefaultPort: Dict[str, int] = {}
        self.desktopFile: Dict[str, str] = {}

        dir_list = [
            file
            for file in os.listdir(filedir("plugins/sql"))
            if not file[0] == "_" and file.find(".py") > -1
        ]
        for item in dir_list:
            file_name = item[: item.find(".py")]
            try:
                mod_ = importlib.import_module("pineboolib.plugins.sql.%s" % file_name)
            except ModuleNotFoundError:
                logger.debug("Error trying to load driver %s", file_name, exc_info=True)
                continue
            except Exception:
                logger.exception("Unexpected error loading driver %s", file_name)
                continue
            driver_ = getattr(mod_, file_name.upper())()
            if driver_.pure_python() or driver_.safe_load():
                self.driversdict[file_name] = driver_.alias_
                self.driversDefaultPort[driver_.alias_] = driver_.defaultPort_
                self.desktopFile[driver_.alias_] = driver_.desktopFile()

        self.defaultDriverName = "FLsqlite"

    """
    Apunta hacia un controlador dado.
    @param driverName. Nombre del controlado que se desea usar.
    @return True o False.
    """

    def loadDriver(self, driver_name):

        if driver_name is None:
            logger.info("Seleccionado driver por defecto %s", self.defaultDriverName)
            driver_name = self.defaultDriverName

        module_path = "pineboolib.plugins.sql.%s" % driver_name.lower()
        if module_path in sys.modules:
            module_ = importlib.reload(sys.modules[module_path])
        else:
            module_ = importlib.import_module(module_path)
        self.driver_ = getattr(module_, driver_name.upper())()

        if self.driver():
            # self.driverName = driverName
            logger.info(
                "Driver %s v%s", self.driver().driverName(), self.driver().version()
            )
            return True
        else:
            return False

    """
    Retorna el Alias de un controlador a partir de su Nombre
    @param name. Nombre del controlador.
    @return Alias o None.
    """

    def nameToAlias(self, name):
        name = name.lower()
        if name in self.driversdict.keys():
            return self.driversdict[name]
        else:
            return None

    """
    Retorna el Nombre de un controlador a partir de su nombre
    @param alias. Alias con el que se conoce al controlador
    @return Nombre o None.
    """

    def aliasToName(self, alias):
        if not alias:
            return self.defaultDriverName

        for key, value in self.driversdict.items():
            if value == alias:
                return key

        return None

    """
    Puerto por defecto que una un controlador.
    @param alias. Alias del controlador.
    @return Puerto por defecto.
    """

    def port(self, alias):
        for k, value in self.driversDefaultPort.items():
            if k == alias:
                return "%s" % value

    """
    Indica si la BD a la que se conecta el controlador es de tipo escriotrio
    @param alias. Alias del controlador.
    @return True o False.
    """

    def isDesktopFile(self, alias):
        for k, value in self.desktopFile.items():
            if k == alias:
                return value

    """
    Lista los alias de los controladores disponibles
    @return lista.
    """

    def aliasList(self):

        list = []
        for key, value in self.driversdict.items():
            list.append(value)

        return list

    """
    Enlace con el controlador usado
    @return Objecto controlador
    """

    def driver(self):
        return self.driver_

    """
    Informa del nombre del controlador
    @return Nombre del controlador
    """

    def driverName(self):
        return self.driver().name()

    def __getattr__(self, k):
        return getattr(self.driver_, k)
