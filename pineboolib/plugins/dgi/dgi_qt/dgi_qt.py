# # -*- coding: utf-8 -*-
import logging
import os
import sys
import pineboolib

from importlib import import_module

from PyQt5 import QtWidgets, QtCore, QtGui, Qt, QtXml
from PyQt5.QtWidgets import qApp

from pineboolib.plugins.dgi.dgi_schema import dgi_schema
from pineboolib.core.utils.utils_base import filedir, load2xml
from pineboolib.application.utils.path import _path
from pineboolib.fllegacy.flsettings import FLSettings


logger = logging.getLogger(__name__)


class dgi_qt(dgi_schema):

    pnqt3ui = None

    def __init__(self):
        super(dgi_qt, self).__init__()  # desktopEnabled y mlDefault a True
        self._name = "qt"
        self._alias = "Qt5"
        self.set_clean_no_python_changeable(True)
        self.set_clean_no_python(FLSettings().readBoolEntry("ebcomportamiento/clean_no_python", False))

        from pineboolib.plugins.dgi.dgi_qt import dgi_qt3ui

        self.pnqt3ui = dgi_qt3ui

    def create_app(self):
        app = QtWidgets.QApplication(sys.argv)
        app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
        return app

    def __getattr__(self, name):

        cls = super().resolveObject(self._name, name)
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
        parent = qApp.focusWidget().parent() if hasattr(qApp.focusWidget(), "parent") else qApp.focusWidget()
        self.MessageBox.warning(t, self.MessageBox.Ok, self.MessageBox.NoButton, self.MessageBox.NoButton, "Pineboo", parent)

    def createUI(self, n, connector=None, parent=None, name=None):

        if ".ui" not in n:
            n += ".ui"

        form_path = n if os.path.exists(n) else _path(n)

        if form_path is None:
            # raise AttributeError("File %r not found in project" % n)
            # logger.warning("%s.createUI : No se encuentra el fichero %s", self.__name__, n)
            return

        tree = load2xml(form_path)

        if not tree:
            return parent

        root_ = tree.getroot()

        UIVersion = root_.get("version")
        if parent is None:
            wid = root_.find("widget")
            parent = getattr(pineboolib.pncontrolsfactory, wid.get("class"))()

        if hasattr(parent, "widget"):
            w_ = parent.widget
        else:
            w_ = parent

        logger.info("Procesando %s (v%s)", n, UIVersion)
        if UIVersion < "4.0":
            self.pnqt3ui.loadUi(form_path, w_)
        else:
            from PyQt5 import uic

            qtWidgetPlugings = filedir("./plugins/qtwidgetsplugins")
            if qtWidgetPlugings not in uic.widgetPluginPath:
                logger.info("Añadiendo path %s a uic.widgetPluginPath", qtWidgetPlugings)
                uic.widgetPluginPath.append(qtWidgetPlugings)
            uic.loadUi(form_path, w_)

        return w_
