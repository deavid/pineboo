# # -*- coding: utf-8 -*-

from pineboo.pineboolib.plugins.dgi.dgi_schema import dgi_schema
from pineboo.pineboolib.utils import Struct
from pineboo.pineboolib import decorators
import pineboo.pineboolib


from importlib import import_module
from PyQt5 import QtCore

import traceback
import logging
import sys

logger = logging.getLogger(__name__)



class dgi_aqnext(dgi_schema):


    def __init__(self):
        # desktopEnabled y mlDefault a True
        super().__init__()
        self._name = "aqnext"
        self._alias = "AQNEXT"
        self.setUseDesktop(True)
        self.setUseMLDefault(True)
        self.setLocalDesktop(False)
        self._mainForm = None
        self.showInitBanner()

    def extraProjectInit(self):
        pass
    
    def create_app(self):
        app = QtCore.QCoreApplication(sys.argv)
        return app

    def setParameter(self, param):
        self._listenSocket = param

    def mainForm(self):
        if not self._mainForm:
            self._mainForm = mainForm()
        return self._mainForm

    def __getattr__(self, name):
        return super().resolveObject(self._name, name)
