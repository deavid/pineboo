# # -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtCore, QtGui, Qt
from PyQt5.QtXml import QDomDocument
from PyQt5.Qt import QMessageBox

from importlib import import_module

from pineboolib.fllegacy.FLDataTable import FLDataTable

from pineboolib.plugins.dgi.dgi_schema import dgi_schema
from pineboolib import decorators
import pineboolib

import datetime
import sys
import re
import logging


def resolveObject(name):
    mod_ = import_module(__name__)
    ret_ = getattr(mod_, name, None)
    return ret_


class dgi_qt(dgi_schema):

    def __init__(self):
        super(dgi_qt, self).__init__()  # desktopEnabled y mlDefault a True
        self._name = "qt"
        self._alias = "Qt5"

    def __getattr__(self, name):
        return resolveObject(name)


class QWidget(Qt.QWidget):

    def child(self, name):
        return self.findChild(QtWidgets.QWidget, name)


class FLDataTable(FLDataTable):
    pass


class FLLineEdit(QtWidgets.QLineEdit):

    _tipo = None
    _partDecimal = 0
    _partInteger = 0
    _maxValue = None
    autoSelect = True
    _name = None
    _longitudMax = None
    _parent = None

    lostFocus = QtCore.pyqtSignal()

    def __init__(self, parent, name=None):
        super(FLLineEdit, self).__init__(parent)
        self._name = name
        if isinstance(parent.fieldName_, str):
            self._fieldName = parent.fieldName_
            self._tipo = parent.cursor_.metadata().fieldType(self._fieldName)
            self._partDecimal = parent.partDecimal_
            self._partInteger = parent.cursor_.metadata().field(self._fieldName).partInteger()
            self._longitudMax = parent.cursor_.metadata().field(self._fieldName).length()
            self._parent = parent

    def __getattr__(self, name):
        return DefFun(self, name)

    def setText(self, texto, b=True):
        # if self._maxValue:
        #    if self._maxValue < int(texto):
        #        texto = self._maxValue

        texto = str(texto)

        super(FLLineEdit, self).setText(texto)
        if not pineboolib.project._DGI.localDesktop():
            pineboolib.project._DGI._par.addQueque("%s_setText" % self._parent.objectName(), texto)
        # self.textChanged.emit(texto)

    def text(self):
        texto = str(super(FLLineEdit, self).text())

        if texto is None:
            texto = ""

        return str(texto)

    """
    Especifica un valor máximo para el text (numérico)
    """

    def setMaxValue(self, value):
        self.setMaxLength(value)
    """
    def focusInEvent(self, *f):
        print("focus in!! ---> ", f)
        if self._tipo == "double" or self._tipo == "int" or self._tipo == "Uint":
            self.blockSignals(True)
            s = self.text()
            super(FLLineEdit,self).setText(s)
            self.blockSignals(False)
        if self.autoSelect and self.selectedText().isEmpty() and not self.isReadOnly():
            self.selectAll()

        QtGui.QLineEdit.focusInEvent(f)

    def focusOutEvent(self, f):
        print("Adios --->", f)
        if self._tipo == "double" or self._tipo == "int" or self._tipo == "Uint":
            self.setText(self.text())

        super(FLLineEdit,self).focusOutEvent(self, f)

    """


class QPushButton(QtWidgets.QPushButton):

    def __init__(self, *args, **kwargs):
        super(QPushButton, self).__init__(*args, **kwargs)

    @property
    def pixmap(self):
        return self.icon()

    @property
    def enabled(self):
        return self.getEnabled()

    @enabled.setter
    def enabled(self, s):
        return self.setEnabled(s)

    @pixmap.setter
    def pixmap(self, value):
        return self.setIcon(value)

    def setPixmap(self, value):
        return self.setIcon(value)

    def getToggleButton(self):
        return self.isCheckable()

    def setToggleButton(self, v):
        return self.setCheckable(v)

    def getOn(self):
        return self.isChecked()

    def setOn(self, value):
        self.setChecked(value)

    toggleButton = property(getToggleButton, setToggleButton)
    on = property(getOn, setOn)


