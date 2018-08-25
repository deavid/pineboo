# -*- coding: utf-8 -*-
import pineboolib
from pineboolib.pncontrolsfactory import *


class MainForm(QMainWindow):

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
    main_windgets_ = None
    lista_tabs_ = []

    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)
        self.ui_ = None
        #self.app_ = QApplication

    def eventFilter(self, o, e):
        if e.type() == AQS.ContextMenu:
            if o == getattr(self.dck_mod_, "w_", None):
                return self.addMarkFromItem(self.dck_mod_.lw_.currentItem(), e.eventData.globalPos)
            elif o == getattr(self.dck_rec_, "w_", None):
                return self.addMarkFromItem(self.dck_rec_.lw_.currentItem(), e.eventData.globalPos)
            elif o == getattr(self.dck_mar_, "w_", None):
                return self.addMarkFromItem(self.dck_mar_.lw_.currentItem(), e.eventData.globalPos)

            pinebooMenu = self.w_.child("pinebooMenu")
            pinebooMenu.exec(e.eventData.globalPos)
            return True

        elif e.type() == AQS.Close:
            if aqApp.mainWidget() and o == aqApp.mainWidget():
                self.w_.setDisabled(True)
                ret = self.exit()
                if not ret:
                    self.w_.setDisabled(False)

                return True

            if o.rtti() == "FormDB":
                self.formClosed(o)

        elif e.type() == AQS.WindowStateChange:
            if sys.isNebulaBuild() and o == self.w_:
                if self.w_.minimized():
                    self.w_.showNormal()
                    self.w_.showFullScreen()
                    return True

                if not self.w_.fullScreen():
                    self.w_.showFullScreen()
                    return True

        return False

    def createUi(self, ui_file):
        mng = aqApp.db().managerModules()
        self.w_ = mgg.createUI(uiFile)
        self.w_.setObjectName("container")

    def exit(self):
        res = MessageBox.Information(sys.translate("¿Quiere salir de la aplicación?"), MessageBox.Yes, MessageBox.No, MessageBox.NoButton, "Pineboo")
        doExit = True if res == MessageBox.Yes else False
        if doExit:
            self.writeState()
            self.w_.removeEventFilter(self.w_)
            aqApp.generalExit(false)
            self.removeAllPages()

        return doExit

    def writeState(self):
        w = self.w_
        self.dck_mod_.writeState()
        self.dck_rec_.writeState()
        self.dck_mar_.wirteState()

        setting = AQSettings
        key = "MainWindow/"

        settings.writeEntry("%smaximized" % key, w.maximized())
        settings.writeEntry("%sx" % key, w.x())
        settings.writeEntry("%sy" % key, w.y())
        settings.writeEntry("%swidth" % key, w.width())
        settings.writeEntry("%sheight" % key, w.height())

        key += "%s/" % aqApp.db().database()

        open_actions = []

        for i in len(self.tw_):
            open_actions.append(tw.page(i).idMDI())

        settings.writeEntry("%sopenActions" % key, open_actions)
        settings.writeEntry("%scurrentPageIndex" % key, self.tw_.currentPageIndex())

        recent_actions = []
        item = self.dck_rec_.lw_.firstChild()
        while item:
            recent_actions.append(item.text(1))
            item = item.nextSibling()
        settings.writeEntry("%srecentActions" % key, open_actions)

        mark_actions = []
        item = self.dck_mar_.lw_.firstChild()
        while item:
            mark_actions.append(item.text(1))
            item = item.nextSibling()
        settings.writeEntry("%smarkActions" % key, mark_actions)

    def readState(self):
        w = self.w_
        self.dck_mod_.readState()
        self.dck_rec_.readState()
        self.dck_mar_.readState()

        settings = AQSettings
        key = "MainWindow/"

        if not sys.isNebulaBuild():
            maximized = settings.readBoolEntry("%smaximized" % key)

            if not maximized:
                x = settings.readNumEntry("%sx" % key)
                y = settings.readNumEntry("%sy" % key)
                if sys.osName() == "MACX" and y < 20:
                    y = 20
                w.move(x, y)
                w.resize(settings.readNumEntry("%swidth" % key, w.width()), settings.readNumEntry("%sheight" % key, w.height()))
            else:
                w.showMaximized()
        else:
            w.showFullScreen()
            aqApp.setProxyDesktop(w)

        if self.ag_menu_:
            key += "%s/" % aqApp.db().database()

            open_actions = settings.readListEntry("%sopenActions" % key)
            for i in len(self.tw_):
                self.tw_.page(i).close()

            for open_action in open_actions:
                action = self.ag_menu_.child(open_action, "QAction")
                if not action:
                    continue
                moduleName = aqApp.db().managerModules().idModuleOfFile("%s.ui" % action.name)
                if moduleName and moduleName != "":
                    self.initModule(moduleName)

                self.addForm(open_actions[i], action.iconSet().pixmap())

            idx = settings.readNumEntry("%scurrentPageIndex" % key)
            if idx > 0 and idx < len(self.tw_):
                self.tw_.setCurrentPage(idx)

            recent_actions = settings.readListEntry("%srecentActions" % key)
            for recent in inverter(recent_actions):
                self.addRecent(self.ag_menu_.child(recent), "QAction")

            mark_actions = settings.readListEntry("%srecentActions" % key)
            for mark in inverter(mark_actions):
                self.addMark(self.ag_menu_.child(mark), "QAction")

    def init(self):

        w = self.w_
        w.statusBar().hide()
        self.main_windgets_ = []
        self.initialized_mods_ = []
        self.act_sig_map_ = QSignalMapper(self.w_, "pinebooActSignalMap")
        # self.act_sig_map_.mapped.connect(self.app_.triggerAction)
        self.act_sig_map_.mapped.connect(self.triggerAction)
        self.initTabWidget()
        self.initHelpMenu()
        self.initConfigMenu()
        self.initTextLabels()
        self.initDocks()
        self.initEventFilter()

    def initFromWidget(self, w):
        self.w_ = w
        self.main_windgets_ = []
        self.initialized_mods_ = []
        self.act_sig_map_ = QSignalMapper(self.w_, "pinebooActSignalMap")
        self.tw_ = w.child("tabWidget", "QTabWidget")
        #self.tw_corner = self.tw_.child("tabWidgetCorner","Qtoolbutton")
        # self.tw_corner.clicked.connect(self.removeCurrentPage)
        self.agMenu_ = w.child("pinebooActionGroup", "QActionGroup")
        self.dck_mod_ = DockListView
        self.dck_mod_.initFromWidget(w.child("pinebooDockModules", "QDockWindow"))
        self.dck_rec_ = DockListView
        self.dck_rec_.initFromWidget(w.child("pinebooDockRecent", "QDockWindow"))
        self.dck_mar_ = DockListView
        self.dck_mar_.initFromWidget(w.child("pinebooDockMark", "QDockWindow"))
        self.initEventFilter()

    def initEventFilter(self):

        w = self.w_
        w.eventFilterFunction = "aqAppScript.mainWindow_.enevtFilter"
        if not sys.isNebulaBuild():
            w.allow_events = [AQS.ContextMenu, AQS.Close]
        else:
            w.allow_events = [AQS.ContextMenu, AQS.Close, AQS.WindowStatechange]

        w.installEventFilter(w)

        self.dck_mod_.w_.installEventFilter(w)
        self.dck_rec_.w_.installEventFilter(w)
        self.dck_mar_.w_.installEventFilter(w)

    def initModule(self, module):
        if module in self.main_windgets_:
            mwi = self.main_windgets_[module]
            mwi.name = module
            aqApp.name = module
            mwi.show()

            if module not in self.initialized_mods_ or self.initialized_mods_[module] is not True:
                self.initialized_mods_[module] = True
                aqApp.call("init", [module])

            mng = aqApp.db().managerModules()
            mng.setActiveIdModule(module)

    def removeCurrentPage(self):
        page = self.tw_.currentPage()
        if not page:
            return

        if page.rtti() == "ForomDB":
            page.close()

    def removeAllPages(self):
        tw = self.tw_

        # if len(tw):
        #    self.tw_corner.hide()

        for page in tw.pages():
            if page.rtti() == "FLFormDB":
                page.close()

    def formClosed(self):
        if len(self.tw_.pages()) == 1 and self.tw_corner:
            self.tw_corner.hide()

    def load(self):
        from pineboolib.utils import filedir
        self.ui_ = pineboolib.project.conn.managerModules().createUI(filedir('plugins/mainform/eneboo/mainform.ui'), None, self)

    @classmethod
    def setDebugLevel(self, q):
        MainForm.debugLevel = q


