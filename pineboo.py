#!/usr/bin/python3 -u
# -*# -*- coding: utf-8 -*-
"""
    Bootstrap. Se encarga de inicializar la aplicación y ceder el control a
    pineboolib.main(); para ello acepta los parámetros necesarios de consola
    y configura el programa adecuadamente.
"""
import sys
import re
import traceback
import os
import gc
import linecache
from optparse import OptionParser
import signal
import importlib
import pineboo
signal.signal(signal.SIGINT, signal.SIG_DFL)

dependences = []


if sys.version_info[0] < 3:
    print("Tienes que usar Python 3 o superior.")
    sys.exit(32)


try:
    from lxml import etree
except ImportError:
    print(traceback.format_exc())
    dependences.append("python3-lxml")

# try:
#    import psycopg2
# except ImportError:
#    print(traceback.format_exc())
#    dependeces.append("python3-psycopg2")


try:
    import ply
except ImportError:
    print(traceback.format_exc())
    dependences.append("python3-ply")


try:

    from PyQt5 import QtGui, QtCore, uic, QtWidgets
except ImportError:
    print(traceback.format_exc())
    dependences.append("python3-pyqt5")

if len(dependences) > 0:
    print()
    print("HINT: Dependencias incumplidas:")
    for dep in dependences:
        print("HINT: Instale el paquete %s e intente de nuevo" % dep)
    print()
    sys.exit(32)

from pineboolib.utils import filedir
import pineboolib.DlgConnect

import pineboolib
import pineboolib.main
# pineboolib.main.main()


def translate_connstring(connstring):
    """
        Acepta un parámetro "connstring" que tenga la forma user@host/dbname
        y devuelve todos los parámetros por separado. Tiene en cuenta los
        valores por defecto y las diferentes formas de abreviar que existen.
    """
    user = "postgres"
    passwd = "passwd"
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
    conn_list = uphpstring.split("@")
    if len(conn_list) == 0:
        raise ValueError("String de conexión vacío")
    elif len(conn_list) == 1:
        host_port = conn_list[0]
    elif len(conn_list) == 2:
        user_pass, host_port = conn_list
    else:
        raise ValueError("String de conexión erróneo.")

    if user_pass:
        user_pass = user_pass.split(":")
        if len(user_pass) == 1:
            user = user_pass[0]
        elif len(user_pass) == 2:
            user, passwd = user_pass[0], user_pass[1]
        elif len(user_pass) == 3:
            user, passwd, driver_alias = user_pass[0], user_pass[1], user_pass[2]
        else:
            raise ValueError(
                "La cadena de usuario tiene tres veces dos puntos.")

    if host_port:
        host_port = host_port.split(":")
        if len(host_port) == 1:
            host = host_port[0]
        elif len(host_port) == 2:
            host, port = host_port[0], host_port[1]
        else:
            raise ValueError("La cadena de host tiene dos veces dos puntos.")
    if not re.match(r"\w+", user):
        raise ValueError("Usuario no valido")
    if not re.match(r"\w+", dbname):
        raise ValueError("base de datos no valida")
    if not re.match(r"\d+", port):
        raise ValueError("puerto no valido")

    return user, passwd, driver_alias, host, port, dbname


