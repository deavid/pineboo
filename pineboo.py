#!/usr/bin/python3
# -*- coding: utf-8 -*-
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
    import sip
    sip.setapi('QString', 1)

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

    (options, args) = parser.parse_args()
    app = QtGui.QApplication(sys.argv)

    pineboolib.no_python_cache = options.no_python_cache

    # Es necesario importarlo a esta altura, QApplication tiene que ser construido antes que cualquier widget
    from pineboolib import mainForm

    project = pineboolib.main.Project()

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
            prjpath = connection_window.ruta
        if not prjpath:
            sys.exit(ret)




    print("Iniciando proyecto ...")
    project.run()

    print("Creando interfaz ...")
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
        print("Módulos y pestañas ...")
        for k,area in sorted(project.areas.items()):
            main_window.addAreaTab(area)
        for k,module in sorted(project.modules.items()):
            main_window.addModuleInTab(module)
        print("Abriendo interfaz ...")
        main_window.show()

        objaction.openDefaultForm()
        return app.exec_()
    else:
        main_window = mainForm.mainWindow
        main_window.load()
        print("Módulos y pestañas ...")
        for k,area in sorted(project.areas.items()):
            main_window.addAreaTab(area)
        for k,module in sorted(project.modules.items()):
            main_window.addModuleInTab(module)
        print("Abriendo interfaz ...")
        main_window.show()
        ret = app.exec_()
        del main_window
        del project
        return ret

if __name__ == "__main__":
    ret = main()
    gc.collect()
    print("Closing Pineboo...")
    if ret: sys.exit(ret)
    else: sys.exit(0)

