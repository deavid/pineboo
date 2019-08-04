"""Main module for starting up Pineboo."""
import gc
import sys
from optparse import Values
from typing import List, Type
from types import TracebackType

from PyQt5 import QtCore, QtWidgets

from pineboolib import logging
from pineboolib.core.utils.utils_base import is_deployed
from pineboolib.core.settings import config, settings
from pineboolib.loader.dlgconnect.conn_dialog import show_connection_dialog
from pineboolib.loader.options import parse_options
from pineboolib.loader.dgi import load_dgi
from pineboolib.loader.connection import config_dbconn, connect_to_db
from pineboolib.loader.connection import DEFAULT_SQLITE_CONN, IN_MEMORY_SQLITE_CONN

from pineboolib.application import project  # FIXME: next time, proper singleton
from pineboolib.application.parsers.qsaparser import pytnyzer

logger = logging.getLogger(__name__)


def startup_no_X() -> None:
    """Start Pineboo with no GUI."""
    startup(enable_gui=False)


def startup(enable_gui: bool = None) -> None:
    """Start up pineboo."""
    # FIXME: No hemos cargado pineboo aún. No se pueden usar métodos internos.
    from pineboolib.core.utils.check_dependencies import check_dependencies_cli

    if not check_dependencies_cli(
        {"ply": "python3-ply", "PyQt5.QtCore": "python3-pyqt5", "Python": "Python"}
    ):
        sys.exit(32)

    MIN_PYTHON = (3, 6)
    if sys.version_info < MIN_PYTHON:
        sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)

    options = parse_options()
    if enable_gui is not None:
        options.enable_gui = enable_gui
    trace_loggers: List[str] = []
    if options.trace_loggers:
        trace_loggers = options.trace_loggers.split(",")

    init_logging(logtime=options.log_time, loglevel=options.loglevel, trace_loggers=trace_loggers)

    if options.enable_profiler:
        ret = exec_main_with_profiler(options)
    else:
        ret = exec_main(options)
    # setup()
    # exec_()
    gc.collect()
    print("Closing Pineboo...")
    if ret:
        sys.exit(ret)
    else:
        sys.exit(0)


def init_logging(
    loglevel: int = logging.INFO, logtime: bool = False, trace_loggers: List[str] = []
) -> None:
    """Initialize pineboo logging."""
    # ---- LOGGING -----
    log_format = "%(levelname)s: %(name)s: %(message)s"

    if logtime:
        log_format = "%(asctime)s - %(levelname)s: %(name)s: %(message)s"

    app_loglevel = logging.TRACE if trace_loggers else loglevel
    if trace_loggers:
        logging.Logger.set_pineboo_default_level(loglevel)

    logging.basicConfig(format=log_format, level=app_loglevel)
    # logger.info("LOG LEVEL: %s", loglevel)
    disable_loggers = ["PyQt5.uic.uiparser", "PyQt5.uic.properties", "blib2to3.pgen2.driver"]
    for loggername in disable_loggers:
        modlogger = logging.getLogger(loggername)
        modlogger.setLevel(logging.WARN)

    for loggername in trace_loggers:
        modlogger = logging.getLogger(loggername)
        modlogger.setLevel(logging.TRACE)


def exec_main_with_profiler(options: Values) -> int:
    """Enable profiler."""
    import cProfile
    import pstats
    import io
    from pstats import SortKey  # type: ignore

    pr = cProfile.Profile()
    pr.enable()
    ret = exec_main(options)
    pr.disable()
    s = io.StringIO()
    sortby = SortKey.TIME
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats(40)
    print(s.getvalue())
    return ret


