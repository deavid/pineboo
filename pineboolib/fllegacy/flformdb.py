# -*- coding: utf-8 -*-
import traceback
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QDialog, QFileDialog, QApplication

from pineboolib import logging
from pineboolib.core import decorators
from pineboolib.core.utils.utils_base import filedir
from pineboolib.application.utils.geometry import loadGeometryForm, saveGeometryForm
from pineboolib.fllegacy.flaction import FLAction
from pineboolib.core.settings import config
from pineboolib.fllegacy.flapplication import aqApp
from typing import Any, Union, Dict, Optional, Tuple, Type

"""
Representa un formulario que enlaza con una tabla.

Se utiliza como contenedor de componentes que quieran
enlazar con la base de datos y acceder a los registros
del cursor. Esta estructura simplifica en gran
medida el acceso a los datos ya que muchas tareas son
automáticamente gestionadas por este formulario contenedor.

En un principio el formulario se crea vacío y debemos invocar
el metodo FLFormDB::setMainWidget(), pasándole como parámetro
otro widget (generalmente un formulario creado con QtDesigner),
el cual contiene distintos componentes, este widget se visualizará
dentro de este contenedor, autofonfigurándose todos los componentes
que contiene, con los datos y metadatos del cursor. Generalmente los
componentes serán plugins, como FLFieldDB o FLTableDB.

@author InfoSiAL S.L.
"""


