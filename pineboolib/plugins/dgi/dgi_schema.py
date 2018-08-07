# # -*- coding: utf-8 -*-
from PyQt5 import QtCore


from importlib import import_module

from pineboolib.fllegacy.aqsobjects.AQSettings import AQSettings
import pineboolib
import sys
import datetime
import re
import logging

logger = logging.getLogger(__name__)


def resolveObject(name):
    mod_ = import_module(__name__)
    ret_ = getattr(mod_, name, None)
    return ret_


class dgi_schema(object):

    _desktopEnabled = False
    _mLDefault = False
    _name = None
    _alias = None
    _localDesktop = True
    _mobile = False
    _deployed = False

    def __init__(self):
        self._desktopEnabled = True  # Indica si se usa en formato escritorio con interface Qt
        self.setUseMLDefault(True)
        self.setLocalDesktop(True)
        self._name = "dgi_shema"
        self._alias = "Default Schema"
        self.loadReferences()
        try:
            import PyQt5.QtAndroidExtras
            self._mobile = True
        except ImportError:
            self._mobile = False

        if AQSettings().readBoolEntry(u"ebcomportamiento/mobileMode", False):
            self._mobile = True

        try:
            from pdytools import hexversion as pdy_hexversion
            self._deployed = True
        except ImportError:
            self._deployed = False

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
        print("                 %s MODE               " % self._alias)
        print("=============================================")
        print("")
        print("")

    def mainForm(self):
        pass

    def loadReferences(self):
        return

    def mobilePlatform(self):
        return self._mobile

    def isDeployed(self):
        return self._deployed

    def iconSize(self):
        size = QtCore.QSize(22, 22)
        if self.mobilePlatform():
            size = QtCore.QSize(60, 60)

        return size

    def __getattr__(self, name):
        return resolveObject(name)
