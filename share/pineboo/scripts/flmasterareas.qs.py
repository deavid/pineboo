# -*- coding: utf-8 -*-
from pineboolib.qsa import *
sys = SysType()

class FormInternalObj(FormDBWidget):
    def _class_init(self):
        pass
    
    def init(self):
        connect(self.cursor(), u"cursorUpdated()", self, u"actualizarAreas")
    
    def actualizarAreas(self):
        sys.updateAreas()
    


form = None
