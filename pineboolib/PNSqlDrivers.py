# -*- coding: utf-8 -*-

#from pineboolib.flcontrols import ProjectClass
from PyQt4.QtCore import QVariant, QTime, QString

from pineboolib.fllegacy.FLFieldMetaData import FLFieldMetaData
from pineboolib.dbschema.schemaupdater import text2bool
from pineboolib.fllegacy.FLUtil import FLUtil

class PNSqlDrivers():

    driverName = None

    def __init__(self, driverName = "PGSql"):
        self.driverName = driverName


    def formatValue(self, type_, v, upper):

        if self.driverName == "PGSql":
            s = None
            # TODO: psycopg2.mogrify ???

            if type_ == "bool" or type_ == "unlock":
                s = text2bool(v)

            elif type_ == "date":
                s = "'%s'" % FLUtil.dateDMAtoAMD(v)

            elif type_ == "time":
                time = QTime(s)
                s = "'%s'" % time

            elif type_ == "uint" or type_ == "int" or type_ == "double" or type_ == "serial":
                s = v

            else:
                if upper:
                    v = v.upper()

                s = "'%s'" % v
            #print ("PNSqlDriver.formatValue(%s, %s) = %s" % (type_, v, s))
            return s







