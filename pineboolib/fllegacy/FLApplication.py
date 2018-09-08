# -*- coding: utf-8 -*-
import logging

from PyQt5 import QtCore, QtWidgets

from pineboolib.fllegacy.FLTranslator import FLTranslator
from pineboolib.fllegacy.FLSettings import FLSettings
from pineboolib import decorators
import pineboolib
from PyQt5.QtWidgets import QWhatsThis

logger = logging.getLogger("FLApplication")


class FLApplication(QtCore.QObject):
    initializing_ = None  # Inicializando
    destroying_ = None  # Cerrandose
    ted_output_ = None
    not_exit_ = None  # No salir de la aplicación
    multi_lang_enabled_ = None  # Activado multiLang
    multi_lang_id_ = None
    translator_ = None  # Traductor
    dict_main_widgets_ = None
    container_ = None  # Contenedor actual??
    map_geometry_form_ = None  # Gemotria de lis mainForm en sdi?
    main_widget_ = None
    p_work_space_ = None
    tool_box_ = None
    toogle_bars_ = None
    project_ = None
    wb_ = None
    form_alone_ = None
    acl_ = None
    popup_warn_ = None
    mng_loader_ = None
    sys_tr_ = None
    fl_factory_ = None
    op_check_update_ = None
    notify_begin_transaction_ = None
    notify_end_transaction_ = None
    notify_roll_back_transaction_ = None
    style = None
    timer_idle_ = None
    init_single_fl_large = None
    show_debug_ = None
    time_user_ = None

    def __init__(self):
        super(FLApplication, self).__init__()
        self.p_work_space_ = None
        self.main_widget_ = None
        self.container_ = None
        self.tool_box_ = None
        self.toogle_bars_ = None
        self.project_ = None
        self.wb_ = None
        self.dict_main_widgets_ = {}
        self.translator_ = []
        self.map_geometry_form_ = []
        self.form_alone_ = False
        self.not_exit_ = False
        self.acl_ = None
        self.popup_warn_ = None
        self.mng_loader_ = None
        self.sys_tr_ = None
        self.initializing_ = False
        self.destroying_ = False
        self.fl_factory_ = None
        self.op_check_update_ = None
        self.notify_begin_transaction_ = False
        self.notify_end_transaction_ = False
        self.notify_roll_back_transaction_ = False

        self.ted_output_ = None
        self.style = None
        self.timer_idle_ = None
        self.init_single_fl_large = False
        self.show_debug_ = True  # FIXME

        self.container_ = None
        # self.fl_factory_ = FLObjectFactory() #FIXME para un futuro
        self.time_user_ = QtCore.QDateTime.currentDateTime()
        self.multi_lang_enabled_ = False
        self.multi_lang_id_ = QtCore.QLocale().name()[:2].upper()

        self.locale_system_ = QtCore.QLocale.system()
        v = 1.1
        self.comma_separator = self.locale_system_.toString(v, 'f', 1)[1]
        self.setObjectName("aqApp")

    def __del__(self):
        self.destroying_ = True
        self.stopTimerIdle()
        self.checkAndFixTransactionLAvel("%s:%s" % (__name__, __class__))
        app_db = self.db()
        if app_db:
            app_db.setInteractiveGUI(False)
            app_db.setQsaExceptions(False)

        if self.dict_main_widgets_:
            for mw in self.dict_main_widgets_:
                del mw
            del self.dict_main_widgets_
            self.dict_main_widgets_ = {}

        self.clearPorject()
        del self.project_
        del self.ted_output_

        if app_db:
            app_db.finish()

        if self.showDebug():
            from pineboolib.fllegacy.FLFieldMetaData import FLFieldMetaData
            from pineboolib.fllegacy.FLTableMetadata import FLTableMetaData
            from pineboolib.fllegacy.FLRelationMetaData import FLRelationMetaData
            from pineboolib.fllegacy.FLSqlCursor import FLSqlCursor
            from pineboolib.fllegacy.FLSqlQuery import FLSqlQuery

            logger.warn("*************************************************")
            logger.warn("FLSqlQuery::count_ref_query")
            logger.warn("*************************************************")
            logger.warn("%d", FLSqlQuery.count_ref_query)
            logger.warn("*************************************************")
            logger.warn("FLSqlQuery::count_ref_query")
            logger.warn("*************************************************")
            logger.warn("FLSqlCursor::count_ref_cursor")
            logger.warn("*************************************************")
            logger.warn("%d", FLSqlCursor.count_ref_cursor)
            logger.warn("*************************************************")
            logger.warn("FLSqlCursor::count_ref_cursor")
            logger.warn("*************************************************")
            logger.warn("FLTableMetaData::count_ %d", FLTableMetaData.count_)
            logger.warn("FLFieldMetaData::count_ %d", FLFieldMetaData.count_)
            logger.warn("FLRelationMetaData::count_ %d", FLRelationMetaData.count_)

        self.aqApp = None

    @decorators.NotImplementedWarn
    def eventFilter(self, obj, ev):
        pass

    @decorators.NotImplementedWarn
    def checkForUpdate(self):
        pass

    @decorators.NotImplementedWarn
    def checkForUpdateFinish(self, op):
        pass

    @decorators.NotImplementedWarn
    def init(self):
        pass

    @decorators.NotImplementedWarn
    def initfcgi(self):
        pass

    @decorators.NotImplementedWarn
    def addObjectFactory(self, new_object_factory):
        pass

    @decorators.NotImplementedWarn
    def callfcgi(self, call_function, argument_list):
        pass

    @decorators.NotImplementedWarn
    def endfcgi(self):
        pass

    @decorators.NotImplementedWarn
    def openQSWorkbench(self):
        pass

    @decorators.NotImplementedWarn
    def initMainWidget(self):
        pass

    @decorators.NotImplementedWarn
    def showMainWidget(self, w):
        pass

    def setMainWidget(self, w):

        if not self.container_:
            return

        if w is self.container_ or not w:
            QApplication.setActiveWindow(w)
            self.main_widget_ = None
            return

        QApplication.setActiveWindow(w)
        self.main_widget_ = w

        mw = self.main_widget_ if isinstance(QtWidgets.QMainWindow, self.main_widget_) else None

        if not mw:
            return

        if self.toogle_bars_:
            tbg = self.container_.findChild(QtWidgets.QActionGroup, "agToggleBars")
            a = tgb.findChild(QtWidgets.QAction, "Herramientas")
            b = tgb.findChild(QtWidgets.QAction, "Estado")
            tb = mw.findChild(QtWidgets.QToolBar, "toolBar")
            if tb:
                a.setOn(tb.isVisible())

            b.setOn(mw.statusBar().isVisible())

    @decorators.NotImplementedWarn
    def makeStyle(self, style_):
        pass

    def chooseFont(self):
        font_ = QtWidgets.QFontDialog().getFont()
        if font_:
            QtWidgets.QApplication.setFont(font_[0])
            save_ = []
            save_.append(font_[0].family())
            save_.append(font_[0].pointSize())
            save_.append(font_[0].weight())
            save_.append(font_[0].italic())

            sett_ = FLSettings()
            sett_.writeEntry("application/font", save_)

    def showStyles(self):
        if not self.style:
            self.initStyles()
        # if self.style:
        #    self.style.exec_()

    @decorators.NotImplementedWarn
    def showToggleBars(self):
        pass

    @decorators.NotImplementedWarn
    def initToolBox(self):
        pass

    @decorators.NotImplementedWarn
    def initActions(self):
        pass

    @decorators.NotImplementedWarn
    def initMenuBar(self):
        pass

    @decorators.NotImplementedWarn
    def initToolBar(self):
        pass

    @decorators.NotImplementedWarn
    def initStatusBar(self):
        pass

    @decorators.NotImplementedWarn
    def initview(self):
        pass

    def setStyle(self, style_):
        if style_:
            sett_ = FLSettings()
            sett_.writeEntry("application/style", style_)
            QtWidgets.QApplication.setStyle(style_)

    def initStyles(self):
        sett_ = FLSettings()
        self.style_mapper = QtCore.QSignalMapper()
        self.style_mapper.mapped[str].connect(self.setStyle)
        style_read = sett_.readEntry("application/style", None)
        if not style_read:
            style_read = "Fusion"

        style_menu = self.mainWidget().findChild(QtWidgets.QMenu, "style")

        if style_menu:
            ag = QtWidgets.QActionGroup(style_menu)
            for style_ in QtWidgets.QStyleFactory.keys():
                action_ = style_menu.addAction(style_)
                action_.setObjectName("style_%s" % style_)
                action_.setCheckable(True)
                if style_ == style_read:
                    action_.setChecked(True)

                action_.triggered.connect(self.style_mapper.map)
                self.style_mapper.setMapping(action_, style_)
                ag.addAction(action_)
            ag.setExclusive(True)

    @decorators.NotImplementedWarn
    def getTabWidgetPages(self, wn, n):
        pass

    @decorators.NotImplementedWarn
    def getWidgetList(self, wn, c):
        pass

    @decorators.NotImplementedWarn
    def toggleToolBar(self, toggle):
        pass

    @decorators.NotImplementedWarn
    def toggleStatusBar(self, toggle):
        pass

    def aboutQt(self):
        QtWidgets.QMessageBox.aboutQt(self.mainWidget())

    def aboutPineboo(self):
        msg = "Texto Acerca de Pineboo"
        QtWidgets.QMessageBox.information(self.mainWidget(), "Pineboo", msg)

    @decorators.NotImplementedWarn
    def statusHelpMsg(self, text):
        pass

    @decorators.NotImplementedWarn
    def windowMenuAboutToShow(self):
        pass

    @decorators.NotImplementedWarn
    def windowMenuActivated(self, id):
        pass

    @decorators.NotImplementedWarn
    def existFormInMDI(self, id):
        pass

    @decorators.NotImplementedWarn
    def openMasterForm(self, n, pix):
        pass

    @decorators.NotImplementedWarn
    def openDefaultForm(self):
        pass

    @decorators.BetaImplementation
    def execMainScript(self, action_name):
        if action_name in pineboolib.project.actions.keys():
            pineboolib.project.actions[action_name].execMainScript(action_name)

    @decorators.NotImplementedWarn
    def execDefaultScript(self):
        pass

    @decorators.NotImplementedWarn
    def windowClose(self):
        pass

    @decorators.NotImplementedWarn
    def loadScriptsFromModule(self, idm):
        pass

    @decorators.NotImplementedWarn
    def activateModule(self, idm=None):  # dos funciones
        pass

    def reinit(self):
        if self.initializing_ or self.destroying_:
            return

        self.stopTimerIdle()
        self.apAppIdle()
        self.initializing_ = True
        self.writeState()
        self.writeStateModule()
        time = QtCore.QTimer()
        time.singleShot(0, self.reinitP)

    @decorators.NotImplementedWarn
    def clearProject(self):
        pass

    def reinitP(self):
        self.db().managerModules().__del__()
        self.db().manager().__del__()
        self.setMainWidget(None)
        self.db().managerModules().setActiveIdModule("")

        if self.dictMainWidgets:
            self.dictMainWidgets = {}

        self.clearProject()

        self.db().manager().init()
        self.db().managerModules().init()
        self.db().managerModules().cleanupMetaData()

        if self.acl_:
            self.ac_.init()

        self.loadScritps()
        self.db().managerModules().setShaFromGlobal()
        self.call("sys.init()", [])
        self.initToolBox()
        self.readState()

        if self.container:
            self.container.installEventFilter(self)
            self.container.setDisable(False)

        self.callScriptEntryFunction()

        self.initializing_ = False
        self.startTimerIdle()

    @decorators.NotImplementedWarn
    def showDocPage(self, url):
        pass

    @decorators.NotImplementedWarn
    def timeUser(self):
        return self.time_user_

    def call(self, function, argument_list=[], object_content=None, show_exceptions=True):
        return pineboolib.project.call(function, argument_list, object_content, show_exceptions)

    def setCaptionMainWidget(self, value):
        self.mainWidget().setWindowTitle("Pineboo v%s - %s" % (pineboolib.project.version, value))
        pass

    @decorators.NotImplementedWarn
    def setNotExit(self, b):
        self.not_exit_ = b

    @decorators.NotImplementedWarn
    def printTextEdit(self, editor_):
        pass

    @decorators.NotImplementedWarn
    def setPrintProgram(self, print_program_):
        pass

    @decorators.NotImplementedWarn
    def addSysCode(self, code, scritp_entry_function):
        pass

    @decorators.NotImplementedWarn
    def setScriptEntryFunction(self, script_enttry_function):
        pass

    @decorators.NotImplementedWarn
    def setDatabaseLockDetection(self, on, msec_lapsus, lim_checks, show_warn, msg_warn, connection_name):
        pass

    @decorators.NotImplementedWarn
    def popupWarn(selfmsg_warn, script_calls=[]):
        pass

    @decorators.NotImplementedWarn
    def checkDatabaseLocks(self, timer_):
        pass

    @decorators.NotImplementedWarn
    def saveGeometryForm(self, name, geo):
        pass

    @decorators.NotImplementedWarn
    def geometryForm(self, name):
        pass

    @decorators.NotImplementedWarn
    def staticLoaderSetup(self):
        pass

    def loadModules(self):
        self.call("sys.loadModules", [], None)

    def exportModules(self):
        self.call("sys.exportModules", [], None)

    def importModules(self):
        self.call("sys.importModules", [], None)

    def updatePineboo(self):
        self.call("sys.uddatePineboo", [], None)

    def dumpDataBase(self):
        self.call("sys.dumpDataBase", [], None)

    def mrProper(self):
        self.db().conn.Mr_Proper()

    def showConsole(self):
        mw = self.mainWidget()
        if mw and not self.ted_output_:
            dw = QtWidgets.QDockWidget("tedOutputDock", mw)
            self.ted_output_ = FLTextEditOutput(dw)
            dw.setWidget(self.ted_output_)
            dw.setWindowTitle(self.tr("Mensajes de Eneboo"))
            mw.addDockWidget(Qt.BottomDockWidgetArea, dw)

    def consoleShown(self):
        return (self.ted_output_ and self.ted_output_.isVisible())

    @decorators.NotImplementedWarn
    def modMainWidget(self, id_modulo):
        pass

    @decorators.NotImplementedWarn
    def evaluateProject(self):
        pass

    @decorators.NotImplementedWarn
    def callScriptEntryFunction(self):
        pass

    @decorators.NotImplementedWarn
    def emitTransactionBegin(self, o):
        if self.notify_begin_transaction_:
            o.transactionBegin.emit()

    @decorators.NotImplementedWarn
    def emitTansactionEnd(self, o):
        if self.notify_end_transaction_:
            o.transactionEnd.emit()

    @decorators.NotImplementedWarn
    def emitTransactionRollBack(self, o):
        if self.notify_roll_back_transaction_:
            o.transsactionRollBack.emit()

    @decorators.NotImplementedWarn
    def gsExecutable(self):
        pass

    @decorators.NotImplementedWarn
    def evalueateProject(self):
        pass

    @decorators.NotImplementedWarn
    def aqAppIdle(self):
        pass

    @decorators.NotImplementedWarn
    def startTimerIdle(self):
        pass

    @decorators.NotImplementedWarn
    def stopTimerIdle(self):
        pass

    @decorators.NotImplementedWarn
    def singleFLLarge(self):
        pass

    @decorators.NotImplementedWarn
    def msgBoxWarning(self, t, _gui):
        pass

    @decorators.NotImplementedWarn
    def checkAndFixTransactionLevel(self, ctx):
        pass

    @decorators.NotImplementedWarn
    def showDebug(self):
        return self.show_debug_

    def db(self):
        return pineboolib.project.conn

    @decorators.NotImplementedWarn
    def classType(self, n):
        return type(resolveObject(n)())

    # def __getattr__(self, name):
    #    return getattr(pineboolib.project, name, None)

    def mainWidget(self):
        return self.main_widget_

    def generalExit(self, ask_exit=True):
        do_exit = True
        if ask_exit:
            do_exit = self.queryExit()
        if do_exit:
            self.destroying_ = True
            if self.ted_output_:
                self.ted_output_.close()

            if not self.form_alone_:
                self.writeState()
                self.writeStateModule()

            if self.db().driverName():
                self.db().managerModules().finish()
                self.db().manager().finish()
                QtCore.QTimer().singleShot(0, self.quit)

    def quit(self):
        pass

    def queryExit(self):
        if self.not_exit_:
            return False

        if not self.db().interactiveGui():
            return True

        ret = QMessageBox.information(self.mainWidget(), self.tr("Salir ..."), self.tr(
            "¿ Quiere salir de la aplicación ?"), QMessageBox.Yes, QMessageBox.No)
        return ret == QMessageBox.Yes

    def writeState(self):

        settings = FLSettings()
        settings.writeEntry("MultiLang/Enabled", self.multi_lang_enabled_)
        settings.writeEntry("MultiLang/LangId", self.multi_lang_id_)

        if self.container_:
            windows_opened = []
            _list = self.topLevelWidgets()

            if self.initializing_:
                for it in _list:
                    it.removeEventFilter(self)
                    if it.onjectName() in self.dict_main_widgets_.keys():
                        if it != self.container_:
                            if it.isVisible():
                                windows_opened.append(it.objectName())
                            it.hide()
                        else:
                            it.setDisabled(True)
            else:
                for it in _list:
                    if it != self.container_ and it.isVisible() and it.objectName() in self.dict_main_widgets_.keys():
                        windows_opened.append(it.objectName())

            settings.writeEntryList("windowsOpened/Main", windows_opened)
            settings.writeEntry("Geometry/MainWindowMaximized", self.container_.isMaximized())
            if not self.container_.isMaximized():
                settings.writeEntry("Geometry/MainWindowX", self.container_.x())
                settings.writeEntry("Geometry/MainWindowY", self.container_.y())
                settings.writeEntry("Geometry/MainWindowWidth", self.container_.width())
                settings.writeEntry("Geometry/MainWindowHeight", self.container_.height())

        for map in self.map_geometry_form_:
            k = "Geometry/%s/" % map.key()
            settings.writeEntry("%s/X" % k, map.x())
            settings.writeEntry("%s/Y" % k, map.y())
            settings.writeEntry("%s/Width" % k, map.width())
            settings.writeEntry("%s/Height" % k, map.height())

    def writeStateModule(self):
        settings = FLSettings()
        idm = self.db().managerModules().activeIdModule()
        if not self.main_widget_ or idm is None or self.main_widget_.objectName() == idm:
            return

        windows_opened = []
        if self.main_widget_ and self.p_work_space_:
            for w in self.p_work_space_.windowList():
                windows_opened.append(w.idMDI())

            settings.writeEntryList("windowsOpened/%s" % idm, windows_opened)
        else:
            settings.writeEntryList("windowsOpened/%s" % idm, windows_opened)

        k = "Geometry/%s" % idm
        settings.writeEntry("%s/Maximized" % k, self.main_widget_.isMaximized())
        settings.writeEntry("%s/X" % k, self.main_widget_.x())
        settings.writeEntry("%s/Y" % k, self.main_widget_.y())
        settings.writeEntry("%s/Width" % k, self.main_widget_.width())
        settings.writeEntry("%s/Height" % k, self.main_widget_.height())

    def readState(self):
        settings = FLSettings()
        self.initializing_ = False
        self.dict_main_widgets_ = {}

        if self.container_:
            r = QtCore.Qrect(self.container_.pos(), self.container_.size())
            self.multi_lang_enabled_ = settings.readBoolEntry("MultiLang/Enabled", False)
            self.multi_lang_id_ = settings.readEntry("MultiLang/LangId", QtCore.QLocale().name()[:2].upper())

            if not settings.readBoolEntry("Geometry/MainWindowMaximized", False):
                r.setX(settings.readNumEntry("Geometry/MainWindowX", r.x()))
                r.setY(settings.readNumEntry("Geometry/MainWindowY", r.y()))
                r.setWidth(settings.readNumEntry("Geometry/MainWindowWidth", r.width()))
                r.setHeight(settings.readNumEntry("Geometry/MainWindowHeight", r.height()))

                desk = QtWidgets.QApplication.desktop().availableGeometry(self.container_)
                inter = desk.intersect(r)
                self.container_.resize(r.size())
                if inter.width() * inter.height() > (r.width() * r.height() / 20):
                    self.container_.move(r.topLeft())

            else:
                self.container_.resize(QtWidgets.QApplication.desktop().availableGeometry(self.container_).size())

            active_id_module = self.db().managerModules().activeIdModule()

            windows_opened = settings.readListEntry("windowsOpened/Main")
            if windows_opened:

                for it in windows_opened:
                    if it in self.db().managerModules().listAllIdModules():
                        w = None
                        if it in self.dict_main_widgets_.keys():
                            w = self.dict_main_widgets_[it]
                        if not w:
                            act = self.container_.findChild(QtWidgets.QAction, it)
                            if not act or not act.isVisible():
                                continue

                            w = self.db().managerModules().createUI("%s.ui" % it, self, None, it)
                            self.dict_main_widgets_[it] = w
                            self.setName(it)
                            if self.acl_:
                                self.acl_.process(w)

                            self.setMainWidget(w)
                            self.call("%s.init()" % it, [])
                            self.db().managerModules().setActiveIdModule(it)
                            self.setMainWidget(w)
                            self.initMainWidget()

            itd = self.dict_main_widgets_
            for w in itd:
                if w.objectName() is not active_id_module:
                    w.installEventFilter(self)
                    w.show()
                    w.setFont(self.font())
                    if not isinstance(w, QtWidgets.QMainWindow):
                        continue

                    view_back = w.centralWidget()
                    if view_back:
                        self.p_work_space_ = view_back.findChild(QtWidgets.QWidget, w.objectName())

            if active_id_module:
                self.container_.show()
                self.container_.setFont(self.font())

            self.activateModule(active_id_module)

    @decorators.BetaImplementation
    def loadScripts(self):

        self.setOverrideCursor(QtCore.Qt.WaitCursor)
        list_modules = self.mngLoader_.listAllIdModules()
        for it in list_modules:
            self.loadScriptFormModule(it)

        self.restoreOverrideCursor()

    def urlPineboo(self):
        self.call("sys.openUrl", ["http://eneboo.org/"])

    def helpIndex(self):
        self.call("sys.openUrl", ["http://manuales-eneboo-pineboo.org/"])

    def tr(self, text):
        return QtWidgets.QApplication.translate("system", text, _1)

        """
    Instala las traducciones cargadas
    """
    @decorators.BetaImplementation
    def loadTranslations(self):
        translatorsCopy = None
        # if self.translators:
        #     translatorsCopy = copy.copy(self.translators)
        #     for it in translatorsCopy:
        #         self.removeTranslator(it)

        lang = QtCore.QLocale().name()[:2]
        for module in self.modules().keys():
            self.loadTranslationFromModule(module, lang)

        if translatorsCopy:
            for it in translatorsCopy:
                item = it
                if item.sysTrans_:
                    self.installTranslator(item)
                else:
                    item.deletelater()

    """
    Busca la traducción de un texto a un Idioma dado
    @param s, Cadena de texto
    @param l, Idioma.
    @return Cadena de texto traducida. 
    """
    @decorators.BetaImplementation
    def trMulti(self, s, l):
        backMultiEnabled = self.multi_lang_enabled_
        ret = self.translate("%s_MULTILANG" % l.upper(), s)
        self.multi_lang_enabled_ = backMultiEnabled
        return ret

    """
    Cambia el estado de la opción MultiLang
    @param enable, Boolean con el nuevo estado
    @param langid, Identificador del leguaje a activar
    """
    @decorators.BetaImplementation
    def setMultiLang(self, enable, langid):
        self.multi_lang_enabled_ = enable
        if enable and langid:
            self.multi_lang_id_ = langid.upper()

    """
    Carga una traducción desde un módulo dado
    @param idM, Identificador del módulo donde buscar
    @param lang, Lenguaje a buscar
    """
    @decorators.BetaImplementation
    def loadTranslationFromModule(self, idM, lang):
        self.installTranslator(self.createModTranslator(idM, lang, True))
        # self.installTranslator(self.createModTranslator(idM, "mutliLang"))

    """
    Instala una traducción para la aplicación
    @param tor, Objeto con la traducción a cargar
    """
    @decorators.BetaImplementation
    def installTranslator(self, tor):
        if not tor:
            return
        else:
            QtWidgets.qApp.installTranslator(tor)
            self.translator_.append(tor)

    """
    Crea una traducción para sys
    @param lang, Idioma a usar
    @param loadDefault, Boolean para cargar los datos por defecto
    @return objeto traducción
    """
    @decorators.NotImplementedWarn
    def createSysTranslator(self, lang, loadDefault):
        pass

    """
    Crea una traducción para un módulo especificado
    @param idM, Identificador del módulo
    @param lang, Idioma a usar
    @param loadDefault, Boolean para cargar los datos por defecto
    @return objeto traducción
    """
    @decorators.BetaImplementation
    def createModTranslator(self, idM, lang, loadDefault=False):
        fileTs = "%s.%s.ts" % (idM, lang)
        key = self.db().managerModules().shaOfFile(fileTs)

        if key is not None or idM == "sys":
            tor = FLTranslator(self, "%s_%s" % (idM, lang), lang == "multilang")

            if tor.loadTsContent(key):
                return tor

        return self.createModTranslator(idM, "es") if loadDefault else None

    def modules(self):
        return pineboolib.project.modules


