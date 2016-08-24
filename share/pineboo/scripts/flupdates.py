# encoding: UTF-8
from pineboolib import qsatype
from pineboolib.qsaglobals import *
import traceback

class interna(object):
    ctx = qsatype.Object()
    def __init__(self, context = None):
        self.ctx = context
    
    def main(self):
        self.ctx.interna_main()
    

class oficial(interna):
    def __init__(self, context = None):
        super(oficial, self).__init__(context)
    

class head(oficial):
    def __init__(self, context = None):
        super(head, self).__init__(context)
    

class ifaceCtx(head):
    def __init__(self, context = None):
        super(ifaceCtx, self).__init__(context)
    

class FormInternalObj(qsatype.FormDBWidget):
    def _class_init(self):
        # DEBUG:: Const Declaration:
        self.iface = ifaceCtx(self)
    
    def interna_main(self):
        sys.updatePineboo()
    


form = None
