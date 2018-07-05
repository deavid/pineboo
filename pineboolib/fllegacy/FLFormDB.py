# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import qWarning

from pineboolib.utils import filedir, loadGeometryForm, saveGeometryForm
from pineboolib import decorators
import pineboolib

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


class FLFormDB(QtWidgets.QDialog):

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
    layout = None

    """
    Widget principal del formulario
    """
    mainWidget_ = None

    """
    Acción asociada al formulario
    """
    action_ = None

    """
    Identificador de ventana MDI.

    Generalmente es el nombre de la acción que abre el formulario
    """
    idMDI_ = None

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
    accepted_ = None

    """
    Nombre del formulario relativo a la acción (form / formRecrd + nombre de la acción)
    """
    actionName_ = None

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
    cursorDestroyed = QtCore.pyqtSignal()

    # signals:

    """
    Señal emitida cuando se cierra el formulario
    """
    closed = QtCore.pyqtSignal()

    """
    Señal emitida cuando el formulario ya ha sido inicializado y está listo para usarse
    """
    formReady = QtCore.pyqtSignal()

    known_instances = {}
    cursor_ = None
    bottomToolbar = None
    pushButtonCancel = None

    _uiName = None
    _scriptForm = None
    ui_ = {}

    def __init__(self, parent, action, load=False):
        # if pineboolib.project._DGI.localDesktop():  # Si es local Inicializa
        #    super(QtWidgets.QWidget, self).__init__(parent)
        super(QtWidgets.QWidget, self).__init__(parent)

        try:
            assert (self.__class__, action) not in self.known_instances
        except AssertionError:
            print("WARN: Clase %r ya estaba instanciada, reescribiendo!. " % ((self.__class__, action),) +
                  "Puede que se estén perdiendo datos!")
        self.known_instances[(self.__class__, action)] = self

        self.ui_ = {}

        self.action = action
        if type(self).__name__ == "FLFormRecordDB":
            self.actionName_ = "formRecord" + action.name
        else:
            self.actionName_ = "form" + action.name

        self.mod = action.mod

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(1, 1, 1, 1)
        self.layout.setSpacing(1)
        self.layout.setContentsMargins(1, 1, 1, 1)
        self.layout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.setLayout(self.layout)
        if not self._uiName:
            self._uiName = action.form

        if not self._scriptForm and getattr(action, "scriptform", None):
            self._scriptForm = action.scriptform

        if not getattr(action, "alias", None):
            qWarning("FLFormDB::Cargando un action XML")
        elif pineboolib.project._DGI.localDesktop():
            self.setWindowTitle(action.alias)

        self.loaded = False
        self.idMDI_ = self.action.name

        self.script = None
        self.iface = None
        try:
            script = self._scriptForm or None
        except AttributeError:
            script = None
        self.action.load_script(script, self)

        self.iconSize = pineboolib.project._DGI.iconSize()

        if load:
            self.load()
            self.initForm()

    def load(self):
        if self.loaded:
            return

        # self.resize(550,350)
        self.layout.insertWidget(0, self.widget)
        self.layout.setSpacing(1)
        self.layout.setContentsMargins(1, 1, 1, 1)
        self.layout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)

        if self._uiName:
            pineboolib.project.conn.managerModules().createUI(self._uiName, None, self)

        self.loaded = True

    """
    Invoca a la función "init" del script "masterprocess" asociado al formulario
    """
    @QtCore.pyqtSlot()
    def initScript(self):
        if self.loaded:
            if not getattr(self.widget, "iface", None):
                self.iface = self.widget  # Es posible que no tenga ifaceCtx, así hacemos que sea polivalente

            if hasattr(self.iface, "init"):
                self.iface.init()
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

    def __del__(self):
        # TODO: Esto hay que moverlo al closeEvent o al close()
        # ..... los métodos __del__ de python son muy poco fiables.
        # ..... Se lanzan o muy tarde, o nunca.
        # (De todos modos creo que ya hice lo mismo a mano en el closeEvent en commits anteriores)

        self.unbindIface()

    def setCursor(self, cursor):
        self.cursor_ = cursor

    """
    Para obtener el cursor utilizado por el formulario.

    return Objeto FLSqlCursor con el cursor que contiene los registros para ser utilizados
      en el formulario
    """

    def cursor(self):
        return self.cursor_

    """
    Para obtener el widget principal del formulario.

    return Objeto QWidget que corresponde con el widget principal del formulario
    """

    def mainWidget(self):
        return self.mainWidget_

    """
    Establece el identificador MDI
    """

    def setIdMDI(self, id_):
        self.idMDI_ = id_

    """
    Obtiene el identificador MDI
    """

    def idMDI(self):
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

    def setMainWidget(self, w=None):
        if not w:
            if not self.cursor_:
                self.setMainWidget(
                    pineboolib.project.conn.managerModules().createForm(self.action_, self))
                return
            else:
                self.setMainWidget(self.cursor_.db().managerModules(
                ).createForm(self.action_.name, self))
                return
        elif isinstance(w, str):
            if not self.cursor_:
                self.setMainWidget(
                    pineboolib.project.conn.managerModules().createUI(self.action_, self))
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
    Obtiene la imagen o captura de pantalla del formulario.
    """

    def snapShot(self):
        pix = QtGui.QPixmap.grabWidget(self)
        return pix.convertToImage()

    """
    Salva en un fichero con formato PNG la imagen o captura de pantalla del formulario.

    @param pathFile Ruta y nombre del fichero donde guardar la imagen
    """

    def saveSnapShot(self, pathFile):

        fi = QtCore.QFile(pathFile)
        if not fi.OpenMode(QtCore.QIODevice.WriteOnly):
            print("FLFormDB : Error I/O al intentar escribir el fichero", pathFile)
            return

        self.snapShot().save(fi, "PNG")

    """
    Establece el título de la ventana.

    @param text Texto a establecer como título de la ventana
    @author Silix
    """

    def setCaptionWidget(self, text):
        if not text:
            return

        self.setWindowTitle(text)

    """
    Devuelve si se ha aceptado el formulario
    """

    def accepted(self):
        return self.accepted_

    """
    Devuelve el nombre de la clase del formulario en tiempo de ejecución
    """

    def formClassName(self):
        return "FormDB"

    """
    Sólo para compatibilizar con FLFormSearchDB. Por defecto sólo llama QWidget::show
    """

    def exec_(self):
        self.show()
        return True

    # public slots:

    """
    Cierra el formulario
    """
    @QtCore.pyqtSlot()
    def close(self):
        if self.isClosing_:
            return True
        self.isClosing_ = True
        super(FLFormDB, self).close()
        if not pineboolib.project._DGI.localDesktop():
            pineboolib.project._DGI._par.addQueque("%s_close" % self.__class__.__module__, None)

    """
    Se activa al pulsar el boton aceptar
    """
    @QtCore.pyqtSlot()
    def accept(self):
        pass

    """
    Se activa al pulsar el botón cancelar
    """
    @QtCore.pyqtSlot()
    def reject(self):
        pass

    """
    Redefinida por conveniencia

    @QtCore.pyqtSlot()
    @decorators.NotImplementedWarn
    def show(self):
        return True
    """
    """
    Muestra el formulario sin llamar al script "init".
    Utilizado en documentación para evitar conflictos al capturar los formularios
    """
    @QtCore.pyqtSlot()
    def showForDocument(self):
        self.showed = True
        self.mainWidget_.show()
        self.resize(self.mainWidget().size())
        super(FLFormDB, self).show()

    """
    Maximiza el formulario
    """
    @QtCore.pyqtSlot()
    @decorators.NotImplementedWarn
    def setMaximized(self):
        return True

    """
    Muestra el script asociado al formulario en el Workbench para depurar
    """
    @QtCore.pyqtSlot()
    @decorators.NotImplementedWarn
    def debugScript(self):
        return True

    """
    Devuelve el script asociado al formulario
    """
    @QtCore.pyqtSlot()
    def script(self):
        ifc = self.iface
        if ifc:
            return str(ifc)
        return None

    # private slots:

    @QtCore.pyqtSlot()
    def callInitScript(self):

        if not self.initScript():
            return

        if not self.isClosing_:
            QtCore.QTimer(self).singleShot(0, self.emitFormReady)

    def emitFormReady(self):
        self.formReady
        from pineboolib.pncontrolsfactory import SysType
        sys_ = SysType()
        if sys_.isLoadedModule('fltesttest'):
            self._prj.call("fltesttest.iface.recibeEvento", ("formReady", self.actionName_), None)

    # protected_:

    """
    Inicialización
    """

    def initForm(self):
        acl = pineboolib.project.acl()
        if acl:
            acl.process(self)

        self.loadControls()

        if self.loaded and not self.__class__.__name__ == "FLFormRecordDB":
            pineboolib.project.conn.managerModules().loadFLTableDBs(self)

        """
        if self.cursor_ and self.cursor_.metadata():
            caption = None
            if self.action_:
                #self.cursor_.setAction(self.action_)
                caption = self.action_.name
                if self.action.description:
                    self.setWhatsThis(self.action_.description)

                self.idMDI_ = self.action_.name

            if not caption:
                caption = self.cursor_.metadata().alias()

            self.setCaptionWidget(caption)

            #self.bindIface()
            #self.setCursor(self.cursor_)




        else:

            self.setCaptionWidget("No hay metadatos")

        """

    def loadControls(self):
        if self.pushButtonCancel:
            self.pushButtonCancel.hide()

        if self.bottomToolbar:
            self.toolButtonClose.hide()
        self.bottomToolbar = QtWidgets.QFrame()
        self.bottomToolbar.setMinimumSize(self.iconSize)

        self.bottomToolbar.layout = QtWidgets.QHBoxLayout()
        self.bottomToolbar.setLayout(self.bottomToolbar.layout)
        self.bottomToolbar.layout.setContentsMargins(0, 0, 0, 0)
        self.bottomToolbar.layout.setSpacing(0)
        self.bottomToolbar.layout.addStretch()
        self.bottomToolbar.setFocusPolicy(QtCore.Qt.NoFocus)
        self.layout.addWidget(self.bottomToolbar)
        # if self.layout:
        #    self.layout = None
        # Limpiamos la toolbar

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy(0), QtWidgets.QSizePolicy.Policy(0))
        sizePolicy.setHeightForWidth(True)

        pbSize = self.iconSize

        if not self.pushButtonCancel:
            self.pushButtonCancel = QtWidgets.QToolButton()
            self.pushButtonCancel.setObjectName("pushButtonCancel")
            self.pushButtonCancel.clicked.connect(self.close)

        self.pushButtonCancel.setSizePolicy(sizePolicy)
        self.pushButtonCancel.setMaximumSize(pbSize)
        self.pushButtonCancel.setMinimumSize(pbSize)
        self.pushButtonCancel.setIcon(
            QtGui.QIcon(filedir("../share/icons", "gtk-stop.png")))
        self.pushButtonCancel.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.pushButtonCancel.setFocus()
        self.pushButtonCancel.setWhatsThis("Aceptar y cerrar formulario (Esc)")
        self.pushButtonCancel.setToolTip("Aceptar y cerrar formulario (Esc)")
        self.bottomToolbar.layout.addWidget(self.pushButtonCancel)
        self.setFocusPolicy(QtCore.Qt.NoFocus)

    """
    Nombre interno del formulario
    """

    def formName(self):
        return "form%s" % self.idMDI_

    def name(self):
        return self.formName()

    def geoName(self):
        return self.formName()

    """
    Une la interfaz de script al objeto del formulario
    """

    def bindIface(self):

        if self.iface:
            self.oldFormObj = self.iface

    """
    Desune la interfaz de script al objeto del formulario
    """

    def unbindIface(self):
        if not self.iface:
            return

        self.iface = self.oldFormObj

    """
    Indica si la interfaz de script está unida al objeto formulario
    """

    def isIfaceBind(self):
        if self.iface:
            return True
        else:
            return False

    """
    Captura evento cerrar
    """

    def closeEvent(self, e):
        self.frameGeometry()
        if self.focusWidget():
            fdb = self.focusWidget().parentWidget()
            if fdb and getattr(fdb, "autoComFrame_", None):
                try:
                    if fdb.autoComFrame_.isvisible():
                        fdb.autoComFrame_.hide()
                        return
                except Exception:
                    print("closeEvent: Error al ocultar el frame")

        self.setCursor(None)
        self.closed.emit()

        super(FLFormDB, self).closeEvent(e)
        self.deleteLater()
        try:
            # self.script.form.close()
            self.script.form = None
            self.iface = None
            self.widget.close()
            del self.widget
        except Exception:
            pass

    """
    Captura evento mostrar
    """

    def showEvent(self, e):
        if not self.showed:
            self.showed = True
            v = None
            if self.cursor_ and self.iface:
                try:
                    v = self.iface.preloadMainFilter()
                except Exception:
                    pass

                if v:
                    self.cursor_.setMainFilter(v, False)

            self.initMainWidget()
            self.callInitScript()

            self.bindIface()

        size = loadGeometryForm(self.geoName())
        if size:
            self.resize(size)

    """
    Captura evento ocultar
    """

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

        saveGeometryForm(self.geoName(), geo)

    """
    Captura evento de entrar foco
    """

    def focusInEvent(self, f):
        super(FLFormDB, self).focusInEvent(f)
        if not self.isIfaceBind():
            self.bindIface()

    """
    Inicializa componenentes del widget principal

    @param w Widget a inicializar. Si no se establece utiliza
            por defecto el widget principal actual
    """

    def initMainWidget(self, w=None):
        if not self.showed:
            self.show()

    @decorators.NotImplementedWarn
    def child(self, childName):
        return False

    def __getattr__(self, name):
        if getattr(self.script, "form", None):
            return getattr(self.script.form, name)
        else:
            qWarning("%s:No se encuentra el atributo %s" %
                     (self.formClassName(), name))
