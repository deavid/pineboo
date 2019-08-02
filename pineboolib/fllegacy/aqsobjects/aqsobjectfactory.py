# -*- coding: utf-8 -*-
"""
AQSobjectsFactory Module.

This module provides the different classes and AQS functions to be used in the module scripts.
"""
# AQSObjects
from pineboolib.fllegacy.aqsobjects.aqsettings import AQSettings  # noqa: F401
from pineboolib.fllegacy.aqsobjects.aqsqlquery import AQSqlQuery  # noqa: F401
from pineboolib.fllegacy.aqsobjects.aqsqlcursor import AQSqlCursor  # noqa: F401
from pineboolib.fllegacy.aqsobjects.aqutil import AQUtil  # noqa: F401
from pineboolib.fllegacy.aqsobjects.aqsql import AQSql  # noqa: F401
from pineboolib.fllegacy.aqsobjects.aqsmtpclient import AQSmtpClient  # noqa: F401
from pineboolib.fllegacy.aqsobjects.aqs import AQS  # noqa: F401
from pineboolib.fllegacy.aqsobjects.aqods import AQOdsGenerator, AQOdsSpreadSheet, AQOdsSheet, AQOdsRow  # noqa: F401
from pineboolib.fllegacy.aqsobjects.aqods import AQOdsColor, AQOdsStyle, AQOdsImage  # noqa: F401
from pineboolib.fllegacy.aqsobjects.aqboolflagstate import AQBoolFlagState, AQBoolFlagStateList  # noqa: F401
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pineboolib.fllegacy.flformdb import FLFormDB
    from PyQt5 import QtWidgets


def AQFormDB(action_name: str, parent: "QtWidgets.QWidget") -> "FLFormDB":
    """Return a FLFormDB instance."""

    from pineboolib.application.utils.convert_flaction import convertFLAction
    from pineboolib.application import project

    if project.conn is None:
        raise Exception("Project is not connected yet")

    ac_flaction = project.conn.manager().action(action_name)
    ac_xml = convertFLAction(ac_flaction)
    ac_xml.load()
    return ac_xml.mainform_widget
