# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets, QtGui, QtXml  # type: ignore

from pineboolib.application.connections import proxy_fn

from pineboolib.application import project
from pineboolib.application.packager import aqunpacker
from pineboolib import qt3_widgets, fllegacy

from pineboolib.fllegacy.systype import SysType

"""
Conjunto de controles usados en Pineboo. Estos son cargados desde el DGI seleccionado en el proyecto
"""

QComboBox = qt3_widgets.qcombobox.QComboBox
QTable = qt3_widgets.qtable.QTable
QLayoutWidget = qt3_widgets.qwidget.QWidget
QToolButton = qt3_widgets.qtoolbutton.QToolButton
QTabWidget = qt3_widgets.qtabwidget.QTabWidget
QLabel = qt3_widgets.qlabel.QLabel
QGroupBox = qt3_widgets.qgroupbox.QGroupBox
QListView = qt3_widgets.qlistview.QListView
QPushButton = qt3_widgets.qpushbutton.QPushButton
QTextEdit = qt3_widgets.qtextedit.QTextEdit
QLineEdit = qt3_widgets.qlineedit.QLineEdit
QDateEdit = qt3_widgets.qdateedit.QDateEdit
QTimeEdit = qt3_widgets.qtimeedit.QTimeEdit
QCheckBox = qt3_widgets.qcheckbox.QCheckBox
QWidget = qt3_widgets.qwidget.QWidget
QColor = QtGui.QColor
QMessageBox = qt3_widgets.messagebox.MessageBox
QButtonGroup = qt3_widgets.qbuttongroup.QButtonGroup
QDialog = qt3_widgets.qdialog.QDialog
QVBoxLayout = qt3_widgets.qvboxlayout.QVBoxLayout
QHBoxLayout = qt3_widgets.qhboxlayout.QHBoxLayout
QFrame = qt3_widgets.qframe.QFrame
QMainWindow = qt3_widgets.qmainwindow.QMainWindow
QSignalMapper = QtCore.QSignalMapper
QDomDocument = QtXml.QDomDocument
QMenu = qt3_widgets.qmenu.QMenu
QToolBar = qt3_widgets.qtoolbar.QToolBar
QListWidgetItem = QtWidgets.QListWidgetItem
QListViewWidget = QtWidgets.QListWidget
QPixmap = QtGui.QPixmap
QImage = QtGui.QImage
QIcon = QtGui.QIcon
QAction = qt3_widgets.qaction.QAction
QActionGroup = QtWidgets.QActionGroup
QTreeWidget = QtWidgets.QTreeWidget
QTreeWidgetItem = QtWidgets.QTreeWidgetItem
QTreeWidgetItemIterator = QtWidgets.QTreeWidgetItemIterator
QDataView = qt3_widgets.qwidget.QWidget
QProcess = qt3_widgets.process.Process
QByteArray = qt3_widgets.qbytearray.QByteArray
QRadioButton = qt3_widgets.qradiobutton.QRadioButton
QSpinBox = qt3_widgets.qspinbox.QSpinBox
QInputDialog = QtWidgets.QInputDialog
QApplication = QtWidgets.QApplication
qApp = QtWidgets.qApp
QStyleFactory = QtWidgets.QStyleFactory
QFontDialog = QtWidgets.QFontDialog
QDockWidget = QtWidgets.QDockWidget
QMdiArea = qt3_widgets.qmdiarea.QMdiArea
QMdiSubWindow = QtWidgets.QMdiSubWindow
QKeySequence = QtGui.QKeySequence
QSize = QtCore.QSize
QSizePolicy = QtWidgets.QSizePolicy
QToolBox = QtWidgets.QToolBox
QPainter = QtGui.QPainter
QBrush = QtGui.QBrush
QProgressDialog = QtWidgets.QProgressDialog
QFileDialog = QtWidgets.QFileDialog

