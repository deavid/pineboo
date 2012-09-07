# encoding: UTF-8
from PyQt4 import QtGui, uic
import main


class MainForm(QtGui.QWidget):
    def load(self):
        self.ui = uic.loadUi(main.filedir('forms/mainform.ui'), self)
        self.areasTab = self.ui.areasTab  
        self.areasTab.removeTab(0) #Borramos tab de ejemplo.
        
    areas = []
    toolBoxs = []
    tab = 0

    def addAreaTab(self, widget, module ):
        self.areasTab.addTab( widget, module.areaid)    

        
    def addModuleInTab(self, module):
        print "Procesando %s " % module.name
        #button = QtGui.QCommandLinkButton(module.description)
        #button.setText(module.description)
        #button.clicked.connect(module.run)
        vl = QtGui.QWidget()
        vBLayout = QtGui.QWidget()
        vBLayout.layout = QtGui.QVBoxLayout() #layout de cada módulo.
        vBLayout.setLayout(vBLayout.layout)
        #Creamos pestañas de areas y un vBLayout por cada módulo. Despues ahí metemos los actions de cada módulo
        if self.areas.count(module.areaid):
            i = 0
            for i in range(self.tab):
                if self.areas[i] == module.areaid:
                    moduleToolBox = self.toolBoxs[i]
                    print"Cargando en pestaña %d" % i
                    moduleToolBox.addItem(vBLayout, module.description)
                    
        else:
            print "Nueva Pestaña"
            vl.layout = QtGui.QVBoxLayout() #layout de la pestaña
            moduleToolBox = QtGui.QToolBox(self)#toolbox de cada módulo            
            moduleToolBox.addItem(vBLayout, module.description)
            
            self.areas.append(module.areaid)
            self.toolBoxs.append(moduleToolBox)
            self.tab = self.tab + 1
            vl.setLayout(vl.layout)
            vl.layout.addWidget(moduleToolBox)
            self.addAreaTab(vl, module)
            

        module.run(vBLayout.layout)            
                
                    