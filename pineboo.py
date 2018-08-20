#!/usr/bin/python3 -u
# -*# -*- coding: utf-8 -*-
"""Start the application and give control to pineboolib.pnapplication().

Bootstrap. Se encarga de inicializar la aplicación y ceder el control a
pineboolib.pnapplication(); para ello acepta los parámetros necesarios de consola
y configura el programa adecuadamente.
"""
import sys
import re
import traceback
import os
import gc
from optparse import OptionParser
import signal
import importlib
import logging
from pineboolib.fllegacy.FLSettings import FLSettings


logger = logging.getLogger("pineboo.__main__")
signal.signal(signal.SIGINT, signal.SIG_DFL)


def startup_check_dependencies():
    """Do a preemptive import of the libraries needed and handle errors in a user friendly way."""
    from pineboolib.utils import checkDependencies

    dict_ = {"ply": "python3-ply", "PyQt5.QtCore": "python3-pyqt5", "barcode": "python-barcode", "PIL": "Pillow", "z3c.rml": "z3c.rml"}
    checkDependencies(dict_)

    if sys.version_info[0] < 3:
        logger.error("Tienes que usar Python 3 o superior.")
        sys.exit(32)


def translate_connstring(connstring):
    """Translate a DSN connection string into user, pass, etc.

    Acepta un parámetro "connstring" que tenga la forma user@host/dbname
    y devuelve todos los parámetros por separado. Tiene en cuenta los
    valores por defecto y las diferentes formas de abreviar que existen.
    """
    user = "postgres"
    passwd = None
    host = "127.0.0.1"
    port = "5432"
    dbname = ""
    driver_alias = ""
    user_pass = None
    host_port = None
    try:
        uphpstring = connstring[:connstring.rindex("/")]
    except ValueError:
        dbname = connstring
        if not re.match(r"\w+", dbname):
            raise ValueError("base de datos no valida")
        return user, passwd, host, port, dbname
    dbname = connstring[connstring.rindex("/") + 1:]
    conn_list = [None, None] + uphpstring.split("@")
    user_pass, host_port = conn_list[-2], conn_list[-1]

    if user_pass:
        user_pass = user_pass.split(":") + [None, None, None]
        user, passwd, driver_alias = user_pass[0], user_pass[1] or passwd, user_pass[2] or driver_alias
        if user_pass[3]:
            raise ValueError(
                "La cadena de usuario debe tener el formato user:pass:driver.")

    if host_port:
        host_port = host_port.split(":") + [None]
        host, port = host_port[0], host_port[1] or port
        if host_port[2]:
            raise ValueError("La cadena de host debe ser host:port.")

    if not re.match(r"\w+", user):
        raise ValueError("Usuario no valido")
    if not re.match(r"\w+", dbname):
        raise ValueError("base de datos no valida")
    if not re.match(r"\d+", port):
        raise ValueError("puerto no valido")
    logger.debug("user:%s, passwd:%s, driver_alias:%s, host:%s, port:%s, dbname:%s",
                 user, "*" * len(passwd), driver_alias, host, port, dbname)
    return user, passwd, driver_alias, host, port, dbname