def main():
    """
        Programa principal. Gestión de las opciones y la ayuda, así como inicializar
        todos los objetos.
    """
    # TODO: Refactorizar función en otras más pequeñas
    parser = OptionParser()
    parser.add_option("-l", "--load", dest="project",
                      help="load projects/PROJECT.xml and run it", metavar="PROJECT")
    parser.add_option("-c", "--connect", dest="connection",
                      help="connect to database with user and password.", metavar="user:passwd:driver_alias@host:port/database")
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose", default=True,
                      help="don't print status messages to stdout")
    parser.add_option("--trace-debug",
                      action="store_true", dest="trace_debug", default=False,
                      help="Write lots of trace information to stdout")
    parser.add_option("-a", "--action", dest="action",
                      help="load action", metavar="ACTION")
    parser.add_option("--no-python-cache",
                      action="store_true", dest="no_python_cache", default=False,
                      help="Always translate QS to Python")
    parser.add_option("--preload",
                      action="store_true", dest="preload", default=False,
                      help="Load everything. Then exit. (Populates Pineboo cache)")
    parser.add_option("--dgi",
                      dest="dgi",
                      help="Change the gdi mode by default", metavar="DGI")

    parser.add_option("--dgi_parameter",
                      dest="dgi_parameter",
                      help="Change the gdi mode by default", metavar="DGIPARAMETER")

    (options, args) = parser.parse_args()

    pineboolib.no_python_cache = options.no_python_cache

    dgiName_ = "qt"
    if options.dgi:
        dgiName_ = options.dgi

    DGI = getattr(importlib.import_module(
        "pineboolib.plugins.dgi.dgi_%s" % dgiName_), "dgi_%s" % dgiName_, None)()
    pineboo.DGI = DGI

    if options.verbose:
        print("DGI used:", dgiName_)

    if options.dgi_parameter:
        DGI.setParameter(options.dgi_parameter)

    if DGI.useDesktop():
        app = QtWidgets.QApplication(sys.argv)

        noto_fonts = [
            "NotoSans-BoldItalic.ttf",
            "NotoSans-Bold.ttf",
            "NotoSans-Italic.ttf",
            "NotoSans-Regular.ttf",
        ]
        for fontfile in noto_fonts:
            QtGui.QFontDatabase.addApplicationFont(
                filedir("../share/fonts/Noto_Sans", fontfile))

        QtWidgets.QApplication.setStyle("QtCurve")
        font = QtGui.QFont('Noto Sans', 9)
        font.setBold(False)
        font.setItalic(False)
        QtWidgets.QApplication.setFont(font)

        # Es necesario importarlo a esta altura, QApplication tiene que ser construido antes que cualquier widget

        mainForm = importlib.import_module("pineboolib.plugins.mainForm.%s.%s" % (
            pineboolib.main.Project.mainFormName, pineboolib.main.Project.mainFormName))
        #mainForm = getattr(module_, "MainForm")()

        #from pineboolib import mainForm

    project = pineboolib.main.Project(DGI)

    if options.verbose:
        project.setDebugLevel(100)
        if DGI.useDesktop():
            mainForm.MainForm.setDebugLevel(100)
    else:
        project.setDebugLevel(0)
        if DGI.useDesktop():
            mainForm.MainForm.setDebugLevel(0)
    if options.project:
        if not options.project.endswith(".xml"):
            options.project += ".xml"
        prjpath = filedir("../projects", options.project)
        if not os.path.isfile(prjpath):
            raise ValueError("el proyecto %s no existe." % options.project)
        project.load(prjpath)
    elif options.connection:
        user, passwd, driver_alias, host, port, dbname = translate_connstring(
            options.connection)
        project.load_db(dbname, host, port, user, passwd, driver_alias)
    else:
        if DGI.useDesktop() and DGI.localDesktop():
            connection_window = pineboolib.DlgConnect.DlgConnect()
            connection_window.load()
            connection_window.show()
            ret = app.exec_()
            if connection_window.close():
                # if connection_window.ruta:
                #    prjpath = connection_window.ruta
                #    print("Cargando desde ruta %r " % prjpath)
                #    project.load(prjpath)
                # elif connection_window.database:
                if connection_window.database:
                    print("Cargando credenciales")
                    project.deleteCache = connection_window.deleteCache
                    project.parseProject = connection_window.parseProject
                    project.load_db(connection_window.database, connection_window.hostname, connection_window.portnumber,
                                    connection_window.username, connection_window.password, connection_window.driveralias)

            if not connection_window.ruta and not connection_window.database:
                sys.exit(ret)

        # Cargando spashscreen
    # Create and display the splash screen
    if DGI.useDesktop() and DGI.localDesktop():
        splash_pix = QtGui.QPixmap(
            filedir("../share/splashscreen/splash_%s.png" % project.dbname))
        splash = QtWidgets.QSplashScreen(
            splash_pix, QtCore.Qt.WindowStaysOnTopHint)
        splash.setMask(splash_pix.mask())
        splash.show()

        frameGm = splash.frameGeometry()
        screen = QtWidgets.QApplication.desktop().screenNumber(
            QtWidgets.QApplication.desktop().cursor().pos())
        centerPoint = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        splash.move(frameGm.topLeft())

    if options.trace_debug:
        sys.settrace(traceit)

    project.run()
    if project.conn.conn == False:
        return main()

    if DGI.useDesktop() and DGI.localDesktop():
        splash.showMessage("Iniciando proyecto ...")
    if options.verbose:
        print("Iniciando proyecto ...")

    if DGI.useDesktop():
        if DGI.localDesktop():
            splash.showMessage("Creando interfaz ...")

        if options.verbose:
            print("Creando interfaz ...")
        if options.action:
            objaction = None
            for k, module in list(project.modules.items()):
                try:
                    if not module.load():
                        continue
                except Exception as err:
                    print("ERROR:", err.__class__.__name__, str(err))
                    continue
                if options.action in module.actions:
                    objaction = module.actions[options.action]
            if objaction is None:
                raise ValueError("Action name %s not found" % options.action)

            main_window = mainForm.mainWindow
            main_window.load()

            if DGI.localDesktop():
                splash.showMessage("Módulos y pestañas ...")
            if options.verbose:
                print("Módulos y pestañas ...")
            for k, area in sorted(project.areas.items()):
                main_window.loadArea(area)
            for k, module in sorted(project.modules.items()):
                main_window.loadModule(module)
            splash.showMessage("Abriendo interfaz ...")
            if options.verbose:
                print("Abriendo interfaz ...")
            main_window.show()
            project.call("sys.widget.init()", [], None, True)
            objaction.openDefaultForm()
            splash.hide()

            ret = app.exec_()
            mainForm.mainWindow = None
            return ret
        else:
            main_window = mainForm.mainWindow
            main_window.load()
            ret = 0
            if DGI.localDesktop():
                splash.showMessage("Módulos y pestañas ...")
            if options.verbose:
                print("Módulos y pestañas ...")
            for k, area in sorted(project.areas.items()):
                main_window.loadArea(area)
            for k, module in sorted(project.modules.items()):
                main_window.loadModule(module)
            if options.preload:
                if options.verbose:
                    print("Precarga ...")
                for action in project.actions:
                    if options.verbose:
                        print("* * * Cargando acción %s . . . " % action)
                    try:
                        project.actions[action].load()
                    except Exception:
                        print(traceback.format_exc())
                        project.conn.conn.rollback()
            else:
                if DGI.localDesktop():
                    splash.showMessage("Abriendo interfaz ...")
                if options.verbose:
                    print("Abriendo interfaz ...")
                main_window.show()
                project.call("sys.widget._class_init()", [], None, True)
                if DGI.localDesktop():
                    splash.showMessage("Listo ...")
                    QtCore.QTimer.singleShot(2000, splash.hide)

            ret = app.exec_()
            mainForm.mainWindow = None
            del main_window
            del project
            return ret

    else:

        if options.verbose:
            print("Cargando Módulos")
        for k, module in sorted(project.modules.items()):
            module.load(True)


