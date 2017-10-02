# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from builtins import str
import os
from PyQt5 import QtWidgets, QtCore, uic

from pineboolib.utils import filedir
from pineboolib.PNSqlDrivers import PNSqlDrivers

class DlgConnect(QtWidgets.QWidget):
    ruta = ""
    username = ""
    password = ""
    hostname = ""
    portnumber = ""
    database = ""
    ui = None
        

    def load(self):
        self.ui = uic.loadUi(filedir('forms/dlg_connect.ui'), self)
        
        frameGm = self.frameGeometry()
        screen = QtWidgets.QApplication.desktop().screenNumber(QtWidgets.QApplication.desktop().cursor().pos())
        centerPoint = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
        
        self.ui.pbnStart.clicked.connect(self.conectar)
        self.ui.pbnSearchFolder.clicked.connect(self.findPathProject)
        DlgConnect.leFolder = self.ui.leFolder
        DlgConnect.leName = self.ui.leName
        DlgConnect.leUserName = self.ui.leUserName
        DlgConnect.lePassword = self.ui.lePassword
        DlgConnect.leHostName = self.ui.leHostName
        DlgConnect.lePort = self.ui.lePort
        DlgConnect.leDBName = self.ui.leDBName
        DlgConnect.cBDrivers = self.ui.cBDrivers
        
        DV = PNSqlDrivers()
        list = DV.aliasList()
        DlgConnect.cBDrivers.addItems(list)
        
        i = 0
        while i < DlgConnect.cBDrivers.count():
            if DV.aliasToName(DlgConnect.cBDrivers.itemText(i)) == DV.defaultDriverName:
                DlgConnect.cBDrivers.setCurrentIndex(i)
                break
            
            i = i + 1
    
    @QtCore.pyqtSlot()
    def conectar(self):
        folder_ =None
        
        if DlgConnect.leFolder.text():
            folder_ = DlgConnect.leFolder.text()
        else:
            folder_ = filedir("../projects")
            
        DlgConnect.ruta = filedir(str(folder_), str(DlgConnect.leName.text()))
        DlgConnect.username = DlgConnect.leUserName.text()
        DlgConnect.password = DlgConnect.lePassword.text()
        DlgConnect.hostname = DlgConnect.leHostName.text()
        DlgConnect.portnumber = DlgConnect.lePort.text()
        DlgConnect.database = DlgConnect.leDBName.text()
        DlgConnect.driveralias = DlgConnect.cBDrivers.currentText()

        if not DlgConnect.leName.text():
            DlgConnect.ruta = ""
        elif not DlgConnect.ruta.endswith(".xml"):
            DlgConnect.ruta += ".xml"
        if not os.path.isfile(DlgConnect.ruta) and DlgConnect.leName.text():
            QtWidgets.QMessageBox.information(self, "AVISO", "El proyecto \n" + DlgConnect.ruta +" no existe")
            DlgConnect.ruta = None
        else:
            self.close()
    
    @QtCore.pyqtSlot()       
    def findPathProject(self):
        filename = QtWidgets.QFileDialog.getExistingDirectory(self, "Seleccione Directorio")
        if filename:
            DlgConnect.leFolder.setText(str(filename))
