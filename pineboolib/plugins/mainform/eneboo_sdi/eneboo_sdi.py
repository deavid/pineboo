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
        mw.createUi(filedir('plugins/mainform/eneboo_sdi/mainform.ui'))     
        aqApp.dict_main_widgets_ = []
        mw.setObjectName("container")
        mw.setWindowIcon(QIcon(AQS.Pixmap_fromMineSource("pineboo.png")))
        if aqApp.db():
            mw.setWindowTitle(aqApp.db().database())
        else:
            mw.setWindowTitle("Eneboo %s" % pineboolib.project.version)
        
        #FLDiskCache.init(self)
        
        window_menu = QMenu(mw)
        window_menu.setObjectName("windowMenu")
        
    
        
        window_cascade_action = QAction(QIcon(AQS.Pixmap_fromMineSource("cascada.png")), self.tr("Cascada"), mw)
        window_menu.addAction(window_cascade_action)
        
        
        window_tile_action = QAction(QIcon(AQS.Pixmap_fromMineSource("mosaico.png")), self.tr("Mosaico"), mw)
        window_menu.addAction(window_tile_action)
        
        window_close_action = QAction(QIcon(AQS.Pixmap_fromMineSource("cerrar.png")), self.tr("Cerrar"), mw)
        window_menu.addAction(window_close_action)
        
        modules_menu = QMenu(mw)
        modules_menu.setObjectName("modulesMenu")
        #self.modules_menu.setCheckable(False)

        w = QWidget(mw)
        w.setObjectName("widgetContainer")
        vl = QVBoxLayout(w)
        
        exit_button = QPushButton(QIcon(AQS.Pixmap_fromMineSource("exit.png")), self.tr("Salir"), w)
        exit_button.setObjectName("pbSalir")
        exit_button.setShortcut(QKeySequence(self.tr("Ctrl+Q")))
        exit_button.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))
        exit_button.setFocusPolicy(QtCore.Qt.NoFocus)
        exit_button.setToolTip(self.tr("Salir de la aplicación (Ctrl+Q)"))
        exit_button.setWhatsThis(self.tr("Salir de la aplicación (Ctrl+Q)"))
        exit_button.clicked.connect(self.close)
        
        tool_box_ = QToolBox(w)
        tool_box_.setObjectName("toolBox")
        
        vl.addWidget(exit_button)
        vl.addWidget(tool_box_)
        mw.setCentralWidget(w)
    
        
        aqApp.db().manager().init()
        #self.mng_loader_.init()
        
        aqApp.initStyles()
        aqApp.initMenuBar()
        

        aqApp.db().manager().loadTables()
        #self.mng_loader_.loadKeyFiles()
        #self.mng_loader_.loadAllIdModules()
        #self.mng_loader_.loadIdAreas()
        aqApp.db().managerModules().loadKeyFiles()
        aqApp.db().managerModules().loadAllIdModules()
        aqApp.db().managerModules().loadIdAreas()
        
        aqApp.acl_ = FLAccessControlLists()
        #self.acl_.init()
        
        #self.loadScripts()
        #self.mng_loader_.setShaLocalFromGlobal()
        aqApp.db().managerModules().setShaLocalFromGlobal()
        aqApp.loadTranslations()
        
        aqApp.call("sys.init", [])
        aqApp.initToolBox()
        aqApp.readState()
        
        mw.installEventFilter(self)
        aqApp.startTimerIdle()
        
    
    def createUi(self, ui_file):
        mng = aqApp.db().managerModules()
        self.w_ = mng.createUI(ui_file, None, self)
        self.w_.setObjectName("container")
    
    def eventFilter(self, o, e):
        if isinstance(e, AQS.Close):
            if isinstance(o, MainForm):
                if not self.is_closing_:
                    self.w_.setDisabled(True)
                    ret = aqApp.generalExit(True) 
                    if ret == False:
                        self.w_.setDisabled(False)
                        e.ignore()
                    else:
                        self.is_closing_ = True
                    
                    return True
        
        return False

mainWindow = MainForm()
