# # -*- coding: utf-8 -*-

from pineboolib.plugins.dgi.dgi_schema import dgi_schema


class dgi_qt(dgi_schema):
    
    
    def __init__(self):
        super(dgi_qt, self).__init__() #desktopEnabled y mlDefault a True
        self._name = "qt"
        self._alias = "Qt5"
        