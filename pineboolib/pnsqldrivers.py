# -*- coding: utf-8 -*-
import importlib
from pineboolib.flcontrols import ProjectClass
from pineboolib.utils import filedir
import os
import logging
logger = logging.getLogger(__name__)


class PNSqlDrivers(ProjectClass):
    driverName = None
    driver_ = None
    _mobile = None

    def __init__(self, _DGI=None):
        self._mobile = False
        if _DGI:
            self._mobile = _DGI.mobilePlatform()

        self.driversdict = {}
        self.driversDefaultPort = {}
        # if not os.path.exists("pineboolib/plugins"):
        #    os.makedirs("pineboolib/plugins")
        if not os.path.exists("pineboolib/plugins/sql"):
            os.makedirs("pineboolib/plugins/sql")

        dirlist = os.listdir(filedir("plugins/sql"))
        for f in dirlist:
            if not f[0:2] == "__":
                f = f[:f.find(".py")]
                mod_ = importlib.import_module("pineboolib.plugins.sql.%s" % f)
                driver_ = getattr(mod_, f.upper())()
                if driver_.mobile_ or not self._mobile:
                    self.driversdict[f] = driver_.alias_
                    self.driversDefaultPort[driver_.alias_] = driver_.defaultPort_

        self.defaultDriverName = "FLsqlite"

    def loadDriver(self, driverName):
        if driverName is None:
            logger.info("Seleccionado driver por defecto %s", self.defaultDriverName)
            driverName = self.defaultDriverName

        module_ = importlib.import_module(
            "pineboolib.plugins.sql.%s" % driverName.lower())
        self.driver_ = getattr(module_, driverName.upper())()

        if self.driver_:
            # self.driverName = driverName
            logger.info("Driver %s v%s", self.driver().driverName(), self.driver().version())
            return True
        else:
            return False

    def nameToAlias(self, name):
        name = name.lower()
        if name in self.driversdict.keys():
            return self.driversdict[name]
        else:
            return None

    def aliasToName(self, alias):
        if not alias:
            return self.defaultDriverName

        for key, value in self.driversdict.items():
            if value == alias:
                return key

        return None

    def port(self, alias):
        for k, value in self.driversDefaultPort.items():
            if k == alias:
                return "%s" % value

    def aliasList(self):

        list = []
        for key, value in self.driversdict.items():
            list.append(value)

        return list

    def driver(self):
        return self.driver_

    def driverName(self):
        return self.driver().name()

    def __getattr__(self, k):
        return getattr(self.driver_, k)
