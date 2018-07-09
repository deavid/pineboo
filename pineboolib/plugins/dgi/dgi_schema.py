# # -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtCore, QtGui, Qt
from importlib import import_module
from xml.etree.ElementTree import fromstring
from json import dumps

from pineboolib.utils import DefFun
from pineboolib import decorators
from pineboolib.fllegacy.aqsobjects.AQSettings import AQSettings
import pineboolib
import sys
import datetime
import re
from PyQt5.QtXml import QDomDocument
from PyQt5.Qt import QMessageBox


def resolveObject(name):
    mod_ = import_module(__name__)
    ret_ = getattr(mod_, name, None)
    return ret_


class dgi_schema(object):

    _desktopEnabled = False
    _mLDefault = False
    _name = None
    _alias = None
    _localDesktop = True
    _mobile = False
    _deployed = False

    def __init__(self):
        self._desktopEnabled = True  # Indica si se usa en formato escritorio con interface Qt
        self.setUseMLDefault(True)
        self.setLocalDesktop(True)
        self._name = "dgi_shema"
        self._alias = "Default Schema"
        self.loadReferences()
        self.parserDGI = parserJson()
        try:
            import PyQt5.QtAndroidExtras
            self._mobile = True
        except ImportError:
            self._mobile = False

        if AQSettings().readBoolEntry(u"ebcomportamiento/mobileMode", False):
            self._mobile = True

        try:
            from pdytools import hexversion as pdy_hexversion
            self._deployed = True
        except ImportError:
            self._deployed = False

    def name(self):
        return self._name

    def alias(self):
        return self._alias

    # Establece un lanzador alternativo al de la aplicación
    def alternativeMain(self, options):
        pass

    def useDesktop(self):
        return self._desktopEnabled

    def setUseDesktop(self, val):
        self._desktopEnabled = val

    def localDesktop(self):  # Indica si son ventanas locales o remotas a traves de algún parser
        return self._localDesktop

    def setLocalDesktop(self, val):
        self._localDesktop = val

    def setUseMLDefault(self, val):
        self._mLDefault = val

    def useMLDefault(self):
        return self._mLDefault

    def setParameter(self, param):  # Se puede pasar un parametro al dgi
        pass

    def extraProjectInit(self):
        pass

    def showInitBanner(self):
        print("")
        print("=============================================")
        print("                 %s MODE               " % self._alias)
        print("=============================================")
        print("")
        print("")

    def mainForm(self):
        pass

    def loadReferences(self):
        return
        """
        self.FLLineEdit = FLLineEdit
        self.FLDateEdit = FLDateEdit
        self.FLTimeEdit = FLTimeEdit
        self.FLPixmapView = FLPixmapView
        self.FLSpinBox = FLSpinBox

        self.QPushButton = QPushButton
        self.QLineEdit = QLineEdit
        self.QComboBox = QComboBox
        self.QCheckBox = QCheckBox
        self.QTextEdit = QTextEdit
        """

    def mobilePlatform(self):
        return self._mobile

    def isDeployed(self):
        return self._deployed

    def iconSize(self):
        size = QtCore.QSize(22, 22)
        if self.mobilePlatform():
            size = QtCore.QSize(60, 60)

        return size

    def __getattr__(self, name):
        return resolveObject(name)
    

