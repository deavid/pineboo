from __future__ import unicode_literals
from builtins import str
# encoding: UTF-8
import os
from PyQt4 import QtGui, QtCore, uic

from pineboolib.utils import filedir

class DlgConnect(QtGui.QWidget):
    ruta = ""
    ui = None

    def load(self):
        self.ui = uic.loadUi(filedir('forms/dlg_connect.ui'), self)
        self.connect(self.ui.pbnStart, QtCore.SIGNAL("clicked()"), self.conectar)
        self.connect(self.ui.pbnSearchFolder, QtCore.SIGNAL("clicked()"), self.findPathProject)
        DlgConnect.leFolder = self.ui.leFolder
        DlgConnect.leName = self.ui.leName

    def conectar(self):
        DlgConnect.ruta = filedir(str(DlgConnect.leFolder.text()), str(DlgConnect.leName.text()))
        if not DlgConnect.ruta.endswith(".xml"):
            DlgConnect.ruta += ".xml"
        if not os.path.isfile(DlgConnect.ruta):
            QtGui.QMessageBox.information(self, "AVISO", "El proyecto \n" + DlgConnect.ruta +" no existe")
            DlgConnect.ruta = None
        else:
            self.close()
    def findPathProject(self):
        filename = QtGui.QFileDialog.getExistingDirectory(self, "Seleccione Directorio")
        if filename:
            DlgConnect.leFolder.setText(str(filename))
