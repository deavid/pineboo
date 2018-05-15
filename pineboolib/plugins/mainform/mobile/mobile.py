# -*- coding: utf-8 -*-
from pineboolib.plugins.mainform.pineboo.pineboo import MainForm, OutputWindow
from PyQt5 import uic
from pineboolib.utils import filedir


class MainForm(MainForm):

    def __init__(self):
        super(MainForm, self).__init__()

    def load(self):
        self.ui = uic.loadUi(
            filedir('plugins/mainform/mobile/mainform.ui'), self)

        super(MainForm, self).load()
        self.setWindowTitle("Pineboo Mobile")


mainWindow = MainForm()
