# -*- coding: utf-8 -*-

# Completa Si

import sip
from pineboolib.fllegacy.FLSqlDatabase import FLSqlDatabase
from pineboolib.fllegacy.FLUtil import FLUtil
from pineboolib import decorators

from PyQt4.QtCore import QString
# switch on QVariant in Python3
# sip.setapi('QVariant', 2)
sip.setapi('QString', 1)


"""
Clase para manejar distintas conexiones a bases de datos.

Cada conexión a una base de datos tendrá una cadena de caracteres
como nombre que la identifica. Se podrán añadir conexiones con FLSqlConnections::addDatabase,
eliminar con FLSqlConnections::removeDatabase y obtener con FLSqlConnections::database.

La conexión por defecto tendrá el nombre "default".

@author InfoSiAL S.L.
"""


class FLSqlConnections():

    @decorators.BetaImplementation
    def addDatabase(self, *args, **kwargs):
        if isinstance(args[0], QString):
            self.addDatabase1(args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7])
        elif len(args) < 2:
            self.addDatabase2(args[0])
        else:
            self.addDatabase2(args[0], args[1])

    """
    Añade una base de datos a las conexiones disponibles.

    La base de datos será abierta. Si ya existiera una conexión con el mismo nombre
    la base datos correspondiente será cerrada y borrada, sustituyéndola por la nueva.

    @param driverAlias Alias del driver ( PostgreSQL, MySQL, SQLite, ... ), ver FLSqlDatabase.
    @param nameDB  Nombre de la base de datos a la que conectar
    @param user  Usuario de la conexión
    @param password Contraseña para el usuario
    @param host  Nombre o dirección del servidor de la base de datos
    @param port  Puerto TCP de conexion
    @param connectionName Nombre de la conexion
    @param connectOptions Contiene opciones auxiliares de conexión a la base de datos.
                        El formato de la cadena de opciones es una lista separada por punto y coma
                        de nombres de opción o la opción = valor. Las opciones dependen del uso del
                        driver de base de datos.
    @return TRUE si se pudo realizar la conexión, FALSE en caso contrario
    """
    @decorators.BetaImplementation
    def addDatabase1(self, driverAlias, nameDB, user, password, host, port, connectionName, connectOptions=None):

        db = FLSqlDatabase()
        if not db.loadDriver(db.driverAliastoDriverName(driverAlias), connectionName):
            del db
            print("FLSqlConnections::addDatabase : Driver no cargado %s" % driverAlias)
            return False

        if not db.connectDB(nameDB, user, password, host, port, connectionName, connectOptions):
            del db
            print("FLSqlConnections::addDatabase : No se pudo conectar a %s" % nameDB)
            return False

        return self.addDatabase(db, connectionName)
    """
    Sobrecargada por conveniencia

    Practicamente hace lo mismo que el método anterior pero utilizando una base de datos ya construida

    @param db  Base datos a añadir a las conexiones disponibles, ver FLSqlDatabase.
    @param connectionName Nombre de la conexion
    @return TRUE si se pudo realizar la conexión, FALSE en caso contrario
    """
    @decorators.BetaImplementation
    def addDatabase2(self, db, connectionName="default"):
        if not self.d:
            self.d = FLSqlConnectionsPrivate()
        if not db:
            return False

        newDB = self.d.dictDB.get(connectionName)

        if newDB and newDB == db:
            return True

        self.d.dictDB[connectionName] = db
        if not self.d.defaultDB == db and connectionName == "default":
            self.d.defaultDB = db

        return True

    """
    Elimina una base de datos de las conexiones disponibles.

    Cierra la base de datos correspondiente y la elimina.

    @param connectionName Nombre de la conexion
    @return TRUE si se pudo eliminar la base de datos, FALSE en caso contrario
    """
    @decorators.BetaImplementation
    def removeDatabase(self, connectionName):
        if not self.d or not self.d.dictDB:
            return False

        if connectionName == "default":
            self.d.defaultDB = None

        return self.d.dictDB(connectionName).clear()

    """
    Obtiene la base de datos de una conexion.

    @param connectionNmae Nombre de la conexion
    @return La base de datos correspondiente al nombre de conexion indicado
    """
    @decorators.BetaImplementation
    def database(self, connectionName="default"):
        if not self.d:
            self.d = FLSqlConnectionsPrivate()

        if connectionName == "default":
            if not self.d.defaultDB:
                self.addDatabase(FLSqlDatabase())
            return self.d.defaultDB

        if not self.d.dictDB:
            self.addDatabase(FLSqlDatabase())
            return self.d.defaultDB

        ret = self.d.dictDB.get(connectionName)

        if not ret:
            print(FLUtil.translate("FLSqlConnections::database : No existe la conexión '%s', se devuelve la conexión por defecto 'default'" % connectionName))

            if not self.d.defaultDB:
                self.addDatabase(FLSqlDatabase())
            ret = self.defaultDB

        return ret

    """
    Finalizar todas las conexiones
    """
    @decorators.BetaImplementation
    def finish(self):
        del self.d

    """
    @return Diccionario con las bases de datos abiertas
    """
    @decorators.BetaImplementation
    def dictDatabases(self):
        if self.d and self.d.dictDB:
            return self.d.dictDB
        
        return None
    #private:

    """
    Privado
    """
    d = None


class FLSqlConnectionsPrivate():
    
    @decorators.BetaImplementation
    def __init__(self, *args, **kwargs):
        self.defaultDB = None
        self.dictDB = {}
    
    @decorators.BetaImplementation
    def __del__(self):
        self.defaultDB = None
        self.dictDB.clear()
    
