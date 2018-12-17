# # -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtCore, QtGui, Qt, QtXml
from importlib import import_module


from pineboolib.plugins.dgi.dgi_schema import dgi_schema
from pineboolib.utils import filedir, load2xml, _path
from pineboolib.fllegacy.fldatatable import FLDataTable
import pineboolib
import logging, os


logger = logging.getLogger(__name__)


class dgi_qt(dgi_schema):
    
    pnqt3ui = None

    def __init__(self):
        super(dgi_qt, self).__init__()  # desktopEnabled y mlDefault a True
        self._name = "qt"
        self._alias = "Qt5"
        
        from pineboolib.plugins.dgi.dgi_qt import dgi_qt3ui
        self.pnqt3ui = dgi_qt3ui
        

    def __getattr__(self, name):
        cls = None
        try:
            mod_ = import_module("pineboolib.plugins.dgi.dgi_%s.dgi_objects.%s" % (self._name, name.lower()))
            cls = getattr(mod_, name, None) 
        except Exception:
            mod_ = import_module(__name__)
            cls = getattr(mod_, name, None)
    
        if cls is None:
            cls = getattr(QtWidgets, name, None) or \
            getattr(QtXml, name, None) or \
            getattr(QtGui, name, None) or \
            getattr(Qt, name, None) or \
            getattr(QtCore, name, None)                   
             
        return cls
    
    def createUI(self, n, connector=None, parent=None, name=None):
        
        if ".ui" not in n:
            n += ".ui"

        form_path = n if os.path.exists(n) else _path(n)

        if form_path is None:
            raise AttributeError("File %r not found in project" % n)
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
            if not qtWidgetPlugings in uic.widgetPluginPath:
                logger.info("Añadiendo path %s a uic.widgetPluginPath", qtWidgetPlugings)
                uic.widgetPluginPath.append(qtWidgetPlugings)
            uic.loadUi(form_path, w_)

        return w_

