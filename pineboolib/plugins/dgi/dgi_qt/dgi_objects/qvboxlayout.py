# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets

class QVBoxLayout(QtWidgets.QVBoxLayout):
    
    def __init__(self, parent):
        if isinstance(parent, QtWidgets.QWidget):
            super().__init__(parent)
        else:
            super().__init__()
            parent.addLayout(self)
            
        
        self.setContentsMargins(1, 1, 1, 1)
        self.setSpacing(1)
        self.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
            
        