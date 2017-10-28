# -*- coding: utf-8 -*-

from builtins import str
import os
from PyQt5 import QtWidgets, QtCore, uic

from pineboolib.utils import filedir
from pineboolib.PNSqlDrivers import PNSqlDrivers

# MODIFICACION 1 PARA CONECTOR SQLITE : Using Python's SQLite Module: self-contained, serverless, zero-configuration and transactional. It is very fast and lightweight, and the entire database is stored in a single disk file.
import sqlite3

# MODIFICACION 2 PARA CONECTOR SQLITE :añado librerías de conexión con qt5: SÓLO RENOMBRO LOS DE QT4
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys

# MODIFICACION 3 PARA CONECTOR SQLITE :añado debugging modulo PARA VER LOS PASOS: sirve cuando activas esto:
        # DEBUGGING:
        # pdb.set_trace()
        # print ("escribe `n´(next) para continuar / `q´(quit) para salir / `c´ para seguir sin debugg")
import pdb

class DlgConnect(QtWidgets.QWidget):
    ruta = ""
    username = ""
    password = ""
    hostname = ""
    portnumber = ""
    database = ""
    ui = None
    dbProjects_ = None
        

    def load(self):
        self.ui = uic.loadUi(filedir('forms/dlg_connect.ui'), self)
        
        frameGm = self.frameGeometry()
        screen = QtWidgets.QApplication.desktop().screenNumber(QtWidgets.QApplication.desktop().cursor().pos())
        centerPoint = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
        
        self.ui.pbnStart.clicked.connect(self.conectar)
        self.ui.pbnSearchFolder.clicked.connect(self.findPathProject)

        # MODIFICACION 4 PARA CONECTOR SQLITE : DEFINIMOS LO QUE HACEN LOS BOTONES nuevos 
        self.ui.pbnCargarDatos.clicked.connect(self.ChargeProject)
        #self.ui.pbnMostrarProyectos.clicked.connect(self.ShowTable)
        self.ui.pbnBorrarProyecto.clicked.connect(self.DeleteProject)
        self.ui.pbnGuardarProyecto.clicked.connect(self.SaveProject)
        #self.ui.pbnProyecto_Ejemplo.clicked.connect(self.SaveProjectEjemplo)
        # hasta aqui la modificación 4
        
        self.ui.leFolderSQLITE.setText(filedir("../projects"))
        
        self.ShowTable()

        DlgConnect.leName = self.ui.leName
        DlgConnect.leDBName = self.ui.leDBName
        DlgConnect.leUserName = self.ui.leUserName
        DlgConnect.lePassword = self.ui.lePassword
        DlgConnect.lePort = self.ui.lePort
        # MODIFICACION 6 PARA CONECTOR SQLITE : DEFINIMOS los NUEVOS CAMPOS DEL UI:
        DlgConnect.leFolder = self.ui.leFolderSQLITE
        #DlgConnect.leDBType = self.ui.leDBType
        DlgConnect.leHostName = self.ui.leHostName
        DlgConnect.leFila = self.ui.leFila
        # hasta aqui la modificación 6
        DlgConnect.cBDrivers = self.ui.cBDrivers
        
        DV = PNSqlDrivers()
        list = DV.aliasList()
        DlgConnect.cBDrivers.addItems(list)
        
        i = 0
        while i < DlgConnect.cBDrivers.count():
            if DV.aliasToName(DlgConnect.cBDrivers.itemText(i)) == DV.defaultDriverName:
                DlgConnect.cBDrivers.setCurrentIndex(i)
                break
            
            i = i + 1
    
    @QtCore.pyqtSlot()
    def conectar(self):
        folder_ =None
        
        if DlgConnect.leFolder.text():
            folder_ = DlgConnect.leFolder.text()
        else:
            folder_ = filedir("../projects")
            
        DlgConnect.ruta = filedir(str(folder_), str(DlgConnect.leName.text()))
        DlgConnect.username = DlgConnect.leUserName.text()
        DlgConnect.password = DlgConnect.lePassword.text()
        DlgConnect.hostname = DlgConnect.leHostName.text()
        DlgConnect.portnumber = DlgConnect.lePort.text()
        DlgConnect.database = DlgConnect.leDBName.text()
        DlgConnect.driveralias = DlgConnect.cBDrivers.currentText()

        """
        if not DlgConnect.leName.text():
            DlgConnect.ruta = ""
        elif not DlgConnect.ruta.endswith(".xml"):
            DlgConnect.ruta += ".xml"
        if not os.path.isfile(DlgConnect.ruta) and DlgConnect.leName.text():
            QtWidgets.QMessageBox.information(self, "AVISO", "El proyecto \n" + DlgConnect.ruta +" no existe")
            DlgConnect.ruta = None
        else:
            self.close()
        """
        self.dbProjects_.close()
        self.close()
        
    @QtCore.pyqtSlot()       
    def findPathProject(self):
        filename = QtWidgets.QFileDialog.getExistingDirectory(self, "Seleccione Directorio")
        if filename:
            DlgConnect.leFolder.setText(str(filename))
            self.ShowTable()

        # cambiamos el directorio de trabajo donde guardar la base de datos Sqlite:
        os.chdir(filename)