class FLWorkSpace(QtWidgets.QWidget):

    logo = None
    f_color = None
    p_color = None

    @decorators.NotImplementedWarn
    def __init__(self, parent, name):
        super(FLWorkSpace, self).__init_(parent)
        self.setObjectName(name)

    @decorators.NotImplementedWarn
    def init(self):
        from pineboolib.fllegacy.aqsobject.AQS import AQS
        self.logo = AQS.Pixmap_fromMineSource("pineboo.png")
        self.f_color.setRgb(self.AQ_RGB_LOGO)
        self.p_color.setRGB(164, 170, 180)

    @decorators.NotImplementedWarn
    def paintEvent(self, pe):
        super(FLWorkSpace, self.paintEvent(pe))


class FLWidget(QtWidgets.QWidget):

    logo = None
    f_color = None
    p_color = None

    @decorators.NotImplementedWarn
    def __init__(self, parent, name):
        super(FLWidget, self).__init_(parent)
        self.setObjectName(name)

    @decorators.NotImplementedWarn
    def init(self):
        from pineboolib.fllegacy.aqsobject.AQS import AQS
        self.logo = AQS.Pixmap_fromMineSource("pineboo.png")
        self.f_color.setRgb(self.AQ_RGB_LOGO)
        self.p_color.setRGB(164, 170, 180)

    @decorators.NotImplementedWarn
    def paintEvent(self, pe):
        super(FLWidget, self.paintEvent(pe))


class FLPopuWarn(QtWidgets.QWhatsThis):

    script_calls_ = {}

    def __init__(self, parent):
        self.script_calls_ = {}
        super(FLPopuWarn, self).__init__(parent)

    def clicked(self, href):
        if href:

            from pineboolib.pncontrols import aqApp

            if href.find(":") > -1:
                h = href.split(":")[1]
            if h.find(".") == 1:
                aqApp.call(h.split(".")[1], self.script_calls_[href], h.split(".")[0])
            else:
                aqApp.call(h, self.script_calls_[href], None)
