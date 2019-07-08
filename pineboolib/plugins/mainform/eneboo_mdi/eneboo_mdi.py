# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QMainWindow  # type: ignore

from pineboolib import logging
from pineboolib.fllegacy.flapplication import aqApp

logger = logging.getLogger("mainForm_%s" % __name__)


class MainForm(QMainWindow):

    is_closing_ = False
    mdi_enable_ = True

    def __init__(self):
        super().__init__()
        aqApp.main_widget_ = self
        self.is_closing_ = False
        self.mdi_enable_ = True

    @classmethod
    def setDebugLevel(self, q):
        MainForm.debugLevel = q

    def initScript(self):
        from pineboolib.core.utils.utils_base import filedir

        mw = mainWindow
        mw.createUi(filedir("plugins/mainform/eneboo_mdi/mainform.ui"))
        aqApp.container_ = mw
        aqApp.init()

    def createUi(self, ui_file):
        from pineboolib.application import project

        mng = project.conn.managerModules()
        self.w_ = mng.createUI(ui_file, None, self)
        self.w_.setObjectName("container")


mainWindow = MainForm()
