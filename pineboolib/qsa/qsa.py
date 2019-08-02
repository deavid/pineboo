# -*- coding: utf-8 -*-
"""
QSA Emulation module.

This file should be imported at top of QS converted files.
"""

from pineboolib.fllegacy.flutil import FLUtil  # noqa: F401
from pineboolib.fllegacy.systype import SysType as sys  # noqa: F401

# Usadas solo por import *
from pineboolib.fllegacy.flposprinter import FLPosPrinter  # noqa: F401
from pineboolib.fllegacy.flsqlquery import FLSqlQuery  # noqa: F401
from pineboolib.fllegacy.flsqlcursor import FLSqlCursor  # noqa: F401
from pineboolib.fllegacy.flnetwork import FLNetwork  # noqa: F401
from pineboolib.fllegacy.flreportviewer import FLReportViewer  # noqa: F401
from pineboolib.fllegacy.flapplication import FLApplication  # noqa: F401
from pineboolib.fllegacy.flvar import FLVar  # noqa: F401

from pineboolib.core.utils.utils_base import ustr, filedir  # noqa: F401
from pineboolib.application.types import Boolean, QString, String, Function, Object, Array, Date, AttributeDict, File, Dir  # noqa: F401
from pineboolib.fllegacy.aqsobjects.aqsobjectfactory import AQS  # noqa: F401
from .input import Input  # noqa: F401
from .utils import switch, qsaRegExp, RegExp, Math, Application, parseFloat, parseString, parseInt, isNaN, length, text  # noqa: F401
from .utils import startTimer, killTimer, debug, from_project, format_exc, isnan, replace  # noqa: F401
from .pncontrolsfactory import *  # noqa: F401


QFile = File
util = FLUtil
print_ = print

undefined = None
LogText = 0
RichText = 1
