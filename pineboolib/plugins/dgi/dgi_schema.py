# # -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtCore, QtGui
import datetime


class dgi_schema(object):

    _desktopEnabled = False
    _mLDefault = False
    _name = None
    _alias = None
    _localDesktop = True

    def __init__(self):
        self._desktopEnabled = True  # Indica si se usa en formato escritorio con interface Qt
        self.setUseMLDefault(True)
        self.setLocalDesktop(True)
        self._name = "dgi_shema"
        self._alias = "Default Schema"
        self.loadReferences()

    def name(self):
        return self._name

    def alias(self):
        return self._alias

    # Establece un lanzador alternativo al de la aplicación
    def alternativeMain(self, main_):
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
        self.FLLineEdit = FLLineEdit
        self.FLDateEdit = FLDateEdit
        self.FLTimeEdit = FLTimeEdit
        self.FLPixmapView = FLPixmapView
        self.FLSpinBox = FLSpinBox

        self.QPushButton = QtWidgets.QPushButton
        self.QLineEdit = QtWidgets.QLineEdit
        self.QComboBox = QtWidgets.QComboBox
        self.QCheckBox = QtWidgets.QCheckBox
        self.QTextEdit = QtWidgets.QTextEdit


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
            # self.textChanged.connect(self.controlFormato)
            self._parent = parent

    def __getattr__(self, name):
        return DefFun(self, name)

    def controlFormato(self):
        texto = str(super(FLLineEdit, self).text())
        denegarCambio_ = False
        denegarCambioEnteros_ = False
        cambiarComa_ = False
        decimales_ = None
        posComa_ = -1

        if texto == "" or texto == None:
            return
        """
        if self._tipo == "int" or self._tipo == "uint":
            if not texto is None:
                try:
                    float(decimales_)
                except:
                        denegarCambio_ = True
            
            texto = texto.replace(",",".")
            try:
                posComa_ = texto.index(".")
            except:
                if posComa_ > -1:
                    denegarCambio_ = True
            
        """
        if self._tipo == "string":
            if len(texto) > int(self._longitudMax):
                denegarCambio_ = True

        if self._tipo == "double":

            texto_old = texto
            if (QtCore.QLocale().decimalPoint() == ","):
                texto = texto.replace(".", ",")
            else:
                texto = texto.replace(",", ".")

            if not texto_old == texto:
                cambiarComa_ = True

            try:
                posComa_ = texto.index(".")
                #print("Coma encontrada en pos", posComa_, denegarCambio_)
            except:
                #print("Coma no encontrada", denegarCambio_)
                a = 1

            if posComa_ > -1:
                decimales_ = texto[posComa_ + 1:]

                if len(decimales_) > int(self._partDecimal):
                    #print("Parte decimal (%s) se pasa de %s" % (decimales_ , self._partDecimal))
                    denegarCambio_ = True

            enteros_ = texto

            if posComa_ > -1:
                enteros_ = texto[:posComa_]

            #print("enteros ...", enteros_)
            if len(enteros_) > int(self._partInteger):
                #print("Parte entera (%s) se pasa de %s" % (enteros_ , self._partInteger))
                denegarCambioEnteros_ = True

            #print("Decimales =", decimales_ , type(decimales_))
            if not decimales_ is None:
                try:
                    float(decimales_)
                except:
                    #print("Decimal esta mal", decimales_, len(decimales_))
                    if len(decimales_) > 0:
                        denegarCambio_ = True

            #print("Enteros =", enteros_, type(enteros_))
            try:
                float(enteros_)
            except:
                #print("Entero esta mal")
                denegarCambioEnteros_ = True
            # if not decimales_.isdecimal():
                #denegarCambio_ = True

            # if not enteros_.isdecimal():
                #denegarCambioEnteros_ = True

        #print("Procesado final", texto, denegarCambio_)

        if denegarCambio_ == True:
            texto = texto[0:len(texto) - 1]
            super(FLLineEdit, self).setText(texto)

        if denegarCambioEnteros_ == True and not decimales_ == None:
            texto = "%s%s%s" % (
                enteros_[0:len(enteros_) - 1], QtCore.QLocale().decimalPoint(), decimales_)
            super(FLLineEdit, self).setText(texto)
        elif denegarCambioEnteros_ == True and decimales_ == None:
            texto = enteros_[0:len(enteros_) - 1]
            super(FLLineEdit, self).setText(texto)

        if cambiarComa_ == True:
            super(FLLineEdit, self).setText(texto)

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
            except:
                pass

            if i:
                #print("Posicion de . (%s) de %s en %s" % (i, l, texto))
                f = (i + self._partDecimal) - l
                #print("Part Decimal = %s , faltan %s" % (self._partDecimal, f))
                while f > 0:
                    texto = texto + "0"
                    f = f - 1

        super(FLLineEdit, self).setText(texto)
        self.textChanged.emit(texto)

    def text(self):
        texto = str(super(FLLineEdit, self).text())

        if texto is "":
            texto = None

        if texto is None:
            if self._tipo == "string":
                texto = ""

            elif self._tipo == "double":
                d = 0
                texto = "0."
                while d < self._partDecimal:
                    texto = texto + "0"
                    d = d + 1

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