def parse_options():
    """Load and parse options."""
    parser = OptionParser()
    parser.add_option("-l", "--load", dest="project",
                      help="load projects/PROJECT.xml and run it", metavar="PROJECT")
    parser.add_option("-c", "--connect", dest="connection",
                      help="connect to database with user and password.", metavar="user:passwd:driver_alias@host:port/database")
    parser.add_option('-v', '--verbose', action='count', default=2,
                      help="increase verbosity level")  # default a 2 para ver los logger.info, 1 no los muestra
    parser.add_option("-q", "--quiet",
                      action='count', default=0,
                      help="decrease verbosity level")
    parser.add_option("--trace-debug",
                      action="store_true", dest="trace_debug", default=False,
                      help="Write lots of trace information to stdout")
    parser.add_option("--log-time",
                      action="store_true", dest="log_time", default=False,
                      help="Add timestamp to logs")
    parser.add_option("--trace-signals",
                      action="store_true", dest="trace_signals", default=False,
                      help="Wrap up every signal, connect and emit, and give useful tracebacks")
    parser.add_option("-a", "--action", dest="action",
                      help="load action", metavar="ACTION")
    parser.add_option("--no-python-cache",
                      action="store_true", dest="no_python_cache", default=False,
                      help="Always translate QS to Python")
    parser.add_option("--preload",
                      action="store_true", dest="preload", default=False,
                      help="Load everything. Then exit. (Populates Pineboo cache)")
    parser.add_option("--force-load",
                      dest="forceload", default=None, metavar="ACTION",
                      help="Preload actions containing string ACTION without caching. Useful to debug pythonyzer")
    parser.add_option("--dgi",
                      dest="dgi", default="qt",
                      help="Change the gdi mode by default", metavar="DGI")
    parser.add_option("--dgi_parameter",
                      dest="dgi_parameter",
                      help="Change the gdi mode by default", metavar="DGIPARAMETER")
    parser.add_option("--test",
                      action="store_true", dest="test", default=False,
                      help="Launch all test")

    (options, args) = parser.parse_args()

    # ---- OPTIONS POST PROCESSING -----
    if options.forceload:
        options.no_python_cache = True
        options.preload = True

    options.loglevel = 30 + (options.quiet - options.verbose) * 5
    options.debug_level = 200  # 50 - (options.quiet - options.verbose) * 25

    # ---- LOGGING -----
    if options.loglevel > 30:
        log_format = '%(name)s:%(levelname)s: %(message)s'
    else:
        log_format = '%(levelname)s: %(message)s'

    if options.log_time:
        log_format = '%(asctime)s - %(name)s:%(levelname)s: %(message)s'

    addLoggingLevel('TRACE', logging.DEBUG - 5)
    addLoggingLevel('NOTICE', logging.INFO - 5)
    addLoggingLevel('HINT', logging.INFO - 2)
    addLoggingLevel('MESSAGE', logging.WARN - 5)

    logging.basicConfig(format=log_format, level=options.loglevel)
    logger.debug("LOG LEVEL: %s  DEBUG LEVEL: %s",
                 options.loglevel, options.debug_level)

    disable_loggers = [
        "PyQt5.uic.uiparser",
        "PyQt5.uic.properties"]
    for loggername in disable_loggers:
        modlogger = logging.getLogger(loggername)
        modlogger.setLevel(logging.WARN)

    return options


def load_dgi(name):
    """Load a DGI module dynamically."""
    modname = "dgi_%s" % name
    modpath = "pineboolib.plugins.dgi.%s" % modname
    try:
        dgi_pymodule = importlib.import_module(modpath)
    except ImportError:
        raise ImportError("No se ha encontrado el módulo DGI %s" % modpath)

    dgi_entrypoint = getattr(dgi_pymodule, modname, None)
    if dgi_entrypoint is None:
        raise ImportError(
            "Fallo al cargar el punto de entrada al módulo DGI %s" % modpath)

    try:
        dgi = dgi_entrypoint()  # FIXME: Necesitamos ejecutar código dinámico tan pronto?
    except Exception:
        logger.exception(
            "Error inesperado al cargar el módulo DGI %s" % modpath)
        sys.exit(32)

    logger.info("DGI loaded: %s", name)

    return dgi


def create_app(DGI):
    """Create a MainForm using the DGI or the core."""
    from PyQt5 import QtGui, QtWidgets
    from pineboolib.utils import filedir
    import pineboolib
    app = QtWidgets.QApplication(sys.argv)
    if DGI.localDesktop():

        noto_fonts = [
            "NotoSans-BoldItalic.ttf",
            "NotoSans-Bold.ttf",
            "NotoSans-Italic.ttf",
            "NotoSans-Regular.ttf"]
        for fontfile in noto_fonts:
            QtGui.QFontDatabase.addApplicationFont(
                filedir("../share/fonts/Noto_Sans", fontfile))

        sett_ = FLSettings()

        styleA = sett_.readEntry("application/style", None)
        if styleA is None:
            styleA = "Fusion"

        QtWidgets.QApplication.setStyle(styleA)

        fontA = sett_.readEntry("application/font", None)
        if fontA is None:
            font = QtGui.QFont('Noto Sans', 9)
            font.setBold(False)
            font.setItalic(False)
        else:
            font = QtGui.QFont(fontA[0], int(fontA[1]), int(fontA[2]), fontA[3] == "true")

        QtWidgets.QApplication.setFont(font)

        if DGI.mobilePlatform():
            pineboolib.pnapplication.Project.mainFormName = "Mobile"

        # Es necesario importarlo a esta altura, QApplication tiene que ser
        # construido antes que cualquier widget
        mainForm = importlib.import_module("pineboolib.plugins.mainform.%s.%s" % (
            pineboolib.pnapplication.Project.mainFormName.lower(), pineboolib.pnapplication.Project.mainFormName.lower()))
    else:
        mainForm = DGI.mainForm()
    # mainForm = getattr(module_, "MainForm")()
    # from pineboolib import mainForm
    return app, mainForm