class FLPixmapView(QtWidgets.QScrollArea):
    frame_ = None
    scrollView = None
    autoScaled_ = None
    path_ = None
    pixmap_ = None
    pixmapView_ = None
    lay_ = None
    gB_ = None
    _parent = None

    def __init__(self, parent):
        super(FLPixmapView, self).__init__(parent)
        # self.scrollView = QtWidgets.QScrollArea(parent)
        self.autoScaled_ = False
        self.lay_ = QtWidgets.QHBoxLayout(self)
        self.pixmap_ = QtGui.QPixmap()
        self.pixmapView_ = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.pixmapView_.setSizePolicy(sizePolicy)
        self.lay_.addWidget(self.pixmapView_)
        self._parent = parent

    def setPixmap(self, pix):
        if not pineboolib.project._DGI.localDesktop():
            pineboolib.project._DGI._par.addQueque("%s_setPixmap" % self._parent.objectName(), self._parent.cursor_.valueBuffer(self._parent.fieldName_))
            return

        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        self.pixmap_ = pix
        if not self.autoScaled_:
            self.resize(self.pixmap_.size().width(),
                        self.pixmap_.size().height())
        else:
            self.pixmapView_.setScaledContents(True)
        self.pixmapView_.clear()
        self.pixmapView_.setPixmap(self.pixmap_)
        self.repaint()
        QtWidgets.QApplication.restoreOverrideCursor()

    def drawContents(self, p, cx, cy, cw, ch):
        p.setBrush(QtGui.QPalette.Background)
        p.drawRect(cx, cy, cw, ch)
        if self.autoScaled_:
            newWidth = self.width() - 2
            newHeight = self.height() - 2

            if self.pixmapWiev_ is not None and self.pixmapView_.width() == newWidth and self.pixmapView_.height() == newHeight:
                return

            img = self.pixmap_
            if img.width() > newWidth or img.height() > newHeight:
                self.pixmapView_.convertFromImage(img.scaled(
                    newWidth, newHeight, QtCore.Qt.KeepAspectRatio))
            else:
                self.pixmapView_.convertFromImage(img)

            if self.pixmapView_ is not None:
                p.drawPixmap((self.width() / 2) - (self.pixmapView_.width() / 2),
                             (self.height() / 2) - (self.pixmapView_.height() / 2), self.pixmapView_)
            elif self.pixmap_ is not None:
                p.drawPixmap((self.width() / 2) - (self.pixmap_.width() / 2),
                             (self.height() / 2) - (self.pixmap_.height() / 2), self.pixmap_)

    def previewUrl(self, url):
        u = QtCore.QUrl(url)
        if u.isLocalFile():
            path = u.path()

        if not path == self.path_:
            self.path_ = path
            img = QtGui.QImage(self.path_)

            if img is None:
                return

            pix = QtGui.QPixmap()
            QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
            pix.convertFromImage(img)
            QtWidgets.QApplication.restoreOverrideCursor()

            if pix is not None:
                self.setPixmap(pix)

    def clear(self):
        self.pixmapView_.clear()

    def pixmap(self):
        return self.pixmap_

    def setAutoScaled(self, autoScaled):
        self.autoScaled_ = autoScaled


class QLayoutWidget(QtWidgets.QWidget):
    pass


class QGroupBox(QtWidgets.QGroupBox):

    def __init__(self, *args, **kwargs):
        super(QGroupBox, self).__init__(*args, **kwargs)

    def setLineWidth(self, width):
        self.setContentsMargins(width, width, width, width)

    @property
    def selectedId(self):
        return 0


class QAction(QtWidgets.QAction):

    activated = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(QAction, self).__init__(*args, **kwargs)
        self.triggered.connect(self.send_activated)

    def send_activated(self, b=None):
        self.activated.emit()


