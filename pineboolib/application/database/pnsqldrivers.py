# -*- coding: utf-8 -*-
"""
Module for PNSqlDrivers class.
"""

import importlib
import sys

from pineboolib.core.utils import logging
from pineboolib.core.utils.singleton import Singleton

from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class PNSqlDrivers(object, metaclass=Singleton):
    """
    PNSqlDrivers class.

    Manage the different available sql drivers.
    """

    _driver: Any
    _default_driver_name: str
    _drivers_dict: Dict[str, str]
    _driver_defaultr_port: Dict[str, int]
    _desktop_file: Dict[str, bool]
    # _only_pure_python = None

    def __init__(self, _DGI: Any = None) -> None:
        """Collect the information of the available cursors."""

        from pineboolib.core.utils.utils_base import filedir  # , is_deployed
        import os

        # self._only_pure_python = is_deployed()

        self._drivers_dict = {}
        self._driver_defaultr_port = {}
        self._desktop_file = {}

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
            _driver = getattr(mod_, file_name.upper())()
            if _driver.pure_python() or _driver.safe_load():
                self._drivers_dict[file_name] = _driver.alias_
                self._driver_defaultr_port[_driver.alias_] = _driver.defaultPort_
                self._desktop_file[_driver.alias_] = _driver.desktopFile()

        self._defautl_driver_name = "FLsqlite"

    def loadDriver(self, driver_name: str) -> bool:
        """
        Load an sql driver specified by name.

        This driver is stored in the internal variable _driver.
        @param driver_name =  Sql driver name.
        @return True or False.
        """

        module_path = "pineboolib.plugins.sql.%s" % driver_name.lower()
        if module_path in sys.modules:
            module_obj = importlib.reload(sys.modules[module_path])
        else:
            module_obj = importlib.import_module(module_path)
        self._driver = getattr(module_obj, driver_name.upper())()

        if self.driver():
            # self.driverName = driverName
            logger.info("Driver %s v%s", self.driver().driverName(), self.driver().version())
            return True
        else:
            return False

    def nameToAlias(self, name: str) -> str:
        """
        Return the alias of a driver from the name.

        @param name =  Driver name.
        @return Alias or None.
        """

        name = name.lower()
        if name in self._drivers_dict.keys():
            return self._drivers_dict[name]

        raise Exception("No driver found matching name!")

    def aliasToName(self, alias: str) -> str:
        """
        Return the alias of a controller from its name.

        @param alias =  Alias ​​with which the controller is known.
        @return Driver name or None.
        """
        if not alias:
            return self._defautl_driver_name

        for key, value in self._drivers_dict.items():
            if value == alias:
                return key

        raise Exception("No driver found matching alias!")

    def port(self, alias: str) -> str:
        """
        Return the default port of an sql driver.

        @param alias. Driver Alias.
        @return Default port or '0'.
        """
        for k, value in self._driver_defaultr_port.items():
            if k == alias:
                return "%s" % value

        return "0"

    def isDesktopFile(self, alias: str) -> bool:
        """
        Indicate if the BD to which the controller is connected is desktop.

        @param alias. Driver Alias.
        @return True or False.
        """
        for k, value in self._desktop_file.items():
            if k == alias:
                return value

        raise Exception("Alias not found in list!")

    def aliasList(self) -> List[str]:
        """
        List the aliases of the available drivers.

        @return List of available aliases.
        """

        list = []
        for key, value in self._drivers_dict.items():
            list.append(value)

        return list

    def driver(self) -> Any:
        """
        Link to the used controller.

        @return Driver instance.
        """

        return self._driver

    """
    Informa del nombre del controlador
    @return Nombre del controlador
    """

    def driverName(self) -> None:
        """
        Indicate the name of the activated driver.
        """

        if self._driver is None:
            raise Exception("No sql driver selected!")

        return self._driver.name()

    def __getattr__(self, attr_name):
        """
        Return an attribute of the sql driver, if it is not found.

        @param attr_name: Attribute name.
        """
        return getattr(self._driver, attr_name)

    def defaultDriverName(self) -> str:
        """
        Return the name of the default sql driver.

        @return Default driver name.
        """
        return self._defautl_driver_name
