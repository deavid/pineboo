# -*- coding: utf-8 -*-

from PyQt4 import QtCore,QtGui

from PyQt4.QtCore import QString, Qt

# TODO: Borrar el import del QVariant!!. QVariant es necesario en C++ porque es
# ... el único modo de representar un tipo polimórfico. En Python esto es innecesario.
from PyQt4.QtCore import QVariant

from pineboolib import decorators
from pineboolib.fllegacy.FLSqlCursor import FLSqlCursor
from pineboolib.utils import DefFun, filedir
from pineboolib.fllegacy.FLSettings import FLSettings
from pineboolib.fllegacy.FLUtil import FLUtil
from pineboolib.fllegacy.FLFieldMetaData import FLFieldMetaData
from pineboolib.fllegacy.FLTableMetaData import FLTableMetaData
#from pineboolib.fllegacy.FLSqlConnections import FLSqlConnections
from pineboolib.fllegacy.FLRelationMetaData import FLRelationMetaData
from pineboolib.fllegacy.FLSqlQuery import FLSqlQuery
from pineboolib.fllegacy.FLManager import FLManager
from pineboolib.fllegacy.FLFormSearchDB import FLFormSearchDB
from pineboolib.flparser.flpremerge import isinside



class FLLineEdit(QtGui.QLineEdit):

    _tipo = None
    partDecimal = 0
    _maxValue = None
    autoSelect = True
    _name = None

    lostFocus = QtCore.pyqtSignal()


    def __init__(self, parent, name):
        super(FLLineEdit,self).__init__(parent)
        self._name = name
        self._fieldName = parent.fieldName_
        self._tipo = parent.cursor_.metadata().fieldType(self._name)


    def setText(self, texto):
        if self._maxValue:
            if self._maxValue < int(texto):
                texto = self._maxValue
        super(FLLineEdit, self).setText(str(texto))
        self.textChanged.emit(texto)

    def text(self):
        texto =  super(FLLineEdit, self).text()
        if texto == "":
            texto = None

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
class FLFieldDB(QtGui.QWidget):

    _loaded = False
    _parent = None


    _tipo = None
    _lineEdit = None
    _partDecimal = None
    autoSelect = False

    editor_ = False #Editor para el contenido del campo que representa el componente
    fieldName_ = None #Nombre del campo de la tabla al que esta asociado este componente
    tableName_ = None #Nombre de la tabla fóranea
    actionName_ = None #Nombre de la accion
    foreignField_ = None #Nombre del campo foráneo
    fieldRelation_ = None #Nombre del campo de la relación
    filter_ = None #Nombre del campo de la relación
    cursor_ = None #Cursor con los datos de la tabla origen para el componente
    cursorInit_ = False #Indica que si ya se ha inicializado el cursor
    cursorAuxInit = None #Indica que si ya se ha inicializado el cursor auxiliar
    cursorBackup_ = False #Backup del cursor por defecto para acceder al modo tabla externa
    cursorAux = False #Cursor auxiliar de uso interno para almacenar los registros de la tabla relacionada con la de origen

    topWidget_ = False
    showed = False
    showAlias_ = True
    datePopup_ = None
    dateFrame_ = None
    datePickedOn_ = False
    autoComPopup_ = None
    autoComFrame_ = None
    accel_ = None
    keepDisabled_ = False
    editorImg_ = None
    pbAux_ = None
    pbAux2_ = None
    pbAux3_ = None
    pbAux4_ = None
    fieldAlias_ = None
    showEditor_ = True
    fieldMapValue_ = None
    autoCompMode_ = "OnDemandF4"
    timerAutoComp_ = False
    textFormat_ = QtCore.Qt.AutoText
    initNotNullColor_ = False
    textLabelDB = None
    FLWidgetFieldDBLayout = None
    name = None

    _initCursorWhenLoad = False
    _initEditorWhenLoad = False

    editorImgInit_ = None

    pushButtonDB = None
    keyF4Pressed = QtCore.pyqtSignal()
    labelClicked = QtCore.pyqtSignal()
    keyReturnPressed = QtCore.pyqtSignal()
    lostFocus = QtCore.pyqtSignal()
    textChanged = QtCore.pyqtSignal(QString)
    keyF2Pressed_ = QtCore.pyqtSignal(name = "keyF2Pressed")


    def __init__(self, parent, *args):
        super(FLFieldDB, self).__init__(parent)






        self.maxPixImages_ = FLSettings().readEntry("maxPixImages",None)
        if self.maxPixImages_ is None:
            self.maxPixImages_ = 600

        self.topWidget_ = self.topLevelWidget()

        #self._parent = parent

        self.FLLayoutH = QtGui.QVBoxLayout(self)

        self.lytButtons = QtGui.QHBoxLayout()
        self.lytButtons.setMargin(0)
        self.lytButtons.setSpacing(2)
        #self.lytButtons.SetMinimumSize(22,22)
        #self.lytButtons.SetMaximumSize(22,22)


        self.FLWidgetFieldDBLayout = QtGui.QHBoxLayout()
        self.FLLayoutH.addLayout(self.lytButtons)
        self.FLLayoutH.addLayout(self.FLWidgetFieldDBLayout)
        self.tableName_ = QString()
        self.fieldName_ = QString()
        self.foreignField_ = QString()
        self.fieldRelation_ = QString()
        self.textLabelDB = QtGui.QLabel() #No inicia originalmente aqui
        self.fieldAlias_ = QString()
        self.actionName_ = QString()
        self.filter_ = QString()


        self.FLWidgetFieldDBLayout.addWidget(self.textLabelDB)

        self.pushButtonDB = QtGui.QPushButton()

        self.setFocusProxy(self.pushButtonDB)
        #self.pushButtonDB.setFlat(True)
        PBSizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed ,QtGui.QSizePolicy.Fixed)
        PBSizePolicy.setHeightForWidth(True)
        self.pushButtonDB.setSizePolicy(PBSizePolicy)
        self.pushButtonDB.setMinimumSize(32, 32)
        self.pushButtonDB.setFocusPolicy(Qt.NoFocus)
        self.pushButtonDB.setIcon(QtGui.QIcon(filedir("icons","flfielddb.png")))
        self.FLWidgetFieldDBLayout.addWidget(self.pushButtonDB)
        self.pushButtonDB.clicked.connect(self.searchValue)


        self.timer_1 = QtCore.QTimer(self)
        self.timer_1.singleShot(120, self.loaded)





    def __getattr__(self, name): return DefFun(self, name)


    def loaded(self):
        self._loaded = True
        while True: #Ahora podemos buscar el cursor ... porque ya estamos añadidos al formulario
            parent = getattr(self.topWidget_,"cursor_", None)
            if parent:
                break
            new_parent = self.topWidget_.parentWidget()
            if new_parent is None:
                self.topWidget_ = None
                print("FLFieldDB : El widget de nivel superior deber ser de la clase FLFormDB o heredar de ella (o fuí demasiado rápido y no lo esperé)")
                break
            self.topWidget_ = new_parent

        if self.topWidget_:
                self.cursor_ = self.topWidget_.cursor()
                #print("Hay topWidget en %s", self)


        if not self.name:
            self.setName("FLFieldDB")

        self.cursorBackup_ = False
        self.partDecimal_ = -1




    def setName(self, value):
        self.name = str(value)

    """
    Para obtener el nombre de la accion.

    @return Nombre de la accion
    """

    def actionName(self):
        return self.actionName_

    """
    Para establecer el nombre de la accion.

    @param aN Nombre de la accion
    """

    def setActionName(self, aN):
        self.actionName_ = QString(aN)
        if self.showed and self.topWidget_:
            self.initEditor()
            self.initCursor()

        else:
            self._initCursorWhenLoad = True
            self._initEditorWhenLoad = True
            self.initFakeEditor()

    """
    Para obtener el nombre del campo.

    @return Nombre del campo
    """

    def fieldName(self):
        return self.fieldName_

    """
    Para añadir un filtro al cursor.

    """

    def setFilter(self, f):
        if not self.filter_ == f:
            self.filter_ = f
            self.setMaValue()

    """
    Para obtener el filtro del cursor.

    """

    def filter(self):
        return self.fliter_

    """
    Para establecer el nombre del campo.

    @param fN Nombre del campo
    """

    def setFieldName(self, fN):
        self.fieldName_ = QString(fN)
        if self.showed:
            if self.topWidget_:
                self.initCursor()
                self.initEditor()
            else:
                self.initFakeEditor()
        else:
            self._initCursorWhenLoad = True
            self._initEditorWhenLoad = True

    """
    Para obtener el nombre de la tabla foránea.

    @return Nombre de la tabla
    """

    def tableName(self):
        return self.tableName_

    """
    Para establecer el nombre de la tabla foránea.

    @param fT Nombre de la tabla
    """

    def setTableName(self, fT):
        self.tableName_ = QString(fT)
        if self.showed:
            if self.topWidget_:
                self.initCursor()
                self.initEditor()
            else:
                self.initFakeEditor()
        else:
            self._initCursorWhenLoad = True
            self._initEditorWhenLoad = True


    """
    Para obtener el nombre del campo foráneo.

    @return Nombre del campo
    """

    def foreignField(self):
        return self.foreingField_
    """
    Para establecer el nombre del campo foráneo.

    @param fN Nombre del campo
    """

    def setForeignField(self, fN):
        self.foreignField_ = QString(fN)
        if self.showed:
            if self.topWidget:
                self.initCursor()
                self.initEditor()
            else:
                self.initFakeEditor()
        else:
            self._initCursorWhenLoad = True
            self._initEditorWhenLoad = True

    """
    Para obtener el nombre del campo relacionado.

    @return Nombre del campo
    """

    def fieldRelation(self):
        return self.fieldRelation_


    """
    Para establecer el nombre del campo relacionado.

    @param fN Nombre del campo
    """

    def setFieldRelation(self, fN):
        self.fieldRelation_ = QString(fN)
        if self.showed:
            if self.topWidget:
                self.initCursor()
                self.initEditor()
            else:
                self.initFakeEditor()
        else:
            self._initCursorWhenLoad = True
            self._initEditorWhenLoad = True

    """
    Para establecer el alias del campo, mostrado en su etiqueta si showAlias es true

    @param alias Alias del campo, es el valor de la etiqueta. Si es vacio no hace nada.
    """

    def setFieldAlias(self, alias):
        if alias:
            self.fieldAlias_ = alias
            if self.showAlias_:
                self.textLabelDB.setText(self.fieldAlias_)

    """
    Establece el formato del texto

    @param f Formato del campo
    """

    def setTextFormat(self, f):
        self.textFormat_ = f
        ted = self.editor_
        if isinstance(ted, QtGui.QTextEdit):
            ted.setTextFormat(self.textFormat_)

    """
    @return El formato del texto
    """

    def textFormat(self):
        ted = self.editor_
        if isinstance(ted, QtGui.QTextEdit):
            return ted.textFormat()
        return self.textFormat_

    """
    Establece el modo de "echo"

    @param m Modo (Normal, NoEcho, Password)
    """

    def setEchoMode(self, m):
        led = self.editor_
        if isinstance(led,QtGui.QLineEdit):
            led.setEchoMode(m)


    """
  @return El mode de "echo" (Normal, NoEcho, Password)
    """

    def echoMode(self):
        led = self.editor_
        if isinstance(led, QtGui.QLineEdit):
            return led.echoMode()
        return QtGui.QLineEdit.Normal


























    """
    Filtro de eventos
    """
    @QtCore.pyqtSlot()
    @QtCore.pyqtSlot(int)
    def eventFilter(self,obj, event):
        QtGui.QWidget.eventFilter(self, obj, event)
        timerActive = False
        if event.type() == QtCore.QEvent.KeyPress:
            k = event

            if self.autoComFrame_ and self.autoComFrame_.isVisible():
                if k.key() == Qt.Key_Down and self.autoComPopup_:
                    self.autoComPopup_.setQuickFocus()
                    return True

                # --> WIN
                if self.editor_:
                    self.editor_.releaseKeyboard()
                if self.autoComPopup_:
                    self.autoComPopup_.releaseKeyboard()
                #<-- WIN

                self.autoComFrame_.hide()
                if self.editor_ and k.key() == Qt.Key_Backspace:
                    self.editor_.backspace()

                if not self.timerAutoComp_:
                    self.timerAutoComp_ = QtCore.QTimer(self)
                    self.timerAutoComp_.timeout.connect(self.toggledAutoCompletion)
                else:
                    self.timerAutoComp_.stop()

                if not k.key() == Qt.Key_Enter and not k.key() == Qt.Key_Return:
                    timerActive = True
                    self.timerAutoComp_.start(500)
                else:
                    timer = QtCore.QTimer(self)
                    timer.singleShot(0, self.autoCompletionUpdateValue)
                    return True

            if not timerActive and self.autoCompMode_ == "AlwaysAuto" and not (self.autoComFrame_ or self.autoComFrame_.isvisible()):
                if k.key() == Qt.Key_Backspace or k.key() == Qt.Key_Delete or ( k.key() >= Qt.Key_Space and k.key() == Qt.Key_ydiaeresis):
                    if not self.timerAutoComp_:
                        self.timerAutoComp_ = QtCore.QTimer(self)
                        self.timerAutoComp_.timeout.connect(self.toggledAutoCompletion)
                    else:
                        self.timerAutoComp_.stop()

                if not k.key() == Qt.Key_Enter and not k.key() == Qt.Key_Return:
                    timerActive = True
                    self.timerAutoComp_.start(500)
                else:
                    timer.singleShot(0, self.autoCompletionUpdateValue)
                    return True
            if isinstance(obj, FLLineEdit):
                if k.key() == Qt.Key_F4:
                    self.keyF4Pressed()
                    return True
            elif isinstance(obj,QtGui.QTextEdit):
                if k.key() == Qt.Key_F4:
                    self.keyF4Pressed()
                    return True
                return False

            if k.key() == Qt.Key_Enter or k.key() == Qt.Key_Return:
                self.focusNextPrevChild(True)
                self.keyReturnPressed.emit()
                return True

            if k.key() == Qt.Key_Up:
                self.focusNextPrevChild(False)
                return True

            if k.key() == Qt.Key_Down:
                self.focusNextPrevChild(True)
                return True

            if k.key() == Qt.Key_F2:
                self.keyF2Pressed_.emit()
                return True

            return False


        #elif isinstance(event, QtCore.QEvent.MouseButtonRelease) and isinstance(obj,self.textLabelDB) and event.button() == Qt.LeftButton:
        elif event.type() == QtCore.QEvent.MouseButtonRelease and isinstance(obj,type(self.textLabelDB)) and event.button() == Qt.LeftButton:
            self.emitLabelClicked()
        else:
            return False


    """
    Actualiza el valor del campo con una cadena de texto.

    @param t Cadena de texto para actualizar el campo
    """
    @QtCore.pyqtSlot('QString')
    def updateValue(self, data = None):
        if isinstance(data, QString): #Para quitar en el futuro
            data = str(data)
        isNull = False
        if data is None:
            if not self.cursor_:
                return
            ted = self.editor_
            if not isinstance(ted, FLLineEdit):
                return

            t = self.editor_.text()

            if not self.cursor_.bufferIsNull(self.fieldName_):
                if t == self.cursor_.valueBuffer(self.fieldName_):
                    return
            else:
                if not t:
                    return

            if not t:
                self.cursor_.setValueBuffer(self.fieldName_, None)
            else:
                self.cursor_.setValueBuffer(self.fieldName_, t)



        elif isinstance(data,QtCore.QDate):
            if not self.cursor_:
                return
            if not data:
                isNull = True
            if not self.cursor_.bufferIsNull(self.fieldName_):
                if data == self.cursor_.valueBuffer(self.fieldName_).toDate():
                    return
            elif isNull:
                return
            if isNull:
                self.cursor_.setValueBuffer(self.fieldName_, QtCore.QDate())
            else:
                self.cursor_.setValueBuffer(self.fieldName_, data)


        elif isinstance(data,QtCore.QTime):
            if not self.cursor_:
                return
            if not data:
                isNull = True
            if not self.cursor_.bufferIsNull(self.fieldName_):
                if data == self.cursor_.valueBuffer(self.fieldName_).toTime():
                    return
            elif isNull:
                return
            if isNull:
                self.cursor_.setValueBuffer(self.fieldName_, QtCore.QTime())
            else:
                self.cursor_.setValueBuffer(self.fieldName_, data)


        elif isinstance(data, bool):
            if not self.cursor_:
                return

            if not self.cursor_.bufferIsNull(self.fieldName_):
                if data == bool(self.cursor_.valueBuffer(self.fieldName_)):
                    return
            # self.cursor_.setValueBuffer(self.fieldName_, QtCore.QVariant(data, 0)) # ... esto porqué era un QVariant??
            self.cursor_.setValueBuffer(self.fieldName_, data)
        elif isinstance(data, str):
            if not self.cursor_:
                return

            tMD = self.cursor_.metadata()
            if not tMD:
                return
            field = tMD.field(self.fieldName_)
            if not field:
                return

            ol = field.hasOptionsList()
            tAux = data

            if ol and self.editor_:
                tAux = self._editor.currentItem()

            if not self.cursor_.bufferIsNull(self.fieldName_):
                if tAux == self.cursor_.valueBuffer(self.fieldName_):
                    return

            elif not tAux:
                return


            s = tAux
            if field.type() == "string" and not ol:
                if len(s) > 0 and s[0] == " ":
                    self.cursor_.bufferChanged.disconnect(self.refreshQuick)
                    self.cursor.setValueBuffer(self.fieldName_, s[1:])
                    self.cursor_.bufferChanged.connect(self.refreshQuick)
                    return

            if self.editor_ and (field.type() == "double" or field.type() == "int" or field.type() == "uint"):
                s = self.editor_.text()

            self.cursor_.setValueBuffer(self.fieldName_, s)

            if self.isVisible() and self.hasFocus() and field.type() == "string" and field.length() == len(s):
                self.focusNextPrevChild(True)









    """
    Establece el valor contenido en elcampo.

    @param v Valor a establecer
    """

    def setValue(self, v):

        # --> Para quitar con el tiempo
        if v and isinstance(v, str):
            if str(v[0:3]) == "RK@":
                v = self.cursor_.fetchLargeValue(v)
        # <--

        if not self.cursor_ or not v:
            return
        #if v:
        #    print("FLFieldDB(%s).setValue(%s) ---> %s" % (self.fieldName_, v, self.editor_))
        tMD = self.cursor_.metadata()
        if not tMD:
            return

        field = tMD.field(self.fieldName_)
        if not field:
            print("FLFieldDB::setValue(%s) : No existe el campo " % self.fieldName_)
            return

        type_ = field.type()
        #v = QVariant(cv)
        if field.hasOptionsList():
            idxItem = -1
            if type_ == "string":
                idxItem = field.optionsList().findIndex(v)
            if idxItem == -1:
                self.editor_.setCurrentItem(v)
            self.updateValue(self.editor_.currentText())
            return


        """
        fltype_ = None

        if type_ == "int" or type_ == "double" or type_ == "time" or type_ == "date" or type_ == "bytearray":
            fltype_ = type_
        elif type_ == "serial" or type_ == "uint":
            fltype_ = "uint"
        elif type_ == "bool" or type_ == "unlock":
            fltype_ = "bool"
        elif type_ == "string" or type_ == "pixmap" or type_ == "stringList":
            fltype_ = "string"



        #print("v.type()", v.type())
        if v.type() == "bool" and not fltype_ == "bool":
            if type_ == "double" or type_ == "int" or type_ == "uint":
                v = 0
            else:
                v.clear()

        if v.type() == "string" and v.toString().isEmpty():

            if type_ == "double" or type_ == "int" or type_ == "uint":

                v.clear()

        isNull = False
        if not v.isValid() or v.isNull():
            isNull = True

        if isNull == True and not field.allowNull():
            defVal = field.defaultValue()
            if defVal.isValid() and not defVal.isNull():
                v = defVal
                isNull = False

        #v.cast(fltype_) FIXME

        """
        if type_ == "uint" or type_ == "int" or type_ == "string":
            if self.editor_:
                doHome = False
                if not self.editor_.text():
                    doHome = True
                if v:
                    self.editor_.setText(v)
                else:
                    self.editor_.setText("")

                if doHome:
                    self.editor_.home(False)
            else:
                return
                #self.editor_.hide()


                return
        elif type_ == "stringList":
            if not self.editor_:
                return

            if not v:
                self.editor_.setText("")
            else:
                self.editor_.setText(v)



        elif type_ == "double":
            if self.editor_:
                #s = QString()
                #if not isNull:
                #    if not self.partDecimal_ == -1:
                #        s.setNum(v.toDouble(), 'f', self.partDecimal_ )
                #    else:
                #        s.setNum(v.toDouble(), 'f', field.partDecimal() )
                #self.editor_.setText(s)
                if v:
                    self.editor_.setText(str(v))
                #else:
                #    self.editor_.setText(0.00)


        elif type_ == "serial":
            if self.editor_:
                if not v:
                    self.editor_.setValue(0)
                else:
                    self.editor_.setValue(str(v))


        elif type_ == "pixmap":
            if self.editorImg_:

                if not v:
                    self.editorImg_.clear()
                    return
                pix = QtGui.QPixmap()
                #if not QtGui.QPixmapCache().find(cs.left(100), pix):
                pix.loadFromData(v)
                #    QtGui.QPixmapCache().insert(cs.left(100), pix)
                #print("PIX =", pix)
                if pix:
                    self.editorImg_.setPixmap(pix)
                else:
                    self.editorImg_.clear()

        elif type_ == "date":
            if self.editor_:
                if not v:
                    self.editor_.setDate(QtCore.QDate())
                else:
                    self.editor_.setDate(v)

        elif type_ == "time":
            if self.editor_:
                if not v:
                    self.editor_.setTime(QtCore.QTime())
                else:
                    self.editor_.setTime(v)

        elif type == "bool":
            if self.editor_ and v:
                self.editor_.setChecked(v)


    """
    Obtiene el valor contenido en el campo.
    """
    def value(self):
        if not self.cursor_:
            return None

        tMD = self.cursor_.metadata()
        if not tMD:
            return None

        field = tMD.field(self.fieldName_)
        if not field:
            print(FLUtil.tr("FLFieldDB::value() : No existe el campo ") + self.fieldName_)
            return None

        v = None

        if field.hasOptionsList():
            v = int(self.editor_.currentItem())
            return v

        type_ = field.type()
        #fltype = FLFieldMetaData.flDecodeType(type_)
        if self.cursor_.bufferIsNull(self.fieldName_):
            if type_ == "double" or type_ == "int" or type_ == "uint":
                return 0

        if type_ == "double" or type_ == "int" or type_ == "uint" or type_ == "string" or type_ == "stringlist":
            if self.editor_:
                ed_ = self.editor_
                if isinstance(ed_, FLLineEdit):
                    v = ed_.text()

        elif type_ == "serial":
            if self.editor_:
                ed_ = self.editor_
                if isinstance(ed_, FLSpinBox):
                    v = ed_.value()

        elif type_ == "pixmap":
            v = self.cursor_.valueBuffer(self.fieldName_)

        elif type_ == "date":
            if self.editor_:
                v = self.editor_.date().toString(Qt.ISODate)

        elif type_ == "time":
            if self.editor_:
                v = self.editor_.time().toString(Qt.ISODate)

        elif type_ == "bool":
            if self.editor_:
                v = self.editor_.isChecked()

        v.cast(fltype)
        return v

    """
    Marca como seleccionado el contenido del campo.
    """
    def selectAll(self):
        if not self.cursor_:
            return

        if not self.cursor_.metadata():
            return

        field = self.cursor_.metadata().field(self.fieldName_)
        if not field:
            return
        type_ = field.type()

        if type_ == "double" or type_ == "int" or type_ == "uint" or type_ == "string":
            if self.editor_:
                self.editor_.selectAll()

        elif type_ == "serial":
            if self.editor_:
                self.editor_.selectAll()



    """
    Devuelve el cursor de donde se obtienen los datos. Muy util
    para ser usado en el modo de tabla externa (fieldName y tableName
    definidos, foreingField y fieldRelation en blanco).
    """

    def cursor(self):
        return self.cursor_

    """
    Devuelve el valor de la propiedad showAlias. Esta propiedad es
    usada para saber si hay que mostrar el alias cuando se está
    en modo de cursor relacionado.
    """

    def showAlias(self):
        return self.showAlias_


    """
    Establece el estado de la propiedad showAlias.
    """

    def setShowAlias(self, value):
        if not self.showAlias_ == value:
            self.showAlias_ = value
            if self.showAlias_:
                self.textLabelDB.show()
            else:
                self.textLabelDB.hide()

    """
    Inserta como acelerador de teclado una combinación de teclas, devolviendo su identificador

    @param key Cadena de texto que representa la combinación de teclas (p.e. "Ctrl+Shift+O")
    @return El identificador asociado internamente a la combinación de teclas aceleración insertada
    """
    @decorators.NotImplementedWarn
    def insertAccel(self, key): #FIXME
        return None
        """
        if not self.accel_:
            self.accel_ = QtCore.QAccel(self.editor_)
            connect(accel_, SIGNAL(activated(int)), this, SLOT(emitActivatedAccel(int)));#FIXME

        id = self.accel_.findKey(QtCore.QKeySequence(key))

        if not id == -1:
            return
        id = self.accel_.insertItem(QtCore.QKeySequence(key))
        return id
        """

    """
    Elimina, desactiva, una combinación de teclas de aceleración según su identificador.

    @param identifier Identificador de la combinación de teclas de aceleración
    """
    @decorators.NotImplementedWarn
    def removeAccel(self, identifier): #FIXME
        if not self.accel_:
            return
        self.accel_.removeItem(identifier)


    """
    Establece la capacidad de mantener el componente deshabilitado ignorando posibles
    habilitaciones por refrescos. Ver FLFieldDB::keepDisabled_ .

    @param keep TRUE para activar el mantenerse deshabilitado y FALSE para desactivar
    """

    def setKeepDisabled(self, keep):
        self.keepDisabled_ = keep

    """
    Devuelve el valor de la propiedad showEditor.
    """

    def showEditor(self):
        return self.showEditor_


    """
    Establece el valor de la propiedad showEditor.
    """
    def setShowEditor(self, show):
        self.showEditor_ = show
        ed = QtGui.QWidget()
        if self.editor_:
            ed = self.editor_
        elif self.editorImg_:
            ed = self.editorImg_

        if ed:
            if show:
                ed.show()
            else:
                ed.hide()

    """
    Establece el número de decimales
    """
    def setPartDecimal(self, d):
        if self.editor_ and isinstance(self._editor.type , (float, QVariant.Double) ):
            self.partDecimal_ = d
            self.editor_.partDecimal = d
            self.refreshQuick(self.fieldName_)
            self.editor_.setText(self.editor_.text(),False)


    """
    Para asistente de completado automático.
    """
    def setAutoCompletionMode(self, m):
        self.autoCompMode_ = m


    def autoCompletionMode(self):
        return self.autoCompMode_

    """
    Refresca el contenido del campo con los valores del cursor de la tabla origen.

    Si se indica el nombre de un campo sólo "refresca" si el campo indicado
    coincide con la propiedad fieldRelation, tomando como filtro el valor del campo
    fieldRelation de la tabla relacionada. Si no se indica nigún nombre de
    campo el refresco es llevado a cabo siempre.

    @param fN Nombre de un campo
    """
    @QtCore.pyqtSlot()
    @QtCore.pyqtSlot('QString')
    def refresh(self, fN = None):
        if not self.cursor_ or not isinstance(self.cursor_, FLSqlCursor):
            #print("FLField.refresh() Cancelado")
            return
        tMD = self.cursor_.metadata()
        if not tMD:
            return

        v = None
        nulo = False
        if not fN:
            v = self.cursor_.valueBuffer(self.fieldName_)
            nulo = self.cursor_.bufferIsNull(self.fieldRelation_)
        else:
            if not self.cursorAux and fN.lower() == self.fieldRelation_.lower():
                if self.cursor_.bufferIsNull(self.fieldRelation_):
                    return

                field = tMD.field(self.fieldRelation_)
                tmd = FLSqlCursor(field.relationM1().foreignTable()).metadata()
                if not tmd:
                    return

                if self.topWidget_ and not self.topWidget_.isShown() and not self.cursor_.modeAccess() == FLSqlCursor.Insert:
                    if tmd and not tmd.inCache():
                        del tmd
                    return

                if not field:
                    if tmd and not tmd.inCache():
                        del tmd


                if not field.relationM1():
                    print( "FLFieldDB :El campo de la relación debe estar relacionado en M1")
                    if tmd and not tmd.inCache():
                        del tmd
                    return


                v = self.cursor_.valueBuffer(self.fieldRelation_)
                q = FLSqlQuery()
                q.setForwardOnly(True)
                q.setTablesList(field.relationM1().foreignTable())
                q.setSelect("%s,%s" % (self.foreignField, field.relationM1().foreignField()))
                q.setFrom(field.relationM1().foreignTable())

                where = field.formatAssignValue(field.relationM1().foreignField(), v, True)
                filterAc = QString(self.cursor_.filterAssoc(self.fieldRelation_, tmd))

                if not filterAc.isEmpty():
                    if where.isEmpty():
                        where = filterAc
                    else:
                        where += QString(" AND " + filterAc)

                if self.filter_.isEmpty():
                    q.setWhere(where)
                else:
                    q.setWhere(QString(self.filter_ + " AND " + where))

                if q.exec_() and q.next():
                    v0 = QVariant(q.value(0))
                    v1 = QVariant(q.value(1))
                    if not v0 == self.value():
                        self.setValue(v0)
                    if not v1 == v:
                        self.cursor_.setValueBuffer(self.fieldRelation_, v1)

                if tmd and not tmd.inCache():
                    del tmd
            return

        field = tMD.field(str(self.fieldName_))
        if not field:
            return
        type_ = field.type()
        if not type_ == "pixmap" and not self.editor_:
            return

        modeAcces = self.cursor_.modeAccess()
        partDecimal = -1
        if not self.partDecimal_ == -1:
            partDecimal = self.partDecimal_
        else:
            partDecimal = field.partDecimal()

        ol = field.hasOptionsList()

        fDis = False

        if isinstance(v , QString): #Para quitar
            v = str(v)

        if self.keepDisabled_ or self.cursor_.fieldDisabled(self.fieldName_) or ( modeAcces == FLSqlCursor.Edit and ( field.isPrimaryKey() or tMD.fieldListOfCompoundKey(self.fieldName_))) or not field.editable() or modeAcces == FLSqlCursor.Browse:
            fDis = True

        self.setDisabled(fDis)

        if type_ == "double":
            try:
                self.editor_.textChanged.disconnect(self.updateValue)
            except:
                pass
            s = None
            if v:
                s = round(float(v), partDecimal)
                if not nulo:
                    self.editor_.setText(str(s))
                else:
                    self.editor_.setText(str(s))
            else:
                self.editor_.setText("0.00")

            self.editor_.textChanged.connect(self.updateValue)


        elif type_ == "string":
            doHome = False
            try:
                self.editor_.textChanged.disconnect(self.updateValue)
            except:
                pass

            if v:
                if ol:
                    self.editor_.setCurrentIndex(field.getIndexOptionsList(v))
                else:
                    if v:
                        self.editor_.setText(v)
            else:
                if ol:
                    self.editor_.setCurrentIndex(0)
                else:
                    self.editor_.setText("")

            if not ol and doHome:
                self.editor_.home(False)

            self.editor_.textChanged.connect(self.updateValue)



        elif type_ == "uint":
            try:
                self.editor_.textChanged.disconnect(self.updateValue)
            except:
                pass
            #s = None
            if not nulo:
                if v:
                    self.editor_.setText(str(s))
                else:
                    self.editor_.setText("0")
            self.editor_.textChanged.connect(self.updateValue)

        elif type_ == "int":
            try:
                self.editor_.textChanged.disconnect(self.updateValue)
            except:
                pass
            #s = None
            if not nulo:
                if v:
                    self.editor_.setText(str(s))
                else:
                    self.editor_.setText("0")
            self.editor_.textChanged.connect(self.updateValue)

        elif type_ == "serial":
            try:
                self.editor_.textChanged.disconnect(self.updateValue)
            except:
                pass
            self.editor_.setText(str(0))

            self.editor_.textChanged.connect(self.updateValue)


        elif type_ == "pixmap":
            if not self.editorImgInit_:
                self.editorImg_ = FLPixmapView(self)
                self.editorImg_.setFocusPolicy(Qt.NoFocus)
                self.editorImg_.setSizePolicy(self.sizePolicy())
                self.editorImg_.setMaximumSize(self.maximumSize())
                self.editorImg_.setMinimumSize(self.minimumSize())
                self.editorImg_.setAutoScaled(True)
                #self.FLWidgetFieldDBLayout.removeWidget(self.pushButtonDB)
                self.FLWidgetFieldDBLayout.addWidget(self.editorImg_)
                self.pushButtonDB.hide()
                self.editorImgInit_ = True

                if field.visible():
                    self.editorImg_.show()
            else:
                return
                #else:
            #if modeAcces == FLSqlCursor.Browse:
            if field.visible():
                #cs = QString()
                if not v:
                    self.editorImg_.clear()
                    return
                    #cs = v.toString()
                #if cs.isEmpty():
                #    self.editorImg_.clear()
                #    return
                pix = QtGui.QPixmap()
                #if not QtGui.QPixmapCache.find(cs.left(100), pix):
                pix.loadFromData(v)
                    #QtGui.QPixmapCache.insert(cs.left(100), pix)

                if pix:
                    self.editorImg_.setPixmap(pix)
                else:
                    self.editorImg_.clear()

            #if modeAcces == FLSqlCursor.Browse:
                #self.pushButtonDB.setVisible(False)

        elif type_ == "date":
            if self.cursor_.modeAccess() == FLSqlCursor.Insert and nulo and not field.allowNull():
                defVal = field.defaultValue()
                if not defVal.isValid() or defVal.isNull():
                    self.editor_.setDate(QtCore.QDate.currentDate())
                else:
                    self.editor_.setDate(defVal.toDate())
            else:
                try:
                    self.editor_.valueChanged.disconnect(self.updateValue)
                except:
                    pass
                self.editor_.valueChanged.connect(self.updateValue)



        elif type_ == "time":
            if self.cursor_.modeAccess() == FLSqlCursor.Insert and nulo and not field.allowNull():
                defVal = field.defaultValue()
                if not defVal.isValid() or defVal.isNull():
                    self.editor_.setDate(QtCore.QTime.currentTime())
                else:
                    self.editor_.setDate(defVal.toTime())
            else:
                try:
                    self.editor_.valueChanged.disconnect(self.updateValue)
                except:
                    pass
                self.editor_.valueChanged.connect(self.updateValue)



        elif type_ == "stringlist":
            try:
                self.editor_.textChanged.disconnect(self.updateValue)
            except:
                pass
            if v:
                self.editor_.setText(v)
            self.editor_.textChanged.connect(self.updateValue)


        elif type_ == "bool":
            try:
                self.editor_.toggled.disconnect(self.updateValue)
            except:
                pass

            if v:
                v = bool(v)

                self.editor_.setChecked(v)

            self.editor_.toggled.connect(self.updateValue)

        if not field.visible():
            if self.editor_:
                self.editor_.hide()
            elif self.editorImg_:
                self.editorImg_.hide()
            self.setDisabled(True)



    """
    Refresco rápido
    """

    @decorators.NotImplementedWarn
    @QtCore.pyqtSlot('QString')
    def refreshQuick(self, fN = None):
        return


    """
    Inicia el cursor segun este campo sea de la tabla origen o de
    una tabla relacionada
    """
    def initCursor(self):

        if not self.tableName_.isEmpty() and self.foreignField_.isEmpty() and self.fieldRelation_.isEmpty():
            self.cursorBackup_ = self.cursor_
            if self.cursor_:
                self.cursor_ = FLSqlCursor(self.tableName_)
                #FIXME: self.cursor_ = FLSqlCursor(self.tableName_, True, self.cursor_.db().connectionName(), 0, 0, self)
            else:
                if not self.topWidget_:
                    return
                self.cursor_ = FLSqlCursor(self.tableName_)
                #FIXME: self.cursor_ = FLSqlCursor(self.tableName_, True, FLSqlConnections.database().connectionName(), 0, 0, self)
            self.cursor_.setModeAccess(FLSqlCursor.Browse)
            if self.showed:
                try:
                    self.cursor_.cursorUpdated.disconnect(self.refresh)
                except:
                    pass
            self.cursor_.cursorUpdated.connect(self.refresh)
            return
        else:
            if self.cursorBackup_:
                try:
                    self.cursor_.cursorUpdated.disconnect(self.refresh)
                except:
                    pass
                self.cursor_ = self.cursorBackup_
                self.cursorBackup_ = False

        if not self.cursor_:
            return


        if self.tableName_.isEmpty() and self.foreignField_.isEmpty() and self.fieldRelation_.isEmpty():
            if not self.foreignField_.isEmpty() and not self.fieldRelation_.isEmpty():
                if self.showed:
                    try:
                        self.cursor_.bufferChanged.disconnect(self.refresh)
                    except:
                        pass
                self.cursor_.bufferChanged.connect(self.refresh)

            if self.showed:
                try:
                    self.cursor_.newBuffer.disconnect(self.refresh)
                except:
                    pass

                try:
                    self.cursor_.bufferChanged.disconnect(self.refreshQuick)
                except:
                    pass

            self.cursor_.newBuffer.connect(self.refresh)
            self.cursor_.bufferChanged.connect(self.refreshQuick)
            return

        if not self.cursorAux:
            #print("No tengo cursor Auxiliar", self.tableName_)
            if not self.cursorAuxInit is None:
                #print("Inicializando cursorauxiliar", self.tableName_)
                return


            tMD = self.cursor_.db().manager().metadata(self.tableName_)

            if not tMD:
                return

            try:
                self.cursor_.newBuffer.disconnect(self.refresh)
            except:
                pass

            try:
                self.cursor_.bufferChanged.disconnect(self.refreshQuick)
            except:
                pass


            self.cursorAux = self.cursor_
            curName = self.cursor_.metadata().name()

            rMD = tMD.relation(self.fieldRelation_, self.foreignField_, curName)
            if not rMD:
                checkIntegrity = False
                testM1 = self.cursor_.metadata().relation(self.foreignField_, self.fieldRelation_, self.tableName_)
                if testM1:
                    if testM1.cardinality() == FLRelationMetaData.RELATION_1M:
                        checkIntegrity = True
                fMD = tMD.field(self.fieldRelation_)
                #print("EOOOOOO", fMD)

                if fMD:
                    rMD = FLRelationMetaData(curName, self.foreignField_, FLRelationMetaData.RELATION_1M, False,False, checkIntegrity)

                    fMD.addRelationMD(rMD)
                    #print("FLFieldDB : La relación entre la tabla del formulario ( %s ) y la tabla ( %s ) de este campo ( %s ) no existe, pero sin embargo se han indicado los campos de relación( %s, %s)" % (curName, self.tableName_, self.fieldName_, self.fieldRelation_, self.foreignField_))
                    #print("FLFieldDB : Creando automáticamente %s.%s --1M--> %s.%s" % (self.tableName_, self.fieldRelation_, curName, self.foreignField_))
                else:
                    #print("FLFieldDB : El campo ( %s ) indicado en la propiedad fieldRelation no se encuentra en la tabla ( %s )" % (self.fieldRelation_, self.tableName_))
                    pass

            if not self.tableName_.isEmpty():
                #self.cursor_ = FLSqlCursor(self.tableName_)
                self.cursor_ = FLSqlCursor(self.tableName_, False, self.cursor_.connectionName(), self.cursorAux, rMD, self)

            if not self.cursor_:
                self.cursor_ = self.cursorAux
                if self.showed:
                    try:
                        self.cursor_.newBuffer.disconnect(self.refresh)
                    except:
                        pass

                    try:
                        self.cursor_.bufferChanged.disconnect(self.refreshQuick)
                    except:
                        pass

                self.cursor_.newBuffer.connect(self.refresh)
                self.cursor_.bufferChanged.connect(self.refreshQuick)
                self.cursorAux = False
                if tMD and not tMD.inCache():
                    del tMD
                return
            else:
                if self.showed:
                    try:
                        self.cursor_.newBuffer.disconnect(self.setNoShowed)
                    except:
                        pass
                self.cursor_.newBuffer.connect(self.setNoShowed)

            self.cursor_.setModeAccess(FLSqlCursor.Browse)
            if self.showed:
                try:
                    self.cursor_.newBuffer.disconnect(self.refresh)
                except:
                    pass

                try:
                    self.cursor_.bufferChanged.disconnect(self.refreshQuick)
                except:
                    pass

            self.cursor_.newBuffer.connect(self.refresh)
            self.cursor_.bufferChanged.connect(self.refreshQuick)

            self.cursorAuxInit = True
            #self.cursor_.append(self.cursor_.db().db().recordInfo(self.tableName_).find(self.fieldName_)) #FIXME
            #self.cursor_.append(self.cursor_.db().db().recordInfo(self.tableName_).find(self.fieldRelation_)) #FIXME
            if tMD and not tMD.inCache():
                del tMD



    """
    Crea e inicia el editor apropiado para editar el tipo de datos
    contenido en el campo (p.e: si el campo contiene una fecha crea
    e inicia un QDataEdit)
    """
    def initEditor(self):

        if not self.cursor_:
            return



        #print("FlFieldDB(%s.%s).initEditor()" % (self.tableName_, self.fieldName_))
        if self.editor_:
            del self.editor_
            self.editor_ = None

        if self.editorImg_:
            del self.editorImg_
            self.editorImg_ = None

        tMD = self.cursor_.metadata()
        if not tMD:
            return

        field = tMD.field(self.fieldName_)
        if not field:
            return

        type_ = field.type()
        len = field.length()
        partInteger = field.partInteger()
        partDecimal = None
        if self.partDecimal_ > -1:
            partDecimal = self.partDecimal_
        else:
            partDecimal = field.partDecimal()

        #rX = field.regExpValidator()
        ol = field.hasOptionsList()

        rt = QString()
        if field.relationM1():
            if not field.relationM1().foreignTable() == tMD.name():
                rt = field.relationM1().foreignTable()

        hasPushButtonDB = False
        self.fieldAlias_ = field.alias()

        self.textLabelDB.setFont(QtGui.QApplication.font())
        if self.showAlias_ and not type == "pixmap" and not type == "bool":
            if not field.allowNull() and field.editable():
                self.textLabelDB.setText(self.fieldAlias_ + QString("*"))
            else:
                self.textLabelDB.setText(self.fieldAlias_)
        else:
            self.textLabelDB.hide()

        if rt:
            hasPushButtonDB = True
            tmd = self.cursor_.db().manager().metadata(rt)
            if not tmd:
                self.pushButtonDB.setDisabled(True)

            if tmd and not tmd.inCache():
                del tmd

        self.initMaxSize_ = self.maximumSize()
        self.initMinSize_ = self.minimumSize()

        if type_ == "unit" or type_ == "int" or type_ == "double" or type_ == "string":
            if ol:
                self.editor_ = QtGui.QComboBox()
                self.editor_.name = "editor"
                self.editor_.setEditable(False)
                self.editor_.setAutoCompletion(True)
                self.editor_.setMinimumSize(32, 32)
                self.editor_.setFont(QtGui.qApp.font())
                if not self.cursor_.modeAccess() == FLSqlCursor.Browse:
                    if not field.allowNull():
                        self.editor_.palette().setColor(QtGui.QPalette.Base, self.notNullColor())

                olTranslated = []
                olNoTranslated = field.optionsList()
                for olN in olNoTranslated:
                    olTranslated.append(olN)
                self.editor_.addItems(olTranslated)

                self.editor_.installEventFilter(self)
                if self.showed:
                    try:
                        self.editor_.activated.disconnect(self.updateValue)
                    except:
                        pass
                self.editor_.activated.connect(self.updateValue)

            else:
                self.editor_ = FLLineEdit(self, "editor")
                self.editor_.setFont(QtGui.qApp.font())
                self.editor_.setMinimumSize(32, 32)
                self.editor_._tipo = type_
                self.editor_.partDecimal = partDecimal
                if not self.cursor_.modeAccess() == FLSqlCursor.Browse:
                    if not field.allowNull():
                        self.editor_.palette().setColor(QtGui.QPalette.Base, self.notNullColor())
                    self.editor_.installEventFilter(self)

                if type_ == "double":
                    #self.editor_.setValidator(FLDoubleValidator(None, pow(10, partInteger) -1 , self.editor_)) FIXME
                    self.editor_.setAlignment(Qt.AlignRight)
                else:
                    if type_ == "uint" or type_ == "int":
                        if type_ == "uint":
                            self.editor_.setValidator(FLUIntValidator(None, pow(10, partInteger) -1 , self.editor_))
                        else:
                            self.editor_.setValidator(FLIntValidator(((pow(10, partInteger) - 1) * (-1)) , pow(10, partInteger) - 1, self.editor_))
                        self.editor_.setAlignment(Qt.AlignRight)
                    else:
                        #self.editor_.setMaxLength(len) FIXME
                        #if not rX.isEmpty():
                            #r = rX
                            #self.editor_.setValidator(QtGui.QRegExpValidator(r, self.editor_))

                        self.editor_.setAlignment(Qt.AlignLeft)

                        self.keyF4Pressed.connect(self.toggleAutoCompletion)
                        if self.autoCompMode_ == "OnDemandF4":
                            self.editor_.setToolTip("Para completado automático pulsar F4")
                            self.editor_.setWhatsThis("Para completado automático pulsar F4")
                        elif self.autoCompMode_ == "AlwaysAuto":
                            self.editor_.setToolTip("Completado automático permanente activado")
                            self.editor_.setWhatsThis("Completado automático permanente activado")
                        else:
                            self.editor_.setToolTip("Completado automático desactivado")
                            self.editor_.setWhatsThis("Completado automático desactivado")

                if self.showed:
                    try:
                        self.editor_.lostFocus.disconnect(self.emitLostFocus)
                        self.editor_.textChanged.disconnect(self.updateValue)
                        self.editor_.textChanged.disconnect(self.emitTextChanged)
                    except:
                        a = 1

                self.editor_.lostFocus.connect(self.emitLostFocus)
                self.editor_.textChanged.connect(self.updateValue)
                self.editor_.textChanged.connect(self.emitTextChanged)

                if hasPushButtonDB:
                    if self.showed:
                        try:
                            self.KeyF2Pressed_.disconnect(self.pushButtonDB.animateClick())
                            self.labelClicked.disconnect(self.openFormRecordRelation)
                        except:
                            a = 1

                    self.keyF2Pressed_.connect(self.pushButtonDB.animateClick) #FIXME
                    self.labelClicked.connect(self.openFormRecordRelation)
                    self.textLabelDB.installEventFilter(self)
                    tlf = self.textLabelDB.font()
                    tlf.setUnderline(True)
                    self.textLabelDB.setFont(tlf)
                    cB = QtGui.QColor(Qt.cyan)
                    self.textLabelDB.palette().setColor(QtGui.QPalette.Base, cB)
                    self.textLabelDB.setCursor(Qt.PointingHandCursor)

            sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7) ,QtGui.QSizePolicy.Policy(0))
            sizePolicy.setHeightForWidth(True)
            self.editor_.setSizePolicy(sizePolicy)
            self.FLWidgetFieldDBLayout.addWidget(self.editor_)

        elif type_ == "serial":
            self.editor_ = FLLineEdit(self, "editor")
            self.editor_.setFont(QtGui.qApp.font())
            self.editor_.setMaxValue(pow(10, field.partInteger()) -1)
            sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7) ,QtGui.QSizePolicy.Policy(0))
            sizePolicy.setHeightForWidth(True)
            self.editor_.setSizePolicy(sizePolicy)
            self.FLWidgetFieldDBLayout.addWidget(self.editor_)
            self.editor_.installEventFilter(self)
            self.editor_.setDisabled(True)
            self.editor_.setAlignment(QtCore.Qt.AlignRight)
            self.pushButtonDB.hide()

            if self.showed:
                try:
                    self.editor_.textChanged.disconnect(self.updateValue)
                except:
                    pass
            self.editor_.textChanged.connect(self.updateValue)


        elif type_ == "pixmap":
            if not self.cursor_.modeAccess() == FLSqlCursor.Browse:
                if not self.editorImgInit_:
                    self.editorImgInit_ = True
                    self.FLWidgetFieldDBLayout.setDirection(QtGui.QBoxLayout.Down)
                    self.editorImg_ = FLPixmapView(self)
                    self.editorImg_.setFocusPolicy(Qt.NoFocus)
                    self.editorImg_.setSizePolicy(self.sizePolicy())
                    self.editorImg_.setMaximumSize(self.maximumSize())
                    self.editorImg_.setMinimumSize(self.minimumSize())
                    self.editorImg_.setAutoScaled(True)
                    self.FLWidgetFieldDBLayout.removeWidget(self.pushButtonDB)
                    self.FLWidgetFieldDBLayout.addWidget(self.editorImg_)
                self.textLabelDB.hide()

                sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed ,QtGui.QSizePolicy.Fixed)
                sizePolicy.setHeightForWidth(True)

                if not self.pbAux3_:
                    spcBut = QtGui.QSpacerItem(20,20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
                    self.lytButtons.addItem(spcBut)
                    self.pbAux3_ = QtGui.QPushButton(self)
                    self.pbAux3_.setSizePolicy(sizePolicy)
                    self.pbAux3_.setMinimumSize(22, 22)
                    self.pbAux3_.setFocusPolicy(Qt.NoFocus)
                    self.pbAux3_.setIcon(QtGui.QIcon(filedir("icons","gtk-open.png")))
                    self.pbAux3_.setText("")
                    self.pbAux3_.setToolTip("Abrir fichero de imagen")
                    self.pbAux3_.setWhatsThis("Abrir fichero de imagen")
                    self.lytButtons.addWidget(self.pbAux3_)
                    if self.showed:
                        self.pbAux3_.clicked.disconnect(self.searchPixmap)
                    self.pbAux3_.clicked.connect(self.searchPixmap)
                    if not hasPushButtonDB:
                        if self.showed:
                            self.KeyF2Pressed_.disconnect(self.pbAux3_.animateClick)
                        #self.KeyF2Pressed_.connect(self.pbAux3_.animateClick)
                        self.pbAux3_.setFocusPolicy(Qt.StrongFocus)
                        self.pbAux3_.installEventFilter(self)

                if not self.pbAux4_:
                    self.pbAux4_ = QtGui.QPushButton(self)
                    self.pbAux4_.setSizePolicy(sizePolicy)
                    self.pbAux4_.setMinimumSize(22, 22)
                    self.pbAux4_.setFocusPolicy(Qt.NoFocus)
                    self.pbAux4_.setIcon(QtGui.QIcon(filedir("icons","gtk-paste.png")))
                    self.pbAux4_.setText("")
                    self.pbAux4_.setToolTip("Pegar imagen desde el portapapeles")
                    self.pbAux4_.setWhatsThis("Pegar imagen desde el portapapeles")
                    self.lytButtons.addWidget(self.pbAux4_)
                    if self.showed:
                        self.pbAux4_.clicked.disconnect(self.clearPixmap)
                    self.pbAux4_.clicked.connect(self.clearPixmap)



                if not self.pbAux_:
                    self.pbAux_ = QtGui.QPushButton(self)
                    self.pbAux_.setSizePolicy(sizePolicy)
                    self.pbAux_.setMinimumSize(22, 22)
                    self.pbAux_.setFocusPolicy(Qt.NoFocus)
                    self.pbAux_.setIcon(QtGui.QIcon(filedir("icons","gtk-clear.png")))
                    self.pbAux_.setText("")
                    self.pbAux_.setToolTip("Borrar imagen")
                    self.pbAux_.setWhatsThis("Borrar imagen")
                    self.lytButtons.addWidget(self.pbAux_)
                    if self.showed:
                        self.pbAux_.clicked.disconnect(self.clearPixmap)
                    self.pbAux_.clicked.connect(self.clearPixmap)


                if not self.pbAux2_:
                    self.pbAux2_ = QtGui.QPushButton(self)
                    savepixmap = QtGui.QMenu(self.pbAux2_)
                    #FIXME a  mejorar
                    fmt = QtGui.QPictureIO.outputFormats()
                    id = 0
                    for format in fmt:
                        savepixmap.insertItem(format , id)
                        id = id + 1

                    self.pbAux2_.setMenu(savepixmap)
                    self.pbAux2_.setSizePolicy(sizePolicy)
                    self.pbAux2_.setMinimumSize(22, 22)
                    self.pbAux2_.setFocusPolicy(Qt.NoFocus)
                    self.pbAux2_.setIcon(QtGui.QIcon(filedir("icons","gtk-save.png")))
                    self.pbAux2_.setText("")
                    self.pbAux2_.setToolTip("Guardar imagen como...")
                    self.pbAux2_.setWhatsThis("Guardar imagen como...")
                    self.lytButtons.addWidget(self.pbAux2_)
                    if self.showed:
                        savepixmap.activated.disconnect(self.savePixmap)
                    savepixmap.activated.connect(self.savePixmap)

                    if hasPushButtonDB:
                        self.pushButtonDB.installEventFilter(self)
                    else: # lo desactivo si no tiene el control
                        self.pushButtonDB.setDisabled(True)

        elif type_ == "date":
            self.editor_ = FLDateEdit(self, "editor")
            self.editor_.setFont(QtGui.qApp.font())
            sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7) ,QtGui.QSizePolicy.Policy(0))
            sizePolicy.setHeightForWidth(True)
            self.editor_.setSizePolicy(sizePolicy)
            self.FLWidgetFieldDBLayout.insertWidget(1, self.editor_)

            #self.editor_.setOrder(QtGui.QDateEdit.DMY)
            #self.editor_.setAutoAdvance(True)
            #self.editor_.setSeparator("-")
            self.editor_.installEventFilter(self)
            self.pushButtonDB.hide()

            if not self.cursor_.modeAccess() == FLSqlCursor.Browse:
                if not self.pbAux_:
                    self.pbAux_ = QtGui.QPushButton(self)
                    self.pbAux_.setFlat(True)
                    sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7) ,QtGui.QSizePolicy.Policy(0))
                    sizePolicy.setHeightForWidth(True)
                    self.pbAux_.setSizePolicy(sizePolicy)
                    self.pbAux_.setMinimumSize(25, 25)
                    self.pbAux_.setMaximumSize(25, 25)
                    self.pbAux_.setFocusPolicy(Qt.NoFocus)
                    self.pbAux_.setIcon(QtGui.QIcon(filedir("icons","date.png")))
                    self.pbAux_.setText("")
                    self.pbAux_.setToolTip("Seleccionar fecha (F2)")
                    self.pbAux_.setWhatsThis("Seleccionar fecha (F2)")
                    #self.lytButtons.addWidget(self.pbAux_) FIXME
                    self.FLWidgetFieldDBLayout.addWidget(self.pbAux_)
                    if self.showed:
                        self.pbAux_.clicked.disconnect(self.toggleDatePicker)
                        self.KeyF2Pressed_.disconnect(self.pbAux_.animateClick)

                    self.pbAux_.clicked.connect(self.toggleDatePicker)
                    #self.keyF2Pressed_.connect(self.pbAux_.animateClick) #FIXME

            if self.showed:
                try:
                    self.editor_.valueChanged.disconnect(self.updateValue)
                except:
                    pass

            self.editor_.valueChanged.connect(self.updateValue) #FIXME
            if self.cursor_.modeAccess() == FLSqlCursor.Insert and not field.allowNull():
                defVal = field.defaultValue()
                if not defVal.isValid() or defVal.isNull():
                    self.editor_.setDate(QtCore.QDate.CurrentDate())
                else:
                    self.editor_.setDate(defVal.toDate())

        elif type_ == "time":
            self.editor_ = QtGui.QTimeEdit(self)
            self.editor_.setFont(QtGui.qApp.font())
            #self.editor_.setAutoAdvance(True)
            sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7) ,QtGui.QSizePolicy.Policy(0))
            sizePolicy.setHeightForWidth(True)
            self.editor_.setSizePolicy(sizePolicy)
            self.FLWidgetFieldDBLayout.addWidget(self.editor_)
            self.editor_.installEventFilter(self)
            self.pushButtonDB.hide()
            if self.showed:
                try:
                    self.editor_.valueChanged.disconnect(self.updateValue)
                except:
                    pass

            #self.editor_.valueChanged.connect(self.updateValue) #FIXME
            if self.cursor_.modeAccess() == FLSqlCursor.Insert and not field.allowNull():
                defVal = field.defaultValue()
                if not defVal.isValid() or defVal.isNull():
                    self.editor_.setDate(QtCore.QDate.CurrentTime())
                else:
                    self.editor_.setDate(defVal.toTime())


        elif type_ == "stringlist":

            self.editor_ = QtGui.QTextEdit(self)
            self.editor_.setFont(QtGui.qApp.font())
            self.editor_.setTabChangesFocus(True)
            sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7) ,QtGui.QSizePolicy.Policy(0))
            sizePolicy.setHeightForWidth(True)
            self.editor_.setSizePolicy(sizePolicy)
            #ted.setTexFormat(self.textFormat_)

            #if isinstance(self.textFormat_, Qt.RichText) and not self.cursor_.modeAccess() == FLSqlCursor.Browse:
                #self.FLWidgetFieldDBLayout.setDirection(QtGui.QBoxLayout.Down)
                #self.FLWidgetFieldDBLayout.remove(self.textLabelDB)
                #textEditTab_ = AQTextEditBar(self, "extEditTab_", self.textLabelDB) #FIXME
                #textEditTab_.doConnections(ted)
                #self.FLWidgetFieldDBLayout.addWidget(textEditTab_)

            self.FLWidgetFieldDBLayout.addWidget(self.editor_)
            self.editor_.installEventFilter(self)

            if self.showed:
                try:
                    self.editor_.textChanged.disconnect(self.updateValue)
                except:
                    pass

            self.editor_.textChanged.connect(self.updateValue)

            self.keyF4Pressed.connect(self.toggleAutoCompletion)
            if self.autoCompMode_ == "OnDemandF4":
                self.editor_.setToolTip( "Para completado automático pulsar F4")
                self.editor_.setWhatsThis("Para completado automático pulsar F4")
            elif self.autoCompMode_ == "AlwaysAuto":
                self.editor_.setToolTip("Completado automático permanente activado")
                self.editor_.setWhatsThis("Completado automático permanente activado")
            else:
                self.editor_.setToolTip("Completado automático desactivado")
                self.editor_.setWhatsThis("Completado automático desactivado")

        elif type_ == "bool":
            self.editor_ = QtGui.QCheckBox(self)
            #self.editor_.setName("editor")
            self.editor_.setText(tMD.fieldNameToAlias(self.fieldName_))
            self.editor_.setFont(QtGui.qApp.font())
            self.editor_.installEventFilter(self)

            self.editor_.setMinimumWidth(self.fontMetrics().width(tMD.fieldNameToAlias(self.fieldName())) + self.fontMetrics().maxWidth() * 2)
            sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7) ,QtGui.QSizePolicy.Policy(0))
            sizePolicy.setHeightForWidth(True)
            self.editor_.setSizePolicy(sizePolicy)
            self.FLWidgetFieldDBLayout.addWidget(self.editor_)

            if self.showed:
                try:
                    self.editor_.toggled.disconnect(self.updateValue)
                except:
                    pass
            self.editor_.toggled.connect(self.updateValue)

        if self.editor_:
            self.editor_.setFocusPolicy(Qt.StrongFocus)
            self.setFocusProxy(self.editor_)
            self.setTabOrder(self.pushButtonDB, self.editor_)
            if hasPushButtonDB:
                self.pushButtonDB.setFocusPolicy(Qt.NoFocus)
                self.editor_.setToolTip("Para buscar un valor en la tabla relacionada pulsar F2")
                self.editor_.setWhatsThis("Para buscar un valor en la tabla relacionada pulsar F2")

        elif self.editorImg_:
            self.editorImg_.setFocusPolicy(Qt.NoFocus)
            if hasPushButtonDB:
                self.pushButtonDB.setFocusPolicy(Qt.StrongFocus)

        if not hasPushButtonDB:
            self.pushButtonDB.hide()

        if self.initMaxSize_.width() < 80:
            self.setShowEditor(False)
        else:
            self.setShowEditor(self.showEditor_)































    """
    Muestra/Oculta el seleccionador de fechas.
    """
    @decorators.NotImplementedWarn
    def toggleDatePicker(self):
        return



    """
    Borra imagen en campos tipo Pixmap.
    """
    def clearPixmap(self):
        if not self.editorImg_:
            self.editorImg_.clear()
            self.cursor_.setValueBuffer(self.fieldName_, QVariant())


    """
    Guarda imagen en campos tipo Pixmap.

    @param fmt Indica el formato con el que guardar la imagen
    """
    def savePixmap(self, f):
        if self.editorImg_:
            fmt = QtGui.QImage.outputFormats()
            fmt = fmt.at(f)
            ext = QString(fmt).lower()
            filename = "imagen.%s" % ext
            ext = "*.%s" % ext
            savefilename = QtGui.QFileDialog.getSaveFileName( filename.lower(), ext , self.filename_, FLUtil.tr("Guardar imagen como"))
            if not savefilename.isEmpty():
                pix = QtGui.QPixmap()
                QtGui.QApplication.setOverrideCursor(Qt.WaitCursor)
                pix.loadFromDate(self.value().toCString())
                if not pix.isNull():
                    if not pix.save(savefilename, fmt):
                        QtGui.QMessageBox.warning(self, FLUtil.tr("Error"), FLUtil.tr("Error guardando fichero"))

            QtGui.QApplication.restoreOverrideCursor()


    """
    Muestra/Oculta el asistente de completado automático.
    """
    @QtCore.pyqtSlot()
    def toggleAutoCompletion(self):
        print("FIXMEEEE: toggleAutoCompletion")
        return



    """
    Actualiza el valor del campo a partir del contenido que
    ofrece el asistente de completado automático.
    """
    @decorators.NotImplementedWarn
    def autoCompletionUpdateValue(self):
        return

    """
    Abre un formulario de edición para el valor seleccionado en su acción correspondiente
    """
    @QtCore.pyqtSlot()
    def openFormRecordRelation(self):
        if not self.cursor_:
            return

        if self.fieldName_.isEmpty():
            return

        tMD = self.cursor_.metadata()
        if not tMD:
            return

        field = tMD.field(self.fieldName_)
        if not field:
            return

        if not field.relationM1():
            print("FLFieldDB : El campo de búsqueda debe tener una relación M1")
            return

        fMD = field.associatedField()
        a = None

        v = self.cursor_.valueBuffer(field.name())
        if not v or ( fMD and self.cursor_.bufferIsNull(fMD.name())):
            QtGui.QMessageBox.warning(QtGui.qApp.focusWidget(), "Aviso", "Debe indicar un valor para %s" % field.alias(), QtGui.QMessageBox.Ok, 0, 0)
            return

        mng = FLManager(self.cursor_.db().manager())
        c = FLSqlCursor(field.relationM1().foreignTable(), True, self.cursor_.db().connectionName())
        #c = FLSqlCursor(field.relationM1().foreignTable())
        c.select(mng.formatAssignValue(field.relationM1().foreignField(), field, v, True))
        #if c.size() <= 0:
        #    return

        if c.size() <= 0:
            return

        if self.actionName_.isEmpty():
            a = c.action()
        else:
            a = self.actionName_

        c.setAction(a)

        self.modemodeAccess = self.cursor_.modeAccess()
        if self.modeAccess == FLSqlCursor.Insert or self.modeAccess == FLSqlCursor.Del:
            self.modeAccess = FLSqlCursor.Edit

        c.openFormInMode(self.modeAccess, False)



    """
    Abre un dialogo para buscar en la tabla relacionada
    """
    @QtCore.pyqtSlot()
    @QtCore.pyqtSlot(int)
    def searchValue(self):

        if not self.cursor_:
            return

        if not self.fieldName_:
            return
        tMD = self.cursor_.metadata()
        if not tMD:
            return

        field = tMD.field(self.fieldName_)
        if not field:
            return

        if not field.relationM1():
            print("FLFieldDB : El campo de búsqueda debe tener una relación M1")
            return

        fMD = field.associatedField()

        if fMD:
            if not fMD.relationM1():
                print("FLFieldDB : El campo asociado debe tener una relación M1")
                return

            v = self.cursor_.valueBuffer(fMD.name())
            if not v or self.cursor_.bufferIsNull(fMD.name()):
                QtGui.QMessageBox.warning(QtGui.qApp.focusWidget(), "Aviso", str("Debe indicar un valor para", fMD.alias()))
                return

            mng = self.cursor_.db().manager()
            c = FLSqlCursor(fMD.relationM1().foreignTable())
            c.select(mng.formatAssignValue(fMD.relationM1().foreignField(), fMD, v, True))

            if c.size() > 0:
                c.next()

            if not self.actionName_:
                a = mng.action(field.relationM1().foreignTable())
            else:
                print(2)
                a = mng.action(self.actionName_)
                a.setTable(field.relationM1().foreignField())

            f = FLFormSearchDB(c, a.name(), None)
            f.setWindowModality(QtCore.Qt.ApplicationModal)

        else:
            mng = self.cursor_.db().manager()
            if not self.actionName_:
                a = mng.action(field.relationM1().foreignTable())
                if not a:
                    return
            else:
                a = mng.action(self.actionName_)
                if not a:
                    return
                a.setTable(field.relationM1().foreignTable())
            c = FLSqlCursor(a.table())
            #f = FLFormSearchDB(c, a.name(), self.topWidget_)
            f = FLFormSearchDB(c, c.action(), None)
            f.setWindowModality(QtCore.Qt.ApplicationModal)

        f.setMainWidget()
        """
        lObjs = f.queryList("FLTableDB")
        obj = lObjs.first()
        del lObjs
        objTdb = obj
        if fMD and objTdb:
            objTdb.setTablename(field.relationM1().foreignTable())
            objTdb.setFieldRelation(field.associatedFieldFilterTo())
            objTdb.setForeignField(fMD.relationM1().foreignField())
            if fMD.relationM1().foreignTable() == tMD.name():
                objTdb.setReadOnly(True)

        f.setFilter(self.filter_)
        if f.mainWidget():
            if objTdb:
                curValue = self.value()
                if field.type() == "string" and curValue:
                    objTdb.setInitSearch(curValue)
                    objTdb.putFisrtCol(field.relationM1().foreignField())
                QtCore.QTimer.singleShot(0,objTdb.lineEditSearch, self.setFocus)
        """
        v = f.exec_(field.relationM1().foreignField())
        if v:
            self.setValue("")
            self.setValue(v)

        #FIXME
        #f.close()
        #if c:
            #c.deletelater()



    """
    Abre un dialogo para buscar un fichero de imagen.

    Si el campo no es de tipo Pixmap no hace nada
    """
    @QtCore.pyqtSlot()
    def searchPixmap(self):
        if not self.cursor_ or not self.editorImg_:
            return


        if self.fieldName_.isEmpty():
            return
        tMD = FLTableMetaData(self.cursor_.metadata())
        if not tMD:
            return

        field = FLFieldMetaData(tMD.field(self.fieldName_))
        if not field:
            return

        if field.type() == "pixmap":
            fd = QtGui.QFileDialog(self,0,True)
            #p = FLPixmapView(fd)

            #p.setAutoScaled(True)
            fd.setContentsPreviewEnabled(True)
            #fd.setContentsPreview(p, p)
            fd.setPreviewMode(QtGui.QFileDialog.Contents)
            fd.setCaption(tr("Elegir archivo"))
            fd.setFilter("*")

            filename = None
            if (fd.exec_() == QtGui.QDialog.Accepted):
                filename = fd.selectedFile()

            if filename.isEmpty():
                return
            self.setPixmap(filename)



    """
  Carga una imagen en el campo de tipo pixmap
  @param filename: Ruta al fichero que contiene la imagen
    """
    @decorators.BetaImplementation
    def setPixmap(self, filename):
        img = QtGui.QImage(filename)

        if img.isNull():
            return

        QtGui.QApplication.setOverrideCursor(Qt.WaitCursor)
        pix = QtGui.QPixmap()
        s = None
        buffer = QtCore.QBuffer(s)

        if img.width() <= self.maxPixImages_ and img.height() <= self.maxPixImages_:
            pix.convertFromImage(img)
        else:
            newWidth = 0
            newHeight = 0
            if img.width() < img.height():
                newHeight = self.maxPixImages_
                newWidth = round(newWidth * img.width() / img.heigth())
            else:
                newWidth = self.mapPixImages_
                newHeight = round(newWidth * img.height() / img.width())
            pix.convertFromImage(img.scale(newWidth, newHeight, QtGui.QImage.ScaleMin))

        QtGui.QApplication.restoreOverrideCursor()

        if pix.isNull():
            return

        self.editorImg_.setPixmap(pix)

        QtGui.QApplication.setOverrideCursor(Qt.WaitCursor)
        buffer.open(Qt.IO_WriteOnly)
        pix.save(buffer,"XPM")

        QtGui.QApplication.restoreOverrideCursor()

        if s.isEmpty():
            return

        if not QtGui.QPixmapCache.find(s.left(100)):
            QtGui.QPixmapCache.insert(s.left(100), pix)

        self.updateValue(QString(s))

    """
  Carga una imagen en el campo de tipo pixmap con el ancho y alto preferido

  @param pixmap: pixmap a cargar en el campo
  @param w: ancho preferido de la imagen
  @param h: alto preferido de la imagen
  @author Silix
    """
    @decorators.NotImplementedWarn
    def setPixmapFromPixmap(self, pixmap, w = 0, h = 0):
        if pixmap.isNull():
            return

        QtGui.QApplication.setOverrideCursor(Qt.WaitCursor)
        pix = None
        s = None
        buffer = QtCore.QBuffer(s)

        img = QtGui.QImage(pixmap.convertToImage())
        if not w == 0 and not h == 0:
            pix.convertFromImage(img.scale(w, h, QtGui.QImage.ScaleMin))
        else:
            pix.convertFromImage(img)

        QtGui.QApplication.restoreOverrideCursor()
        if pix.isNull():
            return

        self.editorImg_.setPixmap(pix)

        QtGui.QApplication.setOverrideCursor(Qt.WaitCursor)

        buffer.open(Qt.IO_WriteOnly)
        pix.save(buffer,"XPM")

        QtGui.QApplication.restoreOverrideCursor()

        if s.isEmpty():
            return

        if not QtGui.QPixmapCache.find(s.left(100)):
            QtGui.QPixmapCache.insert(s.left(100), pix)

        self.updateValue(QString(s))

    """
  Carga una imagen desde el portapapeles en el campo de tipo pixmap
  @author Silix
    """
    @decorators.NotImplementedWarn
    def setPixmapFromClipboard(self):
        img = QtGui.QImage(QtGui.QApplication.clipboard().image())
        if img.isNull():
            return
        QtGui.QApplication.setOverrideCursor(Qt.WaitCursor)
        pix = None
        s = None
        buffer = QtCore.QBuffer(s)

        if img.width() <= self.maxPixImages_ and img.height() <= self.maxPixImages_:
            pix.convertFromImage(img)
        else:
            newWidth = 0
            newHeight = 0
            if img.width() < img.height():
                newHeight = self.maxPixImages_
                newWidth = round(newHeight * img.width() / img.height())
            else:
                newWidth = self.maxPixImages_
                newHeight = round(newWidth * img.height() / img.width())

            pix.convertFromImage(img.scale(newWidth, newHeight, QtGui.QImage.ScaleMin))

        QtGui.QApplication.restoreOverrideCursor()

        if pix.isNull():
            return

        self.editorImg_.setPixmap(pix)

        QtGui.QApplication.setOverrideCursor(Qt.WaitCursor)
        buffer.open(Qt.IO_WriteOnly)
        pix.save(buffer,"XPM")

        QtGui.QApplication.restoreOverrideCursor()

        if s.isEmpty():
            return

        if not QtGui.QPixmapCache.find(s.left(100)):
            QtGui.QPixmapCache.insert(s.left(100), pix)

        self.updateValue(QString(s))




    """
  Devueve el objeto imagen asociado al campo

  @return imagen asociada al campo
  @author Silix
    """
    @decorators.NotImplementedWarn
    def pixmap(self):
        pix = QtGui.QPixmap
        pix.loadFromData(self.value().toCString())
        return pix


    """
    Emite la señal de foco perdido
    """
    def emitLostFocus(self):
        self.lostFocus.emit()



    """
    Establece que el control no está mostrado
    """
    @QtCore.pyqtSlot()
    def setNoShowed(self):
        if not self.foreignField_.isEmpty() and not self.fieldRelation_.isEmpty():
            self.showed = False
            if self.isVisible():
                self.showWidget()

    """
    Establece el valor de este campo según el resultado de la consulta
    cuya claúsula 'where' es;  nombre campo del objeto que envía la señal igual
    al valor que se indica como parámetro.

    Sólo se pueden conectar objetos tipo FLFielDB, y su uso normal es conectar
    la señal FLFieldDB::textChanged(cons QString&) a este slot.

    @param v Valor
    """
    @decorators.NotImplementedWarn
    @QtCore.pyqtSlot(QString)
    def setMapValue(self, v):
        self.fieldMapValue_ = self.sender()
        self.mapValue_ = v
        self.setMapValue()
        #FIXME: Falta sin parametro




    """
    Emite la señal de keyF2Pressed.

    La señal key_F2_Pressed del editor (sólo si el editor es FLLineEdit)
    está conectada a este slot.
    """
    @QtCore.pyqtSlot()
    def emitKeyF2Pressed(self):
        self.keyF2Pressed_.emit()

    """
    Emite la señal de labelClicked. Se usa en los campos M1 para editar el formulario de edición del valor seleccionado.
    """
    @QtCore.pyqtSlot()
    def emitLabelClicked(self):
        self.labelClicked.emit()

    """
    Emite la señal de textChanged.

    La señal textChanged del editor (sólo si el editor es FLLineEdit)
    está conectada a este slot.
    """
    @QtCore.pyqtSlot(QString)
    def emitTextChanged(self, t):
        self.textChanged.emit(t)

    """
    Emite la señal activatedAccel( int )
    """
    @QtCore.pyqtSlot(int)
    def ActivatedAccel(self, identifier):
        if self.editor_ and self.editor_.hasFocus:
            self.activatedAccel.emit()



    """
    Redefinida por conveniencia
    """
    def setEnabled(self , enable):
        if enable:
            self.setAttribute(Qt.WA_ForceDisabled, False)
        else:
            self.setAttribute(Qt.WA_ForceDisabled, True)

        if not self.isTopLevel() and self.parentWidget() and not self.parentWidget().isEnabled() and enable:
            return

        if enable:
            if self.testAttribute(Qt.WA_Disabled):
                self.setAttribute(Qt.WA_Disabled, False)
                self.enabledChange(not enable)
                if self.children():
                    for w in self.children():
                        if not w.testAttribute(Qt.WA_ForceDisabled):
                            le = w
                            if isinstance(le, QtGui.QLineEdit):
                                allowNull = True
                                tMD = self.cursor_.metadata()
                                if tMD:
                                    field = tMD.field(self.fieldName_)
                                    if field and not field.allowNull():
                                        allowNull = False


                                if allowNull:
                                    cBg = QtGui.QColor.blue()
                                    cBg = QtGui.QApplication().palette().color(QtGui.QPalette.Active, QtGui.QPalette.Base)
                                else:
                                    cBg = self.NotNullColor()

                                le.setDisabled(False)
                                le.setReadOnly(False)
                                le.palette().setColor(QtGui.QPalette.Base, cBg);
                                le.setCursor(Qt.IBeamCursor)
                                le.setFocusPolicy(Qt.StrongFocus)
                                continue
                            w.setEnabled(True)



            else:
                if not self.testAttribute(Qt.WA_Disabled):
                    if self.focusWidget() == self:
                        parentIsEnabled = False
                        if not self.parentWidget() or self.parentWidget().isEnabled():
                            parentIsEnabled = True
                        if not parentIsEnabled or not self.focusNextPrevChild(True):
                            self.clearFocus()
                    self.setAttribute(Qt.WA_Disabled)
                    self.enabledChange(not enable)

                    if self.children():
                        for w in self.children():
                            if isinstance(w , QtGui.QLineEdit):
                                le = w
                                if le:
                                    le.setDisabled(False)
                                    le.setReadOnly(True)
                                    le.setCursor(Qt.IBeamCursor)
                                    le.setFocusPolicy(Qt.NoFocus)
                                    continue

                            if isinstance(w , QtGui.QTextEdit):
                                te = w
                                te.setDisabled(False)
                                te.setReadOnly(True)
                                te.viewPort().setCursor(Qt.IBeamCursor)
                                te.setFocusPolicy(Qt.NoFocus)
                                continue

                            if w == self.textLabelDB and self.pushButtonDB:
                                w.setDisabled(False)
                                continue

                            w.setEnabled(False)
                            w.setAttribute(Qt.WA_ForceDisabled, False)














    """
    Captura evento mostrar
    """
    def showEvent(self, e):
        self.showWidget()
        super(FLFieldDB,self).showEvent(e)
    """
    Redefinida por conveniencia
    """
    def showWidget(self):
        if not self._loaded: #Esperamos a que la carga se realice
            timer = QtCore.QTimer(self)
            timer.singleShot(30, self.showWidget)
            return
        else:
            if not self.showed:
                if self.topWidget_:
                    self.refresh()
                    #if self.cursorAux:
                        #print("Cursor auxiliar a ", self.tableName_)
                    if self.cursorAux and self.cursor_ and self.cursor_.bufferIsNull(self.fieldName_):
                        if not self.cursorAux.bufferIsNull(self.foreignField_):
                            mng = self.cursor_.db().manager()
                            tMD = self.cursor_.metadata()
                            if tMD:
                                v = self.cursorAux.valueBuffer(self.foreignField_)
                                #print("El valor de %s.%s es %s" % (tMD.name(), self.foreignField_, v))

                                #FIXME q = FLSqlQuery(False, self.cursor_.db().connectionName())
                                q = FLSqlQuery()
                                q.setForwardOnly(True)
                                q.setTablesList(self.tableName_)
                                q.setSelect(self.fieldName_)
                                q.setFrom(self.tableName_)
                                where = mng.formatAssignValue(tMD.field(self.fieldRelation_),v,True)
                                filterAc = self.cursorAux.filterAssoc(self.foreignField_, tMD)

                                if filterAc:
                                    #print("FilterAC == ", filterAc)
                                    if where.isEmpty():
                                        where = filterAc
                                    else:
                                        where += " AND " + filterAc

                                if self.filter_.isEmpty():
                                    q.setWhere(where)
                                else:
                                    q.setWhere(self.filter_ + " AND " + where)

                                #print("where tipo", type(where))
                                #print("Consulta = %s" % q.sql())
                                if q.exec_() and q.first():
                                    self.setValue(q.value(0))
                                if not tMD.inCache():
                                    del tMD


                else:
                    self.initFakeEditor()
                    self.showed = True
                    #print("FLFieldDB(%s).showWidget(): No tengo Padre! Snif !" % self.name)


            if self._initCursorWhenLoad:
                self._initCursorWhenLoad = False
                self.setNoShowed()
                self.initCursor()
                self.showWidget()

            if self._initEditorWhenLoad:
                self._initEditorWhenLoad = False
                self.setNoShowed()
                self.initEditor()
                self.showWidget()







    """
    Inicializa un editor falso y no funcional.

    Esto se utiliza cuando se está editando el formulario con el diseñador y no
    se puede mostrar el editor real por no tener conexión a la base de datos.
    Crea una previsualización muy esquemática del editor, pero suficiente para
    ver la posisicón y el tamaño aproximado que tendrá el editor real.
    """

    def initFakeEditor(self):

        hasPushButtonDB = None
        if self.tableName_.isEmpty() and self.foreignField_.isEmpty() and self.fieldRelation_.isEmpty():
            hasPushButtonDB = True
        else:
            hasPushButtonDB = False

        if self.fieldName_.isEmpty():
            self.fieldAlias_ = FLUtil.tr("Error: fieldName vacio")
        else:
            self.fieldAlias_ = self.fieldName_

        if not self.editor_:
            self.editor_ = QtGui.QLineEdit()
            self.editor_.setSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Fixed)
            self.textLabelDB.setSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Fixed)
            self.FLWidgetFieldDBLayout.addWidget(self.editor_)
            self.editor_.setFocusPolicy(Qt.StrongFocus)
            self.setFocusProxy(self.editor_)
            self.setTabOrder(self.pushButtonDB, self.editor_)
            self.editor_.show()

        self.textLabelDB.setText(self.fieldAlias_)
        if self.showAlias_:
            self.textLabelDB.show()
        else:
            self.textLabelDB.hide()

        if hasPushButtonDB:
            self.pushButtonDB.setFocusPolicy(Qt.NoFocus)
            self.pushButtonDB.show()
        else:
            self.pushButtonDB.hide()


        prty = QString()
        if not self.tableName_.isEmpty():
            prty += "tN:" + self.tableName_ + ","
        if not self.foreignField_.isEmpty():
            prty += "fF:" + self.foreignField_ + ","
        if not self.fieldRelation_.isEmpty():
            prty += "fR:" + self.fieldRelation_ + ","
        if not self.actionName_.isEmpty():
            prty += "aN:" + self.actionName_ + ","

        if not prty.isEmpty():
            self.editor_.setText(prty)
            self.editor_.home(False)

        if self.maximumSize().width() < 80:
            self.setShowEditor(False)
        else:
            self.setShowEditor(self.showEditor_)













    """
    Color de los campos obligatorios
    """
    def notNullColor(self):
        if not self.initNotNullColor_:
            self.initNotNullColor_ = True
        self.notNullColor_ = FLSettings().readEntry("ebcomportamiento/colorObligatorio",None)
        if self.notNullColor_ is None:
            self.notNullColor_ = QtGui.QColor(255, 233, 173)
        return self.notNullColor_



