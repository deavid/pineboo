import gc
import sys
import traceback
import logging

from pineboolib.core.utils import is_deployed
from pineboolib.core.settings import config
from .dgi import load_dgi

logger = logging.getLogger(__name__)


def startup():
    # FIXME: No hemos cargado pineboo aún. No se pueden usar métodos internos.
    # from pineboolib.core.utils.utils_base import check_dependencies
    # check_dependencies({"ply": "python3-ply", "PyQt5.QtCore": "python3-pyqt5", "Python": "Python"})

    MIN_PYTHON = (3, 6)
    if sys.version_info < MIN_PYTHON:
        sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)

    from .options import parse_options

    options = parse_options()

    ret = exec_main(options)
    # setup()
    # exec_()
    gc.collect()
    print("Closing Pineboo...")
    if ret:
        sys.exit(ret)
    else:
        sys.exit(0)


def exec_main(options):
    """Exec main program.

    Handles optionlist and help.
    Also initializes all the objects
    """
    # PyQt 5.5 o superior aborta la ejecución si una excepción en un slot()
    # no es capturada dentro de la misma; el programa falla con SegFault.
    # Aunque esto no debería ocurrir, y se debería prevenir lo máximo posible
    # es bastante incómodo y genera problemas graves para detectar el problema.
    # Agregamos sys.excepthook para controlar esto y hacer que PyQt5 no nos
    # dé un segfault, aunque el resultado no sea siempre correcto:
    sys.excepthook = traceback.print_exception
    # -------------------

    # Corregir Control-C:
    import signal

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    # -------------------

    # import pineboolib.pnapplication
    # from pineboolib.core.utils.utils_base import filedir
    # from pineboolib.pnsqldrivers import PNSqlDrivers

    # FIXME: This function should not initialize the program

    # TODO: Refactorizar función en otras más pequeñas

    if options.trace_debug:
        from pineboolib.core.utils.utils_base import traceit

        sys.settrace(traceit)
    if options.trace_signals:
        from .utils import monkey_patch_connect

        monkey_patch_connect()

    if is_deployed():
        logging.basicConfig(stream=sys.stdout, level=logging.INFO)
        from pineboolib.core.utils.utils_base import download_files

        download_files()

    _DGI = load_dgi(options.dgi, options.dgi_parameter)

    from .create_app import create_app

    app = create_app(_DGI, options)

    from .connection import config_dbconn, connect_to_db, DEFAULT_SQLITE_CONN

    configdb = config_dbconn(options)

    if not configdb and _DGI.useDesktop() and _DGI.localDesktop():
        if not _DGI.mobilePlatform():
            from .conn_dialog import show_connection_dialog

            configdb = show_connection_dialog(app)
        else:
            configdb = DEFAULT_SQLITE_CONN

    if not configdb:
        raise ValueError("No connection given. Nowhere to connect. Cannot start.")

    import pineboolib

    project = pineboolib.project  # FIXME: next time, proper singleton
    project.setDebugLevel(options.debug_level)
    project.init_dgi(_DGI)
    project.init_conn(connection=connect_to_db(configdb))
    project.no_python_cache = options.no_python_cache

    if options.test:
        project.test()
        return

    if options.enable_dbadmin:
        config.set_value("application/dbadmin_enabled", True)

    if options.enable_quick:
        config.set_value("application/dbadmin_enabled", False)

    if _DGI.useDesktop():
        # FIXME: What is happening here? Why dynamic load?
        import importlib  # FIXME: Delete dynamic import and move this code between Project and DGI plugins

        project.main_form = (
            importlib.import_module("pineboolib.plugins.mainform.%s.%s" % (project.main_form_name, project.main_form_name))
            if _DGI.localDesktop()
            else _DGI.mainForm()
        )
        project.main_window = project.main_form.mainWindow
        project.main_form.MainForm.setDebugLevel(options.debug_level)

    # Cargando spashscreen
    # Create and display the splash screen
    # if _DGI.localDesktop() and not options.action:
    #     splash = show_splashscreen(project)
    #     _DGI.processEvents()
    # else:
    #     splash = None
    splash = None

    project._splash = splash
    project.run()
    if project.conn.conn is False:
        logger.warning("No connection was provided. Aborting Pineboo load.")
    else:
        from .init_project import init_project

        init_project(_DGI, splash, options, project, project.main_form if _DGI.useDesktop() else None, app)
