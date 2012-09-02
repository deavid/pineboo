# encoding: UTF-8
import os
from PyQt4 import QtGui, QtCore, uic
import main

class DlgConnect(QtGui.QWidget):
    def load(self):
        self.ui = uic.loadUi(main.filedir('forms/dlg_connect.ui'), self)
        self.connect(self.ui.pbnStart,QtCore.SIGNAL("clicked()"),self.conectar)
        self.connect(self.ui.pbnSearchFolder,QtCore.SIGNAL("clicked()"),self.findPathProject)
        DlgConnect.leFolder = self.ui.leFolder
        DlgConnect.leName = self.ui.leName
    
    ruta=""    
        
    def conectar(self):
        DlgConnect.ruta = main.filedir(str(DlgConnect.leFolder.text()) , str(DlgConnect.leName.text()))
        if not DlgConnect.ruta.endswith(".xml"): 
            DlgConnect.ruta += ".xml"        
        if not os.path.isfile(DlgConnect.ruta):
            QtGui.QMessageBox.information(self, "AVISO","El proyecto \n" + DlgConnect.ruta +" no existe") 
            DlgConnect.ruta = None
        else:        
            self.close()       
        
    def findPathProject(self):
        filename = QtGui.QFileDialog.getExistingDirectory(self,"Seleccione Directorio")
        if filename:
                DlgConnect.leFolder.setText(unicode(filename))
        
        
