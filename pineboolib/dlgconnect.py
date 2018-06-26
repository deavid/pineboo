# -*- coding: utf-8 -*-
from builtins import str
import os
import sys
import traceback
import logging
import base64

from xml import etree
from xml.etree.ElementTree import Element, SubElement, ElementTree

from pineboolib.pnsqldrivers import PNSqlDrivers
from pineboolib.utils import filedir

from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtWidgets import QTableWidgetItem, QFrame, QMessageBox
from PyQt5.QtCore import QFileInfo, QSize
from PyQt5.Qt import QWidget

"""
Esta clase muestra gestiona el dialogo de Login
"""


class DlgConnect(QtWidgets.QWidget):
    _DGI = None
    optionsShowed = True
    minSize = None
    maxSize = None
    profileDir = None

    """
    Constructor
    @param _DGI. DGI cargado.
    """

    def __init__(self, _DGI):
        super(DlgConnect, self).__init__()
        self._DGI = _DGI
        self.optionsShowed = True
        self.minSize = QSize(350, 140)
        self.maxSize = QSize(350, 495)
        self.profileDir = filedir("../profiles")

    """
    Carga el form dlg_connect
    """

    def load(self):
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
        self.showOptions()
        self.loadProfiles()
    """
    SLOTS
    """

    """
    Muestra el frame opciones
    """
    @QtCore.pyqtSlot()
    def showOptions(self):
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

    """
    Actualiza el ComboBox de los perfiles
    """

    def loadProfiles(self):
        self.ui.cbProfiles.clear()
        if not os.path.exists(self.profileDir):
            os.mkdir(filedir(self.profileDir))

        files = [f for f in os.listdir(self.profileDir) if os.path.isfile(os.path.join(self.profileDir, f))]
        for file in files:
            fileName = file.split(".")[0]
            self.ui.cbProfiles.addItem(fileName)

    """
    Abre la conexión seleccionada
    """
    @QtCore.pyqtSlot()
    def open(self):
        print("lanzando!!")

    """
    Guarda la conexión
    """
    @QtCore.pyqtSlot()
    def saveProfile(self):
        profile = Element("Profile")
        description = self.ui.leDescription.text()
        dbt = self.ui.cbDBType.currentText()
        url = self.ui.leURL.text()
        port = self.ui.lePort.text()
        userDB = self.ui.leDBUser.text()
        passwDB = self.ui.leDBPassword.text()  # Base 64?
        nameDB = self.ui.leDBName.text()
        passProfile = self.ui.leProfilePassword.text()  # base 64?
        autoLogin = self.ui.cbAutoLogin.isChecked()

        name = SubElement(profile, "name")
        name.text = description
        dbs = SubElement(profile, "database-server")
        dbstype = SubElement(dbs, "type")
        dbstype.text = dbt
        dbshost = SubElement(dbs, "host")
        dbshost.text = url
        dbsport = SubElement(dbs, "port")
        dbsport.text = port

        dbc = SubElement(profile, "database-credentials")
        dbcuser = SubElement(dbc, "username")
        dbcuser.text = userDB
        dbcpasswd = SubElement(dbc, "password")
        dbcpasswd.text = base64.b64encode(passwDB.encode()).decode()
        dbname = SubElement(profile, "database-name")
        dbname.text = nameDB
        profile_user = SubElement(profile, "profile-data")
        if not autoLogin:
            profile_password = SubElement(profile_user, "password")
            profile_password.text = base64.b64encode(passProfile.encode()).decode()

        tree = ElementTree(profile)
        tree.write(os.path.join(self.profileDir, "%s.xml" % description), xml_declaration=True, encoding='utf-8')
        self.cleanProfileForm()

    """
    Borra la conexión seleccionada
    """
    @QtCore.pyqtSlot()
    def deleteProfile(self):
        if self.ui.cbProfiles.count() > 0:
            res = QMessageBox.warning(
                self.ui, "Pineboo", "¿Desea borrar el perfil %s?" % self.ui.cbProfiles.currentText(),
                QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
            if res == QtWidgets.QMessageBox.No:
                return

            fileName = "%s.xml" % self.ui.cbProfiles.currentText()
            os.remove(os.path.join(self.profileDir, fileName))
            self.loadProfiles()

    def cleanProfileForm(self):
        self.ui.leDescription.setText("")
        # FIX cargar drivers y poner el por defecto
        # Conectar el changeitem del driver para actualizar el numero de puerto
        self.ui.leURL.setText("localhost")
        self.ui.lePort.setText("")
        self.ui.leDBUser.setText("")
        self.ui.leDBPassword.setText("")
        self.ui.leDBName.setText("")
        self.ui.leProfilePassword.setText("")
        self.ui.cbAutoLogin.setChecked(False)
