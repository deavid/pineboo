# -*- coding: utf-8 -*-
from pineboolib import logging
from PyQt5.QtWidgets import QMainWindow  # type: ignore

logger = logging.getLogger("mainForm_%s" % __name__)


class MainForm(QMainWindow):

    is_closing_ = False
    mdi_enable_ = True

    def __init__(self):
        super().__init__()
        from pineboolib import pncontrolsfactory

        pncontrolsfactory.aqApp.main_widget_ = self
        self.is_closing_ = False
        self.mdi_enable_ = True

    @classmethod
    def setDebugLevel(self, q):
        MainForm.debugLevel = q

    def initScript(self):
        from pineboolib.core.utils.utils_base import filedir
        from pineboolib import pncontrolsfactory

        mw = mainWindow
        mw.createUi(filedir("plugins/mainform/eneboo_mdi/mainform.ui"))
        pncontrolsfactory.aqApp.container_ = mw
        pncontrolsfactory.aqApp.init()

    def createUi(self, ui_file):
        from pineboolib import project

        mng = project.conn.managerModules()
        self.w_ = mng.createUI(ui_file, None, self)
        self.w_.setObjectName("container")


mainWindow = MainForm()
