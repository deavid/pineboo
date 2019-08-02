# -*- coding: utf-8 -*-
"""
QSA Emulation module.

This file should be imported at top of QS converted files.
"""

from pineboolib.core.utils.utils_base import ustr, filedir  # noqa: F401
from pineboolib.application.types import Boolean, QString, String, Function, Object, Array, Date, AttributeDict  # noqa: F401
from pineboolib.application.types import File, Dir  # noqa: F401

from .input import Input  # noqa: F401
from .utils import switch, qsaRegExp, RegExp, Math, Application, parseFloat, parseString, parseInt, isNaN, length, text  # noqa: F401
from .utils import startTimer, killTimer, debug, format_exc, isnan, replace  # noqa: F401
from .dictmodules import Application, from_project  # noqa: F401

# QT
from .pncontrolsfactory import QComboBox, QTable, QLayoutWidget, QToolButton, QTabWidget, QLabel, QGroupBox, QListView, QImage  # noqa: F401
from .pncontrolsfactory import QTextEdit, QLineEdit, QDateEdit, QTimeEdit, QCheckBox, QWidget, QMessageBox, QDialog  # noqa: F401
from .pncontrolsfactory import QVBoxLayout, QHBoxLayout, QFrame, QMainWindow, QMenu, QToolBar, QAction, QDataView, QByteArray  # noqa: F401
from .pncontrolsfactory import QMdiArea, QEventLoop, QActionGroup, QInputDialog, QApplication, QStyleFactory, QFontDialog  # noqa: F401
from .pncontrolsfactory import QMdiSubWindow, QSizePolicy, QProgressDialog, QFileDialog, QTreeWidget, QTreeWidgetItem  # noqa: F401
from .pncontrolsfactory import QTreeWidgetItemIterator, QListWidgetItem, QListViewWidget, QSignalMapper, QPainter, QBrush  # noqa: F401
from .pncontrolsfactory import QKeySequence, QIcon, QColor, QDomDocument, QPushButton, QSpinBox, QRadioButton, QPixmap  # noqa: F401
from .pncontrolsfactory import QButtonGroup, QToolBox, QSize, QDockWidget


# FL
from .pncontrolsfactory import FLDomDocument, FLDomElement, FLDomNode, FLDomNodeList, FLLineEdit, FLTimeEdit, FLDateEdit  # noqa: F401
from .pncontrolsfactory import FLPixmapView, FLDataTable, FLCheckBox, FLTextEditOutput, FLSpinBox, FLTableDB, FLFieldDB  # noqa: F401
from .pncontrolsfactory import FLFormDB, FLFormRecordDB, FLFormSearchDB, FLDoubleValidator, FLIntValidator, FLUIntValidator  # noqa: F401
from .pncontrolsfactory import FLCodBar, FLWidget, FLWorkSpace, FLPosPrinter, FLSqlQuery, FLSqlCursor, FLNetwork  # noqa: F401
from .pncontrolsfactory import FLApplication, FLVar, FLSmtpClient, FLTable, FLListViewItem, FLReportViewer, FLUtil


# QSA
from .pncontrolsfactory import FileDialog, Color, Label, Line, CheckBox, ComboBox, TextEdit, LineEdit, MessageBox, RadioButton  # noqa: F401
from .pncontrolsfactory import GroupBox, SpinBox, NumberEdit, DateEdit, TimeEdit, Dialog  # noqa: F401

# AQS

from .pncontrolsfactory import AQS, AQUnpacker, AQSettings, AQSqlQuery, AQSqlCursor, AQUtil, AQSql, AQSmtpClient  # noqa: F401
from .pncontrolsfactory import AQOdsGenerator, AQOdsSpreadSheet, AQOdsSheet, AQOdsRow, AQOdsColor, AQOdsStyle, AQOdsImage  # noqa: F401
from .pncontrolsfactory import AQBoolFlagState, AQBoolFlagStateList  # noqa: F401


from .pncontrolsfactory import aqApp
from .pncontrolsfactory import FormDBWidget
from .pncontrolsfactory import Process
from .pncontrolsfactory import sys


QFile = File
util = FLUtil
print_ = print

undefined = None
LogText = 0
RichText = 1
