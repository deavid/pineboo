import gc
import sys
import traceback
import logging

from pineboolib.core.utils import is_deployed
from pineboolib.application.project import Project
from pineboolib.core.settings import config

from .dgi import load_dgi

logger = logging.getLogger(__name__)


def startup():
    # FIXME: No hemos cargado pineboo aún. No se pueden usar métodos internos.
    # from pineboolib.utils import checkDependencies
    # checkDependencies({"ply": "python3-ply", "PyQt5.QtCore": "python3-pyqt5", "Python": "Python"})

    MIN_PYTHON = (3, 6)
    if sys.version_info < MIN_PYTHON:
        sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)

    from .options import parse_options

    options = parse_options()

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
    # import pineboolib.pnapplication
    # import pineboolib.dlgconnect
    # from pineboolib.utils import filedir
    # from pineboolib.pnsqldrivers import PNSqlDrivers

    # FIXME: This function should not initialize the program

    # TODO: Refactorizar función en otras más pequeñas

    if is_deployed():
        logging.basicConfig(stream=sys.stdout, level=logging.INFO)
        from pineboolib.utils_base import download_files

        download_files()

    if options.trace_debug:
        from pineboolib.utils import traceit

        sys.settrace(traceit)
    if options.trace_signals:
        from .utils import monkey_patch_connect

        monkey_patch_connect()

    project = Project()
    _DGI = load_dgi(options.dgi, options.dgi_parameter)
    project.init_dgi(_DGI)
    project.no_python_cache = options.no_python_cache

    if options.test:
        project.test()
        return

    if options.enable_dbadmin:
        config.set_value("application/dbadmin_enabled", True)

    if options.enable_quick:
        config.set_value("application/dbadmin_enabled", False)

    from .create_app import create_app

    app = create_app(_DGI)

    if _DGI.useDesktop():
        # FIXME: What is happening here? Why dynamic load?
        project.main_form = (
            importlib.import_module("pineboolib.plugins.mainform.%s.%s" % (project.main_form_name, project.main_form_name))
            if _DGI.localDesktop()
            else _DGI.mainForm()
        )
        project.main_window = project.main_form.mainWindow

    project.setDebugLevel(options.debug_level)
    if _DGI.useDesktop():
        project.main_form.MainForm.setDebugLevel(options.debug_level)

    if options.project:  # FIXME: --project debería ser capaz de sobreescribir algunas opciones
        if not options.project.endswith(".xml"):
            options.project += ".xml"
        prjpath = filedir("../profiles", options.project)
        if not os.path.isfile(prjpath):
            logger.warning("el proyecto %s no existe." % options.project)
        else:
            if not project.load(prjpath):
                return
    elif options.connection:
        user, passwd, driver_alias, host, port, dbname = translate_connstring(options.connection)
        project.load_db(dbname, host, port, user, passwd, driver_alias)
    elif _DGI.useDesktop() and _DGI.localDesktop():
        if not _DGI.mobilePlatform():
            show_connection_dialog(project, app)
        else:
            project.load_db("pineboo.sqlite3", None, None, None, None, "SQLite3 (SQLITE3)")

    # Cargando spashscreen
    # Create and display the splash screen
    if _DGI.localDesktop() and not options.action:
        splash = show_splashscreen(project)
        _DGI.processEvents()
    else:
        splash = None

    project._splash = splash
    project.run()
    if project.conn.conn is False:
        logger.warning("No connection was provided. Aborting Pineboo load.")
    else:
        init_project(_DGI, splash, options, project, project.main_form if _DGI.useDesktop() else None, app)
