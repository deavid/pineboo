# -*- coding: utf-8 -*-
"""dlgconnect module."""

import os
import base64
import hashlib
from xml.etree import ElementTree as ET

from PyQt5 import QtWidgets  # type: ignore
from PyQt5.QtWidgets import QMessageBox  # type: ignore
from PyQt5.QtCore import QSize  # type: ignore

from pineboolib.core.utils.utils_base import filedir, pretty_print_xml
from pineboolib.core.settings import config, settings
from pineboolib.core.utils import logging
from pineboolib.core.decorators import pyqtSlot
from pineboolib.loader.projectconfig import ProjectConfig, PasswordMismatchError
from typing import Optional, cast, Dict

logger = logging.getLogger(__name__)


class DlgConnect(QtWidgets.QWidget):
    """
    DlgConnect Class.

    This class shows manages the Login dialog.
    """

    optionsShowed: bool
    minSize: QSize
    maxSize: QSize
    edit_mode: bool

    profiles: Dict[str, ProjectConfig]  #: Index of loaded profiles. Keyed by description.
    selected_project_config: Optional[ProjectConfig]  #: Contains the selected item to load.

    def __init__(self) -> None:
        """
        Initialize.
        """
        from pineboolib.application.database.pnsqldrivers import PNSqlDrivers

        super(DlgConnect, self).__init__()
        self.optionsShowed = False
        self.minSize = QSize(350, 140)
        self.maxSize = QSize(350, 495)
        self.profile_dir: str = ProjectConfig.profile_dir
        self.sql_drivers = PNSqlDrivers()
        self.edit_mode = False
        self.profiles = {}
        self.selected_project_config = None

    def load(self) -> None:
        """
        Load the dlgconnect form.
        """
        from pineboolib.fllegacy.flmanagermodules import FLManagerModules

        dlg_ = filedir("loader/dlgconnect/dlgconnect.ui")

        self.ui = FLManagerModules.createUI(dlg_, None, self)
        if not self.ui:
            raise Exception("Error creating dlgConnect")
        # Centrado en pantalla
        frameGm = self.frameGeometry()
        screen = QtWidgets.QApplication.desktop().screenNumber(
            QtWidgets.QApplication.desktop().cursor().pos()
        )
        centerPoint = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

        self.ui.pbLogin.clicked.connect(self.open)
        self.ui.tbOptions.clicked.connect(self.toggleOptions)
        self.ui.pbSaveConnection.clicked.connect(self.saveProfile)
        self.ui.tbDeleteProfile.clicked.connect(self.deleteProfile)
        self.ui.tbEditProfile.clicked.connect(self.editProfile)
        self.cleanProfileForm()
        self.ui.cbDBType.currentIndexChanged.connect(self.updatePort)
        self.ui.cbProfiles.currentIndexChanged.connect(self.enablePassword)
        self.ui.cbAutoLogin.stateChanged.connect(self.cbAutoLogin_checked)
        self.ui.le_profiles.setText(self.profile_dir)
        self.ui.tb_profiles.clicked.connect(self.change_profile_dir)
        self.showOptions(False)
        self.loadProfiles()
        self.ui.leDescription.textChanged.connect(self.updateDBName)

    def cleanProfileForm(self) -> None:
        """
        Clean the profiles creation tab, and fill in the basic data of the default SQL driver.
        """
        self.ui.leDescription.setText("")
        driver_list = self.sql_drivers.aliasList()
        self.ui.cbDBType.clear()
        self.ui.cbDBType.addItems(driver_list)
        self.ui.cbDBType.setCurrentText(self.sql_drivers.defaultDriverName())
        self.ui.leURL.setText("localhost")
        self.ui.leDBUser.setText("")
        self.ui.leDBPassword.setText("")
        self.ui.leDBName.setText("")
        self.ui.leProfilePassword.setText("")
        self.ui.cbAutoLogin.setChecked(False)
        self.updatePort()

    def loadProfiles(self) -> None:
        """
        Update ComboBox of profiles.
        """
        self.ui.cbProfiles.clear()
        if not os.path.exists(self.profile_dir):
            # os.mkdir(filedir(self.profile_dir))
            return

        with os.scandir(self.profile_dir) as it:
            for entry in it:
                if entry.name.startswith("."):
                    continue
                if not entry.name.endswith(".xml"):
                    continue
                if not entry.is_file():
                    continue

                pconf = ProjectConfig(
                    filename=os.path.join(self.profile_dir, entry.name),
                    database="unset",
                    type="unset",
                )
                try:
                    pconf.load_projectxml()
                except PasswordMismatchError:
                    logger.trace(
                        "Profile %r [%r] requires a password", pconf.description, entry.name
                    )
                except Exception:
                    logger.exception("Unexpected error trying to read profile %r", entry.name)
                    continue
                self.profiles[pconf.description] = pconf

        for name in sorted(self.profiles.keys()):
            self.ui.cbProfiles.addItem(name)

        last_profile = settings.value("DBA/last_profile", None)
        if last_profile:
            self.ui.cbProfiles.setCurrentText(last_profile)

    @pyqtSlot()
    def toggleOptions(self) -> None:
        """Show/Hide Options."""
        self.showOptions(not self.optionsShowed)

    def showOptions(self, showOptions: bool) -> None:
        """
        Show the frame options.
        """
        if showOptions:
            self.ui.frmOptions.show()
            self.ui.tbDeleteProfile.show()
            self.ui.tbEditProfile.show()
            self.ui.setMinimumSize(self.maxSize)
            self.ui.setMaximumSize(self.maxSize)
            self.ui.resize(self.maxSize)
        else:
            self.ui.frmOptions.hide()
            self.ui.tbDeleteProfile.hide()
            self.ui.tbEditProfile.hide()
            self.ui.setMinimumSize(self.minSize)
            self.ui.setMaximumSize(self.minSize)
            self.ui.resize(self.minSize)

        self.optionsShowed = showOptions

    @pyqtSlot()
    def open(self) -> None:
        """
        Open the selected connection.
        """
        pconf = self.getProjectConfig(self.ui.cbProfiles.currentText())
        if pconf is None:
            return
        self.selected_project_config = pconf
        self.close()

    @pyqtSlot()
    def saveProfile(self) -> None:
        """
        Save the connection.
        """
        profile = ET.Element("Profile")
        profile.set("Version", "1.1")
        description = self.ui.leDescription.text()

        if description == "":
            QMessageBox.information(
                self.ui, "Pineboo", "La descripción no se puede dejar en blanco"
            )
            self.ui.leDescription.setFocus()
            return

        if not os.path.exists(self.profile_dir):
            os.mkdir(filedir(self.profile_dir))

        if (
            os.path.exists(os.path.join(self.profile_dir, "%s.xml" % description))
            and not self.edit_mode
        ):
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
        pass_profile_text = ""
        if not auto_login:
            pass_profile_text = self.ui.leProfilePassword.text()

        pass_profile = hashlib.sha256(pass_profile_text.encode())
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

        pretty_print_xml(profile)

        tree = ET.ElementTree(profile)

        if self.edit_mode:
            if os.path.exists(os.path.join(self.profile_dir, "%s.xml" % description)):
                os.remove(os.path.join(self.profile_dir, "%s.xml" % description))
                self.edit_mode = False

        tree.write(
            os.path.join(self.profile_dir, "%s.xml" % description),
            xml_declaration=True,
            encoding="utf-8",
        )
        # self.cleanProfileForm()
        self.loadProfiles()
        self.ui.cbProfiles.setCurrentText(description)

    @pyqtSlot()
    def deleteProfile(self) -> None:
        """
        Delete the selected connection.
        """
        if self.ui.cbProfiles.count() > 0:
            res = QMessageBox.warning(
                self.ui,
                "Pineboo",
                "¿Desea borrar el perfil %s?" % self.ui.cbProfiles.currentText(),
                cast(QtWidgets.QMessageBox, QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.No),
                QtWidgets.QMessageBox.No,
            )
            if res == QtWidgets.QMessageBox.No:
                return

            fileName = "%s.xml" % self.ui.cbProfiles.currentText()
            os.remove(os.path.join(self.profile_dir, fileName))
            self.loadProfiles()

    def getProjectConfig(self, name: str) -> Optional[ProjectConfig]:
        """
        Get a profile by name and ensure its fully loaded.
        """
        pconf: ProjectConfig = self.profiles[name]

        if pconf.password_required:
            # As it failed to load earlier, it needs a password.
            # Copy the current password and test again...
            pconf.project_password = self.ui.lePassword.text()
            try:
                pconf.load_projectxml()
            except PasswordMismatchError:
                QMessageBox.information(self.ui, "Pineboo", "Contraseña Incorrecta")
                return None
        return pconf

    @pyqtSlot()
    def editProfile(self) -> None:
        """
        Edit the selected connection.
        """
        # Cogemos el perfil y lo abrimos
        self.editProfileName(self.ui.cbProfiles.currentText())

    def editProfileName(self, name: str) -> None:
        """
        Edit profile from name. Must have been loaded earlier on loadProfiles.
        """
        pconf = self.getProjectConfig(name)
        if pconf is None:
            return

        self.ui.leProfilePassword.setText(pconf.project_password)

        self.ui.cbAutoLogin.setChecked(pconf.project_password == "")

        self.ui.leDescription.setText(pconf.description)
        self.ui.leDBName.setText(pconf.database)

        self.ui.leURL.setText(pconf.host)
        self.ui.lePort.setText(str(pconf.port))
        self.ui.cbDBType.setCurrentText(pconf.type)

        self.ui.leDBUser.setText(pconf.username)

        self.ui.leDBPassword.setText(pconf.password)
        self.ui.leDBPassword2.setText(pconf.password)

        self.edit_mode = True

    @pyqtSlot(int)
    def updatePort(self) -> None:
        """
        Update to the driver default port.
        """
        self.ui.lePort.setText(self.sql_drivers.port(self.ui.cbDBType.currentText()))

    @pyqtSlot(int)
    def enablePassword(self, n: Optional[int] = None) -> None:
        """
        Check if the profile requires password to login or not.
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
                self.ui,
                "Pineboo",
                "El perfil %s no parece válido" % self.ui.cbProfiles.currentText(),
                QtWidgets.QMessageBox.Ok,
            )
            return

        _version = root.get("Version")
        if _version is None:
            version = 1.0
        else:
            version = float(_version)

        for profile in root.findall("profile-data"):
            password = profile.find("password")

        enable_passwd_control = False
        if (
            password is not None
            and version > 1.0
            and password.text != ""
            and password.text != hashlib.sha256("".encode()).hexdigest()
        ):
            enable_passwd_control = True

        self.ui.lePassword.setEnabled(enable_passwd_control)
        self.ui.lePassword.setText("")

    def updateDBName(self) -> None:
        """
        Update the name of the database with the description name.
        """
        self.ui.leDBName.setText(self.ui.leDescription.text().replace(" ", "_"))

    @pyqtSlot(int)
    def cbAutoLogin_checked(self) -> None:
        """
        Process checked event from AutoLogin checkbox.
        """

        if self.ui.cbAutoLogin.isChecked():
            self.ui.leProfilePassword.setEnabled(False)
        else:
            self.ui.leProfilePassword.setEnabled(True)

    def change_profile_dir(self) -> None:
        """
        Change the path where profiles are saved.
        """

        new_dir = QtWidgets.QFileDialog.getExistingDirectory(
            self.ui,
            self.tr("Carpeta profiles"),
            self.profile_dir,
            QtWidgets.QFileDialog.ShowDirsOnly,
        )

        if new_dir and new_dir is not self.profile_dir:
            config.set_value("ebcomportamiento/profiles_folder", new_dir)
            self.profile_dir = new_dir
            ProjectConfig.profile_dir = new_dir
            self.loadProfiles()