def show_connection_dialog(project, app):
    """Show the connection dialog, and configure the project accordingly."""
    from pineboolib.dlgconnect import dlgconnect
    connection_window = dlgconnect.DlgConnect(project._DGI)
    connection_window.load()
    connection_window.show()
    ret = app.exec_()
    if connection_window.close():
        # if connection_window.ruta:
        #    prjpath = connection_window.ruta
        #    print("Cargando desde ruta %r " % prjpath)
        #    project.load(prjpath)
        # elif connection_window.database:
        if getattr(connection_window, "database", None):
            logger.info("Cargando credenciales")
            project.deleteCache = FLSettings().readBoolEntry("ebcomportamiento/deleteCache", False)
            project.parseProject = FLSettings().readBoolEntry("ebcomportamiento/parseProject", False)
            project.load_db(connection_window.database, connection_window.hostname, connection_window.portnumber,
                            connection_window.username, connection_window.password, connection_window.driveralias)
        else:
            sys.exit(ret)


def show_splashscreen(project):
    """Show a splashscreen to inform keep the user busy while Pineboo is warming up."""
    from PyQt5 import QtGui, QtCore, QtWidgets
    from pineboolib.utils import filedir
    splash_path = filedir("../share/splashscreen/splash_%s.png" % project.dbname)
    if not os.path.exists(splash_path):
        splash_path = filedir("../share/splashscreen/splash.png")

    splash_pix = QtGui.QPixmap(splash_path)
    splash = QtWidgets.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()

    frameGm = splash.frameGeometry()
    screen = QtWidgets.QApplication.desktop().screenNumber(
        QtWidgets.QApplication.desktop().cursor().pos())
    centerPoint = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
    frameGm.moveCenter(centerPoint)
    splash.move(frameGm.topLeft())
    return splash


def main():
    """Execute main program.

    Handles optionlist and help.
    Also initializes all the objects
    """
    import pineboolib.pnapplication
    import pineboolib.dlgconnect
    from pineboolib.utils import download_files, filedir

    # FIXME: This function should not initialize the program

    # TODO: Refactorizar función en otras más pequeñas
    options = parse_options()

    _DGI = load_dgi(options.dgi)
    if _DGI.isDeployed():
        download_files()

    pineboolib.no_python_cache = options.no_python_cache

    if options.trace_debug:
        from pineboolib.utils import traceit
        sys.settrace(traceit)
    if options.trace_signals:
        monkey_patch_connect()

    if options.dgi_parameter:
        _DGI.setParameter(options.dgi_parameter)

    if not _DGI.useMLDefault():
        return _DGI.alternativeMain(options)

    if _DGI.useDesktop():
        app, mainForm = create_app(_DGI)

    project = pineboolib.pnapplication.Project(_DGI)
    project.setDebugLevel(options.debug_level)
    if _DGI.useDesktop():
        mainForm.MainForm.setDebugLevel(options.debug_level)

    if options.project:  # FIXME: --project debería ser capaz de sobreescribir algunas opciones
        if not options.project.endswith(".xml"):
            options.project += ".xml"
        prjpath = filedir("../projects", options.project)
        if not os.path.isfile(prjpath):
            logger.warn("el proyecto %s no existe." % options.project)
        else:
            project.load(prjpath)
    elif options.connection:
        user, passwd, driver_alias, host, port, dbname = translate_connstring(
            options.connection)
        project.load_db(dbname, host, port, user, passwd, driver_alias)
    elif _DGI.useDesktop() and _DGI.localDesktop() and not _DGI.mobilePlatform():
        show_connection_dialog(project, app)
    elif _DGI.useDesktop() and _DGI.localDesktop() and _DGI.mobilePlatform():
        project.load_db("pineboo.sqlite3", None, None, None, None, "SQLite3")

    # Cargando spashscreen
    # Create and display the splash screen
    if _DGI.useDesktop() and _DGI.localDesktop():
        splash = show_splashscreen(project)
    else:
        splash = None

    project._splash = splash
    project.run()
    if project.conn.conn is False:
        logger.warn("No connection was provided. Aborting Pineboo load.")
    else:
        # return main()

        init_project(_DGI, splash, options, project, mainForm, app)