# MODIFICACION 8 PARA CONECTOR SQLITE :añado uso botón CARGAR PROYECTO
    @QtCore.pyqtSlot()
    def ChargeProject(self):

        self.dbProjects_ = sqlite3.connect(filedir(self.ui.leFolderSQLITE.text()) + '/pinebooconectores.sqlite') 
        # cambiamos el directorio de trabajo donde guardar la base de datos Sqlite:
        #filename = DlgConnect.leFolder
        #if filename:
        #    os.chdir(filename)

        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            DlgConnect.leFila.setText(str(currentQTableWidgetItem.row() + 1))
            fila = str(self.ui.leFila.text())
        par = (fila,)
        #fila = str(self.ui.leFila.text())
        
        #ABRIMOS LA BASE DE DATOS:
        
        cursor = self.dbProjects_.cursor()
        # ELEGIR UNA FILA DE LA TABLA proyectos DE LA BASE DE DATOS:
        
        cursor.execute("SELECT * FROM proyectos WHERE id=?", par)
        for registro in cursor:
            valor1 = registro[1]
            valor2 = registro[2]
            valor3 = registro[3]
            valor4 = registro[4]
            valor5 = registro[5]
            valor6 = registro[6]
            valor7 = registro[7]
        # escribir los campos de la fila ELEGIDA en la zona de "CARGAR DATOS":
        DlgConnect.leName.setText(str(valor1))
        DlgConnect.leDBName.setText(str(valor2))
        id = DlgConnect.cBDrivers.findText(str(valor3))
        DlgConnect.cBDrivers.setCurrentIndex(id)
        DlgConnect.leHostName.setText(str(valor4))
        DlgConnect.lePort.setText(str(valor5))
        DlgConnect.leUserName.setText(str(valor6))
        DlgConnect.lePassword.setText(str(valor7))


        self.dbProjects_.commit()
        print ("DATOS CARGADOS")
        #db.close()
        # hasta aqui la modificación 8

