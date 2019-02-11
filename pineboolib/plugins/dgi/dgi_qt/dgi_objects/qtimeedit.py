# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, Qt

class QTimeEdit(QtWidgets.QTimeEdit):
    
    def __init__(self, parent = None):
        super().__init__(parent)
        
        self.setDisplayFormat("hh:mm:ss A")

    def setTime(self, time):
        if not isinstance(time, Qt.QTime):
            t_list = time.split(":")
            time = Qt.QTime(int(t_list[0]), int(t_list[1]), int(t_list[2]))
        super().setTime(time)
    
    def getTime(self):
        return super().time().toString("hh:mm:ss")
    
    

    time = property(getTime, setTime)