def preload_actions(project, forceload=None):
    """Preload actions for warming up the pythonizer cache.

    forceload: When passed an string, it filters and loads all
        actions that match "*forceload*". If None, all actions
        are loaded.
    """
    logger.info("Precarga ...")
    for action in project.actions:
        if forceload and action not in forceload:
            continue
        logger.info("* * * Cargando acción %s . . . " % action)
        try:
            project.actions[action].load()
        except Exception:
            print(traceback.format_exc())
            project.conn.conn.rollback()
    sys.exit(0)


def init_project(DGI, splash, options, project, mainForm, app):
    """Initialize the project and start it."""
    from PyQt5 import QtCore
    if DGI.useDesktop() and DGI.localDesktop():
        splash.showMessage("Iniciando proyecto ...", QtCore.Qt.AlignLeft, QtCore.Qt.white)
    logger.info("Iniciando proyecto ...")

    # Necesario para que funcione isLoadedModule ¿es este el mejor sitio?
    project.conn.manager().db_.managerModules().loadAllIdModules()

    objaction = None
    for k, module in list(project.modules.items()):
        try:
            if not module.load():
                continue
        except Exception as err:
            logger.error("%s: %s", err.__class__.__name__, str(err))
            continue
        if options.action in module.actions:
            objaction = module.actions[options.action]

    if options.action and not objaction:
        raise ValueError("Action name %s not found" % options.action)

    if DGI.localDesktop():
        splash.showMessage("Creando interfaz ...", QtCore.Qt.AlignLeft, QtCore.Qt.white)

    logger.info("Creando interfaz ...")
    main_window = mainForm.mainWindow
    main_window.load()
    ret = 0

    if options.preload:
        preload_actions(project, options.forceload)

    if options.test:
        print(project.test())
        return

    if DGI.localDesktop():
        splash.showMessage("Abriendo interfaz ...", QtCore.Qt.AlignLeft, QtCore.Qt.white)
    logger.info("Abriendo interfaz ...")
    main_window.show()
    project.call("sys.iface.init()", [], None, True)
    if DGI.localDesktop():
        splash.showMessage("Listo ...", QtCore.Qt.AlignLeft, QtCore.Qt.white)
        main_window.activateWindow()
        QtCore.QTimer.singleShot(1000, splash.hide)

    if objaction:
        objaction.openDefaultForm()

    if DGI.localDesktop():
        ret = app.exec_()
    else:
        ret = DGI.exec_()

    mainForm.mainWindow = None
    del main_window
    del project
    return ret


