# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget
from pineboolib.utils import DEPENDENCIES_CHECKED

class about_pineboo(QWidget):
    
    ui = None
    
    def __init__(self):
        super().__init__()
        self.load()
    

    def load(self):
        from PyQt5 import uic
    
        import pineboolib
        from pineboolib.fllegacy.flmanagermodules import FLManagerModules
        from pineboolib.utils import filedir
        mng_mod = FLManagerModules()
    
        dlg_ = filedir('dlgabout/about_pineboo.ui')
        version_ = pineboolib.project.version
        self.ui = mng_mod.createUI(dlg_, None, self)
        self.ui.lbl_version.setText("Pineboo v%s" % version_)
        self.ui.btn_close.clicked.connect(self.ui.close)
        self.ui.show()
        
        self.ui.lbl_librerias.setText(self.load_components())
    
    def load_components(self):
        components = "Versiones de componentes:\n\n"
        
        for k in DEPENDENCIES_CHECKED.keys():
            components += "%s = %s\n" % (k, DEPENDENCIES_CHECKED[k])
            
        
        
        
        
        
        return components
        
        