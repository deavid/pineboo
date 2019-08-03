# -*- coding: utf-8 -*-
import datetime

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QDateTime, pyqtSignal

from pineboolib.core.utils.utils_base import filedir, aqtt
from pineboolib.core.settings import config
from pineboolib.core import decorators

from pineboolib.application.metadata.pntablemetadata import PNTableMetaData
from pineboolib.application.metadata.pnrelationmetadata import PNRelationMetaData
from pineboolib.application import project

from pineboolib.qt3_widgets.qpushbutton import QPushButton
from pineboolib.qt3_widgets.qtextedit import QTextEdit
from pineboolib.qt3_widgets.qlineedit import QLineEdit
from pineboolib.qt3_widgets.qcheckbox import QCheckBox
from pineboolib.qt3_widgets.qcombobox import QComboBox
from pineboolib.qt3_widgets.qwidget import QWidget
from pineboolib.qt3_widgets.qvboxlayout import QVBoxLayout

from .flsqlcursor import FLSqlCursor
from .fllineedit import FLLineEdit
from .flutil import FLUtil
from .flsqlquery import FLSqlQuery
from .flformsearchdb import FLFormSearchDB
from .flformdb import FLFormDB
from .fltabledb import FLTableDB
from .fluintvalidator import FLUIntValidator
from .flintvalidator import FLIntValidator
from .fldoublevalidator import FLDoubleValidator
from .fldateedit import FLDateEdit
from .fltimeedit import FLTimeEdit
from .flpixmapview import FLPixmapView
from .flspinbox import FLSpinBox
from .fldatatable import FLDataTable

from pineboolib import logging

from typing import Any, Optional, TYPE_CHECKING, cast

if TYPE_CHECKING:
    from PyQt5.QtGui import QPixmap