class FLDoubleValidator(QtGui.QDoubleValidator):

    def __init__(self, *args, **kwargs):
            super(FLDoubleValidator, self).__init__(*args)

    def validate(self, input_, i):
        if input_.isEmpty():
            return QtGui.QValidator.Acceptable

        input_.replace(",", ".")

        state = QtGui.QDoubleValidator.validate(input_, i)

        if isinstance(state, QtGui.QValidator.Invalid) or isinstance(state, QtGui.QValidator.Intermediate):
            s = QString(input_.right(input_.length() - 1))
            if input_.left(1) == "-" and (QtGui.QDoubleValidator.validate(s, i) == QtGui.QValidator.Acceptable or s.isEmpty()):
                state = QtGui.QValidator.Acceptable
            else:
                state = QtGui.QValidator.Invalid
        else:
            state = QtGui.QValidator.Acceptable

        if (QtGui.qApp.commaSeparator() == ","):
            input_.replace(".", ",")
        else:
            input_.replace(",", ".")

        return state




class FLIntValidator(QtGui.QIntValidator):

    def __init__(self, *args, **kwargs):
            super(FLIntValidator, self).__init__(*args)

    def validate(self, input_, i):
        if input_.isEmpty():
            return QtGui.QValidator.Acceptable

        input_.replace(",", ".")

        state = QtGui.QIntValidator.validate(input_, i)

        if isinstance(state, QtGui.QValidator.Invalid) or isinstance(state, QtGui.QValidator.Intermediate):
            s = QString(input_.right(input_.length() - 1))
            if input_.left(1) == "-" and (QtGui.QIntValidator.validate(s, i) == QtGui.QValidator.Acceptable or s.isEmpty()):
                state = QtGui.QValidator.Acceptable
            else:
                state = QtGui.QValidator.Invalid
        else:
            state = QtGui.QValidator.Acceptable

        if (QtGui.qApp.commaSeparator() == ","):
            input_.replace(".", ",")
        else:
            input_.replace(",", ".")

        return state