def init_cli(catch_ctrl_c: bool = True) -> None:
    """Initialize singletons, signal handling and exception handling."""

    def _excepthook(
        type_: Type[BaseException], value: BaseException, traceback: TracebackType
    ) -> None:
        import traceback as pytback

        pytback.print_exception(type_, value, traceback)

    # PyQt 5.5 o superior aborta la ejecución si una excepción en un slot()
    # no es capturada dentro de la misma; el programa falla con SegFault.
    # Aunque esto no debería ocurrir, y se debería prevenir lo máximo posible
    # es bastante incómodo y genera problemas graves para detectar el problema.
    # Agregamos sys.excepthook para controlar esto y hacer que PyQt5 no nos
    # dé un segfault, aunque el resultado no sea siempre correcto:
    sys.excepthook = _excepthook
    # -------------------
    if catch_ctrl_c:
        # Fix Control-C / KeyboardInterrupt for PyQt:
        import signal

        signal.signal(signal.SIGINT, signal.SIG_DFL)

    # FIXME: Order of import is REALLY important here. FIX.
    # from pineboolib.fllegacy.aqsobjects import aqsobjectfactory
    #
    # aqsobjectfactory.AQUtil = aqsobjectfactory.AQUtil_class()
    # aqsobjectfactory.AQS = aqsobjectfactory.AQS_class()

    from pineboolib.fllegacy import flapplication

    flapplication.aqApp = flapplication.FLApplication()

    from pineboolib.qsa import qsa

    qsa.aqApp = flapplication.aqApp
    # from pineboolib import pncontrolsfactory
    #
    # pncontrolsfactory.System = pncontrolsfactory.System_class()
    # pncontrolsfactory.qsa_sys = pncontrolsfactory.SysType()


def init_gui() -> None:
    """Create GUI singletons."""
    from pineboolib.plugins.mainform.eneboo import eneboo
    from pineboolib.plugins.mainform.eneboo_mdi import eneboo_mdi

    eneboo.mainWindow = eneboo.MainForm()
    eneboo_mdi.mainWindow = eneboo_mdi.MainForm()


def setup_gui(app: QtCore.QCoreApplication, options: Values) -> None:
    """Configure GUI app."""
    from pineboolib.core.utils.utils_base import filedir
    from pineboolib.application.utils.mobilemode import is_mobile_mode
    from PyQt5 import QtGui

    noto_fonts = [
        "NotoSans-BoldItalic.ttf",
        "NotoSans-Bold.ttf",
        "NotoSans-Italic.ttf",
        "NotoSans-Regular.ttf",
    ]
    for fontfile in noto_fonts:
        QtGui.QFontDatabase.addApplicationFont(filedir("../share/fonts/Noto_Sans", fontfile))

    styleA = config.value("application/style", None)
    if styleA is None:
        styleA = "Fusion"

    app.setStyle(styleA)

    fontA = config.value("application/font", None)
    if fontA is None:
        if is_mobile_mode():
            font = QtGui.QFont("Noto Sans", 14)
        else:
            font = QtGui.QFont("Noto Sans", 9)
        font.setBold(False)
        font.setItalic(False)
    else:
        # FIXME: FLSettings.readEntry does not return an array
        font = QtGui.QFont(fontA[0], int(fontA[1]), int(fontA[2]), fontA[3] == "true")

    app.setFont(font)


def init_testing() -> None:
    """Initialize Pineboo for testing purposes."""

    if project._conn is not None:
        # Assume already initialized, return without doing anything
        # Tests may call this several times, so we have to take it into account.
        return
    qapp = QtWidgets.QApplication(sys.argv + ["-platform", "offscreen"])

    init_logging()  # NOTE: Use pytest --log-level=0 for debug
    init_cli(catch_ctrl_c=False)

    pytnyzer.STRICT_MODE = False
    project.load_version()
    project.setDebugLevel(1000)
    project.set_app(qapp)
    _DGI = load_dgi("qt", None)
    project.init_dgi(_DGI)
    conn = connect_to_db(IN_MEMORY_SQLITE_CONN)
    project.init_conn(connection=conn)
    project.no_python_cache = True
    project.run()

    # Necesario para que funcione isLoadedModule ¿es este el mejor sitio?
    project.conn.managerModules().loadIdAreas()
    project.conn.managerModules().loadAllIdModules()

    project.load_modules()


