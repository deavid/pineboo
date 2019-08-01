# -*- coding: utf-8 -*-
"""FLApplication Module."""

from PyQt5 import QtCore, QtWidgets  # type: ignore
from PyQt5.QtCore import QTimer, QEvent, QRect, QObject  # type: ignore
from PyQt5.QtGui import QCursor  # type: ignore

from pineboolib import logging
from pineboolib.core import decorators
from pineboolib.core.settings import config, settings

from pineboolib.application import project
from pineboolib.application.database import db_signals

from pineboolib.fllegacy.fltranslator import FLTranslator


from typing import Any, Optional, Union, Dict, List, TYPE_CHECKING

if TYPE_CHECKING:
    from pineboolib import pncontrolsfactory
    from pineboolib.application.database.pnsqlcursor import PNSqlCursor
    from pineboolib.fllegacy.flaccesscontrollists import FLAccessControlLists  # noqa: F401


logger = logging.getLogger("FLApplication")


class FLPopupWarn(QtCore.QObject):
    """FLPoppupWarn Class."""

    # FIXME: Incomplete class!
    def __init__(self, mainwindow) -> None:
        """Inicialize."""

        self.mainWindow = mainwindow


class FLApplication(QtCore.QObject):
    """FLApplication Class."""

    _inicializing: bool
    _destroying: bool
    _ted_output: Optional[QtWidgets.QWidget]
    _not_exit: bool
    _multi_lang_enabled: bool
    _multi_lang_id: str
    _translator: List[FLTranslator]
    _dict_main_widgets: Dict[str, Any]
    container_: Optional[QtWidgets.QWidget]  # Contenedor actual??
    _map_geometry_form: List[Any]
    main_widget_: Optional[QtWidgets.QWidget]
    _p_work_space: Any
    tool_box_: Any
    toogle_bars_: Any
    # project_ = None
    mdi_toolbuttons: List[QtWidgets.QToolButton]
    form_alone_: bool
    acl_: Optional["FLAccessControlLists"]
    popup_warn_: Any
    fl_factory_: Any
    op_check_update_: bool
    style = None
    timer_idle_: Optional[QtCore.QTimer] = None
    init_single_fl_large: bool
    show_debug_: bool
    time_user_: QtCore.QTimer
    script_entry_function_: Optional[str]
    event_loop = None
    window_menu = None
    last_text_caption_: Optional[str]
    modules_menu: Any

    def __init__(self) -> None:
        """Create new FLApplication."""
        super(FLApplication, self).__init__()
        self._p_work_space = None
        self.main_widget_ = None
        self.container_ = None
        self.tool_box_ = None
        self.toogle_bars_ = None
        # self.project_ = None
        self.wb_ = None
        self._dict_main_widgets = {}
        self._translator = []
        self._map_geometry_form = []
        self.form_alone_ = False
        self._not_exit = False
        self.acl_ = None
        self.mdi_toolbuttons = []
        self.popup_warn_ = None
        self._inicializing = False
        self._destroying = False
        self.fl_factory_ = None
        self.op_check_update_ = False
        self.window_menu = None
        db_signals.notify_begin_transaction_ = False
        db_signals.notify_end_transaction_ = False
        db_signals.notify_roll_back_transaction_ = False
        self._ted_output = None
        self.style = None
        self.timer_idle_ = None
        self.init_single_fl_large = False
        self.show_debug_ = True  # FIXME
        self.script_entry_function_ = None
        self.last_text_caption_ = None

        # self.fl_factory_ = FLObjectFactory() # FIXME para un futuro
        # self.time_user_ = QtCore.QDateTime.currentDateTime() # Moved to pncontrolsfacotry.SysType
        self._multi_lang_enabled = False
        self._multi_lang_id = QtCore.QLocale().name()[:2].upper()

        self.locale_system_ = QtCore.QLocale.system()
        v = 1.1
        self.comma_separator = self.locale_system_.toString(v, "f", 1)[1]
        self.setObjectName("aqApp")
        self.event_loop = QtCore.QEventLoop()

    def __del__(self) -> None:
        """Cleanup."""
        self._destroying = True
        self.stopTimerIdle()
        # self.checkAndFixTransactionLAvel("%s:%s" % (__name__, __class__))
        app_db = self.db()
        if app_db:
            app_db.setInteractiveGUI(False)
            app_db.setQsaExceptions(False)

        if self._dict_main_widgets:
            for mw in self._dict_main_widgets:

                del mw
            del self._dict_main_widgets
            self._dict_main_widgets = {}

        self.clearProject()
        # self.project_ = None
        self._ted_output = None

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

    def eventFilter(self, obj, ev) -> Any:
        """React to user events."""
        from pineboolib import pncontrolsfactory

        if self._inicializing or self._destroying:
            return super().eventFilter(obj, ev)

        if pncontrolsfactory.QApplication.activeModalWidget() or pncontrolsfactory.QApplication.activePopupWidget():
            return super().eventFilter(obj, ev)

        evt = ev.type()
        if obj != self.main_widget_ and not isinstance(obj, pncontrolsfactory.QMainWindow):
            return super().eventFilter(obj, ev)

        # aw = None
        # if self._p_work_space is not None:
        #    aw = QApplication.setActiveWindow(self._p_work_space)
        # if aw is not None and aw != obj and evt not in (QEvent.Resize, QEvent.Close):
        #     obj.removeEventFilter(self)
        #     if evt == QEvent.WindowActivate:
        #         if obj == self.container_:
        #             self.activateModule(None)
        #         else:
        #             self.activateModule(obj.objectName())
        #
        #     if self._p_work_space and self.notify(self._p_work_space, ev):
        #         obj.installEventFilter(self)
        #         return True
        #
        #     obj.installEventFilter(self)

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
                if ke.key() == QtCore.Qt.Key_W and (ke.state() in (QtCore.Qt.Key_Control, QtCore.Qt.Key_Alt)):
                    print("????")
                    return True
                if ke.key() == QtCore.Qt.Key_Escape:
                    obj.hide()
                    return True

        elif evt == QEvent.Close:
            if obj == self.container_:
                ret = self.generalExit()
                if not ret:
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
                    self.modules_menu.pop(QCursor.pos())
                    return True
                else:
                    return False
            else:
                return False

        elif evt == QEvent.Resize and isinstance(obj, project.main_form.MainForm):
            for bt in self.mdi_toolbuttons:
                bt.setMinimumWidth(obj.width() - 10)

            return True

        return super().eventFilter(obj, ev)

    def eventLoop(self) -> "pncontrolsfactory.QEventLoop":
        """Create main event loop."""
        from pineboolib import pncontrolsfactory

        return pncontrolsfactory.QEventLoop()

    @decorators.NotImplementedWarn
    def checkForUpdate(self):
        """Not used in Pineboo."""
        pass

    @decorators.NotImplementedWarn
    def checkForUpdateFinish(self, op):
        """Not used in pineboo."""
        pass

    def init(self) -> None:
        """Initialize FLApplication."""
        from pineboolib import pncontrolsfactory
        from pineboolib.fllegacy.flaccesscontrollists import FLAccessControlLists  # noqa: F811
        from pineboolib.fllegacy.aqsobjects.aqs import AQS

        self._dict_main_widgets = {}

        if self.container_ is None:
            raise Exception("init. self.container_ is empty")

        self.container_.setObjectName("container")
        self.container_.setWindowIcon(pncontrolsfactory.QIcon(AQS.pixmap_fromMimeSource("pineboo.png")))
        if self.db() is not None:
            self.container_.setWindowTitle(self.db().DBName())
        else:
            self.container_.setWindowTitle("Pineboo %s" % project.version)

        # FLDiskCache.init(self)

        self.window_menu = pncontrolsfactory.QMenu(self.container_)
        self.window_menu.setObjectName("windowMenu")

        self.window_cascade_action = pncontrolsfactory.QAction(
            pncontrolsfactory.QIcon(AQS.pixmap_fromMimeSource("cascada.png")), self.tr("Cascada"), self.container_
        )
        self.window_menu.addAction(self.window_cascade_action)

        self.window_tile_action = pncontrolsfactory.QAction(
            pncontrolsfactory.QIcon(AQS.pixmap_fromMimeSource("mosaico.png")), self.tr("Mosaico"), self.container_
        )
        self.window_menu.addAction(self.window_tile_action)

        self.window_close_action = pncontrolsfactory.QAction(
            pncontrolsfactory.QIcon(AQS.pixmap_fromMimeSource("cerrar.png")), self.tr("Cerrar"), self.container_
        )
        self.window_menu.addAction(self.window_close_action)

        self.modules_menu = pncontrolsfactory.QMenu(self.container_)
        self.modules_menu.setObjectName("modulesMenu")
        # self.modules_menu.setCheckable(False)

        w = pncontrolsfactory.QWidget(self.container_)
        w.setObjectName("widgetContainer")
        vl = pncontrolsfactory.QVBoxLayout(w)

        self.exit_button = pncontrolsfactory.QPushButton(
            pncontrolsfactory.QIcon(AQS.pixmap_fromMimeSource("exit.png")), self.tr("Salir"), w
        )
        self.exit_button.setObjectName("pbSalir")
        self.exit_button.setShortcut(pncontrolsfactory.QKeySequence(self.tr("Ctrl+Q")))
        self.exit_button.setSizePolicy(
            pncontrolsfactory.QSizePolicy(pncontrolsfactory.QSizePolicy.Expanding, pncontrolsfactory.QSizePolicy.Fixed)
        )
        self.exit_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.exit_button.setToolTip(self.tr("Salir de la aplicación (Ctrl+Q)"))
        self.exit_button.setWhatsThis(self.tr("Salir de la aplicación (Ctrl+Q)"))
        self.exit_button.clicked.connect(self.container_.close)

        self.tool_box_ = pncontrolsfactory.QToolBox(w)
        self.tool_box_.setObjectName("toolBox")

        vl.addWidget(self.exit_button)
        vl.addWidget(self.tool_box_)
        self.container_.setCentralWidget(w)

        self.db().manager().init()

        self.initStyles()
        self.initMenuBar()

        self.db().manager().loadTables()
        self.db().managerModules().loadKeyFiles()
        self.db().managerModules().loadAllIdModules()
        self.db().managerModules().loadIdAreas()

        self.acl_ = FLAccessControlLists()
        # self.acl_.init()

        # self.loadScripts()
        self.db().managerModules().setShaLocalFromGlobal()
        self.loadTranslations()

        self.call("sys.init", [])
        self.initToolBox()
        self.readState()

        self.container_.installEventFilter(self)
        self.startTimerIdle()

    @decorators.NotImplementedWarn
    def initfcgi(self):
        """Init for fast cgi."""
        pass

    @decorators.NotImplementedWarn
    def addObjectFactory(self, new_object_factory):
        """Add object onctructor. unused."""
        pass

    @decorators.NotImplementedWarn
    def callfcgi(self, call_function, argument_list):
        """Perform fastcgi call."""
        pass

    @decorators.NotImplementedWarn
    def endfcgi(self):
        """End fastcgi call signal."""
        pass

    def localeSystem(self) -> str:
        """Return locale of the system."""
        return self.locale_system_

    @decorators.NotImplementedWarn
    def openQSWorkbench(self):
        """Open debugger. Unused."""
        pass

    def initMainWidget(self) -> None:
        """Init mainwidget UI."""
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

    def showMainWidget(self, w) -> None:
        """Show UI."""
        from pineboolib import pncontrolsfactory

        if not self.container_:
            if w:
                w.show()
            return

        focus_w = pncontrolsfactory.QApplication.focusWidget()
        if w is self.container_ or not w:
            if self.container_.isMinimized():
                self.container_.showNormal()
            elif not self.container_.isVisible():
                self.container_.setFont(self.font())
                self.container_.show()

            if focus_w and isinstance(focus_w, pncontrolsfactory.QMainWindow) and focus_w != self.container_:
                self.container_.setFocus()

            if not self.container_.isActiveWindow():
                self.container_.raise_()
                pncontrolsfactory.QApplication.setActiveWindow(self.container_)

            if self.db() is not None:
                self.container_.setWindowTitle(self.db().database())
            else:
                self.container_.setWindowTitle("Pineboo %s" % project.version)

            return

        if w.isMinimized():
            w.showNormal()
        elif not w.isVisible():
            w.show()
            w.setFont(pncontrolsfactory.QApplication.font())

        if focus_w and isinstance(focus_w, pncontrolsfactory.QMainWindow) and focus_w != w:
            w.setFocus()
        if not w.isActiveWindow():
            w.raise_()
            pncontrolsfactory.QApplication.setActiveWindow(w)

        if w:
            view_back = w.centralWidget()
            if view_back:
                self._p_work_space = view_back.findChild(pncontrolsfactory.FLWorkSpace, w.objectName())
                view_back.show()

        self.setCaptionMainWidget(None)
        descript_area = self.db().managerModules().idAreaToDescription(self.db().managerModules().activeIdArea())
        w.setWindowIcon(pncontrolsfactory.QIcon(self.db().managerModules().iconModule(w.objectName())))
        self.tool_box_.setCurrentIndex(self.tool_box_.indexOf(self.tool_box_.findChild(pncontrolsfactory.QToolBar, descript_area)))

    def setMainWidget(self, w) -> None:
        """Set mainWidget."""
        if not self.container_:
            return
        from pineboolib import pncontrolsfactory

        if w == self.container_ or w is None:
            pncontrolsfactory.QApplication.setActiveWindow(self.container_)
            self.main_widget_ = None
            return

        pncontrolsfactory.QApplication.setActiveWindow(w)
        self.main_widget_ = w

        # mw = self.main_widget_ if isinstance(self.main_widget_, QMainWindow) else None
        mw = self.main_widget_
        if mw is None:
            return

        if self.toogle_bars_:
            tool_bar = mw.findChild(pncontrolsfactory.QToolBar)
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
        """Apply specified style."""
        pass

    def chooseFont(self) -> None:
        """Open font selector."""
        from pineboolib import pncontrolsfactory

        font_ = pncontrolsfactory.QFontDialog().getFont()
        if font_:
            pncontrolsfactory.QApplication.setFont(font_[0])
            save_ = []
            save_.append(font_[0].family())
            save_.append(font_[0].pointSize())
            save_.append(font_[0].weight())
            save_.append(font_[0].italic())

            config.set_value("application/font", save_)

    def showStyles(self) -> None:
        """Open style selector."""
        if not self.style:
            self.initStyles()
        # if self.style:
        #    self.style.exec_()

    @decorators.NotImplementedWarn
    def showToggleBars(self):
        """Show toggle bars."""
        pass

    def initToolBox(self) -> None:
        """Initialize toolbox."""
        from pineboolib import pncontrolsfactory
        from pineboolib.fllegacy.aqsobjects.aqsobjectfactory import AQS

        if self.main_widget_ is None:
            raise Exception("self.main_widget_ is empty!")

        self.tool_box_ = self.main_widget_.findChild(pncontrolsfactory.QToolBox, "toolBox")
        self.modules_menu = self.main_widget_.findChild(pncontrolsfactory.QMenu, "modulesMenu")

        if self.tool_box_ is None or self.modules_menu is None:
            return

        self.modules_menu.clear()
        for n in reversed(range(self.tool_box_.count())):
            item = self.tool_box_widget(n)
            if isinstance(item, pncontrolsfactory.QToolBar):
                item.clear()

            self.tool_box_.removeItem(item)

        for tb in self.mdi_toolbuttons:
            self.mdi_toolbuttons.remove(tb)

        del self.mdi_toolbuttons
        self.mdi_toolbuttons = []

        c = 65

        for it in self.db().managerModules().listIdAreas():
            if it == "sys" and not config.value("application/dbadmin_enabled", False):
                continue
            descript_area = self.db().managerModules().idAreaToDescription(it)
            new_area_bar = pncontrolsfactory.QToolBar(self.tr(descript_area), self.container_)
            new_area_bar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
            # new_area_bar.setFrameStyle(QFrame.NoFrame)
            new_area_bar.setOrientation(QtCore.Qt.Vertical)
            new_area_bar.layout().setSpacing(3)
            self.tool_box_.addItem(new_area_bar, self.tr(descript_area))
            ag = pncontrolsfactory.QActionGroup(new_area_bar)
            ag.setObjectName(descript_area)
            # ac = QAction(ag)
            # ac.setText(descript_area)
            # ac.setUsesDropDown(True)

            list_modules = self.db().managerModules().listIdModules(it)
            list_modules.sort()

            for mod in list_modules:
                if str(chr(c)) == "Q":
                    c += 1
                    continue

                if mod == "sys":
                    if config.value("application/isDebuggerMode", False):

                        descript_module = "%s: %s" % (str(chr(c)), self.tr("Carga Estática desde Disco Duro"))
                        new_module_action = pncontrolsfactory.QAction(new_area_bar)
                        new_module_action.setObjectName("StaticLoadAction")
                        new_module_action.setText(self.tr(descript_module))
                        new_module_action.setShortcut(getattr(QtCore.Qt, "Key_%s" % str(chr(c))))
                        new_module_action.setIcon(pncontrolsfactory.QIcon(AQS.pixmap_fromMimeSource("folder_update.png")))
                        new_area_bar.addAction(new_module_action)
                        new_module_action.triggered.connect(self.staticLoaderSetup)
                        ag.addAction(new_module_action)
                        c += 1

                        descript_module = "%s: %s" % (str(chr(c)), self.tr("Reiniciar Script"))
                        new_module_action = pncontrolsfactory.QAction(new_area_bar)
                        new_module_action.setObjectName("reinitScriptAction")
                        new_module_action.setText(self.tr(descript_module))
                        new_module_action.setShortcut(getattr(QtCore.Qt, "Key_%s" % str(chr(c))))
                        new_module_action.setIcon(pncontrolsfactory.QIcon(AQS.pixmap_fromMimeSource("reload.png")))
                        new_area_bar.addAction(new_module_action)
                        new_module_action.triggered.connect(self.reinit)
                        ag.addAction(new_module_action)
                        c += 1

                        descript_module = "%s: %s" % (str(chr(c)), self.tr("Mostrar Consola de mensajes"))
                        new_module_action = pncontrolsfactory.QAction(new_area_bar)
                        new_module_action.setObjectName("shConsoleAction")
                        new_module_action.setText(self.tr(descript_module))
                        new_module_action.setShortcut(getattr(QtCore.Qt, "Key_%s" % str(chr(c))))
                        new_module_action.setIcon(pncontrolsfactory.QIcon(AQS.pixmap_fromMimeSource("consola.png")))
                        new_area_bar.addAction(new_module_action)
                        new_module_action.triggered.connect(self.showConsole)
                        ag.addAction(new_module_action)
                        c += 1

                descript_module = "%s: %s" % (str(chr(c)), self.db().managerModules().idModuleToDescription(mod))
                new_module_action = pncontrolsfactory.QAction(new_area_bar)
                new_module_action.setObjectName(mod)
                new_module_action.setText(self.tr(descript_module))
                new_module_action.setShortcut(getattr(QtCore.Qt, "Key_%s" % str(chr(c))))
                new_module_action.setIcon(pncontrolsfactory.QIcon(self.db().managerModules().iconModule(mod)))
                new_area_bar.addAction(new_module_action)
                new_module_action.triggered.connect(self.activateModule)
                ag.addAction(new_module_action)
                c += 1

            # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)

            lay = new_area_bar.layout()
            for child in new_area_bar.children():
                if isinstance(child, QtWidgets.QToolButton):
                    self.mdi_toolbuttons.append(child)
                    lay.setAlignment(child, QtCore.Qt.AlignCenter)

            a_menu = self.modules_menu.addMenu(descript_area)
            for a in ag.actions():
                a_menu.addAction(a)

        descript_area = "Configuración"
        config_tool_bar = pncontrolsfactory.QToolBar(self.tr(descript_area), self.container_)
        config_tool_bar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        # config_tool_bar.setFrameStyle(QFrame.NoFrame)
        config_tool_bar.setOrientation(QtCore.Qt.Vertical)
        # config_tool_bar.layout().setSpacing(3)
        self.tool_box_.addItem(config_tool_bar, self.tr(descript_area))

        descript_module = self.tr("Fuente")
        font_action = pncontrolsfactory.QAction(new_area_bar)
        font_action.setObjectName("fontAction")
        font_action.setText(self.tr(descript_module))
        # font_action.setShortcut(getattr(QtCore.Qt, "Key_%s" % str(chr(c))))
        font_action.setIcon(pncontrolsfactory.QIcon(AQS.pixmap_fromMimeSource("font.png")))
        config_tool_bar.addAction(font_action)
        font_action.triggered.connect(self.chooseFont)
        ag.addAction(font_action)

        descript_module = self.tr("Estilo")
        style_action = pncontrolsfactory.QAction(new_area_bar)
        style_action.setObjectName("styleAction")
        style_action.setText(self.tr(descript_module))
        # style_action.setShortcut(getattr(QtCore.Qt, "Key_%s" % str(chr(c))))
        style_action.setIcon(pncontrolsfactory.QIcon(AQS.pixmap_fromMimeSource("estilo.png")))
        config_tool_bar.addAction(style_action)
        style_action.triggered.connect(self.showStyles)
        ag.addAction(style_action)

        descript_module = self.tr("Indice")
        help_action = pncontrolsfactory.QAction(new_area_bar)
        help_action.setObjectName("helpAction")
        help_action.setText(self.tr(descript_module))
        # help_action.setShortcut(getattr(QtCore.Qt, "Key_%s" % str(chr(c))))
        help_action.setIcon(pncontrolsfactory.QIcon(AQS.pixmap_fromMimeSource("help_index.png")))
        config_tool_bar.addAction(help_action)
        help_action.triggered.connect(self.helpIndex)
        ag.addAction(help_action)

        descript_module = self.tr("Acerca de Pineboo")
        about_pineboo_action = pncontrolsfactory.QAction(new_area_bar)
        about_pineboo_action.setObjectName("aboutPinebooAction")
        about_pineboo_action.setText(self.tr(descript_module))
        # help_action.setShortcut(getattr(QtCore.Qt, "Key_%s" % str(chr(c))))
        about_pineboo_action.setIcon(pncontrolsfactory.QIcon(AQS.pixmap_fromMimeSource("about.png")))
        config_tool_bar.addAction(about_pineboo_action)
        about_pineboo_action.triggered.connect(self.aboutPineboo)
        ag.addAction(about_pineboo_action)

        descript_module = self.tr("Visita Eneboo.org")
        visit_pineboo_action = pncontrolsfactory.QAction(new_area_bar)
        visit_pineboo_action.setObjectName("visitPinebooAction")
        visit_pineboo_action.setText(self.tr(descript_module))
        # help_action.setShortcut(getattr(QtCore.Qt, "Key_%s" % str(chr(c))))
        visit_pineboo_action.setIcon(pncontrolsfactory.QIcon(AQS.pixmap_fromMimeSource("about.png")))
        config_tool_bar.addAction(visit_pineboo_action)
        visit_pineboo_action.triggered.connect(self.urlPineboo)
        ag.addAction(visit_pineboo_action)

        descript_module = self.tr("Acerca de Qt")
        about_qt_action = pncontrolsfactory.QAction(new_area_bar)
        about_qt_action.setObjectName("aboutQtAction")
        about_qt_action.setText(self.tr(descript_module))
        # help_action.setShortcut(getattr(QtCore.Qt, "Key_%s" % str(chr(c))))
        about_qt_action.setIcon(pncontrolsfactory.QIcon(AQS.pixmap_fromMimeSource("aboutqt.png")))
        config_tool_bar.addAction(about_qt_action)
        about_qt_action.triggered.connect(self.aboutQt)
        ag.addAction(about_qt_action)

        lay = config_tool_bar.layout()
        for child in config_tool_bar.children():
            if isinstance(child, QtWidgets.QToolButton):
                self.mdi_toolbuttons.append(child)
                lay.setAlignment(child, QtCore.Qt.AlignCenter)

        if self.acl_:
            self.acl_.process(self.container_)

    def workspace(self) -> Any:
        """Get current workspace."""
        return self._p_work_space

    def initActions(self) -> None:
        """Initialize actions."""
        if self.main_widget_ is not None and self._p_work_space is not None:
            self.window_cascade_action.triggered.connect(self._p_work_space.cascadeSubWindows)
            self.window_tile_action.triggered.connect(self._p_work_space.tileSubWindows)
            self.window_close_action.triggered.connect(self._p_work_space.closeActiveSubWindow)

    def initMenuBar(self) -> None:
        """Initialize menus."""
        if self.window_menu is None:
            raise Exception("initMenuBar. self.window_menu is empty!")

        self.window_menu.aboutToShow.connect(self.windowMenuAboutToShow)

    def initToolBar(self) -> None:
        """Initialize toolbar."""
        from pineboolib import pncontrolsfactory

        mw = self.main_widget_
        if mw is None:
            return

        tb = mw.menuBar()
        if tb is None:
            logger.warning("No se encuentra toolbar en %s", mw.objectName())
            return

        # tb.setMovingEnabled(False)

        tb.addSeparator()
        # what_this_button = QWhatsThis(tb)

        if not self.toogle_bars_:
            self.toogle_bars_ = pncontrolsfactory.QMenu(self.container_)
            self.toogle_bars_.setObjectName("toggleBars")
            # self.toogle_bars_.setCheckable(True)

            # ag = QActionGroup(self.container_)
            # ag.setObjectName("agToggleBars")

            a = pncontrolsfactory.QAction(self.tr("Barra de Herramientas"), self.container_)
            a.setObjectName("Herramientas")
            a.setCheckable(True)
            a.setChecked(True)
            a.triggered.connect(self.toggleToolBar)
            self.toogle_bars_.addAction(a)

            b = pncontrolsfactory.QAction(self.tr("Barra de Estado"), self.container_)
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

    def initStatusBar(self) -> None:
        """Initialize statusbar."""
        if not self.main_widget_:
            return

        from pineboolib import pncontrolsfactory

        self.statusHelpMsg(self.tr("Listo."))
        self.main_widget_.statusBar().setSizeGripEnabled(False)

        conexion = pncontrolsfactory.QLabel(self.main_widget_.statusBar())
        conexion.setText("%s@%s" % (self.db().user(), self.db().database()))
        self.main_widget_.statusBar().addWidget(conexion)

    def initView(self) -> None:
        """Initialize view."""
        mw = self.main_widget_

        if mw is None:
            return

        view_back = mw.centralWidget()
        if view_back is None:
            from pineboolib import pncontrolsfactory

            view_back = pncontrolsfactory.QMdiArea()
            view_back.setObjectName("mdi_area")
            self._p_work_space = pncontrolsfactory.FLWorkSpace(view_back, self.db().managerModules().activeIdModule())
            self._p_work_space.setAttribute(QtCore.Qt.WA_NoSystemBackground)
            # p_work_space.setScrollBarsEnabled(True)
            # FIXME: setScrollBarsEnabled
            mw.setCentralWidget(view_back)

    def setStyle(self, style_: Optional[Union[int, str]]) -> None:
        """Change application style."""

        if style_:
            config.set_value("application/style", style_)
            from pineboolib import pncontrolsfactory

            pncontrolsfactory.QApplication.setStyle(style_)

    def initStyles(self) -> None:
        """Initialize styles."""
        from pineboolib.core.settings import config

        self.style_mapper = QtCore.QSignalMapper()
        self.style_mapper.mapped.connect(self.setStyle)  # FIXME: was mapped[str].connect
        style_read = config.value("application/style", None)
        if not style_read:
            style_read = "Fusion"

        from pineboolib import pncontrolsfactory

        style_menu = self.mainWidget().findChild(pncontrolsfactory.QMenu, "style")

        if style_menu:
            ag = pncontrolsfactory.QActionGroup(style_menu)
            for style_ in pncontrolsfactory.QStyleFactory.keys():
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
        """Get tabs."""
        pass

    @decorators.NotImplementedWarn
    def getWidgetList(self, wn, c):
        """Get widgets."""
        pass

    def toggleToolBar(self, toggle) -> None:
        """Show or hide toolbar."""
        if not self.main_widget_:
            return

        from pineboolib import pncontrolsfactory

        tb = self.main_widget_.findChild(pncontrolsfactory.QToolBar)
        if not tb:
            return

        tb.show() if toggle else tb.hide()

    def toggleStatusBar(self, toggle) -> None:
        """Toggle status bar."""
        if not self.main_widget_:
            return

        self.main_widget_.statusBar().show() if toggle else self.main_widget_.statusBar().hide()

    def aboutQt(self) -> None:
        """Show About QT."""
        from pineboolib import pncontrolsfactory

        pncontrolsfactory.QMessageBox.aboutQt(self.mainWidget())

    def aboutPineboo(self) -> None:
        """Show about Pineboo."""
        if project.DGI.localDesktop():
            project.DGI.about_pineboo()

    def statusHelpMsg(self, text) -> None:
        """Show help message."""
        from pineboolib.core.settings import config

        if config.value("application/isDebuggerMode", False):
            logger.warning("StatusHelpMsg: %s", text)

        if not self.main_widget_:
            return

        self.main_widget_.statusBar().showMessage(text, 2000)

    def windowMenuAboutToShow(self) -> None:
        """Signal called before window menu is shown."""
        if not self._p_work_space:
            return
        if self.window_menu is None:
            return
        self.window_menu.clear()
        self.window_menu.addAction(self.window_cascade_action)
        self.window_menu.addAction(self.window_tile_action)
        self.window_menu.addAction(self.window_close_action)

        if not self._p_work_space.subWindowList():
            self.window_cascade_action.setEnabled(False)
            self.window_tile_action.setEnabled(False)
            self.window_close_action.setEnabled(False)
        else:
            self.window_cascade_action.setEnabled(True)
            self.window_tile_action.setEnabled(True)
            self.window_close_action.setEnabled(True)
            self.window_menu.addSeparator()

        for window in self._p_work_space.subWindowList():
            ac = self.window_menu.addAction(window.windowTitle())
            ac.setCheckable(True)

            if window == self._p_work_space.activeSubWindow():
                ac.setChecked(True)

            ac.triggered.connect(window.setFocus)

    def windowMenuActivated(self, id) -> None:
        """Signal called when user clicks on menu."""
        if not self._p_work_space:
            return

        w = self._p_work_space.subWindowList().at(id)
        if w:
            w.setFocus()

    def existFormInMDI(self, id) -> bool:
        """Return if named FLFormDB is open."""
        from pineboolib import pncontrolsfactory

        if id is None or not self._p_work_space:
            return False

        for window in self.subWindowList():
            s = window.findChild(pncontrolsfactory.FLFormDB)
            if s.idMDI() == id:
                window.showNormal()
                window.setFocus()
                return True

        return False

    def openMasterForm(self, action_name, pix) -> None:
        """Open a tab."""
        if action_name in project.actions.keys():
            project.actions[action_name].openDefaultForm()

    @decorators.NotImplementedWarn
    def openDefaultForm(self):
        """Open a default form."""
        pass

    def execMainScript(self, action_name) -> None:
        """Execute main script."""
        if action_name in project.actions.keys():
            project.actions[action_name].execDefaultScript()

    @decorators.NotImplementedWarn
    def execDefaultScript(self):
        """Execute default script."""
        pass

    def windowClose(self) -> None:
        """Signal called on close."""
        if self._p_work_space is None:
            return

        self._p_work_space.closeActiveWindow()

    def loadScriptsFromModule(self, idm) -> None:
        """Load scripts from named module."""
        if idm in project.modules.keys():
            project.modules[idm].load()

    def activateModule(self, idm=None) -> None:
        """Initialize module."""
        if not idm:
            if self.sender():
                idm = self.sender().objectName()

        if idm is None:
            return

        self.writeStateModule()

        w = None
        if idm in self.db().managerModules().listAllIdModules():
            w = self._dict_main_widgets[idm] if idm in self._dict_main_widgets.keys() else None
            if not w:
                w = self.db().managerModules().createUI("%s.ui" % idm, self, None, idm)

                if not w:
                    return

                self._dict_main_widgets[idm] = w
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

    def reinit(self) -> None:
        """Cleanup and restart."""
        if self._inicializing or self._destroying:
            return

        self.stopTimerIdle()
        # self.apAppIdle()
        self._inicializing = True
        self.writeState()
        self.writeStateModule()

        self._p_work_space = None

        QtCore.QTimer.singleShot(0, self.reinitP)
        from pineboolib.application.parsers.mtdparser.pnormmodelsfactory import empty_base

        empty_base()

    def clearProject(self) -> None:
        """Cleanup."""
        project.actions = {}
        project.areas = {}
        project.modules = {}
        project.tables = {}

    def reinitP(self) -> None:
        """Reinitialize project."""
        from pineboolib import qsa as qsa_dict_modules
        from pineboolib.application.proxy import DelayedObjectProxyLoader

        self.db().managerModules().finish()
        self.db().manager().finish()
        self.setMainWidget(None)
        self.db().managerModules().setActiveIdModule("")

        if self._dict_main_widgets:
            self._dict_main_widgets = {}

        self.clearProject()

        if self.main_widget_ is None:
            self.main_widget_ = project.main_form.mainWindow

        if project.main_window is None:
            raise Exception("project.main_window is empty!")

        project.main_window.initialized_mods_ = []

        list_ = [attr for attr in dir(qsa_dict_modules) if not attr[0] == "_"]
        for name in list_:
            att = getattr(qsa_dict_modules, name)
            if isinstance(att, DelayedObjectProxyLoader):
                delattr(qsa_dict_modules, name)

        project.run()
        self.db().managerModules().loadIdAreas()
        self.db().managerModules().loadAllIdModules()
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
            # self.container_.setDisable(False)

        self.callScriptEntryFunction()

        self._inicializing = False
        self.startTimerIdle()

        if hasattr(project.main_window, "reinitSript"):
            project.main_window.reinitSript()

    @decorators.NotImplementedWarn
    def showDocPage(self, url):
        """Show documentation."""
        pass

    def timeUser(self) -> Any:
        """Get amount of time running."""
        from pineboolib import pncontrolsfactory

        return pncontrolsfactory.SysType().time_user_

    def call(self, function, argument_list=[], object_content=None, show_exceptions=True) -> Any:
        """Call a QS project function."""
        return project.call(function, argument_list, object_content, show_exceptions)

    def setCaptionMainWidget(self, value) -> None:
        """Set application title."""
        if value:
            self.last_text_caption_ = value

        # FIXME: main_form_name Belongs to loader.main; will be removed
        if project.main_form_name != "eneboo_mdi":
            self.mainWidget().setWindowTitle("Pineboo %s - %s" % (project.version, self.last_text_caption_))

        else:
            if self.main_widget_ is None:
                raise Exception("self.main_widget_ is empty!")

            descript_area = self.db().managerModules().idAreaToDescription(self.db().managerModules().activeIdArea())
            descript_module = self.db().managerModules().idModuleToDescription(self.main_widget_.objectName())

            if descript_area:
                self.main_widget_.setWindowTitle("%s - %s - %s" % (self.last_text_caption_, descript_area, descript_module))

    @decorators.NotImplementedWarn
    def setNotExit(self, b):
        """Protect against window close."""
        self._not_exit = b

    @decorators.NotImplementedWarn
    def printTextEdit(self, editor_):
        """Not implemented."""
        pass

    @decorators.NotImplementedWarn
    def setPrintProgram(self, print_program_):
        """Not implemented."""
        pass

    @decorators.NotImplementedWarn
    def addSysCode(self, code, scritp_entry_function):
        """Not implemented."""
        pass

    def setScriptEntryFunction(self, script_enttry_function) -> None:
        """Set which QS function to call on startup."""
        self.script_entry_function_ = script_enttry_function

    @decorators.NotImplementedWarn
    def setDatabaseLockDetection(self, on, msec_lapsus, lim_checks, show_warn, msg_warn, connection_name):
        """Not implemented."""
        pass

    def popupWarn(self, msg_warn, script_calls=[]) -> None:
        """Show a warning popup."""
        mw = self.container_ or self.main_widget_

        from pineboolib import pncontrolsfactory

        wi = QtWidgets.QWhatsThis

        if script_calls:
            if not mw:
                self.container_ = pncontrolsfactory.QMainWindow(pncontrolsfactory.QApplication.desktop())

            if not self.popup_warn_:
                self.popup_warn_ = FLPopupWarn(mw)  # FIXME: Empty class yet!

            self.popup_warn_.script_calls_ = script_calls
            wi.showText(pncontrolsfactory.QApplication.desktop().mapToGlobal(QtCore.QPoint(5, 5)), msg_warn, mw)

        else:

            if not mw:
                return

        if mw is None:
            raise Exception("self.container_ and self.main_widget are empty!")

        if not mw.isHidden():
            wi.showText(self.mainWidget().mapToGlobal(QtCore.QPoint(mw.width() * 2, 0)), msg_warn, mw)
            QtCore.QTimer.singleShot(4000, wi.hideText)
            self.processEvents()

    @decorators.NotImplementedWarn
    def checkDatabaseLocks(self, timer_):
        """Not implemented."""
        pass

    @decorators.NotImplementedWarn
    def saveGeometryForm(self, name, geo):
        """Not implemented."""
        pass

    @decorators.NotImplementedWarn
    def geometryForm(self, name):
        """Not implemented."""
        pass

    def staticLoaderSetup(self) -> None:
        """Initialize static loader."""
        self.db().managerModules().staticLoaderSetup()

    def mrProper(self) -> None:
        """Cleanup database."""
        self.db().conn.Mr_Proper()

    def showConsole(self) -> None:
        """Show application console on GUI."""
        mw = self.mainWidget()
        if mw:
            if self._ted_output:
                self._ted_output.parentWidget().close()

            from pineboolib import pncontrolsfactory

            dw = pncontrolsfactory.QDockWidget("tedOutputDock", mw)
            self._ted_output = pncontrolsfactory.FLTextEditOutput(dw)
            dw.setWidget(self._ted_output)
            dw.setWindowTitle(self.tr("Mensajes de Eneboo"))
            mw.addDockWidget(QtCore.Qt.BottomDockWidgetArea, dw)

    def consoleShown(self) -> bool:
        """Return if console is shown."""
        return bool(self._ted_output and not self._ted_output.isHidden())

    @decorators.NotImplementedWarn
    def modMainWidget(self, id_modulo):
        """Not implemented."""
        pass

    def evaluateProject(self) -> None:
        """Execute QS entry function."""
        QtCore.QTimer.singleShot(0, self.callScriptEntryFunction)

    def callScriptEntryFunction(self) -> None:
        """Execute QS entry function."""
        if self.script_entry_function_:
            self.call(self.script_entry_function_, [], self)
            self.script_entry_function_ = None

    def emitTransactionBegin(self, o: "PNSqlCursor") -> None:
        """Emit signal."""
        db_signals.emitTransactionBegin(o)

    def emitTransactionEnd(self, o: "PNSqlCursor") -> None:
        """Emit signal."""
        db_signals.emitTransactionEnd(o)

    def emitTransactionRollback(self, o: "PNSqlCursor") -> None:
        """Emit signal."""
        db_signals.emitTransactionRollback(o)

    @decorators.NotImplementedWarn
    def gsExecutable(self):
        """Not implemented."""
        pass

    @decorators.NotImplementedWarn
    def evalueateProject(self):
        """Not implemented."""
        pass

    def aqAppIdle(self) -> None:
        """Check and fix transaction level."""
        if project.DGI.localDesktop():
            from pineboolib import pncontrolsfactory

            if (
                # not self.project_ or
                pncontrolsfactory.QApplication.activeModalWidget()
                or pncontrolsfactory.QApplication.activePopupWidget()
            ):
                return

            self.checkAndFixTransactionLevel("Application::aqAppIdle()")

    def DGI(self) -> Any:
        """Return current DGI."""
        return project._DGI

    def startTimerIdle(self) -> None:
        """Start timer."""
        if not self.timer_idle_:
            self.timer_idle_ = QTimer()
            self.timer_idle_.timeout.connect(self.aqAppIdle)
        else:
            self.timer_idle_.stop()

        self.timer_idle_.start(1000)

    def stopTimerIdle(self) -> None:
        """Stop timer."""
        if self.timer_idle_ and self.timer_idle_.isActive():
            self.timer_idle_.stop()

    def singleFLLarge(self) -> bool:
        """
        Para especificar si usa fllarge unificado o multiple (Eneboo/Abanq).

        @return True (Tabla única), False (Múltiples tablas)
        """
        from pineboolib.fllegacy.flutil import FLUtil

        ret = FLUtil().sqlSelect("flsettings", "valor", "flkey='FLLargeMode'")
        if ret == "True":
            return False

        return True

    def msgBoxWarning(self, t, _gui) -> None:
        """Display warning."""
        _gui.msgBoxWarning(t)

    def checkAndFixTransactionLevel(self, ctx=None) -> None:
        """Fix transaction."""
        dict_db = self.db().dictDatabases()
        if not dict_db:
            return

        roll_back_done = False
        for it in dict_db.values():
            if it.transactionLevel() <= 0:
                continue
            roll_back_done = True
            if it.lastActiveCursor():
                it.lastActiveCursor().rollbackOpened(-1)
            if it.transactionLevel <= 0:
                continue

        if not roll_back_done:
            return

        msg = self.tr(
            "Se han detectado transacciones abiertas en estado inconsistente.\n"
            "Esto puede suceder por un error en la conexión o en la ejecución\n"
            "de algún proceso de la aplicación.\n"
            "Para mantener la consistencia de los datos se han deshecho las\n"
            "últimas operaciones sobre la base de datos.\n"
            "Los últimos datos introducidos no han sido guardados, por favor\n"
            "revise sus últimas acciones y repita las operaciones que no\n"
            "se han guardado.\n"
        )

        if ctx is not None:

            msg += self.tr("Contexto: %1\n").arg(ctx)

        # FIXME: Missing _gui parameter
        # self.msgBoxWarning(msg)
        logger.warning("%s\n", msg)

    @decorators.NotImplementedWarn
    def showDebug(self):
        """Return if debug is shown."""
        return self.show_debug_

    def db(self) -> Any:
        """Return current connection."""
        return project._conn

    @decorators.NotImplementedWarn
    def classType(self, n):
        """Return class for object."""
        from pineboolib import pncontrolsfactory

        return type(pncontrolsfactory.resolveObject(n)())

    # def __getattr__(self, name):
    #    return getattr(project, name, None)

    def mainWidget(self) -> Any:
        """Return current mainWidget."""
        ret_ = self.main_widget_
        if ret_ is None:
            ret_ = self.container_
        return ret_

    def generalExit(self, ask_exit=True) -> bool:
        """Perform before close checks."""
        do_exit = True
        if ask_exit:
            do_exit = self.queryExit()
        if do_exit:
            self._destroying = True
            if self.consoleShown():
                if self._ted_output is not None:
                    self._ted_output.close()

            if not self.form_alone_:
                self.writeState()
                self.writeStateModule()

            if self.db().driverName():
                self.db().managerModules().finish()
                self.db().manager().finish()
                QtCore.QTimer.singleShot(0, self.quit)

            for mw in self._dict_main_widgets.values():
                mw.close()

            return True
        else:
            return False

    def quit(self) -> None:
        """Handle quit/close signal."""
        if self.main_widget_ is not None:
            self.main_widget_.close()

    def queryExit(self) -> Any:
        """Ask user if really wants to quit."""
        if self.not_exit_:
            return False

        from pineboolib import pncontrolsfactory

        if not pncontrolsfactory.SysType().interactiveGUI():
            return True

        ret = pncontrolsfactory.QMessageBox.information(
            self.mainWidget(),
            self.tr("Salir ..."),
            self.tr("¿ Quiere salir de la aplicación ?"),
            pncontrolsfactory.QMessageBox.Yes,
            pncontrolsfactory.QMessageBox.No,
        )
        return ret == pncontrolsfactory.QMessageBox.Yes

    def writeState(self) -> None:
        """Write settings back to disk."""
        from pineboolib import pncontrolsfactory

        settings.set_value("MultiLang/Enabled", self._multi_lang_enabled)
        settings.set_value("MultiLang/LangId", self._multi_lang_id)

        if self.container_ is not None:
            windows_opened = []
            _list = pncontrolsfactory.QApplication.topLevelWidgets()

            if self._inicializing:
                for it in _list:
                    it.removeEventFilter(self)
                    if it.objectName() in self._dict_main_widgets.keys():
                        if it != self.container_:
                            if it.isVisible():
                                windows_opened.append(it.objectName())
                            it.hide()
                        else:
                            it.setDisabled(True)
            else:
                for it in _list:
                    if it != self.container_ and it.isVisible() and it.objectName() in self._dict_main_widgets.keys():
                        windows_opened.append(it.objectName())

            settings.set_value("windowsOpened/Main", windows_opened)
            settings.set_value("Geometry/MainWindowMaximized", self.container_.isMaximized())
            if not self.container_.isMaximized():
                settings.set_value("Geometry/MainWindowX", self.container_.x())
                settings.set_value("Geometry/MainWindowY", self.container_.y())
                settings.set_value("Geometry/MainWindowWidth", self.container_.width())
                settings.set_value("Geometry/MainWindowHeight", self.container_.height())

        for map in self._map_geometry_form:  # FIXME esto no se rellena nunca
            k = "Geometry/%s/" % map.key()
            settings.set_value("%s/X" % k, map.x())
            settings.set_value("%s/Y" % k, map.y())
            settings.set_value("%s/Width" % k, map.width())
            settings.set_value("%s/Height" % k, map.height())

    def writeStateModule(self) -> None:
        """Write settings for modules."""
        from pineboolib import pncontrolsfactory

        idm = self.db().managerModules().activeIdModule()
        if not idm:
            return
        if self.main_widget_ is None or self.main_widget_.objectName() != idm:
            return

        windows_opened: List[str] = []
        if self.main_widget_ is not None and self._p_work_space is not None:
            for w in self._p_work_space.subWindowList():
                s = w.findChild(pncontrolsfactory.FLFormDB)
                if s is not None:
                    windows_opened.append(s.idMDI())

        settings.set_value("windowsOpened/%s" % idm, windows_opened)

        k = "Geometry/%s" % idm
        settings.set_value("%s/Maximized" % k, self.main_widget_.isMaximized())
        settings.set_value("%s/X" % k, self.main_widget_.x())
        settings.set_value("%s/Y" % k, self.main_widget_.y())
        settings.set_value("%s/Width" % k, self.main_widget_.width())
        settings.set_value("%s/Height" % k, self.main_widget_.height())

    def readState(self) -> None:
        """Read settings."""
        self._inicializing = False
        self._dict_main_widgets = {}

        from pineboolib import pncontrolsfactory

        if self.container_:
            r = QtCore.QRect(self.container_.pos(), self.container_.size())
            self._multi_lang_enabled = settings.value("MultiLang/Enabled", False)
            self._multi_lang_id = settings.value("MultiLang/LangId", QtCore.QLocale().name()[:2].upper())

            if not settings.value("Geometry/MainWindowMaximized", False):
                r.setX(settings.value("Geometry/MainWindowX", r.x()))
                r.setY(settings.value("Geometry/MainWindowY", r.y()))
                r.setWidth(settings.value("Geometry/MainWindowWidth", r.width()))
                r.setHeight(settings.value("Geometry/MainWindowHeight", r.height()))

                desk = pncontrolsfactory.QApplication.desktop().availableGeometry(self.container_)
                inter = desk.intersected(r)
                self.container_.resize(r.size())
                if inter.width() * inter.height() > (r.width() * r.height() / 20):
                    self.container_.move(r.topLeft())

            else:
                self.container_.resize(pncontrolsfactory.QApplication.desktop().availableGeometry(self.container_).size())

            active_id_module = self.db().managerModules().activeIdModule()

            windows_opened = settings.value("windowsOpened/Main", [])

            for it in windows_opened:
                if it in self.db().managerModules().listAllIdModules():
                    w = None
                    if it in self._dict_main_widgets.keys():
                        w = self._dict_main_widgets[it]
                    if w is None:
                        act = self.container_.findChild(QtWidgets.QAction, it)
                        if not act or not act.isVisible():
                            continue

                        w = self.db().managerModules().createUI("%s.ui" % it, self, None, it)
                        self._dict_main_widgets[it] = w
                        w.setObjectName(it)
                        if self.acl_:
                            self.acl_.process(w)

                        self.setCaptionMainWidget(None)
                        self.setMainWidget(w)
                        self.call("%s.init()" % it, [])
                        self.db().managerModules().setActiveIdModule(it)
                        self.setMainWidget(w)
                        self.initMainWidget()

            for k in self._dict_main_widgets.keys():
                w = self._dict_main_widgets[k]
                if w.objectName() != active_id_module:
                    w.installEventFilter(self)
                    w.show()
                    w.setFont(pncontrolsfactory.QApplication.font())
                    if not isinstance(w, pncontrolsfactory.QMainWindow):
                        continue

                    view_back = w.centralWidget()
                    if view_back is not None:
                        self._p_work_space = view_back.findChild(pncontrolsfactory.QWidget, w.objectName())

            if active_id_module:
                self.container_.show()
                self.container_.setFont(self.font())

            self.activateModule(active_id_module)

    def readStateModule(self) -> None:
        """Read settings for module."""
        from pineboolib import pncontrolsfactory

        idm = self.db().managerModules().activeIdModule()
        if not idm:
            return

        if self.main_widget_ is None or self.main_widget_.objectName() != idm:
            return

        windows_opened = settings.value("windowsOpened/%s" % idm, None)
        if windows_opened:
            for it in windows_opened:
                act = self.main_widget_.findChild(QObject, it)
                if act and act.isVisible():
                    self.openMasterForm(it, act.icon())

        r = QRect(self.main_widget_.pos(), self.main_widget_.size())
        k = "Geometry/%s" % idm
        if not settings.value("%s/Maximized" % k, False):
            r.setX(settings.value("%s/X" % k, r.x()))
            r.setY(settings.value("%s/Y" % k, r.y()))
            r.setWidth(settings.value("%s/Width" % k, r.width()))
            r.setHeight(settings.value("%s/Height" % k, r.height()))
            desk = pncontrolsfactory.QApplication.desktop().availableGeometry(self.main_widget_)
            inter = desk.intersected(r)
            self.main_widget_.resize(r.size())
            if (inter.width() * inter.height()) > (r.width() * r.height() / 20):
                self.main_widget_.move(r.topLeft())
            else:
                self.main_widget_.resize(pncontrolsfactory.QApplication.desktop().availableGeometry(self.main_widget_).size())

    def loadScripts(self) -> None:
        """Load scripts for all modules."""
        from pineboolib import pncontrolsfactory

        pncontrolsfactory.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        list_modules = self.db().managerModules().listAllIdModules()
        for it in list_modules:
            self.loadScriptsFromModule(it)

        pncontrolsfactory.QApplication.restoreOverrideCursor()

    def urlPineboo(self) -> None:
        """Open Eneboo URI."""
        self.call("sys.openUrl", ["http://eneboo.org/"])

    def helpIndex(self) -> None:
        """Open help."""
        self.call("sys.openUrl", ["http://manuales-eneboo-pineboo.org/"])

    def tr(self, sourceText: str, disambiguation: Optional[str] = None, n: int = 0) -> Any:
        """Open translations."""
        from pineboolib import pncontrolsfactory

        return pncontrolsfactory.QApplication.translate("system", sourceText)

    def loadTranslations(self) -> None:
        """
        Install loaded translations.
        """
        translatorsCopy = []
        if self._translator:
            for t in self._translator:
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

    @decorators.BetaImplementation
    def trMulti(self, s, l):
        """
        Lookup translation for certain language.

        @param s, Cadena de texto
        @param l, Idioma.
        @return Cadena de texto traducida.
        """
        return s
        # FIXME: self.tr does not support two arguments.
        # backMultiEnabled = self._multi_lang_enabled
        # ret = self.tr("%s_MULTILANG" % l.upper(), s)
        # self._multi_lang_enabled = backMultiEnabled
        # return ret

    @decorators.BetaImplementation
    def setMultiLang(self, enable, langid):
        """
        Change multilang status.

        @param enable, Boolean con el nuevo estado
        @param langid, Identificador del leguaje a activar
        """
        self._multi_lang_enabled = enable
        if enable and langid:
            self._multi_lang_id = langid.upper()

    def loadTranslationFromModule(self, idM, lang) -> None:
        """
        Load translation from module.

        @param idM, Identificador del módulo donde buscar
        @param lang, Lenguaje a buscar
        """
        self.installTranslator(self.createModTranslator(idM, lang, True))
        # self.installTranslator(self.createModTranslator(idM, "mutliLang"))

    def installTranslator(self, tor) -> None:
        """
        Install translation for app.

        @param tor, Objeto con la traducción a cargar
        """

        if tor is None:
            return
        else:
            from pineboolib import pncontrolsfactory

            pncontrolsfactory.qApp.installTranslator(tor)
            self._translator.append(tor)

    def removeTranslator(self, tor) -> None:
        """
        Delete translation on app.

        @param tor, Objeto con la traducción a cargar
        """
        if tor is None:
            return
        else:
            from pineboolib import pncontrolsfactory

            pncontrolsfactory.qApp.removeTranslator(tor)
            for t in self._translator:
                if t == tor:
                    del t
                    break

    @decorators.NotImplementedWarn
    def createSysTranslator(self, lang, loadDefault):
        """
        Create SYS Module translation.

        @param lang, Idioma a usar
        @param loadDefault, Boolean para cargar los datos por defecto
        @return objeto traducción
        """
        pass

    def createModTranslator(self, idM, lang, loadDefault=False) -> Optional["FLTranslator"]:
        """
        Create new translation for module.

        @param idM, Identificador del módulo
        @param lang, Idioma a usar
        @param loadDefault, Boolean para cargar los datos por defecto
        @return objeto traducción
        """

        fileTs = "%s.%s.ts" % (idM, lang)
        key = self.db().managerModules().shaOfFile(fileTs)

        if key is not None or idM == "sys":
            tor = FLTranslator(self, "%s_%s" % (idM, lang), lang == "multilang")

            if tor.loadTsContent(key):
                return tor

        return self.createModTranslator(idM, "es") if loadDefault else None

    def modules(self) -> Any:
        """Return loaded modules."""
        return project.modules

    def commaSeparator(self) -> Any:
        """Return comma separator for floating points on current language."""
        return self.comma_separator

    def tmp_dir(self) -> Any:
        """Return temporary folder."""
        return project.tmpdir

    def transactionLevel(self):
        """Return number of concurrent transactions."""
        return project.conn.transactionLevel()

    def version(self):
        """Return app version."""
        return project.version


"""
class FLPopuWarn(QtWidgets.QWhatsThis):

    script_calls_ = []

    def __init__(self, parent):
        self.script_calls_ = []
        super(FLPopuWarn, self).__init__(parent)

    def clicked(self, href):
        if href:

            from pineboolib import pncontrolsfactory

            if href.find(":") > -1:
                h = href.split(":")[1]
            if h.find(".") == 1:
                pncontrolsfactury.aqApp.call(h.split(".")[1], self.script_calls_[href], h.split(".")[0])
            else:
                pncontrolsfacotry.aqApp.call(h, self.script_calls_[href], None)
"""


# aqApp = FLApplication()
aqApp: FLApplication