class DockListView(QtWidgets.QDockWidget):

    w_ = None
    lw_ = None
    ag_ = None

    def __init__(self, parent, name, title):
        if parent is None:
            return

        w = self.w_ = self

        super(DockListView, self).__init__(name, parent, AQS.InDock)

        self.lw_ = QListView(self)
        self.lw_.setObjectName("%sListView" % name)

        """
        this.lw_.addColumn("");
        this.lw_.addColumn("");
        this.lw_.setSorting(-1);
        this.lw_.rootIsDecorated = true;
        this.lw_.setColumnWidthMode(1, 0);
        this.lw_.hideColumn(1);
        this.lw_.header().hide();
        this.lw_.header().setResizeEnabled(false, 1);
        """

        w.setWidget(self.lw_)
        w.setWindowTitle(title)

        """
        w.resizeEnabled = true;
        w.closeMode = true;
        w.setFixedExtentWidth(300);
        """

        self.lw_.doubleClicked.connect(self.activateAction)

    def writeState(self):

        settings = AQSettings
        key = "MainWindow/%s/" % self.objectName()

        settings.writeEntry("%splace" % key, self.place())  # Donde está emplazado
        settings.writeEntry("%svisible" % key, self.isVisible())
        settings.writeEntry("%sx", key, self.x())
        settings.writeEntry("%sy", key, self.y())
        settings.writeEntry("%swidth", key, self.width())
        settings.writeEntry("%sheight", key, self.height())
        #settings.writeEntry("%soffset", key, self.offset())
        area = self.area()
        settings.writeEntry("%sindex", key, area.findDockWindow(self) if area else None)

    def readState(self):

        settings = AQSettings
        key = "MainWindow/%s/" % self.objectName()

        place = setttingsreadNumEntry("%splace" % key, AQS.InDock)
        if place == AQS.OutSideDock:
            self.undock()
            self.move(settings.readNumEntry("%sx" % key, self.x()), settings.readNumEntry("%sy" % key, self.y()))

        self.offset = settings.readNumEntry("%soffset" % key, self.offset)
        index = settings.readNumEntry("%index" % key, None)
        if index is not None:
            area = self.area()
            if area:
                area.moveDockWindow(self, index)

        width = settings.readNumEntry("%width" % key, self.width())
        height = settings.readNumEntry("%height" % key, self.height())
        self.lw_.resize(width, height)
        self.resize(width, height)
        visible = settings.readNumEntry("%visible" % key, True)
        if visible:
            self.show()
        else:
            self.hide()

    def initFromWidget(self, w):
        self.w_ = w
        self.lw_ = w.widget()
        self.lw_.doubleClicked.connect(self.activateAction)

    def activateAction(self, item):
        if item is None:
            return

        actionName = item.text(1)
        if actionName == "":
            return

        ac = self.ag_.findChild("QAction", actionName)
        if ac:
            ac.activate()

    def update(self, actionGroup, reverse):
        self.ag_ = QActionGroup()
        self.lw_.clear()
        if not actionGroup:
            return

        self.buildListView(self.lw_, AQS.toXml(actionGroup), actionGroup, reverse)

    def buildListView(self, parent_item, parent_element, ag, reverse):

        this_item = None
        node = parent_element.lastChild().toElement() if reverse else parent_element.firstChild().toElement()

        while not node.isNull():
            class_name = node.attribute("class")
            if node.tagName() == "object" and class_name.startswith("Action"):
                if node.attribute("visible") == "false":
                    node = node.previousSibling().toElement() if reverse else node.nextSibling().toElement()
                    continue

                if node.attibute("usesDropDown") == "false":
                    self.buildListView(parent_item, node, ag, reverse)
                    node = node.previousSibling().toElement() if reverse else node.nextSibling().toElement()
                    continue

                if not this_item:
                    this_item = QListViewItem(parent_item)
                else:
                    this_item = QListViewItem(parent_item, this_item)

                action_name = node.attribute("name")
                ac = ag.child(action_name)
                if ac is not None:
                    this_item.setPixmap(None, QPixmap(ac.iconSet().pixmap()))
                    if class_name == "Action":
                        this_item.setText(1, actionName)

                this_item.setText(0, node.attribute("menuText").replace("&", ""))
                if node.attribute("enabled") == "false":
                    this_item.setEnabled(False)
                self.buildListView(this_item, node, ag, reverse)

            node = node.previousSibling().toElement() if reverse else node.nextSibling().toElement()


mainWindow = MainForm()