class FLFieldDB(QtWidgets.QWidget):
    logger = logging.getLogger("FLFieldDB")
    _loaded: bool
    _parent: QtWidgets.QWidget

    _tipo: str
    _partDecimal: int
    autoSelect: bool

    editor_: QtWidgets.QWidget  # Editor para el contenido del campo que representa el componente
    fieldName_: str  # Nombre del campo de la tabla al que esta asociado este componente
    tableName_: Optional[str]  # Nombre de la tabla fóranea
    actionName_: Optional[str]  # Nombre de la accion
    foreignField_: Optional[str]  # Nombre del campo foráneo
    fieldRelation_: Optional[str]  # Nombre del campo de la relación
    filter_: Optional[str]  # Nombre del campo de la relación
    cursor_: Any  # Cursor con los datos de la tabla origen para el componente
    cursorInit_: bool  # Indica que si ya se ha inicializado el cursor
    cursorAuxInit: bool  # Indica que si ya se ha inicializado el cursor auxiliar
    cursorBackup_: Any  # Backup del cursor por defecto para acceder al modo tabla externa
    cursorAux: Any  # Cursor auxiliar de uso interno para almacenar los registros de la tabla relacionada con la de origen

    showed: bool
    showAlias_: bool
    datePopup_ = None
    dateFrame_ = None
    datePickedOn_ = False
    autoComPopup_ = None
    autoComFrame_ = None
    autoComFieldName_ = None
    accel_ = None
    keepDisabled_: bool
    editorImg_: Optional["FLPixmapView"]
    pbAux_: Optional[QPushButton]
    pbAux2_: Optional[QPushButton]
    pbAux3_: Optional[QPushButton]
    pbAux4_: Optional[QPushButton]
    fieldAlias_: Optional[str]
    showEditor_: bool
    fieldMapValue_ = None
    autoCompMode_: str  # NeverAuto, OnDemandF4, AlwaysAuto
    timerAutoComp_: QtCore.QTimer
    textFormat_ = QtCore.Qt.AutoText
    initNotNullColor_: bool
    textLabelDB = None
    FLWidgetFieldDBLayout = None
    name: str

    _refreshLaterEditor: Optional[str]

    pushButtonDB: QPushButton
    keyF4Pressed = QtCore.pyqtSignal()
    labelClicked = QtCore.pyqtSignal()
    keyReturnPressed = QtCore.pyqtSignal()
    lostFocus = QtCore.pyqtSignal()
    textChanged = QtCore.pyqtSignal(str)
    keyF2Pressed = QtCore.pyqtSignal()

    firstRefresh = None
    default_style = None

    """
    Tamaño de icono por defecto
    """
    iconSize: QtCore.QSize

    def __init__(self, parent: "QtWidgets.QWidget", *args) -> None:
        super(FLFieldDB, self).__init__(parent)
        self._loaded = False
        self.DEBUG = False  # FIXME: debe recoger DEBUG de pineboolib.project
        self.editor_ = QtWidgets.QWidget(parent)
        self.editor_.hide()
        self.cursor_ = None
        self.cursorBackup_ = None
        self.cursorInit_ = False
        self.cursorAuxInit_ = False
        self.showAlias_ = True
        self.showEditor_ = True
        self.autoCompMode_ = "OnDemandF4"
        self.name = "FLFieldDB"
        self.showed = False
        self._refreshLaterEditor = None
        self.keepDisabled_ = False
        self.initNotNullColor_ = False
        self.actionName_ = None
        self.pbAux_ = None
        self.pbAux2_ = None
        self.pbAux3_ = None
        self.pbAux4_ = None

        self.maxPixImages_ = config.value("ebcomportamiento/maxPixImages", None)
        self.autoCompMode_ = config.value("ebcomportamiento/autoComp", "OnDemandF4")
        if self.maxPixImages_ in (None, ""):
            self.maxPixImages_ = 600
        self.maxPixImages_ = int(self.maxPixImages_)
        self.editorImg_ = None
        self.topWidget_ = parent
        # self._parent = parent
        from pineboolib.qt3_widgets.qpushbutton import QPushButton
        from pineboolib.application import project

        self.iconSize = project.DGI.iconSize()

        self.FLLayoutH = QtWidgets.QVBoxLayout(self)
        self.FLLayoutH.setContentsMargins(0, 0, 0, 0)
        self.FLLayoutH.setSpacing(1)
        # self.FLLayoutH.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)

        self.lytButtons = QtWidgets.QHBoxLayout()
        self.lytButtons.setContentsMargins(0, 0, 0, 0)
        self.lytButtons.setSpacing(1)
        self.lytButtons.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)

        # self.lytButtons.SetMinimumSize(22,22)
        # self.lytButtons.SetMaximumSize(22,22)

        self.FLWidgetFieldDBLayout = QtWidgets.QHBoxLayout()
        self.FLWidgetFieldDBLayout.setSpacing(1)
        self.FLWidgetFieldDBLayout.setContentsMargins(0, 0, 0, 0)
        self.FLWidgetFieldDBLayout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.FLLayoutH.addLayout(self.lytButtons)
        self.FLLayoutH.addLayout(self.FLWidgetFieldDBLayout)
        self.tableName_ = None
        self.foreignField_ = None
        self.fieldRelation_ = None

        self.textLabelDB = QtWidgets.QLabel()
        self.textLabelDB.setMinimumHeight(16)  # No inicia originalmente aqui
        self.textLabelDB.setAlignment(
            cast(QtCore.Qt.AlignmentFlag, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        )
        # self.textLabelDB.setFrameShape(QtGui.QFrame.WinPanel)
        self.textLabelDB.setFrameShadow(QtWidgets.QFrame.Plain)
        self.textLabelDB.setLineWidth(0)
        self.textLabelDB.setTextFormat(QtCore.Qt.PlainText)
        self.textLabelDB.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        self.fieldAlias_ = None
        self.filter_ = None

        self.FLWidgetFieldDBLayout.addWidget(self.textLabelDB)

        self.pushButtonDB = QPushButton()
        if project.DGI.localDesktop():
            self.setFocusProxy(self.pushButtonDB)
        # self.pushButtonDB.setFlat(True)
        PBSizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        PBSizePolicy.setHeightForWidth(True)
        self.pushButtonDB.setSizePolicy(PBSizePolicy)
        self.pushButtonDB.setMinimumSize(self.iconSize)
        self.pushButtonDB.setMaximumSize(self.iconSize)
        self.pushButtonDB.setFocusPolicy(Qt.NoFocus)
        self.pushButtonDB.setIcon(QtGui.QIcon(filedir("../share/icons", "flfielddb.png")))
        # self.FLWidgetFieldDBLayout.addWidget(self.pushButtonDB)
        self.pushButtonDB.clicked.connect(self.searchValue)

        self.timer_1 = QtCore.QTimer(self)
        # self.timer_1.singleShot(120, self.loaded)
        self.cursorAux = None

        while not isinstance(self.topWidget_, FLFormDB):
            self.topWidget_ = self.topWidget_.parentWidget()
            if not self.topWidget_:
                break

    def load(self) -> None:

        if self._loaded:
            return

        self._loaded = True
        if self.topWidget_:
            self.cursor_ = self.topWidget_.cursor()
            # print("Hay topWidget en %s", self)
        if self.DEBUG:
            if self.cursor_ and self.cursor_.d.buffer_:
                self.logger.info(
                    "*** FLFieldDB::loaded: cursor: %r name: %r at:%r",
                    self.cursor_,
                    self.cursor_.curName(),
                    self.cursor_.at(),
                )
                cur_values = [f.value for f in self.cursor_.d.buffer_.fieldList_]
                self.logger.info("*** cursor Buffer: %r", cur_values)
            else:
                self.logger.warning("*** FLFieldDB::loaded: SIN cursor ??")

        self.cursorBackup_ = False
        self._partDecimal = 0
        self.initCursor()
        if self.tableName_ and not self.cursor_.db().manager().metadata(self.tableName_):
            self.cursor_ = None
            self.initFakeEditor()
        else:
            self.initEditor()

    def setName(self, value: str) -> None:
        self.name = str(value)

    """
    Para obtener el nombre de la accion.

    @return Nombre de la accion
    """

    def actionName(self) -> str:
        if not self.actionName_:
            raise ValueError("actionName is not defined!")
        return self.actionName_

    """
    Para establecer el nombre de la accion.

    @param aN Nombre de la accion
    """

    def setActionName(self, aN: str) -> None:
        self.actionName_ = str(aN)

    """
    Para obtener el nombre del campo.

    @return Nombre del campo
    """

    def fieldName(self) -> str:
        if not self.fieldName_:
            raise ValueError("fieldName is not defined!")
        return self.fieldName_

    """
    Para añadir un filtro al cursor.

    """

    def setFilter(self, f: str) -> None:
        self.filter_ = f
        self.setMapValue()

    """
    Para obtener el filtro del cursor.

    """

    def filter(self) -> Optional[str]:
        return self.filter_

    """
    Para establecer el nombre del campo.

    @param fN Nombre del campo
    """

    def setFieldName(self, fN: str) -> None:
        self.fieldName_ = fN

    """
    Para obtener el nombre de la tabla foránea.

    @return Nombre de la tabla
    """

    def tableName(self) -> Optional[str]:
        return self.tableName_

    """
    Para establecer el nombre de la tabla foránea.

    @param fT Nombre de la tabla
    """

    def setTableName(self, fT: str) -> None:

        self.tableName_ = None
        if not fT == "":
            self.tableName_ = fT

    """
    Para obtener el nombre del campo foráneo.

    @return Nombre del campo
    """

    def foreignField(self) -> Optional[str]:
        return self.foreignField_

    """
    Para establecer el nombre del campo foráneo.

    @param fN Nombre del campo
    """

    def setForeignField(self, fN: str) -> None:
        self.foreignField_ = fN

    """
    Para obtener el nombre del campo relacionado.

    @return Nombre del campo
    """

    def fieldRelation(self) -> Optional[str]:
        return self.fieldRelation_

    """
    Para establecer el nombre del campo relacionado.

    @param fN Nombre del campo
    """

    def setFieldRelation(self, fN: str) -> None:
        self.fieldRelation_ = fN

    """
    Para establecer el alias del campo, mostrado en su etiqueta si showAlias es true

    @param alias Alias del campo, es el valor de la etiqueta. Si es vacio no hace nada.
    """

    def setFieldAlias(self, alias: str) -> None:
        if alias:
            self.fieldAlias_ = alias
            if self.showAlias_ and self.textLabelDB:
                self.textLabelDB.setText(self.fieldAlias_)

    """
    Establece el formato del texto

    @param f Formato del campo
    """

    def setTextFormat(self, f: Qt.TextFormat) -> None:
        self.textFormat_ = f
        ted = self.editor_
        if isinstance(ted, QTextEdit):
            ted.setTextFormat(self.textFormat_)

    def textFormat(self) -> Qt.TextFormat:
        """@return El formato del texto."""
        ted = self.editor_
        if isinstance(ted, QTextEdit):
            return ted.textFormat()
        return self.textFormat_

    def setEchoMode(self, m: QLineEdit.EchoMode) -> None:
        """Establece el modo de "echo".

        @param m Modo (Normal, NoEcho, Password)
        """
        led = self.editor_
        if isinstance(led, QLineEdit):
            led.setEchoMode(m)

    def echoMode(self) -> int:
        """Returns the echo mode.

        @return El mode de "echo" (Normal, NoEcho, Password)
        """
        led = self.editor_
        if isinstance(led, QLineEdit):
            return led.echoMode()

        return QLineEdit.Normal

    def _process_autocomplete_events(self, event: Any) -> bool:
        timerActive = False
        if self.autoComFrame_ and self.autoComFrame_.isVisible():
            if event.key() == Qt.Key_Down and self.autoComPopup_:
                self.autoComPopup_.setQuickFocus()
                return True

            # --> WIN
            if self.editor_:
                self.editor_.releaseKeyboard()
            if self.autoComPopup_:
                self.autoComPopup_.releaseKeyboard()
            # <-- WIN

            self.autoComFrame_.hide()
            if self.editor_ and event.key() == Qt.Key_Backspace:
                self.editor_.backspace()

            if not self.timerAutoComp_:
                self.timerAutoComp_ = QtCore.QTimer(self)
                self.timerAutoComp_.timeout.connect(self.toggleAutoCompletion)
            else:
                self.timerAutoComp_.stop()

            if not event.key() in (Qt.Key_Enter, Qt.Key_Return):
                timerActive = True
                self.timerAutoComp_.start(500)
            else:
                QtCore.QTimer.singleShot(0, self.autoCompletionUpdateValue)
                return True
        if (
            not timerActive
            and self.autoCompMode_ == "AlwaysAuto"
            and (not self.autoComFrame_ or not self.autoComFrame_.isVisible())
        ):
            if event.key() in (Qt.Key_Backspace, Qt.Key_Delete, Qt.Key_Space, Qt.Key_ydiaeresis):
                if not self.timerAutoComp_:
                    self.timerAutoComp_ = QtCore.QTimer(self)
                    self.timerAutoComp_.timeout.connect(self.toggleAutoCompletion)
                else:
                    self.timerAutoComp_.stop()

                if not event.key() in (Qt.Key_Enter, Qt.Key_Return):
                    timerActive = True
                    self.timerAutoComp_.start(500)
                else:
                    QtCore.QTimer.singleShot(0, self.autoCompletionUpdateValue)
                    return True
        return False

    @decorators.pyqtSlot()
    @decorators.pyqtSlot(int)
    def eventFilter(self, obj: Any, event: Any):
        """Process Qt events for keypresses.

        Filtro de eventos
        """
        if not obj:
            return True

        QtWidgets.QWidget.eventFilter(self, obj, event)
        if event.type() == QtCore.QEvent.KeyPress:
            k = event
            if self._process_autocomplete_events(event):
                return True

            if isinstance(obj, FLLineEdit):
                if k.key() == Qt.Key_F4:
                    self.keyF4Pressed.emit()
                    return True
            elif isinstance(obj, QTextEdit):
                if k.key() == Qt.Key_F4:
                    self.keyF4Pressed.emit()
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
                self.keyF2Pressed.emit()
                return True

            return False

        # elif isinstance(event, QtCore.QEvent.MouseButtonRelease) and
        # isinstance(obj,self.textLabelDB) and event.button() == Qt.LeftButton:
        elif (
            event.type() == QtCore.QEvent.MouseButtonRelease
            and isinstance(obj, type(self.textLabelDB))
            and event.button() == Qt.LeftButton
        ):
            self.emitLabelClicked()
            return True
        else:
            return False

    @decorators.pyqtSlot()
    def updateValue(self, data: Optional[Any] = None):
        """Actualiza el valor del campo con una cadena de texto.

        @param t Cadena de texto para actualizar el campo
        """
        # print("Update Value", type(data), type(self.editor_))
        # if isinstance(data, QString): #Para quitar en el futuro
        #   data = str(data)
        if not self.cursor_:
            return

        isNull = False

        """
        if data is None:
            if not self.cursor_:
                return
            #ted = self.editor_
            data = self.editor_
            print("Tipo ...", type(data))
            if isinstance(data, FLLineEdit):
                t = self.editor_.text()

            elif isinstance(data, QtGui.QTextEdit):
                t = str(self.editor_.toPlainText())

            elif isinstance(data, FLDateEdit):
                t = str(self.editor_.date().toString(Qt.ISODate))

            #else:
                #return

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

        """
        if isinstance(self.editor_, FLDateEdit):
            data = str(self.editor_.getDate())
            if not data:
                isNull = True

            if not self.cursor_.bufferIsNull(self.fieldName_):

                if str(data) == self.cursor_.valueBuffer(self.fieldName_):
                    return
            elif isNull:
                return

            if isNull:
                self.cursor_.setValueBuffer(self.fieldName_, QtCore.QDate().toString("dd-MM-yyyy"))
            else:
                self.cursor_.setValueBuffer(self.fieldName_, data)

        elif isinstance(self.editor_, FLTimeEdit):
            data = str(self.editor_.time().toString("hh:mm:ss"))

            if not data:
                isNull = True
            if not self.cursor_.bufferIsNull(self.fieldName_):

                if str(data) == self.cursor_.valueBuffer(self.fieldName_):
                    return
            elif isNull:
                return

            if isNull:
                self.cursor_.setValueBuffer(
                    self.fieldName_, str(QtCore.QTime().toString("hh:mm:ss"))
                )
            else:
                self.cursor_.setValueBuffer(self.fieldName_, data)

        elif isinstance(self.editor_, QCheckBox):
            data = bool(self.editor_.checkState())

            if not self.cursor_.bufferIsNull(self.fieldName_):
                if data == bool(self.cursor_.valueBuffer(self.fieldName_)):
                    return

            self.cursor_.setValueBuffer(self.fieldName_, data)

        elif isinstance(self.editor_, QTextEdit):
            data = str(self.editor_.toPlainText())
            if not self.cursor_.bufferIsNull(self.fieldName_):
                if self.cursor_.valueBuffer(self.fieldName_) == data:
                    return

            self.cursor_.setValueBuffer(self.fieldName_, data)

        elif isinstance(self.editor_, FLLineEdit):

            data = self.editor_.text()
            if not self.cursor_.bufferIsNull(self.fieldName_):
                if data == self.cursor_.valueBuffer(self.fieldName_):
                    return
            self.cursor_.setValueBuffer(self.fieldName_, data)

        elif isinstance(self.editor_, QComboBox):
            data = str(self.editor_.getCurrentText())

            if not self.cursor_.bufferIsNull(self.fieldName_):
                if data == self.cursor_.valueBuffer(self.fieldName_):
                    return

            self.cursor_.setValueBuffer(self.fieldName_, str(data))

        elif isinstance(self.editorImg_, FLPixmapView):
            if data == self.cursor_.valueBuffer(self.fieldName_):
                return
            self.cursor_.setValueBuffer(self.fieldName_, data)

        """
        elif isinstance(self.editor_, str) or isinstance(data, int):
            tMD = self.cursor_.metadata()
            if not tMD:
                return
            field = tMD.field(self.fieldName_)
            if not field:
                return

            ol = field.hasOptionsList()
            tAux = data

            if ol and self.editor_:
                tAux = field.optionsList()[data]

            if not self.cursor_.bufferIsNull(self.fieldName_):
                if tAux == self.cursor_.valueBuffer(self.fieldName_):
                    return

            elif not tAux:
                return


            s = tAux
            if field.type() == "string" and not ol:
                if len(s) > 1 and s[0] == " ":
                    self.cursor_.bufferChanged.disconnect(self.refreshQuick)
                    self.cursor.setValueBuffer(self.fieldName_, s[1:])
                    self.cursor_.bufferChanged.connect(self.refreshQuick)
                    return

            if self.editor_ and (field.type() == "double" or field.type() == "int" or field.type() == "uint"):
                s = self.editor_.text()

            if s:
                self.cursor_.setValueBuffer(self.fieldName_, s)
            else:
                self.cursor_.setValueBuffer(self.fieldName_, "")
        """
        # if self.isVisible() and self.hasFocus() and field.type() == "string" and field.length() == len(s):
        # self.focusNextPrevChild(True)

    def status(self) -> None:
        self.logger.info("****************STATUS**************")
        self.logger.info("FLField:", self.fieldName_)
        self.logger.info("FieldAlias:", self.fieldAlias_)
        self.logger.info("FieldRelation:", self.fieldRelation_)
        self.logger.info("Cursor:", self.cursor_)
        self.logger.info("CurName:", self.cursor().curName() if self.cursor_ else None)
        self.logger.info("Editor: %s, EditorImg: %s" % (self.editor_, self.editorImg_))
        self.logger.info("RefreshLaterEditor:", self._refreshLaterEditor)
        self.logger.info("************************************")

    """
    Establece el valor contenido en el campo.

    @param v Valor a establecer
    """

    def setValue(self, v: Any) -> None:
        if not self.cursor_:
            self.logger.error(
                "FLFieldDB(%s):ERROR: El control no tiene cursor todavía. (%s)",
                self.fieldName_,
                self,
            )
            return
        # if v:
        #    print("FLFieldDB(%s).setValue(%s) ---> %s" % (self.fieldName_, v, self.editor_))

        if v == "":
            v = None

        tMD = self.cursor_.metadata()
        if not tMD:
            return

        field = tMD.field(self.fieldName_)
        if field is None:
            self.logger.warning("FLFieldDB::setValue(%s) : No existe el campo ", self.fieldName_)
            return

        type_ = field.type()

        # v = QVariant(cv)
        if field.hasOptionsList():
            idxItem = -1
            if type_ == "string":
                if v in field.optionsList():
                    idxItem = field.optionsList().index(v)
                else:
                    self.logger.warning(
                        "No se encuentra el valor %s en las opciones %s", v, field.optionsList()
                    )
            if idxItem == -1:
                self.editor_.setCurrentItem(v)
            self.updateValue(self.editor_.currentText)
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
        if type_ in ("uint", "int"):
            if self.editor_:
                doHome = False
                if not self.editor_.text():
                    doHome = True
                if v:
                    self.editor_.setText(v)
                else:
                    self.editor_.setText("0")

                if doHome:
                    self.editor_.home(False)

        elif type_ == "string":
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

        elif type_ == "stringlist":
            if not self.editor_:
                return

            if v is not None:
                self.editor_.setText(v)
            else:
                self.editor_.setText("")

        elif type_ == "double":
            if self.editor_:
                s = None
                if v is not None:
                    if self._partDecimal:
                        s = round(float(v), self._partDecimal)
                    else:
                        s = round(float(v), field.partDecimal())
                    self.editor_.setText(str(s))
                else:

                    self.editor_.setText("")

        elif type_ == "serial":
            if self.editor_:
                if v is not None:
                    self.editor_.setText(str(v))
                else:
                    self.editor_.setText("")

        elif type_ == "pixmap":
            if self.editorImg_:

                if v is None:
                    self.editorImg_.clear()
                    return
                pix = QtGui.QPixmap(v)
                # if not QtGui.QPixmapCache().find(cs.left(100), pix):
                # print("FLFieldDB(%s) :: La imagen no se ha cargado correctamente" % self.fieldName_)
                #    QtGui.QPixmapCache().insert(cs.left(100), pix)
                # print("PIX =", pix)
                if pix:
                    self.editorImg_.setPixmap(pix)
                else:
                    self.editorImg_.clear()

        elif type_ == "date":
            if self.editor_:
                if v is None:
                    self.editor_.setDate(QtCore.QDate())
                elif isinstance(v, str):
                    if v.find("T") > -1:
                        v = v[0 : v.find("T")]
                    self.editor_.setDate(QtCore.QDate.fromString(v, "yyyy-MM-dd"))
                else:
                    self.editor_.setDate(v)

        elif type_ == "time":
            if self.editor_:
                if v is None:
                    self.editor_.setTime(QtCore.QTime())
                else:
                    self.editor_.setTime(v)

        elif type_ == "bool":
            if self.editor_ and v is not None:
                self.editor_.setChecked(v)

    """
    Obtiene el valor contenido en el campo.
    """

    def value(self) -> Any:
        if not self.cursor_:
            return None

        tMD = self.cursor_.metadata()
        if not tMD:
            return None

        field = tMD.field(self.fieldName_)
        if field is None:
            self.logger.warning(
                self.tr("FLFieldDB::value() : No existe el campo %s" % self.fieldName_)
            )
            return None

        v: Any = None

        if field.hasOptionsList():
            v = int(self.editor_.currentItem())
            return v

        type_ = field.type()
        # fltype = FLFieldMetaData.flDecodeType(type_)

        if self.cursor_.bufferIsNull(self.fieldName_):
            if type_ == "double" or type_ == "int" or type_ == "uint":
                return 0

        if type_ in ("string", "stringlist"):
            if self.editor_:
                ed_ = self.editor_
                if isinstance(ed_, FLLineEdit):
                    v = ed_.text()

        if type_ in ("int", "uint"):
            if self.editor_:
                ed_ = self.editor_
                if isinstance(ed_, FLLineEdit):
                    v = ed_.text()
                    if v == "":
                        v = 0
                    else:
                        v = int(v)

        if type_ == "double":
            if self.editor_:
                ed_ = self.editor_
                if isinstance(ed_, FLLineEdit):
                    v = ed_.text()
                    if v == "":
                        v = 0.00
                    else:
                        v = float(v)

        elif type_ == "serial":
            if self.editor_:
                ed_ = self.editor_
                if isinstance(ed_, FLSpinBox):
                    v = ed_.value()

        elif type_ == "pixmap":
            v = self.cursor_.valueBuffer(self.fieldName_)

        elif type_ == "date":
            if self.editor_:
                v = self.editor_.date
                if v:
                    from pineboolib.application.types import Date

                    v = Date(v)

        elif type_ == "time":
            if self.editor_:
                v = self.editor_.time

        elif type_ == "bool":
            if self.editor_:
                v = self.editor_.isChecked()

        # v.cast(fltype)
        return v

    """
    Marca como seleccionado el contenido del campo.
    """

    def selectAll(self) -> None:
        if not self.cursor_:
            return

        if not self.cursor_.metadata():
            return

        field = self.cursor_.metadata().field(self.fieldName_)
        if field is None:
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

    def cursor(self) -> FLSqlCursor:
        return self.cursor_

    """
    Devuelve el valor de la propiedad showAlias. Esta propiedad es
    usada para saber si hay que mostrar el alias cuando se está
    en modo de cursor relacionado.
    """

    def showAlias(self) -> bool:
        return self.showAlias_

    """
    Establece el estado de la propiedad showAlias.
    """

    def setShowAlias(self, value: bool) -> None:
        if not self.showAlias_ == value:
            self.showAlias_ = value
            if self.textLabelDB:
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
    def insertAccel(self, key: str):  # FIXME
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
    def removeAccel(self, identifier: str):  # FIXME
        if not self.accel_:
            return
        self.accel_.removeItem(identifier)

    """
    Establece la capacidad de mantener el componente deshabilitado ignorando posibles
    habilitaciones por refrescos. Ver FLFieldDB::keepDisabled_ .

    @param keep TRUE para activar el mantenerse deshabilitado y FALSE para desactivar
    """

    def setKeepDisabled(self, keep: bool) -> None:
        self.keepDisabled_ = keep

    """
    Devuelve el valor de la propiedad showEditor.
    """

    def showEditor(self) -> bool:
        return self.showEditor_

    """
    Establece el valor de la propiedad showEditor.
    """

    def setShowEditor(self, show: bool) -> None:
        self.showEditor_ = show
        ed = QtWidgets.QWidget()
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

    def setPartDecimal(self, d: int) -> None:
        self._partDecimal = d
        self.refreshQuick(self.fieldName_)
        # self.editor_.setText(self.editor_.text(),False)

    """
    Para asistente de completado automático.
    """

    def setAutoCompletionMode(self, m: str) -> None:
        self.autoCompMode_ = m

    def autoCompletionMode(self) -> str:
        return self.autoCompMode_

    """
    Refresca el contenido del campo con los valores del cursor de la tabla origen.

    Si se indica el nombre de un campo sólo "refresca" si el campo indicado
    coincide con la propiedad fieldRelation, tomando como filtro el valor del campo
    fieldRelation de la tabla relacionada. Si no se indica nigún nombre de
    campo el refresco es llevado a cabo siempre.

    @param fN Nombre de un campo
    """

    @decorators.pyqtSlot()
    @decorators.pyqtSlot("QString")
    def refresh(self, fN: Optional[str] = None) -> None:
        if not self.cursor_ or not isinstance(self.cursor_, FLSqlCursor):
            self.logger.debug("FLField.refresh() Cancelado")
            return
        tMD = self.cursor_.metadata()
        if not tMD:
            return

        v = None
        nulo = False
        if not fN:
            v = self.cursor_.valueBuffer(self.fieldName_)
            if self.fieldRelation_ is not None:
                nulo = self.cursor_.bufferIsNull(self.fieldRelation_)

            # if self.cursor_.cursorRelation():
            # print(1)
            # if self.cursor_.cursorRelation().valueBuffer(self.fieldRelation_) in ("", None):
            # FIXME: Este código estaba provocando errores al cargar formRecord hijos
            # ... el problema es, que posiblemente el cursorRelation entrega información
            # ... errónea, y aunque comentar el código soluciona esto, seguramente esconde
            # ... otros errores en el cursorRelation. Pendiente de investigar más.
            # v = None
            # if DEBUG: print("FLFieldDB: valueBuffer padre vacío.")

        else:
            if not self.fieldRelation_:
                raise ValueError("fieldRelation_ is not defined!")

            if not self.cursorAux and fN.lower() == self.fieldRelation_.lower():
                if self.cursor_.bufferIsNull(self.fieldRelation_):
                    return

                field = tMD.field(self.fieldRelation_)
                if field is None:
                    return

                relation_m1 = field.relationM1()
                if relation_m1 is None:
                    return

                tmd = FLSqlCursor(relation_m1.foreignTable()).metadata()
                if tmd is None:
                    return

                # if self.topWidget_ and not self.topWidget_.isShown() and not self.cursor_.modeAccess() == FLSqlCursor.Insert:
                #    return

                if field is None:
                    return

                if not field.relationM1():
                    self.logger.info(
                        "FLFieldDB :El campo de la relación debe estar relacionado en M1"
                    )
                    return

                v = self.cursor_.valueBuffer(self.fieldRelation_)
                q = FLSqlQuery()
                q.setForwardOnly(True)
                relation_m1 = field.relationM1()
                if relation_m1 is None:
                    raise ValueError("relationM1 does not exist!")

                q.setTablesList(relation_m1.foreignTable())
                q.setSelect("%s,%s" % (self.foreignField(), relation_m1.foreignField()))
                q.setFrom(relation_m1.foreignTable())
                where = field.formatAssignValue(relation_m1.foreignField(), v, True)
                filterAc = self.cursor_.filterAssoc(self.fieldRelation_, tmd)
                if filterAc:
                    if not where:
                        where = filterAc
                    else:
                        where += " AND %s" % filterAc

                # if not self.filter_:
                #    q.setWhere(where)
                # else:
                #    q.setWhere(str(self.filter_ + " AND " + where))
                if self.filter_:
                    where = "%s AND %s" % (self.filter_, where)

                q.setWhere(where)
                if q.exec_() and q.next():
                    v0 = q.value(0)
                    v1 = q.value(1)
                    if not v0 == self.value():
                        self.setValue(v0)
                    if not v1 == v:
                        self.cursor_.setValueBuffer(self.fieldRelation_, v1)

            return

        field = tMD.field(str(self.fieldName_))
        if field is None:
            return
        type_ = field.type()

        if not type_ == "pixmap" and not self.editor_ and fN is not None:
            self._refreshLaterEditor = fN
            return

        modeAcces = self.cursor_.modeAccess()
        partDecimal = None
        if self._partDecimal:
            partDecimal = self._partDecimal
        else:
            partDecimal = field.partDecimal() or 0
            self._partDecimal = field.partDecimal()

        ol = field.hasOptionsList()

        fDis = False

        # if isinstance(v , QString): #Para quitar
        # v = str(v)
        if self.DEBUG:
            self.logger.info(
                "FLFieldDB:: refresh fN:%r fieldName:%r v:%s" % (fN, self.fieldName_, repr(v)[:64])
            )

        if (
            self.keepDisabled_
            or self.cursor_.fieldDisabled(self.fieldName_)
            or (
                modeAcces == FLSqlCursor.Edit
                and (field.isPrimaryKey() or tMD.fieldListOfCompoundKey(self.fieldName_))
            )
            or not field.editable()
            or modeAcces == FLSqlCursor.Browse
        ):
            fDis = True

        self.setEnabled(not fDis)

        if type_ == "double":
            try:
                self.editor_.textChanged.disconnect(self.updateValue)
            except Exception:
                self.logger.debug("Error al desconectar señal textChanged", exc_info=True)
            s = None
            if nulo and v in (None, 0):
                dv = field.defaultValue()
                if field.allowNull():
                    if dv is None:
                        self.editor_.setText("")
                    else:
                        self.editor_.setText(dv)
                else:
                    if dv is not None:
                        self.editor_.setText(dv)

            else:
                if v is None:
                    v = 0.0
                s = str(round(float(v), partDecimal))
                pos_dot = s.find(".")

                if pos_dot is not None and pos_dot > -1:
                    while len(s[pos_dot + 1 :]) < partDecimal:
                        s = "%s0" % s
                self.editor_.setText(s)

            self.editor_.textChanged.connect(self.updateValue)

            # if v == None and not nulo:
            #    self.editor_.setText("0.00")

        elif type_ == "string":
            doHome = False
            if not ol:
                try:
                    self.editor_.textChanged.disconnect(self.updateValue)
                except Exception:
                    self.logger.exception("Error al desconectar señal textChanged")

            if v is not None:
                if ol:
                    if v.find("QT_TRANSLATE") != -1:
                        v = aqtt(v)
                    idx = field.getIndexOptionsList(v)
                    if idx is not None:
                        self.editor_.setCurrentIndex(idx)
                else:
                    self.editor_.setText(v)
            else:
                if ol:
                    self.editor_.setCurrentIndex(0)
                elif not nulo:
                    self.editor_.setText(field.defaultValue())
                else:
                    self.editor_.setText("")

            if not ol and doHome:
                self.editor_.home(False)

            if not ol:
                self.editor_.textChanged.connect(self.updateValue)

        elif type_ in ("int", "uint"):
            try:
                self.editor_.textChanged.disconnect(self.updateValue)
            except Exception:
                self.logger.exception("Error al desconectar señal textChanged")

            if nulo and v in (None, 0):
                dv = field.defaultValue()
                if field.allowNull():
                    if dv is None:
                        self.editor_.setText("")
                    else:
                        self.editor_.setText(dv)
                else:
                    if dv is not None:
                        self.editor_.setText(dv)
            else:
                if v in (None, 0):
                    self.editor_.setText("")
                else:
                    self.editor_.setText(v)

            self.editor_.textChanged.connect(self.updateValue)

        elif type_ == "serial":
            try:
                self.editor_.textChanged.disconnect(self.updateValue)
            except Exception:
                self.logger.exception("Error al desconectar señal textChanged")
            self.editor_.setText(str(0))

            self.editor_.textChanged.connect(self.updateValue)

        elif type_ == "pixmap":
            if not self.editorImg_:
                from pineboolib.fllegacy.flpixmapview import FLPixmapView

                self.editorImg_ = FLPixmapView(self)
                self.editorImg_.setFocusPolicy(Qt.NoFocus)
                self.editorImg_.setSizePolicy(self.sizePolicy())
                self.editorImg_.setMaximumSize(147, 24)
                # self.editorImg_.setMinimumSize(self.minimumSize())
                self.editorImg_.setAutoScaled(True)
                # self.FLWidgetFieldDBLayout.removeWidget(self.pushButtonDB)
                if self.FLWidgetFieldDBLayout is None:
                    raise Exception("FLWidgetFieldDBLayout is empty!")
                self.FLWidgetFieldDBLayout.addWidget(self.editorImg_)
                self.pushButtonDB.hide()

                if field.visible():
                    self.editorImg_.show()
                else:
                    return
                # else:
            # if modeAcces == FLSqlCursor.Browse:
            if field.visible():
                # cs = QString()
                if not v:
                    self.editorImg_.clear()
                    return
                    # cs = v.toString()
                # if cs.isEmpty():
                #    self.editorImg_.clear()
                #    return
                if isinstance(v, str):
                    if v.find("static char") > -1:
                        from pineboolib.application.utils.xpm import cacheXPM

                        v = cacheXPM(v)

                pix = QtGui.QPixmap(v)
                # if not QtGui.QPixmapCache.find(cs.left(100), pix):
                # pix.loadFromData()
                # QtGui.QPixmapCache.insert(cs.left(100), pix)

                if pix:
                    self.editorImg_.setPixmap(pix)
                else:
                    self.editorImg_.clear()

            # if modeAcces == FLSqlCursor.Browse:
            # self.pushButtonDB.setVisible(False)

        elif type_ == "date":
            if self.cursor_.modeAccess() == FLSqlCursor.Insert and nulo and not field.allowNull():
                defVal = field.defaultValue()
                if defVal is not None:
                    defVal = QtCore.QDate.fromString(str(defVal))
                else:
                    defVal = QtCore.QDate.currentDate()

                self.editor_.setDate(defVal)
                self.updateValue(defVal)

            else:
                try:
                    self.editor_.dateChanged.disconnect(self.updateValue)
                except Exception:
                    self.logger.exception("Error al desconectar señal textChanged")

                if v:
                    util = FLUtil()
                    v = util.dateDMAtoAMD(v)
                    self.editor_.setDate(v)
                else:
                    self.editor_.setDate()

                self.editor_.dateChanged.connect(self.updateValue)

        elif type_ == "time":
            if self.cursor_.modeAccess() == FLSqlCursor.Insert and nulo and not field.allowNull():
                defVal = field.defaultValue()
                if defVal is not None:
                    defVal = QtCore.QTime.fromString(str(defVal))
                else:
                    defVal = QtCore.QTime.currentTime()

                self.editor_.setTime(defVal)
                self.updateValue(defVal)

            else:
                try:
                    self.editor_.timeChanged.disconnect(self.updateValue)
                except Exception:
                    self.logger.exception("Error al desconectar señal timeChanged")

                if v is not None:
                    self.editor_.setTime(v)

                self.editor_.timeChanged.connect(self.updateValue)

        elif type_ == "stringlist":
            try:
                self.editor_.textChanged.disconnect(self.updateValue)
            except Exception:
                self.logger.exception("Error al desconectar señal timeChanged")
            if v is not None:
                self.editor_.setText(v)
            else:
                self.editor_.setText(field.defaultValue())
            self.editor_.textChanged.connect(self.updateValue)

        elif type_ == "bool":
            try:
                self.editor_.toggled.disconnect(self.updateValue)
            except Exception:
                self.logger.exception("Error al desconectar señal toggled")

            if v is not None:

                self.editor_.setChecked(v)
            else:
                dV = field.defaultValue()
                if dV is not None:
                    self.editor_.setChecked(dV)

            self.editor_.toggled.connect(self.updateValue)

        if not field.visible():
            if self.editor_:
                self.editor_.hide()
            elif self.editorImg_:
                self.editorImg_.hide()
            self.setEnabled(False)

    """
    Refresco rápido
    """

    @decorators.pyqtSlot("QString")
    def refreshQuick(self, fN: Optional[str] = None) -> None:
        if not fN or not fN == self.fieldName_ or not self.cursor_:
            return

        tMD = self.cursor_.metadata()
        field = tMD.field(self.fieldName_)

        if field is None:
            return

        if field.outTransaction():
            return

        type_ = field.type()

        if not type_ == "pixmap" and not self.editor_:
            return
        v = self.cursor_.valueBuffer(self.fieldName_)
        nulo = self.cursor_.bufferIsNull(self.fieldName_)

        if self._partDecimal < 0:
            self._partDecimal = field.partDecimal()

        ol = field.hasOptionsList()

        if type_ == "double":

            # part_decimal = self._partDecimal if self._partDecimal > -1 else field.partDecimal()

            e_text = self.editor_.text() if self.editor_.text() != "" else 0.0
            if float(e_text) == float(v):
                return
            try:
                self.editor_.textChanged.disconnect(self.updateValue)
            except Exception:
                self.logger.exception("Error al desconectar señal textChanged")

            if not nulo:
                v = round(v, self._partDecimal)

            self.editor_.setText(v, False)

            self.editor_.textChanged.connect(self.updateValue)

        elif type_ == "string":
            doHome = False
            if ol:
                if str(v) == self.editor_.currentText:
                    return
            else:
                if str(v) == self.editor_.text():
                    return

                if not self.editor_.text():
                    doHome = True

            if not ol:
                self.editor_.textChanged.disconnect(self.updateValue)

            if v:
                if ol:
                    self.editor_.setCurrentText(v)

                else:
                    self.editor_.setText(v, False)

            else:
                if ol:
                    self.editor_.setCurrentIndex(0)

                else:
                    self.editor_.setText("", False)

            if not ol and doHome:
                self.editor_.home(False)

            if not ol:

                self.editor_.textChanged.connect(self.updateValue)

        elif type_ == "uint" or type_ == "int" or type_ == "serial":
            if v == self.editor_.text():
                return
            try:
                self.editor_.textChanged.disconnect(self.updateValue)
            except Exception:
                self.logger.exception("Error al desconectar señal textChanged")

            if not nulo:
                self.editor_.setText(v)

            self.editor_.textChanged.connect(self.updateValue)

        elif type_ == "pixmap":
            if not self.editorImg_:
                self.editorImg_ = FLPixmapView(self)
                self.editorImg_.setFocusPolicy(QtCore.Qt.NoFocus)
                self.editorImg_.setSizePolicy(self.sizePolicy())
                self.editorImg_.setMaximumSize(147, 24)
                # self.editorImg_.setMinimumSize(self.minimumSize())
                self.editorImg_.setAutoScaled(True)
                if self.FLWidgetFieldDBLayout is None:
                    raise Exception("FLWidgetFieldDBLayout is empty!")
                self.FLWidgetFieldDBLayout.addWidget(self.editorImg_)
                if field.visible():
                    self.editorImg_.show()

            if not nulo:
                if not v:
                    self.editorImg_.clear()
                    return

            if isinstance(v, str):
                if v.find("static char") > -1:
                    from pineboolib.application.utils.xpm import cacheXPM

                    v = cacheXPM(v)

            pix = QtGui.QPixmap(v)
            # pix.loadFromData(v)

            if pix.isNull():
                self.editorImg_.clear()
            else:
                self.editorImg_.setPixmap(pix)

        elif type_ == "date":
            if v == self.editor_.date:
                return

            try:
                self.editor_.dateChanged.disconnect(self.updateValue)
            except Exception:
                self.logger.exception("Error al desconectar señal dateChanged")
            self.editor_.setDate(v)
            self.editor_.dateChanged.connect(self.updateValue)

        elif type_ == "time":
            if v == str(self.editor_.time()):
                return

            try:
                self.editor_.timeChanged.disconnect(self.updateValue)
            except Exception:
                self.logger.exception("Error al desconectar señal")

            self.editor_.setTime(v)
            self.editor_.timeChanged.connect(self.updateValue)

        elif type_ == "stringlist":
            if v == str(self.editor_.toPlainText()):
                return

            try:
                self.editor_.textChanged.disconnect(self.updateValue)
            except Exception:
                self.logger.exception("Error al desconectar señal")

            self.editor_.setText(v)
            self.editor_.textChanged.connect(self.updateValue)

        elif type_ == "bool":
            if v == self.editor_.isChecked():
                return

            try:
                self.editor_.toggled.disconnect(self.updateValue)
            except Exception:
                self.logger.exception("Error al desconectar señal")

            self.editor_.setChecked(v)
            self.editor_.toggled.connect(self.updateValue)

    def initCursor(self) -> None:
        """
        Inicia el cursor segun este campo sea de la tabla origen o de
        una tabla relacionada
        """
        if project.conn is None:
            raise Exception("Project is not connected yet")

        if self.tableName_ and not self.foreignField_ and not self.fieldRelation_:
            self.cursorBackup_ = self.cursor_
            if self.cursor_:
                self.cursor_ = FLSqlCursor(
                    self.tableName_, True, project.conn.db().connectionName(), None, None, self
                )
            else:
                if not self.topWidget_:
                    return
                self.cursor_ = FLSqlCursor(
                    self.tableName_,
                    True,
                    project.conn.database().connectionName(),
                    None,
                    None,
                    self,
                )
            self.cursor_.setModeAccess(FLSqlCursor.Browse)
            if self.showed:
                try:
                    self.cursor_.cursorUpdated.disconnect(self.refresh)
                except Exception:
                    self.logger.exception("Error al desconectar señal")
            self.cursor_.cursorUpdated.connect(self.refresh)
            return
        else:
            if self.cursorBackup_:
                try:
                    self.cursor_.cursorUpdated.disconnect(self.refresh)
                except Exception:
                    self.logger.exception("Error al desconectar señal")
                self.cursor_ = self.cursorBackup_
                self.cursorBackup_ = False

        if not self.cursor_:
            return

        if not self.tableName_ or not self.foreignField_ or not self.fieldRelation_:
            if self.foreignField_ and self.fieldRelation_:
                if self.showed:
                    try:
                        self.cursor_.bufferChanged.disconnect(self.refresh)
                    except Exception:
                        self.logger.exception("Error al desconectar señal")
                self.cursor_.bufferChanged.connect(self.refresh)

            if self.showed:
                try:
                    self.cursor_.newBuffer.disconnect(self.refresh)
                except Exception:
                    self.logger.exception("Error al desconectar señal")

                try:
                    self.cursor_.bufferChanged.disconnect(self.refreshQuick)
                except Exception:
                    self.logger.exception("Error al desconectar señal")

            self.cursor_.newBuffer.connect(self.refresh)
            self.cursor_.bufferChanged.connect(self.refreshQuick)
            return

        tMD = self.cursor_.db().manager().metadata(self.tableName_)
        if not tMD:
            return

        try:
            self.cursor_.newBuffer.disconnect(self.refresh)
        except TypeError:
            pass

        try:
            self.cursor_.bufferChanged.disconnect(self.refreshQuick)
        except TypeError:
            pass

        self.cursorAux = self.cursor()
        if not self.cursor().metadata():
            return

        curName = self.cursor().metadata().name()

        rMD = tMD.relation(self.fieldRelation_, self.foreignField_, curName)
        if not rMD:
            checkIntegrity = False
            testM1 = self.cursor_.metadata().relation(
                self.foreignField_, self.fieldRelation_, self.tableName_
            )
            if testM1:
                if testM1.cardinality() == PNRelationMetaData.RELATION_1M:
                    checkIntegrity = True
            fMD = tMD.field(self.fieldRelation_)

            if fMD is not None:
                rMD = PNRelationMetaData(
                    curName,
                    self.foreignField_,
                    PNRelationMetaData.RELATION_1M,
                    False,
                    False,
                    checkIntegrity,
                )

                fMD.addRelationMD(rMD)
                self.logger.trace(
                    "FLFieldDB : La relación entre la tabla del formulario ( %s ) y la tabla ( %s ) de este campo ( %s ) no existe, "
                    "pero sin embargo se han indicado los campos de relación( %s, %s)",
                    curName,
                    self.tableName_,
                    self.fieldName_,
                    self.fieldRelation_,
                    self.foreignField_,
                )
                self.logger.trace(
                    "FLFieldDB : Creando automáticamente %s.%s --1M--> %s.%s",
                    self.tableName_,
                    self.fieldRelation_,
                    curName,
                    self.foreignField_,
                )
            else:
                self.logger.trace(
                    "FLFieldDB : El campo ( %s ) indicado en la propiedad fieldRelation no se encuentra en la tabla ( %s )",
                    self.fieldRelation_,
                    self.tableName_,
                )

        if self.tableName_:
            # self.cursor_ = FLSqlCursor(self.tableName_)
            self.cursor_ = FLSqlCursor(
                self.tableName_, False, self.cursor_.connectionName(), self.cursorAux, rMD, self
            )

        if not self.cursor_:
            self.cursor_ = self.cursorAux
            if self.showed:
                try:
                    self.cursor_.newBuffer.disconnect(self.refresh)
                except Exception:
                    self.logger.exception("Error al desconectar señal")

                try:
                    self.cursor_.bufferChanged.disconnect(self.refreshQuick)
                except Exception:
                    self.logger.exception("Error al desconectar señal")

            self.cursor_.newBuffer.connect(self.refresh)
            self.cursor_.bufferChanged.connect(self.refreshQuick)
            self.cursorAux = None
            return
        else:
            if self.showed:
                try:
                    self.cursor_.newBuffer.disconnect(self.setNoShowed)
                except Exception:
                    self.logger.exception("Error al desconectar señal")
            self.cursor_.newBuffer.connect(self.setNoShowed)

        self.cursor_.setModeAccess(FLSqlCursor.Browse)
        if self.showed:
            try:
                self.cursor_.newBuffer.disconnect(self.refresh)
            except Exception:
                self.logger.exception("Error al desconectar señal")

            try:
                self.cursor_.bufferChanged.disconnect(self.refreshQuick)
            except Exception:
                self.logger.exception("Error al desconectar señal")

        self.cursor_.newBuffer.connect(self.refresh)
        self.cursor_.bufferChanged.connect(self.refreshQuick)

        # self.cursor_.append(self.cursor_.db().db().recordInfo(self.tableName_).find(self.fieldName_)) #FIXME
        # self.cursor_.append(self.cursor_.db().db().recordInfo(self.tableName_).find(self.fieldRelation_))
        # #FIXME

    def initEditor(self) -> None:
        """
        Crea e inicia el editor apropiado para editar el tipo de datos
        contenido en el campo (p.e: si el campo contiene una fecha crea
        e inicia un QDataEdit)
        """
        if not self.cursor_:
            return

        # if self.editor_:
        #    del self.editor_
        #    self.editor_ = None

        # if self.editorImg_:
        #    del self.editorImg_
        #    self.editorImg_ = None

        tMD = self.cursor_.metadata()
        if not tMD:
            return

        field = tMD.field(self.fieldName_)
        if field is None:
            return

        type_ = field.type()
        len_ = field.length()
        partInteger = field.partInteger()
        partDecimal = None
        if type_ == "double":
            if self._partDecimal:
                partDecimal = self._partDecimal
            else:
                partDecimal = field.partDecimal()
                self._partDecimal = field.partDecimal()

        rX = field.regExpValidator()
        ol = field.hasOptionsList()

        rt = None
        if field.relationM1():
            if not field.relationM1().foreignTable() == tMD.name():
                rt = field.relationM1().foreignTable()

        hasPushButtonDB = False
        self.fieldAlias_ = field.alias()

        if self.fieldAlias_ is None:
            raise Exception(
                "alias from %s.%s is not defined!" % (field.metadata().name(), field.name())
            )

        if self.textLabelDB:
            self.textLabelDB.setFont(self.font())
            if type_ not in ["pixmap", "bool"]:
                if not field.allowNull() and field.editable():
                    self.textLabelDB.setText("%s*" % self.fieldAlias_)
                else:
                    self.textLabelDB.setText(self.fieldAlias_)
            else:
                self.textLabelDB.hide()

        if rt:
            hasPushButtonDB = True
            tmd = self.cursor_.db().manager().metadata(rt)
            if not tmd and self.pushButtonDB:
                self.pushButtonDB.setDisabled(True)
                field.setEditable(False)

            if tmd and not tmd.inCache():
                del tmd

        self.initMaxSize_ = self.maximumSize()
        self.initMinSize_ = self.minimumSize()
        from pineboolib.application import project
        from pineboolib.fllegacy.fllineedit import FLLineEdit
        from pineboolib.fllegacy.fldateedit import FLDateEdit
        from pineboolib.fllegacy.fltimeedit import FLTimeEdit
        from pineboolib.fllegacy.flpixmapview import FLPixmapView

        from pineboolib.qt3_widgets.qpushbutton import QPushButton
        from pineboolib.qt3_widgets.qtextedit import QTextEdit

        if project._DGI and not project.DGI.localDesktop():
            project.DGI._par.addQueque("%s_setType" % self.objectName(), type_)
            if self.showAlias():
                project.DGI._par.addQueque("%s_setAlias" % self.objectName(), self.fieldAlias_)

        if type_ in ("uint", "int", "double", "string"):
            self.initEditorControlForNumber(
                has_option_list=ol,
                field=field,
                type_=type_,
                partDecimal=partDecimal,
                partInteger=partInteger,
                len_=len_,
                rX=rX,
                hasPushButtonDB=hasPushButtonDB,
            )
        elif type_ == "serial":
            self.editor_ = FLLineEdit(self, "editor")
            self.editor_.setFont(self.font())
            self.editor_.setMaxValue(pow(10, field.partInteger()) - 1)
            sizePolicy = QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Policy(7), QtWidgets.QSizePolicy.Policy(0)
            )
            sizePolicy.setHeightForWidth(True)
            self.editor_.setSizePolicy(sizePolicy)
            if self.FLWidgetFieldDBLayout:
                self.FLWidgetFieldDBLayout.addWidget(self.editor_)
            self.editor_.installEventFilter(self)
            self.editor_.setDisabled(True)
            self.editor_.setAlignment(QtCore.Qt.AlignRight)
            if self.pushButtonDB:
                self.pushButtonDB.hide()

            if self.showed:
                try:
                    self.editor_.textChanged.disconnect(self.updateValue)
                except Exception:
                    self.logger.exception("Error al desconectar señal")
            self.editor_.textChanged.connect(self.updateValue)

        elif type_ == "pixmap":
            # if not self.cursor_.modeAccess() == FLSqlCursor.Browse:
            if not self.tableName():
                if not self.editorImg_ and self.FLWidgetFieldDBLayout:
                    self.FLWidgetFieldDBLayout.setDirection(QtWidgets.QBoxLayout.Down)
                    self.editorImg_ = FLPixmapView(self)
                    self.editorImg_.setFocusPolicy(Qt.NoFocus)
                    self.editorImg_.setSizePolicy(self.sizePolicy())
                    self.editorImg_.setMaximumSize(self.maximumSize())
                    self.editorImg_.setMinimumSize(self.minimumSize())
                    if self.iconSize:
                        self.setMinimumHeight(self.iconSize.height() + self.minimumHeight() + 1)
                        self.setMinimumWidth(self.iconSize.width() * 4)
                    self.editorImg_.setAutoScaled(True)
                    self.FLWidgetFieldDBLayout.removeWidget(self.pushButtonDB)
                    self.FLWidgetFieldDBLayout.addWidget(self.editorImg_)

                if self.textLabelDB:
                    self.textLabelDB.hide()

                sizePolicy = QtWidgets.QSizePolicy(
                    QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
                )
                # sizePolicy.setHeightForWidth(True)

                if not self.pbAux3_:
                    spcBut = QtWidgets.QSpacerItem(
                        20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
                    )
                    self.lytButtons.addItem(spcBut)
                    self.pbAux3_ = QPushButton(self)
                    if self.pbAux3_:
                        self.pbAux3_.setSizePolicy(sizePolicy)
                        self.pbAux3_.setMinimumSize(self.iconSize)
                        self.pbAux3_.setFocusPolicy(Qt.NoFocus)
                        self.pbAux3_.setIcon(QtGui.QIcon(filedir("../share/icons", "gtk-open.png")))
                        self.pbAux3_.setText("")
                        self.pbAux3_.setToolTip("Abrir fichero de imagen")
                        self.pbAux3_.setWhatsThis("Abrir fichero de imagen")
                        self.lytButtons.addWidget(self.pbAux3_)
                        # if self.showed:
                        #    try:
                        #        self.pbAux3_.clicked.disconnect(self.searchPixmap)
                        #    except Exception:
                        #        self.logger.exception("Error al desconectar señal")
                        self.pbAux3_.clicked.connect(self.searchPixmap)
                        if not hasPushButtonDB:
                            if self.showed:
                                try:
                                    self.KeyF2Pressed.disconnect(self.pbAux3_.animateClick)
                                except Exception:
                                    self.logger.exception("Error al desconectar señal")
                            try:
                                self.keyF2Pressed.connect(self.pbAux3_.animateClick)
                            except Exception:
                                self.logger.exception("Error al desconectar señal")

                        self.pbAux3_.setFocusPolicy(Qt.StrongFocus)
                        self.pbAux3_.installEventFilter(self)

                if not self.pbAux4_:
                    self.pbAux4_ = QPushButton(self)
                    if self.pbAux4_:
                        self.pbAux4_.setSizePolicy(sizePolicy)
                        self.pbAux4_.setMinimumSize(self.iconSize)
                        self.pbAux4_.setFocusPolicy(Qt.NoFocus)
                        self.pbAux4_.setIcon(
                            QtGui.QIcon(filedir("../share/icons", "gtk-paste.png"))
                        )
                        self.pbAux4_.setText("")
                        self.pbAux4_.setToolTip("Pegar imagen desde el portapapeles")
                        self.pbAux4_.setWhatsThis("Pegar imagen desde el portapapeles")
                        self.lytButtons.addWidget(self.pbAux4_)
                        # if self.showed:
                        #    try:
                        #        self.pbAux4_.clicked.disconnect(self.setPixmapFromClipboard)
                        #    except Exception:
                        #        self.logger.exception("Error al desconectar señal")
                        self.pbAux4_.clicked.connect(self.setPixmapFromClipboard)

                if not self.pbAux_:
                    self.pbAux_ = QPushButton(self)
                    if self.pbAux_:
                        self.pbAux_.setSizePolicy(sizePolicy)
                        self.pbAux_.setMinimumSize(self.iconSize)
                        self.pbAux_.setFocusPolicy(Qt.NoFocus)
                        self.pbAux_.setIcon(QtGui.QIcon(filedir("../share/icons", "gtk-clear.png")))
                        self.pbAux_.setText("")
                        self.pbAux_.setToolTip("Borrar imagen")
                        self.pbAux_.setWhatsThis("Borrar imagen")
                        self.lytButtons.addWidget(self.pbAux_)
                        # if self.showed:
                        #    try:
                        #        self.pbAux_.clicked.disconnect(self.clearPixmap)
                        #    except Exception:
                        #        self.logger.exception("Error al desconectar señal")
                        self.pbAux_.clicked.connect(self.clearPixmap)

                if not self.pbAux2_:
                    self.pbAux2_ = QPushButton(self)
                    if self.pbAux2_:
                        savepixmap_ = QtWidgets.QMenu(self.pbAux2_)
                        savepixmap_.addAction("JPG")
                        savepixmap_.addAction("XPM")
                        savepixmap_.addAction("PNG")
                        savepixmap_.addAction("BMP")

                        self.pbAux2_.setMenu(savepixmap_)
                        self.pbAux2_.setSizePolicy(sizePolicy)
                        self.pbAux2_.setMinimumSize(self.iconSize)
                        self.pbAux2_.setFocusPolicy(Qt.NoFocus)
                        self.pbAux2_.setIcon(QtGui.QIcon(filedir("../share/icons", "gtk-save.png")))
                        self.pbAux2_.setText("")
                        self.pbAux2_.setToolTip("Guardar imagen como...")
                        self.pbAux2_.setWhatsThis("Guardar imagen como...")
                        self.lytButtons.addWidget(self.pbAux2_)
                        # if self.showed:
                        #    try:
                        #        savepixmap_.triggered.disconnect(self.savePixmap)
                        #    except Exception:
                        #        self.logger.exception("Error al desconectar señal")
                        triggered = cast(pyqtSignal, savepixmap_.triggered)
                        triggered.connect(self.savePixmap)

                    if self.pushButtonDB:
                        if hasPushButtonDB:
                            self.pushButtonDB.installEventFilter(self)
                        else:
                            self.pushButtonDB.setDisabled(True)

        elif type_ == "date":
            self.editor_ = FLDateEdit(self, "editor")
            self.editor_.setFont(self.font())
            sizePolicy = QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed
            )
            sizePolicy.setHeightForWidth(True)
            self.editor_.setSizePolicy(sizePolicy)
            if self.FLWidgetFieldDBLayout:
                self.FLWidgetFieldDBLayout.insertWidget(1, self.editor_)

            # self.editor_.setOrder(QtGui.QDateEdit.DMY)
            # self.editor_.setAutoAdvance(True)
            # self.editor_.setSeparator("-")
            self.editor_.installEventFilter(self)
            if self.pushButtonDB:
                self.pushButtonDB.hide()

            if not self.cursor_.modeAccess() == FLSqlCursor.Browse:
                # if not self.pbAux_:
                #    #self.pbAux_ = QtGui.QPushButton(self)
                #    # self.pbAux_.setFlat(True)
                #    #sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7) ,QtGui.QSizePolicy.Policy(0))
                #    # sizePolicy.setHeightForWidth(True)
                #    # self.pbAux_.setSizePolicy(sizePolicy)
                #    #self.pbAux_.setMinimumSize(25, 25)
                #    #self.pbAux_.setMaximumSize(25, 25)
                #    # self.pbAux_.setFocusPolicy(Qt.NoFocus)
                #    # self.pbAux_.setIcon(QtGui.QIcon(filedir("../share/icons","date.png")))
                #    # self.pbAux_.setText("")
                #    #self.pbAux_.setToolTip("Seleccionar fecha (F2)")
                #    #self.pbAux_.setWhatsThis("Seleccionar fecha (F2)")
                #    # self.lytButtons.addWidget(self.pbAux_) FIXME
                #    # self.FLWidgetFieldDBLayout.addWidget(self.pbAux_)
                #    # if self.showed:
                #        # self.pbAux_.clicked.disconnect(self.toggleDatePicker)
                #        # self.KeyF2Pressed_.disconnect(self.pbAux_.animateClick)
                #    # self.pbAux_.clicked.connect(self.toggleDatePicker)
                #    # self.keyF2Pressed_.connect(self.pbAux_.animateClick) #FIXME
                self.editor_.setCalendarPopup(True)

            if self.showed:
                try:
                    cast(pyqtSignal, self.editor_.dateChanged).disconnect(self.updateValue)
                except Exception:
                    self.logger.exception("Error al desconectar señal")

            cast(pyqtSignal, self.editor_.dateChanged).connect(self.updateValue)
            if self.cursor_.modeAccess() == FLSqlCursor.Insert and not field.allowNull():
                defVal = field.defaultValue()
                # if not defVal.isValid() or defVal.isNull():
                if not defVal:
                    self.editor_.setDate(QtCore.QDate.currentDate())
                else:
                    self.editor_.setDate(defVal.toDate())

        elif type_ == "time":
            self.editor_ = FLTimeEdit(self)
            self.editor_.setFont(self.font())
            # self.editor_.setAutoAdvance(True)
            sizePolicy = QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed
            )
            sizePolicy.setHeightForWidth(True)
            self.editor_.setSizePolicy(sizePolicy)
            if self.FLWidgetFieldDBLayout:
                self.FLWidgetFieldDBLayout.addWidget(self.editor_)
            self.editor_.installEventFilter(self)
            if self.pushButtonDB:
                self.pushButtonDB.hide()
            if self.showed:
                try:
                    cast(pyqtSignal, self.editor_.timeChanged).disconnect(self.updateValue)
                except Exception:
                    self.logger.exception("Error al desconectar señal")

            cast(pyqtSignal, self.editor_.timeChanged).connect(self.updateValue)
            if self.cursor_.modeAccess() == FLSqlCursor.Insert and not field.allowNull():
                defVal = field.defaultValue()
                # if not defVal.isValid() or defVal.isNull():
                if not defVal:
                    self.editor_.setTime(QtCore.QTime.currentTime())
                else:
                    self.editor_.setTime(defVal.toTime())

        elif type_ == "stringlist":

            self.editor_ = QTextEdit(self)
            self.editor_.setFont(self.font())
            self.editor_.setTabChangesFocus(True)
            self.editor_.setMinimumHeight(100)
            self.editor_.setMaximumHeight(120)
            sizePolicy = QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding
            )
            sizePolicy.setHeightForWidth(True)
            self.editor_.setSizePolicy(sizePolicy)
            # ted.setTexFormat(self.textFormat_)
            # if isinstance(self.textFormat_, Qt.RichText) and not self.cursor_.modeAccess() == FLSqlCursor.Browse:
            # self.FLWidgetFieldDBLayout.setDirection(QtGui.QBoxLayout.Down)
            # self.FLWidgetFieldDBLayout.remove(self.textLabelDB)
            # textEditTab_ = AQTextEditBar(self, "extEditTab_", self.textLabelDB) #FIXME
            # textEditTab_.doConnections(ted)
            # self.FLWidgetFieldDBLayout.addWidget(textEditTab_)
            self.setMinimumHeight(130)
            if self.FLWidgetFieldDBLayout:
                self.FLWidgetFieldDBLayout.addWidget(self.editor_)
            verticalSpacer = QtWidgets.QSpacerItem(
                20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
            )
            self.FLLayoutH.addItem(verticalSpacer)
            self.editor_.installEventFilter(self)

            if self.showed:
                try:
                    cast(pyqtSignal, self.editor_.textChanged).disconnect(self.updateValue)
                except Exception:
                    self.logger.exception("Error al desconectar señal")

            cast(pyqtSignal, self.editor_.textChanged).connect(self.updateValue)

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

        elif type_ == "bool":
            from pineboolib.qt3_widgets.qcheckbox import QCheckBox

            self.editor_ = QCheckBox(self)
            # self.editor_.setName("editor")
            self.editor_.setText(tMD.fieldNameToAlias(self.fieldName_))
            self.editor_.setFont(self.font())
            self.editor_.installEventFilter(self)

            self.editor_.setMinimumWidth(
                self.fontMetrics().width(tMD.fieldNameToAlias(self.fieldName()))
                + self.fontMetrics().maxWidth() * 2
            )
            sizePolicy = QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Policy(7), QtWidgets.QSizePolicy.Policy(0)
            )
            sizePolicy.setHeightForWidth(True)
            self.editor_.setSizePolicy(sizePolicy)
            if self.FLWidgetFieldDBLayout:
                self.FLWidgetFieldDBLayout.addWidget(self.editor_)

            if self.showed:
                try:
                    self.editor_.toggled.disconnect(self.updateValue)
                except Exception:
                    self.logger.exception("Error al desconectar señal")
            self.editor_.toggled.connect(self.updateValue)

        if self.editor_:
            self.editor_.setFocusPolicy(Qt.StrongFocus)
            self.setFocusProxy(self.editor_)

            if hasPushButtonDB:
                if self.pushButtonDB:
                    self.setTabOrder(self.pushButtonDB, self.editor_)
                    self.pushButtonDB.setFocusPolicy(Qt.NoFocus)
                self.editor_.setToolTip("Para buscar un valor en la tabla relacionada pulsar F2")
                self.editor_.setWhatsThis("Para buscar un valor en la tabla relacionada pulsar F2")

        elif self.editorImg_:
            self.editorImg_.setFocusPolicy(Qt.NoFocus)
            if hasPushButtonDB:
                if self.pushButtonDB:
                    self.pushButtonDB.setFocusPolicy(Qt.StrongFocus)

        if not hasPushButtonDB:
            if self.pushButtonDB:
                self.pushButtonDB.hide()

        if self.initMaxSize_.width() < 80:
            self.setShowEditor(False)
        else:
            self.setShowEditor(self.showEditor_)

        if self._refreshLaterEditor is not None:
            self.refresh(self._refreshLaterEditor)
            self._refreshLaterEditor = None

    def initEditorControlForNumber(
        self,
        has_option_list: bool,
        field,
        type_,
        partDecimal,
        partInteger,
        len_,
        rX,
        hasPushButtonDB,
    ) -> None:
        if has_option_list:
            self.editor_ = QComboBox()
            style_ = self.editor_.styleSheet()
            self.editor_.setParent(self)

            self.editor_.name = "editor"
            self.editor_.setEditable(False)
            # self.editor_.setAutoCompletion(True)
            self.editor_.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
            self.editor_.setMinimumSize(self.iconSize)
            self.editor_.setFont(self.font())
            # if not self.cursor_.modeAccess() == FLSqlCursor.Browse:
            # if not field.allowNull():
            # self.editor_.palette().setColor(self.editor_.backgroundRole(), self.notNullColor())
            # self.editor_.setStyleSheet('background-color:' + self.notNullColor().name())
            if not field.allowNull() and field.editable():
                self.editor_.setStyleSheet(
                    "background-color:%s; color:%s"
                    % (self.notNullColor(), QtGui.QColor(Qt.black).name())
                )
            else:
                self.editor_.setStyleSheet(style_)

            olTranslated = []
            olNoTranslated = field.optionsList()
            for olN in olNoTranslated:
                olTranslated.append(olN)
            self.editor_.addItems(olTranslated)
            if project._DGI and not project.DGI.localDesktop():
                project.DGI._par.addQueque("%s_setOptionsList" % self.objectName(), olTranslated)
            self.editor_.installEventFilter(self)
            if self.showed:
                try:
                    cast(pyqtSignal, self.editor_.activated).disconnect(self.updateValue)
                except Exception:
                    self.logger.exception("Error al desconectar señal")
            cast(pyqtSignal, self.editor_.activated).connect(self.updateValue)

        else:
            from pineboolib.fllegacy.fllineedit import FLLineEdit

            self.editor_ = FLLineEdit(self, "editor")
            self.editor_.setFont(self.font())
            if self.iconSize:
                self.editor_.setMinimumSize(self.iconSize)
                self.editor_.setMaximumHeight(self.iconSize.height())
            self.editor_._tipo = type_
            self.editor_.partDecimal = partDecimal
            if not self.cursor_.modeAccess() == FLSqlCursor.Browse:
                if not field.allowNull() and field.editable() and type_ not in ("time", "date"):
                    # self.editor_.palette().setColor(self.editor_.backgroundRole(), self.notNullColor())
                    self.editor_.setStyleSheet(
                        "background-color:%s; color:%s"
                        % (self.notNullColor(), QtGui.QColor(Qt.black).name())
                    )
                self.editor_.installEventFilter(self)

            if type_ == "double":
                self.editor_.setValidator(
                    FLDoubleValidator(
                        ((pow(10, partInteger) - 1) * -1),
                        pow(10, partInteger) - 1,
                        self.editor_.partDecimal,
                        self.editor_,
                    )
                )
                self.editor_.setAlignment(Qt.AlignRight)
            else:
                if type_ == "uint":
                    self.editor_.setValidator(
                        FLUIntValidator(0, pow(10, partInteger), self.editor_)
                    )
                    pass
                elif type_ == "int":
                    self.editor_.setValidator(
                        FLIntValidator(
                            ((pow(10, partInteger) - 1) * -1),
                            pow(10, partInteger) - 1,
                            self.editor_,
                        )
                    )
                    self.editor_.setAlignment(Qt.AlignRight)
                else:
                    self.editor_.setMaxValue(len_)
                    if rX:
                        self.editor_.setValidator(
                            QtGui.QRegExpValidator(QtCore.QRegExp(rX), self.editor_)
                        )

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

            self.editor_.installEventFilter(self)

            if self.showed:
                try:
                    self.editor_.lostFocus.disconnect(self.emitLostFocus)
                    self.editor_.textChanged.disconnect(self.updateValue)
                    self.editor_.textChanged.disconnect(self.emitTextChanged)
                except Exception:
                    self.logger.exception("Error al desconectar señal")

            self.editor_.lostFocus.connect(self.emitLostFocus)
            self.editor_.textChanged.connect(self.updateValue)
            self.editor_.textChanged.connect(self.emitTextChanged)

            if hasPushButtonDB and self.pushButtonDB:
                if project._DGI and not project.DGI.localDesktop():
                    project.DGI._par.addQueque("%s_setHasPushButton" % self.objectName(), True)
                if self.showed:
                    try:
                        self.KeyF2Pressed.disconnect(self.pushButtonDB.animateClick)
                        self.labelClicked.disconnect(self.openFormRecordRelation)
                    except Exception:
                        self.logger.exception("Error al desconectar señal")

                self.keyF2Pressed.connect(self.pushButtonDB.animateClick)  # FIXME
                self.labelClicked.connect(self.openFormRecordRelation)
                if not self.textLabelDB:
                    raise ValueError("textLabelDB is not defined!")

                self.textLabelDB.installEventFilter(self)
                tlf = self.textLabelDB.font()
                tlf.setUnderline(True)
                self.textLabelDB.setFont(tlf)
                cB = QtGui.QColor(Qt.darkBlue)
                # self.textLabelDB.palette().setColor(self.textLabelDB.foregroundRole(), cB)
                self.textLabelDB.setStyleSheet("color:" + cB.name())
                self.textLabelDB.setCursor(Qt.PointingHandCursor)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy(7), QtWidgets.QSizePolicy.Policy(0)
        )
        sizePolicy.setHeightForWidth(True)
        self.editor_.setSizePolicy(sizePolicy)
        if self.FLWidgetFieldDBLayout is not None:
            self.FLWidgetFieldDBLayout.addWidget(self.pushButtonDB)
            self.FLWidgetFieldDBLayout.addWidget(self.editor_)

    """
    Borra imagen en campos tipo Pixmap.
    """

    def clearPixmap(self) -> None:
        if self.editorImg_:
            self.editorImg_.clear()
            self.cursor_.setValueBuffer(self.fieldName_, None)

    """
    Guarda imagen en campos tipo Pixmap.

    @param fmt Indica el formato con el que guardar la imagen
    """

    @decorators.pyqtSlot(QtWidgets.QAction)
    def savePixmap(self, f: "QPixmap") -> None:
        if self.editorImg_:
            ext = f.text().lower()
            filename = "imagen.%s" % ext
            ext = "*.%s" % ext
            util = FLUtil()
            savefilename = QtWidgets.QFileDialog.getSaveFileName(
                self, util.translate("Pineboo", "Guardar imagen como"), filename, ext
            )
            if savefilename:
                pix = QtGui.QPixmap(self.editorImg_.pixmap())
                QtWidgets.QApplication.setOverrideCursor(Qt.WaitCursor)
                if pix:
                    if not pix.save(savefilename[0]):
                        QtWidgets.QMessageBox.warning(
                            self,
                            util.translate("Pineboo", "Error"),
                            util.translate("Pineboo", "Error guardando fichero"),
                        )

            QtWidgets.QApplication.restoreOverrideCursor()

    """
    Muestra/Oculta el asistente de completado automático.
    """

    @decorators.pyqtSlot()
    def toggleAutoCompletion(self) -> None:
        if self.autoCompMode_ == "NeverAuto":
            return

        if not self.autoComFrame_ and self.cursor():
            self.autoComFrame_ = QWidget(self, Qt.Popup)
            lay = QVBoxLayout()
            self.autoComFrame_.setLayout(lay)
            self.autoComFrame_.setWindowTitle("autoComFrame")
            # self.autoComFrame_->setFrameStyle(QFrame::PopupPanel | QFrame::Raised);
            # self.autoComFrame_->setLineWidth(1);
            self.autoComFrame_.hide()

            if not self.autoComPopup_:
                tMD = self.cursor_.metadata()
                field = tMD.field(self.fieldName_) if tMD else None

                if field:
                    self.autoComPopup_ = FLDataTable(None, "autoComPopup", True)
                    lay.addWidget(self.autoComPopup_)
                    cur = None

                    if not field.relationM1():
                        if self.fieldRelation_ is not None and self.foreignField_ is not None:
                            self.autoComFieldName_ = self.foreignField_

                            fRel = tMD.field(self.fieldRelation_) if tMD else None
                            if not fRel:
                                return

                            self.autoComFieldRelation_ = fRel.relationM1().foreignField()
                            cur = FLSqlCursor(
                                fRel.relationM1().foreignTable(),
                                False,
                                self.cursor_.db().connectionName(),
                                None,
                                None,
                                self.autoComFrame_,
                            )
                            tMD = cur.metadata()
                            field = tMD.field(self.autoCopmFieldName_) if tMD else field
                        else:
                            self.autoComFieldName_ = self.fieldName_
                            self.autoComFieldRelation_ = None
                            cur = FLSqlCursor(
                                tMD.name(),
                                False,
                                self.cursor_.db().connectionName(),
                                None,
                                None,
                                self.autoComFrame_,
                            )

                    else:

                        self.autoComFieldName_ = field.relationM1().foreignField()
                        self.autoComFieldRelation_ = None
                        cur = FLSqlCursor(
                            field.relationM1().foreignTable(),
                            False,
                            self.cursor_.db().connectionName(),
                            None,
                            None,
                            self.autoComFrame_,
                        )
                        tMD = cur.metadata()
                        field = tMD.field(self.autoComFieldName_) if tMD else field

                    # Añade campo al cursor ...    FIXME!!
                    # cur.append(self.autoComFieldName_, field.type(), -1, field.length(), -1)

                    # for fieldNames in tMD.fieldNames().split(","):
                    #    field = tMD.field(fieldNames)
                    #    if field:
                    # cur.append(field.name(), field.type(), -1, field.length(), -1,
                    # "Variant", None, True) #qvariant,0,true

                    if self.autoComFieldRelation_ is not None and self.topWidget_:
                        list1 = self.topWidget_.queryList("FLFieldDB")
                        fdb = None
                        for itf in list1:
                            if itf.fieldName() == self.autoComFieldRelation_:
                                fdb = itf
                                break

                        if fdb and fdb.filter() is not None:
                            cur.setMainFilter(fdb.filter())

                    self.autoComPopup_.setFLSqlCursor(cur)
                    # FIXME
                    # self.autoComPopup_.setTopMargin(0)
                    # self.autoComPopup_.setLeftMargin(0)
                    self.autoComPopup_.horizontalHeader().hide()
                    self.autoComPopup_.verticalHeader().hide()

                    cur.newBuffer.connect(self.autoCompletionUpdateValue)
                    self.autoComPopup_.recordChoosed.connect(self.autoCompletionUpdateValue)

        if self.autoComPopup_:
            cur = self.autoComPopup_.cursor()
            if cur is None:
                raise Exception("Unexpected: No cursor could be obtained")
            tMD = cur.metadata()
            field = tMD.field(self.autoComFieldName_) if tMD else None

            if field:
                filter = (
                    self.cursor().db().manager().formatAssignValueLike(field, self.value(), True)
                )
                self.autoComPopup_.setFilter(filter)
                self.autoComPopup_.setSort("%s ASC" % self.autoComFieldName_)
                self.autoComPopup_.refresh()

            if self.autoComFrame_ is None:
                raise Exception("autoComFrame_ is empty")

            if not self.autoComFrame_.isVisible() and cur.size() > 1:
                tmpPoint = None
                if self.showAlias_ and self.textLabelDB:
                    tmpPoint = self.mapToGlobal(self.textLabelDB.geometry().bottomLeft())
                elif self.pushButtonDB and self.pushButtonDB.isShown():
                    tmpPoint = self.mapToGlobal(self.pushButtonDB.geometry().bottomLeft())
                else:
                    tmpPoint = self.mapToGlobal(self.editor_.geometry().bottonLeft())

                frameWidth = self.width()
                if frameWidth < self.autoComPopup_.width():
                    frameWidth = self.autoComPopup_.width()

                if frameWidth < self.autoComFrame_.width():
                    frameWidth = self.autoComFrame_.width()

                self.autoComFrame_.setGeometry(tmpPoint.x(), tmpPoint.y(), frameWidth, 300)
                self.autoComFrame_.show()
                self.autoComFrame_.setFocus()
            elif self.autoComFrame_.isVisible() and cur.size() == 1:
                self.autoComFrame_.hide()

            cur.first()
            del cur

    """
    Actualiza el valor del campo a partir del contenido que
    ofrece el asistente de completado automático.
    """

    def autoCompletionUpdateValue(self) -> None:
        if not self.autoComPopup_ or not self.autoComFrame_:
            return

        cur = self.autoComPopup_.cursor()
        if not cur or not cur.isValid():
            return

        if isinstance(self.sender(), FLDataTable):
            self.setValue(cur.valueBuffer(self.autoComFieldName_))
            self.autoComFrame_.hide()
            # ifdef Q_OS_WIN32
            # if (editor_)
            #    editor_->releaseKeyboard();
            # if (autoComPopup_)
            #    autoComPopup_->releaseKeyboard();
            # endif
        elif isinstance(self.editor_, QTextEdit):
            self.setValue(self.autoComFieldName_)
        else:
            ed = self.editor_
            if self.autoComFrame_.isVisible() and not ed.hasFocus():
                if not self.autoComPopup_.hasFocus():
                    cval = str(cur.valueBuffer(self.autoComFieldName_))
                    val = ed.text()
                    ed.autoSelect = False
                    ed.setText(cval)
                    ed.setFocus()
                    ed.setCursorPosition(len(cval))
                    ed.cursorBackward(True, len(cval) - len(val))
                    # ifdef Q_OS_WIN32
                    # ed->grabKeyboard();
                    # endif
                else:
                    self.setValue(cur.valueBuffer(self.autoComFieldName_))

            elif not self.autoComFrame_.isVisible():
                cval = str(cur.valueBuffer(self.autoComFieldName_))
                val = ed.text()
                ed.autoSelect = False
                ed.setText(cval)
                ed.setFocus()
                ed.setCursorPosition(len(cval))
                ed.cursorBackward(True, len(cval) - len(val))

        if self.autoComFieldRelation_ is not None and not self.autoComFrame_.isVisible():
            self.cursor_.setValueBuffer(
                self.fieldRelation_, cur.valueBuffer(self.autoComFieldRelation_)
            )

    """
    Abre un formulario de edición para el valor seleccionado en su acción correspondiente
    """

    @decorators.pyqtSlot()
    def openFormRecordRelation(self) -> None:
        if not self.cursor_:
            return

        if not self.fieldName_:
            return

        tMD = self.cursor_.metadata()
        if not tMD:
            return

        field = tMD.field(self.fieldName_)
        if field is None:
            return

        if not field.relationM1():
            self.logger.info("FLFieldDB : El campo de búsqueda debe tener una relación M1")
            return

        fMD = field.associatedField()
        a = None
        v = self.cursor_.valueBuffer(field.name())
        if v in [None, ""] or (fMD is not None and self.cursor_.bufferIsNull(fMD.name())):
            QtWidgets.QMessageBox.warning(
                QtWidgets.QApplication.focusWidget(),
                "Aviso",
                "Debe indicar un valor para %s" % field.alias(),
                QtWidgets.QMessageBox.Ok,
            )
            return

        self.cursor_.db().manager()
        c = FLSqlCursor(field.relationM1().foreignTable(), True, self.cursor_.db().connectionName())
        # c = FLSqlCursor(field.relationM1().foreignTable())
        c.select(
            self.cursor_.db()
            .manager()
            .formatAssignValue(field.relationM1().foreignField(), field, v, True)
        )
        # if c.size() <= 0:
        #    return

        if c.size() <= 0:
            return

        c.next()

        if self.actionName_:
            a = self.actionName_
            if a is None:
                raise Exception("action is empty!")
            c.setAction(a)

        self.modeAccess = self.cursor_.modeAccess()
        if self.modeAccess == FLSqlCursor.Insert or self.modeAccess == FLSqlCursor.Del:
            self.modeAccess = FLSqlCursor.Edit

        c.openFormInMode(self.modeAccess, False)

    """
    Abre un dialogo para buscar en la tabla relacionada
    """

    @decorators.pyqtSlot()
    @decorators.pyqtSlot(int)
    def searchValue(self) -> None:
        if not self.cursor_:
            return

        if not self.fieldName_:
            return
        tMD = self.cursor_.metadata()
        if not tMD:
            return

        field = tMD.field(self.fieldName_)
        if field is None:
            return

        if not field.relationM1():
            self.logger.info("FLFieldDB : El campo de búsqueda debe tener una relación M1")
            return

        fMD = field.associatedField()
        form_search: FLFormSearchDB
        if fMD:
            if not fMD.relationM1():
                self.logger.info("FLFieldDB : El campo asociado debe tener una relación M1")
                return
            v = self.cursor_.valueBuffer(fMD.name())
            if v is None or self.cursor_.bufferIsNull(fMD.name()):
                QtWidgets.QMessageBox.warning(
                    QtWidgets.QApplication.focusWidget(),
                    "Aviso",
                    "Debe indicar un valor para %s" % fMD.alias(),
                )
                return

            mng = self.cursor_.db().manager()
            c = FLSqlCursor(
                fMD.relationM1().foreignTable(), True, self.cursor_.db().connectionName()
            )
            c.select(mng.formatAssignValue(fMD.relationM1().foreignField(), fMD, v, True))
            if c.size() > 0:
                c.first()

            c2 = FLSqlCursor(
                field.relationM1().foreignTable(),
                True,
                self.cursor_.db().connectionName(),
                c,
                fMD.relationM1(),
            )

            # if self.actionName_ is None:
            #    a = mng.action(field.relationM1().foreignTable())
            # else:
            #    a = mng.action(self.actionName_)
            #    if not a:
            #        return
            #    a.setTable(field.relationM1().foreignField())

            form_search = FLFormSearchDB(c2, self.topWidget_)

            form_search.setFilter(
                mng.formatAssignValue(fMD.relationM1().foreignField(), fMD, v, True)
            )
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
            c = FLSqlCursor(a.table(), True, self.cursor_.db().connectionName())
            # f = FLFormSearchDB(c, a.name(), self.topWidget_)
            form_search = FLFormSearchDB(c, self.topWidget_)

        form_search.setMainWidget()

        list_objs = form_search.findChildren(FLTableDB)
        obj_tdb = None

        if list_objs:
            obj_tdb = list_objs[0]
        if fMD and obj_tdb:
            # obj_tdb.setTableName(field.relationM1().foreignTable())
            # obj_tdb.setFieldRelation(field.associatedFieldFilterTo())
            # obj_tdb.setForeignField(fMD.relationM1().foreignField())
            if fMD.relationM1().foreignTable() == tMD.name():
                obj_tdb.setReadOnly(True)

        if self.filter_:
            form_search.setFilter(self.filter_)
        if form_search.mainWidget():
            if obj_tdb:
                cur_value = self.value()
                if field.type() == "string" and cur_value:
                    obj_tdb.setInitSearch(cur_value)
                    obj_tdb.putFisrtCol(field.relationM1().foreignField())

                QtCore.QTimer.singleShot(0, obj_tdb.lineEditSearch, self.setFocus)
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
        v = form_search.exec_(field.relationM1().foreignField())
        form_search.close()
        if c:
            del c
        if v:
            # self.setValue("")
            self.setValue(v)

    """
    Abre un dialogo para buscar un fichero de imagen.

    Si el campo no es de tipo Pixmap no hace nada
    """

    @decorators.pyqtSlot()
    def searchPixmap(self) -> None:
        if not self.cursor_ or not self.editorImg_:
            return

        if not self.fieldName_:
            return
        tMD = PNTableMetaData(self.cursor_.metadata())
        if not tMD:
            return

        field = tMD.field(self.fieldName_)

        if field is None:
            return
        util = FLUtil()
        if field.type() == "pixmap":
            fd = QtWidgets.QFileDialog(
                self.parentWidget(), util.translate("pineboo", "Elegir archivo"), "", "*"
            )
            fd.setViewMode(QtWidgets.QFileDialog.Detail)
            filename = None
            if fd.exec_() == QtWidgets.QDialog.Accepted:
                filename = fd.selectedFiles()

            if not filename:
                return
            self.setPixmap(filename[0])

    """
  Carga una imagen en el campo de tipo pixmap
  @param filename: Ruta al fichero que contiene la imagen
    """

    def setPixmap(self, filename: str) -> None:
        img = QtGui.QImage(filename)

        if not img:
            return

        QtWidgets.QApplication.setOverrideCursor(Qt.WaitCursor)
        pix = QtGui.QPixmap()
        buffer = QtCore.QBuffer()

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
            pix.convertFromImage(img.scaled(newWidth, newHeight))

        QtWidgets.QApplication.restoreOverrideCursor()

        if not pix:
            return

        if self.editorImg_ is None:
            raise Exception("editorImg_ is empty!")

        self.editorImg_.setPixmap(pix)
        QtWidgets.QApplication.setOverrideCursor(Qt.WaitCursor)
        buffer.open(QtCore.QBuffer.ReadWrite)
        pix.save(buffer, "XPM")

        QtWidgets.QApplication.restoreOverrideCursor()

        if not buffer:
            return

        s = str(buffer.data(), "utf-8")

        if s.find("*dummy") > -1:
            s = s.replace(
                "*dummy",
                "%s_%s_%s"
                % (
                    self.cursor().metadata().name(),
                    self.fieldName_,
                    QDateTime().currentDateTime().toString("ddhhmmssz"),
                ),
            )
        self.updateValue(s)

    """
  Carga una imagen en el campo de tipo pixmap con el ancho y alto preferido

  @param pixmap: pixmap a cargar en el campo
  @param w: ancho preferido de la imagen
  @param h: alto preferido de la imagen
  @author Silix
    """

    def setPixmapFromPixmap(self, pixmap: "QPixmap", w: int = 0, h: int = 0) -> None:
        if pixmap.isNull():
            return

        QtWidgets.QApplication.setOverrideCursor(Qt.WaitCursor)
        pix = QtGui.QPixmap()
        buffer = QtCore.QBuffer()

        img = QtGui.QImage(pixmap.convertToImage())
        if not w == 0 and not h == 0:
            pix.convertFromImage(img.scaled(w, h))
        else:
            pix.convertFromImage(img)

        QtWidgets.QApplication.restoreOverrideCursor()
        if not pix:
            return

        if self.editorImg_ is None:
            raise Exception("editorImg_ is empty!")

        self.editorImg_.setPixmap(pix)
        QtWidgets.QApplication.setOverrideCursor(Qt.WaitCursor)
        buffer.open(QtCore.QBuffer.ReadWrite)
        pix.save(buffer, "XPM")

        QtWidgets.QApplication.restoreOverrideCursor()

        if not buffer:
            return
        s = None

        s = str(buffer.data(), "utf-8")

        # if not QtGui.QPixmapCache.find(s.left(100)):
        #    QtGui.QPixmapCache.insert(s.left(100), pix)
        self.updateValue(s)

    """
  Carga una imagen desde el portapapeles en el campo de tipo pixmap
  @author Silix
    """

    def setPixmapFromClipboard(self, unknown: Any) -> None:
        clb = QtWidgets.QApplication.clipboard()
        img = clb.image()

        if not isinstance(img, QtGui.QImage):
            return

        QtWidgets.QApplication.setOverrideCursor(Qt.WaitCursor)
        pix = QtGui.QPixmap()
        buffer = QtCore.QBuffer()

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

            pix.convertFromImage(img.scaled(newWidth, newHeight))

        QtWidgets.QApplication.restoreOverrideCursor()

        if not pix:
            return

        if self.editorImg_ is None:
            raise Exception("editorImg_ is empty!")

        self.editorImg_.setPixmap(pix)
        QtWidgets.QApplication.setOverrideCursor(Qt.WaitCursor)
        buffer.open(QtCore.QBuffer.ReadWrite)
        pix.save(buffer, "XPM")

        QtWidgets.QApplication.restoreOverrideCursor()

        if not buffer:
            return
        s = None

        s = str(buffer.data(), "utf-8")

        # if not QtGui.QPixmapCache.find(s.left(100)):
        #    QtGui.QPixmapCache.insert(s.left(100), pix)
        self.updateValue(s)

    """
  Devueve el objeto imagen asociado al campo

  @return imagen asociada al campo
  @author Silix
    """

    @decorators.NotImplementedWarn
    def pixmap(self) -> "QPixmap":
        pix = QtGui.QPixmap()
        pix.loadFromData(self.value().toCString())
        return pix

    """
    Emite la señal de foco perdido
    """

    def emitLostFocus(self) -> None:
        self.lostFocus.emit()

    """
    Establece que el control no está mostrado
    """

    @decorators.pyqtSlot()
    def setNoShowed(self) -> None:
        if self.foreignField_ and self.fieldRelation_:
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

    @decorators.pyqtSlot(str)
    def setMapValue(self, v=None) -> None:
        if v:
            self.fieldMapValue_ = self.sender()
            self.mapValue_ = v
            self.setMapValue()
        else:
            if not self.fieldMapValue_ or not self.cursor_:
                return
            tMD = self.cursor_.metadata()
            if not tMD:
                return

            fSN = self.fieldMapValue_.fieldName()
            field = tMD.field(self.fieldName_)
            fieldSender = tMD.field(fSN)

            if field is None or not fieldSender:
                return

            if field.relationM1():
                if not field.relationM1().foreignTable() == tMD.name():
                    mng = self.cursor_.db().manager()
                    rt = field.relationM1().foreignTable()
                    fF = self.fieldMapValue_.foreignField()
                    q = FLSqlQuery(None, self.cursor_.db().connectionName())
                    q.setForwardOnly(True)
                    q.setTablesList(rt)
                    q.setSelect("%s,%s" % (field.relationM1().foreignField(), fF))
                    q.setFrom(rt)

                    where = mng.formatAssignValue(fF, fieldSender, self.mapValue_, True)
                    assocTmd = mng.metadata(rt)
                    filterAc = self.cursor_.filterAssoc(fF, assocTmd)
                    if assocTmd and not assocTmd.inCache():
                        del assocTmd

                    if filterAc:
                        if not where:
                            where = filterAc
                        else:
                            where = "%s AND %s" % (where, filterAc)

                    if not self.filter_:
                        q.setWhere(where)
                    else:
                        q.setWhere("%s AND %s" % (self.filter_, where))

                    if q.exec_() and q.next():
                        # self.setValue("")
                        self.setValue(q.value(0))

    """
    Emite la señal de keyF2Pressed.

    La señal key_F2_Pressed del editor (sólo si el editor es FLLineEdit)
    está conectada a este slot.
    """

    @decorators.pyqtSlot()
    def emitKeyF2Pressed(self) -> None:
        self.keyF2Pressed.emit()

    """
    Emite la señal de labelClicked. Se usa en los campos M1 para editar el formulario de edición del valor seleccionado.
    """

    @decorators.pyqtSlot()
    def emitLabelClicked(self) -> None:
        self.labelClicked.emit()

    """
    Emite la señal de textChanged.

    La señal textChanged del editor (sólo si el editor es FLLineEdit)
    está conectada a este slot.
    """

    @decorators.pyqtSlot(str)
    def emitTextChanged(self, t: str) -> None:
        self.textChanged.emit(t)

    """
    Emite la señal activatedAccel( int )
    """

    @decorators.pyqtSlot(int)
    def ActivatedAccel(self, identifier: str) -> None:
        if self.editor_ and self.editor_.hasFocus:
            self.activatedAccel.emit()

    def setDisabled(self, disable: bool) -> None:
        self.setEnabled(not disable)

    """
    Redefinida por conveniencia
    """

    def setEnabled(self, enable: bool) -> None:
        # print("FLFieldDB: %r setEnabled: %r" % (self.fieldName_, enable))
        if self.editor_:
            if not self.cursor():
                self.default_style = self.editor_.styleSheet()
                self.editor_.setDisabled(True)
                self.editor_.setStyleSheet("background-color: #f0f0f0")
            else:

                read_only = getattr(self.editor_, "setReadOnly", None)
                if read_only:
                    tMD = self.cursor_.metadata()
                    field = tMD.field(self.fieldName_)

                    read_only(not enable)
                    if not enable or not field.editable():
                        self.editor_.setStyleSheet("background-color: #f0f0f0")
                    else:
                        if not field.allowNull() and not (
                            field.type() == "time" or field.type() == "date"
                        ):
                            self.editor_.setStyleSheet(
                                "background-color:%s; color:%s"
                                % (self.notNullColor(), QtGui.QColor(Qt.black).name())
                            )
                        elif self.default_style:
                            self.editor_.setStyleSheet(self.default_style)

                else:
                    self.editor_.setEnabled(enable)
        if self.pushButtonDB:
            self.pushButtonDB.setEnabled(enable)
        return  # Mirar esto!! FIXME
        if enable:
            self.setAttribute(Qt.WA_ForceDisabled, False)
        else:
            self.setAttribute(Qt.WA_ForceDisabled, True)

        if (
            not self.isTopLevel()
            and self.parentWidget()
            and not self.parentWidget().isEnabled()
            and enable
        ):
            return

        if enable:
            if self.testAttribute(Qt.WA_Disabled):
                self.setAttribute(Qt.WA_Disabled, False)
                self.enabledChange(not enable)
                if self.children():
                    for w in self.children():
                        if not w.testAttribute(Qt.WA_ForceDisabled):
                            le = w
                            if isinstance(le, QLineEdit):
                                allowNull = True
                                tMD = self.cursor_.metadata()
                                if tMD:
                                    field = tMD.field(self.fieldName_)
                                    if field and not field.allowNull():
                                        allowNull = False

                                if allowNull:
                                    cBg = QtGui.QColor.blue()
                                    cBg = (
                                        QtWidgets.QApplication()
                                        .palette()
                                        .color(QtGui.QPalette.Active, QtGui.QPalette.Base)
                                    )
                                else:
                                    cBg = self.NotNullColor()

                                le.setDisabled(False)
                                le.setReadOnly(False)
                                le.palette().setColor(QtGui.QPalette.Base, cBg)
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
                            if isinstance(w, QLineEdit):
                                le = w
                                if le:
                                    le.setDisabled(False)
                                    le.setReadOnly(True)
                                    le.setCursor(Qt.IBeamCursor)
                                    le.setFocusPolicy(Qt.NoFocus)
                                    continue

                            if isinstance(w, QTextEdit):
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

    def showEvent(self, e: Any) -> None:
        self.load()
        if self._loaded:
            self.showWidget()
        super(FLFieldDB, self).showEvent(e)

    """
    Redefinida por conveniencia
    """

    def showWidget(self) -> None:
        if self._loaded:
            if not self.showed:
                if self.topWidget_:
                    self.showed = True
                    if not self.firstRefresh:
                        self.refresh()
                        self.firstRefresh = True

                    # if self.cursorAux:
                    # print("Cursor auxiliar a ", self.tableName_)
                    if (
                        self.cursorAux
                        and self.cursor_
                        and self.cursor_.bufferIsNull(self.fieldName_)
                    ):

                        if not self.cursorAux.bufferIsNull(self.foreignField_):
                            mng = self.cursor_.db().manager()
                            tMD = self.cursor_.metadata()
                            if tMD:
                                v = self.cursorAux.valueBuffer(self.foreignField_)
                                # print("El valor de %s.%s es %s" % (tMD.name(), self.foreignField_, v))
                                if self.tableName_ is None:
                                    raise ValueError("tableName_ no puede ser Nulo")

                                if self.fieldName_ is None:
                                    raise ValueError("fieldName_ no puede ser Nulo")
                                # FIXME q = FLSqlQuery(False,
                                # self.cursor_.db().connectionName())
                                q = FLSqlQuery(None, self.cursor_.db().connectionName())
                                q.setForwardOnly(True)
                                q.setTablesList(self.tableName_)
                                q.setSelect(self.fieldName_)
                                q.setFrom(self.tableName_)
                                where = mng.formatAssignValue(
                                    tMD.field(self.fieldRelation_), v, True
                                )
                                filterAc = self.cursorAux.filterAssoc(self.foreignField_, tMD)

                                if filterAc:
                                    # print("FilterAC == ", filterAc)
                                    if where not in (None, ""):
                                        where = filterAc
                                    else:
                                        where = "%s AND %s" % (where, filterAc)

                                if not self.filter_:
                                    q.setWhere(where)
                                else:
                                    q.setWhere("%s AND %s" % (self.filter_ + where))

                                # print("where tipo", type(where))
                                # print("Consulta = %s" % q.sql())
                                if q.exec_() and q.first():
                                    value = q.value(0)
                                    if isinstance(value, str):
                                        if value[0:3] == "RK@":
                                            value = self.cursor_.fetchLargeValue(value)
                                    if isinstance(value, datetime.date):
                                        value = value.strftime("%d-%m-%Y")
                                    self.setValue(value)
                                if not tMD.inCache():
                                    del tMD

                else:
                    self.initFakeEditor()

                self.showed = True

    def editor(self) -> Any:
        return self.editor_

    """
    Inicializa un editor falso y no funcional.

    Esto se utiliza cuando se está editando el formulario con el diseñador y no
    se puede mostrar el editor real por no tener conexión a la base de datos.
    Crea una previsualización muy esquemática del editor, pero suficiente para
    ver la posisicón y el tamaño aproximado que tendrá el editor real.
    """

    def initFakeEditor(self) -> None:

        hasPushButtonDB = None
        if not self.tableName_ and not self.foreignField_ and not self.fieldRelation_:
            hasPushButtonDB = True
        else:
            hasPushButtonDB = False

        if not self.fieldName_:
            self.fieldAlias_ = self.tr("Error: fieldName vacio")
        else:
            self.fieldAlias_ = self.fieldName_

        if not self.editor_:

            from pineboolib.application import project

            self.editor_ = QLineEdit(self)
            self.editor_.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
            if self.textLabelDB:
                self.textLabelDB.setSizePolicy(
                    QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed
                )
            # self.editor_.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
            self.editor_.setMinimumWidth(100)
            if project.DGI.mobilePlatform():
                self.editor_.setMinimumHeight(60)

            if self.FLWidgetFieldDBLayout:
                self.FLWidgetFieldDBLayout.addWidget(self.editor_)
            self.editor_.setFocusPolicy(Qt.StrongFocus)
            self.setFocusProxy(self.editor_)

            self.editor_.show()

        if self.textLabelDB:
            self.textLabelDB.setText(self.fieldAlias_)
            if self.showAlias_:
                self.textLabelDB.show()
            else:
                self.textLabelDB.hide()

        if hasPushButtonDB:
            if self.pushButtonDB:
                self.setTabOrder(self.pushButtonDB, self.editor_)
                self.pushButtonDB.setFocusPolicy(Qt.NoFocus)
                self.pushButtonDB.show()
        else:
            if self.pushButtonDB:
                self.pushButtonDB.hide()

        prty = ""
        if self.tableName_:
            prty += "tN:" + str(self.tableName_).upper() + ","
        if self.foreignField_:
            prty += "fF:" + str(self.foreignField_).upper() + ","
        if self.fieldRelation_:
            prty += "fR:" + str(self.fieldRelation_).upper() + ","
        if self.actionName_:
            prty += "aN:" + str(self.actionName_).upper() + ","

        if prty:
            self.editor_.setText(prty)
            self.setEnabled(False)
            self.editor_.home(False)

        if self.maximumSize().width() < 80:
            self.setShowEditor(False)
        else:
            self.setShowEditor(self.showEditor_)

    """
    Color de los campos obligatorios
    """

    def notNullColor(self) -> Any:
        if not self.initNotNullColor_:
            self.initNotNullColor_ = True
        self.notNullColor_ = config.value("ebcomportamiento/colorObligatorio", None)
        if self.notNullColor_ is None:
            self.notNullColor_ = QtGui.QColor(255, 233, 173).name()
        return self.notNullColor_
