#!/usr/bin/python3 -u
# -*# -*- coding: utf-8 -*-



"""
    Bootstrap. Se encarga de inicializar la aplicación y ceder el control a
    pineboolib.main(); para ello acepta los parámetros necesarios de consola
    y configura el programa adecuadamente.
"""
import sys, re, traceback, os, gc
from optparse import OptionParser
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)


try:
    from lxml import etree
except ImportError:
    print(traceback.format_exc())
    print()
    print("HINT: Instale el paquete python3-lxml e intente de nuevo")
    print()
    sys.exit(32)
try:
    import psycopg2
except ImportError:
    print(traceback.format_exc())
    print()
    print("HINT: Instale el paquete python3-psycopg2 e intente de nuevo")
    print()
    sys.exit(32)

try:
    #import sip
    # switch on QVariant in Python3
    #sip.setapi('QVariant', 1)
    #sip.setapi('QString', 1)

    from PyQt4 import QtGui, QtCore, uic
except ImportError:
    print(traceback.format_exc())
    print()
    print("HINT: Instale el paquete python3-pyqt4 e intente de nuevo")
    print()
    sys.exit(32)


from pineboolib.utils import filedir
import pineboolib.DlgConnect

import pineboolib
import pineboolib.main
#pineboolib.main.main()


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
    user_pass = None
    host_port = None
    try:
        uphpstring = connstring[:connstring.rindex("/")]
    except ValueError:
        dbname = connstring
        if not re.match(r"\w+", dbname): raise ValueError("base de datos no valida")
        return user, passwd, host, port, dbname
    dbname = connstring[connstring.rindex("/")+1:]
    conn_list = uphpstring.split("@")
    if len(conn_list) == 0: raise ValueError("String de conexión vacío")
    elif len(conn_list) == 1: host_port = conn_list[0]
    elif len(conn_list) == 2: user_pass, host_port = conn_list
    else: raise ValueError("String de conexión erróneo.")

    if user_pass:
        user_pass = user_pass.split(":")
        if len(user_pass) == 1: user = user_pass[0]
        elif len(user_pass) == 2: user, passwd = user_pass[0], user_pass[1]
        else: raise ValueError("La cadena de usuario tiene dos veces dos puntos.")

    if host_port:
        host_port = host_port.split(":")
        if len(host_port) == 1: host = host_port[0]
        elif len(host_port) == 2: host, port = host_port[0], host_port[1]
        else: raise ValueError("La cadena de host tiene dos veces dos puntos.")
    if not re.match(r"\w+", user): raise ValueError("Usuario no valido")
    if not re.match(r"\w+", dbname): raise ValueError("base de datos no valida")
    if not re.match(r"\d+", port): raise ValueError("puerto no valido")

    return user, passwd, host, port, dbname


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
                      help="connect to database with user and password.", metavar="user:passwd@host:port/database")
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose", default=True,
                      help="don't print status messages to stdout")
    parser.add_option("-a", "--action", dest="action",
                      help="load action", metavar="ACTION")
    parser.add_option("--no-python-cache",
                      action="store_true", dest="no_python_cache", default=False,
                      help="Always translate QS to Python")
    parser.add_option("--preload",
                      action="store_true", dest="preload", default=False,
                      help="Load everything. Then exit. (Populates Pineboo cache)")

    (options, args) = parser.parse_args()
    
    
    app = QtGui.QApplication(sys.argv)
    noto_fonts = [
        "NotoSans-BoldItalic.ttf",
        "NotoSans-Bold.ttf",
        "NotoSans-Italic.ttf",
        "NotoSans-Regular.ttf",
    ]
    for fontfile in noto_fonts:
        QtGui.QFontDatabase.addApplicationFont(filedir("fonts/Noto_Sans", fontfile))
    
                                               
    QtGui.QApplication.setStyle("QtCurve")
    font = QtGui.QFont('Noto Sans',9)
    font.setBold(False)
    font.setItalic(False)
    QtGui.QApplication.setFont(font)
        
    pineboolib.no_python_cache = options.no_python_cache

    # Es necesario importarlo a esta altura, QApplication tiene que ser construido antes que cualquier widget
    from pineboolib import mainForm

    project = pineboolib.main.Project()
    if options.verbose:
        project.setDebugLevel(100)
        mainForm.MainForm.setDebugLevel(100)
    else:
        project.setDebugLevel(0)
        mainForm.MainForm.setDebugLevel(0)
    if options.project:
        if not options.project.endswith(".xml"):
            options.project += ".xml"
        prjpath = filedir("../projects", options.project)
        if not os.path.isfile(prjpath):
            raise ValueError("el proyecto %s no existe." % options.project)
        project.load(prjpath)
    elif options.connection:
        user, passwd, host, port, dbname = translate_connstring(options.connection)
        project.load_db(dbname, host, port, user, passwd)
    else:
        connection_window = pineboolib.DlgConnect.DlgConnect()
        connection_window.load()
        connection_window.show()
        ret = app.exec_()
        if connection_window.close():    
            if connection_window.ruta:
                prjpath = connection_window.ruta
                print("Cargando desde ruta %r " % prjpath)
                project.load(prjpath)
            elif connection_window.database:
                print("Cargando credenciales")
                project.load_db(connection_window.database,connection_window.hostname,connection_window.portnumber,connection_window.username,connection_window.password)
            
            
            
            
        if not connection_window.ruta and not connection_window.database:
            sys.exit(ret)

        #Cargando spashscreen
    # Create and display the splash screen
    splash_pix = QtGui.QPixmap(filedir("../share/splashscreen/splash_%s.png" % project.dbname))
    splash = QtGui.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    
    frameGm = splash.frameGeometry()
    screen = QtGui.QApplication.desktop().screenNumber(QtGui.QApplication.desktop().cursor().pos())
    centerPoint = QtGui.QApplication.desktop().screenGeometry(screen).center()
    frameGm.moveCenter(centerPoint)
    splash.move(frameGm.topLeft())


    splash.showMessage("Iniciando proyecto ...")
    if options.verbose: print("Iniciando proyecto ...")
    project.run()

    splash.showMessage("Creando interfaz ...")
    if options.verbose: print("Creando interfaz ...")
    if options.action:
        objaction = None
        for k, module in list(project.modules.items()):
            try:
                if not module.load(): continue
            except Exception as err:
                print("ERROR:", err.__class__.__name__, str(err))
                continue
            if options.action in module.actions:
                objaction = module.actions[options.action]
        if objaction is None: raise ValueError("Action name %s not found" % options.action)

        main_window = mainForm.mainWindow
        main_window.load()
        splash.showMessage("Módulos y pestañas ...")
        if options.verbose: print("Módulos y pestañas ...")
        for k,area in sorted(project.areas.items()):
            main_window.addAreaTab(area)
        for k,module in sorted(project.modules.items()):
            main_window.addModuleInTab(module)
        splash.showMessage("Abriendo interfaz ...")
        if options.verbose: print("Abriendo interfaz ...")
        main_window.show()
        objaction.openDefaultForm()
        splash.hide()
        ret = app.exec_()
        mainForm.mainWindow = None
        return ret
    else:
        main_window = mainForm.mainWindow
        main_window.load()
        ret = 0
        splash.showMessage("Módulos y pestañas ...")
        if options.verbose: print("Módulos y pestañas ...")
        for k,area in sorted(project.areas.items()):
            main_window.addAreaTab(area)
        for k,module in sorted(project.modules.items()):
            main_window.addModuleInTab(module)
        if options.preload:
            if options.verbose: print("Precarga ...")
            for action in project.actions:
                if options.verbose: print("* * * Cargando acción %s . . . " % action)
                try:
                    project.actions[action].load()
                except Exception:
                    print(traceback.format_exc())
                    project.conn.conn.rollback()
        else:
            splash.showMessage("Abriendo interfaz ...")
            if options.verbose: print("Abriendo interfaz ...")
            main_window.show()
    
            splash.showMessage("Listo ...")
            QtCore.QTimer.singleShot(2000, splash.hide)
            
            ret = app.exec_()
        mainForm.mainWindow = None
        del main_window
        del project
        return ret
    
    
if __name__ == "__main__":
    ret = main()
    gc.collect()
    print("Closing Pineboo...")
    if ret: sys.exit(ret)
    else: sys.exit(0)

