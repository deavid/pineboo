#!/usr/bin/python3 -u
# -*# -*- coding: utf-8 -*-
"""
    Bootstrap. Se encarga de inicializar la aplicación y ceder el control a
    pineboolib.main(); para ello acepta los parámetros necesarios de consola
    y configura el programa adecuadamente.
"""
import sys, re, traceback, os, gc
from optparse import OptionParser
import signal, importlib
signal.signal(signal.SIGINT, signal.SIG_DFL)

import pineboo_fastcgi

dependeces = []


if sys.version_info[0] < 3:
    print("Tienes que usar Python 3 o superior.")
    sys.exit(32)
    

try:
    from lxml import etree
except ImportError:
    print(traceback.format_exc())
    dependeces.append("python3-lxml")
 
#try:
#    import psycopg2
#except ImportError:
#    print(traceback.format_exc())
#    dependeces.append("python3-psycopg2")


try:
    import ply
except ImportError:
    print(traceback.format_exc())
    dependeces.append("python3-ply")

try:
    import flup
except ImportError:
    print(traceback.format_exc())
    dependeces.append("flup-py3")

try:

    from PyQt5 import QtGui, QtCore, uic, QtWidgets
except ImportError:
    print(traceback.format_exc())
    dependeces.append("python3-pyqt5")

if len(dependeces) > 0:
    print()
    print("HINT: Dependencias incumplidas:")
    for dep in dependeces:
        print("HINT: Instale el paquete %s e intente de nuevo" % dep)
    print()
    sys.exit(32)

from flup.server.fcgi import WSGIServer

from pineboolib.utils import filedir
import pineboolib.DlgConnect

import pineboolib
import pineboolib.main
#pineboolib.main.main()

path_socket = None


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
        elif len(user_pass) == 3: user, passwd, driver_alias = user_pass[0], user_pass[1], user_pass[2]
        else: raise ValueError("La cadena de usuario tiene tres veces dos puntos.")

    if host_port:
        host_port = host_port.split(":")
        if len(host_port) == 1: host = host_port[0]
        elif len(host_port) == 2: host, port = host_port[0], host_port[1]
        else: raise ValueError("La cadena de host tiene dos veces dos puntos.")
    if not re.match(r"\w+", user): raise ValueError("Usuario no valido")
    if not re.match(r"\w+", dbname): raise ValueError("base de datos no valida")
    if not re.match(r"\d+", port): raise ValueError("puerto no valido")

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
    parser.add_option("-a", "--action", dest="action",
                      help="load action", metavar="ACTION")
    parser.add_option("--no-python-cache",
                      action="store_true", dest="no_python_cache", default=False,
                      help="Always translate QS to Python")
    parser.add_option("--preload",
                      action="store_true", dest="preload", default=False,
                      help="Load everything. Then exit. (Populates Pineboo cache)")
    
    parser.add_option("--fcgiSocket",
                      dest="fcgiSocket",
                      help="Start in fastcgi mode", metavar="FCGISOCKET")
    
    
    
    app = QtWidgets.QApplication(sys.argv)
    
    (options, args) = parser.parse_args()
    
    noto_fonts = [
        "NotoSans-BoldItalic.ttf",
        "NotoSans-Bold.ttf",
        "NotoSans-Italic.ttf",
        "NotoSans-Regular.ttf",
    ]
    for fontfile in noto_fonts:
        QtGui.QFontDatabase.addApplicationFont(filedir("fonts/Noto_Sans", fontfile))
    
                                               
    QtWidgets.QApplication.setStyle("QtCurve")
    font = QtGui.QFont('Noto Sans',9)
    font.setBold(False)
    font.setItalic(False)
    QtWidgets.QApplication.setFont(font)
        
    pineboolib.no_python_cache = options.no_python_cache

    # Es necesario importarlo a esta altura, QApplication tiene que ser construido antes que cualquier widget

    mainForm = importlib.import_module("pineboolib.plugins.mainForm.%s.%s" % (pineboolib.main.Project.mainFormName, pineboolib.main.Project.mainFormName))
    #mainForm = getattr(module_, "MainForm")()
        
    #from pineboolib import mainForm

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
        user, passwd,driver_alias, host, port, dbname = translate_connstring(options.connection)
        project.load_db(dbname, host, port, user, passwd, driver_alias)
    
    if options.fcgiSocket:
        pineboo_fastcgi.path_socket = options.fcgiSocket
    
    if options.verbose:
        
        print("Iniciando en modo FastCGI ...")
    project.run()
    if options.verbose: print("Cargando Módulos")
    for k,module in sorted(project.modules.items()):
        module.load()
        
    project.call("sys.widget._class_init()", [], None, True)
    
    return project
 
 
 
class parser(object):
    prj = None
     
    def __init__(self, prj):
         self.prj = prj
 
    def call(self, env):
        #fn = eval(env[0], pineboolib.qsaglobals.__dict__)
        fn = eval("flfactppal.fcgiProcessRequest", pineboolib.qsaglobals.__dict__)
        aList = env
        if aList:
            return fn(aList)
        
     
     
     
 
        
    
    
if __name__ == "__main__":
    app = parser(main())
    print("Ruta socket", pineboo_fastcgi.path_socket)
    WSGIServer(app, bindAddress=pineboo_fastcgi.path_socket).run()
    #gc.collect()
    print("Closing Pineboo...")
    if ret: sys.exit(ret)
    else: sys.exit(0)

