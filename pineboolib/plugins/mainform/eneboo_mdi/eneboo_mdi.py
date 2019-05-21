# -*- coding: utf-8 -*-
from pineboolib import decorators
from PyQt5 import QtWidgets, QtCore
from PyQt5.Qt import QIcon
from pineboolib.pncontrolsfactory import aqApp, AQS
from pineboolib.fllegacy.flaccesscontrollists import FLAccessControlLists

import logging
from PyQt5.QtWidgets import QMenu, QAction, QWidget, QVBoxLayout, QPushButton,\
    QToolBox, QSizePolicy
from PyQt5.QtGui import QKeySequence


logger = logging.getLogger("mainForm_%s" % __name__)


class MainForm(QtWidgets.QMainWindow):

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
        from pineboolib.utils import filedir
        
        
        mw = mainWindow
        mw.createUi(filedir('plugins/mainform/eneboo_mdi/mainform.ui'))
        aqApp.container_ = mw
        aqApp.init()
        
    
    def createUi(self, ui_file):
        mng = aqApp.db().managerModules()
        self.w_ = mng.createUI(ui_file, None, self)
        self.w_.setObjectName("container")
    

mainWindow = MainForm()
