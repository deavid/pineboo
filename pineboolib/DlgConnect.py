# -*- coding: utf-8 -*-


from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from pineboolib.utils import filedir
from pineboolib.PNSqlDrivers import PNSqlDrivers
from pineboolib.fllegacy.FLSettings import FLSettings

from builtins import str
import sqlite3
import os
import sys


class DlgConnect(QtWidgets.QWidget):
    ruta = ""
    username = ""
    password = ""
    hostname = ""
    portnumber = ""
    database = ""
    ui = None
    dbProjects_ = None

    def __init__(self):
        super(DlgConnect, self).__init__()
        self.ruta = ""
        self.username = ""
        self.password = ""
        self.hostname = ""
        self.portnumber = ""
        self.database = ""
        self.dbProjects_ = None
        self.deleteCache = False
        self.parseProject = False

    def openDB(self):
        if self.dbProjects_:
            self.dbProjects_.close()

        self.dbProjects_ = sqlite3.connect(
            filedir(self.ui.leFolderSQLITE.text()) + '/pinebooconectores.sqlite')

    def load(self):
        self.ui = uic.loadUi(filedir('../share/forms/dlg_connect.ui'), self)

        frameGm = self.frameGeometry()
        screen = QtWidgets.QApplication.desktop().screenNumber(
            QtWidgets.QApplication.desktop().cursor().pos())
        centerPoint = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

        self.ui.pbnStart.clicked.connect(self.on_click)
        self.ui.pbnSearchFolder.clicked.connect(self.findPathProject)

        # MODIFICACION 4 PARA CONECTOR SQLITE : DEFINIMOS LO QUE HACEN LOS BOTONES nuevos
        self.ui.pbnCargarDatos.clicked.connect(self.ChargeProject)
        self.tableWidget.doubleClicked.connect(self.on_click)
        # self.ui.pbnMostrarProyectos.clicked.connect(self.ShowTable)
        self.ui.pbnBorrarProyecto.clicked.connect(self.DeleteProject)
        self.ui.pbnGuardarProyecto.clicked.connect(self.SaveProject)
        self.ui.pbnProyectoEjemplo.clicked.connect(self.SaveProjectExample)
        self.ui.pbnEnebooImportButton.clicked.connect(self.SaveEnebooImport)
        # hasta aqui la modificación 4

        self.ui.leFolderSQLITE.setText(filedir("../projects"))

        self.leName = self.ui.leName
        self.leDBName = self.ui.leDBName
        self.leUserName = self.ui.leUserName
        self.lePassword = self.ui.lePassword
        self.lePort = self.ui.lePort
        # MODIFICACION 6 PARA CONECTOR SQLITE : DEFINIMOS los NUEVOS CAMPOS DEL UI:
        self.leFolder = self.ui.leFolderSQLITE
        #self.leDBType = self.ui.leDBType
        self.leHostName = self.ui.leHostName

        # hasta aqui la modificación 6
        self.cBDrivers = self.ui.cBDrivers

        DV = PNSqlDrivers()
        list = DV.aliasList()
        self.cBDrivers.addItems(list)

        i = 0
        while i < self.cBDrivers.count():
            if DV.aliasToName(self.cBDrivers.itemText(i)) == DV.defaultDriverName:
                self.cBDrivers.setCurrentIndex(i)
                break

            i = i + 1
        self.loadPreferences()
        self.openDB()
        self.ShowTable()

    @QtCore.pyqtSlot()
    def conectar(self):
        folder_ = None

        if self.leFolder.text():
            folder_ = self.leFolder.text()
        else:
            folder_ = filedir("../projects")

        self.ruta = filedir(str(folder_), str(self.leName.text()))
        self.username = self.leUserName.text()
        self.password = self.lePassword.text()
        self.hostname = self.leHostName.text()
        self.portnumber = self.lePort.text()
        self.database = self.leDBName.text()
        self.driveralias = self.cBDrivers.currentText()
        self.deleteCache = self.ui.cBDeleteCache.isChecked()
        self.parseProject = self.ui.cBParseProject.isChecked()

        """
        if not self.leName.text():
            self.ruta = ""
        elif not self.ruta.endswith(".xml"):
            self.ruta += ".xml"
        if not os.path.isfile(self.ruta) and self.leName.text():
            QtWidgets.QMessageBox.information(self, "AVISO", "El proyecto \n" + self.ruta +" no existe")
            self.ruta = None
        else:
            self.close()
        """
        self.dbProjects_.close()
        self.close()

    @QtCore.pyqtSlot()
    def findPathProject(self):
        filename = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Seleccione Directorio")
        if filename:
            self.leFolder.setText(str(filename))
            self.ShowTable()

        self.openDB()
        # cambiamos el directorio de trabajo donde guardar la base de datos Sqlite:
        os.chdir(filename)

