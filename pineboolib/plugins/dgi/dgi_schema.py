# # -*- coding: utf-8 -*-

from importlib import import_module

from pineboolib.fllegacy.aqsobjects.aqsettings import AQSettings
import pineboolib
import re
import logging

logger = logging.getLogger(__name__)


class dgi_schema(object):

    _desktopEnabled = False
    _mLDefault = False
    _name = None
    _alias = None
    _localDesktop = True
    _mobile = False
    _deployed = False
    _clean_no_python = True
    _clean_no_python_changeable = True
    _alternative_content_cached = False

    def __init__(self):
        self._desktopEnabled = True  # Indica si se usa en formato escritorio con interface Qt
        self.setUseMLDefault(True)
        self.setLocalDesktop(True)
        self._name = "dgi_shema"
        self._alias = "Default Schema"
        self._show_object_not_found_warnings = True
        self.loadReferences()
        try:
            import PyQt5.QtAndroidExtras
            self._mobile = True
        except ImportError:
            self._mobile = False

        if AQSettings().readBoolEntry(u"ebcomportamiento/mobileMode", False):
            self._mobile = True

        from pineboolib.utils import imFrozen
        self._deployed = imFrozen()
        self.set_clean_no_python(True)
        self.set_clean_no_python_changeable(False)

    def name(self):
        return self._name

    def alias(self):
        return self._alias

    # Establece un lanzador alternativo al de la aplicación
    def alternativeMain(self, options):
        pass

    def useDesktop(self):
        return self._desktopEnabled

    def setUseDesktop(self, val):
        self._desktopEnabled = val

    def localDesktop(self):  # Indica si son ventanas locales o remotas a traves de algún parser
        return self._localDesktop

    def setLocalDesktop(self, val):
        self._localDesktop = val

    def setUseMLDefault(self, val):
        self._mLDefault = val

    def useMLDefault(self):
        return self._mLDefault

    def setParameter(self, param):  # Se puede pasar un parametro al dgi
        pass

    def extraProjectInit(self):
        pass

    def showInitBanner(self):
        print("")
        print("=============================================")
        print("                GDI_%s MODE               " % self._alias)
        print("=============================================")
        print("")
        print("")

    def mainForm(self):
        pass
    
    def show_object_not_found_warnings(self):
        return self._show_object_not_found_warnings

    def loadReferences(self):
        return

    def mobilePlatform(self):
        return self._mobile

    def isDeployed(self):
        return self._deployed

    def iconSize(self):
        from PyQt5 import QtCore
        size = QtCore.QSize(22, 22)
        if self.mobilePlatform():
            size = QtCore.QSize(60, 60)

        return size
    
    def clean_no_python(self):
        return self._clean_no_python
    
    def set_clean_no_python(self, b):
        if self._clean_no_python_changeable:
            self._clean_no_python = b
    
    def clean_no_python_changeable(self):
        return self._clean_no_python_changeable
    
    def set_clean_no_python_changeable(self, b):
        self._clean_no_python_changeable = b
    
    def alternative_content_cached(self):
        return self._alternative_content_cached
    
    def alternative_path(self, script_name):
        return None

    def __getattr__(self, name):
        return self.resolveObject(self._name, name)

    def resolveObject(self, module_name, name):
        cls = None
        try:
            mod_ = import_module("pineboolib.plugins.dgi.dgi_%s.dgi_objects.%s" % (module_name, name.lower()))
            cls = getattr(mod_, name, None)
        except Exception:
            pass
        return cls