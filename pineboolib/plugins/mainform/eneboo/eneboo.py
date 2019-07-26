# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtCore, QtGui  # type: ignore
from PyQt5.QtWidgets import QTreeWidgetItem, QTreeWidget, QMainWindow, QActionGroup, QMenu  # type: ignore
from PyQt5.QtXml import QDomDocument  # type: ignore

# from pineboolib.core.settings import settings
from pineboolib.fllegacy.aqsobjects.aqs import AQS
from pineboolib import pncontrolsfactory
from pineboolib.fllegacy.aqsobjects.aqsobjectfactory import AQUtil, AQSettings
from pineboolib.pncontrolsfactory import aqApp
from pineboolib import logging
from typing import Any


logger = logging.getLogger("mainForm_%s" % __name__)


class MainForm(QtWidgets.QMainWindow):

    MAX_RECENT = 10
    app_ = None
    ag_menu_ = None
    ag_rec_ = None
    ag_mar_ = None
    dck_mod_ = None
    dck_rec_ = None
    dck_mar_ = None
    tw_ = None
    tw_corner = None  # deprecated
    act_sig_map_ = None
    initialized_mods_ = None
    main_widgets_ = {}
    lista_tabs_ = []

    def __init__(self) -> None:

        super(MainForm, self).__init__()

        self.qsa_sys = pncontrolsfactory.SysType()

        aqApp.main_widget_ = self

    def eventFilter(self, o, e) -> bool:

        if isinstance(e, pncontrolsfactory.AQS.ContextMenu):
            if o == getattr(self.dck_mod_, "w_", None):
                return self.addMarkFromItem(self.dck_mod_.lw_.currentItem(), e.globalPos())
            elif o == getattr(self.dck_rec_, "w_", None):
                return self.addMarkFromItem(self.dck_rec_.lw_.currentItem(), e.globalPos())
            elif o == getattr(self.dck_mar_, "w_", None):
                return self.removeMarkFromItem(self.dck_mar_.lw_.currentItem(), e.globalPos())

            # pinebooMenu = self.w_.child("pinebooMenu")
            # pinebooMenu.exec_(e.globalPos)
            return True

        elif isinstance(e, pncontrolsfactory.AQS.Close):
            if isinstance(o, MainForm):
                self.w_.setDisabled(True)
                ret = self.exit()
                if not ret:
                    self.w_.setDisabled(False)
                    e.ignore()

                return True

            elif isinstance(o, pncontrolsfactory.FLFormDB):
                self.formClosed()

            elif isinstance(o, pncontrolsfactory.QDockWidget):
                o.topLevelChanged.emit(False)

        elif isinstance(e, pncontrolsfactory.AQS.WindowStateChange):
            if self.qsa_sys.isNebulaBuild() and o == self.w_:
                if self.w_.minimized():
                    self.w_.showNormal()
                    self.w_.showFullScreen()
                    return True

                if not self.w_.fullScreen():
                    self.w_.showFullScreen()
                    return True

        elif isinstance(e, pncontrolsfactory.AQS.Show):
            if isinstance(o, pncontrolsfactory.FLFormDB):
                return True

        return False

    def createUi(self, ui_file) -> None:
        from pineboolib.application import project

        mng = project.conn.managerModules()
        self.w_ = mng.createUI(ui_file, None, self)
        self.w_.setObjectName("container")

    def exit(self) -> bool:

        res = pncontrolsfactory.QMessageBox.information(
            self.w_, "Pineboo", "¿ Quiere salir de la aplicación ?", pncontrolsfactory.QMessageBox.Yes, pncontrolsfactory.QMessageBox.No
        )
        doExit = True if res == pncontrolsfactory.QMessageBox.Yes else False
        if doExit:
            self.writeState()
            self.w_.removeEventFilter(self.w_)
            self.removeAllPages()

        return doExit

    def writeState(self) -> None:
        from pineboolib.application import project

        w = self.w_
        self.dck_mod_.writeState()
        self.dck_rec_.writeState()
        self.dck_mar_.writeState()

        settings = AQSettings()
        key = "MainWindow/"

        settings.writeEntry("%smaximized" % key, w.isMaximized())
        settings.writeEntry("%sx" % key, w.x())
        settings.writeEntry("%sy" % key, w.y())
        settings.writeEntry("%swidth" % key, w.width())
        settings.writeEntry("%sheight" % key, w.height())

        key += "%s/" % project.conn.database()

        open_actions = []

        for i in range(self.tw_.count()):
            open_actions.append(self.tw_.widget(i).idMDI())

        settings.writeEntryList("%sopenActions" % key, open_actions)
        settings.writeEntry("%scurrentPageIndex" % key, self.tw_.currentIndex())

        recent_actions = []
        root_recent = self.dck_rec_.lw_.invisibleRootItem()
        count_recent = root_recent.childCount()
        for i in range(count_recent):
            recent_actions.append(root_recent.child(i).text(1))
        settings.writeEntryList("%srecentActions" % key, recent_actions)

        mark_actions = []
        root_mark = self.dck_mar_.lw_.invisibleRootItem()
        count_mark = root_mark.childCount()
        for i in range(count_mark):
            mark_actions.append(root_mark.child(i).text(1))
        settings.writeEntryList("%smarkActions" % key, mark_actions)

    def readState(self) -> None:
        w = self.w_
        self.dck_mod_.readState()
        self.dck_rec_.readState()
        self.dck_mar_.readState()

        settings = AQSettings()
        key = "MainWindow/"

        if not self.qsa_sys.isNebulaBuild():
            maximized = settings.readBoolEntry("%smaximized" % key)

            if not maximized:
                x = settings.readNumEntry("%sx" % key)
                y = settings.readNumEntry("%sy" % key)
                if self.qsa_sys.osName() == "MACX" and y < 20:
                    y = 20
                w.move(x, y)
                w.resize(settings.readNumEntry("%swidth" % key, w.width()), settings.readNumEntry("%sheight" % key, w.height()))
            else:
                w.showMaximized()
        else:
            w.showFullScreen()

            aqApp.setProxyDesktop(w)

        self.loadTabs()

    def loadTabs(self) -> None:
        if self.ag_menu_:
            from pineboolib.application import project

            settings = AQSettings()
            key = "MainWindow/%s/" % project.conn.database()

            open_actions = settings.readListEntry("%sopenActions" % key)
            i = 0
            for i in range(self.tw_.count()):
                self.tw_.widget(i).close()

            for open_action in open_actions:
                action = self.ag_menu_.findChild(QtWidgets.QAction, open_action)
                if not action:
                    continue
                module_name = project.conn.managerModules().idModuleOfFile("%s.ui" % action.name)
                if module_name:
                    self.initModule(module_name)

                self.addForm(open_action, action.icon().pixmap(16, 16))

            idx = settings.readNumEntry("%scurrentPageIndex" % key)
            if idx > 0 and idx < len(self.tw_):
                self.tw_.setCurrentWidget(self.tw_.widget(idx))

            recent_actions = settings.readListEntry("%srecentActions" % key)
            for recent in reversed(recent_actions):
                self.addRecent(self.ag_menu_.findChild(QtWidgets.QAction, recent))

            mark_actions = settings.readListEntry("%smarkActions" % key)
            for mark in reversed(mark_actions):
                self.addMark(self.ag_menu_.findChild(QtWidgets.QAction, mark))

    def init(self) -> None:
        self.w_.statusBar().hide()
        self.main_widgets_ = {}
        self.initialized_mods_ = []
        self.act_sig_map_ = QtCore.QSignalMapper(self.w_)
        self.act_sig_map_.setObjectName("pinebooActSignalMap")
        self.act_sig_map_.mapped[str].connect(self.triggerAction)
        self.initTabWidget()
        self.initHelpMenu()
        self.initConfigMenu()
        self.initTextLabels()
        self.initDocks()
        self.initEventFilter()

    def initFromWidget(self, w) -> None:
        self.w_ = w
        self.main_widgets_ = {}
        self.initialized_mods_ = []
        self.act_sig_map_ = QtCore.QSignalMapper(self.w_)
        self.act_sig_map_.setObjectName("pinebooActSignalMap")
        self.tw_ = w.findChild(QtWidgets.QTabWidget, "tabWidget")
        self.agMenu_ = w.child("pinebooActionGroup", "QActionGroup")
        self.dck_mod_ = DockListView()
        self.dck_mod_.initFromWidget(w.child("pinebooDockModules", "QDockWindow"))
        self.dck_rec_ = DockListView()
        self.dck_rec_.initFromWidget(w.child("pinebooDockRecent", "QDockWindow"))
        self.dck_mar_ = DockListView()
        self.dck_mar_.initFromWidget(w.child("pinebooDockMark", "QDockWindow"))
        self.initEventFilter()

    def initEventFilter(self) -> None:

        # w = self.w_
        self.w_.eventFilterFunction = "aqAppScript.mainWindow_.eventFilter"
        if not pncontrolsfactory.qsa_sys.isNebulaBuild():
            self.w_.allow_events = [pncontrolsfactory.AQS.ContextMenu, pncontrolsfactory.AQS.Close]
        else:
            self.w_.allow_events = [pncontrolsfactory.AQS.ContextMenu, pncontrolsfactory.AQS.Close, pncontrolsfactory.AQS.WindowStatechange]

        self.w_.installEventFilter(self)

        self.dck_mod_.w_.installEventFilter(self)
        self.dck_rec_.w_.installEventFilter(self)
        self.dck_mar_.w_.installEventFilter(self)

    def initModule(self, module) -> None:

        if module in self.main_widgets_:
            mwi = self.main_widgets_[module]
            mwi.name = module
            aqApp.name = module
            mwi.show()

        if module not in self.initialized_mods_:
            self.initialized_mods_.append(module)
            aqApp.call("%s.iface.init" % module, [], None, False)

        mng = aqApp.db().managerModules()
        mng.setActiveIdModule(module)

    def removeCurrentPage(self, n=None) -> None:
        if n is None:
            widget = self.tw_.currentWidget()
        else:
            widget = self.tw_.widget(n)

        if not widget:
            return

        if widget.__class__.__name__ == "FLFormDB":
            widget.close()

    def removeAllPages(self) -> None:

        # if len(tw):
        #    self.tw_corner.hide()

        for i in range(self.tw_.count()):
            self.tw_.widget(i).close()

    def formClosed(self) -> None:
        if self.tw_.count() == 1 and self.tw_corner:
            self.tw_corner.hide()

    def addForm(self, action_name, icono) -> None:
        tw = self.tw_
        for i in range(tw.count()):
            if tw.widget(i).action().name() == action_name:
                tw.widget(i).close()

        fm = pncontrolsfactory.AQFormDB(action_name, tw, None)
        fm.setMainWidget()
        if not fm.mainWidget():
            return

        tw.addTab(fm, self.ag_menu_.findChild(QtWidgets.QAction, action_name).icon(), fm.windowTitle())
        fm.setIdMDI(action_name)
        fm.show()
        # idx = tw.indexOf(fm)
        # self.tw_.setCurrentPage(idx)
        self.tw_.setCurrentWidget(fm)
        fm.installEventFilter(self.w_)
        # if len(tw.pages()) == 1 and self.tw_corner is not None:
        #    self.tw_corner.show()

    def addRecent(self, action) -> None:
        if not action:
            return

        if not self.ag_rec_:
            self.ag_rec_ = pncontrolsfactory.QActionGroup(self.w_)

        check_max = True

        new_ag_rec_ = pncontrolsfactory.QActionGroup(self.w_)
        new_ag_rec_.setObjectName("pinebooAgRec")

        for ac in self.ag_rec_.actions():
            if ac.objectName() == action.objectName():
                check_max = False
                continue

            self.cloneAction(ac, new_ag_rec_)

        self.cloneAction(action, new_ag_rec_)

        self.ag_rec_ = new_ag_rec_

        lw = self.dck_rec_.lw_
        if check_max and lw.topLevelItemCount() >= self.MAX_RECENT:
            last_name = lw.topLevelItem(lw.topLevelItemCount() - 1).text(1)
            ac = self.ag_rec_.findChild(QtWidgets.QAction, last_name)
            if ac:
                self.ag_rec_.removeAction(ac)
                del ac

        self.dck_rec_.update(self.ag_rec_)

    def addMark(self, action) -> None:
        if not action:
            return

        if not self.ag_mar_:
            self.ag_mar_ = QActionGroup(self.w_)

        new_ag_mar = QActionGroup(self.w_)
        new_ag_mar.setObjectName("pinebooAgMar")

        for ac in self.ag_mar_.actions():
            if ac.objectName() == action.objectName():
                continue

            self.cloneAction(ac, new_ag_mar)

        self.cloneAction(action, new_ag_mar)

        self.ag_mar_ = new_ag_mar

        self.dck_mar_.update(self.ag_mar_, True)

    def addMarkFromItem(self, item, pos) -> bool:
        if not item:
            return False

        if item.text(1) is None:
            return True

        popMenu = QMenu()
        popMenu.move(pos)
        popMenu.addAction(self.qsa_sys.translate("Añadir Marcadores"))
        res = popMenu.exec_()
        if res:
            ac = self.ag_menu_.findChild(QtWidgets.QAction, item.text(1))
            if ac:
                self.addMark(ac)

        return True

    def removeMarkFromItem(self, item, pos) -> bool:
        if not item or not self.ag_mar_ or self.dck_mar_.lw_.invisibleRootItem().childCount() == 0:
            return False

        if item.text(1) is None:
            return True

        popMenu = QMenu()
        popMenu.move(pos)
        popMenu.addAction(self.qsa_sys.translate("Eliminar Marcador"))
        res = popMenu.exec_()
        if res:
            ac = self.ag_mar_.findChild(QtWidgets.QAction, item.text(1))
            if ac:
                self.ag_mar_.removeAction(ac)
                del ac
                self.dck_mar_.update(self.ag_mar_)

        return True

    def updateMenu(self, action_group, parent) -> None:

        object_list = action_group.children()
        for obj_ in object_list:
            o_name = obj_.objectName()
            if isinstance(obj_, pncontrolsfactory.QActionGroup):
                new_parent = parent

                ac_name = obj_.findChild(QtWidgets.QAction, "%s_actiongroup_name" % o_name)
                if ac_name:
                    if not o_name.endswith("Actions") or o_name.endswith("MoreActions"):
                        new_parent = parent.addMenu(ac_name.icon(), ac_name.text())
                        new_parent.triggered.connect(ac_name.trigger)

                self.updateMenu(obj_, new_parent)
                continue

            if o_name.endswith("_actiongroup_name"):
                continue

            if o_name == "separator":
                a_ = parent.addAction("")
                a_.setSeparator(True)
            else:
                if isinstance(obj_, pncontrolsfactory.QAction):
                    a_ = parent.addAction(obj_.text())
                    a_.setIcon(obj_.icon())
                    a_.triggered.connect(obj_.activate)
                else:
                    continue

            a_.setObjectName(o_name)

    def updateMenuAndDocks(self) -> None:
        # FIXME: Duplicated piece of code
        self.updateActionGroup()
        pinebooMenu = self.w_.findChild(QtWidgets.QMenu, "menuPineboo")
        pinebooMenu.clear()
        self.updateMenu(self.ag_menu_, pinebooMenu)

        aqApp.setMainWidget(self.w_)
        self.dck_mod_.update(self.ag_menu_)
        self.dck_rec_.update(self.ag_rec_)
        self.dck_mar_.update(self.ag_mar_)
        self.w_.findChild(QtWidgets.QAction, "aboutQtAction").triggered.connect(aqApp.aboutQt)
        self.w_.findChild(QtWidgets.QAction, "aboutPinebooAction").triggered.connect(aqApp.aboutPineboo)
        self.w_.findChild(QtWidgets.QAction, "fontAction").triggered.connect(aqApp.chooseFont)
        # self.w_.findChild(QtWidgets.QAction, "style").triggered.connect(aqApp.showStyles)
        self.w_.findChild(QtWidgets.QAction, "helpIndexAction").triggered.connect(aqApp.helpIndex)
        self.w_.findChild(QtWidgets.QAction, "urlEnebooAction").triggered.connect(aqApp.urlPineboo)

    def updateActionGroup(self) -> None:

        if self.ag_menu_:
            list_ = self.ag_menu_.children()
            for obj in list_:
                if isinstance(obj, QtWidgets.QAction):
                    self.ag_menu_.removeAction(obj)
                    del obj

            self.ag_menu_.deleteLater()
            self.ag_menu_ = None

        self.ag_menu_ = pncontrolsfactory.QActionGroup(self.w_)
        self.ag_menu_.setObjectName("pinebooActionGroup")
        ac_name = pncontrolsfactory.QAction(self.ag_menu_)
        ac_name.setObjectName("pinebooActionGroup_actiongroup_name")
        ac_name.setText(self.qsa_sys.translate("Menú"))

        mng = aqApp.db().managerModules()
        areas = mng.listIdAreas()
        for area in areas:
            if not self.qsa_sys.isDebuggerEnabled() and area == "sys":
                break
            ag = pncontrolsfactory.QActionGroup(self.ag_menu_)
            ag.setObjectName(area)
            ag_action = pncontrolsfactory.QAction(ag)
            ag_action.setObjectName("%s_actiongroup_name" % ag.objectName())
            ag_action.setText(mng.idAreaToDescription(ag.objectName()))
            ag_action.setIcon(pncontrolsfactory.QIcon(pncontrolsfactory.AQS.pixmap_fromMimeSource("folder.png")))

            modules = mng.listIdModules(ag.objectName())
            for module in modules:
                if module == "sys" and self.qsa_sys.isUserBuild():
                    continue
                ac = pncontrolsfactory.QActionGroup(ag)
                ac.setObjectName(module)
                if self.qsa_sys.isQuickBuild():
                    if module == "sys":
                        continue
                actions = self.widgetActions("%s.ui" % ac.objectName(), ac)

                if not actions:
                    ac.setObjectName(None)
                    ac.deleteLater()
                    ac = pncontrolsfactory.QAction(ag)
                    ac.setObjectName(module)

                ac_action = pncontrolsfactory.QAction(ac)
                ac_action.setObjectName("%s_actiongroup_name" % ac.objectName())
                ac_action.setText(mng.idModuleToDescription(ac.objectName()))
                ac_action.setIcon(self.iconSet16x16(mng.iconModule(ac.objectName())))

                ac_action.triggered.connect(self.act_sig_map_.map)
                self.act_sig_map_.setMapping(ac_action, "triggered():initModule():%s_actiongroup_name" % ac.objectName())
                if ac.objectName() == "sys" and ag.objectName() == "sys":
                    if self.qsa_sys.isDebuggerMode():
                        staticLoad = pncontrolsfactory.QAction(ag)
                        staticLoad.setObjectName("staticLoaderSetupAction")
                        staticLoad.setText(self.qsa_sys.translate("Configurar carga estática"))
                        staticLoad.setIcon(pncontrolsfactory.QIcon(pncontrolsfactory.AQS.pixmap_fromMimeSource("folder_update.png")))
                        staticLoad.triggered.connect(self.act_sig_map_.map)
                        self.act_sig_map_.setMapping(staticLoad, "triggered():staticLoaderSetup():%s" % staticLoad.objectName())

                        reInit = pncontrolsfactory.QAction(ag)
                        reInit.setObjectName("reinitAction")
                        reInit.setText(self.qsa_sys.translate("Recargar scripts"))
                        reInit.setIcon(pncontrolsfactory.QIcon(pncontrolsfactory.AQS.pixmap_fromMimeSource("reload.png")))
                        reInit.triggered.connect(self.act_sig_map_.map)
                        self.act_sig_map_.setMapping(reInit, "triggered():reinit():%s" % reInit.objectName())

        shConsole = pncontrolsfactory.QAction(self.ag_menu_)
        shConsole.setObjectName("shConsoleAction")
        shConsole.setText(self.qsa_sys.translate("Mostrar Consola de mensajes"))
        shConsole.setIcon(pncontrolsfactory.QIcon(pncontrolsfactory.AQS.pixmap_fromMimeSource("consola.png")))
        shConsole.triggered.connect(self.act_sig_map_.map)
        self.act_sig_map_.setMapping(shConsole, "triggered():shConsole():%s" % shConsole.objectName())

        exit = pncontrolsfactory.QAction(self.ag_menu_)
        exit.setObjectName("exitAction")
        exit.setText(self.qsa_sys.translate("&Salir"))
        exit.setIcon(pncontrolsfactory.QIcon(pncontrolsfactory.AQS.pixmap_fromMimeSource("exit.png")))
        exit.triggered.connect(self.act_sig_map_.map)
        self.act_sig_map_.setMapping(exit, "triggered():exit():%s" % exit.objectName())

    def initTabWidget(self) -> None:
        self.tw_ = self.w_.findChild(QtWidgets.QTabWidget, "tabWidget")
        self.tw_.setTabsClosable(True)
        self.tw_.tabCloseRequested[int].connect(self.removeCurrentPage)
        self.tw_.removeTab(0)
        """
        tb = self.tw_corner = QToolButton(tw, "tabWidgetCorner")
        tb.autoRaise = False
        tb.setFixedSize(16, 16)
        tb.setIconSet(self.iconset16x16(AQS.pixmap_fromMimeSource("file_close.png")))
        tb.clicked.connect(self.removeCurrentPage)
        tw.setCornerWidget(tb, AQS.TopRight)
        AQS.toolTip_add(tb, self.qsa_sys.translate("Cerrar pestaña"))
        tb.hide()
        """

    def initHelpMenu(self) -> None:

        aboutQt = self.w_.findChild(QtWidgets.QAction, "aboutQtAction")
        aboutQt.setIcon(self.iconSet16x16(AQS.pixmap_fromMimeSource("aboutqt.png")))
        # aboutQt.triggered.connect(aqApp.aboutQt)

        aboutPineboo = self.w_.findChild(QtWidgets.QAction, "aboutPinebooAction")
        aboutPineboo.setIcon(self.iconSet16x16(AQS.pixmap_fromMimeSource("pineboo-logo-32.png")))
        # aboutPineboo.triggered.connect(aqApp.aboutPineboo)

        helpIndex = self.w_.findChild(QtWidgets.QAction, "helpIndexAction")
        helpIndex.setIcon(self.iconSet16x16(AQS.pixmap_fromMimeSource("help_index.png")))
        # helpIndex.triggered.connect(aqApp.helpIndex)

        urlPineboo = self.w_.findChild(QtWidgets.QAction, "urlEnebooAction")
        urlPineboo.setIcon(self.iconSet16x16(AQS.pixmap_fromMimeSource("pineboo-logo-32.png")))
        # urlPineboo.triggered.connect(aqApp.urlPineboo)

    def initConfigMenu(self) -> None:

        font = self.w_.findChild(QtWidgets.QAction, "fontAction")
        font.setIcon(self.iconSet16x16(AQS.pixmap_fromMimeSource("font.png")))
        # font.triggered.connect(aqApp.chooseFont)

        style = self.w_.findChild(QtWidgets.QMenu, "style")

        aqApp.initStyles()
        style.setIcon(self.iconSet16x16(AQS.pixmap_fromMimeSource("estilo.png")))
        # style.triggered.connect(aqApp.showStyles)

    def initTextLabels(self) -> None:

        tL = self.w_.findChild(QtWidgets.QLabel, "tLabel")
        tL2 = self.w_.findChild(QtWidgets.QLabel, "tLabel2")
        texto = AQUtil.sqlSelect("flsettings", "valor", "flkey='verticalName'")
        if texto and texto != "False":
            tL.setText(texto)

        if AQUtil.sqlSelect("flsettings", "valor", "flkey='PosInfo'") == "True":
            text_ = "%s@%s" % (self.qsa_sys.nameUser(), self.qsa_sys.nameBD())
            if self.qsa_sys.osName() == "MACX":
                text_ += "     "

            tL2.setText(text_)

    def initDocks(self) -> None:

        self.dck_mar_ = DockListView(self.w_, "pinebooDockMarks", pncontrolsfactory.qsa_sys.translate("Marcadores"))
        self.w_.addDockWidget(pncontrolsfactory.AQS.DockLeft, self.dck_mar_.w_)
        self.dck_rec_ = DockListView(self.w_, "pinebooDoctkRecent", pncontrolsfactory.qsa_sys.translate("Recientes"))
        self.w_.addDockWidget(pncontrolsfactory.AQS.DockLeft, self.dck_rec_.w_)
        self.dck_mod_ = DockListView(self.w_, "pinebooDockModules", pncontrolsfactory.qsa_sys.translate("Módulos"))
        self.w_.addDockWidget(pncontrolsfactory.AQS.DockLeft, self.dck_mod_.w_)

        windowMenu = self.w_.findChild(QtWidgets.QMenu, "windowMenu")
        sub_menu = windowMenu.addMenu(pncontrolsfactory.qsa_sys.translate("&Vistas"))

        docks = self.w_.findChildren(DockListView)
        for dock in docks:
            ac = sub_menu.addAction(dock.w_.windowTitle())
            ac.setCheckable(True)
            # FIXME: Comprobar si estoy visible o no
            # ac.setChecked(dock.w_.isVisible())
            dock.set_visible.connect(ac.setChecked)
            ac.triggered.connect(dock.change_state)
            dock.w_.topLevelChanged.connect(ac.setChecked)
            # dock.w_.Close.connect(ac.setChecked)

    def cloneAction(self, act, parent) -> Any:

        ac = pncontrolsfactory.QAction(parent)
        ac.setObjectName(act.objectName())
        ac.setText(act.text())
        ac.setStatusTip(act.statusTip())
        ac.setToolTip(act.toolTip())
        ac.setWhatsThis(act.whatsThis())
        ac.setEnabled(act.isEnabled())
        ac.setVisible(act.isVisible())
        ac.triggered.connect(act.trigger)
        ac.toggled.connect(act.toggle)
        if not act.icon().isNull():
            ac.setIcon(self.iconSet16x16(act.icon().pixmap(16, 16)))

        return ac

    def addActions(self, node, actGroup, wi) -> None:
        actions = node.elementsByTagName("action")
        i = 0
        while i < actions.length():
            itn = actions.at(i).toElement()
            acw = wi.findChild(QtWidgets.QAction, itn.attribute("name"))
            if acw is None:
                i += 1
                continue

            prev = itn.previousSibling().toElement()
            if not prev.isNull() and prev.tagName() == "separator":
                sep_ = actGroup.addAction("separator")
                sep_.setObjectName("separator")
                sep_.setSeparator(True)
                # actGroup.addSeparator()

            self.cloneAction(acw, actGroup)
            i += 1

    def widgetActions(self, ui_file, parent) -> Any:

        mng = aqApp.db().managerModules()
        doc = QDomDocument()
        cc = mng.contentCached(ui_file)
        if not cc or not doc.setContent(cc):
            if cc:
                logger.warning("No se ha podido cargar %s" % (ui_file))
            return None

        w = mng.createUI(ui_file)

        if not w or not isinstance(w, QMainWindow):
            if w:
                self.main_widgets_[w.objectName()] = w

            return None

        w.setObjectName(parent.objectName())
        aqApp.setMainWidget(w)
        # if (self.qsa_sys.isNebulaBuild()):
        #    w.show()

        w.hide()

        settings = AQSettings()
        reduced = settings.readBoolEntry("ebcomportamiento/ActionsMenuRed")
        root = doc.documentElement().toElement()

        ag = pncontrolsfactory.QActionGroup(parent)
        ag.setObjectName("%sActions" % parent.objectName())
        # ag.menuText = ag.text = self.qsa_sys.translate("Acciones")
        if not reduced:
            bars = root.namedItem("toolbars").toElement()
            self.addActions(bars, ag, w)

        menu = root.namedItem("menubar").toElement()
        items = menu.elementsByTagName("item")
        if len(items) > 0:
            if not reduced:
                sep_ = ag.addAction("separator")
                sep_.setObjectName("separator")
                sep_.setSeparator(True)

                menu_ag = pncontrolsfactory.QActionGroup(ag)
                menu_ag.setObjectName("%sMore" % ag.objectName())
                menu_ag_name = pncontrolsfactory.QAction(menu_ag)
                menu_ag_name.setObjectName("%s_actiongroup_name" % ag.objectName())
                menu_ag_name.setText(self.qsa_sys.translate("Más"))
                menu_ag_name.setIcon(pncontrolsfactory.QIcon(pncontrolsfactory.AQS.pixmap_fromMimeSource("plus.png")))

            i = 0
            while i < items.length():
                itn = items.at(i).toElement()
                if itn.parentNode().toElement().tagName() == "item":
                    i += 1
                    continue

                if not reduced:
                    sub_menu_ag = pncontrolsfactory.QActionGroup(menu_ag)
                    sub_menu_ag.setObjectName("%sActions" % menu_ag.objectName())
                else:
                    sub_menu_ag = pncontrolsfactory.QActionGroup(ag)
                    sub_menu_ag.setObjectName(ag.objectName())

                sub_menu_ag_name = pncontrolsfactory.QAction(sub_menu_ag)
                sub_menu_ag_name.setObjectName("%s_actiongroup_name" % sub_menu_ag.objectName())
                sub_menu_ag_name.setText(self.qsa_sys.toUnicode(itn.attribute("text"), "UTF-8"))
                self.addActions(itn, sub_menu_ag, w)
                i += 1

        conns = root.namedItem("connections").toElement()
        connections = conns.elementsByTagName("connection")
        i = 0
        while i < connections.length():
            itn = connections.at(i).toElement()
            sender = itn.namedItem("sender").toElement().text()
            ac = ag.findChild(QtWidgets.QAction, sender)
            if ac:

                signal = itn.namedItem("signal").toElement().text()
                if signal == "activated()":
                    signal_fix = "triggered"
                    signal = "triggered()"
                slot = itn.namedItem("slot").toElement().text()
                getattr(ac, signal_fix).connect(self.act_sig_map_.map)
                self.act_sig_map_.setMapping(ac, "%s:%s:%s" % (signal, slot, ac.name))
                # getattr(ac, signal).connect(self.act_sig_map_.map)
                # ac.triggered.connect(self.triggerAction)

                # print("Guardando señales  %s:%s:%s de %s" % (signal, slot, ac.name, ac))

            i += 1

        aqApp.setMainWidget(None)
        w.close()
        return ag

    def iconSet16x16(self, pix) -> Any:
        p_ = QtGui.QPixmap(pix)
        # img_ = p_.convertToImage()
        # img_.smoothScale(16, 16)
        # ret = QIconSet(QPixmap(img_))
        img_ = QtGui.QImage(p_)
        if not img_.isNull():
            img_ = img_.scaled(16, 16)
        ret = QtGui.QIcon(QtGui.QPixmap(img_))
        return ret

    def show(self) -> None:
        super(MainForm, self).show()
        self.activateWindow()

    def initScript(self) -> None:
        from pineboolib.core.utils.utils_base import filedir

        mw = mainWindow
        mw.createUi(filedir("plugins/mainform/eneboo/mainform.ui"))

        mw.init()

        mw.updateMenuAndDocks()
        mw.initModule("sys")
        mw.show()

        mw.readState()

    def reinitSript(self) -> None:

        main_wid = aqApp.mainWidget() if mainWindow.w_ is None else mainWindow.w_
        if main_wid is None or main_wid.objectName() != "container":
            return

        mw = mainWindow
        # mw.initFormWidget(main_wid)
        mw.writeState()
        mw.removeAllPages()
        mw.w_.findChild(QtWidgets.QAction, "aboutQtAction").triggered.disconnect(aqApp.aboutQt)
        mw.w_.findChild(QtWidgets.QAction, "aboutPinebooAction").triggered.disconnect(aqApp.aboutPineboo)
        mw.updateMenuAndDocks()
        mw.initModule("sys")
        mw.readState()

    def aqAppScriptMain(self) -> None:
        pass

    def triggerAction(self, signature) -> None:
        mw = mainWindow
        sgt = signature.split(":")
        # ok = True
        ac = mw.ag_menu_.findChild(QtWidgets.QAction, sgt[2])
        if ac is None:
            logger.debug("triggerAction: Action not Found: %s" % signature)
            return

        signal = sgt[0]
        if signal == "triggered()":
            if not ac.isVisible() or not ac.isEnabled():
                return
        else:
            logger.debug("triggerAction: Unhandled signal: %s" % signature)
            return

        fn_ = sgt[1]
        if fn_ == "initModule()":
            mw.initModule(ac.objectName().replace("_actiongroup_name", ""))

        elif fn_ == "openDefaultForm()":
            mw.addForm(ac.name, ac.icon().pixmap(16, 16))
            mw.addRecent(ac)

        elif fn_ == "execDefaultScript()":
            aqApp.execMainScript(ac.objectName())
            mw.addRecent(ac)

        elif fn_ == "loadModules()":
            self.qsa_sys.loadModules()

        elif fn_ == "exportModules()":
            self.qsa_sys.exportModules()

        elif fn_ == "importModules()":
            self.qsa_sys.importModules()

        elif fn_ == "updatePineboo()":
            self.qsa_sys.updatePineboo()

        elif fn_ == "dumpDatabase()":
            self.qsa_sys.dumpDatabase()

        elif fn_ == "staticLoaderSetup()":
            aqApp.staticLoaderSetup()

        elif fn_ == "reinit()":
            self.qsa_sys.reinit()

        elif fn_ == "mrProper()":
            self.qsa_sys.Mr_Proper()

        elif fn_ == "shConsole()":
            aqApp.showConsole()

        elif fn_ == "exit()":
            self.close()

        else:
            logger.debug("tiggerAction: Unhandled slot : %s" % signature)

    # def load(self):
    #    from pineboolib.core.utils.utils_base import filedir
    #    self.ui_ = project.conn.managerModules().createUI(filedir('plugins/mainform/eneboo/mainform.ui'), None, self)

    @classmethod
    def setDebugLevel(self, q) -> None:
        MainForm.debugLevel = q

    def child(self, name) -> Any:
        return self.w_.findChild(QtWidgets.QWidget, name)