class QWidget(Qt.QWidget):
    

    def child(self, name):
        return self.findChild(QtWidgets.QWidget, name)


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
        if self._maxValue:
            if self._maxValue < int(texto):
                texto = self._maxValue

        texto = str(texto)

        # Miramos si le falta digitos a la parte decimal ...
        if self._tipo == "double" and len(texto) > 0:
            if texto == "0":
                d = 0
                texto = "0."
                while d < self._partDecimal:
                    texto = texto + "0"
                    d = d + 1

            i = None
            l = len(texto) - 1
            try:
                i = texto.index(".")
            except Exception:
                pass

            if i:
                # print("Posicion de . (%s) de %s en %s" % (i, l, texto))
                f = (i + self._partDecimal) - l
                # print("Part Decimal = %s , faltan %s" % (self._partDecimal, f))
                while f > 0:
                    texto = texto + "0"
                    f = f - 1

        super(FLLineEdit, self).setText(texto)
        if not pineboolib.project._DGI.localDesktop():
            pineboolib.project._DGI._par.addQueque("%s_setText" % self._parent.objectName(), texto)
        self.textChanged.emit(texto)

    def text(self):
        texto = str(super(FLLineEdit, self).text())

        if texto is None:
            texto = ""

        return str(texto)

    """
    Especifica un valor máximo para el text (numérico)
    """

    def setMaxValue(self, value):
        self._maxValue = value

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


class QToolButton(QtWidgets.QToolButton):

    def __getattr__(self, name):
        return DefFun(self, name)

    @QtCore.pyqtProperty(bool)
    def on(self):
        return self.isDown()


class FLPixmapView(QtWidgets.QWidget):
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


class FLTable(QtWidgets.QTableWidget):
    def __getattr__(self, name):
        return DefFun(self, name)


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

    def __init__(self, parent):
        self._parent = parent
        super(QTextEdit, self).__init__(parent)

    def setText(self, text):
        super(QTextEdit, self).setText(text)
        if not pineboolib.project._DGI.localDesktop():
            pineboolib.project._DGI._par.addQueque("%s_setText" % self._parent.objectName(), text)

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


"""
Exportador UI a JSON
"""


class parserJson():

    def __init__(self):
        self.aPropsForbidden = ['images', 'includehints', 'layoutdefaults',
                                'slots', 'stdsetdef', 'stdset', 'version', 'spacer', 'connections']
        self.aObjsForbidden = ['geometry', 'sizePolicy', 'margin', 'spacing', 'frameShadow',
                               'frameShape', 'maximumSize', 'minimumSize', 'font', 'focusPolicy', 'iconSet', 'author', 'comment', 'forwards', 'includes', 'sizepolicy', 'horstretch', 'verstretch']

    def isInDgi(self, property, type):
        if type == "prop":
            if property in self.aPropsForbidden:
                return False
            else:
                if property in self.aObjsForbidden:
                    return False

        return True

    def manageProperties(self, obj):
        if isinstance(obj, dict):
            for property in list(obj):
                if self.isInDgi(property, "prop"):
                    if property == "name" and not self.isInDgi(obj[property], "obj"):
                        del obj
                        return None
                    else:
                        prop = self.manageProperties(obj[property])
                        if prop:
                            obj[property] = prop
                        else:
                            del obj[property]
                else:
                    del obj[property]
        elif isinstance(obj, list):
            ind = 0
            while ind < len(obj):
                it = self.manageProperties(obj[ind])
                if it:
                    obj[ind] = it
                    ind += 1
                else:
                    del obj[ind]
        return obj

    def parse(self, name):
        from xmljson import yahoo as xml2json
        inputFile = name
        outputFile = re.search("\w+.ui", inputFile)

        if outputFile is None:
            print("Error. El fichero debe tener extension .ui")
            return None

        # ret_out = outputFile

        outputFile = re.sub(".ui", ".dgi", inputFile)

        try:
            ui = open(inputFile, 'r')
            xml = ui.read()

        except Exception:
            print("Error. El fichero no existe o no tiene formato XML")
            sys.exit()

        json = xml2json.data(fromstring(xml))
        json = self.manageProperties(json)
        strJson = dumps(json, sort_keys=True, indent=2)

        """
        try:
            dgi = open(outputFile, 'w')
            dgi.write(strJson)
            dgi.close()
        except:
            print("Error. Ha habido un problema durante la escritura del fichero")
            return None
        """
        strJson = strJson.replace("\n", "")
        strJson = " ".join(strJson.split())
        return strJson

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

FLDomDocument= QDomDocument
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
            from pinebooolib.utils import filedir
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
