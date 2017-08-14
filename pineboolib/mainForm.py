# -*- coding: utf-8 -*-

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
    debugLevel = 100
    
    @classmethod
    def setDebugLevel(self, q):
        MainForm.debugLevel = q
    
    def load(self):
        self.ui = uic.loadUi(filedir('forms/mainform.ui'), self)
        
        frameGm = self.frameGeometry()
        screen = QtGui.QApplication.desktop().screenNumber(QtGui.QApplication.desktop().cursor().pos())
        centerPoint = QtGui.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
        
        
        self.areasTab = self.ui.areasTab
        try:
            self.areasTab.removeItem = self.areasTab.removeTab
            self.areasTab.addItem = self.areasTab.addTab
        except Exception: pass
        self.areasTab.removeItem(0) #Borramos tab de ejemplo.
        self.formTab = self.ui.formTab
        self.formTab.setTabsClosable(True)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.connect(self.formTab, QtCore.SIGNAL('tabCloseRequested(int)'), self.closeFormTab)
        self.formTab.removeTab(0)
        app_icon = QtGui.QIcon()
        app_icon.addFile(filedir('icons/pineboo-logo-16.png'), QtCore.QSize(16,16))
        app_icon.addFile(filedir('icons/pineboo-logo-24.png'), QtCore.QSize(24,24))
        app_icon.addFile(filedir('icons/pineboo-logo-32.png'), QtCore.QSize(32,32))
        app_icon.addFile(filedir('icons/pineboo-logo-48.png'), QtCore.QSize(48,48))
        app_icon.addFile(filedir('icons/pineboo-logo-64.png'), QtCore.QSize(64,64))
        app_icon.addFile(filedir('icons/pineboo-logo-128.png'), QtCore.QSize(128,128))
        app_icon.addFile(filedir('icons/pineboo-logo-256.png'), QtCore.QSize(256,256))
        self.setWindowIcon(app_icon)
        self.setWindowTitle("Pineboo")


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
        vl.layout.setSpacing(0)
        vl.layout.setContentsMargins(0, 0, 0, 0)
        vl.layout.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)
        
        moduleToolBox = QtGui.QToolBox(self)#toolbox de cada módulo

        self.areas.append(area.idarea)
        self.toolBoxs.append(moduleToolBox)
        self.tab = self.tab + 1
        vl.setLayout(vl.layout)
        vl.layout.addWidget(moduleToolBox)
        self.areasTab.addItem(vl, area.descripcion)


    def addModuleInTab(self, module):
        if MainForm.debugLevel > 50: print("- Procesando %s " % module.name)
        #Creamos pestañas de areas y un vBLayout por cada módulo. Despues ahí metemos los actions de cada módulo
        if module.areaid not in self.areas:
            self.addAreaTab(Struct(idarea=module.areaid, descripcion=module.areaid))


        moduleToolBox = self.toolBoxs[self.areas.index(module.areaid)]

        vBLayout = QtGui.QWidget()
        vBLayout.layout = QtGui.QVBoxLayout() #layout de cada módulo.
        vBLayout.layout.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)

        vBLayout.layout.setSpacing(0)
        vBLayout.layout.setContentsMargins(0, 0, 0, 0)

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
        iconsize = QtCore.QSize(22,22)
        iconsize = QtCore.QSize(16,16)
        vBLayout.setSpacing(0)
        vBLayout.setContentsMargins(0,0,0,0)
        for key in module.mainform.toolbar:
            action = module.mainform.actions[key]

            button = QtGui.QToolButton()
            button.setText(action.text)
            button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
            button.setIconSize(iconsize)
            button.setAutoRaise(True)
            if action.icon: button.setIcon(action.icon)
            button.clicked.connect(action.run)
            vBLayout.addWidget(button)
        vBLayout.addStretch()
    
    
    
    def closeEvent(self, evnt):
        
        dialog = QtGui.QDialog()
        dialog.setWindowTitle("Salir de Pineboo")
        dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        _layout = QtGui.QVBoxLayout()
        dialog.setLayout(_layout)
        buttonBox = QtGui.QDialogButtonBox()
        OKButton = QtGui.QPushButton("&Aceptar")
        cancelButton = QtGui.QPushButton("&Cancelar")
        
        buttonBox.addButton(OKButton, QtGui.QDialogButtonBox.AcceptRole)
        buttonBox.addButton(cancelButton, QtGui.QDialogButtonBox.RejectRole)
        label = QtGui.QLabel("¿ Desea salir ?")
        _layout.addWidget(label)
        _layout.addWidget(buttonBox)
        OKButton.clicked.connect(dialog.accept)
        cancelButton.clicked.connect(dialog.reject)
        
        if not dialog.exec_():
            evnt.ignore()
        else:
            print("FIXME::Guardando pestañas abiertas ...")
        

mainWindow = MainForm()


