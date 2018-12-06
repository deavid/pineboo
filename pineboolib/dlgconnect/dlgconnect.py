# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtWidgets import QTableWidgetItem, QFrame, QMessageBox, QFileDialog
from PyQt5.QtCore import QFileInfo, QSize
from PyQt5.Qt import QWidget

from pineboolib.utils import filedir, indent
from pineboolib.fllegacy.flsettings import FLSettings

from builtins import str
import os
import sys
import traceback
import logging
import base64
import xml
from xml.etree import ElementTree as ET


class DlgConnect(QtWidgets.QWidget):
    """
    Esta clase muestra gestiona el dialogo de Login
    """
    _DGI = None
    optionsShowed = True
    minSize = None
    maxSize = None
    profile_dir = None
    pNSqlDrivers = None

    def __init__(self, _DGI):
        """
        Constructor
        @param _DGI. DGI cargado.
        """
        super(DlgConnect, self).__init__()
        self._DGI = _DGI
        self.optionsShowed = True
        self.minSize = QSize(350, 140)
        self.maxSize = QSize(350, 495)
        self.profile_dir = FLSettings().readEntry("ebcomportamiento/profiles_folder", filedir("../profiles"))
        import pineboolib
        self.pNSqlDrivers = pineboolib.project.sql_drivers_manager

    def load(self):
        """
        Carga el form dlgconnect
        """
        from pineboolib.fllegacy.flmanagermodules import FLManagerModules
        mM = FLManagerModules()
        dlg_ = filedir('dlgconnect/dlgconnect.ui')

        self.ui = mM.createUI(dlg_, None, self)
        del mM

        # Centrado en pantalla
        frameGm = self.frameGeometry()
        screen = QtWidgets.QApplication.desktop().screenNumber(QtWidgets.QApplication.desktop().cursor().pos())
        centerPoint = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
        
        
        self.ui.pbLogin.clicked.connect(self.open)
        self.ui.tbOptions.clicked.connect(self.showOptions)
        self.ui.pbSaveConnection.clicked.connect(self.saveProfile)
        self.ui.tbDeleteProfile.clicked.connect(self.deleteProfile)
        self.cleanProfileForm()
        self.ui.cbDBType.currentIndexChanged.connect(self.updatePort)
        self.ui.cbProfiles.currentIndexChanged.connect(self.enablePassword)
        self.ui.cbAutoLogin.stateChanged.connect(self.enableProfilePassword)
        self.ui.le_profiles.setText(self.profile_dir)
        self.ui.tb_profiles.clicked.connect(self.change_profile_dir)
        self.showOptions()
        self.loadProfiles()
        self.ui.leDescription.textChanged.connect(self.updateDBName)

    def cleanProfileForm(self):
        """
        Limpia el tab de creación de profiles , y rellena los datos básicos del driver SQL por defecto
        """
        self.ui.leDescription.setText("")
        driver_list = self.pNSqlDrivers.aliasList()
        self.ui.cbDBType.clear()
        self.ui.cbDBType.addItems(driver_list)
        self.ui.cbDBType.setCurrentText(self.pNSqlDrivers.defaultDriverName)
        self.ui.leURL.setText("localhost")
        self.ui.leDBUser.setText("")
        self.ui.leDBPassword.setText("")
        self.ui.leDBName.setText("")
        self.ui.leProfilePassword.setText("")
        self.ui.cbAutoLogin.setChecked(False)
        self.updatePort()

    def loadProfiles(self):
        """
        Actualiza el ComboBox de los perfiles
        """
        self.ui.cbProfiles.clear()
        if not os.path.exists(self.profile_dir):
            #os.mkdir(filedir(self.profile_dir))
            return
        
        files = [f for f in os.listdir(self.profile_dir) if os.path.isfile(os.path.join(self.profile_dir, f))]
        for file in files:
            fileName = file.split(".")[0]
            self.ui.cbProfiles.addItem(fileName)

        settings = FLSettings()
        last_profile = settings.readEntry("DBA/last_profile", None)
        if last_profile:
            self.ui.cbProfiles.setCurrentText(last_profile)

    """
    SLOTS
    """

    @QtCore.pyqtSlot()
    def showOptions(self):
        """
        Muestra el frame opciones
        """
        if self.optionsShowed:
            self.ui.frmOptions.hide()
            self.ui.tbDeleteProfile.hide()
            self.ui.setMinimumSize(self.minSize)
            self.ui.setMaximumSize(self.minSize)
            self.ui.resize(self.minSize)
        else:
            self.ui.frmOptions.show()
            self.ui.tbDeleteProfile.show()
            self.ui.setMinimumSize(self.maxSize)
            self.ui.setMaximumSize(self.maxSize)
            self.ui.resize(self.maxSize)

        self.optionsShowed = not self.optionsShowed

    @QtCore.pyqtSlot()
    def open(self):
        """
        Abre la conexión seleccionada
        """
        fileName = os.path.join(self.profile_dir, "%s.xml" % self.ui.cbProfiles.currentText())
        tree = ET.parse(fileName)
        root = tree.getroot()
        last_profile = self.ui.cbProfiles.currentText()
        if last_profile not in (None, ""):
            settings = FLSettings()
            settings.writeEntry("DBA/last_profile", last_profile)

        for profile in root.findall("profile-data"):
            if getattr(profile.find("password"), "text", None):
                psP = profile.find("password").text
                psP = base64.b64decode(psP).decode()
                if psP:
                    if self.ui.lePassword.text() != psP:
                        QMessageBox.information(self.ui, "Pineboo", "Contraseña Incorrecta")
                        return

        self.database = root.find("database-name").text
        for db in root.findall("database-server"):
            self.hostname = db.find("host").text
            self.portnumber = db.find("port").text
            self.driveralias = db.find("type").text

        for credentials in root.findall("database-credentials"):
            self.username = credentials.find("username").text
            ps = credentials.find("password").text
            if ps:
                self.password = base64.b64decode(ps).decode()
            else:
                self.password = ""

        if self.pNSqlDrivers.isDesktopFile(self.driveralias):
            self.database = "tempdata/%s.sqlite3" % self.database

        self.close()

    @QtCore.pyqtSlot()
    def saveProfile(self):
        """
        Guarda la conexión
        """
        profile = ET.Element("Profile")
        description = self.ui.leDescription.text()
        
        if not os.path.exists(self.profile_dir):
            os.mkdir(filedir(self.profile_dir))

        if os.path.exists(os.path.join(self.profile_dir, "%s.xml" % description)):
            QMessageBox.information(self.ui, "Pineboo", "El perfil ya existe")
            return

        dbt = self.ui.cbDBType.currentText()
        url = self.ui.leURL.text()
        port = self.ui.lePort.text()
        userDB = self.ui.leDBUser.text()
        if self.ui.leDBPassword.text() != self.ui.leDBPassword2.text():
            QMessageBox.information(self.ui, "Pineboo", "La contraseña de la BD no coincide")
            self.ui.leDBPassword.setText("")
            self.ui.leDBPassword2.setText("")
            return

        passwDB = self.ui.leDBPassword.text()  # Base 64?
        nameDB = self.ui.leDBName.text()
        passProfile = self.ui.leProfilePassword.text()  # base 64?
        autoLogin = self.ui.cbAutoLogin.isChecked()

        name = ET.SubElement(profile, "name")
        name.text = description
        dbs = ET.SubElement(profile, "database-server")
        dbstype = ET.SubElement(dbs, "type")
        dbstype.text = dbt
        dbshost = ET.SubElement(dbs, "host")
        dbshost.text = url
        dbsport = ET.SubElement(dbs, "port")
        dbsport.text = port

        dbc = ET.SubElement(profile, "database-credentials")
        dbcuser = ET.SubElement(dbc, "username")
        dbcuser.text = userDB
        dbcpasswd = ET.SubElement(dbc, "password")
        dbcpasswd.text = base64.b64encode(passwDB.encode()).decode()
        dbname = ET.SubElement(profile, "database-name")
        dbname.text = nameDB
        profile_user = ET.SubElement(profile, "profile-data")
        if not autoLogin:
            profile_password = ET.SubElement(profile_user, "password")
            profile_password.text = base64.b64encode(passProfile.encode()).decode()

        indent(profile)

        tree = ET.ElementTree(profile)

        tree.write(os.path.join(self.profile_dir, "%s.xml" % description), xml_declaration=True, encoding='utf-8')
        # self.cleanProfileForm()
        self.loadProfiles()

    @QtCore.pyqtSlot()
    def deleteProfile(self):
        """
        Borra la conexión seleccionada
        """
        if self.ui.cbProfiles.count() > 0:
            res = QMessageBox.warning(
                self.ui, "Pineboo", "¿Desea borrar el perfil %s?" % self.ui.cbProfiles.currentText(),
                QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
            if res == QtWidgets.QMessageBox.No:
                return

            fileName = "%s.xml" % self.ui.cbProfiles.currentText()
            os.remove(os.path.join(self.profile_dir, fileName))
            self.loadProfiles()

    @QtCore.pyqtSlot(int)
    def updatePort(self):
        """
        Actualiza al puerto por defecto del driver
        """
        self.ui.lePort.setText(self.pNSqlDrivers.port(self.ui.cbDBType.currentText()))

    @QtCore.pyqtSlot(int)
    def enablePassword(self, n = None):
        """
        Comprueba si el perfil requiere password para login o no
        """
        if self.ui.cbProfiles.count() == 0:
            return
        password = None
        fileName = os.path.join(self.profile_dir, "%s.xml" % self.ui.cbProfiles.currentText())
        try:
            tree = ET.parse(fileName)
            root = tree.getroot()
        except Exception:
            QMessageBox.warning(self.ui,"Pineboo", "El perfil %s no parece válido" % self.ui.cbProfiles.currentText() ,QtWidgets.QMessageBox.Ok)
            return

        for profile in root.findall("profile-data"):
            password = profile.find("password")

        if password is None:
            self.ui.lePassword.setEnabled(False)
        else:
            self.ui.lePassword.setEnabled(True)

    def updateDBName(self):
        """
        Actualiza el nombre de la BD con el nombre de la descripción
        """
        self.ui.leDBName.setText(self.ui.leDescription.text())

    @QtCore.pyqtSlot(int)
    def enableProfilePassword(self):
        """
        Comprueba si el perfil requiere password
        """

        if self.ui.cbAutoLogin.isChecked():
            self.ui.leProfilePassword.setEnabled(False)
        else:
            self.ui.leProfilePassword.setEnabled(True)
    
    def change_profile_dir(self):
        
        new_dir = QtWidgets.QFileDialog.getExistingDirectory(self.ui, self.tr("Carpeta profiles"), self.profile_dir, QtWidgets.QFileDialog.ShowDirsOnly)
        
        if new_dir and new_dir is not self.profile_dir:
            FLSettings().writeEntry("ebcomportamiento/profiles_folder", new_dir)
            self.profile_dir = new_dir
            self.loadProfiles()
        
    