class FLFormDB(QDialog):

    """
    Cursor, con los registros, utilizado por el formulario
    """

    cursor_ = None

    """
    Nombre de la tabla, contiene un valor no vacío cuando
    la clase es propietaria del cursor
    """
    name_ = None

    """
    Capa principal del formulario
    """
    layout_ = None

    """
    Widget principal del formulario
    """
    mainWidget_ = None
    """
    Identificador de ventana MDI.

    Generalmente es el nombre de la acción que abre el formulario
    """
    idMDI_: Optional[str] = None

    """
    Capa para botones
    """
    layoutButtons = None

    """
    Boton Cancelar
    """
    pushButtonCancel = None

    """
    Indica que la ventana ya ha sido mostrada una vez
    """
    showed = None

    """
    Guarda el contexto anterior que tenia el cursor
    """
    oldCursorCtxt = None

    """
    Indica que el formulario se está cerrando
    """
    isClosing_ = None

    """
    Componente con el foco inicial
    """
    initFocusWidget_ = None

    """
    Guarda el último objeto de formulario unido a la interfaz de script (con bindIface())
    """
    oldFormObj = None

    """
    Boton Debug Script
    """
    pushButtonDebug = None

    """
    Almacena que se aceptado, es decir NO se ha pulsado, botón cancelar
    """
    accepted_: bool = False

    """
    Nombre del formulario relativo a la acción (form / formRecrd + nombre de la acción)
    """
    actionName_: str = ""

    """
    Interface para scripts
    """
    iface = None

    """
    Tamaño de icono por defecto
    """
    iconSize = None

    # protected slots:

    """
    Uso interno
    """
    oldFormObjDestroyed = QtCore.pyqtSignal()

    # signals:

    """
    Señal emitida cuando se cierra el formulario
    """
    closed = QtCore.pyqtSignal()

    """
    Señal emitida cuando el formulario ya ha sido inicializado y está listo para usarse
    """
    formReady = QtCore.pyqtSignal()
    formClosed = QtCore.pyqtSignal()

    known_instances: Dict[Tuple[Type["FLFormDB"], str], "FLFormDB"] = {}
    cursor_ = None
    bottomToolbar = None
    pushButtonCancel = None
    toolButtonClose = None

    _uiName = None
    _scriptForm: Union[Any, str] = None

    loop: bool

    init_thread_script = None
    logger = logging.getLogger("FLFormDB")

    def __init__(self, parent, action: FLAction, load=False):

        # self.tiempo_ini = time.time()
        from pineboolib.application import project

        if not parent:
            parent = aqApp.mainWidget()
        # if project.DGI.localDesktop():  # Si es local Inicializa
        QtWidgets.QWidget.__init__(self, parent)  # FIXME: Porqué pide dos argumentos extra??
        # super(QtWidgets.QWidget, self).__init__(parent)

        self._loaded = False
        self.known_instances[(self.__class__, action.name())] = self

        self._action: "FLAction" = action
        if type(self).__name__ == "FLFormRecordDB":
            self.actionName_ = "formRecord" + self._action.name()
            script_name = self._action.scriptFormRecord()
        else:
            if self._action.table():
                self.actionName_ = "form" + self._action.name()
                script_name = self._action.scriptForm()
            else:
                # Load of the main script (flfactppal/flfacturac)
                # Currently detected by having no table
                # FIXME: A better detection method should be placed.
                self.actionName_ = self._action.name()
                script_name = self._action.name()

        # self.mod = self._action.mod
        self.loop = False
        self.eventloop = QtCore.QEventLoop()

        self.layout_ = QtWidgets.QVBoxLayout()
        self.layout_.setContentsMargins(1, 1, 1, 1)
        self.layout_.setSpacing(1)
        self.layout_.setContentsMargins(1, 1, 1, 1)
        self.layout_.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.setLayout(self.layout_)
        if not self._uiName:
            self._uiName = self._action.form()

        # if not self._scriptForm and self._action.scriptForm():
        #    self._scriptForm = self._action.scriptForm()

        # if not getattr(self._action, "alias", None):
        #    qWarning("FLFormDB::Cargando un action XML")
        # elif project.DGI.localDesktop():
        # self.setWindowTitle(self._action.alias)

        self.idMDI_ = self._action.name()

        self.logger.info("init: Action: %s", self._action)
        self.script = project.actions[self._action.name()].load_script(script_name, self)
        self.widget = self.script.form
        self.iface = self.widget.iface

        if project._DGI is not None:
            self.iconSize = project.DGI.iconSize()
        self.init_thread_script = None
        if load:
            self.load()
            self.initForm()

    def load(self) -> None:
        if self._loaded:
            return

        # self.resize(550,350)
        if self.layout_ is None:
            return

        self.layout_.insertWidget(0, self.widget)
        self.layout_.setSpacing(1)
        self.layout_.setContentsMargins(1, 1, 1, 1)
        self.layout_.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)

        if self._uiName:
            from pineboolib.application import project

            if project.conn is None:
                raise Exception("Project is not connected yet")

            project.conn.managerModules().createUI(self._uiName, None, self)

        self._loaded = True

    def loaded(self) -> bool:
        return self._loaded

    """
    Invoca a la función "init" del script "masterprocess" asociado al formulario
    """

    @decorators.pyqtSlot()
    def initScript(self):
        if self._loaded:
            if not getattr(self.widget, "iface", None):
                self.iface = self.widget  # Es posible que no tenga ifaceCtx, así hacemos que sea polivalente

            if self.widget:
                self.widget.clear_connections()

            if hasattr(self.iface, "init"):  # Meterlo en un hilo
                try:
                    self.iface.init()
                except Exception:
                    # script_name = self.iface.__module__
                    from pineboolib.core.error_manager import error_manager
                    from pineboolib.application import project

                    aqApp.msgBoxWarning(error_manager(traceback.format_exc(limit=-6, chain=False)), project._DGI)

            return True

        return False

    """
    constructor
    """
    # explicit FLFormDB(QWidget *parent = 0, const char *name = 0, WFlags f =
    # 0);

    """
    constructor.

    @param actionName Nombre de la acción asociada al formulario
    """
    # FLFormDB(const QString &actionName, QWidget *parent = 0, WFlags f = 0);

    """
    constructor sobrecargado.

    @param cursor Objeto FLSqlCursor para asignar a este formulario
    @param actionName Nombre de la acción asociada al formulario
    """
    # FLFormDB(FLSqlCursor *cursor, const QString &actionName = QString::null,
    #       QWidget *parent = 0, WFlags f = 0);

    """
    destructor
    """

    def __del__(self) -> None:
        # TODO: Esto hay que moverlo al closeEvent o al close()
        # ..... los métodos __del__ de python son muy poco fiables.
        # ..... Se lanzan o muy tarde, o nunca.
        # (De todos modos creo que ya hice lo mismo a mano en el closeEvent en commits anteriores)

        self.unbindIface()

    def setCursor(self, cursor=None) -> None:
        if cursor is not self.cursor_ and self.cursor_ and self.oldCursorCtxt:
            self.cursor_.setContext(self.oldCursorCtxt)

        if not cursor:
            return

        if self.cursor_ and self.cursor_ is not cursor:
            if type(self).__name__ == "FLFormRecodDB":
                self.cursor_.restoreEditionFlag(self)
                self.cursor_.restoreBrowseFlag(self)

        if self.cursor_:
            self.cursor_.destroyed.disconnect(self.cursorDestroyed)

        self.cursor_ = cursor

        if type(self).__name__ == "FLFormRecodDB":
            self.cursor_.setEdition(False, self)
            self.cursor_.setBrowse(False, self)

        self.cursor_.destroyed.connect(self.cursorDestroyed)
        if self.iface and self.cursor_:
            self.oldCursorCtxt = self.cursor().context()
            self.cursor_.setContext(self.iface)

    """
    Para obtener el cursor utilizado por el formulario.

    return Objeto FLSqlCursor con el cursor que contiene los registros para ser utilizados
      en el formulario
    """

    def cursor(self) -> Any:
        return self.cursor_

    """
    Para obtener el widget principal del formulario.

    return Objeto QWidget que corresponde con el widget principal del formulario
    """

    def mainWidget(self) -> Any:
        return self.mainWidget_

    """
    Establece el identificador MDI
    """

    def setIdMDI(self, id_) -> None:
        self.idMDI_ = id_

    """
    Obtiene el identificador MDI
    """

    def idMDI(self) -> Optional[str]:
        return self.idMDI_

    """
    Establece widget como principal del formulario.

    Este widget contendrá componentes que quieran enlazar con la
    base de datos, por lo que esperan estar contenidos en una clase
    FLFormDB, la cual les proporciona el cursor (registros) a los que enlazar.
    Si ya existiera otro widget como principal, este será borrado.

    Si existe un widget principal establecido con anterioridad será borrado

    @param w Widget principal para el formulario
    """

    def setMainWidget(self, w=None) -> None:
        """
        if not w:
            if not self.cursor_:
                self.setMainWidget(
                    project.conn.managerModules().createForm(self.action_, self))
                return
            else:
                self.setMainWidget(self.cursor_.db().managerModules(
                ).createForm(self.action_.name, self))
                return
        elif isinstance(w, str):
            if not self.cursor_:
                self.setMainWidget(
                    project.conn.managerModules().createUI(self.action_, self))
                return
            else:
                self.setMainWidget(self.cursor_.db().managerModules(
                ).createUI(self.action_.name, self))
                return
        else:

            print("Creamos la ventana")

            if self.showed:
                if self.mainWidget_ and not self.mainWidget_ == w:
                    self.initMainWidget(w)
            else:
                w.hide()

            if self.layoutButtons:
                del self.layoutButtons

            if self.layout:
                del self.layout

            w.setFont(QtWidgets.QApplication.font())
            self.layout = QtWidgets.QVBoxLayout()
            self.layout.addWidget(w)
            self.layoutButtons = QtWidgets.QHBoxLayout()

            # pbSize = Qt.QSize(22,22)

            wt = QtWidgets.QToolButton.whatsThis()
            wt.setIcon(QtGui.QIcon(filedir("../share/icons", "gtk-find.png")))
            self.layoutButtons.addWidget(wt)
            wt.show()

            self.mainWidget_ = w

            # self.cursor_.setEdition(False)
            # self.cursor_.setBrowse(False)
            # self.cursor_.recordChoosed.emit(self.acepted)
        """
        self.mainWidget_ = self

    """
    Obtiene la imagen o captura de pantalla del formulario.
    """

    def snapShot(self) -> Any:
        pix = self.grab()
        return pix.toImage()

    """
    Salva en un fichero con formato PNG la imagen o captura de pantalla del formulario.

    @param pathFile Ruta y nombre del fichero donde guardar la imagen
    """

    def saveSnapShot(self, path_file=None) -> None:
        if not path_file:

            tmp_file = "%s/snap_shot_%s.png" % (aqApp.tmp_dir(), QtCore.QDateTime.currentDateTime().toString("ddMMyyyyhhmmsszzz"))

            ret = QFileDialog.getSaveFileName(QApplication.activeWindow(), "Pineboo", tmp_file, "PNG(*.png)")
            path_file = ret[0] if ret else None

        if path_file:
            fi = QtCore.QFile(path_file)
            if not fi.OpenMode(QtCore.QIODevice.WriteOnly):
                print("FLFormDB : Error I/O al intentar escribir el fichero", path_file)
                return

            self.snapShot().save(fi, "PNG")

    def saveGeometry(self) -> QtCore.QByteArray:
        # pW = self.parentWidget()
        # if not pW:
        geo = QtCore.QSize(self.width(), self.height())
        if self.isMinimized():
            geo.setWidth(1)
        elif self.isMaximized():
            geo.setWidth(9999)
        # else:
        #    geo = QtCore.QSize(pW.width(), pW.height())

        saveGeometryForm(self.geoName(), geo)
        return super().saveGeometry()

    """
    Establece el título de la ventana.

    @param text Texto a establecer como título de la ventana
    @author Silix
    """

    def setCaptionWidget(self, text) -> None:
        if not text:
            return

        self.setWindowTitle(text)

    """
    Devuelve si se ha aceptado el formulario
    """

    def accepted(self) -> bool:  # type: ignore   # FIXME: QDialog.accepted() is a signal. We're shadowing it.
        return self.accepted_

    """
    Devuelve el nombre de la clase del formulario en tiempo de ejecución
    """

    def formClassName(self) -> str:
        return "FormDB"

    """
    Sólo para compatibilizar con FLFormSearchDB. Por defecto sólo llama QWidget::show
    """

    def exec_(self) -> bool:
        super().show()
        return True

    def hide(self) -> None:
        super().hide()

    # public slots:

    """
    Cierra el formulario
    """

    @decorators.pyqtSlot()
    def close(self):
        if self.isClosing_:
            return True

        self.isClosing_ = True
        super(FLFormDB, self).close()
        self.isClosing_ = False

    """
    Se activa al pulsar el boton aceptar
    """

    @decorators.pyqtSlot()
    def accept(self):
        pass

    """
    Se activa al pulsar el botón cancelar
    """

    @decorators.pyqtSlot()
    def reject(self):
        pass

    """
    Redefinida por conveniencia

    @decorators.pyqtSlot()
    @decorators.NotImplementedWarn
    def show(self):
        return True
    """
    """
    Muestra el formulario sin llamar al script "init".
    Utilizado en documentación para evitar conflictos al capturar los formularios
    """

    @decorators.pyqtSlot()
    def showForDocument(self):
        self.showed = True
        self.mainWidget_.show()
        self.resize(self.mainWidget().size())
        super(FLFormDB, self).show()

    # """
    # Maximiza el formulario
    # """
    # @decorators.pyqtSlot()
    # @decorators.NotImplementedWarn
    # def setMaximized(self):
    #    return True

    """
    Muestra el script asociado al formulario en el Workbench para depurar
    """

    @decorators.pyqtSlot()
    @decorators.NotImplementedWarn
    def debugScript(self):
        return True

    """
    Devuelve el script asociado al formulario
    """

    @decorators.pyqtSlot()
    def get_script(self):
        ifc = self.iface
        if ifc:
            return str(ifc)
        return None

    # private slots:

    @decorators.pyqtSlot()
    def callInitScript(self):

        if not self.initScript():
            return

        if not self.isClosing_:
            QtCore.QTimer.singleShot(0, self.emitFormReady)

    def emitFormReady(self) -> None:
        from pineboolib.application.qsatypes.sysbasetype import SysBaseType

        qsa_sys = SysBaseType()
        if qsa_sys.isLoadedModule("fltesttest"):

            aqApp.call("fltesttest.iface.recibeEvento", ("formReady", self.actionName_), None)
        self.formReady.emit()

    # protected_:

    def emitFormClosed(self) -> None:
        from pineboolib.application import project

        if project.conn is None:
            raise Exception("Project is not connected yet")

        if "fltesttest" in project.conn.managerModules().listAllIdModules():
            project.call("fltesttest.iface.recibeEvento", ["formClosed", self.actionName_], None)

        self.formClosed.emit()
        if self.widget:
            self.widget.closed.emit()

    def action(self) -> FLAction:
        return self._action

    """
    Inicialización
    """

    def initForm(self) -> None:
        # acl = project.acl()
        acl = None  # FIXME: Add ACL later
        if acl:
            acl.process(self)

        self.loadControls()

        if self._action.table():
            if not self.cursor() or self.cursor()._action.table() is not self._action.table():
                from pineboolib.fllegacy.flsqlcursor import FLSqlCursor

                cursor = FLSqlCursor(self._action.table())
                self.setCursor(cursor)

            v = None

            preload_main_filter = getattr(self.iface, "preloadMainFilter", None)

            if preload_main_filter:
                v = preload_main_filter()

            if v is not None and self.cursor_:
                self.cursor_.setMainFilter(v, False)

            # if self._loaded and not self.__class__.__name__ == "FLFormRecordDB":
            # project.conn.managerModules().loadFLTableDBs(self)

            if self._action.description() not in ("", None):
                self.setWhatsThis(self._action.description())

            caption = self._action.caption()

            if caption in ("", None) and self.cursor() and self.cursor().metadata():
                caption = self.cursor().metadata().alias()

            if caption in ("", None):
                caption = "No hay metadatos"
            self.setCaptionWidget(caption)

    def loadControls(self) -> None:
        if self.pushButtonCancel:
            self.pushButtonCancel.hide()

        if self.bottomToolbar and self.toolButtonClose:
            self.toolButtonClose.hide()
        self.bottomToolbar = QtWidgets.QFrame()
        if self.iconSize is not None:
            self.bottomToolbar.setMinimumSize(self.iconSize)

        self.bottomToolbar.setLayout(QtWidgets.QHBoxLayout())
        self.bottomToolbar.setLayout(self.bottomToolbar.layout())
        self.bottomToolbar.layout().setContentsMargins(0, 0, 0, 0)
        self.bottomToolbar.layout().setSpacing(0)
        self.bottomToolbar.layout().addStretch()
        self.bottomToolbar.setFocusPolicy(QtCore.Qt.NoFocus)
        if self.layout_ is not None:
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

        if not self.pushButtonCancel:
            self.pushButtonCancel = QtWidgets.QToolButton()
            self.pushButtonCancel.setObjectName("pushButtonCancel")
            self.pushButtonCancel.clicked.connect(self.close)

        self.pushButtonCancel.setSizePolicy(sizePolicy)
        self.pushButtonCancel.setMaximumSize(pbSize)
        self.pushButtonCancel.setMinimumSize(pbSize)
        self.pushButtonCancel.setIcon(QtGui.QIcon(filedir("../share/icons", "gtk-stop.png")))
        # self.pushButtonCancel.setFocusPolicy(QtCore.Qt.StrongFocus)
        # self.pushButtonCancel.setFocus()
        self.pushButtonCancel.setShortcut(QKeySequence(self.tr("Esc")))
        self.pushButtonCancel.setWhatsThis("Cerrar formulario (Esc)")
        self.pushButtonCancel.setToolTip("Cerrar formulario (Esc)")
        self.bottomToolbar.layout().addWidget(self.pushButtonCancel)
        self.setFocusPolicy(QtCore.Qt.NoFocus)

    """
    Nombre interno del formulario
    """

    def formName(self) -> str:
        return "form%s" % self.idMDI_

    def name(self) -> str:
        return self.formName()

    def geoName(self) -> str:
        return self.formName()

    """
    Une la interfaz de script al objeto del formulario
    """

    def bindIface(self) -> None:

        if self.iface:
            self.oldFormObj = self.iface

    """
    Desune la interfaz de script al objeto del formulario
    """

    def unbindIface(self) -> None:
        if not self.iface:
            return

        self.iface = self.oldFormObj

    """
    Indica si la interfaz de script está unida al objeto formulario
    """

    def isIfaceBind(self) -> bool:
        if self.iface:
            return True
        else:
            return False

    """
    Captura evento cerrar
    """

    def closeEvent(self, e) -> None:
        self.frameGeometry()

        self.saveGeometry()
        self.setCursor(None)
        # self.closed.emit()
        self.hide()
        self.emitFormClosed()
        super().closeEvent(e)
        # self._action.mainform_widget = None
        self.deleteLater()
        self._loaded = False
        from pineboolib import pncontrolsfactory

        pncontrolsfactory.SysType().processEvents()

        # self.hide()
        try:
            # if hasattr(self.script, "form"):
            #    print("Borrando self.script.form", self.script.form)
            #    self.script.form = None
            if self.widget is not None and type(self).__name__ != "FLFormSearchDB":
                self.widget.close()
                self.widget = None
                # del self.widget

            # self.iface = None
            # del self.iface
            # if hasattr(self, "widget"):
            #    print("Borrando self.widget", self.widget)
            #    self.widget.close()
            #    del self.widget
            instance_name = (self.__class__, self._action.name())
            if instance_name in self.known_instances.keys():
                del self.known_instances[instance_name]

            # if hasattr(self, "script"):
            #    print("Borrando self.script", self.script)
            self.script = None
        except Exception:

            self.logger.error("El FLFormDB %s no se cerró correctamente:\n%s", self.formName(), traceback.format_exc())

        if isinstance(self.parent(), pncontrolsfactory.QMdiSubWindow):
            self.parent().close()

    """
    Captura evento mostrar
    """

    def showEvent(self, e) -> None:
        # --> Para mostrar form sin negro previo
        from PyQt5.QtWidgets import QMdiSubWindow
        from pineboolib.fllegacy.systype import SysType

        qsa_sys = SysType()

        qsa_sys.processEvents()
        # <--
        if not self.loaded():
            return

        if not self.showed:
            self.showed = True

            # self.initMainWidget()

            self.callInitScript()

            if not self._loaded:
                return

            self.bindIface()

        size = loadGeometryForm(self.geoName())
        if size:
            self.resize(size)

            if self.parent() and isinstance(self.parent(), QMdiSubWindow):
                self.parent().resize(size)
                self.parent().repaint()

    def cursorDestroyed(self, obj_=None) -> None:
        if not obj_:
            obj_ = self.sender()

        if not obj_ or obj_ is self.cursor_:
            return

        self.cursor_ = None

    """
    Captura evento ocultar


    def hideEvent(self, h):
        pW = self.parentWidget()
        if not pW:
            geo = QtCore.QSize(self.width(), self.height())
            if self.isMinimized():
                geo.setWidth(1)
            elif self.isMaximized():
                geo.setWidth(9999)
        else:
            geo = QtCore.QSize(pW.width(), pW.height())

        #saveGeometryForm(self.geoName(), geo)
    """
    """
    Captura evento de entrar foco
    """

    def focusInEvent(self, f) -> None:
        super().focusInEvent(f)
        if not self.isIfaceBind():
            self.bindIface()

    """
    Inicializa componenentes del widget principal

    @param w Widget a inicializar. Si no se establece utiliza
            por defecto el widget principal actual
    """

    def show(self):
        from pineboolib.qt3_widgets.qmdiarea import QMdiArea
        from PyQt5.QtWidgets import QMdiSubWindow
        from pineboolib.application import project

        module_name = getattr(project.actions[self._action.name()].mod, "module_name", None)
        if module_name:

            if module_name in aqApp._dict_main_widgets.keys():
                module_window = aqApp._dict_main_widgets[module_name]
                mdi_area = module_window.centralWidget()

                if isinstance(mdi_area, QMdiArea) and type(self).__name__ == "FLFormDB":
                    if not isinstance(self.parent(), QMdiSubWindow):
                        # size = self.size()
                        mdi_area.addSubWindow(self)

        if self.initFocusWidget_ is None:
            self.initFocusWidget_ = self.focusWidget()

        if self.initFocusWidget_:
            self.initFocusWidget_.setFocus()

        # if not self.tiempo_ini:
        #    self.tiempo_ini = time.time()
        super().show()
        # tiempo_fin = time.time()

        if self.parent().parent() is None:
            from PyQt5.QtWidgets import QDesktopWidget  # type: ignore # Centrado

            qt_rectangle = self.frameGeometry()
            center_point = QDesktopWidget().availableGeometry().center()
            qt_rectangle.moveCenter(center_point)
            self.move(qt_rectangle.topLeft())
        # if settings.readBoolEntry("application/isDebuggerMode", False):
        #    self.logger.warning("INFO:: Tiempo de carga de %s: %.3fs %s (iface %s)" %
        #                     (self.actionName_, tiempo_fin - self.tiempo_ini, self, self.iface))
        # self.tiempo_ini = None

    def initMainWidget(self, w=None) -> None:
        if not self.showed:
            self.show()

    @decorators.NotImplementedWarn
    def child(self, childName):
        return False

    # def __getattr__(self, name):
    # if getattr(self.script, "form", None):
    #    return getattr(self.script.form, name)
    # else:
    #    qWarning("%s (%s):No se encuentra el atributo %s" % (self, self.iface, name))

    @decorators.NotImplementedWarn
    def exportToXml(self, b):
        from pineboolib.fllegacy.aqsobjects.aqs import AQS

        xml = AQS().toXml(self, True, True)
        print(xml.toString(2))
        pass
