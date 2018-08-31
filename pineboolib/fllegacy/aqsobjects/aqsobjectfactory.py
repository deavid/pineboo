# -*- coding: utf-8 -*-

# AQSObjects
from pineboolib.fllegacy.aqsobjects.AQSettings import AQSettings
from pineboolib.fllegacy.aqsobjects.AQUtil import AQUtil as AQUtil_class
from pineboolib.fllegacy.aqsobjects.AQSql import AQSql
from pineboolib.fllegacy.aqsobjects.AQS import AQS as AQS_class
import pineboolib

AQUtil = AQUtil_class()
AQS = AQS_class()


def AQFormDB(action_name, parent, other):
    from pineboolib.fllegacy.FLAction import FLAction
    ac = pineboolib.project.conn.manager().action(action_name)
    print("AC", ac)
    return pineboolib.project.conn.managerModules().createForm(ac, None, parent, name=None)
