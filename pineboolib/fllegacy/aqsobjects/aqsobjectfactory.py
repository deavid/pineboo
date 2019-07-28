# -*- coding: utf-8 -*-

# AQSObjects
from pineboolib.fllegacy.aqsobjects.aqsettings import AQSettings  # noqa: F401
from pineboolib.fllegacy.aqsobjects.aqsqlquery import AQSqlQuery  # noqa: F401
from pineboolib.fllegacy.aqsobjects.aqsqlcursor import AQSqlCursor  # noqa: F401
from pineboolib.fllegacy.aqsobjects.aqutil import AQUtil as AQUtil_class
from pineboolib.fllegacy.aqsobjects.aqsql import AQSql  # noqa: F401
from pineboolib.fllegacy.aqsobjects.aqsmtpclient import AQSmtpClient  # noqa: F401
from pineboolib.fllegacy.aqsobjects.aqs import AQS as AQS_class
from pineboolib.fllegacy.aqsobjects.aqods import (
    AQOdsGenerator,
    AQOdsSpreadSheet,
    AQOdsSheet,
    AQOdsRow,
)  # noqa: F401
from pineboolib.fllegacy.aqsobjects.aqods import (
    AQOdsColor,
    AQOdsStyle,
    AQOdsImage,
)  # noqa: F401
from pineboolib.fllegacy.aqsobjects.aqboolflagstate import (
    AQBoolFlagState,
    AQBoolFlagStateList,
)  # noqa: F401
from typing import Any

AQUtil = AQUtil_class()
AQS = AQS_class()

"""
FLFormDB
"""


def AQFormDB(action_name, parent, other) -> Any:
    from pineboolib.application.utils.convert_flaction import convertFLAction
    from pineboolib.application import project

    if project.conn is None:
        raise Exception("Project is not connected yet")

    ac_flaction = project.conn.manager().action(action_name)
    ac_xml = convertFLAction(ac_flaction)
    ac_xml.load()
    return ac_xml.mainform_widget