# Clases FL
FLLineEdit = fllegacy.fllineedit.FLLineEdit
FLTimeEdit = fllegacy.fltimeedit.FLTimeEdit
FLDateEdit = fllegacy.fldateedit.FLDateEdit
FLPixmapView = fllegacy.flpixmapview.FLPixmapView
FLDomDocument = QtXml.QDomDocument
FLDomElement = QtXml.QDomElement
FLDomNode = QtXml.QDomNode
FLDomNodeList = QtXml.QDomNodeList
FLListViewItem = fllegacy.fllistviewitem.FLListViewItem
FLTable = qt3_widgets.qtable.QTable
FLDataTable = fllegacy.fldatatable.FLDataTable
FLCheckBox = fllegacy.flcheckbox.FLCheckBox
FLTextEditOutput = fllegacy.fltexteditoutput.FLTextEditOutput
FLSpinBox = fllegacy.flspinbox.FLSpinBox
FLTableDB = fllegacy.fltabledb.FLTableDB
FLFieldDB = fllegacy.flfielddb.FLFieldDB
FLFormDB = fllegacy.flformdb.FLFormDB
FLFormRecordDB = fllegacy.flformrecorddb.FLFormRecordDB
FLFormSearchDB = fllegacy.flformsearchdb.FLFormSearchDB
FLDoubleValidator = fllegacy.fldoublevalidator.FLDoubleValidator
FLIntValidator = fllegacy.flintvalidator.FLIntValidator
FLUIntValidator = fllegacy.fluintvalidator.FLUIntValidator
FLCodBar = fllegacy.flcodbar.FLCodBar
FLWidget = fllegacy.flwidget.FLWidget
FLWorkSpace = fllegacy.flworkspace.FLWorkSpace

FormDBWidget = qt3_widgets.formdbwidget.FormDBWidget
# Clases QSA
CheckBox = qt3_widgets.checkbox.CheckBox
ComboBox = qt3_widgets.qcombobox.QComboBox
TextEdit = qt3_widgets.qtextedit.QTextEdit
LineEdit = qt3_widgets.lineedit.LineEdit
FileDialog = QtWidgets.QFileDialog
MessageBox = qt3_widgets.messagebox.MessageBox
RadioButton = qt3_widgets.radiobutton.RadioButton
Color = QtGui.QColor
Dialog = qt3_widgets.dialog.Dialog
Label = QtWidgets.QLabel
GroupBox = qt3_widgets.groupbox.GroupBox
Process = qt3_widgets.process.Process
SpinBox = qt3_widgets.qspinbox.QSpinBox
Line = QtCore.QLine
NumberEdit = qt3_widgets.numberedit.NumberEdit
DateEdit = qt3_widgets.qdateedit.QDateEdit
TimeEdit = qt3_widgets.qtimeedit.QTimeEdit

AQUnpacker = aqunpacker.AQUnpacker

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


def check_gc_referrers(typename: Any, w_obj: Callable, name: str) -> None:
    import threading
    import time

    def checkfn() -> None:
        import gc

        time.sleep(2)
        gc.collect()
        obj = w_obj()
        if not obj:
            return
        # TODO: Si ves el mensaje a continuación significa que "algo" ha dejado
        # ..... alguna referencia a un formulario (o similar) que impide que se destruya
        # ..... cuando se deja de usar. Causando que los connects no se destruyan tampoco
        # ..... y que se llamen referenciando al código antiguo y fallando.
        # print("HINT: Objetos referenciando %r::%r (%r) :" % (typename, obj, name))
        for ref in gc.get_referrers(obj):
            if isinstance(ref, dict):
                x: List[str] = []
                for k, v in ref.items():
                    if v is obj:
                        k = "(**)" + k
                        x.insert(0, k)
                # print(" - dict:", repr(x), gc.get_referrers(ref))
            else:
                if "<frame" in str(repr(ref)):
                    continue
                # print(" - obj:", repr(ref), [x for x in dir(ref) if getattr(ref, x) is obj])

    threading.Thread(target=checkfn).start()


class QEventLoop(QtCore.QEventLoop):
    def exitLoop(self) -> None:
        super().exit()

    def enterLoop(self) -> None:
        super().exec_()


def print_stack(maxsize: int = 1) -> None:
    for tb in traceback.format_list(traceback.extract_stack())[1:-2][-maxsize:]:
        print(tb.rstrip())


# from pineboolib.fllegacy.aqsobjects.aqsobjectfactory import *  # noqa:

# aqApp -- imported from loader.main after reload_from_DGI() call, as it is a cyclic dependency

# System = System_class()
# qsa_sys = SysType()