# MODIFICACION 8 PARA CONECTOR SQLITE :añado uso botón CARGAR PROYECTO
    @QtCore.pyqtSlot()
    def ChargeProject(self):
        if not self.tableWidget.item(self.tableWidget.currentRow(), 0):
            return False

        par = self.tableWidget.item(self.tableWidget.currentRow(), 0).text()

        cursor = self.dbProjects_.cursor()
        # ELEGIR UNA FILA DE LA TABLA proyectos DE LA BASE DE DATOS:
        cursor.execute("SELECT * FROM proyectos WHERE name = '%s'" % par)

        registro = cursor.fetchone()
        # escribir los campos de la fila ELEGIDA en la zona de "CARGAR DATOS":
        self.leName.setText(str(registro[1]))
        self.leDBName.setText(str(registro[2]))
        id = self.cBDrivers.findText(str(registro[3]))
        self.cBDrivers.setCurrentIndex(id)
        self.leHostName.setText(str(registro[4]))
        self.lePort.setText(str(registro[5]))
        self.leUserName.setText(str(registro[6]))
        self.lePassword.setText(str(registro[7]))

        return True

        # hasta aqui la modificación 8

# MODIFICACION 9 PARA CONECTOR SQLITE :añado uso botón MOSTRAR TABLA DE REGISTROS-PROYECTOS
    @QtCore.pyqtSlot()
    def ShowTable(self):
        self.tableWidget.clear()
        cursor = self.dbProjects_.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS proyectos(id INTEGER PRIMARY KEY, name TEXT UNIQUE, dbname TEXT, dbtype TEXT, dbhost TEXT, dbport TEXT, username TEXT, password TEXT)')
        cursor.execute(
            'SELECT id, name, dbname, dbtype, dbhost, dbport, username, password FROM proyectos')
        conectores = cursor.fetchall()
        self.tableWidget.setHorizontalHeaderLabels(
            ['Name', 'DBname', 'DBType', 'DBHost', 'DBPort', 'Username', 'Password'])
        # cuento el número de filas TOTAL. Necessary even when there are no rows in the table
        currentRowCount = self.tableWidget.rowCount()
        self.tableWidget.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setAlternatingRowColors(True)
        # escribir el campo 0 de la fila 1:
        i = 0
        self.tableWidget.setRowCount(len(conectores))
        for conector in conectores:
            # add more if there is more columns in the database.
            self.tableWidget.setItem(i, 0, QTableWidgetItem(conector[1]))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(conector[2]))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(conector[3]))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(conector[4]))
            self.tableWidget.setItem(i, 4, QTableWidgetItem(conector[5]))
            self.tableWidget.setItem(i, 5, QTableWidgetItem(conector[6]))
            self.tableWidget.setItem(i, 6, QTableWidgetItem(conector[7]))
            i = i + 1

    @QtCore.pyqtSlot()
    def on_click(self):
        if self.ChargeProject():
            self.conectar()

    @QtCore.pyqtSlot()
    def DeleteProject(self):
        cursor = self.dbProjects_.cursor()
        try:
            par = self.tableWidget.item(
                self.tableWidget.currentRow(), 0).text()
            if par:
                cursor.execute("DELETE FROM proyectos WHERE name= '%s'" % par)
                self.dbProjects_.commit()
        except:
            pass

        self.ShowTable()

    @QtCore.pyqtSlot()
    def SaveProject(self):

        name2 = str(self.ui.leName.text())
        dbname2 = str(self.ui.leDBName.text())
        dbtype2 = self.ui.cBDrivers.currentText()
        dbhost2 = str(self.ui.leHostName.text())
        dbport2 = str(self.ui.lePort.text())
        username2 = str(self.ui.leUserName.text())
        password2 = str(self.ui.lePassword.text())

        cursor = self.dbProjects_.cursor()
        with self.dbProjects_:
            sql = "INSERT INTO proyectos(name, dbname, dbtype, dbhost, dbport, username, password) VALUES ('%s','%s','%s','%s','%s','%s','%s')" % (
                name2, dbname2, dbtype2, dbhost2, dbport2, username2, password2)
            cursor.execute(sql)

        self.ShowTable()

    @QtCore.pyqtSlot()
    def SaveProjectExample(self):
        #db = sqlite3.connect('pinebooconectores.sqlite')
        # Get a cursor object para CREAR la tabla "proyectos"
        cursor = self.dbProjects_.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS proyectos(id INTEGER PRIMARY KEY, name TEXT, dbname TEXT, dbtype TEXT, dbhost TEXT, dbport TEXT, username TEXT, password TEXT)
