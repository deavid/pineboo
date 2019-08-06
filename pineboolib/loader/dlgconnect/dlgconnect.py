# -*- coding: utf-8 -*-
"""dlgconnect module."""

import os

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QSize

from pineboolib.core.utils.utils_base import filedir
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
        self.ui.leProfilePassword2.setText("")
        self.ui.cbAutoLogin.setChecked(False)
        self.updatePort()

    def loadProfiles(self) -> None:
        """
        Update ComboBox of profiles.
        """
        if not os.path.exists(self.profile_dir):
            # os.mkdir(filedir(self.profile_dir))
            return
        self.ui.cbProfiles.clear()
        self.profiles.clear()

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
        if self.ui.leDescription.text() == "":
            QMessageBox.information(
                self.ui, "Pineboo", "La descripción no se puede dejar en blanco"
            )
            self.ui.leDescription.setFocus()
            return

        if self.ui.leDBPassword.text() != self.ui.leDBPassword2.text():
            QMessageBox.information(self.ui, "Pineboo", "La contraseña de la BD no coincide")
            self.ui.leDBPassword.setText("")
            self.ui.leDBPassword2.setText("")
            return

        if self.ui.leProfilePassword.text() != self.ui.leProfilePassword2.text():
            QMessageBox.information(self.ui, "Pineboo", "La contraseña del perfil no coincide")
            self.ui.leProfilePassword.setText("")
            self.ui.leProfilePassword2.setText("")
            return

        if self.edit_mode:
            pconf = self.getProjectConfig(self.ui.cbProfiles.currentText())
            if pconf is None:
                return
            pconf.description = self.ui.leDescription.text()
        else:
            pconf = ProjectConfig(
                description=self.ui.leDescription.text(), database="unset", type="unset"
            )

        if not os.path.exists(self.profile_dir):
            os.mkdir(filedir(self.profile_dir))

        if os.path.exists(pconf.filename) and not self.edit_mode:
            QMessageBox.information(self.ui, "Pineboo", "El perfil ya existe")
            return

        pconf.type = self.ui.cbDBType.currentText()
        pconf.host = self.ui.leURL.text()
        pconf.port = int(self.ui.lePort.text())
        pconf.username = self.ui.leDBUser.text()

        pconf.password = self.ui.leDBPassword.text()
        pconf.database = self.ui.leDBName.text()

        pass_profile_text = ""
        if not self.ui.cbAutoLogin.isChecked():
            pass_profile_text = self.ui.leProfilePassword.text()
        pconf.project_password = pass_profile_text
        pconf.save_projectxml(overwrite_existing=self.edit_mode)

        # self.cleanProfileForm()
        self.loadProfiles()
        self.ui.cbProfiles.setCurrentText(pconf.description)

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

            pconf: ProjectConfig = self.profiles[self.ui.cbProfiles.currentText()]
            os.remove(pconf.filename)
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
        self.ui.leProfilePassword2.setText(pconf.project_password)

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
        pconf: ProjectConfig = self.profiles[self.ui.cbProfiles.currentText()]
        # NOTE: This disables the password entry once the password has been processed for
        # .. the profile once. So the user does not need to retype it.
        self.ui.lePassword.setEnabled(pconf.password_required)
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
            self.ui.leProfilePassword2.setEnabled(False)
        else:
            self.ui.leProfilePassword.setEnabled(True)
            self.ui.leProfilePassword2.setEnabled(True)

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
