# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets

class QRadioButton(QtWidgets.QRadioButton):
    
    bg_id = None

    def __init__(self, parent = None):
        super().__init__(parent)
        self.setChecked(False)
        self.bg_id = None
                
        self.clicked.connect(self.send_clicked)
        
    def setButtonGroupId(self, id):  
        self.bg_id = id
        if self.parent() and hasattr(self.parent(), "selectedId"):
            if self.bg_id == self.parent().selectedId:
                self.setChecked(True)
    
    def send_clicked(self):
        if self.parent() and hasattr(self.parent(), "selectedId"):
            self.parent().presset.emit(self.dg_id)
        

    def __setattr__(self, name, value):
        if name == "text":
            self.setText(value)
        elif name == "checked":
            self.setChecked(value)
        else:
            super().__setattr__(name, value)

    def __getattr__(self, name):
        if name == "checked":
            return self.isChecked()
        else:
            print("QRadioButton", name)