def traceit(frame, event, arg):
    if event != "line":
        return traceit
    try:
        lineno = frame.f_lineno
        filename = frame.f_globals["__file__"]
        if "pineboo" not in filename:
            return traceit
        if (filename.endswith(".pyc") or
                filename.endswith(".pyo")):
            filename = filename[:-1]
        name = frame.f_globals["__name__"]
        line = linecache.getline(filename, lineno)
        print("%s:%s: %s" % (name, lineno, line.rstrip()))
    except:
        pass
    return traceit


if __name__ == "__main__":
    # PyQt 5.5 o superior aborta la ejecución si una excepción en un slot()
    # no es capturada dentro de la misma; el programa falla con SegFault.
    # Aunque esto no debería ocurrir, y se debería prevenir lo máximo posible
    # es bastante incómodo y genera problemas graves para detectar el problema.
    # Agregamos sys.excepthook para controlar esto y hacer que PyQt5 no nos
    # dé un segfault, aunque el resultado no sea siempre correcto:
    sys.excepthook = traceback.print_exception

    ret = main()
    if pineboo.DGI.useMLDefault():
        gc.collect()
        print("Closing Pineboo...")
        if ret:
            sys.exit(ret)
        else:
            sys.exit(0)

    else:
        pineboo.DGI.alternativeMain(ret)
