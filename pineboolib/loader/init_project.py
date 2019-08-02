from pineboolib import logging
from typing import Any

logger = logging.getLogger("loader.init_project")


def init_project(DGI, options, project, mainForm, app) -> Any:
    """Initialize the project and start it."""
    # from PyQt5 import QtCore  # type: ignore

    # if DGI.useDesktop() and DGI.localDesktop() and splash:
    #     splash.showMessage("Iniciando proyecto ...", QtCore.Qt.AlignLeft, QtCore.Qt.white)
    #     DGI.processEvents()

    logger.info("Iniciando proyecto ...")

    if options.preload:
        from .preload import preload_actions

        preload_actions(project, options.forceload)

        logger.info("Finished preloading")
        return

    if options.action:
        list = options.action.split(":")
        action_name = list[0].split(".")[0]
        # FIXME: Why is commented out?
        # objaction = project.conn.manager(options.action)
        if action_name in project.actions.keys():

            ret = project.call(list[0], list[1:] if len(list) > 1 else [])
            return ret
        else:
            raise ValueError("Action name %s not found" % options.action)

    from pineboolib.core.settings import settings

    call_function = settings.value("application/callFunction", None)
    if call_function:
        project.call(call_function, [])

    project.message_manager().send("splash", "showMessage", ["Creando interface ..."])

    if mainForm is not None:
        logger.info("Creando interfaz ...")
        main_window = mainForm.mainWindow
        main_window.initScript()
        ret = 0

    if mainForm is not None:
        project.message_manager().send("splash", "showMessage", ["Abriendo interfaz ..."])

        logger.info("Abriendo interfaz ...")
        main_window.show()
        project.message_manager().send("splash", "showMessage", ["Listo ..."])
        project.message_manager().send("splash", "hide")
    # FIXME: Is always None because the earlier code is commented out
    # if objaction:
    #     project.openDefaultForm(objaction.form())

    if DGI.localDesktop():
        ret = app.exec_()
    else:
        ret = DGI.exec_()

    if mainForm is not None:
        mainForm.mainWindow = None
        del main_window
    del project
    return ret
