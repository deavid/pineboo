# -*- coding: utf-8 -*-
from pineboolib import qsatype
from pineboolib.qsaglobals import *
import traceback
sys = SysType()

class FormInternalObj(qsatype.FormDBWidget):
    def _class_init(self):
        pass
    
    def main(self):
        sys.loadModules()
    


form = None
