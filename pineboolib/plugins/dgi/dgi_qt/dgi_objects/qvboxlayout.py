# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets

class QVBoxLayout(QtWidgets.QVBoxLayout):
    
    def __init__(self, parent):
        print("Creando QVBox y se pasa", parent)
        if isinstance(parent, QtWidgets.QWidget):
            print("V1")
            super().__init__(parent)
        else:
            print("V2", parent)
            super().__init__()
            self.setParent(parent)
            
        
        self.setContentsMargins(1, 1, 1, 1)
        self.setSpacing(1)
        self.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
            
        