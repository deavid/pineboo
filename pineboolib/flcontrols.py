# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets, QtGui  # , QtGui, QtWidgets, uic
from PyQt5.Qt import Qt


from pineboolib.utils import DefFun
from pineboolib import decorators
import pineboolib

import logging
logger = logging.getLogger("FLControls")

"""
Conjunto de controles que originalmente podian ser alcanzados desde QSA. Estos emulan los controles de QT3
"""


"""
Convierte a string un valor dado
@param t, valor a convertir
@return valor convertido
"""


def ustr1(t):
    if isinstance(t, str):
        return t
    # if isinstance(t, QtCore.QString): return str(t)
    # if isinstance(t, str): return str(t,"UTF-8")
    try:
        return str(t)
    except Exception as e:
        logger.error("ERROR Coercing to string:", repr(t), e.__class__.__name__, str(e))
        return None


"""
Convierte a string un array de valores datos
@param t1, array de valores
@return cadena string
"""


def ustr(*t1):
    return "".join([ustr1(t) for t in t1])


class QLayoutWidget(QtWidgets.QWidget):
    pass


class QCheckBox(QtWidgets.QCheckBox):
    def __getattr__(self, name):
        return DefFun(self, name)

    @QtCore.pyqtProperty(int)
    def checked(self):
        return self.isChecked()

    @checked.setter
    def checked(self, v):
        if not v:
            v = False
        if isinstance(v, str):
            v = (v == "true")
        self.setChecked(v)


class QToolButton(QtWidgets.QToolButton):

    def __getattr__(self, name):
        return DefFun(self, name)

    @QtCore.pyqtProperty(bool)
    def on(self):
        return self.isDown()


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


class QComboBox(QtWidgets.QComboBox):
    def __getattr__(self, name):
        return DefFun(self, name)

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


class QButtonGroup(QtWidgets.QGroupBox):
    def __getattr__(self, name):
        return DefFun(self, name)

    @property
    def selectedId(self):
        return 0


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


class FLTable(QtWidgets.QTableWidget):
    def __getattr__(self, name):
        return DefFun(self, name)


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
            pineboolib.project._DGI._par.addQueque("%s_setText" % self._parent.objectName(), "QLineEdit")

    # def __getattr__(self, name):
        # return DefFun(self, name)


class QDateEdit(QtWidgets.QDateEdit):

    _parent = None

    def __init__(self, parent):
        super(QDateEdit, self).__init__(parent)
        super(QDateEdit, self).setDisplayFormat("dd-MM-yyyy")
        self._parent = parent
        if not pineboolib.project._DGI.localDesktop():
            pineboolib.project._DGI._par.addQueque("%s_CreateWidget" % self._parent.objectName(), "QDateEdit")

    @QtCore.pyqtProperty(str)
    def date(self):
        if super(QDateEdit, self).date().toString(Qt.ISODate) == "2000-01-01":
            return None
        return super(QDateEdit, self).date().toString(Qt.ISODate)

    @date.setter
    def date(self, v):
        if not isinstance(v, str):
            v = str(v)
        super(QDateEdit, self).setDate(v)
        if not pineboolib.project._DGI.localDesktop():
            pineboolib.project._DGI._par.addQueque("%s_setDate" % self._parent.objectName(), "QDateEdit")


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


class QPushButton(QtWidgets.QPushButton):

    on = True  # FIXME :No se para que es

    def __init__(self, *args, **kwargs):
        super(QPushButton, self).__init__(*args, **kwargs)
        self.on = True

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

    toggleButton = property(getToggleButton, setToggleButton)

    def on(self):
        return self.on_

    def setOn(self, value):
        self.on_ = value


class QGroupBox(QtWidgets.QGroupBox):

    def __init__(self, *args, **kwargs):
        super(QGroupBox, self).__init__(*args, **kwargs)

    def setLineWidth(self, width):
        self.setContentsMargins(width, width, width, width)


class QAction(QtWidgets.QAction):

    activated = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(QAction, self).__init__(*args, **kwargs)
        self.triggered.connect(self.send_activated)

    def send_activated(self, b=None):
        self.activated.emit()


class QTextEdit(QtWidgets.QTextEdit):

    def __init__(self, *args, **kwargs):
        super(QTextEdit, self).__init__(*args, **kwargs)

    @decorators.NotImplementedWarn
    def textFormat(self):
        return

    @decorators.NotImplementedWarn
    def setTextFormat(self, value):
        pass

    @decorators.NotImplementedWarn
    def setShown(self, value):
        pass

    @decorators.NotImplementedWarn
    def setAutoFormatting(self, value):
        pass