class DockListView(QtCore.QObject):

    w_ = None
    lw_ = None
    ag_ = None
    _name = None
    set_visible = QtCore.pyqtSignal(bool)
    Close = QtCore.pyqtSignal(bool)

    def __init__(self, parent=None, name="", title="") -> None:

        super(DockListView, self).__init__(parent)
        if parent is None:
            return

        self.w_ = QtWidgets.QDockWidget(name, parent)
        self.w_.setObjectName("%sListView" % name)
        self.lw_ = QTreeWidget(self.w_)
        self.lw_.setObjectName(self._name)
        # this.lw_.addColumn("");
        # this.lw_.addColumn("");
        self.lw_.setColumnCount(2)
        self.lw_.setHeaderLabels(["", ""])
        self.lw_.headerItem().setHidden(True)
        # this.lw_.setSorting(-1);
        # this.lw_.rootIsDecorated = true;
        # this.lw_.setColumnWidthMode(1, 0);
        self.lw_.hideColumn(1)
        # self.lw_.headerItem().hide()
        # self.lw_.headerItem().setResizeEnabled(false, 1)

        self.w_.setWidget(self.lw_)
        self.w_.setWindowTitle(title)

        """
        w.resizeEnabled = true;
        w.closeMode = true;
        w.setFixedExtentWidth(300);
        """

        self.lw_.doubleClicked.connect(self.activateAction)

    def writeState(self) -> None:

        settings = AQSettings()
        key = "MainWindow/%s/" % self.w_.objectName()
        # FIXME
        # settings.writeEntry("%splace" % key, self.w_.place())  # Donde está emplazado

        settings.writeEntry("%svisible" % key, self.w_.isVisible())
        settings.writeEntry("%sx" % key, self.w_.x())
        settings.writeEntry("%sy" % key, self.w_.y())
        settings.writeEntry("%swidth" % key, self.w_.width())
        settings.writeEntry("%sheight" % key, self.w_.height())
        # FIXME
        # settings.writeEntry("%soffset", key, self.offset())
        # area = self.area()
        # settings.writeEntry("%sindex" % key, area.findDockWindow(self.w_) if area else None)

    def readState(self) -> None:

        settings = AQSettings()
        key = "MainWindow/%s/" % self.w_.objectName()
        # FIXME
        # place = settings.readNumEntry("%splace" % key, AQS.InDock)
        # if place == AQS.OutSideDock:
        #    self.w_.setFloating(True)
        #    self.w_.move(settings.readNumEntry("%sx" % key, self.w_.x()),
        #                 settings.readNumEntry("%sy" % key, self.w_.y()))

        # self.w_.offset = settings.readNumEntry("%soffset" % key, self.offset)
        # index = settings.readNumEntry("%sindex" % key, None)
        # FIXME
        # if index is not None:
        #    area = w.area()
        #    if area:
        #        area.moveDockWindow(w, index)

        width = settings.readNumEntry("%swidth" % key, self.w_.width())
        height = settings.readNumEntry("%sheight" % key, self.w_.height())
        self.lw_.resize(width, height)
        # self.w_.resize(width, height)
        from pineboolib.application import project

        if not project.DGI.mobilePlatform():
            visible = settings.readBoolEntry("%svisible" % key, True)
            if visible:
                self.w_.show()

            else:
                self.w_.hide()

            self.set_visible.emit(not self.w_.isHidden())
        else:
            self.w_.hide()
            self.set_visible.emit(False)
            self.w_.close()

    def initFromWidget(self, w) -> None:
        self.w_ = w
        self.lw_ = w.widget()
        self.lw_.doubleClicked.connect(self.activateAction)

    def change_state(self, s) -> None:
        if s:
            self.w_.show()
        else:
            self.w_.close()

    def activateAction(self, item) -> None:
        if item is None:
            return

        action_name = item.sibling(item.row(), 1).data()
        if action_name == "":
            return

        ac = self.ag_.findChild(pncontrolsfactory.QAction, action_name)
        if ac:
            ac.triggered.emit()

    def update(self, action_group=None, reverse=False) -> None:
        from pineboolib.fllegacy.aqsobjects.aqs import AQS

        self.ag_ = action_group

        if not self.ag_:
            return

        self.lw_.clear()

        self.buildListView(self.lw_, AQS().toXml(self.ag_), self.ag_, reverse)

    def buildListView(self, parent_item, parent_element, ag, reverse) -> None:
        this_item = None
        node = parent_element.lastChild().toElement() if reverse else parent_element.firstChild().toElement()
        while not node.isNull():
            if node.attribute("objectName") in ("", "separator"):  # Pasamos de este
                node = node.previousSibling().toElement() if reverse else node.nextSibling().toElement()
                continue
            class_name = node.attribute("class")
            if class_name.startswith("QAction"):
                if node.attribute("visible") == "false":
                    node = node.previousSibling().toElement() if reverse else node.nextSibling().toElement()
                    continue

                if class_name == "QActionGroup":
                    group_name = node.attribute("objectName")
                    if (
                        group_name not in ("pinebooActionGroup")
                        and not group_name.endswith("Actions")
                        and not group_name.startswith(("pinebooAg"))
                    ) or group_name.endswith("MoreActions"):

                        this_item = QTreeWidgetItem(parent_item)
                        this_item.setText(0, group_name)

                    else:
                        this_item = parent_item

                    self.buildListView(this_item, node, ag, reverse)
                    node = node.previousSibling().toElement() if reverse else node.nextSibling().toElement()
                    continue

                if node.attribute("objectName") not in ("pinebooActionGroup", "pinebooActionGroup_actiongroup_name"):

                    action_name = node.attribute("objectName")

                    ac = ag.findChild(QtWidgets.QAction, action_name)
                    if ac is not None:

                        if action_name.endswith("actiongroup_name"):
                            # action_name = action_name.replace("_actiongroup_name", "")
                            this_item = parent_item
                        else:
                            this_item = QTreeWidgetItem(parent_item)

                        this_item.setIcon(0, ac.icon())  # Code el icono mal!!
                        if class_name == "QAction":
                            this_item.setText(1, action_name)
                        this_item.setText(0, node.attribute("text").replace("&", ""))
                    if this_item is not None and node.attribute("enabled") == "false":
                        this_item.setEnabled(False)

                self.buildListView(this_item, node, ag, reverse)

            node = node.previousSibling().toElement() if reverse else node.nextSibling().toElement()


mainWindow = MainForm()
