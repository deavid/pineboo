# encoding: UTF-8
from PyQt4 import QtGui, uic
import main


class MainForm(QtGui.QWidget):
    def load(self):
        self.ui = uic.loadUi(main.filedir('forms/mainform.ui'), self)
        self.areasTab = self.ui.areasTab  
        self.areasTab.removeTab(0) #Borramos tab de ejemplo.
        


    def addArea(self,areaName):
        self.tab = QtGui.QWidget()
        self.areasTab.addTab(self.tab, areaName)
        tb = QtGui.QToolBox()
        tb.setObjectName(areaName)        
        #Falta conectar cada toolbox con su tab
        #Falta boton cerrar y conectar
        