# MODIFICACION 9 PARA CONECTOR SQLITE :añado uso botón MOSTRAR TABLA DE REGISTROS-PROYECTOS
    @QtCore.pyqtSlot()
    def ShowTable(self):
        if self.dbProjects_:
            self.dbProjects_.close()
        # DEBUGGING:
        # pdb.set_trace()
        # print ("escribe `n´(next) para continuar / `q´(quit) para salir / `c´ para seguir sin debugg")
        
        #if not db.open():
        #    QMessageBox.critical(None, "Cannot open database",
        #            "Unable to establish a database connection.\n"
        #            "This example needs SQLite support. Please read the Qt SQL "
        #            "driver documentation for information how to build it.\n\n"
        #            "Click Cancel to exit.", QMessageBox.Cancel)
        #    return False
        #return True

        # Creamos la conexión con la BASE DE DATOS SQLITE3 DB
        self.dbProjects_ = sqlite3.connect(filedir(self.ui.leFolderSQLITE.text()) + '/pinebooconectores.sqlite')
        cursor = self.dbProjects_.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS proyectos(id INTEGER PRIMARY KEY, name TEXT, dbname TEXT, dbtype TEXT, dbhost TEXT, dbport TEXT, username TEXT, password TEXT)
        ''')
        cursor.execute('''SELECT id, name, dbname, dbtype, dbhost, dbport, username, password FROM proyectos''')
        conectores = cursor.fetchall()
        self.tableWidget.clear()
        self.tableWidget.setHorizontalHeaderLabels(['Name', 'DBname', 'DBType', 'DBHost', 'DBPort', 'Username', 'Password'])
        currentRowCount = self.tableWidget.rowCount() #necessary even when there are no rows in the table
        
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        # escribir el campo 0 de la fila 1:
        for conector in conectores:
            inx = conectores.index(conector)
            self.tableWidget.insertRow(inx)
            # add more if there is more columns in the database.
            self.tableWidget.setItem(inx, 0, QTableWidgetItem(conector[1]))
            self.tableWidget.setItem(inx, 1, QTableWidgetItem(conector[2]))
            self.tableWidget.setItem(inx, 2, QTableWidgetItem(conector[3]))
            self.tableWidget.setItem(inx, 3, QTableWidgetItem(conector[4]))
            self.tableWidget.setItem(inx, 4, QTableWidgetItem(conector[5]))
            self.tableWidget.setItem(inx, 5, QTableWidgetItem(conector[6]))
            self.tableWidget.setItem(inx, 6, QTableWidgetItem(conector[7]))

        #self.dbProjects_.commit()
        #self.dbProjects_.close()
        self.tableWidget.doubleClicked.connect(self.on_click)
        print ("TABLA MOSTRADA")
# hasta aqui la modificación 9
    
    @QtCore.pyqtSlot()
    def on_click(self):
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            DlgConnect.leFila.setText(str(currentQTableWidgetItem.row() + 1))
            self.ChargeProject()
            self.conectar()
            
    

# MODIFICACION 10 PARA CONECTOR SQLITE :añado uso botón BORRAR PROYECTO
    @QtCore.pyqtSlot()
    def DeleteProject(self):
        if self.dbProjects_:
            self.dbProjects_.close()
        # Creamos la conexión con la BASE DE DATOS SQLITE3 DB
        self.dbProjects_ = sqlite3.connect(filedir(self.ui.leFolderSQLITE.text()) + '/pinebooconectores.sqlite')
        
        cursor = self.dbProjects_.cursor()
        
        # ELEGIR UNA FILA DE LA TABLA proyectos DE LA BASE DE DATOS:
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            DlgConnect.leFila.setText(str(currentQTableWidgetItem.row() + 1))
            fila = str(self.ui.leFila.text())
        par = (fila,)
        print(par)
        cursor.execute("DELETE FROM proyectos WHERE id=?", par)
        #enviamos la orden:
        self.dbProjects_.commit()
        self.dbProjects_.close()

        print ("PROYECTO BORRADO")
        self.tableWidget.clear()
        self.ShowTable()
            
# hasta aqui la modificación 10

# MODIFICACION 11 PARA CONECTOR SQLITE :añado uso botón GUARDAR PROYECTO
    @QtCore.pyqtSlot()
    def SaveProject(self):

        #db = sqlite3.connect('pinebooconectores.sqlite')
        cursor = self.dbProjects_.cursor()
        cursor.execute('''SELECT id, name, dbname, dbtype, dbhost, dbport, username, password FROM proyectos''')
        conectores1 = cursor.fetchone()
        # Get a cursor object  para AÑADIR CAMPOS
        cursor = self.dbProjects_.cursor()
        #id2 = str(self.ui.leID.text())
        name2 = str(self.ui.leName.text())
        dbname2 = str(self.ui.leDBName.text())
        dbtype2 = self.ui.cBDrivers.currentText()
        dbhost2 = str(self.ui.leHostName.text())
        dbport2 = str(self.ui.lePort.text())
        username2 = str(self.ui.leUserName.text())
        password2 = str(self.ui.lePassword.text())


        with self.dbProjects_:
            cursor.execute('''
        INSERT INTO proyectos(name, dbname, dbtype, dbhost, dbport, username, password) VALUES (?,?,?,?,?,?,?)''', (name2, dbname2, dbtype2, dbhost2, dbport2, username2, password2))
        self.dbProjects_.commit()
        print ("PROYECTO GUARDADO")
        self.ShowTable()
        

        #self.dbProjects_.close()
# hasta aqui la modificación 11

# MODIFICACION 12 PARA CONECTOR SQLITE :añado uso botón GUARDAR PROYECTO de EJEMPLO
    @QtCore.pyqtSlot()
    def SaveProjectEjemplo(self):
        #db = sqlite3.connect('pinebooconectores.sqlite')
        # Get a cursor object para CREAR la tabla "proyectos"
        cursor = self.dbProjects_.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS proyectos(id INTEGER PRIMARY KEY, name TEXT, dbname TEXT, dbtype TEXT, dbhost TEXT, dbport TEXT, username TEXT, password TEXT)
''')
        self.dbProjects_.commit()
        # Get a cursor object  para AÑADIR CAMPOS DE EJEMPLO:
        cursor = self.dbProjects_.cursor()
        name1 = ''
        dbname1 = 'eneboobase'
        dbtype1 = 'QPSQL'
        dbhost1 = 'localhost'
        dbport1 = '5432'
        username1 = 'postgres'
        password1 = 'postgres'
        cursor.execute('''INSERT INTO proyectos(name, dbname, dbtype, dbhost, dbport, username, password) VALUES (?,?,?,?,?,?,?)''', (name1, dbname1, dbtype1, dbhost1, dbport1, username1, password1))
        self.dbProjects_.commit()

        # escribir los campos de la fila ELEGIDA en la zona de "CARGAR DATOS":
        DlgConnect.leName.setText(str(name1))
        DlgConnect.leDBName.setText(str(dbname1))
        #DlgConnect.leDBType.setText(str(dbtype1))
        DlgConnect.leHostName.setText(str(dbhost1))
        DlgConnect.lePort.setText(str(dbport1))
        DlgConnect.leUserName.setText(str(username1))
        DlgConnect.lePassword.setText(str(password1))
        # When we are done working with the DB we need to close the connection:
        #db.close()
        print ("PROYECTO DE EJEMPLO GRABADO y CARGADO")

# hasta aqui la modificación 12        