# -*- coding: utf-8 -*-


from PyQt5 import QtCore, QtWidgets, QtGui  # , QtGui, QtWidgets, uic

import pineboolib
# from pineboolib.qsaglobals import ustr
from pineboolib.utils import DefFun
from pineboolib import decorators

Qt = QtCore.Qt
# TODO: separar en otro fichero de utilidades


def ustr1(t):
    if isinstance(t, str):
        return t
    # if isinstance(t, QtCore.QString): return str(t)
    # if isinstance(t, str): return str(t,"UTF-8")
    try:
        return str(t)
    except Exception as e:
        print("ERROR Coercing to string:", repr(t))
        print("ERROR", e.__class__.__name__, str(e))
        return None


def ustr(*t1):
    return "".join([ustr1(t) for t in t1])


class QLayoutWidget(QtWidgets.QWidget):
    pass


class ProjectClass(QtCore.QObject):
    def __init__(self):
        super(ProjectClass, self).__init__()
        self._prj = pineboolib.project

    def __iter__(self):
        # Para soportar el modo Javascript de "attribute" in object
        # agregamos soporte de iteración
        return iter(self.__dict__.keys())


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
                pineboolib.project._DGI._par.addQueqe("%s_setCurrentIndex" % self.objectName(), n)
            self.setCurrentIndex(i)

    def insertStringList(self, strl):
        if not pineboolib.project._DGI.localDesktop():
            pineboolib.project._DGI._par.addQueqe("%s_insertStringList" % self.objectName(), strl)
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
        # print("QTabWidget::setTabEnabled %r : %r" % (tab, enabled))
        if isinstance(tab, int):
            if not pineboolib.project._DGI.localDesktop():
                pineboolib.project._DGI._par.addQueqe("%s_setTabEnabled" % self.objectName(), [tab, enabled])
            return QtWidgets.QTabWidget.setTabEnabled(self, tab, enabled)
        if isinstance(tab, str):
            """
            tabs = [ str(QtWidgets.QTabWidget.tabText(self, i)).lower().replace("&","") for i in range(self.count()) ]
            try:
                idx = tabs.index(tab.lower())
                return QtWidgets.QTabWidget.setTabEnabled(self, idx, enabled)
            """
            try:
                for idx in range(self.count()):
                    if self.widget(idx).objectName() == tab.lower():
                        if not pineboolib.project._DGI.localDesktop():
                            pineboolib.project._DGI._par.addQueqe("%s_setTabEnabled" % self.objectName(), [idx, enabled])
                        return QtWidgets.QTabWidget.setTabEnabled(self, idx, enabled)

            except ValueError:
                print("ERROR: Tab not found:: QTabWidget::setTabEnabled %r : %r" % (tab, enabled))
                return False
        print("ERROR: Unknown type for 1st arg:: QTabWidget::setTabEnabled %r : %r" % (tab, enabled))


class QTable(QtWidgets.QTableWidget):

    lineaActual = None
    currentChanged = QtCore.pyqtSignal(int, int)

    def __init__(self, parent=None):
        super(QTable, self).__init__(parent)
        if not parent:
            self.setParent(self.parentWidget())

        self.lineaActual = -1
        self.currentCellChanged.connect(self.currentChanged_)

    def currentChanged_(self, currentRow, currentColumn, previousRow, previousColumn):
        self.currentChanged.emit(currentRow, currentColumn)

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
        self.setRowCount(numero + 1)

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
            pineboolib.project._DGI._par.addQueqe("%s_CreateWidget" % self._parent.objectName(), "QLineEdit")

    @QtCore.pyqtProperty(str)
    def text(self):
        return super(QLineEdit, self).text()

    @text.setter
    def text(self, v):
        if not isinstance(v, str):
            v = str(v)
        super(QLineEdit, self).setText(v)
        if not pineboolib.project._DGI.localDesktop():
            pineboolib.project._DGI._par.addQueqe("%s_setText" % self._parent.objectName(), "QLineEdit")

    # def __getattr__(self, name):
        # return DefFun(self, name)


class QListView(QtWidgets.QListView):

    model = None

    def __init__(self, *args, **kwargs):
        super(QListView, self).__init__(*args, **kwargs)

        self.model = QtGui.QStandardItemModel(self)

    def __getattr__(self, name):
        print("flcontrols.QListView: Emulando método %r" % name)
        return self.defaultFunction

    def addItem(self, item):
        it = QtGui.QStandardItem(item)
        self.model.appendRow(it)
        self.setModel(self.model)

    @decorators.Deprecated
    def setItemMargin(self, margin):
        pass

    def defaultFunction(self, *args, **kwargs):
        print("flcontrols.QListView: llamada a método no implementado", args, kwargs)


class QPushButton(QtWidgets.QPushButton):
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


class QGroupBox(QtWidgets.QGroupBox):

    def __init__(self, *args, **kwargs):
        super(QGroupBox, self).__init__(*args, **kwargs)

    def setLineWidth(self, width):
        self.setContentsMargins(width, width, width, width)
