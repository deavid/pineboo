# -*- coding: utf-8 -*-
import os
import base64
import hashlib
from xml.etree import ElementTree as ET

from PyQt5 import QtWidgets, QtCore  # type: ignore
from PyQt5.QtWidgets import QMessageBox  # type: ignore
from PyQt5.QtCore import QSize  # type: ignore

from pineboolib.core.utils.utils_base import filedir, indent
from pineboolib.fllegacy.flsettings import FLSettings  # FIXME: Use pineboolib.core.settings

from typing import Optional


class DlgConnect(QtWidgets.QWidget):
    """
    Esta clase muestra gestiona el dialogo de Login
    """

    optionsShowed = True
    minSize = None
    maxSize = None
    profile_dir = None
    pNSqlDrivers = None
    edit_mode = None

    def __init__(self) -> None:
        """
        Constructor
        """
        super(DlgConnect, self).__init__()
        self.optionsShowed = True
        self.minSize = QSize(350, 140)
        self.maxSize = QSize(350, 495)
        self.profile_dir = FLSettings().readEntry("ebcomportamiento/profiles_folder", filedir("../profiles"))
        from pineboolib.application.database.pnsqldrivers import PNSqlDrivers

        self.pNSqlDrivers = PNSqlDrivers()
        self.edit_mode = False

    def load(self) -> None:
        """
        Carga el form dlgconnect
        """
        from pineboolib.fllegacy.flmanagermodules import FLManagerModules

        mM = FLManagerModules()
        dlg_ = filedir("loader/dlgconnect/dlgconnect.ui")

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
        self.ui.tbEditProfile.clicked.connect(self.editProfile)
        self.cleanProfileForm()
        self.ui.cbDBType.currentIndexChanged.connect(self.updatePort)
        self.ui.cbProfiles.currentIndexChanged.connect(self.enablePassword)
        self.ui.cbAutoLogin.stateChanged.connect(self.enableProfilePassword)
        self.ui.le_profiles.setText(self.profile_dir)
        self.ui.tb_profiles.clicked.connect(self.change_profile_dir)
        self.showOptions()
        self.loadProfiles()
        self.ui.leDescription.textChanged.connect(self.updateDBName)

    def cleanProfileForm(self) -> None:
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

    def loadProfiles(self) -> None:
        """
        Actualiza el ComboBox de los perfiles
        """
        self.ui.cbProfiles.clear()
        if not os.path.exists(self.profile_dir):
            # os.mkdir(filedir(self.profile_dir))
            return

        files = [f for f in sorted(os.listdir(self.profile_dir)) if os.path.isfile(os.path.join(self.profile_dir, f))]
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
    def showOptions(self) -> None:
        """
        Muestra el frame opciones
        """
        if self.optionsShowed:
            self.ui.frmOptions.hide()
            self.ui.tbDeleteProfile.hide()
            self.ui.tbEditProfile.hide()
            self.ui.setMinimumSize(self.minSize)
            self.ui.setMaximumSize(self.minSize)
            self.ui.resize(self.minSize)
        else:
            self.ui.frmOptions.show()
            self.ui.tbDeleteProfile.show()
            self.ui.tbEditProfile.show()
            self.ui.setMinimumSize(self.maxSize)
            self.ui.setMaximumSize(self.maxSize)
            self.ui.resize(self.maxSize)

        self.optionsShowed = not self.optionsShowed

    @QtCore.pyqtSlot()
    def open(self) -> None:
        """
        Abre la conexión seleccionada
        """
        fileName = os.path.join(self.profile_dir, "%s.xml" % self.ui.cbProfiles.currentText())
        tree = ET.parse(fileName)
        root = tree.getroot()

        version = root.get("Version")
        if version is None:
            version = 1.0
        else:
            version = float(version)

        last_profile = self.ui.cbProfiles.currentText()
        if last_profile not in (None, ""):
            settings = FLSettings()
            settings.writeEntry("DBA/last_profile", last_profile)

        for profile in root.findall("profile-data"):
            if getattr(profile.find("password"), "text", None):
                psP = profile.find("password").text
                invalid_password = False
                if version == 1.0:
                    psP = base64.b64decode(psP).decode()
                    if psP:
                        if self.ui.lePassword.text() != psP:
                            invalid_password = True

                else:
                    user_pass = self.ui.lePassword.text()
                    if not user_pass:
                        user_pass = ""
                    user_pass = hashlib.sha256(user_pass.encode()).hexdigest()
                    if psP != user_pass:
                        invalid_password = True

                if invalid_password:
                    QMessageBox.information(self.ui, "Pineboo", "Contraseña Incorrecta")
                    return

        self.database = root.find("database-name").text
        for db in root.findall("database-server"):
            self.hostname = db.find("host").text
            self.portnumber = db.find("port").text
            self.driveralias = db.find("type").text
            if self.driveralias not in self.pNSqlDrivers.aliasList():
                QMessageBox.information(self.ui, "Pineboo", "Esta versión de pineboo no soporta el driver '%s'" % self.driveralias)
                self.database = None
                return
        for credentials in root.findall("database-credentials"):
            self.username = credentials.find("username").text
            ps = credentials.find("password").text
            if ps:
                self.password = base64.b64decode(ps).decode()
            else:
                self.password = ""

        if self.pNSqlDrivers.isDesktopFile(self.driveralias):
            self.database = "%s.sqlite3" % self.database

        self.close()

    @QtCore.pyqtSlot()
    def saveProfile(self):
        """
        Guarda la conexión
        """
        profile = ET.Element("Profile")
        profile.set("Version", "1.1")
        description = self.ui.leDescription.text()

        if description == "":
            QMessageBox.information(self.ui, "Pineboo", "La descripción no se puede dejar en blanco")
            self.ui.leDescription.setFocus()
            return

        if not os.path.exists(self.profile_dir):
            os.mkdir(filedir(self.profile_dir))

        if os.path.exists(os.path.join(self.profile_dir, "%s.xml" % description)) and not self.edit_mode:
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

        passwDB = self.ui.leDBPassword.text()
        nameDB = self.ui.leDBName.text()

        auto_login = self.ui.cbAutoLogin.isChecked()
        pass_profile = ""
        if not auto_login:
            pass_profile = self.ui.leProfilePassword.text()

        pass_profile = hashlib.sha256(pass_profile.encode())
        profile_user = ET.SubElement(profile, "profile-data")
        profile_password = ET.SubElement(profile_user, "password")
        profile_password.text = pass_profile.hexdigest()

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

        indent(profile)

        tree = ET.ElementTree(profile)

        if self.edit_mode:
            if os.path.exists(os.path.join(self.profile_dir, "%s.xml" % description)):
                os.remove(os.path.join(self.profile_dir, "%s.xml" % description))
                self.edit_mode = False

        tree.write(os.path.join(self.profile_dir, "%s.xml" % description), xml_declaration=True, encoding="utf-8")
        # self.cleanProfileForm()
        self.loadProfiles()
        self.ui.cbProfiles.setCurrentText(description)

    @QtCore.pyqtSlot()
    def deleteProfile(self):
        """
        Borra la conexión seleccionada
        """
        if self.ui.cbProfiles.count() > 0:
            res = QMessageBox.warning(
                self.ui,
                "Pineboo",
                "¿Desea borrar el perfil %s?" % self.ui.cbProfiles.currentText(),
                QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No,
            )
            if res == QtWidgets.QMessageBox.No:
                return

            fileName = "%s.xml" % self.ui.cbProfiles.currentText()
            os.remove(os.path.join(self.profile_dir, fileName))
            self.loadProfiles()

    @QtCore.pyqtSlot()
    def editProfile(self):
        """
        Edita la conexión seleccionada
        """
        # Cogemos el perfil y lo abrimos
        file_name = os.path.join(self.profile_dir, "%s.xml" % self.ui.cbProfiles.currentText())
        tree = ET.parse(file_name)
        root = tree.getroot()

        version = root.get("Version")
        if version is None:
            version = 1.0
        else:
            version = float(version)

        self.ui.leProfilePassword.setText("")

        if version == 1.0:
            self.ui.cbAutoLogin.setChecked(True)
            for profile in root.findall("profile-data"):
                if getattr(profile.find("password"), "text", None):
                    psP = profile.find("password").text
                    psP = base64.b64decode(psP).decode()
                    if psP is not None:
                        self.ui.leProfilePassword.setText(psP)
                        self.ui.cbAutoLogin.setChecked(False)
        else:
            QMessageBox.information(
                self.ui, "Pineboo", "Tiene que volver a escribir las contraseñas\ndel perfil antes de guardar.", QtWidgets.QMessageBox.Ok
            )
            self.ui.cbAutoLogin.setChecked(False)

        self.ui.leDescription.setText(self.ui.cbProfiles.currentText())
        self.ui.leDBName.setText(root.find("database-name").text)
        root.find("database-name").text
        for db in root.findall("database-server"):
            self.ui.leURL.setText(db.find("host").text)
            self.ui.lePort.setText(db.find("port").text)
            self.ui.cbDBType.setCurrentText(db.find("type").text)
        for credentials in root.findall("database-credentials"):
            if credentials.find("username").text is not None:
                self.ui.leDBUser.setText(credentials.find("username").text)
            if credentials.find("password").text is not None and version == 1.0:
                self.ui.leDBPassword.setText(base64.b64decode(credentials.find("password").text).decode())
                self.ui.leDBPassword2.setText(base64.b64decode(credentials.find("password").text).decode())

        self.edit_mode = True

    @QtCore.pyqtSlot(int)
    def updatePort(self) -> None:
        """
        Actualiza al puerto por defecto del driver
        """
        self.ui.lePort.setText(self.pNSqlDrivers.port(self.ui.cbDBType.currentText()))

    @QtCore.pyqtSlot(int)
    def enablePassword(self, n: Optional[int] = None) -> None:
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
            QMessageBox.warning(
                self.ui, "Pineboo", "El perfil %s no parece válido" % self.ui.cbProfiles.currentText(), QtWidgets.QMessageBox.Ok
            )
            return

        version = root.get("Version")
        if version is None:
            version = 1.0
        else:
            version = float(version)

        for profile in root.findall("profile-data"):
            password = profile.find("password")

        if password is None or (version > 1.0 and password.text == hashlib.sha256("".encode()).hexdigest()):
            self.ui.lePassword.setEnabled(False)
        else:
            self.ui.lePassword.setEnabled(True)

    def updateDBName(self):
        """
        Actualiza el nombre de la BD con el nombre de la descripción
        """
        self.ui.leDBName.setText(self.ui.leDescription.text().replace(" ", "_"))

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

        new_dir = QtWidgets.QFileDialog.getExistingDirectory(
            self.ui, self.tr("Carpeta profiles"), self.profile_dir, QtWidgets.QFileDialog.ShowDirsOnly
        )

        if new_dir and new_dir is not self.profile_dir:
            FLSettings().writeEntry("ebcomportamiento/profiles_folder", new_dir)
            self.profile_dir = new_dir
            self.loadProfiles()
