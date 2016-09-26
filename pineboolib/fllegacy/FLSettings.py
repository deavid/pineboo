# -*- coding: utf-8 -*-

from PyQt4 import QtCore

from pineboolib.flcontrols import ProjectClass
from pineboolib import decorators
from pineboolib.utils import filedir





class FLSettings(ProjectClass):
    
    s = QtCore.QSettings(QtCore.QSettings.NativeFormat, QtCore.QSettings.UserScope,"Eneboo","Pineboo")
    
    @decorators.BetaImplementation 
    def readListEntry(self, key, retOk = False):
        ret = []
        if key in self.s:
            ret = self.s.value(key)
        return ret
        
    def readEntry(self, _key, _def = None, retOk = False):

        
        ret = self.s.value(_key, None) #devuelve un QVariant !!!!
        
        if "geo" in _key:
            ret = ret.toSize()
            print("Geo vale", ret)
            if not ret:
                ret = _def
        else:
            if ret.toString() == "":
                ret = _def
        
        #print("Retornando %s ---> %s" % (_key, ret))          
        return ret
    
    @decorators.BetaImplementation
    def readNumEntry(self, key, _def = 0, retOk = False):
        ret = self.s.value(key)
        return int(ret)
        
    @decorators.BetaImplementation
    def readDoubleEntry(self, key, _def = 0, retOk = False):
        ret = self.s.value(key)
        return float(ret)
    
    @decorators.BetaImplementation
    def readBoolEntry(self, key, _def = False, retOk = False):
        ret = self.s.value(key)
        return bool(ret)
        
    @decorators.BetaImplementation
    def writeEntry(self, key, value):
        self.s.setValue(key, value)
    
    @decorators.BetaImplementation
    def writeEntryList(self, key, value):
        self.s.setValue(key, value)