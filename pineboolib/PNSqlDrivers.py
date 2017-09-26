# -*- coding: utf-8 -*-
import importlib
from pineboolib.flcontrols import ProjectClass

class PNSqlDrivers(ProjectClass):

    driverName = None
    driver_ = None
    
    def __init__(self, driverName = "FLQPSQL"):
        
        module_ = importlib.import_module("pineboolib.plugins.sql.%s" % driverName)
        self.driver_ = getattr(module_, driverName)()
        
        if self.driver_:
            #self.driverName = driverName
            print("Driver cargado",self.driver().driverName(), self.driver().version())
        else:
            print("PNSqlDrivers :: No se ha podidio inicializar el driver")
    
    
    def driver(self):
        return self.driver_
    
    def driverName(self):
        return self.driver().name()
    
    def __getattr__(self, k):
        return getattr(self.driver_,k)
            


    







