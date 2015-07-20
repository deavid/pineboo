# encoding: UTF-8
from __future__ import print_function
from __future__ import unicode_literals
from builtins import range
import traceback
import os.path

from PyQt4 import QtGui, QtCore, uic

from pineboolib.utils import filedir, Struct

class MainForm(QtGui.QWidget):
    areas = []
    toolBoxs = []
    tab = 0
    ui = None
    areasTab = None
    formTab = None

    def load(self):
        self.ui = uic.loadUi(filedir('forms/mainform.ui'), self)
        self.areasTab = self.ui.areasTab
        self.areasTab.removeTab(0) #Borramos tab de ejemplo.
        self.formTab = self.ui.formTab
        self.formTab.setTabsClosable(True)
        self.connect(self.formTab, QtCore.SIGNAL('tabCloseRequested(int)'), self.closeFormTab)
        self.formTab.removeTab(0)

    def closeFormTab(self, numero):
        #print"Cerrando pestaña número %d " % numero
        self.formTab.removeTab(numero)

    def addFormTab(self, widget):
        #print"Añadiendo Form a pestaña"
        self.formTab.addTab(widget, widget.windowTitle())
        self.formTab.setCurrentWidget(widget)



    def addAreaTab(self, area):
        assert area.idarea not in self.areas
        vl = QtGui.QWidget()
        vl.layout = QtGui.QVBoxLayout() #layout de la pestaña
        moduleToolBox = QtGui.QToolBox(self)#toolbox de cada módulo

        self.areas.append(area.idarea)
        self.toolBoxs.append(moduleToolBox)
        self.tab = self.tab + 1
        vl.setLayout(vl.layout)
        vl.layout.addWidget(moduleToolBox)
        self.areasTab.addTab(vl, area.descripcion)


    def addModuleInTab(self, module):
        print("- Procesando %s " % module.name)
        #Creamos pestañas de areas y un vBLayout por cada módulo. Despues ahí metemos los actions de cada módulo
        if module.areaid not in self.areas:
            self.addAreaTab(Struct(idarea=module.areaid, descripcion=module.areaid))


        moduleToolBox = self.toolBoxs[self.areas.index(module.areaid)]

        vBLayout = QtGui.QWidget()
        vBLayout.layout = QtGui.QVBoxLayout() #layout de cada módulo.
        vBLayout.layout.setSpacing(0)
        vBLayout.layout.setContentsMargins(1, 2, 2, 0)

        vBLayout.setLayout(vBLayout.layout)

        moduleToolBox.addItem(vBLayout, module.description)

        try:
            module.run(vBLayout.layout)
        except Exception:
            print("ERROR al procesar modulo %s:" % module.name)
            print(traceback.format_exc(), "---")

mainWindow = MainForm()


