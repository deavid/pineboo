# -*- coding: utf-8 -*-
from builtins import str
import os
import sys
import traceback
import logging
import base64

import xml

from pineboolib.pnsqldrivers import PNSqlDrivers
from pineboolib.utils import filedir

from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtWidgets import QTableWidgetItem, QFrame, QMessageBox
from PyQt5.QtCore import QFileInfo, QSize
from PyQt5.Qt import QWidget


class DlgConnect(QtWidgets.QWidget):
    """
    Esta clase muestra gestiona el dialogo de Login
    """
    _DGI = None
    optionsShowed = True
    minSize = None
    maxSize = None
    profileDir = None
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
        self.profileDir = filedir("../profiles")
        self.pNSqlDrivers = PNSqlDrivers()

    def load(self):
        """
        Carga el form dlg_connect
        """
        dlg_ = filedir('forms/dlg_connect.ui')

        self.ui = uic.loadUi(dlg_, self)

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
        self.showOptions()
        self.loadProfiles()

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
        if not os.path.exists(self.profileDir):
            os.mkdir(filedir(self.profileDir))

        files = [f for f in os.listdir(self.profileDir) if os.path.isfile(os.path.join(self.profileDir, f))]
        for file in files:
            fileName = file.split(".")[0]
            self.ui.cbProfiles.addItem(fileName)

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
        fileName = os.path.join(self.profileDir, "%s.xml" % self.ui.cbProfiles.currentText())
        tree = xml.etree.ElementTree.parse(fileName)
        root = tree.getroot()

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
            self.password = base64.b64decode(ps).decode()

        self.close()

    @QtCore.pyqtSlot()
    def saveProfile(self):
        """
        Guarda la conexión
        """
        profile = xml.etree.ElementTree.Element("Profile")
        description = self.ui.leDescription.text()

        if os.path.exists(os.path.join(self.profileDir, "%s.xml" % description)):
            QMessageBox.information(self.ui, "Pineboo", "El perfil ya existe")
            return

        dbt = self.ui.cbDBType.currentText()
        url = self.ui.leURL.text()
        port = self.ui.lePort.text()
        userDB = self.ui.leDBUser.text()
        passwDB = self.ui.leDBPassword.text()  # Base 64?
        nameDB = self.ui.leDBName.text()
        passProfile = self.ui.leProfilePassword.text()  # base 64?
        autoLogin = self.ui.cbAutoLogin.isChecked()

        name = xml.etree.ElementTree.SubElement(profile, "name")
        name.text = description
        dbs = xml.etree.ElementTree.SubElement(profile, "database-server")
        dbstype = xml.etree.ElementTree.SubElement(dbs, "type")
        dbstype.text = dbt
        dbshost = xml.etree.ElementTree.SubElement(dbs, "host")
        dbshost.text = url
        dbsport = xml.etree.ElementTree.SubElement(dbs, "port")
        dbsport.text = port

        dbc = xml.etree.ElementTree.SubElement(profile, "database-credentials")
        dbcuser = xml.etree.ElementTree.SubElement(dbc, "username")
        dbcuser.text = userDB
        dbcpasswd = xml.etree.ElementTree.SubElement(dbc, "password")
        dbcpasswd.text = base64.b64encode(passwDB.encode()).decode()
        dbname = xml.etree.ElementTree.SubElement(profile, "database-name")
        dbname.text = nameDB
        profile_user = xml.etree.ElementTree.SubElement(profile, "profile-data")
        if not autoLogin:
            profile_password = xml.etree.ElementTree.SubElement(profile_user, "password")
            profile_password.text = base64.b64encode(passProfile.encode()).decode()

        tree = xml.etree.ElementTree.ElementTree(profile)

        tree.write(os.path.join(self.profileDir, "%s.xml" % description), xml_declaration=True, encoding='utf-8')
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
            os.remove(os.path.join(self.profileDir, fileName))
            self.loadProfiles()

    @QtCore.pyqtSlot(int)
    def updatePort(self):
        """
        Actualiza al puerto por defecto del driver
        """
        self.ui.lePort.setText(self.pNSqlDrivers.port(self.ui.cbDBType.currentText()))

    @QtCore.pyqtSlot(int)
    def enablePassword(self):
        """
        Comprueba si el perfil requiere password para login o no
        """
        if self.ui.cbProfiles.count() == 0:
            return
        password = None
        fileName = os.path.join(self.profileDir, "%s.xml" % self.ui.cbProfiles.currentText())
        tree = xml.etree.ElementTree.parse(fileName)
        root = tree.getroot()

        for profile in root.findall("profile-data"):
            password = profile.find("password")

        if password is None:
            self.ui.lePassword.setEnabled(False)
        else:
            self.ui.lePassword.setEnabled(True)
