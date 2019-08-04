# -*- coding: utf-8 -*-
"""
AQSobjectsFactory Module.

This module provides the different classes and AQS functions to be used in the module scripts.
"""
import sys

# AQSObjects
from .aqsettings import AQSettings  # noqa: F401
from .aqsqlquery import AQSqlQuery  # noqa: F401
from .aqsqlcursor import AQSqlCursor  # noqa: F401
from .aqutil import AQUtil  # noqa: F401
from .aqsql import AQSql  # noqa: F401
from .aqsmtpclient import AQSmtpClient  # noqa: F401
from .aqs import AQS  # noqa: F401
from .aqboolflagstate import AQBoolFlagState, AQBoolFlagStateList  # noqa: F401
from .aqformdb import AQFormDB  # noqa: F401


if not getattr(sys, "frozen", False):  # FIXME: No module named 'xml.sax.expatreader' in deploy
    from .aqods import AQOdsGenerator, AQOdsSpreadSheet, AQOdsSheet, AQOdsRow  # noqa: F401
    from .aqods import AQOdsColor, AQOdsStyle, AQOdsImage  # noqa: F401
