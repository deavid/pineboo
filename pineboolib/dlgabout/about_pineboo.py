# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget

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
        mM = FLManagerModules()
    
        dlg_ = filedir('dlgabout/about_pineboo.ui')
        version_ = pineboolib.project.version
        self.ui = mM.createUI(dlg_, None, self)
        self.ui.lbl_version.setText("Pineboo v%s" % version_)
        self.ui.btn_close.clicked.connect(self.ui.close)
        self.ui.show()
    