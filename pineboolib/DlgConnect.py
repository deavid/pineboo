from __future__ import unicode_literals
from builtins import str
# encoding: UTF-8
import os
from PyQt4 import QtGui, QtCore, uic

from pineboolib.utils import filedir

class DlgConnect(QtGui.QWidget):
    ruta = ""
    username = ""
    password = ""
    hostname = ""
    portnumber = ""
    database = ""
    ui = None

    def load(self):
        self.ui = uic.loadUi(filedir('forms/dlg_connect.ui'), self)
        self.connect(self.ui.pbnStart, QtCore.SIGNAL("clicked()"), self.conectar)
        self.connect(self.ui.pbnSearchFolder, QtCore.SIGNAL("clicked()"), self.findPathProject)
        DlgConnect.leFolder = self.ui.leFolder
        DlgConnect.leName = self.ui.leName
        DlgConnect.leUserName = self.ui.leUserName
        DlgConnect.lePassword = self.ui.lePassword
        DlgConnect.leHostName = self.ui.leHostName
        DlgConnect.lePort = self.ui.lePort
        DlgConnect.leDBName = self.ui.leDBName

    def conectar(self):
        DlgConnect.ruta = filedir(str(DlgConnect.leFolder.text()), str(DlgConnect.leName.text()))
        DlgConnect.username = DlgConnect.leUserName.text()
        DlgConnect.password = DlgConnect.lePassword.text()
        DlgConnect.hostname = DlgConnect.leHostName.text()
        DlgConnect.portnumber = DlgConnect.lePort.text()
        DlgConnect.database = DlgConnect.leDBName.text()

        if not DlgConnect.leName.text():
            DlgConnect.ruta = ""
        elif not DlgConnect.ruta.endswith(".xml"):
            DlgConnect.ruta += ".xml"
        if not os.path.isfile(DlgConnect.ruta) and DlgConnect.leName.text():
            QtGui.QMessageBox.information(self, "AVISO", "El proyecto \n" + DlgConnect.ruta +" no existe")
            DlgConnect.ruta = None
        else:
            self.close()
    def findPathProject(self):
        filename = QtGui.QFileDialog.getExistingDirectory(self, "Seleccione Directorio")
        if filename:
            DlgConnect.leFolder.setText(str(filename))
