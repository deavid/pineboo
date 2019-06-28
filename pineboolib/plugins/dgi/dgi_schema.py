# # -*- coding: utf-8 -*-

from importlib import import_module

from pineboolib.fllegacy.aqsobjects.aqsettings import AQSettings
import logging

logger = logging.getLogger(__name__)


class dgi_schema(object):

    _desktopEnabled = False
    _mLDefault = False
    _name = None
    _alias = None
    _localDesktop = True
    _mobile = False
    _clean_no_python = True
    # FIXME: Guess this is because there is conditional code we don't want to run on certain DGI
    # .... this is really obscure. Please avoid at all costs. Having __NO_PYTHON__ is bad enough.
    _alternative_content_cached = False

    def __init__(self):
        # FIXME: This init is intended to be called only on certain conditions.
        # ... Worse than it seems: looks like this class is prepared to be constructed without
        # ... calling __init__, on purpose, to have different behavior than calling it.

        self._desktopEnabled = True  # Indica si se usa en formato escritorio con interface Qt
        self.setUseMLDefault(True)  # FIXME: Setters are wrong. Inside private context, even wronger.
        self.setLocalDesktop(True)
        self._name = "dgi_shema"
        self._alias = "Default Schema"
        self._show_object_not_found_warnings = True
        self.loadReferences()
        try:
            import PyQt5.QtAndroidExtras  # noqa   # FIXME

            self._mobile = True
            # FIXME: Did we just assume that we're running on android just because we found a library??
        except ImportError:
            self._mobile = False

        if AQSettings().readBoolEntry(u"ebcomportamiento/mobileMode", False):
            # FIXME: But now we enable mobile mode regardless of the library
            self._mobile = True
        # FIXME: Then, if not, can we disable it even if it is found? (...)

    def name(self):
        return self._name

    def alias(self):
        return self._alias

    # Establece un lanzador alternativo al de la aplicación
    def alternativeMain(self, options):
        pass

    def accept_file(self, name):
        return True

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

    def interactiveGUI(self):
        return "Pineboo"

    def processEvents(self):
        from PyQt5 import QtWidgets

        QtWidgets.qApp.processEvents()

    def show_object_not_found_warnings(self):
        return self._show_object_not_found_warnings

    def loadReferences(self):
        return

    def mobilePlatform(self):
        return self._mobile

    def isDeployed(self):
        """Returns True only if the code is running inside a PyInstaller bundle"""
        # FIXME: Delete me. This functionality DOES NOT DEPEND on which interface is being used.
        # .... a bundle is a bundle regardless of wether is running as jsonrpc or Qt.
        # .... A copy of this function has been moved to pineboolib.is_deployed() for convenience
        import sys

        return getattr(sys, "frozen", False)

    def iconSize(self):
        from PyQt5 import QtCore

        size = QtCore.QSize(22, 22)
        # if self.mobilePlatform():
        #    size = QtCore.QSize(60, 60)

        return size

    def alternative_content_cached(self):
        # FIXME: This is not needed. Use "content_cached" to return an exception or None, to signal
        # ... the module is unaware on how to perform the task
        # ... also the naming is bad. It conveys having done a cache in the past.
        return self._alternative_content_cached

    def alternative_script_path(self, script_name):
        # FIXME: Probably the same. Not needed.
        return None

    def use_model(self):
        return False

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

    def sys_mtds(self):
        return []

    def use_alternative_credentials(self):
        return False