def exec_main(options: Values) -> int:
    """
    Exec main program.

    Handles optionlist and help.
    Also initializes all the objects
    """
    # FIXME: This function should not initialize the program

    # -------------------

    # import pineboolib.pnapplication
    # from pineboolib.core.utils.utils_base import filedir
    # from pineboolib.pnsqldrivers import PNSqlDrivers

    init_cli()

    # TODO: Refactorizar función en otras más pequeñas

    pytnyzer.STRICT_MODE = False

    project.load_version()
    project.setDebugLevel(options.debug_level)

    project.options = options
    if options.enable_gui:
        project.set_app(QtWidgets.QApplication(sys.argv))
        project.app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
        setup_gui(project.app, options)
    else:
        project.set_app(QtWidgets.QApplication(sys.argv + ["-platform", "offscreen"]))

    if options.trace_debug:
        from pineboolib.core.utils.utils_base import traceit

        # "sys.settrace" function could lead to arbitrary code execution
        sys.settrace(traceit)  # noqa: DUO111

    if options.trace_signals:
        from .utils import monkey_patch_connect

        monkey_patch_connect()

    if options.enable_dbadmin:
        config.set_value("application/dbadmin_enabled", True)

    if options.enable_quick:
        config.set_value("application/dbadmin_enabled", False)

    if is_deployed():
        logging.basicConfig(stream=sys.stdout, level=logging.INFO)
        from pineboolib.core.utils.utils_base import download_files

        download_files()

    _DGI = load_dgi(options.dgi, options.dgi_parameter)
    if options.enable_gui:
        init_gui()

    if _DGI.useDesktop() and not options.enable_gui:
        logger.info(
            "Selected DGI <%s> is not compatible with <pineboo-core>. Use <pineboo> instead"
            % options.dgi
        )

    if not _DGI.useDesktop() and options.enable_gui:
        logger.info(
            "Selected DGI <%s> does not need graphical interface. Use <pineboo-core> for better results"
            % options.dgi
        )

    if not _DGI.useMLDefault():
        # When a particular DGI doesn't want the standard init, we stop loading here
        # and let it take control of the remaining pieces.
        return _DGI.alternativeMain(options)

    configdb = config_dbconn(options)
    logger.debug(configdb)
    project.init_dgi(_DGI)

    if not configdb and _DGI.useDesktop() and _DGI.localDesktop():
        if not _DGI.mobilePlatform():

            configdb = show_connection_dialog(project.app)
        else:
            configdb = DEFAULT_SQLITE_CONN

    if not configdb:
        raise ValueError("No connection given. Nowhere to connect. Cannot start.")

    conn = connect_to_db(configdb)
    project.init_conn(connection=conn)

    settings.set_value("DBA/lastDB", conn.DBName())

    project.no_python_cache = options.no_python_cache

    if options.test:
        return 0 if project.test() else 1

    if _DGI.useDesktop():
        # FIXME: What is happening here? Why dynamic load?
        import importlib  # FIXME: Delete dynamic import and move this code between Project and DGI plugins

        project.main_form = (
            importlib.import_module(
                "pineboolib.plugins.mainform.%s.%s"
                % (project.main_form_name, project.main_form_name)
            )
            if _DGI.localDesktop()
            else _DGI.mainForm()
        )
        project.main_window = getattr(project.main_form, "mainWindow", None)
        main_form_ = getattr(project.main_form, "MainForm", None)
        if main_form_ is not None:
            main_form_.setDebugLevel(options.debug_level)

    project.message_manager().send("splash", "show")

    project.run()

    if not project.conn.conn:
        logger.warning("No connection was provided. Aborting Pineboo load.")
        return -99

    if not config.value("ebcomportamiento/orm_parser_disabled", False):
        from pineboolib.application.parsers.mtdparser.pnmtdparser import mtd_parse

        for table in project.conn.tables("Tables"):
            mtd_parse(table)

    # Necesario para que funcione isLoadedModule ¿es este el mejor sitio?
    project.conn.managerModules().loadIdAreas()
    project.conn.managerModules().loadAllIdModules()

    project.load_modules()

    # FIXME: move this code to pineboo.application
    from pineboolib.fllegacy.flapplication import aqApp

    aqApp.loadTranslations()

    from .init_project import init_project

    ret = init_project(
        _DGI, options, project, project.main_form if _DGI.useDesktop() else None, project.app
    )
    return ret
