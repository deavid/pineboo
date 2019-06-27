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

import logging


logger = logging.getLogger("pineboo.__main__")


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
        uphpstring = connstring[: connstring.rindex("/")]
    except ValueError:
        dbname = connstring
        if not re.match(r"\w+", dbname):
            raise ValueError("base de datos no valida")
        return user, passwd, host, port, dbname
    dbname = connstring[connstring.rindex("/") + 1 :]
    conn_list = [None, None] + uphpstring.split("@")
    user_pass, host_port = conn_list[-2], conn_list[-1]

    if user_pass:
        user_pass = user_pass.split(":") + [None, None, None]
        user, passwd, driver_alias = user_pass[0], user_pass[1] or passwd, user_pass[2] or driver_alias
        if user_pass[3]:
            raise ValueError("La cadena de usuario debe tener el formato user:pass:driver.")

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
    logger.debug(
        "user:%s, passwd:%s, driver_alias:%s, host:%s, port:%s, dbname:%s", user, "*" * len(passwd), driver_alias, host, port, dbname
    )
    return user, passwd, driver_alias, host, port, dbname


def create_app(DGI):
    """Create a MainForm using the DGI or the core."""
    from pineboolib.utils import filedir
    import pineboolib

    app = DGI.create_app()
    pineboolib._DGI = DGI  # Almacenamos de DGI seleccionado para futuros usos

    if DGI.localDesktop():
        from PyQt5 import QtGui

        noto_fonts = ["NotoSans-BoldItalic.ttf", "NotoSans-Bold.ttf", "NotoSans-Italic.ttf", "NotoSans-Regular.ttf"]
        for fontfile in noto_fonts:
            QtGui.QFontDatabase.addApplicationFont(filedir("../share/fonts/Noto_Sans", fontfile))

        from pineboolib.fllegacy.flsettings import FLSettings

        sett_ = FLSettings()

        styleA = sett_.readEntry("application/style", None)
        if styleA is None:
            styleA = "Fusion"

        app.setStyle(styleA)

        fontA = sett_.readEntry("application/font", None)
        if fontA is None:
            if DGI.mobilePlatform():
                font = QtGui.QFont("Noto Sans", 14)
            else:
                font = QtGui.QFont("Noto Sans", 9)
            font.setBold(False)
            font.setItalic(False)
        else:
            font = QtGui.QFont(fontA[0], int(fontA[1]), int(fontA[2]), fontA[3] == "true")

        app.setFont(font)
    return app


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
            from pineboolib.fllegacy.flsettings import FLSettings

            project.deleteCache = FLSettings().readBoolEntry("ebcomportamiento/deleteCache", False)
            project.parseProject = FLSettings().readBoolEntry("ebcomportamiento/parseProject", False)
            project.load_db(
                connection_window.database,
                connection_window.hostname,
                connection_window.portnumber,
                connection_window.username,
                connection_window.password,
                connection_window.driveralias,
            )
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

    frameGm = splash.frameGeometry()
    screen = QtWidgets.QApplication.desktop().screenNumber(QtWidgets.QApplication.desktop().cursor().pos())
    centerPoint = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
    frameGm.moveCenter(centerPoint)
    splash.move(frameGm.topLeft())
    splash.show()

    return splash


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

    if DGI.useDesktop() and DGI.localDesktop() and splash:
        splash.showMessage("Iniciando proyecto ...", QtCore.Qt.AlignLeft, QtCore.Qt.white)
        DGI.processEvents()
    logger.info("Iniciando proyecto ...")

    # Necesario para que funcione isLoadedModule ¿es este el mejor sitio?
    project.conn.managerModules().loadIdAreas()
    project.conn.managerModules().loadAllIdModules()

    objaction = None

    for module_name in project.modules.keys():
        project.modules[module_name].load()

    if options.action:
        list = options.action.split(":")
        action_name = list[0].split(".")[0]
        # objaction = project.conn.manager(options.action)
        if action_name in project.actions.keys():

            ret = project.call(list[0], list[1:] if len(list) > 1 else [])
            return ret
        else:
            raise ValueError("Action name %s not found" % options.action)

    if DGI.localDesktop() and splash:
        splash.showMessage("Creando interfaz ...", QtCore.Qt.AlignLeft, QtCore.Qt.white)
        DGI.processEvents()

    if mainForm is not None:
        logger.info("Creando interfaz ...")
        main_window = mainForm.mainWindow
        main_window.initScript()
        ret = 0

    if options.preload:
        preload_actions(project, options.forceload)

    if mainForm is not None:
        if DGI.localDesktop():
            splash.showMessage("Abriendo interfaz ...", QtCore.Qt.AlignLeft, QtCore.Qt.white)
            DGI.processEvents()

        logger.info("Abriendo interfaz ...")
        main_window.show()
        if DGI.localDesktop():
            splash.showMessage("Listo ...", QtCore.Qt.AlignLeft, QtCore.Qt.white)
            DGI.processEvents()
            # main_window.w_.activateWindow()
        QtCore.QTimer.singleShot(1000, splash.hide)

    if objaction:
        project.openDefaultForm(objaction.form())

    if DGI.localDesktop():
        ret = app.exec_()
    else:
        ret = DGI.exec_()

    if mainForm is not None:
        mainForm.mainWindow = None
        del main_window
    del project
    return ret


if __name__ == "__main__":
    from pineboolib.loader.main import startup

    startup()
