# -*- coding: utf-8 -*-

from PyQt4.QtCore import QTime

from pineboolib.dbschema.schemaupdater import text2bool
from pineboolib.fllegacy import FLUtil

class PNSqlDrivers():

    driverName = None

    def __init__(self, driverName = "PGSql"):
        self.driverName = driverName


    def formatValue(self, type_, v, upper):
        util = FLUtil.FLUtil()
        if self.driverName == "PGSql":
            s = None
            # TODO: psycopg2.mogrify ???

            if type_ == "bool" or type_ == "unlock":
                s = text2bool(v)

            elif type_ == "date":
                s = "'%s'" % util.dateDMAtoAMD(v)
                
            elif type_ == "time":
                time = QTime(s)
                s = "'%s'" % time

            elif type_ == "uint" or type_ == "int" or type_ == "double" or type_ == "serial":
                s = v

            else:
                if upper == True and type_ == "string":
                    v = v.upper()

                s = "'%s'" % v
            #print ("PNSqlDriver.formatValue(%s, %s) = %s" % (type_, v, s))
            return s







