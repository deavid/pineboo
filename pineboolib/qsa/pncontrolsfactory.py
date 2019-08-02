# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets, QtGui, QtXml  # type: ignore

from pineboolib.application.connections import proxy_fn

from pineboolib.application import project
from pineboolib.application.packager import aqunpacker

# from pineboolib import qt3_widgets, fllegacy


from pineboolib.fllegacy.systype import SysType

"""
Conjunto de controles usados en Pineboo. Estos son cargados desde el DGI seleccionado en el proyecto
"""
from pineboolib.qt3_widgets.qcombobox import QComboBox
from pineboolib.qt3_widgets.qtable import QTable
from pineboolib.qt3_widgets.qwidget import QWidget as QLayoutWidget
from pineboolib.qt3_widgets.qtoolbutton import QToolButton
from pineboolib.qt3_widgets.qtabwidget import QTabWidget
from pineboolib.qt3_widgets.qlabel import QLabel
from pineboolib.qt3_widgets.qgroupbox import QGroupBox
from pineboolib.qt3_widgets.qlistview import QListView
from pineboolib.qt3_widgets.qpushbutton import QPushButton
from pineboolib.qt3_widgets.qtextedit import QTextEdit
from pineboolib.qt3_widgets.qlineedit import QLineEdit
from pineboolib.qt3_widgets.qdateedit import QDateEdit
from pineboolib.qt3_widgets.qtimeedit import QTimeEdit
from pineboolib.qt3_widgets.qcheckbox import QCheckBox
from pineboolib.qt3_widgets.qwidget import QWidget
from pineboolib.qt3_widgets.messagebox import QMessageBox
from pineboolib.qt3_widgets.qbuttongroup import QButtonGroup
from pineboolib.qt3_widgets.qdialog import QDialog
from pineboolib.qt3_widgets.qvboxlayout import QVBoxLayout
from pineboolib.qt3_widgets.qhboxlayout import QHBoxLayout
from pineboolib.qt3_widgets.qframe import QFrame
from pineboolib.qt3_widgets.qmainwindow import QMainWindow
from pineboolib.qt3_widgets.qmenu import QMenu
from pineboolib.qt3_widgets.qtoolbar import QToolBar
from pineboolib.qt3_widgets.qaction import QAction
from pineboolib.qt3_widgets.qwidget import QWidget as QDataView
from pineboolib.qt3_widgets.process import Process
from pineboolib.qt3_widgets.qbytearray import QByteArray
from pineboolib.qt3_widgets.qradiobutton import QRadioButton
from pineboolib.qt3_widgets.qspinbox import QSpinBox
from pineboolib.qt3_widgets.qmdiarea import QMdiArea
from pineboolib.qt3_widgets.qeventloop import QEventLoop

from PyQt5.QtWidgets import QActionGroup
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import qApp
from PyQt5.QtWidgets import QStyleFactory
from PyQt5.QtWidgets import QFontDialog
from PyQt5.QtWidgets import QDockWidget
from PyQt5.QtWidgets import QMdiSubWindow
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QToolBox
from PyQt5.QtWidgets import QProgressDialog
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QTreeWidget
from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.QtWidgets import QTreeWidgetItemIterator
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QListWidget as QListViewWidget

from PyQt5.QtCore import QSignalMapper
from PyQt5.QtCore import QSize

from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QKeySequence
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor


from PyQt5.QtXml import QDomDocument

# Clases FL
from PyQt5.QtXml import QDomDocument as FLDomDocument
from PyQt5.QtXml import QDomElement as FLDomElement
from PyQt5.QtXml import QDomNode as FLDomNode
from PyQt5.QtXml import QDomNodeList as FLDomNodeList

from pineboolib.qt3_widgets.formdbwidget import FormDBWidget
from pineboolib.qt3_widgets.qtable import QTable as FLTable

from pineboolib.fllegacy.fllineedit import FLLineEdit
from pineboolib.fllegacy.fltimeedit import FLTimeEdit
from pineboolib.fllegacy.fldateedit import FLDateEdit
from pineboolib.fllegacy.flpixmapview import FLPixmapView
from pineboolib.fllegacy.fllistviewitem import FLListViewItem
from pineboolib.fllegacy.fldatatable import FLDataTable
from pineboolib.fllegacy.flcheckbox import FLCheckBox
from pineboolib.fllegacy.fltexteditoutput import FLTextEditOutput
from pineboolib.fllegacy.flspinbox import FLSpinBox
from pineboolib.fllegacy.fltabledb import FLTableDB
from pineboolib.fllegacy.flfielddb import FLFieldDB
from pineboolib.fllegacy.flformdb import FLFormDB
from pineboolib.fllegacy.flformrecorddb import FLFormRecordDB
from pineboolib.fllegacy.flformsearchdb import FLFormSearchDB
from pineboolib.fllegacy.fldoublevalidator import FLDoubleValidator
from pineboolib.fllegacy.flintvalidator import FLIntValidator
from pineboolib.fllegacy.fluintvalidator import FLUIntValidator
from pineboolib.fllegacy.flcodbar import FLCodBar
from pineboolib.fllegacy.flwidget import FLWidget
from pineboolib.fllegacy.flworkspace import FLWorkSpace


# Clases QSA
from pineboolib.qt3_widgets.checkbox import CheckBox
from pineboolib.qt3_widgets.qcombobox import QComboBox as ComboBox
from pineboolib.qt3_widgets.qtextedit import QTextEdit as TextEdit
from pineboolib.qt3_widgets.qlineedit import QLineEdit as LineEdit
from PyQt5.QtWidgets import QFileDialog as FileDialog
from pineboolib.qt3_widgets.messagebox import MessageBox
from pineboolib.qt3_widgets.radiobutton import RadioButton

from PyQt5.QtGui import QColor as Color
from pineboolib.qt3_widgets.dialog import Dialog
from PyQt5.QtWidgets import QLabel as Label
from pineboolib.qt3_widgets.groupbox import GroupBox
from pineboolib.qt3_widgets.process import Process
from pineboolib.qt3_widgets.qspinbox import QSpinBox as SpinBox
from PyQt5.QtCore import QLine as Line
from pineboolib.qt3_widgets.numberedit import NumberEdit
from pineboolib.qt3_widgets.qdateedit import QDateEdit as DateEdit
from pineboolib.qt3_widgets.qtimeedit import QTimeEdit as TimeEdit
from pineboolib.fllegacy.flapplication import aqApp


AQUnpacker = aqunpacker.AQUnpacker

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

# FIXME: meter todo QSA
# from pineboolib.fllegacy.aqsobjects.aqsobjectfactory import *

# FIXME: Belongs to RPC drivers
# def GET(function_name, arguments=[], conn=None) -> Any:
#     if conn is None:
#         conn = project.conn
#     if hasattr(conn.driver(), "send_to_server"):
#         return conn.driver().send_to_server(create_dict("call_function", function_name, conn.driver().id_, arguments))
#     else:
#         return "Funcionalidad no soportada"


# from pineboolib.fllegacy.aqsobjects.aqsobjectfactory import *  # noqa:

# aqApp -- imported from loader.main after reload_from_DGI() call, as it is a cyclic dependency

# System = System_class()
# qsa_sys = SysType()