class FLUIntValidator(QtGui.QIntValidator):

    def __init__(self, *args, **kwargs):
            super(FLUIntValidator, self).__init__(*args)

    def validate(self, input_, i):
        if input_.isEmpty():
            return QtGui.QValidator.Acceptable

        iV = QtGui.QIntValidator(0, 1000000000, 0)
        state = iV.validate(input_, i)
        if state == QtGui.QValidator.Intermediate:
            state = QtGui.QValidator.Invalid

        return state







class FLPixmapView(QtGui.QWidget):
    frame_ = None
    scrollView = None
    autoScaled_ = None
    path_ = None
    pixmap_ = None
    pixmapView_ = None
    lay_ = None
    gB_ = None

    def __init__(self, parent):
        super(FLPixmapView,self).__init__(parent)
        self.scrollView = QtGui.QScrollArea(parent)
        self.autoScaled_ = False
        self.lay_ = QtGui.QHBoxLayout(self)
        self.pixmap_ = QtGui.QPixmap()
        self.pixmapView_ = QtGui.QLabel(self)
        self.lay_.addWidget(self.pixmapView_)

    def setPixmap(self, pix):
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        self.pixmap_ = pix
        if not self.autoScaled_:
            self.resize(self.pixmap_.size().width(), self.pixmap_.size().height())
        self.pixmapView_.clear()
        self.pixmapView_.setPixmap(self.pixmap_)
        self.repaint()
        QtGui.QApplication.restoreOverrideCursor()

    def drawContents(self, p, cx, cy, cw, ch):
        p.setBrush(QtGui.QPalette.Background)
        p.drawRect(cx, cy, cw, ch)
        if self.autoScaled_:
            newWidth = self.width() -2
            newHeight = self.height() -2

            if not self.pixmapWiev_ is None and self.pixmapView_.width() == newWidth and self.pixmapView_.height() == newHeight:
                return

            img = self.pixmap_
            if img.width() > newWidth or img.height() > newHeight:
                self.pixmapView_.convertFromImage(img.scaled(newWidth, newHeight, QtCore.Qt.KeepAspectRatio))
            else:
                self.pixmapView_.convertFromImage(img)

            if not self.pixmapView_ is None:
                p.drawPixmap((self.width() /2) - (self.pixmapView_.width() /2), (self.height()/ 2) - (self.pixmapView_.height() /2), self.pixmapView_ )
            elif not self.pixmap_ is None:
                p.drawPixmap((self.width() /2) - (self.pixmap_.width() /2), (self.height()/ 2) - (self.pixmap_.height() /2), self.pixmap_ )

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
            QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
            pix.convertFromImage(img)
            QtGui.QApplication.restoreOverrideCursor()

            if not pix is None:
                self.setPixmap(pix)

    def clear(self):
        self.pixmapView_.clear()

    def pixmap(self):
        return self.pixmap_

    def setAutoScaled(self, autoScaled):
        self.autoScaled_ = autoScaled


class FLDateEdit(QtGui.QDateEdit):

    valueChanged = QtCore.pyqtSignal()

    def __init__(self, parent, name):
        super(FLDateEdit,self).__init__(parent)



class FLSpinBox(QtGui.QSpinBox):

    @decorators.WorkingOnThis
    def __init__(self, parent = False, name = False):
        super(FLSpinBox,self).__init__(parent, name)
        #editor()setAlignment(Qt::AlignRight);



















