# encoding: UTF-8
from pineboolib import qsatype
from pineboolib.qsaglobals import *
import traceback

class FormInternalObj(qsatype.FormDBWidget):
    def _class_init(self):
        pass
    
    def init(self):
        connect(self.cursor(), u"cursorUpdated()", self, u"actualizarAreas")
    
    def actualizarAreas(self):
        sys.updateAreas()
    


form = None
