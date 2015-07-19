#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys, re
from optparse import OptionParser

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
    from PyQt4 import QtGui, QtCore, uic
except ImportError:
    print(traceback.format_exc())
    print()
    print("HINT: Instale el paquete python3-pyqt4 e intente de nuevo")
    print()
    sys.exit(32)


import pineboolib
import pineboolib.main
#pineboolib.main.main()


def translate_connstring(connstring):
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
        if len(user_pass) == 1: user = user_pass[0]
        elif len(user_pass) == 2: user, passwd = user_pass
        else: raise ValueError("La cadena de usuario tiene dos veces dos puntos.")

    if host_port:
        if len(host_port) == 1: host = host_port[0]
        elif len(host_port) == 2: host, port = host_port
        else: raise ValueError("La cadena de host tiene dos veces dos puntos.")
    if not re.match(r"\w+", user): raise ValueError("Usuario no valido")
    if not re.match(r"\w+", dbname): raise ValueError("base de datos no valida")
    if not re.match(r"\d+", port): raise ValueError("puerto no valido")

    return user, password, host, port, dbname


def main():
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
                      action="store_true",dest="no_python_cache", default=False,
                      help="Always translate QS to Python")

    (options, args) = parser.parse_args()
    app = QtGui.QApplication(sys.argv)

    pineboolib.no_python_cache = options.no_python_cache

    from pineboolib import mainForm # Es necesario importarlo a esta altura, QApplication tiene que ser construido antes que cualquier widget

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
        w = DlgConnect.DlgConnect()
        w.load()
        w.show()
        ret = app.exec_()
        if (w.close()):
            prjpath = w.ruta
        if not prjpath:
            sys.exit(ret)




    print("Iniciando proyecto ...")
    project.run()

    print("Creando interfaz ...")
    if options.action:
        objaction = None
        for k,module in list(project.modules.items()):
            try:
                if not module.load(): continue
            except Exception as e:
                print("ERROR:", e.__class__.__name__, str(e))
                continue
            if options.action in module.actions:
                objaction = module.actions[options.action]
        if objaction is None: raise ValueError("Action name %s not found" % options.action)
        objaction.openDefaultForm()
        sys.exit(app.exec_())
    else:
        w = mainForm.mainWindow
        w.load()
        print("Módulos y pestañas ...")
        for module in list(project.modules.values()):
            w.addModuleInTab(module)
        print("Abriendo interfaz ...")
        w.show()
        ret = app.exec_()
        del w
        del project
        sys.exit(ret)

if __name__ == "__main__": main()
