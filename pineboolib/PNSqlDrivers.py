# -*- coding: utf-8 -*-
import importlib
from pineboolib.flcontrols import ProjectClass

class PNSqlDrivers(ProjectClass):

    driverName = None
    driver_ = None
    
    def __init__(self, driverName = "PGSql"):
        
        module_ = importlib.import_module("pineboolib.plugins.sql.%s" % driverName)
        self.driver_ = getattr(module_, driverName)()
        
        if self.driver_:
            self.driverName = driverName
            print("Driver cargado",self.driver_.name(), self.driver_.version())
        else:
            print("PNSqlDrivers :: No se ha podidio inicializar el driver")
    
    
    def driver(self):
        return self.driver_
    
    def driverName(self):
        return self.driverName()
    
    def __getattr__(self, k):
        return getattr(self.driver_,k)
            


    







