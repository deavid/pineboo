# -*- coding: utf-8 -*-
"""
QSA Emulation module.

This file should be imported at top of QS converted files.
"""

from pineboolib.core.utils.utils_base import ustr, filedir  # noqa: F401
from pineboolib.application.types import Boolean, QString, String, Function, Object  # noqa: F401
from pineboolib.application.types import File, Dir, Array, Date, AttributeDict  # noqa: F401

from .input import Input  # noqa: F401
from .utils import switch, qsaRegExp, RegExp, Math, parseFloat, parseString, parseInt  # noqa: F401
from .utils import startTimer, killTimer, debug, isnan, replace, isNaN, length, text  # noqa: F401
from .utils import format_exc  # noqa: F401
from .dictmodules import Application, from_project  # noqa: F401

# QT
from .pncontrolsfactory import QComboBox, QTable, QLayoutWidget, QToolButton  # noqa: F401
from .pncontrolsfactory import QTabWidget, QLabel, QGroupBox, QListView, QImage  # noqa: F401
from .pncontrolsfactory import QTextEdit, QLineEdit, QDateEdit, QTimeEdit  # noqa: F401
from .pncontrolsfactory import QCheckBox, QWidget, QMessageBox, QDialog  # noqa: F401
from .pncontrolsfactory import QVBoxLayout, QHBoxLayout, QFrame, QMainWindow  # noqa: F401
from .pncontrolsfactory import QMenu, QToolBar, QAction, QDataView, QByteArray  # noqa: F401
from .pncontrolsfactory import QMdiArea, QEventLoop, QActionGroup, QInputDialog  # noqa: F401
from .pncontrolsfactory import QApplication, QStyleFactory, QFontDialog  # noqa: F401
from .pncontrolsfactory import QMdiSubWindow, QSizePolicy, QProgressDialog  # noqa: F401
from .pncontrolsfactory import QFileDialog, QTreeWidget, QTreeWidgetItem  # noqa: F401
from .pncontrolsfactory import QTreeWidgetItemIterator, QListWidgetItem  # noqa: F401
from .pncontrolsfactory import QListViewWidget, QSignalMapper, QPainter, QBrush  # noqa: F401
from .pncontrolsfactory import QKeySequence, QIcon, QColor, QDomDocument  # noqa: F401
from .pncontrolsfactory import QPushButton, QSpinBox, QRadioButton, QPixmap  # noqa: F401
from .pncontrolsfactory import QButtonGroup, QToolBox, QSize, QDockWidget  # noqa: F401


# FL
from .pncontrolsfactory import FLDomDocument, FLDomElement, FLDomNode  # noqa: F401
from .pncontrolsfactory import FLDomNodeList, FLLineEdit, FLTimeEdit, FLDateEdit  # noqa: F401
from .pncontrolsfactory import FLPixmapView, FLDataTable, FLCheckBox  # noqa: F401
from .pncontrolsfactory import FLTextEditOutput, FLSpinBox, FLTableDB, FLFieldDB  # noqa: F401
from .pncontrolsfactory import FLFormDB, FLFormRecordDB, FLFormSearchDB  # noqa: F401
from .pncontrolsfactory import FLDoubleValidator, FLIntValidator, FLUIntValidator  # noqa: F401
from .pncontrolsfactory import FLCodBar, FLWidget, FLWorkSpace, FLPosPrinter  # noqa: F401
from .pncontrolsfactory import FLSqlQuery, FLSqlCursor, FLNetwork  # noqa: F401
from .pncontrolsfactory import FLApplication, FLVar, FLSmtpClient, FLTable  # noqa: F401
from .pncontrolsfactory import FLListViewItem, FLReportViewer, FLUtil  # noqa: F401


# QSA
from .pncontrolsfactory import FileDialog, Color, Label, Line, CheckBox, Dialog  # noqa: F401
from .pncontrolsfactory import ComboBox, TextEdit, LineEdit, MessageBox, RadioButton  # noqa: F401
from .pncontrolsfactory import GroupBox, SpinBox, NumberEdit, DateEdit, TimeEdit  # noqa: F401


# AQS
from .pncontrolsfactory import AQS, AQUnpacker, AQSettings, AQSqlQuery  # noqa: F401
from .pncontrolsfactory import AQSqlCursor, AQUtil, AQSql, AQSmtpClient  # noqa: F401

from pineboolib.application import project

if not project.DGI.isDeployed():  # FIXME: No module named 'xml.sax.expatreader' in deploy
    from .pncontrolsfactory import AQOdsGenerator, AQOdsSpreadSheet, AQOdsSheet  # noqa: F401
    from .pncontrolsfactory import AQOdsRow, AQOdsColor, AQOdsStyle, AQOdsImage  # noqa: F401

from .pncontrolsfactory import AQBoolFlagState, AQBoolFlagStateList  # noqa: F401


from .pncontrolsfactory import aqApp  # noqa: F401
from .pncontrolsfactory import FormDBWidget  # noqa: F401
from .pncontrolsfactory import Process  # noqa: F401
from .pncontrolsfactory import sys  # noqa: F401


QFile = File
util = FLUtil
print_ = print

undefined = None
LogText = 0
RichText = 1
