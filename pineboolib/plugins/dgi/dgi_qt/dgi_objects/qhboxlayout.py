# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets

class QHBoxLayout(QtWidgets.QHBoxLayout):
    
    def __init__(self, parent):
        print("Creando QHBox y se pasa", parent)
        if isinstance(parent, QtWidgets.QWidget):
            print("H1", parent)
            super().__init__(parent)
        else:
            print("H2", parent)
            super().__init__()
            parent.addLayout(self)
        
        self.setContentsMargins(1, 1, 1, 1)
        self.setSpacing(1)
        self.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
            