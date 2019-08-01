# -*- coding: utf-8 -*-
import traceback

from PyQt5 import QtCore, QtGui, QtWidgets  # type: ignore
from PyQt5.Qt import QKeySequence  # type: ignore

from pineboolib import logging
from pineboolib.core import decorators
from pineboolib.core.utils.utils_base import filedir
from pineboolib.core.settings import config
from pineboolib.plugins.dgi.dgi_qt.dgi_objects.flformdb import FLFormDB
from pineboolib.fllegacy.flsqlcursor import FLSqlCursor
from pineboolib.fllegacy.flsqlquery import FLSqlQuery
from pineboolib.fllegacy.flapplication import aqApp
from typing import Any, cast


DEBUG = False

"""
class FLFormRecordDBInterface;

Subclase de FLFormDB pensada para editar registros.

Básicamente esta clase hace lo mismo que su clase
base FLFormDB, lo único que añade son dos botones
Aceptar y/o Cancelar para confirmar o cancelar
los cambios que se realizan en los componentes de
datos que contiene.

Esta clase es idónea para cargar los formularios de
edición de registros definidos en los metadatos
( FLTableMetaData ).

@author InfoSiAL S.L.
"""


class FLFormRecordDB(FLFormDB):

    logger = logging.getLogger("dgi_qt.FLFormRecordDB")
    """
    Boton Aceptar
    """

    pushButtonAccept = None

    """
    Boton Aceptar y continuar
    """
    pushButtonAcceptContinue = None

    """
    Boton Primero
    """
    pushButtonFirst = None

    """
    Boton Anterior
    """
    pushButtonPrevious = None

    """
    Boton Siguiente
    """
    pushButtonNext = None

    """
    Boton Ultimo
    """
    pushButtonLast = None

    """
    Indica si se debe mostrar el botón Aceptar y Continuar
    """
    showAcceptContinue_ = True

    """
    Indica que se está intentando aceptar los cambios
    """
    accepting = None

    """
    Modo en el que inicialmente está el cursor
    """
    initialModeAccess = None

    """
    Registra el nivel de anidamiento de transacciones en el que se entra al iniciar el formulario
    """
    initTransLevel = None

    """
    constructor.

    Solo acepta que se le indique un cursor ya creado.

    @param cursor Objeto FLSqlCursor con el cursor con el que tratar.
    @param actionName Nombre de la acción asociada al formulario
    @param showAcceptContinue Indica si se debe mostrar el botón de Aceptar y Continuar

    FLFormRecordDB(FLSqlCursor *cursor, const QString &actionName = QString::null,
                 QWidget *parent = 0, bool showAcceptContinue = true);
    """

    def __init__(self, parent_or_cursor, action, load=False) -> None:
        self.logger.trace("__init__: parent_or_cursor=%s, action=%s, load=%s", parent_or_cursor, action, load)

        if isinstance(action, str):
            aqApp.db().manager().action(action)

        parent = aqApp.mainWidget() if isinstance(parent_or_cursor, FLSqlCursor) else parent_or_cursor
        cursor = parent_or_cursor if isinstance(parent_or_cursor, FLSqlCursor) else None
        # if not cursor:
        #    load = True

        super().__init__(parent, action, load)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        if cursor:
            self.setCursor(parent_or_cursor)
        self.logger.trace("__init__: load formRecord")
        self._uiName = action.formRecord()
        self._scriptForm = action.scriptFormRecord() or "emptyscript"

        if self.cursor_:
            self.initialModeAccess = self.cursor_.modeAccess()
            if DEBUG:
                print("*** FLFormRecordDB::__init__: cursor: %r name: %r at:%r" % (self.cursor_, self.cursor_.curName(), self.cursor_.at()))
                cur_values = [f.value for f in self.cursor_.d.buffer_.fieldList_]
                print("*** cursor Buffer: %r" % cur_values)

        else:
            if DEBUG:
                print("*** FLFormRecordDB::__init__ -> Sin cursor??")
            self.initialModeAccess = FLSqlCursor.Browse

        self.logger.trace("__init__: load form")
        self.load()
        self.logger.trace("__init__: init form")
        self.initForm()
        self.logger.trace("__init__: done")
        self.loop = False

    """
    Reimplementado, añade un widget como principal del formulario
    """

    @decorators.NotImplementedWarn
    def setMainWidget(self, w=None):
        pass

    """
    Establece el título de la ventana.

    @param text Texto a establecer como título de la ventana
    @author Silix
    """

    def setCaptionWidget(self, text=None) -> None:
        if not self.cursor_:
            return

        if not text:
            text = self.cursor_.metadata().alias()

        if self.cursor_.modeAccess() == self.cursor_.Insert:
            self.setWindowTitle("Insertar %s" % text)
        elif self.cursor_.modeAccess() == self.cursor_.Edit:
            self.setWindowTitle("Editar %s" % text)
        elif self.cursor_.modeAccess() == self.cursor_.Browse:
            self.setWindowTitle("Visualizar %s" % text)

    """
    Devuelve el nombre de la clase del formulario en tiempo de ejecución
    """

    def formClassName(self):
        return "FormRecordDB"

    """
    Inicialización
    """

    def initForm(self):
        if self.cursor() and self.cursor().metadata():
            # caption = None
            if self._action:
                self.cursor().setAction(self._action)
                if self._action.description():
                    self.setWhatsThis(self._action.description())
                self.idMDI_ = self._action.name()

            # self.bindIface()
            # self.setCursor(self.cursor_)

        else:
            self.setCaptionWidget("No hay metadatos")
        # acl = project.acl()
        acl = None  # FIXME: Add ACL later
        if acl:
            acl.process(self)

    def loadControls(self):
        if self.pushButtonAcceptContinue:
            self.pushButtonAcceptContinue.hide()

        if self.pushButtonAccept:
            self.pushButtonAccept.hide()

        if self.pushButtonCancel:
            self.pushButtonCancel.hide()

        if self.pushButtonFirst:
            self.pushButtonFirst.hide()

        if self.pushButtonPrevious:
            self.pushButtonPrevious.hide()

        if self.pushButtonNext:
            self.pushButtonNext.hide()

        if self.pushButtonLast:
            self.pushButtonLast.hide()

        if self.bottomToolbar and self.toolButtonClose:
            self.toolButtonClose.hide()

        self.bottomToolbar = QtWidgets.QFrame()
        self.bottomToolbar.setMinimumSize(self.iconSize)
        self.bottomToolbar.setLayout(QtWidgets.QHBoxLayout())

        self.bottomToolbar.layout().setContentsMargins(0, 0, 0, 0)
        self.bottomToolbar.layout().setSpacing(0)
        self.bottomToolbar.layout().addStretch()
        self.bottomToolbar.setFocusPolicy(QtCore.Qt.NoFocus)
        self.layout_.addWidget(self.bottomToolbar)
        # if self.layout:
        #    self.layout = None
        # Limpiamos la toolbar

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy(0), QtWidgets.QSizePolicy.Policy(0))
        sizePolicy.setHeightForWidth(True)

        pbSize = self.iconSize

        if config.value("application/isDebuggerMode", False):

            pushButtonExport = QtWidgets.QToolButton()
            pushButtonExport.setObjectName("pushButtonExport")
            pushButtonExport.setSizePolicy(sizePolicy)
            pushButtonExport.setMinimumSize(pbSize)
            pushButtonExport.setMaximumSize(pbSize)
            pushButtonExport.setIcon(QtGui.QIcon(filedir("../share/icons", "gtk-properties.png")))
            pushButtonExport.setShortcut(QKeySequence(self.tr("F3")))
            pushButtonExport.setWhatsThis("Exportar a XML(F3)")
            pushButtonExport.setToolTip("Exportar a XML(F3)")
            pushButtonExport.setFocusPolicy(QtCore.Qt.NoFocus)
            self.bottomToolbar.layout().addWidget(pushButtonExport)
            pushButtonExport.clicked.connect(self.exportToXml)

            if config.value("ebcomportamiento/show_snaptshop_button", False):
                push_button_snapshot = QtWidgets.QToolButton()
                push_button_snapshot.setObjectName("pushButtonSnapshot")
                push_button_snapshot.setSizePolicy(sizePolicy)
                push_button_snapshot.setMinimumSize(pbSize)
                push_button_snapshot.setMaximumSize(pbSize)
                push_button_snapshot.setIcon(QtGui.QIcon(filedir("../share/icons", "gtk-paste.png")))
                push_button_snapshot.setShortcut(QKeySequence(self.tr("F8")))
                push_button_snapshot.setWhatsThis("Capturar pantalla(F8)")
                push_button_snapshot.setToolTip("Capturar pantalla(F8)")
                push_button_snapshot.setFocusPolicy(QtCore.Qt.NoFocus)
                self.bottomToolbar.layout().addWidget(push_button_snapshot)
                push_button_snapshot.clicked.connect(self.saveSnapShot)

            spacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            self.bottomToolbar.layout().addItem(spacer)

        if self.cursor().modeAccess() in (self.cursor().Edit, self.cursor().Browse):
            if not self.pushButtonFirst:
                self.pushButtonFirst = QtWidgets.QToolButton()
                self.pushButtonFirst.setObjectName("pushButtonFirst")
                self.pushButtonFirst.setIcon(QtGui.QIcon(filedir("../share/icons", "gtk-goto-first-ltr.png")))
                self.pushButtonFirst.clicked.connect(self.firstRecord)
                self.pushButtonFirst.setSizePolicy(sizePolicy)
                self.pushButtonFirst.setMaximumSize(pbSize)
                self.pushButtonFirst.setMinimumSize(pbSize)
                self.pushButtonFirst.setShortcut(QKeySequence(self.tr("F5")))
                self.pushButtonFirst.setWhatsThis("Aceptar los cambios e ir al primer registro (F5)")
                self.pushButtonFirst.setToolTip("Aceptar los cambios e ir al primer registro (F5)")
                self.pushButtonFirst.setFocusPolicy(QtCore.Qt.NoFocus)
                self.bottomToolbar.layout().addWidget(self.pushButtonFirst)
                # self.pushButtonFirst.show()

            if not self.pushButtonPrevious:
                self.pushButtonPrevious = QtWidgets.QToolButton()
                self.pushButtonPrevious.setObjectName("pushButtonPrevious")
                self.pushButtonPrevious.setIcon(QtGui.QIcon(filedir("../share/icons", "gtk-go-back-ltr.png")))
                self.pushButtonPrevious.clicked.connect(self.previousRecord)
                self.pushButtonPrevious.setSizePolicy(sizePolicy)
                self.pushButtonPrevious.setMaximumSize(pbSize)
                self.pushButtonPrevious.setMinimumSize(pbSize)
                self.pushButtonPrevious.setShortcut(QKeySequence(self.tr("F6")))
                self.pushButtonPrevious.setWhatsThis("Aceptar los cambios e ir al registro anterior (F6)")
                self.pushButtonPrevious.setToolTip("Aceptar los cambios e ir al registro anterior (F6)")
                self.pushButtonPrevious.setFocusPolicy(QtCore.Qt.NoFocus)
                self.bottomToolbar.layout().addWidget(self.pushButtonPrevious)
                # self.pushButtonPrevious.show()

            if not self.pushButtonNext:
                self.pushButtonNext = QtWidgets.QToolButton()
                self.pushButtonNext.setObjectName("pushButtonNext")
                self.pushButtonNext.setIcon(QtGui.QIcon(filedir("../share/icons", "gtk-go-back-rtl.png")))
                self.pushButtonNext.clicked.connect(self.nextRecord)
                self.pushButtonNext.setSizePolicy(sizePolicy)
                self.pushButtonNext.setMaximumSize(pbSize)
                self.pushButtonNext.setMinimumSize(pbSize)
                self.pushButtonNext.setShortcut(QKeySequence(self.tr("F7")))
                self.pushButtonNext.setWhatsThis("Aceptar los cambios e ir al registro siguiente (F7)")
                self.pushButtonNext.setToolTip("Aceptar los cambios e ir al registro siguiente (F7)")
                self.pushButtonNext.setFocusPolicy(QtCore.Qt.NoFocus)
                self.bottomToolbar.layout().addWidget(self.pushButtonNext)
                # self.pushButtonNext.show()

            if not self.pushButtonLast:
                self.pushButtonLast = QtWidgets.QToolButton()
                self.pushButtonLast.setObjectName("pushButtonLast")
                self.pushButtonLast.setIcon(QtGui.QIcon(filedir("../share/icons", "gtk-goto-last-ltr.png")))
                self.pushButtonLast.clicked.connect(self.lastRecord)
                self.pushButtonLast.setSizePolicy(sizePolicy)
                self.pushButtonLast.setMaximumSize(pbSize)
                self.pushButtonLast.setMinimumSize(pbSize)
                self.pushButtonLast.setShortcut(QKeySequence(self.tr("F8")))
                self.pushButtonLast.setWhatsThis("Aceptar los cambios e ir al último registro (F8)")
                self.pushButtonLast.setToolTip("Aceptar los cambios e ir al último registro (F8)")
                self.pushButtonLast.setFocusPolicy(QtCore.Qt.NoFocus)
                self.bottomToolbar.layout().addWidget(self.pushButtonLast)
                # self.pushButtonLast.show()

        if not self.cursor().modeAccess() == self.cursor().Browse:
            self.pushButtonAcceptContinue = QtWidgets.QToolButton()
            self.pushButtonAcceptContinue.setObjectName("pushButtonAcceptContinue")
            self.pushButtonAcceptContinue.clicked.connect(self.acceptContinue)
            self.pushButtonAcceptContinue.setSizePolicy(sizePolicy)
            self.pushButtonAcceptContinue.setMaximumSize(pbSize)
            self.pushButtonAcceptContinue.setMinimumSize(pbSize)
            self.pushButtonAcceptContinue.setIcon(QtGui.QIcon(filedir("../share/icons", "gtk-refresh.png")))
            self.pushButtonAcceptContinue.setShortcut(QKeySequence(self.tr("F9")))
            self.pushButtonAcceptContinue.setWhatsThis("Aceptar los cambios y continuar con la edición de un nuevo registro (F9)")
            self.pushButtonAcceptContinue.setToolTip("Aceptar los cambios y continuar con la edición de un nuevo registro (F9)")
            self.pushButtonAcceptContinue.setFocusPolicy(QtCore.Qt.NoFocus)
            self.bottomToolbar.layout().addWidget(self.pushButtonAcceptContinue)
            if not self.showAcceptContinue_:
                self.pushButtonAcceptContinue.close()
                # self.pushButtonAcceptContinue.show()

            if not self.pushButtonAccept:
                self.pushButtonAccept = QtWidgets.QToolButton()
                self.pushButtonAccept.setObjectName("pushButtonAccept")
                self.pushButtonAccept.clicked.connect(self.accept)

            self.pushButtonAccept.setSizePolicy(sizePolicy)
            self.pushButtonAccept.setMaximumSize(pbSize)
            self.pushButtonAccept.setMinimumSize(pbSize)
            self.pushButtonAccept.setIcon(QtGui.QIcon(filedir("../share/icons", "gtk-save.png")))
            self.pushButtonAccept.setShortcut(QKeySequence(self.tr("F10")))
            self.pushButtonAccept.setWhatsThis("Aceptar los cambios y cerrar formulario (F10)")
            self.pushButtonAccept.setToolTip("Aceptar los cambios y cerrar formulario (F10)")
            self.pushButtonAccept.setFocusPolicy(QtCore.Qt.NoFocus)
            self.bottomToolbar.layout().addWidget(self.pushButtonAccept)
            # self.pushButtonAccept.show()

        if not self.pushButtonCancel:
            self.pushButtonCancel = QtWidgets.QToolButton()
            self.pushButtonCancel.setObjectName("pushButtonCancel")
            try:
                self.cursor().autocommit.connect(self.disablePushButtonCancel)
            except Exception:
                pass

            self.pushButtonCancel.clicked.connect(self.reject)

        self.pushButtonCancel.setSizePolicy(sizePolicy)
        self.pushButtonCancel.setMaximumSize(pbSize)
        self.pushButtonCancel.setMinimumSize(pbSize)
        self.pushButtonCancel.setShortcut(QKeySequence(self.tr("Esc")))
        self.pushButtonCancel.setIcon(QtGui.QIcon(filedir("../share/icons", "gtk-stop.png")))
        if not self.cursor().modeAccess() == self.cursor().Browse:
            self.pushButtonCancel.setFocusPolicy(QtCore.Qt.NoFocus)
            self.pushButtonCancel.setWhatsThis("Cancelar los cambios y cerrar formulario (Esc)")
            self.pushButtonCancel.setToolTip("Cancelar los cambios y cerrar formulario (Esc)")
        else:
            self.pushButtonCancel.setFocusPolicy(QtCore.Qt.StrongFocus)
            self.pushButtonCancel.setFocus()
            # pushButtonCancel->setAccel(4096); FIXME
            self.pushButtonCancel.setWhatsThis("Aceptar y cerrar formulario (Esc)")
            self.pushButtonCancel.setToolTip("Aceptar y cerrar formulario (Esc)")

        # pushButtonCancel->setDefault(true);
        self.bottomToolbar.layout().addItem(QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed))
        self.bottomToolbar.layout().addWidget(self.pushButtonCancel)
        # self.pushButtonAccept.show()

        self.setFocusPolicy(QtCore.Qt.NoFocus)

        # self.toolButtonAccept = QtGui.QToolButton()
        # self.toolButtonAccept.setIcon(QtGui.QIcon(filedir("../share/icons","gtk-add.png")))
        # self.toolButtonAccept.clicked.connect(self.validateForm)
        # self.bottomToolbar.layout.addWidget(self.toolButtonAccept)
        self.inicializeControls()

    """
    Nombre interno del formulario
    """

    def formName(self):
        return "formRecord%s" % self.idMDI_

    """
    Une la interfaz de script al objeto del formulario
    """
    # void bindIface();

    """
    Desune la interfaz de script al objeto del formulario
    """
    # void unbindIface();

    """
    Indica si la interfaz de script está unida al objeto formulario
    """
    # bool isIfaceBind() const;

    """
    Captura evento cerrar
    """

    def closeEvent(self, e):
        self.frameGeometry()
        if self.focusWidget():
            fdb = self.focusWidget().parentWidget()
            try:
                if fdb.autoComFrame_.isvisible():
                    fdb.autoComFrame_.hide()
                    return
            except Exception:
                pass

        if self.cursor_:

            try:
                levels = self.cursor_.transactionLevel() - self.initTransLevel
                if levels > 0:
                    self.cursor_.rollbackOpened(
                        levels,
                        "Se han detectado transacciones no finalizadas en la última operación.\n"
                        "Se van a cancelar las transacciones pendientes.\n"
                        "Los últimos datos introducidos no han sido guardados, por favor\n"
                        "revise sus últimas acciones y repita las operaciones que no\n"
                        "se han guardado.\n"
                        "FLFormRecordDB::closeEvent: %s %s" % (levels, self.name()),
                    )
            except Exception:
                print("ERROR: FLFormRecordDB @ closeEvent :: las transacciones aún no funcionan.")

            if self.accepted_:
                if not self.cursor_.commit():
                    return
                self.afterCommitTransaction()
            else:
                if not self.cursor_.rollback():
                    e.ignore()
                    return
                # else:
                #    self.cursor_.select()

            self.closed.emit()
            self.setCursor(None)
        else:
            self.closed.emit()

        super(FLFormRecordDB, self).closeEvent(e)
        self.deleteLater()

    """
    Validación de formulario.

    Invoca a la función "validateForm" del script asociado cuando se acepta el
    formulario y sólo continua con el commit del registro cuando esa función
    de script devuelve TRUE.

    Si FLTableMetaData::concurWarn() es true y dos o mas sesiones/usuarios están
    modificando los mismos campos mostrará un aviso de advertencia.

    @return TRUE si el formulario ha sido validado correctamente
    """

    def validateForm(self) -> Any:
        if not self.cursor_:
            return True
        mtd = self.cursor_.metadata()
        if not mtd:
            return True

        if self.cursor_.modeAccess() == FLSqlCursor.Edit and mtd.concurWarn():
            colFields = self.cursor_.concurrencyFields()

            if colFields:
                pKN = mtd.primaryKey()
                pKWhere = self.cursor_.db().manager().formatAssignValue(mtd.field(pKN), self.cursor_.valueBuffer(pKN))
                q = FLSqlQuery(None, self.cursor_.db().connectionName())
                q.setTablesList(mtd.name())
                q.setSelect(colFields)
                q.setFrom(mtd.name())
                q.setWhere(pKWhere)
                q.setForwardOnly(True)

                if q.exec_() and q.next():
                    i = 0
                    for field in colFields:
                        # msg = "El campo '%s' con valor '%s' ha sido modificado\npor otro usuario con el valor '%s'" % (
                        #    mtd.fieldNameToAlias(field), self.cursor_.valueBuffer(field), q.value(i))
                        res = QtWidgets.QMessageBox.warning(
                            QtWidgets.QApplication.focusWidget(),
                            "Aviso de concurrencia",
                            "\n\n ¿ Desea realmente modificar este campo ?\n\n"
                            "Sí : Ignora el cambio del otro usuario y utiliza el valor que acaba de introducir\n"
                            "No : Respeta el cambio del otro usuario e ignora el valor que ha introducido\n"
                            "Cancelar : Cancela el guardado del registro y vuelve a la edición del registro\n\n",
                            cast(QtWidgets.QMessageBox, QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Default),
                            cast(
                                QtWidgets.QMessageBox,
                                QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Escape,
                            ),
                        )
                        if res == QtWidgets.QMessageBox.Cancel:
                            return False

                        if res == QtWidgets.QMessageBox.No:
                            self.cursor_.setValueBuffer(field, q.value(i))

        if self.iface and self.cursor_.modeAccess() == FLSqlCursor.Insert or self.cursor_.modeAccess() == FLSqlCursor.Edit:
            ret_ = True
            fun_ = getattr(self.iface, "validateForm", None)
            if fun_ is not None and fun_ != self.validateForm:
                try:
                    ret_ = fun_()
                except Exception:
                    # script_name = self.iface.__module__
                    from pineboolib.core.error_manager import error_manager
                    from pineboolib.application import project

                    aqApp.msgBoxWarning(error_manager(traceback.format_exc(limit=-6, chain=False)), project._DGI)

            return ret_ if isinstance(ret_, bool) else False
        return True

    """
    Aceptación de formulario.

    Invoca a la función "acceptedForm" del script asociado al formulario, cuando
    se acepta el formulario y justo antes de hace el commit del registro.
    """

    def acceptedForm(self) -> None:
        if self.iface:
            try:
                self.iface.acceptedForm()
            except Exception:
                pass

    """
    Después de fijar los cambios del buffer del registro actual.

    Invoca a la función "afterCommitBuffer" del script asociado al formulario,
    justo después de hacer el commit del buffer del registro.
    """

    def afterCommitBuffer(self) -> None:
        if self.iface:
            try:
                self.iface.afterCommitBuffer()
            except Exception:
                pass

    """
    Despues de fijar la transacción.

    Invoca a la función "afterCommitTransaction" del script asociado al formulario,
    juesto despues de terminar la transacción en curso aceptando.
    """

    def afterCommitTransaction(self) -> None:
        if self.iface:
            try:
                self.iface.afterCommitTransaction()
            except Exception:
                pass

    """
    Cancelación de formulario.

    Invoca a la función "canceledForm" del script asociado al formulario, cuando se
    cancela el formulario.
    """

    def canceledForm(self) -> None:
        if self.iface:
            try:
                self.iface.canceledForm()
            except Exception:
                pass

    """
    Se activa al pulsar el boton aceptar
    """

    @decorators.pyqtSlot()
    def accept(self):
        if self.accepting:
            return

        self.accepting = True

        if not self.cursor_:
            self.close()
            self.accepting = False
            return

        if not self.validateForm():
            self.accepting = False
            return

        if self.cursor_.checkIntegrity():
            self.acceptedForm()
            self.cursor_.setActivatedCheckIntegrity(False)
            if not self.cursor_.commitBuffer():
                self.accepting = False
                return
            else:
                self.cursor_.setActivatedCheckIntegrity(True)
        else:
            self.accepting = False
            return

        self.afterCommitBuffer()
        self.accepted_ = True
        self.close()
        self.accepting = False

    """
    Se activa al pulsar el boton aceptar y continuar
    """

    @decorators.pyqtSlot()
    def acceptContinue(self):
        if self.accepting:
            return

        self.accepting = True
        if not self.cursor_:
            self.close()
            self.accepting = False
            return

        if not self.validateForm():
            self.accepting = False
            return

        if self.cursor_.checkIntegrity():
            self.acceptedForm()
            self.cursor_.setActivatedCheckIntegrity(False)
            if self.cursor_.commitBuffer():
                self.cursor_.setActivatedCheckIntegrity(True)
                self.cursor_.commit()
                self.cursor_.setModeAccess(FLSqlCursor.Insert)
                self.accepted_ = False
                caption = None
                if self._action:
                    caption = self._action.name()
                if not caption:
                    caption = self.cursor_.metadata().alias()
                self.cursor_.transaction()
                self.setCaptionWidget(caption)
                if self.initFocusWidget_:
                    self.initFocusWidget_.setFocus()
                self.cursor_.refreshBuffer()
                self.initScript()

        self.accepting = False

    """
    Se activa al pulsar el botón cancelar
    """

    @decorators.pyqtSlot()
    def reject(self):
        self.accepted_ = False
        self.canceledForm()
        self.close()

    """
    Devuelve el script asociado al formulario
    """

    @decorators.pyqtSlot()
    @decorators.NotImplementedWarn
    def script(self):
        pass

    """
    Ir al primer anterior
    """

    @decorators.pyqtSlot()
    def firstRecord(self):
        if self.cursor_ and not self.cursor_.at() == 0:
            if not self.validateForm():
                return

            if self.cursor_.checkIntegrity():
                self.acceptedForm()
                self.cursor_.setActivatedCheckIntegrity(False)
                if self.cursor_.commitBuffer():
                    self.cursor_.setActivatedCheckIntegrity(True)
                    self.cursor_.commit()
                    self.cursor_.setModeAccess(self.initialModeAccess)
                    self.accepted_ = False
                    self.cursor_.transaction()
                    self.cursor_.first()
                    self.setCaptionWidget()
                    self.initScript()

    """
    Ir al registro anterior
    """

    @decorators.pyqtSlot()
    def previousRecord(self):
        if self.cursor_ and self.cursor_.isValid():
            if self.cursor_.at() == 0:
                self.lastRecord()
                return

            if not self.validateForm():
                return

            if self.cursor_.checkIntegrity():
                self.acceptedForm()
                self.cursor_.setActivatedCheckIntegrity(False)
                if self.cursor_.commitBuffer():
                    self.cursor_.setActivatedCheckIntegrity(True)
                    self.cursor_.commit()
                    self.cursor_.setModeAccess(self.initialModeAccess)
                    self.accepted_ = False
                    self.cursor_.transaction()
                    self.cursor_.prev()
                    self.setCaptionWidget()
                    self.initScript()

    """
    Ir al registro siguiente
    """

    @decorators.pyqtSlot()
    def nextRecord(self):
        if self.cursor_ and self.cursor_.isValid():
            if self.cursor_.at() == (self.cursor_.size() - 1):
                self.firstRecord()
                return

            if not self.validateForm():
                return

            if self.cursor_.checkIntegrity():
                self.acceptedForm()
                self.cursor_.setActivatedCheckIntegrity(False)
                if self.cursor_.commitBuffer():
                    self.cursor_.setActivatedCheckIntegrity(True)
                    self.cursor_.commit()
                    self.cursor_.setModeAccess(self.initialModeAccess)
                    self.accepted_ = False
                    self.cursor_.transaction()
                    self.cursor_.next()
                    self.setCaptionWidget()
                    self.initScript()

    """
    Ir al ultimo registro
    """

    @decorators.pyqtSlot()
    def lastRecord(self):
        if self.cursor_ and not self.cursor_.at() == (self.cursor_.size() - 1):
            if not self.validateForm():
                return

            if self.cursor_.checkIntegrity():
                self.acceptedForm()
                self.cursor_.setActivatedCheckIntegrity(False)
                if self.cursor_.commitBuffer():
                    self.cursor_.setActivatedCheckIntegrity(True)
                    self.cursor_.commit()
                    self.cursor_.setModeAccess(self.initialModeAccess)
                    self.accepted_ = False
                    self.cursor_.transaction()
                    self.cursor_.last()
                    self.setCaptionWidget()
                    self.initScript()

    """
    Desactiva el botón cancelar
    """

    @decorators.pyqtSlot()
    def disablePushButtonCancel(self):
        if self.pushButtonCancel:
            self.pushButtonCancel.setDisabled(True)

    def show(self):
        if self.showed:
            QtWidgets.QMessageBox.information(
                QtWidgets.QApplication.activeWindow(),
                "Aviso",
                "Ya hay abierto un formulario de edición de resgistro para esta tabla.\n"
                "No se abrirán mas para evitar ciclos repetitivos de edición de registros.",
                QtWidgets.QMessageBox.Yes,
            )
            return
        else:
            caption = self._action.caption()
            if not caption:
                caption = self.cursor().metadata().alias()

            if not self.cursor().isValid():
                self.cursor().model().refresh()

            if self.cursor().modeAccess() in (self.cursor().Insert, self.cursor().Edit, self.cursor().Browse):
                self.cursor().transaction()
                self.initTransLevel = self.cursor().transactionLevel()
                self.setCaptionWidget(caption)
                self.cursor().setContext(self.iface)
            if self.cursor().modeAccess() == FLSqlCursor.Insert:
                self.showAcceptContinue_ = True
            else:
                self.showAcceptContinue_ = False

            self.loadControls()

        super(FLFormRecordDB, self).show()

    def inicializeControls(self) -> None:
        from pineboolib import pncontrolsfactory

        for child_ in self.findChildren(QtWidgets.QWidget):
            if isinstance(child_, pncontrolsfactory.FLFieldDB):
                loaded = getattr(child_, "_loaded", None)
                if loaded is False:
                    QtCore.QTimer.singleShot(0, child_.load)

    def show_and_wait(self) -> None:
        if self.loop:
            raise Exception("show_and_wait(): Se ha detectado una llamada recursiva")

        self.loop = True
        self.show()
        if self.eventloop:
            self.eventloop.exec_()

        self.loop = False

    def hide(self) -> None:
        if self.loop:
            self.eventloop.exit()