class FLPixmapView(QtWidgets.QWidget):
    frame_ = None
    scrollView = None
    autoScaled_ = None
    path_ = None
    pixmap_ = None
    pixmapView_ = None
    lay_ = None
    gB_ = None

    def __init__(self, parent):
        super(FLPixmapView, self).__init__(parent)
        self.scrollView = QtWidgets.QScrollArea(parent)
        self.autoScaled_ = False
        self.lay_ = QtWidgets.QHBoxLayout(self)
        self.pixmap_ = QtGui.QPixmap()
        self.pixmapView_ = QtWidgets.QLabel(self)
        self.lay_.addWidget(self.pixmapView_)

    def setPixmap(self, pix):
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

            if not self.pixmapWiev_ is None and self.pixmapView_.width() == newWidth and self.pixmapView_.height() == newHeight:
                return

            img = self.pixmap_
            if img.width() > newWidth or img.height() > newHeight:
                self.pixmapView_.convertFromImage(img.scaled(
                    newWidth, newHeight, QtCore.Qt.KeepAspectRatio))
            else:
                self.pixmapView_.convertFromImage(img)

            if not self.pixmapView_ is None:
                p.drawPixmap((self.width() / 2) - (self.pixmapView_.width() / 2),
                             (self.height() / 2) - (self.pixmapView_.height() / 2), self.pixmapView_)
            elif not self.pixmap_ is None:
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

            if not pix is None:
                self.setPixmap(pix)

    def clear(self):
        self.pixmapView_.clear()

    def pixmap(self):
        return self.pixmap_

    def setAutoScaled(self, autoScaled):
        self.autoScaled_ = autoScaled


class FLDateEdit(QtWidgets.QDateEdit):

    valueChanged = QtCore.pyqtSignal()
    DMY = "dd-MM-yyyy"

    def __init__(self, parent, name):
        super(FLDateEdit, self).__init__(parent)
        self.setDisplayFormat("dd-MM-yyyy")
        self.setMinimumWidth(120)
        self.setMaximumWidth(120)

    def setOrder(self, order):
        self.setDisplayFormat(order)

    def setDate(self, d=None):
        from pineboolib.qsatype import Date

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
        self.setStyleSheet('color: black')

    def __getattr__(self, name):
        return DefFun(self, name)


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

    def __getattr__(self, name):
        return DefFun(self, name)


class FLSpinBox(QtWidgets.QSpinBox):

    def __init__(self, parent=None):
        super(FLSpinBox, self).__init__(parent)
        # editor()setAlignment(Qt::AlignRight);

    def setMaxValue(self, v):
        self.setMaximum(v)
