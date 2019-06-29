import logging

logger = logging.getLogger("loader.init_project")


def init_project(DGI, splash, options, project, mainForm, app):
    """Initialize the project and start it."""
    # from PyQt5 import QtCore

    # if DGI.useDesktop() and DGI.localDesktop() and splash:
    #     splash.showMessage("Iniciando proyecto ...", QtCore.Qt.AlignLeft, QtCore.Qt.white)
    #     DGI.processEvents()

    logger.info("Iniciando proyecto ...")

    # Necesario para que funcione isLoadedModule ¿es este el mejor sitio?
    project.conn.managerModules().loadIdAreas()
    project.conn.managerModules().loadAllIdModules()

    objaction = None

    for module_name in project.modules.keys():
        project.modules[module_name].load()

    if options.preload:
        from .preload import preload_actions

        preload_actions(project, options.forceload)

        logger.info("Finished preloading")
        return

    if options.action:
        list = options.action.split(":")
        action_name = list[0].split(".")[0]
        # objaction = project.conn.manager(options.action)
        if action_name in project.actions.keys():

            ret = project.call(list[0], list[1:] if len(list) > 1 else [])
            return ret
        else:
            raise ValueError("Action name %s not found" % options.action)

    # if DGI.localDesktop() and splash:
    #     splash.showMessage("Creando interfaz ...", QtCore.Qt.AlignLeft, QtCore.Qt.white)
    #     DGI.processEvents()

    if mainForm is not None:
        logger.info("Creando interfaz ...")
        main_window = mainForm.mainWindow
        main_window.initScript()
        ret = 0

    if mainForm is not None:
        # if DGI.localDesktop():
        #     splash.showMessage("Abriendo interfaz ...", QtCore.Qt.AlignLeft, QtCore.Qt.white)
        #     DGI.processEvents()

        logger.info("Abriendo interfaz ...")
        main_window.show()
        # if DGI.localDesktop():
        #     splash.showMessage("Listo ...", QtCore.Qt.AlignLeft, QtCore.Qt.white)
        #     DGI.processEvents()
        #     # main_window.w_.activateWindow()
        # QtCore.QTimer.singleShot(1000, splash.hide)

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