''')
        self.dbProjects_.commit()
        # Get a cursor object  para AÑADIR CAMPOS DE EJEMPLO:
        cursor = self.dbProjects_.cursor()
        name1 = 'Empresa de Ejemplo'
        dbname1 = 'eneboobase'
        dbtype1 = 'PostgreSQL'
        dbhost1 = 'localhost'
        dbport1 = '5432'
        username1 = 'postgres'
        password1 = 'postgres'
        cursor = self.dbProjects_.cursor()
        with self.dbProjects_:
            sql = "INSERT INTO proyectos(name, dbname, dbtype, dbhost, dbport, username, password) VALUES ('%s','%s','%s','%s','%s','%s','%s')" % (
                name1, dbname1, dbtype1, dbhost1, dbport1, username1, password1)
            cursor.execute(sql)

        self.ShowTable()

        # escribir los campos de la fila ELEGIDA en la zona de "CARGAR DATOS":
        self.leName.setText(str(name1))
        self.leDBName.setText(str(dbname1))
        # self.leDBType.setText(str(dbtype1))
        self.leHostName.setText(str(dbhost1))
        self.lePort.setText(str(dbport1))
        self.leUserName.setText(str(username1))
        self.lePassword.setText(str(password1))
        # When we are done working with the DB we need to close the connection:
        # db.close()
        print("PROYECTO DE EJEMPLO GRABADO y CARGADO")

    @QtCore.pyqtSlot()
    def SaveEnebooImport(self):
        """  
        Este codigo es para reutilizar la configuracion del mismo equipo con Eneboo
        Para conseguir la contraseña del fichero en texto plano:
        password + username+ port+ hostname + db + lastDB
        print config.get('DBA', 'passwordusuario5432localhostPostgresSQLapertus')


        from os.path import expanduser
        HOME = expanduser("~")
        import configparser
        config = configparser.ConfigParser()
        config.read( HOME + '/.qt/eneboorc')

        A = config['DBA']['db']
        B = config['DBA']['hostname']
        C = config['DBA']['lastDB']
        D = config['DBA']['username']
        E = config['DBA']['port']
        F = config['DBA']['rememberPasswd']

        print (A)


        # Get a cursor object para CREAR la tabla "proyectos"
        cursor = self.dbProjects_.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS proyectos(id INTEGER PRIMARY KEY, name TEXT, dbname TEXT, dbtype TEXT, dbhost TEXT, dbport TEXT, username TEXT, password TEXT)
''')
        self.dbProjects_.commit()

        # ABRO BUCLE PARA GRABAR VARIAS EMPRESAS DE ENEBOO
        currentRowCount = self.tableWidget.rowCount() #cuento el número de filas TOTAL ACTUAL (ANTES DE TRAER LAS DE ENEBOO).
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setAlternatingRowColors(True)
        # escribir A PARTIR DE LA FILA EXISTENTE:
        i = currentRowCount + 1
        self.tableWidget.setRowCount(len(conectores))
        for conector in conectores:
            # add more if there is more columns in the database.        
            # Get a cursor object  para AÑADIR CAMPOS:

            # PASO-1: COPIAR LOS DATOS DE ENEBOO
            cursor = self.dbProjects_.cursor()
            nameE = FLUtil.readSettingEntry('Empresa de Ejemplo')
            dbnameE = FLUtil.readSettingEntry()
            dbtypeE = FLUtil.readSettingEntry('PostgreSQL')
            dbhostE = FLUtil.readSettingEntry('localhost')
            dbportE = FLUtil.readSettingEntry('5432')
            usernameE = FLUtil.readSettingEntry('postgres')
            passwordE = FLUtil.readSettingEntry('postgres')

            # PASO-2: GRABAR LOS DATOS EN LA BASE DE DATOS PINEBOOCONECTORES
            cursor = self.dbProjects_.cursor()
            with self.dbProjects_:
                sql = "INSERT INTO proyectos(name, dbname, dbtype, dbhost, dbport, username, password) VALUES ('%s','%s','%s','%s','%s','%s','%s')" % (nameE, dbnameE, dbtypeE, dbhostE, dbportE, usernameE, passwordE)
                cursor.execute(sql)
            self.ShowTable()

            # PASO-3: ESCRIBIR LOS DATOS DE ESA EMPRESA EN la zona de "CARGAR DATOS":
            self.leName.setText(str(nameE))
            self.leDBName.setText(str(dbnameE))
            #self.leDBType.setText(str(dbtypeE))
            self.leHostName.setText(str(dbhostE))
            self.lePort.setText(str(dbportE))
            self.leUserName.setText(str(usernameE))
            self.lePassword.setText(str(passwordE))
            self.tableWidget.setItem(i, 0, QTableWidgetItem(conector[1]))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(conector[2]))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(conector[3]))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(conector[4]))
            self.tableWidget.setItem(i, 4, QTableWidgetItem(conector[5]))
            self.tableWidget.setItem(i, 5, QTableWidgetItem(conector[6]))
            self.tableWidget.setItem(i, 6, QTableWidgetItem(conector[7]))

            i = i + 1

"""
        print("Conexiones de Eneboo IMPORTADAS")

    def loadPreferences(self):
        dCache = FLSettings().readBoolEntry("DEVELOP/deleteCache", False)
        parseProject = FLSettings().readBoolEntry("DEVELOP/parseProject", False)
        self.ui.cBDeleteCache.setChecked(dCache)
        self.ui.cBParseProject.setChecked(parseProject)

    def savePreferences(self):
        FLSettings().writeEntry("DEVELOP/deleteCache", self.ui.cBDeleteCache.isChecked())
        FLSettings().writeEntry("DEVELOP/parseProject", self.ui.cBParseProject.isChecked())

    def close(self):
        self.savePreferences()
        return super(DlgConnect, self).close()
