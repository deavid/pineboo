# encoding: UTF-8
from __future__ import print_function
from __future__ import unicode_literals
from builtins import range
import traceback
import os.path
from binascii import unhexlify

from PyQt4 import QtGui, QtCore, uic
Qt = QtCore.Qt

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
        self.areasTab.removeItem(0) #Borramos tab de ejemplo.
        self.formTab = self.ui.formTab
        self.formTab.setTabsClosable(True)
        self.connect(self.formTab, QtCore.SIGNAL('tabCloseRequested(int)'), self.closeFormTab)
        self.formTab.removeTab(0)

    def closeFormTab(self, numero):
        #print"Cerrando pestaña número %d " % numero
        self.formTab.removeTab(numero)

    def addFormTab(self, action):
        widget = action.mainform_widget
        #print"Añadiendo Form a pestaña"
        icon = None
        try:
            icon = action.mod.mod.mainform.actions[action.name].icon
            self.formTab.addTab(widget, icon, widget.windowTitle())
        except Exception as e:
            print("ERROR: addFormTab: No pude localizar icono para %r. Error: %s" % (action.name, e))
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
        self.areasTab.addItem(vl, area.descripcion)


    def addModuleInTab(self, module):
        print("- Procesando %s " % module.name)
        #Creamos pestañas de areas y un vBLayout por cada módulo. Despues ahí metemos los actions de cada módulo
        if module.areaid not in self.areas:
            self.addAreaTab(Struct(idarea=module.areaid, descripcion=module.areaid))


        moduleToolBox = self.toolBoxs[self.areas.index(module.areaid)]

        vBLayout = QtGui.QWidget()
        vBLayout.layout = QtGui.QVBoxLayout() #layout de cada módulo.
        vBLayout.layout.setSpacing(1)
        vBLayout.layout.setContentsMargins(1, 1, 1, 1)

        vBLayout.setLayout(vBLayout.layout)

        moduleToolBox.addItem(vBLayout, module.description)

        try:
            self.moduleLoad(vBLayout.layout,module)
        except Exception:
            print("ERROR al procesar modulo %s:" % module.name)
            print(traceback.format_exc(), "---")

    def moduleLoad(self, vBLayout, module):
        if module.loaded == False: module.load()
        if module.loaded == False:
            print("WARN: Ignorando modulo %r por fallo al cargar" % (module.name))
            return False
        #print "Running module %s . . . " % self.name
        vBLayout.setSpacing(1)
        vBLayout.setContentsMargins(1,1,1,1)
        for key in module.mainform.toolbar:
            action = module.mainform.actions[key]

            button = QtGui.QToolButton()
            button.setText(action.text)
            button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
            button.setAutoRaise(True)
            if action.icon: button.setIcon(action.icon)
            button.clicked.connect(action.run)
            vBLayout.addWidget(button)


mainWindow = MainForm()