class ProgressDialog(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(ProgressDialog, self).__init__(*args, **kwargs)
        self.title = "Untitled"
        self.step = 0
        self.steps = 100

    def __getattr__(self, name):
        return DefFun(self, name)

    def setup(self, title, steps):
        self.title = title
        self.step = 0
        self.steps = steps
        self.setWindowTitle("%s - %d/%d" % (self.title, self.step, self.steps))
        self.setWindowModality(QtCore.Qt.ApplicationModal)

    def setProgress(self, step):
        self.step = step
        self.setWindowTitle("%s - %d/%d" % (self.title, self.step, self.steps))
        if step > 0:
            self.show()
        self.update()
        QtCore.QCoreApplication.processEvents(
            QtCore.QEventLoop.ExcludeUserInputEvents)


class QLabel(QtWidgets.QLabel):

    def __getattr__(self, name):
        return DefFun(self, name)

    @QtCore.pyqtProperty(str)
    def text(self):
        return self.text()

    @text.setter
    def text(self, v):
        if not isinstance(v, str):
            v = str(v)
        self.setText(v)

    def setText(self, text):
        if not isinstance(text, str):
            text = str(text)
        super(QLabel, self).setText(text)


class QListView(QtWidgets.QListView):

    model = None

    def __init__(self, *args, **kwargs):
        super(QListView, self).__init__(*args, **kwargs)

        self.model = QtGui.QStandardItemModel(self)

    def __getattr__(self, name):
        return self.defaultFunction

    def addItem(self, item):
        it = QtGui.QStandardItem(item)
        self.model.appendRow(it)
        self.setModel(self.model)

    @decorators.Deprecated
    def setItemMargin(self, margin):
        pass

    @decorators.NotImplementedWarn
    def defaultFunction(self, *args, **kwargs):
        pass


class QDateEdit(QtWidgets.QDateEdit):

    _parent = None
    _date = None

    def __init__(self, parent):
        super(QDateEdit, self).__init__(parent)
        super(QDateEdit, self).setDisplayFormat("dd-MM-yyyy")
        self._parent = parent
        self.date_ = super(QDateEdit, self).date().toString(QtCore.Qt.ISODate)
        if not pineboolib.project._DGI.localDesktop():
            pineboolib.project._DGI._par.addQueque("%s_CreateWidget" % self._parent.objectName(), "QDateEdit")

    def getDate(self):
        ret = super(QDateEdit, self).date().toString(QtCore.Qt.ISODate)
        if ret != "2000-01-01":
            return ret
        else:
            return None

    def setDate(self, v):
        if not isinstance(v, str):
            if hasattr(v, "toString"):
                v = v.toString()
            else:
                v = str(v)

        date = QtCore.QDate.fromString(v[:10], "yyyy-MM-dd")
        super(QDateEdit, self).setDate(date)
        if not pineboolib.project._DGI.localDesktop():
            pineboolib.project._DGI._par.addQueque("%s_setDate" % self._parent.objectName(), "QDateEdit")

    date = property(getDate, setDate)

    def __getattr__(self, name):
        if name == "date":
            return super(QDateEdit, self).date().toString(QtCore.Qt.ISODate)


class FLDateEdit(QDateEdit):

    valueChanged = QtCore.pyqtSignal()
    DMY = "dd-MM-yyyy"
    _parent = None

    def __init__(self, parent, name):
        super(FLDateEdit, self).__init__(parent)
        self.setDisplayFormat("dd-MM-yyyy")
        self.setMinimumWidth(120)
        self.setMaximumWidth(120)
        self._parent = parent

    def setOrder(self, order):
        self.setDisplayFormat(order)

    def getDate(self):
        return super(FLDateEdit, self).date

    def setDate(self, d=None):
        from pineboolib.qsa import Date

        if d in (None, "NAN"):
            d = QtCore.QDate.fromString(str("01-01-2000"), "dd-MM-yyyy")
        if isinstance(d, str):
            if "T" in d:
                d = d[:d.find("T")]

        if isinstance(d, Date):
            d = d.date_

        if isinstance(d, datetime.date):
            d = QtCore.QDate.fromString(str(d), "yyyy-MM-dd")

        if not isinstance(d, QtCore.QDate):
            date = QtCore.QDate.fromString(d, "dd-MM-yyyy")
        else:
            date = d

        super(FLDateEdit, self).setDate(date)
        if not pineboolib.project._DGI.localDesktop():
            pineboolib.project._DGI._par.addQueque("%s_setDate" % self._parent.objectName(), date.toString())
        else:
            self.setStyleSheet('color: black')

    date = property(getDate, setDate)


class QTabWidget(QtWidgets.QTabWidget):

    def setTabEnabled(self, tab, enabled):

        idx = self.indexByName(tab)
        if idx is None:
            return

        if pineboolib.project._DGI.localDesktop():
            return QtWidgets.QTabWidget.setTabEnabled(self, idx, enabled)
        else:
            pineboolib.project._DGI._par.addQueque("%s_setTabEnabled" % self.objectName(), [idx, enabled])

            # try:
            #     for idx in range(self.count()):
            #         if self.widget(idx).objectName() == tab.lower():
            #             if not pineboolib.project._DGI.localDesktop():
            #                 pineboolib.project._DGI._par.addQueque("%s_setTabEnabled" % self.objectName(), [idx, enabled])
            #             return QtWidgets.QTabWidget.setTabEnabled(self, idx, enabled)

            # except ValueError:
            #     print("ERROR: Tab not found:: QTabWidget::setTabEnabled %r : %r" % (tab, enabled))
            #     return False
        # print("ERROR: Unknown type for 1st arg:: QTabWidget::setTabEnabled %r : %r" % (tab, enabled))

    def showPage(self, tab):

        idx = self.indexByName(tab)
        if idx is None:
            return

        if pineboolib.project._DGI.localDesktop():
            return QtWidgets.QTabWidget.setCurrentIndex(self, idx)
        else:
            pass
            # pineboolib.project._DGI._par.addQueque("%s_setTabEnabled" % self.objectName(), [idx, enabled])

    def indexByName(self, tab):

        idx = None
        if isinstance(tab, int):
            return tab
        elif not isinstance(tab, str):
            logger.error("ERROR: Unknown type tab name or index:: QTabWidget %r", tab)
            return None

        try:
            for idx in range(self.count()):
                if self.widget(idx).objectName() == tab.lower():
                    return idx
        except ValueError:
            logger.error("ERROR: Tab not found:: QTabWidget, tab name = %r", tab)
        return None


class FLTable(QtWidgets.QTableWidget):
    AlwaysOff = None

    def setNumRows(self, rows):
        self.setRowCount(rows)

    def setNumCols(self, cols):
        self.setColumnCount(cols)

    @decorators.NotImplementedWarn
    def setReadOnly(self, b):
        pass

    @decorators.NotImplementedWarn
    def setColumnMovingEnabled(self, b):
        pass

    @decorators.NotImplementedWarn
    def setVScrollBarMode(self, mode):
        pass

    @decorators.NotImplementedWarn
    def setHScrollBarMode(self, mode):
        pass


class QTable(QtWidgets.QTableWidget):

    lineaActual = None
    currentChanged = QtCore.pyqtSignal(int, int)
    doubleClicked = QtCore.pyqtSignal(int, int)

    def __init__(self, parent=None):
        super(QTable, self).__init__(parent)
        if not parent:
            self.setParent(self.parentWidget())

        self.lineaActual = -1
        self.currentCellChanged.connect(self.currentChanged_)
        self.cellDoubleClicked.connect(self.doubleClicked_)

    def currentChanged_(self, currentRow, currentColumn, previousRow, previousColumn):
        self.currentChanged.emit(currentRow, currentColumn)

    def doubleClicked_(self, f, c):
        self.doubleClicked.emit(f, c)

    def numRows(self):
        return self.rowCount()

    def numCols(self):
        return self.columnCount()

    def setNumCols(self, n):
        self.setColumnCount(n)

    def setNumRows(self, n):
        self.setRowCount(n)

    def setReadOnly(self, b):
        if b:
            self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        else:
            self.setEditTriggers(QtWidgets.QAbstractItemView.EditTriggers)

    @decorators.NotImplementedWarn
    def setColumnReadOnly(self, n, b):
        pass

    def selectionMode(self):
        return super(QTable, self).selectionMode()

    def setFocusStyle(self, m):
        self.setStyleSheet(m)

    def setColumnLabels(self, separador, lista):
        array_ = lista.split(separador)
        self.setHorizontalHeaderLabels(array_)

    def insertRows(self, numero):
        self.insertRow(numero)

    def text(self, row, col):
        return self.item(row, col).text()

    def setText(self, linea, col, value):
        # self.setItem(self.numRows() - 1, col, QtWidgets.QTableWidgetItem(str(value)))
        self.setItem(linea, col, QtWidgets.QTableWidgetItem(str(value)))

    @decorators.NotImplementedWarn
    def adjustColumn(self, k):
        pass

    @decorators.NotImplementedWarn
    def setRowReadOnly(self, row, b):
        pass

    # def __getattr__(self, name):
        # return DefFun(self, name)


class FLTimeEdit(QtWidgets.QTimeEdit):

    def __init__(self, parent):
        super(FLTimeEdit, self).__init__(parent)
        self.setDisplayFormat("hh:mm:ss")
        self.setMinimumWidth(90)
        self.setMaximumWidth(90)

    def setTime(self, v):
        if isinstance(v, str):
            v = v.split(':')
            time = QtCore.QTime(int(v[0]), int(v[1]), int(v[2]))
        else:
            time = v

        super(FLTimeEdit, self).setTime(time)
        if not pineboolib.project._DGI.localDesktop():
            pineboolib.project._DGI._par.addQueque("%s_setTime" % self._parent.objectName(), date.toString())

    def __getattr__(self, name):
        return DefFun(self, name)


class FLSpinBox(QtWidgets.QSpinBox):

    def __init__(self, parent=None):
        super(FLSpinBox, self).__init__(parent)
        # editor()setAlignment(Qt::AlignRight);

    def setMaxValue(self, v):
        self.setMaximum(v)


class QComboBox(QtWidgets.QComboBox):

    _parent = None

    def __init__(self, parent=None):
        self._parent = parent
        super(QComboBox, self).__init__(parent)

    # def __getattr__(self, name):
    #    return DefFun(self, name)

    @QtCore.pyqtProperty(str)
    def currentItem(self):
        return self.currentIndex

    @currentItem.setter
    def currentItem(self, i):
        if i:
            if not pineboolib.project._DGI.localDesktop():
                pineboolib.project._DGI._par.addQueque("%s_setCurrentIndex" % self.objectName(), n)
            self.setCurrentIndex(i)

    def insertStringList(self, strl):
        if not pineboolib.project._DGI.localDesktop():
            pineboolib.project._DGI._par.addQueque("%s_insertStringList" % self.objectName(), strl)
        self.insertItems(len(strl), strl)


"""
class QComboBox(QWidget):

    _label = None
    _combo = None

    def __init__(self):
        super(QComboBox, self).__init__()

        self._label = QtWidgets.QLabel(self)
        self._combo = QtWidgets.QComboBox(self)
        self._combo.setMinimumHeight(25)
        _lay = QtWidgets.QHBoxLayout()
        _lay.addWidget(self._label)
        _lay.addWidget(self._combo)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(True)
        self._combo.setSizePolicy(sizePolicy)

        self.setLayout(_lay)

    def __setattr__(self, name, value):
        if name == "label":
            self._label.setText(str(value))
        elif name == "itemList":
            self._combo.insertItems(len(value), value)
        elif name == "currentItem":
            self._combo.setCurrentText(str(value))
        else:
            super(QComboBox, self).__setattr__(name, value)

    def __getattr__(self, name):
        if name == "currentItem":
            return self._combo.currentText()
        else:
            return super(QComboBox, self).__getattr__(name)
"""


class QLineEdit(QtWidgets.QLineEdit):

    _parent = None

    def __init__(self, parent):
        super(QLineEdit, self).__init__(parent)
        self._parent = parent
        if not pineboolib.project._DGI.localDesktop():
            pineboolib.project._DGI._par.addQueque("%s_CreateWidget" % self._parent.objectName(), "QLineEdit")

    @QtCore.pyqtProperty(str)
    def text(self):
        return super(QLineEdit, self).text()

    @text.setter
    def text(self, v):
        if not isinstance(v, str):
            v = str(v)
        super(QLineEdit, self).setText(v)
        if not pineboolib.project._DGI.localDesktop():
            pineboolib.project._DGI._par.addQueque("%s_setText" % self._parent.objectName(), v)


class QTextEdit(QtWidgets.QTextEdit):

    _parent = None
    LogText = 0

    def __init__(self, parent):
        self._parent = parent
        super(QTextEdit, self).__init__(parent)
        self.LogText = 0

    def setText(self, text):
        super(QTextEdit, self).setText(text)
        if not pineboolib.project._DGI.localDesktop():
            pineboolib.project._DGI._par.addQueque("%s_setText" % self._parent.objectName(), text)

    @decorators.NotImplementedWarn
    def textFormat(self):
        return

    @decorators.Incomplete
    def setTextFormat(self, value):
        if value == 0:  # LogText
            self.setReadOnly(True)

    @decorators.NotImplementedWarn
    def setShown(self, value):
        pass

    @decorators.NotImplementedWarn
    def setAutoFormatting(self, value):
        pass


class QCheckBox(QtWidgets.QCheckBox):

    _parent = None

    def __init__(self, parent):
        self._parent = parent
        super(QCheckBox, self).__init__(parent)

    @QtCore.pyqtProperty(int)
    def checked(self):
        return self.isChecked()

    @checked.setter
    def checked(self, b):
        if isinstance(b, str):
            b = (b == "true")
        super(QCheckBox, self).setChecked(b)
        if not pineboolib.project._DGI.localDesktop():
            pineboolib.project._DGI._par.addQueque("%s_setChecked" % self._parent.objectName(), b)


class QToolButton(QtWidgets.QToolButton):

    groupId = None

    def __init__(self, parent):
        super(QToolButton, self).__init__(parent)
        self.groupId = None

    def setToggleButton(self, value):
        self.setDown(value)

    @decorators.Deprecated
    def setUsesBigPixmap(self, value):
        pass

    def toggleButton(self):
        return self.isDown()

    def getOn(self):
        return self.isChecked()

    def setOn(self, value):
        self.setChecked(value)

    on = property(getOn, setOn)

    @decorators.Deprecated
    def setUsesTextLabel(self, value):
        pass

    def buttonGroupId(self):
        return self.groupId

    def setButtonGroupId(self, id):
        self.groupId = id


class QButtonGroup(QtWidgets.QGroupBox):

    @decorators.NotImplementedWarn
    def setLineWidth(self, w):
        pass


class CheckBox(QWidget):
    _label = None
    _cb = None

    def __init__(self):
        super(CheckBox, self).__init__()

        self._label = QtWidgets.QLabel(self)
        self._cb = QtWidgets.QCheckBox(self)
        spacer = QtWidgets.QSpacerItem(
            1, 1, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        _lay = QtWidgets.QHBoxLayout()
        _lay.addWidget(self._cb)
        _lay.addWidget(self._label)
        _lay.addSpacerItem(spacer)
        self.setLayout(_lay)

    def __setattr__(self, name, value):
        if name == "text":
            self._label.setText(str(value))
        elif name == "checked":
            self._cb.setChecked(value)
        else:
            super(CheckBox, self).__setattr__(name, value)

    def __getattr__(self, name):
        if name == "checked":
            return self._cb.isChecked()
        else:
            return super(CheckBox, self).__getattr__(name)


class LineEdit(QWidget):
    _label = None
    _line = None

    def __init__(self):
        super(LineEdit, self).__init__()

        self._label = QtWidgets.QLabel(self)
        self._line = QtWidgets.QLineEdit(self)
        _lay = QtWidgets.QHBoxLayout()
        _lay.addWidget(self._label)
        _lay.addWidget(self._line)
        self.setLayout(_lay)

    def __setattr__(self, name, value):
        if name == "label":
            self._label.setText(str(value))
        elif name == "text":
            self._line.setText(str(value))
        else:
            super(LineEdit, self).__setattr__(name, value)

    def __getattr__(self, name):
        if name == "text":
            return self._line.text()
        else:
            return super(LineEdit, self).__getattr__(name)


FLDomDocument = QDomDocument
FLListViewItem = QtWidgets.QListView


class FileDialog(QtWidgets.QFileDialog):

    def getOpenFileName(*args):
        obj = None
        parent = QtWidgets.QApplication.activeModalWidget()
        if len(args) == 1:
            obj = QtWidgets.QFileDialog.getOpenFileName(parent, str(args[0]))
        elif len(args) == 2:
            obj = QtWidgets.QFileDialog.getOpenFileName(parent, str(args[0]), str(args[1]))
        elif len(args) == 3:
            obj = QtWidgets.QFileDialog.getOpenFileName(parent, str(args[0]), str(args[1]), str(args[2]))
        elif len(args) == 4:
            obj = QtWidgets.QFileDialog.getOpenFileName(parent, str(args[0]), str(args[1]), str(args[2]), str(args[3]))

        if obj is None:
            return None

        return obj[0]

    def getExistingDirectory(basedir=None, caption=None):
        if not basedir:
            from pineboolib.utils import filedir
            basedir = filedir("..")

        import pineboolib
        if pineboolib.project._DGI.localDesktop():
            parent = pineboolib.project.main_window.ui_
            ret = QtWidgets.QFileDialog.getExistingDirectory(parent, caption, basedir, QtWidgets.QFileDialog.ShowDirsOnly)
            if ret:
                ret = ret + "/"

            return ret


class MessageBox(QMessageBox):
    @classmethod
    def msgbox(cls, typename, text, button0, button1=None, button2=None, title=None, form=None):
        if title or form:
            logger.warn("MessageBox: Se intentó usar título y/o form, y no está implementado.")
        icon = QMessageBox.NoIcon
        title = "Message"
        if typename == "question":
            icon = QMessageBox.Question
            title = "Question"
        elif typename == "information":
            icon = QMessageBox.Information
            title = "Information"
        elif typename == "warning":
            icon = QMessageBox.Warning
            title = "Warning"
        elif typename == "critical":
            icon = QMessageBox.Critical
            title = "Critical"
        # title = unicode(title,"UTF-8")
        # text = unicode(text,"UTF-8")
        msg = QMessageBox(icon, str(title), str(text))
        msg.addButton(button0)
        if button1:
            msg.addButton(button1)
        if button2:
            msg.addButton(button2)
        return msg.exec_()

    @classmethod
    def question(cls, *args):
        return cls.msgbox("question", *args)

    @classmethod
    def information(cls, *args):
        return cls.msgbox("question", *args)

    @classmethod
    def warning(cls, *args):
        return cls.msgbox("warning", *args)

    @classmethod
    def critical(cls, *args):
        return cls.msgbox("critical", *args)


QColor = QtGui.QColor


class RadioButton(QtWidgets.QRadioButton):

    def __ini__(self):
        super(RadioButton, self).__init__()
        self.setChecked(False)

    def __setattr__(self, name, value):
        if name == "text":
            self.setText(value)
        elif name == "checked":
            self.setChecked(value)
        else:
            super(RadioButton, self).__setattr__(name, value)

    def __getattr__(self, name):
        if name == "checked":
            return self.isChecked()


class Dialog(QtWidgets.QDialog):
    _layout = None
    buttonBox = None
    okButtonText = None
    cancelButtonText = None
    okButton = None
    cancelButton = None
    _tab = None

    def __init__(self, title=None, f=None, desc=None):
        # FIXME: f no lo uso , es qt.windowsflg
        super(Dialog, self).__init__()
        if title:
            self.setWindowTitle(str(title))

        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self._layout = QtWidgets.QVBoxLayout()
        self.setLayout(self._layout)
        self.buttonBox = QtWidgets.QDialogButtonBox()
        self.okButton = QtWidgets.QPushButton("&Aceptar")
        self.cancelButton = QtWidgets.QPushButton("&Cancelar")
        self.buttonBox.addButton(
            self.okButton, QtWidgets.QDialogButtonBox.AcceptRole)
        self.buttonBox.addButton(
            self.cancelButton, QtWidgets.QDialogButtonBox.RejectRole)
        self.okButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)
        from PyQt5.Qt import QTabWidget
        self._tab = QTabWidget()
        self._tab.hide()
        self._layout.addWidget(self._tab)
        self.oKButtonText = None
        self.cancelButtonText = None

    def add(self, _object):
        self._layout.addWidget(_object)

    def exec_(self):
        if self.okButtonText:
            self.okButton.setText(str(self.okButtonText))
        if (self.cancelButtonText):
            self.cancelButton.setText(str(self.cancelButtonText))
        self._layout.addWidget(self.buttonBox)

        return super(Dialog, self).exec_()

    def newTab(self, name):
        if self._tab.isHidden():
            self._tab.show()
        self._tab.addTab(QtWidgets.QWidget(), str(name))

    def __getattr__(self, name):
        if name == "caption":
            name = self.setWindowTitle

        return getattr(super(Dialog, self), name)


class GroupBox(QtWidgets.QGroupBox):
    def __init__(self):
        super(GroupBox, self).__init__()
        self._layout = QtWidgets.QVBoxLayout()
        self.setLayout(self._layout)

    def add(self, _object):
        self._layout.addWidget(_object)

    def __setattr__(self, name, value):
        if name == "title":
            self.setTitle(str(value))
        else:
            super(GroupBox, self).__setattr__(name, value)


class QDialog(QtWidgets.QDialog):
    pass


class QVBoxLayout(QtWidgets.QVBoxLayout):
    pass


class QHBoxLayout(QtWidgets.QHBoxLayout):
    pass


class QFrame(QtWidgets.QFrame):
    pass
