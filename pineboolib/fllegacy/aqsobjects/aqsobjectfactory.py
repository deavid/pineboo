# -*- coding: utf-8 -*-

# AQSObjects
from pineboolib.fllegacy.aqsobjects.AQSettings import AQSettings
from pineboolib.fllegacy.aqsobjects.AQUtil import AQUtil as AQUtil_class
from pineboolib.fllegacy.aqsobjects.AQSql import AQSql
from pineboolib.fllegacy.aqsobjects.AQS import AQS as AQS_class
from pineboolib.fllegacy.aqsobjects.aqods import AQOdsGenerator, AQOdsSpreadSheet, AQOdsSheet, AQOdsRow, AQOdsColor, AQOdsStyle

import pineboolib

AQUtil = AQUtil_class()
AQS = AQS_class()


def AQFormDB(action_name, parent, other):
    ac_flaction = pineboolib.project.conn.manager().action(action_name)
    from pineboolib.utils import convertFLAction
    ac_xml = convertFLAction(ac_flaction)
    ac_xml.load()
    return ac_xml.mainform_widget
