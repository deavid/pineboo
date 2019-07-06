# -*- coding: utf-8 -*-
from pineboolib import logging

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QToolButton
from PyQt5.Qt import QKeySequence

from pineboolib.plugins.dgi.dgi_qt.dgi_objects.flformdb import FLFormDB
from pineboolib.fllegacy.flsqlcursor import FLSqlCursor
from pineboolib.fllegacy.flsettings import FLSettings
from pineboolib.core.utils.utils_base import filedir


class FLFormSearchDB(FLFormDB):

    """
    Subclase de la clase FLFormDB, pensada para buscar un registro
    en una tabla.

    El comportamiento de elegir un registro se modifica para solamente
    cerrar el formulario y así el objeto que lo invoca pueda obtener
    del cursor dicho registro.

    También añade botones Aceptar y Cancelar. Aceptar indica que se ha
    elegido el registro activo (igual que hacer doble clic sobre él o
    pulsar la tecla Intro) y Cancelar aborta la operación.

    @author InfoSiAL S.L.
    """

    """
    Boton Aceptar
    """
    pushButtonAccept = None

    """
    Almacena si se ha abierto el formulario con el método FLFormSearchDB::exec()
    """
    loop = None

    acceptingRejecting_ = None
    inExec_ = None
    accepted_ = None

    eventloop = None

    logger = logging.getLogger("FLFormSearchDB")
    """
    constructor.
    """

    def __init__(self, name_or_cursor, parent=None):

        if not name_or_cursor:
            self.logger.warning("Se ha llamado a FLFormSearchDB sin name_or_cursor")
            return

        from pineboolib import pncontrolsfactory, project

        parent = parent or pncontrolsfactory.aqApp.mainWidget()
        if isinstance(name_or_cursor, str):
            action = project.conn.manager().action(name_or_cursor)
            cursor = FLSqlCursor(action.table(), True, "default", None, None, self)
        else:
            action = name_or_cursor._action
            cursor = name_or_cursor

        super(FLFormSearchDB, self).__init__(parent, action, load=False)
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        self.setCursor(cursor)

        self.accepted_ = False

        self.load()
        self.initForm()
        self.setFocusPolicy(QtCore.Qt.NoFocus)

        self.eventloop = QtCore.QEventLoop()

    def setAction(self, a):
        self.cursor_.setAction(a)

    """
    destructor
    """

    def __delattr__(self, *args, **kwargs):
        if self.cursor_:
            self.cursor_.restoreEditionFlag(self)
            self.cursor_.restoreBrowseFlag(self)

        FLFormDB.__delattr__(self, *args, **kwargs)

    """
    formReady = QtCore.pyqtSignal()
    """

    def loadControls(self):
        from pineboolib import pncontrolsfactory

        self.bottomToolbar = QtWidgets.QFrame()
        self.bottomToolbar.setMaximumHeight(64)
        self.bottomToolbar.setMinimumHeight(16)
        self.bottomToolbar.layout = QtWidgets.QHBoxLayout()
        self.bottomToolbar.setLayout(self.bottomToolbar.layout)
        self.bottomToolbar.layout.setContentsMargins(0, 0, 0, 0)
        self.bottomToolbar.layout.setSpacing(0)
        self.bottomToolbar.layout.addStretch()
        self.bottomToolbar.setFocusPolicy(QtCore.Qt.NoFocus)
        self.layout.addWidget(self.bottomToolbar)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy(0), QtWidgets.QSizePolicy.Policy(0))
        sizePolicy.setHeightForWidth(True)

        pbSize = self.iconSize
        settings = FLSettings()
        if settings.readBoolEntry("application/isDebuggerMode", False):

            pushButtonExport = pncontrolsfactory.QToolButton(self)
            pushButtonExport.setObjectName("pushButtonExport")
            pushButtonExport.setSizePolicy(sizePolicy)
            pushButtonExport.setMinimumSize(pbSize)
            pushButtonExport.setMaximumSize(pbSize)
            pushButtonExport.setIcon(pncontrolsfactory.QIcon(filedir("../share/icons", "gtk-properties.png")))
            pushButtonExport.setShortcut(QKeySequence(self.tr("F3")))
            pushButtonExport.setWhatsThis("Exportar a XML(F3)")
            pushButtonExport.setToolTip("Exportar a XML(F3)")
            pushButtonExport.setFocusPolicy(QtCore.Qt.NoFocus)
            self.bottomToolbar.layout.addWidget(pushButtonExport)
            pushButtonExport.clicked.connect(self.exportToXml)

            if settings.readBoolEntry("ebcomportamiento/show_snaptshop_button", False):
                push_button_snapshot = QToolButton(self)
                push_button_snapshot.setObjectName("pushButtonSnapshot")
                push_button_snapshot.setSizePolicy(sizePolicy)
                push_button_snapshot.setMinimumSize(pbSize)
                push_button_snapshot.setMaximumSize(pbSize)
                push_button_snapshot.setIcon(pncontrolsfactory.QIcon(filedir("../share/icons", "gtk-paste.png")))
                push_button_snapshot.setShortcut(QKeySequence(self.tr("F8")))
                push_button_snapshot.setWhatsThis("Capturar pantalla(F8)")
                push_button_snapshot.setToolTip("Capturar pantalla(F8)")
                push_button_snapshot.setFocusPolicy(QtCore.Qt.NoFocus)
                self.bottomToolbar.layout.addWidget(push_button_snapshot)
                push_button_snapshot.clicked.connect(self.saveSnapShot)

            spacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            self.bottomToolbar.layout.addItem(spacer)

        if not self.pushButtonAccept:
            self.pushButtonAccept = pncontrolsfactory.QToolButton(self)
            self.pushButtonAccept.setObjectName("pushButtonAccept")
            self.pushButtonAccept.clicked.connect(self.accept)

        self.pushButtonAccept.setSizePolicy(sizePolicy)
        self.pushButtonAccept.setMaximumSize(pbSize)
        self.pushButtonAccept.setMinimumSize(pbSize)
        self.pushButtonAccept.setIcon(pncontrolsfactory.QIcon(filedir("../share/icons", "gtk-save.png")))
        # pushButtonAccept->setAccel(QKeySequence(Qt::Key_F10)); FIXME
        self.pushButtonAccept.setFocus()
        self.pushButtonAccept.setWhatsThis("Seleccionar registro actual y cerrar formulario (F10)")
        self.pushButtonAccept.setToolTip("Seleccionar registro actual y cerrar formulario (F10)")
        self.pushButtonAccept.setFocusPolicy(QtCore.Qt.NoFocus)
        self.bottomToolbar.layout.addWidget(self.pushButtonAccept)
        self.pushButtonAccept.show()

        if not self.pushButtonCancel:
            self.pushButtonCancel = pncontrolsfactory.QToolButton(self)
            self.pushButtonCancel.setObjectName("pushButtonCancel")
            self.pushButtonCancel.clicked.connect(self.reject)

        self.pushButtonCancel.setSizePolicy(sizePolicy)
        self.pushButtonCancel.setMaximumSize(pbSize)
        self.pushButtonCancel.setMinimumSize(pbSize)
        self.pushButtonCancel.setIcon(pncontrolsfactory.QIcon(filedir("../share/icons", "gtk-stop.png")))
        self.pushButtonCancel.setFocusPolicy(QtCore.Qt.NoFocus)
        # pushButtonCancel->setAccel(Esc); FIXME
        self.pushButtonCancel.setWhatsThis("Cerrar formulario sin seleccionar registro (Esc)")
        self.pushButtonCancel.setToolTip("Cerrar formulario sin seleccionar registro (Esc)")
        self.bottomToolbar.layout.addWidget(self.pushButtonCancel)
        self.pushButtonCancel.show()

        self.cursor_.setEdition(False)
        self.cursor_.setBrowse(False)
        self.cursor_.recordChoosed.connect(self.accept)

    """
    Muestra el formulario y entra en un nuevo bucle de eventos
    para esperar, a seleccionar registro.

    Se espera el nombre de un campo del cursor
    devolviendo el valor de dicho campo si se acepta el formulario
    y un QVariant::Invalid si se cancela.

    @param n Nombre del un campo del cursor del formulario
    @return El valor del campo si se acepta, o QVariant::Invalid si se cancela
    """

    def exec_(self, valor=None):
        if not self.cursor_:
            return False

        if self.cursor_.isLocked():
            self.cursor_.setModeAccess(FLSqlCursor.Browse)

        if self.loop or self.inExec_:
            print("FLFormSearchDB::exec(): Se ha detectado una llamada recursiva")
            if self.isHidden():
                super().show()
            if self.initFocusWidget_:
                self.initFocusWidget_.setFocus()
            return False

        self.inExec_ = True
        self.acceptingRejecting_ = False
        self.accepted_ = False

        super().show()
        if self.initFocusWidget_:
            self.initFocusWidget_.setFocus()

        if self.iface:
            try:
                timer1 = QtCore.QTimer(self)
                timer1.singleShot(300, self.iface.init)
            except Exception:
                pass

        if not self.isClosing_:
            timer2 = QtCore.QTimer(self)
            timer2.singleShot(0, self.emitFormReady)

        self.loop = True
        self.eventloop.exec_()
        self.loop = False
        self.inExec_ = False

        if self.accepted_ and valor:
            return self.cursor_.valueBuffer(valor)
        else:
            self.close()
            return False

    """
    Aplica un filtro al cursor
    """

    def setFilter(self, f):

        if not self.cursor_:
            return
        previousF = self.cursor_.mainFilter()
        newF = None
        if previousF == "":
            newF = f
        elif f is None or previousF.find(f) > -1:
            return
        else:
            newF = "%s AND %s" % (previousF, f)
        self.cursor_.setMainFilter(newF)

    """
    Devuelve el nombre de la clase del formulario en tiempo de ejecución
    """

    def formClassName(self):
        return "FormSearchDB"

    """
    Nombre interno del formulario
    """

    def geoName(self):
        return "formSearch%s" % self.idMDI_

    """
    Captura evento cerrar
    """

    def closeEvent(self, e):
        self.frameGeometry()
        # if self.focusWidget():
        #    fdb = self.focusWidget().parentWidget()
        #    try:
        #        if fdb and fdb.autoComFrame_ and fdb.autoComFrame_.isvisible():
        #            fdb.autoComFrame_.hide()
        #            return
        #    except Exception:
        #        pass

        if self.cursor_ and self.pushButtonCancel:
            if not self.pushButtonCancel.isEnabled():
                return

            self.isClosing_ = True
            self.setCursor(None)
        else:
            self.isClosing_ = True

        if self.isHidden():
            # self.saveGeometry()
            # self.closed.emit()
            super().closeEvent(e)
            self.deleteLater()
        else:
            self.reject()

    """
    Invoca a la función "init" del script "masterprocess" asociado al formulario
    """

    @QtCore.pyqtSlot()
    def callInitScript(self):
        pass

    """
    Redefinida por conveniencia
    """

    @QtCore.pyqtSlot()
    def hide(self):
        if self.isHidden():
            return

        super().hide()
        if self.loop:
            self.loop = False
            self.eventloop.exit()

    """
    Se activa al pulsar el boton aceptar
    """

    @QtCore.pyqtSlot()
    def accept(self):
        if self.acceptingRejecting_:
            return
        self.frameGeometry()
        if self.cursor_:
            try:
                self.cursor_.recordChoosed.disconnect(self.accept)
            except Exception:
                pass
        self.acceptingRejecting_ = True
        self.accepted_ = True
        self.saveGeometry()
        self.hide()

        from pineboolib import pncontrolsfactory

        if isinstance(self.parent(), pncontrolsfactory.QMdiSubWindow):
            self.parent().hide()

    """
    Se activa al pulsar el botón cancelar
    """

    @QtCore.pyqtSlot()
    def reject(self):
        if self.acceptingRejecting_:
            return
        self.frameGeometry()
        if self.cursor_:
            try:
                self.cursor_.recordChoosed.disconnect(self.accept)
            except Exception:
                pass
        self.acceptingRejecting_ = True
        self.hide()

    """
    Redefinida por conveniencia
    """

    @QtCore.pyqtSlot()
    def show(self):
        self.exec_()

    def child(self, childName):
        return self.findChild(QtWidgets.QWidget, childName, QtCore.Qt.FindChildrenRecursively)

    def accepted(self):
        return self.accepted_

    def setMainWidget(self, w=None):

        if not self.cursor_:
            return

        if w:
            w.hide()
            self.mainWidget_ = w
