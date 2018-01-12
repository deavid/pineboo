# # -*- coding: utf-8 -*-

class dgi_schema(object):
    
    _desktopEnabled = False
    _mLDefault = False
    _name = None
    _alias = None
    
    
    def __init__(self):
        self._desktopEnabled = True #Indica si se usa en formato escritorio con interface Qt
        self._mLDefault = True
        self._name = "dgi_shema"
        self._alias = "Default Schema"
    
    
    def alternativeMain(self, main_): #Establece un lanzador alternativo al de la aplicación
        pass
    
    def useDesktop(self):
        return self._desktopEnabled
    
    def useMLDefault(self):
        return self._mLDefault
    
    def setParameter(self, param): # Se puede pasar un parametro al dgi
        pass