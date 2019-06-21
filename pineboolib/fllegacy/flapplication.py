# -*- coding: utf-8 -*-
import logging

from PyQt5 import QtCore, QtWidgets

from pineboolib.fllegacy.fltranslator import FLTranslator
from pineboolib.fllegacy.flsettings import FLSettings
from pineboolib import decorators
import pineboolib

from PyQt5.QtCore import QTimer, pyqtSignal, QPoint, QEvent, QRect, QObject



logger = logging.getLogger("FLApplication")


class FLApplication(QtCore.QObject):
    initializing_ = None  # Inicializando
    destroying_ = None  # Cerrandose
    ted_output_ = None
    not_exit_ = None  # No salir de la aplicación
    multi_lang_enabled_ = None  # Activado multiLang
    multi_lang_id_ = None
    translator_ = []  # Traductor
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
    script_entry_function_ = None
    event_loop = None
    window_menu = None
    last_text_caption_ = None

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
        self.popup_warn_ = None
        self.window_menu = None

        self.ted_output_ = None
        self.style = None
        self.timer_idle_ = None
        self.init_single_fl_large = False
        self.show_debug_ = True  # FIXME
        self.script_entry_function_ = None
        self.last_text_caption_ = None

        # self.fl_factory_ = FLObjectFactory() #FIXME para un futuro
        self.time_user_ = QtCore.QDateTime.currentDateTime()
        self.multi_lang_enabled_ = False
        self.multi_lang_id_ = QtCore.QLocale().name()[:2].upper()

        self.locale_system_ = QtCore.QLocale.system()
        v = 1.1
        self.comma_separator = self.locale_system_.toString(v, 'f', 1)[1]
        self.setObjectName("aqApp")
        self.event_loop = QtCore.QEventLoop()

    def __del__(self):
        self.destroying_ = True
        self.stopTimerIdle()
        #self.checkAndFixTransactionLAvel("%s:%s" % (__name__, __class__))
        app_db = self.db()
        if app_db:
            app_db.setInteractiveGUI(False)
            app_db.setQsaExceptions(False)

        if self.dict_main_widgets_:
            for mw in self.dict_main_widgets_:

                del mw
            del self.dict_main_widgets_
            self.dict_main_widgets_ = {}

        self.clearProject()
        self.project_ = None
        self.ted_output_ = None

        if app_db:
            app_db.finish()
        """
        if self.showDebug():
            from pineboolib.fllegacy.FLFieldMetaData import FLFieldMetaData
            from pineboolib.fllegacy.FLTableMetadata import FLTableMetaData
            from pineboolib.fllegacy.FLRelationMetaData import FLRelationMetaData
            from pineboolib.fllegacy.FLSqlCursor import FLSqlCursor
            from pineboolib.fllegacy.FLSqlQuery import FLSqlQuery

            logger.warning("*************************************************")
            logger.warning("FLSqlQuery::count_ref_query")
            logger.warning("*************************************************")
            logger.warning("%d", FLSqlQuery.count_ref_query)
            logger.warning("*************************************************")
            logger.warning("FLSqlQuery::count_ref_query")
            logger.warning("*************************************************")
            logger.warning("FLSqlCursor::count_ref_cursor")
            logger.warning("*************************************************")
            logger.warning("%d", FLSqlCursor.count_ref_cursor)
            logger.warning("*************************************************")
            logger.warning("FLSqlCursor::count_ref_cursor")
            logger.warning("*************************************************")
            logger.warning("FLTableMetaData::count_ %d", FLTableMetaData.count_)
            logger.warning("FLFieldMetaData::count_ %d", FLFieldMetaData.count_)
            logger.warning("FLRelationMetaData::count_ %d", FLRelationMetaData.count_)
        """
        self.aqApp = None


    def eventFilter(self, obj, ev):
        from pineboolib.pncontrolsfactory import QApplication, QMainWindow
        
        
        if self.initializing_ or self.destroying_:
            return super().eventFilter(obj, ev)
        
        if QApplication.activeModalWidget() or QApplication.activePopupWidget():
            return super().eventFilter(obj, ev)
        
        evt = ev.type()
        if obj != self.main_widget_ and not isinstance(obj, QMainWindow):
            return super().eventFilter(obj, ev)
        
        aw = None
        #if self.p_work_space_ is not None:
        #    aw = QApplication.setActiveWindow(self.p_work_space_)
        if aw is not None and aw != obj and evt not in (QEvent.Resize, QEvent.Close):
            obj.removeEventFilter(self)
            if evt == QEvent.WindowActivate:
                if obj == self.container_:
                    self.activateModule(None)
                else:
                    self.activateModule(obj.objectName())
            
            
            if self.p_work_space_ and self.notify(self.p_work_space_, ev):
                obj.installEventFilter(self)
                return True
            
            obj.installEventFilter(self)
        
        if evt == QEvent.KeyPress:
            if obj == self.container_:
                ke = ev
            
            elif obj == self.main_widget_:
                ke = ev
                if ke.key() == QtCore.Qt.Key_Shift and (ke.state() == QtCore.Qt.Key_Control):
                    self.activateModule(None)
                    return True
                if ke.key() == QtCore.Qt.Key_Q and (ke.state() == QtCore.Qt.Key_Control):
                    self.generalExit()
                    return True
                if ke.key() == QtCore.Qt.Key_W and (ke.state() in  (QtCore.Qt.Key_Control, QtCore.Qt.Key_Alt)):
                    print("????")
                    return True
                if ke.key() == QtCore.Qt.Key_Escape:
                    obj.hide()
                    return True
        
        elif evt == QEvent.Close:
            if obj == self.container_:
                ret = self.generalExit()
                if ret == False:
                    obj.setDisabled(False)
                    ev.ignore()
                return True
            else:
                obj.hide()
                return True
        elif evt == QEvent.WindowActivate:
            if obj == self.container_:
                self.activateModule(None)
                return True
            else:
                self.activateModule(obj.objectName())
                return True
        
        elif evt == QEvent.MouseButtonPress:
            if self.modules_menu:
                me = ev
                if me.button() == QtCore.Qt.RightButton:
                    self.modules_menu.popup(QCursor.pos())
                    return True
                else:
                    return False
            else:
                return False
        
        
        return super().eventFilter(obj, ev)
        
            
            
            
    
    def eventLoop(self):
        from pineboolib.pncontrolsfactory import QEventLoop
        return QEventLoop()
        

    @decorators.NotImplementedWarn
    def checkForUpdate(self):
        pass

    @decorators.NotImplementedWarn
    def checkForUpdateFinish(self, op):
        pass


    def init(self):
        from pineboolib.pncontrolsfactory import AQS, QWidget, QVBoxLayout, QPushButton, QKeySequence, QMenu, QAction, QSizePolicy, QToolBox, QIcon
        from pineboolib.fllegacy.flaccesscontrollists import FLAccessControlLists
        self.dict_main_widgets_ = {}
        self.container_.setObjectName("container")
        self.container_.setWindowIcon(QIcon(AQS.Pixmap_fromMineSource("pineboo.png")))
        if self.db() is not None:
            self.container_.setWindowTitle(self.db().database())
        else:
            self.container_.setWindowTitle("Eneboo %s" % pineboolib.project.version)
        
        #FLDiskCache.init(self)
        
        self.window_menu = QMenu(self.container_)
        self.window_menu.setObjectName("windowMenu")
        
    
        
        self.window_cascade_action = QAction(QIcon(AQS.Pixmap_fromMineSource("cascada.png")), self.tr("Cascada"), self.container_)
        self.window_menu.addAction(self.window_cascade_action)
        
        
        self.window_tile_action = QAction(QIcon(AQS.Pixmap_fromMineSource("mosaico.png")), self.tr("Mosaico"), self.container_)
        self.window_menu.addAction(self.window_tile_action)
        
        self.window_close_action = QAction(QIcon(AQS.Pixmap_fromMineSource("cerrar.png")), self.tr("Cerrar"), self.container_)
        self.window_menu.addAction(self.window_close_action)
        
        self.modules_menu = QMenu(self.container_)
        self.modules_menu.setObjectName("modulesMenu")
        #self.modules_menu.setCheckable(False)

        w = QWidget(self.container_)
        w.setObjectName("widgetContainer")
        vl = QVBoxLayout(w)
        
        self.exit_button = QPushButton(QIcon(AQS.Pixmap_fromMineSource("exit.png")), self.tr("Salir"), w)
        self.exit_button.setObjectName("pbSalir")
        self.exit_button.setShortcut(QKeySequence(self.tr("Ctrl+Q")))
        self.exit_button.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))
        self.exit_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.exit_button.setToolTip(self.tr("Salir de la aplicación (Ctrl+Q)"))
        self.exit_button.setWhatsThis(self.tr("Salir de la aplicación (Ctrl+Q)"))
        self.exit_button.clicked.connect(self.container_.close)
        
        self.tool_box_ = QToolBox(w)
        self.tool_box_.setObjectName("toolBox")
        
        vl.addWidget(self.exit_button)
        vl.addWidget(self.tool_box_)
        self.container_.setCentralWidget(w)
    
        
        self.db().manager().init()
        #self.mng_loader_.init()
        
        self.initStyles()
        self.initMenuBar()
        

        self.db().manager().loadTables()
        #self.mng_loader_.loadKeyFiles()
        #self.mng_loader_.loadAllIdModules()
        #self.mng_loader_.loadIdAreas()
        self.db().managerModules().loadKeyFiles()
        self.db().managerModules().loadAllIdModules()
        self.db().managerModules().loadIdAreas()
        
        self.acl_ = FLAccessControlLists()
        #self.acl_.init()
        
        #self.loadScripts()
        #self.mng_loader_.setShaLocalFromGlobal()
        self.db().managerModules().setShaLocalFromGlobal()
        self.loadTranslations()
        
        self.call("sys.init", [])
        self.initToolBox()
        self.readState()
        
        self.container_.installEventFilter(self)
        self.startTimerIdle()

        

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
    
    def localeSystem(self):
        return self.locale_system_

    @decorators.NotImplementedWarn
    def openQSWorkbench(self):
        pass

    def initMainWidget(self):
        if not self.main_widget_ or not self.container_:
            return
        
        if self.main_widget_:
            ac = self.main_widget_.menuBar().addMenu(self.window_menu)
            ac.setText(self.tr("&Ventana"))
            self.main_widget_.setCentralWidget(None)
        
        self.initView()
        self.initActions()
        self.initToolBar()
        self.initStatusBar()
        
        self.readStateModule()
        


    def showMainWidget(self, w):
        
        from pineboolib.pncontrolsfactory import QApplication, QMainWindow, QToolBar, QIcon, FLWorkSpace
        
        if not self.container_:
            if w:
                w.show()
            return
        
        
        focus_w = QApplication.focusWidget()
        if w is self.container_ or not w:
            if self.container_.isMinimized():
                self.container_.showNormal()
            elif not self.container_.isVisible():
                self.container_.setFont(self.font())
                self.container_.show()
            
            if focus_w and isinstance(focus_w, QMainWindow) and focus_w != self.container_:
                self.container_.setFocus()
            
            if not self.container_.isActiveWindow():
                self.container_.raise_()
                QApplication.setActiveWindow(self.container_)
            
            if self.db() is not None:
                self.container_.setWindowTitle(self.db().database())
            else:
                self.container_.setWindowTitle("Eneboo %s" % pineboolib.project.version)
            
            return
        
        if w.isMinimized():
            w.showNormal()
        elif not w.isVisible():
            w.show()
            w.setFont(QApplication.font())
        
        if focus_w and isinstance(focus_w, QMainWindow) and focus_w != w:
            w.setFocus()
        if not w.isActiveWindow():
            w.raise_()
            QApplication.setActiveWindow(w)
        
        if w:
            view_back = w.centralWidget()
            if view_back:
                self.p_work_space_ = view_back.findChild(FLWorkSpace, w.objectName())
                view_back.show()
        
        self.setCaptionMainWidget(None)
        descript_area = self.db().managerModules().idAreaToDescription(self.db().managerModules().activeIdArea())
        w.setWindowIcon(QIcon(self.db().managerModules().iconModule(w.objectName())))
        self.tool_box_.setCurrentIndex(self.tool_box_.indexOf(self.tool_box_.findChild(QToolBar, descript_area)))
        
            

    def setMainWidget(self, w):
        if not self.container_:
            return

        from pineboolib.pncontrolsfactory import QApplication, QMainWindow, QAction, QActionGroup, QToolBar, QWidget
        if w == self.container_ or not w:
            QApplication.setActiveWindow(self.container_)
            self.main_widget_ = None
            return

        QApplication.setActiveWindow(w)
        self.main_widget_ = w

        #mw = self.main_widget_ if isinstance(self.main_widget_, QMainWindow) else None
        mw = self.main_widget_
        if not mw:
            return

        if self.toogle_bars_:
            tool_bar = self.main_widget_.findChild(QToolBar)
            for ac in self.toogle_bars_.actions():
                if ac.objectName() == "Herramientas":
                    a = ac
                elif ac.objectName() == "Estado":
                    b = ac

            if tool_bar:
                a.setChecked(tool_bar.isVisible())

            b.setChecked(mw.statusBar().isVisible())

    @decorators.NotImplementedWarn
    def makeStyle(self, style_):
        pass

    def chooseFont(self):
        from pineboolib.pncontrolsfactory import QFontDialog, QApplication
        
        font_ = QFontDialog().getFont()
        if font_:
            QApplication.setFont(font_[0])
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

    def initToolBox(self):
        from pineboolib.pncontrolsfactory import QToolBox, QMenu, QToolBar, QActionGroup, QAction, QIcon, AQS, QSize
        from PyQt5.QtWidgets import QToolButton
        
        
        
        self.tool_box_ = self.main_widget_.findChild(QToolBox, "toolBox")
        self.modules_menu = self.main_widget_.findChild(QMenu, "modulesMenu")
        
        if self.tool_box_ is None or self.modules_menu is None:
            return
        
        self.modules_menu.clear()
        for item in range(self.tool_box_.count()):
            if isinstance(item, QToolBar):
                item.clear()
            
            self.tool_box_.removeItem(item)
            del item
        
        c = 65
        
        for it in self.db().managerModules().listIdAreas():
            descript_area = self.db().managerModules().idAreaToDescription(it)
            new_area_bar = QToolBar(self.tr(descript_area), self.container_)
            new_area_bar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
            #new_area_bar.setFrameStyle(QFrame.NoFrame)
            new_area_bar.setOrientation(QtCore.Qt.Vertical)
            new_area_bar.layout().setSpacing(3)
            self.tool_box_.addItem(new_area_bar, self.tr(descript_area))
            ag = QActionGroup(new_area_bar)
            ag.setObjectName(descript_area)
            #ac = QAction(ag)
            #ac.setText(descript_area)
            #ac.setUsesDropDown(True)
            
            list_modules = self.db().managerModules().listIdModules(it)
            list_modules.sort()
            
            for mod in list_modules:
                if str(chr(c)) == "Q":
                    c += 1
                    continue
                
                if mod == "sys":
                    if FLSettings().readBoolEntry("application/isDebuggerMode"):
                        
                        descript_module = "%s: %s" % (str(chr(c)), self.tr("Carga Estática desde Disco Duro"))
                        new_module_action = QAction(new_area_bar)
                        new_module_action.setObjectName("StaticLoadAction")
                        new_module_action.setText(self.tr(descript_module))
                        new_module_action.setShortcut(getattr(QtCore.Qt, "Key_%s" % str(chr(c))))
                        new_module_action.setIcon(QIcon(AQS.Pixmap_fromMineSource("folder_update.png")))
                        new_area_bar.addAction(new_module_action)
                        new_module_action.triggered.connect(self.staticLoaderSetup)
                        ag.addAction(new_module_action)
                        c += 1
                        
                        descript_module = "%s: %s" % (str(chr(c)), self.tr("Reiniciar Script"))
                        new_module_action = QAction(new_area_bar)
                        new_module_action.setObjectName("reinitScriptAction")
                        new_module_action.setText(self.tr(descript_module))
                        new_module_action.setShortcut(getattr(QtCore.Qt, "Key_%s" % str(chr(c))))
                        new_module_action.setIcon(QIcon(AQS.Pixmap_fromMineSource("reload.png")))
                        new_area_bar.addAction(new_module_action)
                        new_module_action.triggered.connect(self.reinit)
                        ag.addAction(new_module_action)
                        c += 1
                    
                        descript_module = "%s: %s" % (str(chr(c)), self.tr("Mostrar Consola de mensajes"))
                        new_module_action = QAction(new_area_bar)
                        new_module_action.setObjectName("shConsoleAction")
                        new_module_action.setText(self.tr(descript_module))
                        new_module_action.setShortcut(getattr(QtCore.Qt, "Key_%s" % str(chr(c))))
                        new_module_action.setIcon(QIcon(AQS.Pixmap_fromMineSource("consola.png")))
                        new_area_bar.addAction(new_module_action)
                        new_module_action.triggered.connect(self.showConsole)
                        ag.addAction(new_module_action)
                        c += 1
                
                descript_module = "%s: %s" % (str(chr(c)), self.db().managerModules().idModuleToDescription(mod))
                new_module_action = QAction(new_area_bar)
                new_module_action.setObjectName(mod)
                new_module_action.setText(self.tr(descript_module))
                new_module_action.setShortcut(getattr(QtCore.Qt, "Key_%s" % str(chr(c))))
                new_module_action.setIcon(QIcon(self.db().managerModules().iconModule(mod)))
                new_area_bar.addAction(new_module_action)
                new_module_action.triggered.connect(self.activateModule)
                ag.addAction(new_module_action)
                c += 1
            
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
            
            lay = new_area_bar.layout()
            for child in new_area_bar.children():
                if isinstance(child, QToolButton):
                    child.setMinimumWidth(self.container_.width())
                    lay.setAlignment(child, QtCore.Qt.AlignCenter)

            
            
            
            a_menu = self.modules_menu.addMenu(descript_area)
            for a in ag.actions():
                a_menu.addAction(a)
            
        descript_area = "Configuración"
        config_tool_bar = QToolBar(self.tr(descript_area), self.container_)
        config_tool_bar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        #config_tool_bar.setFrameStyle(QFrame.NoFrame)
        config_tool_bar.setOrientation(QtCore.Qt.Vertical)
        #config_tool_bar.layout().setSpacing(3)
        self.tool_box_.addItem(config_tool_bar, self.tr(descript_area))
        
        descript_module = self.tr("Fuente")
        font_action = QAction(new_area_bar)
        font_action.setObjectName("fontAction")
        font_action.setText(self.tr(descript_module))
        #font_action.setShortcut(getattr(QtCore.Qt, "Key_%s" % str(chr(c))))
        font_action.setIcon(QIcon(AQS.Pixmap_fromMineSource("font.png")))
        config_tool_bar.addAction(font_action)
        font_action.triggered.connect(self.chooseFont)
        ag.addAction(font_action)
        
        
        
        descript_module = self.tr("Estilo")
        style_action = QAction(new_area_bar)
        style_action.setObjectName("styleAction")
        style_action.setText(self.tr(descript_module))
        #style_action.setShortcut(getattr(QtCore.Qt, "Key_%s" % str(chr(c))))
        style_action.setIcon(QIcon(AQS.Pixmap_fromMineSource("estilo.png")))
        config_tool_bar.addAction(style_action)
        style_action.triggered.connect(self.showStyles)
        ag.addAction(style_action)
        
        descript_module = self.tr("Indice")
        help_action = QAction(new_area_bar)
        help_action.setObjectName("helpAction")
        help_action.setText(self.tr(descript_module))
        #help_action.setShortcut(getattr(QtCore.Qt, "Key_%s" % str(chr(c))))
        help_action.setIcon(QIcon(AQS.Pixmap_fromMineSource("help_index.png")))
        config_tool_bar.addAction(help_action)
        help_action.triggered.connect(self.helpIndex)
        ag.addAction(help_action)
        
        descript_module = self.tr("Acerca de Pineboo")
        about_pineboo_action = QAction(new_area_bar)
        about_pineboo_action.setObjectName("aboutPinebooAction")
        about_pineboo_action.setText(self.tr(descript_module))
        #help_action.setShortcut(getattr(QtCore.Qt, "Key_%s" % str(chr(c))))
        about_pineboo_action.setIcon(QIcon(AQS.Pixmap_fromMineSource("about.png")))
        config_tool_bar.addAction(about_pineboo_action)
        about_pineboo_action.triggered.connect(self.aboutPineboo)
        ag.addAction(about_pineboo_action)
        
        descript_module = self.tr("Visita Eneboo.org")
        visit_pineboo_action = QAction(new_area_bar)
        visit_pineboo_action.setObjectName("visitPinebooAction")
        visit_pineboo_action.setText(self.tr(descript_module))
        #help_action.setShortcut(getattr(QtCore.Qt, "Key_%s" % str(chr(c))))
        visit_pineboo_action.setIcon(QIcon(AQS.Pixmap_fromMineSource("about.png")))
        config_tool_bar.addAction(visit_pineboo_action)
        visit_pineboo_action.triggered.connect(self.urlPineboo)
        ag.addAction(visit_pineboo_action)
        
        descript_module = self.tr("Acerca de Qt")
        about_qt_action = QAction(new_area_bar)
        about_qt_action.setObjectName("aboutQtAction")
        about_qt_action.setText(self.tr(descript_module))
        #help_action.setShortcut(getattr(QtCore.Qt, "Key_%s" % str(chr(c))))
        about_qt_action.setIcon(QIcon(AQS.Pixmap_fromMineSource("aboutqt.png")))
        config_tool_bar.addAction(about_qt_action)
        about_qt_action.triggered.connect(self.aboutQt)
        ag.addAction(about_qt_action)
        
        lay = config_tool_bar.layout()
        for child in config_tool_bar.children():
            if isinstance(child, QToolButton):
                    child.setMinimumWidth(self.container_.width())
                    lay.setAlignment(child, QtCore.Qt.AlignCenter)
        
        
            
        if self.acl_:
            self.acl_.process(self.container_)        
            
    
    def workspace(self):
        return self.p_work_space_
        


    def initActions(self):
        if self.main_widget_ is not None and self.p_work_space_ is not None:
            self.window_cascade_action.triggered.connect(self.p_work_space_.cascadeSubWindows)
            self.window_tile_action.triggered.connect(self.p_work_space_.tileSubWindows)
            self.window_close_action.triggered.connect(self.p_work_space_.closeActiveSubWindow)

    def initMenuBar(self):
        self.window_menu.aboutToShow.connect(self.windowMenuAboutToShow)

    def initToolBar(self):
        from pineboolib.pncontrolsfactory import QMenu, QAction
        
        mw = self.main_widget_
        if mw is None:
            return
        
        tb = mw.menuBar()
        if tb is None:
            print("*** No se encuentra toolbar en", mw.objectName())
            return
        
        #tb.setMovingEnabled(False)
        
        tb.addSeparator()
        #what_this_button = QWhatsThis(tb)
        
        if not self.toogle_bars_:
            self.toogle_bars_ = QMenu(self.container_)
            self.toogle_bars_.setObjectName("toggleBars")
            #self.toogle_bars_.setCheckable(True)
            
            
            #ag = QActionGroup(self.container_)
            #ag.setObjectName("agToggleBars")
            
            a = QAction(self.tr("Barra de Herramientas"), self.container_)
            a.setObjectName("Herramientas")
            a.setCheckable(True)
            a.setChecked(True)
            a.triggered.connect(self.toggleToolBar)
            self.toogle_bars_.addAction(a)
            
            b = QAction(self.tr("Barra de Estado"), self.container_)
            b.setObjectName("Estado")
            b.setCheckable(True)
            b.setChecked(True)
            b.triggered.connect(self.toggleStatusBar) 
            self.toogle_bars_.addAction(b)
            
            mw.menuBar().addMenu(self.toogle_bars_)
        
        
            
        
            
        ac = mw.menuBar().addMenu(self.toogle_bars_)
        ac.setText(self.tr("&Ver"))
        
        
        ac = mw.menuBar().addMenu(self.modules_menu)
        ac.setText(self.tr("&Módulos"))
        
        


    def initStatusBar(self):
        if not self.main_widget_:
            return
        
        from pineboolib.pncontrolsfactory import QLabel 
        
        self.statusHelpMsg(self.tr("Listo."))
        self.main_widget_.statusBar().setSizeGripEnabled(False)
        
        conexion = QLabel(self.main_widget_.statusBar())
        conexion.setText("%s@%s" % (self.db().user(), self.db().database()))
        self.main_widget_.statusBar().addWidget(conexion)


    def initView(self):
        mw = self.main_widget_
        
        if mw is None:
            return
        
        view_back = mw.centralWidget()
        if view_back is None:
            from pineboolib.pncontrolsfactory import QMdiArea, FLWorkSpace
            view_back = QMdiArea()
            view_back.setObjectName("mdi_area")
            self.p_work_space_ = FLWorkSpace(view_back, self.db().managerModules().activeIdModule())
            self.p_work_space_.setAttribute(QtCore.Qt.WA_NoSystemBackground)
            #p_work_space.setScrollBarsEnabled(True)
            #FIXME: setScrollBarsEnabled
            mw.setCentralWidget(view_back)
        

    def setStyle(self, style_):
        if style_:
            sett_ = FLSettings()
            sett_.writeEntry("application/style", style_)
            from pineboolib.pncontrolsfactory import QApplication
            QApplication.setStyle(style_)

    def initStyles(self):
        sett_ = FLSettings()
        self.style_mapper = QtCore.QSignalMapper()
        self.style_mapper.mapped[str].connect(self.setStyle)
        style_read = sett_.readEntry("application/style", None)
        if not style_read:
            style_read = "Fusion"
        
        from pineboolib.pncontrolsfactory import QMenu, QActionGroup, QStyleFactory
        style_menu = self.mainWidget().findChild(QMenu, "style")

        if style_menu:
            ag = QActionGroup(style_menu)
            for style_ in QStyleFactory.keys():
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


    def toggleToolBar(self, toggle):
        if not self.main_widget_:
            return
        
        from pineboolib.pncontrolsfactory import QToolBar
        
        tb = self.main_widget_.findChild(QToolBar)
        if not tb:
            return
        
        tb.show() if toggle else tb.hide()


    def toggleStatusBar(self, toggle):
        if not self.main_widget_:
            return
        
        self.main_widget_.statusBar().show() if toggle else self.main_widget_.statusBar().hide()

        

    def aboutQt(self):
        from pineboolib.pncontrolsfactory import QMessageBox
        QMessageBox.aboutQt(self.mainWidget())

    def aboutPineboo(self):
        if pineboolib.project._DGI.localDesktop():
            from pineboolib.dlgabout.about_pineboo import about_pineboo
            about_dlg = about_pineboo()
        
    def statusHelpMsg(self, text):
        if FLSettings().readBoolEntry("application/isDebuggerMode"):
            logger.warning("StatusHelpMsg: %s", text)
        
        if not self.main_widget_:
            return
        
        self.main_widget_.statusBar().showMessage(text, 2000)


    def windowMenuAboutToShow(self):
        if not self.p_work_space_:
            return
        
        self.window_menu.clear()
        self.window_menu.addAction(self.window_cascade_action)
        self.window_menu.addAction(self.window_tile_action)
        self.window_menu.addAction(self.window_close_action)
        
        if not self.p_work_space_.subWindowList():
            self.window_cascade_action.setEnabled(False)
            self.window_tile_action.setEnabled(False)
            self.window_close_action.setEnabled(False)
        else:
            self.window_cascade_action.setEnabled(True)
            self.window_tile_action.setEnabled(True)
            self.window_close_action.setEnabled(True)
            self.window_menu.addSeparator()
        
        for window in self.p_work_space_.subWindowList():
            ac = self.window_menu.addAction(window.windowTitle())
            ac.setCheckable(True)
            
            if window == self.p_work_space_.activeSubWindow():
                ac.setChecked(True)
            
            ac.triggered.connect(window.setFocus)
            
        


    def windowMenuActivated(self, id):
        if not self.p_work_space_:
            return
        
        w = self.p_work_space_.subWindowList().at(id)
        if w:
            w.setFocus()


    def existFormInMDI(self, id):
        if id is None or not self.p_work_space_:
            return False
        

        for window in self.subWindowList():
           s = w.findChild(pineboolib.pncontrolsfactory.FLFormDB)
           if s.idMDI() == id:
               window.showNormal()
               window.setFocus()
               return True
        
        return False
            

    def openMasterForm(self, action_name, pix):
        if action_name in pineboolib.project.actions.keys():
            pineboolib.project.actions[action_name].openDefaultForm()
        

    @decorators.NotImplementedWarn
    def openDefaultForm(self):
        pass

    def execMainScript(self, action_name):
        if action_name in pineboolib.project.actions.keys():
            pineboolib.project.actions[action_name].execDefaultScript()

    @decorators.NotImplementedWarn
    def execDefaultScript(self):
        pass

    def windowClose(self):
        if self.p_work_space_ is None:
            return
        
        self.p_work_space_.closeActiveWindow()
        

    def loadScriptsFromModule(self, idm):
        if idm in pineboolib.project.modules.keys():
            pineboolib.project.modules[idm].load()

    def activateModule(self, idm=None):
        if not idm:
            if self.sender():
                idm = self.sender().objectName()
        
        if idm is None:
            return 
        
        self.writeStateModule()
        
        w = None
        if idm in self.db().managerModules().listAllIdModules():
            w = self.dict_main_widgets_[idm] if idm in self.dict_main_widgets_.keys() else None
            if not w:
                w = self.db().managerModules().createUI("%s.ui" % idm, self, None, idm)
                
                if not w:
                    return
                
                self.dict_main_widgets_[idm] = w
                w.setObjectName(idm)
                
                if self.acl_:
                    self.acl_.process(w)
                   
                self.setMainWidget(w)
                self.call("%s.init()" % idm, [])
                w.removeEventFilter(self)
                self.db().managerModules().setActiveIdModule(idm)
                self.setMainWidget(w)
                self.initMainWidget()
                self.showMainWidget(w)
                w.installEventFilter(self)
                return 
        
        if not w:
            self.db().managerModules().setActiveIdModule("")
        else:
            self.db().managerModules().setActiveIdModule(idm)
        
        self.setMainWidget(w)
        self.showMainWidget(w)
        

    def reinit(self):
        if self.initializing_ or self.destroying_:
            return

        self.stopTimerIdle()
        # self.apAppIdle()
        self.initializing_ = True
        self.writeState()
        self.writeStateModule()
        
        self.p_work_space_ = None
        
        time = QtCore.QTimer()
        time.singleShot(0, self.reinitP)
        from pineboolib.pnobjectsfactory import empty_base
        empty_base()

    def clearProject(self):
        pineboolib.project.actions = {}
        pineboolib.project.areas = {}
        pineboolib.project.modules = {}
        pineboolib.project.tables = {}

    def reinitP(self):
        self.db().managerModules().finish()
        self.db().manager().finish()
        self.setMainWidget(None)
        self.db().managerModules().setActiveIdModule("")

        if self.dict_main_widgets_:
            self.dict_main_widgets_ = {}

        self.clearProject()
        project = pineboolib.project

        if self.main_widget_ is None:
            self.main_widget_ = pineboolib.project.main_form.mainWindow

        project.main_window.initialized_mods_ = []

        from pineboolib import qsa as qsa_dict_modules
        list_ = [attr for attr in dir(qsa_dict_modules) if not attr[0] == "_"]
        for name in list_:
            att = getattr(qsa_dict_modules, name)
            if isinstance(att, pineboolib.pnapplication.DelayedObjectProxyLoader):
                delattr(qsa_dict_modules, name)

        project.run()
        project.conn.managerModules().loadIdAreas()
        project.conn.managerModules().loadAllIdModules()
        # for module_name in project.modules.keys():
        #    project.modules[module_name].load()
        self.db().manager().init()

        self.db().managerModules()
        self.db().manager().cleanupMetaData()

        if self.acl_:
            self.acl_.init()

        self.loadScripts()
        # self.db().managerModules().setShaFromGlobal()
        self.call("sys.init()", [])
        self.initToolBox()
        self.readState()

        if self.container_:
            
            self.container_.installEventFilter(self)
            #self.container_.setDisable(False)

        self.callScriptEntryFunction()

        self.initializing_ = False
        self.startTimerIdle()

        if hasattr(project.main_window, "reinitSript"):
            project.main_window.reinitSript()

    @decorators.NotImplementedWarn
    def showDocPage(self, url):
        pass

    def timeUser(self):
        return self.time_user_

    def call(self, function, argument_list=[], object_content=None, show_exceptions=True):
        return pineboolib.project.call(function, argument_list, object_content, show_exceptions)

    def setCaptionMainWidget(self, value):
        
        if value:
            self.last_text_caption_ = value
        
        if not self.main_widget_:
            mwi = self.mainWidget()
            if mwi:
                db = self.db().driverNameToDriverAlias(self.db().driverName())
                self.mainWidget().setWindowTitle("Pineboo v%s - %s" % (pineboolib.project.version, self.last_text_caption_))
            
            return
        
        descript_area = self.db().managerModules().idAreaToDescription(self.db().managerModules().activeIdArea())
        descript_module = self.db().managerModules().idModuleToDescription(self.main_widget_.objectName())
        
        if descript_area:
            self.main_widget_.setWindowTitle("%s - %s - %s" % (self.last_text_caption_, descript_area, descript_module))

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

    def setScriptEntryFunction(self, script_enttry_function):
        self.script_entry_function_ = script_enttry_function

    @decorators.NotImplementedWarn
    def setDatabaseLockDetection(self, on, msec_lapsus, lim_checks, show_warn, msg_warn, connection_name):
        pass

    def popupWarn(self, msg_warn, script_calls=[]):
        mw = self.container_ or self.main_widget_
        
        from pineboolib.pnconotrlsfactory import QWhatsThis, QMainWindow, QApplication
        
        wi = QWhatsThis

        if script_calls:
            if not mw:
                self.container_ = QMainWindow(QApplication.desktop())

            if not self.popup_warn_:
                self.popup_warn_ = FLPopupWarn(mw)

            self.popup_warn_.script_calls_ = script_calls
            wi.showText(QApplication.desktop().mapToGlobal(QtCore.QPoint(5, 5)), msg_warn,  mw)

        else:

            if not mw:
                return

        if not mw.isHidden():
            wi.showText(self.mainWidget().mapToGlobal(QtCore.QPoint(mw.width() *2 , 0)), msg_warn, mw)
            QtCore.QTimer().singleShot(4000, wi.hideText)
            qApp.processEvents()

    @decorators.NotImplementedWarn
    def checkDatabaseLocks(self, timer_):
        pass

    @decorators.NotImplementedWarn
    def saveGeometryForm(self, name, geo):
        pass

    @decorators.NotImplementedWarn
    def geometryForm(self, name):
        pass

    def staticLoaderSetup(self):
        self.db().managerModules().staticLoaderSetup()

    def mrProper(self):
        self.db().conn.Mr_Proper()

    def showConsole(self):
        mw = self.mainWidget()
        if mw:
            if self.ted_output_:
                self.ted_output_.parentWidget().close()

            
            from pineboolib.pncontrolsfactory import FLTextEditOutput, QDockWidget
            dw = QDockWidget("tedOutputDock", mw)
            self.ted_output_ = FLTextEditOutput(dw)
            dw.setWidget(self.ted_output_)
            dw.setWindowTitle(self.tr("Mensajes de Eneboo"))
            mw.addDockWidget(QtCore.Qt.BottomDockWidgetArea, dw)

    def consoleShown(self):
        return self.ted_output_ and not self.ted_output_.isHidden()

    @decorators.NotImplementedWarn
    def modMainWidget(self, id_modulo):
        pass

    def evaluateProject(self):
        QtCore.QTimer.singleShot(0, self.callScriptEntryFunction)

    def callScriptEntryFunction(self):
        if self.script_entry_function_:
            self.call(self.script_entry_function_, [], self)
            self.script_entry_function_ = None


    def emitTransactionBegin(self, o):
        if self.notify_begin_transaction_:
            o.transactionBegin.emit()


    def emitTransactionEnd(self, o):
        if self.notify_end_transaction_:
            o.transactionEnd.emit()


    def emitTransactionRollback(self, o):
        if self.notify_roll_back_transaction_:
            o.transsactionRollBack.emit()

    @decorators.NotImplementedWarn
    def gsExecutable(self):
        pass

    @decorators.NotImplementedWarn
    def evalueateProject(self):
        pass

    def aqAppIdle(self):
        if pineboolib.project._DGI.localDesktop():
            from pineboolib.pncontrolsfactory import QApplication
            if self.wb_ or not self.project_ or QApplication.activeModalWidget() or QApplication.activePopupWidget():
                return

            self.checkAndFixTransactionLevel("Application::aqAppIdle()")
            
    
    def DGI(self):
        return pineboolib.project._DGI
    

    def startTimerIdle(self):
        if not self.timer_idle_:
            self.timer_idle_ = QTimer()
            self.timer_idle_.timeout.connect(self.aqAppIdle)
        else:
            self.timer_idle_.stop()
        
        self.timer_idle_.start(1000)

    def stopTimerIdle(self):
        if self.timer_idle_ and self.timer_idle_.isActive():
            self.timer_idle_.stop()

    """
    Para especificar si usa fllarge unificado o multiple (Eneboo/Abanq)
    @return True (Tabla única), False (Múltiples tablas)
    """

    def singleFLLarge(self):
        from pineboolib.fllegacy.flutil import FLUtil
        ret = FLUtil().sqlSelect("flsettings", "valor", "flkey='FLLargeMode'")
        if ret == "True":
            return False

        return True


    def msgBoxWarning(self, t, _gui):            
        _gui.msgBoxWarning(t)

    def checkAndFixTransactionLevel(self, ctx=None):
        dict_db = self.db().dictDatabases()
        if not dict_db:
            return
        
        roll_back_done = False
        for it in dict_db:
            if it.transactionLevel() <= 0:
                continue
            roll_back_done = True
            if it.lastActiveCursor():
                it.lastActiveCursor().rollbackOpened(-1)
            if it.transactionLevel <= 0:
                continue
            
        
        if not roll_back_done:
            return
        
        
        msg =   self.tr("Se han detectado transacciones abiertas en estado inconsistente.\n"
                                "Esto puede suceder por un error en la conexión o en la ejecución\n"
                                "de algún proceso de la aplicación.\n"
                                "Para mantener la consistencia de los datos se han deshecho las\n"
                                "últimas operaciones sobre la base de datos.\n"
                                "Los últimos datos introducidos no han sido guardados, por favor\n"
                                "revise sus últimas acciones y repita las operaciones que no\n"
                                "se han guardado.\n")
        
        if ctx is not None:
            
            msg += self.tr("Contexto: %1\n").arg(ctx)
        
        self.msgBoxWarning(msg)
        logger.warning("%s\n", msg)
        

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
        ret_ = self.main_widget_
        if ret_ is None:
            ret_ = self.container_
        return ret_

    def generalExit(self, ask_exit=True):
        do_exit = True
        if ask_exit:
            do_exit = self.queryExit()
        if do_exit:
            self.destroying_ = True
            if self.consoleShown():
                self.ted_output_.close()

            if not self.form_alone_:
                self.writeState()
                self.writeStateModule()


            if self.db().driverName():
                self.db().managerModules().finish()
                self.db().manager().finish()
                QtCore.QTimer().singleShot(0, self.quit)
            
            for mw in self.dict_main_widgets_.values():
                mw.close()
            
            return True
        else:
            return False

    def quit(self):
        if self.main_widget_ is not None:
            self.main_widget_.close()

    def queryExit(self):
        if self.not_exit_:
            return False

        from pineboolib.pncontrolsfactory import SysType

        if not SysType().interactiveGUI():
            return True
        
        from pineboolib.pncontrolsfactory import QMessageBox

        ret = QMessageBox.information(self.mainWidget(), self.tr("Salir ..."), self.tr(
            "¿ Quiere salir de la aplicación ?"), QMessageBox.Yes, QMessageBox.No)
        return ret == QMessageBox.Yes

    def writeState(self):

        from pineboolib.pncontrolsfactory import QApplication

        settings = FLSettings()
        settings.writeEntry("MultiLang/Enabled", self.multi_lang_enabled_)
        settings.writeEntry("MultiLang/LangId", self.multi_lang_id_)

        if self.container_ is not None:
            windows_opened = []
            _list = QApplication.topLevelWidgets()

            if self.initializing_:
                for it in _list:
                    it.removeEventFilter(self)
                    if it.objectName() in self.dict_main_widgets_.keys():
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
        if not idm:
            return
        if self.main_widget_ is None or self.main_widget_.objectName() != idm:
            return


        windows_opened = []
        if self.main_widget_ is not None and self.p_work_space_ is not None:
            for w in self.p_work_space_.subWindowList():
                s = w.findChild(pineboolib.pncontrolsfactory.FLFormDB)
                if s is not None:
                    windows_opened.append(s.idMDI())


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
        
        from pineboolib.pncontrolsfactory import QApplication, QWidget, QMainWindow

        if self.container_:
            r = QtCore.QRect(self.container_.pos(), self.container_.size())
            self.multi_lang_enabled_ = settings.readBoolEntry("MultiLang/Enabled", False)
            self.multi_lang_id_ = settings.readEntry("MultiLang/LangId", QtCore.QLocale().name()[:2].upper())

            if not settings.readBoolEntry("Geometry/MainWindowMaximized", False):
                r.setX(settings.readNumEntry("Geometry/MainWindowX", r.x()))
                r.setY(settings.readNumEntry("Geometry/MainWindowY", r.y()))
                r.setWidth(settings.readNumEntry("Geometry/MainWindowWidth", r.width()))
                r.setHeight(settings.readNumEntry("Geometry/MainWindowHeight", r.height()))

                desk = QApplication.desktop().availableGeometry(self.container_)
                inter = desk.intersected(r)
                self.container_.resize(r.size())
                if inter.width() * inter.height() > (r.width() * r.height() / 20):
                    self.container_.move(r.topLeft())

            else:
                self.container_.resize(QApplication.desktop().availableGeometry(self.container_).size())

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
                            w.setObjectName(it)
                            if self.acl_:
                                self.acl_.process(w)
                            
                            self.setCaptionMainWidget(None)
                            self.setMainWidget(w)
                            self.call("%s.init()" % it, [])
                            self.db().managerModules().setActiveIdModule(it)
                            self.setMainWidget(w)
                            self.initMainWidget()

            for k in self.dict_main_widgets_.keys():
                w = self.dict_main_widgets_[k]
                if w.objectName() != active_id_module:
                    w.installEventFilter(self)
                    w.show()
                    w.setFont(QApplication.font())
                    if not isinstance(w, QMainWindow):
                        continue

                    view_back = w.centralWidget()
                    if view_back is not None:
                        self.p_work_space_ = view_back.findChild(QWidget, w.objectName())

            if active_id_module:
                self.container_.show()
                self.container_.setFont(self.font())

            self.activateModule(active_id_module)
    

    def readStateModule(self):
        
        from pineboolib.pncontrolsfactory import QAction, QApplication
        
        idm = self.db().managerModules().activeIdModule()
        if not idm:
            return 
        
        if self.main_widget_ is None or self.main_widget_.objectName() != idm:
            return
        
        windows_opened = FLSettings().readListEntry("windowsOpened/%s" % idm)
        if windows_opened:
            for it in windows_opened:
                act = self.main_widget_.findChild(QAction, it)
                if act and act.isVisible():
                    self.openMasterForm(it, act.icon())
        
        
        r = QRect(self.main_widget_.pos(), self.main_widget_.size())
        k = "Geometry/%s" % idm
        
        if not FLSettings().readBoolEntry("%s/Maximized" % k, False):
            r.setX(FLSettings().readNumEntry("%s/X" % k, r.x()))
            r.setY(FLSettings().readNumEntry("%s/Y" % k, r.y()))
            r.setWidth(FLSettings().readNumEntry("%s/Width" % k, r.width()))
            r.setWidth(FLSettings().readNumEntry("%s/Height" % k, r.height()))
            desk = QApplication.desktop().availableGeometry(self.main_widget_)
            inter = desk.intersected(r)
            self.main_widget_.resize(r.size())
            if (inter.width() * inter.height()) > (r.width() * r.height() / 20):
                self.main_widget_.move(r.topLeft())
            else:
                self.main_widget_.resize(QApplication.desktop().availableGeometry(self.main_widget_).size()) 

    def loadScripts(self):
        from pineboolib.pncontrolsfactory import QApplication
        QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        #list_modules = self.mng_loader_.listAllIdModules()
        list_modules = self.db().managerModules().listAllIdModules()
        for it in list_modules:
            self.loadScriptsFromModule(it)

        QApplication.restoreOverrideCursor()

    def urlPineboo(self):
        self.call("sys.openUrl", ["http://eneboo.org/"])

    def helpIndex(self):
        self.call("sys.openUrl", ["http://manuales-eneboo-pineboo.org/"])

    def tr(self, text):
        from pineboolib.pncontrolsfactory import QApplication
        return QApplication.translate("system", text)

        """
    Instala las traducciones cargadas
    """
    def loadTranslations(self):
        translatorsCopy = []
        if self.translator_:
            for t in self.translator_:
                translatorsCopy.append(t) 
            for it in translatorsCopy:
                self.removeTranslator(it)

        lang = QtCore.QLocale().name()[:2]
        
        if lang == "C":
            lang = "es"
        
        for module in self.modules().keys():
            self.loadTranslationFromModule(module, lang)

        for it in translatorsCopy:
            if it.sysTrans_:
                self.installTranslator(it)
            else:
                del it

    """
    Busca la traducción de un texto a un Idioma dado
    @param s, Cadena de texto
    @param l, Idioma.
    @return Cadena de texto traducida. 
    """
    @decorators.BetaImplementation
    def trMulti(self, s, l):
        backMultiEnabled = self.multi_lang_enabled_
        ret = self.tr("%s_MULTILANG" % l.upper(), s)
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
    def loadTranslationFromModule(self, idM, lang):
        self.installTranslator(self.createModTranslator(idM, lang, True))
        # self.installTranslator(self.createModTranslator(idM, "mutliLang"))

    """
    Instala una traducción para la aplicación
    @param tor, Objeto con la traducción a cargar
    """
    def installTranslator(self, tor):
        
        if tor is None:
            return
        else:
            from pineboolib.pncontrolsfactory import qApp
            qApp.installTranslator(tor)
            self.translator_.append(tor)

    """
    Elimina una traducción para la aplicación
    @param tor, Objeto con la traducción a cargar
    """
    def removeTranslator(self, tor):
        if tor is None:
            return
        else:
            from pineboolib.pncontrolsfactory import qApp
            qApp.removeTranslator(tor)
            for t in self.translator_:
                if t == tor:
                    del t
                    break
            

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

    def commaSeparator(self):
        return self.comma_separator
    
    def tmp_dir(self):
        return pineboolib.project.get_temp_dir()


        
        





"""
class FLPopuWarn(QtWidgets.QWhatsThis):

    script_calls_ = []

    def __init__(self, parent):
        self.script_calls_ = []
        super(FLPopuWarn, self).__init__(parent)

    def clicked(self, href):
        if href:

            from pineboolib.pncontrolsfactory import aqApp

            if href.find(":") > -1:
                h = href.split(":")[1]
            if h.find(".") == 1:
                aqApp.call(h.split(".")[1], self.script_calls_[href], h.split(".")[0])
            else:
                aqApp.call(h, self.script_calls_[href], None)
"""