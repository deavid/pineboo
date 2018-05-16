# -*- coding: utf-8 -*-
from pineboolib.plugins.mainform.pineboo.pineboo import MainForm, OutputWindow
from PyQt5 import uic
from pineboolib.utils import filedir
from pineboolib.fllegacy.FLSettings import FLSettings


class MainForm(MainForm):

    def __init__(self):
        super(MainForm, self).__init__()

    def load(self):
        self.ui = uic.loadUi(
            filedir('plugins/mainform/mobile/mainform.ui'), self)

        sett_ = FLSettings()
        sett_.writeEntry("application/isDebuggerMode", True)

        super(MainForm, self).load()
        self.setWindowTitle("Pineboo Mobile")


mainWindow = MainForm()
