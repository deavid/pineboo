# # -*- coding: utf-8 -*-
import os
from importlib import import_module

from PyQt5 import QtWidgets, QtCore, QtGui, Qt, QtXml  # type: ignore

from pineboolib import logging
from pineboolib.plugins.dgi.dgi_schema import dgi_schema
from pineboolib.core.utils.utils_base import filedir, load2xml
from pineboolib.application.utils.path import _path
from pineboolib import qt3_widgets


from typing import Any

logger = logging.getLogger(__name__)


class dgi_qt(dgi_schema):

    pnqt3ui = None
    splash = None
    progress_dialog_mng = None

    def __init__(self):
        super(dgi_qt, self).__init__()  # desktopEnabled y mlDefault a True
        self._name = "qt"
        self._alias = "Qt5"

        from pineboolib.application.parsers.qt3uiparser import dgi_qt3ui
        from .dgi_objects.splash_screen import splashscreen
        from .dgi_objects.progress_dialog_manager import ProgressDialogManager
        from .dgi_objects.status_help_msg import StatusHelpMsg

        self.pnqt3ui = dgi_qt3ui
        self.splash = splashscreen()
        self.progress_dialog_manager = ProgressDialogManager()
        self.status_help_msg = StatusHelpMsg()

    def __getattr__(self, name):

        cls = self.resolveObject(self._name, name)
        if cls is None:
            mod_ = import_module(__name__)
            cls = getattr(mod_, name, None)

        if cls is None:
            cls = (
                getattr(QtWidgets, name, None)
                or getattr(QtXml, name, None)
                or getattr(QtGui, name, None)
                or getattr(Qt, name, None)
                or getattr(QtCore, name, None)
            )

        return cls

    def msgBoxWarning(self, t):
        from PyQt5.QtWidgets import qApp  # type: ignore
        from pineboolib.qt3_widgets.messagebox import MessageBox

        parent = qApp.focusWidget().parent() if hasattr(qApp.focusWidget(), "parent") else qApp.focusWidget()
        MessageBox.warning(t, MessageBox.Ok, MessageBox.NoButton, MessageBox.NoButton, "Pineboo", parent)

    def createUI(self, n, connector=None, parent=None, name=None) -> Any:

        if ".ui" not in n:
            n += ".ui"

        form_path = n if os.path.exists(n) else _path(n)

        if form_path is None:
            # raise AttributeError("File %r not found in project" % n)
            logger.debug("createUI: No se encuentra el fichero %s", n)
            return None

        tree = load2xml(form_path)

        if not tree:
            return parent

        root_ = tree.getroot()

        UIVersion = root_.get("version")
        if UIVersion is None:
            UIVersion = "1.0"
        if parent is None:
            wid = root_.find("widget")
            if wid is None:
                raise Exception("No parent provided and also no <widget> found")
            xclass = wid.get("class")
            if xclass is None:
                raise Exception("class was expected")
            parent = None
            if xclass == "QMainWindow":
                parent = qt3_widgets.qmainwindow.QMainWindow()

            if parent is None:
                raise Exception("xclass not found %s" % xclass)

        if hasattr(parent, "widget"):
            w_ = parent.widget
        else:
            w_ = parent

        logger.info("Procesando %s (v%s)", n, UIVersion)
        if UIVersion < "4.0":
            if self.pnqt3ui:
                self.pnqt3ui.loadUi(form_path, w_)
        else:
            from PyQt5 import uic  # type: ignore

            qtWidgetPlugings = filedir("../qtdesigner-plugins")
            if qtWidgetPlugings not in uic.widgetPluginPath:
                logger.info("Añadiendo path %s a uic.widgetPluginPath", qtWidgetPlugings)
                uic.widgetPluginPath.append(qtWidgetPlugings)
            uic.loadUi(form_path, w_)

        return w_

    def about_pineboo(self):
        from .dgi_objects.dlg_about.about_pineboo import AboutPineboo

        about_ = AboutPineboo()
        about_.show()
