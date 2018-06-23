# -*- coding: utf-8 -*-
from builtins import str
import sqlite3
import os
import sys
import traceback
import logging

from pineboolib.pnsqldrivers import PNSqlDrivers
from pineboolib.fllegacy.FLSettings import FLSettings
from pineboolib.utils import filedir

from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtWidgets import QTableWidgetItem, QFrame
from PyQt5.QtCore import QFileInfo, QSize
from PyQt5.Qt import QWidget

"""
Esta clase muestra gestiona el dialogo de Login
"""


class DlgConnect(QtWidgets.QWidget):
    _DGI = None
    optionsShowed = True

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

    """
    Abre la DB que contiene las difererentes conexiones
    """

    def openDB(self):
        if self.dbProjects_:
            self.dbProjects_.close()
        self.dbProjects_ = sqlite3.connect(self.DBConnectors)

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
        self.ui.pbSaveConnection.clicked.connect(self.saveConnection)
        self.showOptions()

        # self.loadProjects()
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
            self.ui.setMinimumSize(self.minSize)
            self.ui.setMaximumSize(self.minSize)
            self.ui.resize(self.minSize)
        else:
            self.ui.frmOptions.show()
            self.ui.setMinimumSize(self.maxSize)
            self.ui.setMaximumSize(self.maxSize)
            self.ui.resize(self.maxSize)

        self.optionsShowed = not self.optionsShowed

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
    def saveConnection(self):
        print("Guardando Conexión")