def monkey_patch_connect():
    """Patch Qt5 signal/event functions for tracing them.

    This is not stable and should be used with care
    """
    from PyQt5 import QtCore
    logger.warn(
        "--trace-signals es experimental. Tiene problemas de memoria y falla en llamadas con un argumento (False)")
    logger.warn(
        "... se desaconseja su uso excepto para depurar. Puede cambiar el comportamiento del programa.")

    class BoundSignal():
        _CONNECT = QtCore.pyqtBoundSignal.connect
        _EMIT = QtCore.pyqtBoundSignal.emit
        _LAST_EMITTED_SIGNAL = {}

        def slot_decorator(self, slot, connect_stack):
            selfid = repr(self)

            def decorated_slot(*args):
                ret = None
                if len(args) == 1 and args[0] is False:
                    args = []
                try:
                    # print("Calling slot: %r %r" % (slot, args))
                    ret = slot(*args)
                except Exception:
                    print("Unhandled exception in slot %r (%r): %r" %
                          (slot, self, args))
                    print("-- Connection --")
                    print(traceback.format_list(connect_stack)[-2].rstrip())
                    last_emit_stack = BoundSignal._LAST_EMITTED_SIGNAL.get(
                        selfid, None)
                    if last_emit_stack:
                        print("-- Last signal emmitted --")
                        print(traceback.format_list(
                            last_emit_stack)[-2].rstrip())
                    print("-- Slot traceback --")
                    print(traceback.format_exc())
                return ret
            return decorated_slot

        def connect(self, slot, type_=0, no_receiver_check=False):
            """Proxy a connection to the original connect in the Qt library.

            This function wraps on top of the original Qt.connect so everything
            is logged.

            slot is either a Python callable or another signal.
            type is a Qt.ConnectionType. (default Qt.AutoConnection = 0)
            no_receiver_check is True to disable the check that the receiver's C++
            instance still exists when the signal is emitted.
            """
            clname = getattr(getattr(slot, "__class__", {}),
                             "__name__", "not a class")
            # print("Connect: %s -> %s" % (type(self), slot))
            if clname == "method":
                stack = traceback.extract_stack()
                newslot = BoundSignal.slot_decorator(self, slot, stack)
            else:
                newslot = slot
            return BoundSignal._CONNECT(self, newslot, type_, no_receiver_check)

        def emit(self, *args):
            """Proxy original Qt Emit function for tracing signal emits."""
            # print("Emit: %s :: %r" % (self, args))
            stack = traceback.extract_stack()
            # print(traceback.format_list(stack)[-2].rstrip())
            BoundSignal._LAST_EMITTED_SIGNAL[repr(self)] = stack
            return BoundSignal._EMIT(self, *args)
    QtCore.pyqtBoundSignal.connect = BoundSignal.connect
    QtCore.pyqtBoundSignal.emit = BoundSignal.emit


def addLoggingLevel(levelName, levelNum, methodName=None):
    """
    Comprehensively adds a new logging level to the `logging` module and the
    currently configured logging class.

    `levelName` becomes an attribute of the `logging` module with the value
    `levelNum`. `methodName` becomes a convenience method for both `logging`
    itself and the class returned by `logging.getLoggerClass()` (usually just
    `logging.Logger`). If `methodName` is not specified, `levelName.lower()` is
    used.

    To avoid accidental clobberings of existing attributes, this method will
    raise an `AttributeError` if the level name is already an attribute of the
    `logging` module or if the method name is already present

    Example
    -------
    >>> addLoggingLevel('TRACE', logging.DEBUG - 5)
    >>> logging.getLogger(__name__).setLevel("TRACE")
    >>> logging.getLogger(__name__).trace('that worked')
    >>> logging.trace('so did this')
    >>> logging.TRACE
    5

    """
    if not methodName:
        methodName = levelName.lower()

    if hasattr(logging, levelName):
        raise AttributeError(
            '{} already defined in logging module'.format(levelName))
    if hasattr(logging, methodName):
        raise AttributeError(
            '{} already defined in logging module'.format(methodName))
    if hasattr(logging.getLoggerClass(), methodName):
        raise AttributeError(
            '{} already defined in logger class'.format(methodName))

    # This method was inspired by the answers to Stack Overflow post
    # http://stackoverflow.com/q/2183233/2988730, especially
    # http://stackoverflow.com/a/13638084/2988730
    def logForLevel(self, message, *args, **kwargs):
        if self.isEnabledFor(levelNum):
            self._log(levelNum, message, args, **kwargs)

    def logToRoot(message, *args, **kwargs):
        logging.log(levelNum, message, *args, **kwargs)

    logging.addLevelName(levelNum, levelName)
    setattr(logging, levelName, levelNum)
    setattr(logging.getLoggerClass(), methodName, logForLevel)
    setattr(logging, methodName, logToRoot)


if __name__ == "__main__":
    # PyQt 5.5 o superior aborta la ejecución si una excepción en un slot()
    # no es capturada dentro de la misma; el programa falla con SegFault.
    # Aunque esto no debería ocurrir, y se debería prevenir lo máximo posible
    # es bastante incómodo y genera problemas graves para detectar el problema.
    # Agregamos sys.excepthook para controlar esto y hacer que PyQt5 no nos
    # dé un segfault, aunque el resultado no sea siempre correcto:
    startup_check_dependencies()
    sys.excepthook = traceback.print_exception
    ret = main()
    gc.collect()
    print("Closing Pineboo...")
    if ret:
        sys.exit(ret)
    else:
        sys.exit(0)
