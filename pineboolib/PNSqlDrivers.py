# -*- coding: utf-8 -*-
import importlib
from pineboolib.flcontrols import ProjectClass
from pineboolib.utils import filedir
import os


class PNSqlDrivers(ProjectClass):

    driverName = None
    driver_ = None

    def __init__(self):

        self.driversdict = {}

        dirlist = os.listdir(filedir("../pineboolib/plugins/sql"))
        for f in dirlist:
            if not f[0:2] == "__":
                f = f[:f.find(".py")]
                mod_ = importlib.import_module("pineboolib.plugins.sql.%s" % f)
                driver_ = getattr(mod_, f)()
                self.driversdict[f] = driver_.alias_

        self.defaultDriverName = "FLQPSQL"

    def loadDriver(self, driverName):
        if driverName is None:
            print("Seleccionado driver por defecto", self.defaultDriverName)
            driverName = self.defaultDriverName

        module_ = importlib.import_module(
            "pineboolib.plugins.sql.%s" % driverName)
        self.driver_ = getattr(module_, driverName)()

        if self.driver_:
            # self.driverName = driverName
            print("PNSqlDrivers::Driver %s v%s" %
                  (self.driver().driverName(), self.driver().version()))
            return True
        else:
            return False

    def nameToAlias(self, name):
        return self.driversdict.get(name, None)

    def aliasToName(self, alias):
        if not alias:
            return self.defaultDriverName

        for key, value in self.driversdict.items():
            if value == alias:
                return key

        return None

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
