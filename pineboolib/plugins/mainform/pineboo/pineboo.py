# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
from pineboolib.utils import filedir, Struct
from pineboolib.fllegacy.FLSettings import FLSettings
import logging
from binascii import unhexlify
from PyQt5.QtWidgets import QAction
logger = logging.getLogger(__name__)

import pineboolib


class MainForm(QtWidgets.QMainWindow):
    areas = []
    toolBoxs = []
    tab = 0
    ui = None
    areasTab = None
    formTab = None
    debugLevel = 100
    dockAreasTab = None
    dockFavoritos = None
    dockForm = None
    mPAreas = {}  # Almacena los nombre de submenus areas de menú pineboo
    mPModulos = {}  # Almacena los nombre de submenus modulos de menú pineboo
    openTabs = []
    favoritosW = None

    @classmethod
    def setDebugLevel(self, q):
        MainForm.debugLevel = q

    def load(self):
        self.ui = uic.loadUi(
            filedir('plugins/mainform/pineboo/mainform.ui'), self)

        frameGm = self.frameGeometry()
        screen = QtWidgets.QApplication.desktop().screenNumber(
            QtWidgets.QApplication.desktop().cursor().pos())
        centerPoint = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

        self.areasTab = QtWidgets.QTabWidget()
        self.areasTab.setTabPosition(QtWidgets.QTabWidget.West)
        self.formTab = QtWidgets.QTabWidget()
        try:
            self.areasTab.removeItem = self.areasTab.removeTab
            self.areasTab.addItem = self.areasTab.addTab
        except Exception:
            pass

        self.dockAreasTab = QtWidgets.QDockWidget()
        self.dockAreasTab.setWindowTitle("Módulos")
        #self.dockAreas = QtWidgets.QDockWidget()
        self.dockFavoritos = QtWidgets.QDockWidget()
        self.dockFavoritos.setWindowTitle("Favoritos")

        self.dockForm = QtWidgets.QDockWidget()

        self.dockAreasTab.setWidget(self.areasTab)
        self.dockAreasTab.setMaximumWidth(400)
        self.dockFavoritos.setMaximumWidth(400)
        self.dockFavoritos.setMaximumHeight(500)
        # self.dockAreasTab.setMinimumWidth(400)
        # self.dockAreasTab.setMaximumHeight(500)

        self.dockForm.setWidget(self.formTab)

        self.addDockWidget(Qt.RightDockWidgetArea, self.dockForm)
        # self.dockForm.setMaximumWidth(950)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dockFavoritos)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dockAreasTab)
        # self.dockAreasTab.show()
        # self.dockForm.show()

        # self.areasTab.removeItem(0) #Borramos tab de ejemplo.

        self.formTab.setTabsClosable(True)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.formTab.tabCloseRequested[int].connect(self.closeFormTab)
        self.formTab.removeTab(0)
        #app_icon = QtGui.QIcon('share/icons/pineboo-logo-16.png')
        # app_icon.addFile(filedir('share/icons/pineboo-logo-16.png'),
        #                 QtCore.QSize(16, 16))
        # app_icon.addFile(filedir('share/icons/pineboo-logo-24.png'),
        #                 QtCore.QSize(24, 24))
        # app_icon.addFile(filedir('share/icons/pineboo-logo-32.png'),
        #                 QtCore.QSize(32, 32))
        # app_icon.addFile(filedir('share/icons/pineboo-logo-48.png'),
        #                 QtCore.QSize(48, 48))
        # app_icon.addFile(filedir('share/icons/pineboo-logo-64.png'),
        #                 QtCore.QSize(64, 64))
        # app_icon.addFile(filedir('share/icons/pineboo-logo-128.png'),
        #                 QtCore.QSize(128, 128))
        # app_icon.addFile(filedir('share/icons/pineboo-logo-256.png'),
        #                 QtCore.QSize(256, 256))
        # self.setWindowIcon(app_icon)
        self.setWindowIcon(QtGui.QIcon('share/icons/pineboo-logo-16.png'))
        self.actionAcercaQt.triggered.connect(pineboolib.main.aboutQt)
        self.actionAcercaPineboo.triggered.connect(pineboolib.main.aboutPineboo)
        self.actionFavoritos.triggered.connect(self.changeStateDockFavoritos)
        self.dockFavoritos.visibilityChanged.connect(self.changeStateActionFavoritos)
        self.actionModulos.triggered.connect(self.changeStateDockAreas)
        self.dockAreasTab.visibilityChanged.connect(self.changeStateActionAreas)
        self.actionTipografia.triggered.connect(pineboolib.main.fontDialog)
        self.menuPineboo.addSeparator()
        # self.actionEstilo.triggered.connect(pineboolib.main.styleDialog)
        pineboolib.main.initStyle(self.configMenu)
        self.setWindowTitle("Pineboo")
        self.loadPreferences()

    def closeFormTab(self, numero):
        if isinstance(numero, str):
            i = 0
            name = numero
            numero = None
            for n in self.openTabs:
                if name == n:
                    numero = i
                    break
                i = i + 1

        if numero is not None:
            logger.debug("Cerrando pestaña número %s ", numero)
            self.formTab.removeTab(numero)

            i = 0
            for name in self.openTabs:
                if i == numero:
                    self.openTabs.remove(name)
                    break
                i = i + 1

    def addFormTab(self, action):
        widget = action.mainform_widget
        if action.name in self.openTabs:
            self.closeFormTab(action.name)
        logger.debug("Añadiendo Form a pestaña %s", action)
        icon = None
        try:
            icon = action.mod.mod.mainform.actions[action.name].icon
            self.formTab.addTab(widget, icon, widget.windowTitle())
        except Exception as e:
            logger.warn("addFormTab: No pude localizar icono para %s: %s", action.name, e)
            self.formTab.addTab(widget, widget.windowTitle())

        self.formTab.setCurrentWidget(widget)
        self.openTabs.append(action.name)

    def loadArea(self, area):
        assert area.idarea not in self.areas
        vl = QtWidgets.QWidget()
        vl.layout = QtWidgets.QVBoxLayout()  # layout de la pestaña
        vl.layout.setSpacing(0)
        vl.layout.setContentsMargins(0, 0, 0, 0)
        vl.layout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)

        moduleToolBox = QtWidgets.QToolBox(self)  # toolbox de cada módulo

        self.areas.append(area.idarea)
        self.toolBoxs.append(moduleToolBox)
        self.tab = self.tab + 1
        vl.setLayout(vl.layout)
        vl.layout.addWidget(moduleToolBox)
        self.areasTab.addItem(vl, area.descripcion)

    def loadModule(self, module):
        logger.debug("loadModule: Procesando %s ", module.name)
        # Creamos pestañas de areas y un vBLayout por cada módulo. Despues ahí metemos los actions de cada módulo
        if module.areaid not in self.areas:
            self.loadArea(Struct(idarea=module.areaid,
                                 descripcion=module.areaid))

        moduleToolBox = self.toolBoxs[self.areas.index(module.areaid)]

        vBLayout = QtWidgets.QWidget()
        vBLayout.layout = QtWidgets.QVBoxLayout()  # layout de cada módulo.
        vBLayout.layout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)

        vBLayout.layout.setSpacing(0)
        vBLayout.layout.setContentsMargins(0, 0, 0, 0)

        vBLayout.setLayout(vBLayout.layout)
        if module.icon[0] != "":
            pixmap = QtGui.QPixmap(module.icon)
            moduleToolBox.addItem(vBLayout, QtGui.QIcon(pixmap), module.description)
        else:
            moduleToolBox.addItem(vBLayout, module.description)

        try:
            self.moduleLoad(vBLayout.layout, module)
        except Exception:
            logger.exception("ERROR al procesar modulo %s", module.name)

    def moduleLoad(self, vBLayout, module):
        if not module.loaded:
            module.load()
        if not module.loaded:
            logger.warn("moduleLoad: Ignorando modulo %s por fallo al cargar", module.name)
            return False
        logger.trace("moduleLoad: Running module %s . . . ", module.name)
        iconsize = QtCore.QSize(22, 22)
        iconsize = QtCore.QSize(16, 16)
        vBLayout.setSpacing(0)
        vBLayout.setContentsMargins(0, 0, 0, 0)
        for key in module.mainform.toolbar:
            action = module.mainform.actions[key]
            button = QtWidgets.QToolButton()
            button.setText(action.text)
            button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
            button.setIconSize(iconsize)
            button.setAutoRaise(True)
            if action.icon:
                button.setIcon(action.icon)
            button.clicked.connect(action.run)
            vBLayout.addWidget(button)
            self.addToMenuPineboo(action, module)
        vBLayout.addStretch()

    def closeEvent(self, evnt):

        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle("Salir de Pineboo")
        dialog.setWindowIcon(QtGui.QIcon('share/icons/pineboo-logo-16.png'))
        dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        _layout = QtWidgets.QVBoxLayout()
        dialog.setLayout(_layout)
        buttonBox = QtWidgets.QDialogButtonBox()
        OKButton = QtWidgets.QPushButton("&Aceptar")
        cancelButton = QtWidgets.QPushButton("&Cancelar")

        buttonBox.addButton(OKButton, QtWidgets.QDialogButtonBox.AcceptRole)
        buttonBox.addButton(
            cancelButton, QtWidgets.QDialogButtonBox.RejectRole)
        label = QtWidgets.QLabel("¿ Desea salir ?")
        _layout.addWidget(label)
        _layout.addWidget(buttonBox)
        OKButton.clicked.connect(dialog.accept)
        OKButton.clicked.connect(self.saveState)
        cancelButton.clicked.connect(dialog.reject)

        if not dialog.exec_():
            evnt.ignore()

    def saveState(self):
        sett_ = FLSettings()
        sett_.writeEntryList("application/mainForm/tabsOpened", self.openTabs)
        sett_.writeEntry("application/mainForm/viewFavorites", self.dockFavoritos.isVisible())
        sett_.writeEntry("application/mainForm/FavoritesSize", self.dockFavoritos.size())
        sett_.writeEntry("application/mainForm/viewAreas", self.dockAreasTab.isVisible())
        sett_.writeEntry("application/mainForm/AreasSize", self.dockFavoritos.size())
        sett_.writeEntry("application/mainForm/mainFormSize", self.size())

    def addToMenuPineboo(self, ac, mod):
        #print(mod.name, ac.name, pineboolib.project.areas[mod.areaid].descripcion)
        # Comprueba si el area ya se ha creado
        if mod.areaid not in self.mPAreas.keys():
            areaM = self.menuPineboo.addMenu(QtGui.QIcon('share/icons/gtk-open.png'), pineboolib.project.areas[mod.areaid].descripcion)
            self.mPAreas[mod.areaid] = areaM
        else:
            areaM = self.mPAreas[mod.areaid]

        # Comprueba si el modulo ya se ha creado
        if mod.name not in self.mPModulos.keys():
            pixmap = None
            if mod.icon[0] != "":
                pixmap = QtGui.QPixmap(mod.icon)
            if pixmap:
                moduloM = areaM.addMenu(QtGui.QIcon(pixmap), mod.description)
            else:
                moduloM = areaM.addMenu(mod.description)

            self.mPModulos[mod.name] = moduloM
        else:
            moduloM = self.mPModulos[mod.name]

        action_ = moduloM.addAction(ac.icon, ac.text)
        action_.triggered.connect(ac.run)

    def restoreOpenedTabs(self):
        # Cargamos pestañas abiertas
        sett_ = FLSettings()
        tabsOpened_ = sett_.readListEntry("application/mainForm/tabsOpened")
        if tabsOpened_:
            for t in tabsOpened_:
                for k, module in sorted(pineboolib.project.modules.items()):
                    if hasattr(module, "mainform"):
                        if t in module.mainform.actions:
                            module.mainform.actions[t].run()
                            break

    def loadPreferences(self):
        sett_ = FLSettings()
        viewFavorites_ = sett_.readBoolEntry("application/mainForm/viewFavorites", True)
        viewAreas_ = sett_.readBoolEntry("application/mainForm/viewAreas", True)
        sizeF_ = sett_.readEntry("application/mainForm/FavoritesSize", None)
        sizeA_ = sett_.readEntry("application/mainForm/AreasSize", None)
        sizeMF_ = sett_.readEntry("application/mainForm/mainFormSize", None)
        if sizeF_ is not None:
            self.dockFavoritos.resize(sizeF_)

        if sizeA_ is not None:
            self.dockAreasTab.resize(sizeA_)

        if sizeMF_ is not None:
            self.resize(sizeMF_)
        else:
            self.showMaximized()

        self.dockFavoritos.setVisible(viewFavorites_)
        self.actionFavoritos.setChecked(viewFavorites_)
        self.dockAreasTab.setVisible(viewAreas_)
        self.actionModulos.setChecked(viewAreas_)

    def changeStateDockFavoritos(self):
        visible_ = self.actionFavoritos.isChecked()
        if visible_:
            sett_ = FLSettings()
            sizeF_ = sett_.readEntry("application/mainForm/FavoritesSize", None)
            if sizeF_ is not None:
                self.dockFavoritos.resize(sizeF_)

        self.dockFavoritos.setVisible(visible_)

    def changeStateActionFavoritos(self):
        if self.dockFavoritos.isVisible():
            self.actionFavoritos.setChecked(True)
        else:
            self.actionFavoritos.setChecked(False)

    def changeStateDockAreas(self):
        visible_ = self.actionModulos.isChecked()
        if visible_:
            sett_ = FLSettings()
            sizeA_ = sett_.readEntry("application/mainForm/AreasSize", None)
            if sizeA_ is not None:
                self.dockAreasTab.resize(sizeA_)
        self.dockAreasTab.setVisible(visible_)

    def changeStateActionAreas(self):
        if self.dockAreasTab.isVisible():
            self.actionModulos.setChecked(True)
        else:
            self.actionModulos.setChecked(False)


mainWindow = MainForm()
