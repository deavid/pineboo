# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget, QApplication
from pineboolib.utils import DEPENDENCIES_CHECKED
from PyQt5 import QtCore

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
        self.ui.lbl_version.setText("Pineboo v%s" % str(version_))
        self.ui.btn_close.clicked.connect(self.ui.close)
        self.ui.btn_clipboard.clicked.connect(self.to_clipboard)
        self.ui.show()
        
        self.ui.lbl_librerias.setText(self.load_components())
    
    def load_components(self):
        components = "Versiones de componentes:\n\n"
        
        import sys
        import platform
        
        components += "S.O.: %s %s %s\n" % (platform.system(), platform.release(), platform.version())
        py_ver = sys.version
        if py_ver.find("(") > -1:
            py_ver = py_ver[:py_ver.find("(")]
            
        components += "Python: %s\n" % py_ver
        
        if not "PyQt5.QtCore" in DEPENDENCIES_CHECKED.keys():
            components += "PyQt5.QtCore : %s\n" % QtCore.QT_VERSION_STR
        else:
            print("Nooo")
        
        for k in DEPENDENCIES_CHECKED.keys():
            components += "%s: %s\n" % (k, DEPENDENCIES_CHECKED[k])
            
        
        
        
        
        
        return components
    
    def to_clipboard(self):
        
        clip_board = QApplication.clipboard()
        clip_board.clear()
        clip_board.setText(self.load_components())
        
        
        