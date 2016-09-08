# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

from pineboolib.utils import filedir
from pineboolib import decorators


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

class FLFormDB(QtGui.QWidget):

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
    Interface para scripts
    """
    iface = None

    #protected slots:

    """
    Emite señal formulari listo. Ver FLFormDB::formReady()
    """
    emitFormReady = QtCore.pyqtSignal()

    """
    Uso interno
    """
    oldFormObjDestroyed = QtCore.pyqtSignal()
    cursorDestroyed = QtCore.pyqtSignal()

    #signals:

    """
    Señal emitida cuando se cierra el formulario
    """
    closed = QtCore.pyqtSignal()

    """
    Señal emitida cuando el formulario ya ha sido inicializado y está listo para usarse
    """
    formReady = QtCore.pyqtSignal()
    
    
    def __init__(self, *args, **kwargs):
        #super(FLFormDB, self).__init__(self, *args, **kwargs)
        


    """
    constructor
    """
    #explicit FLFormDB(QWidget *parent = 0, const char *name = 0, WFlags f = 0);

    """
    constructor.

    @param actionName Nombre de la acción asociada al formulario
    """
    #FLFormDB(const QString &actionName, QWidget *parent = 0, WFlags f = 0);

    """
    constructor sobrecargado.

    @param cursor Objeto FLSqlCursor para asignar a este formulario
    @param actionName Nombre de la acción asociada al formulario
    """
    #FLFormDB(FLSqlCursor *cursor, const QString &actionName = QString::null,
    #       QWidget *parent = 0, WFlags f = 0);

    """
    destructor
    """
    def __del__(self):
        print("FLform: Destructor")

    """
    Establece el cursor que debe utilizar el formulario.

    @param c Cursor con el que trabajar
    """
    @decorators.NotImplementedWarn
    def setCursor(self, c):
        return True

    """
    Para obtener el cursor utilizado por el formulario.

    return Objeto FLSqlCursor con el cursor que contiene los registros para ser utilizados
      en el formulario
    """
    def cursor(self):    
        return self.cursor_;


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
    @decorators.NotImplementedWarn
    def setMainWidget(self, w):
        return True


    """
    Obtiene la imagen o captura de pantalla del formulario.
    """
    @decorators.NotImplementedWarn
    def snapShot(self):
        return True

    """
    Salva en un fichero con formato PNG la imagen o captura de pantalla del formulario.

    @param pathFile Ruta y nombre del fichero donde guardar la imagen
    """
    @decorators.NotImplementedWarn
    def saveSnapShot(self, pathFile):
        return True

    """
    Establece el título de la ventana.

    @param text Texto a establecer como título de la ventana
    @author Silix
    """
    @decorators.NotImplementedWarn
    def setCaptionWidget(self, text):
        return True

    """
    Devuelve si se ha aceptado el formulario
    """
    def accepted(self):
        return self.accepted_

    """
    Devuelve el nombre de la clase del formulario en tiempo de ejecución
    """
    @decorators.NotImplementedWarn
    def formClassName(self):
        return True

    """
    Sólo para compatibilizar con FLFormSearchDB. Por defecto sólo llama QWidget::show
    """
    @decorators.NotImplementedWarn
    def exec(self, none):
        return True

    #public slots:

    """
    Cierra el formulario
    """
    @QtCore.pyqtSlot()
    @decorators.NotImplementedWarn
    def  close(self):
        return True
      

    """
    Invoca a la función "init" del script "masterprocess" asociado al formulario
    """
    @QtCore.pyqtSlot()
    @decorators.NotImplementedWarn
    def initScript(self):
        return True

    """
    Se activa al pulsar el boton aceptar
    """
    @QtCore.pyqtSlot()
    @decorators.NotImplementedWarn
    def accept(self):
        return True

    """
    Se activa al pulsar el botón cancelar
    """
    @QtCore.pyqtSlot()
    @decorators.NotImplementedWarn
    def reject(self):
        return True

    """
    Redefinida por conveniencia
    """
    @QtCore.pyqtSlot()
    @decorators.NotImplementedWarn
    def show(self):
        return True

    """
    Muestra el formulario sin llamar al script "init".
    Utilizado en documentación para evitar conflictos al capturar los formularios
    """
    @QtCore.pyqtSlot()
    @decorators.NotImplementedWarn
    def showForDocument(self):
        return True

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
    @decorators.NotImplementedWarn
    def script(self):
        return True

    #private slots:
    
    @QtCore.pyqtSlot()
    @decorators.NotImplementedWarn
    def callInitScript(self):
        return True

    #protected_:

    """
    Inicialización
    """
    @decorators.NotImplementedWarn
    def initForm(self):
        return True

    """
    Nombre interno del formulario
    """
    @decorators.NotImplementedWarn
    def formName(self):
        return True
    @decorators.NotImplementedWarn
    def geoName(self):
        return True

    """
    Une la interfaz de script al objeto del formulario
    """
    @decorators.NotImplementedWarn
    def bindIface(self):
        return True

    """
    Desune la interfaz de script al objeto del formulario
    """
    @decorators.NotImplementedWarn
    def unbindIface(self):
        return True

    """
    Indica si la interfaz de script está unida al objeto formulario
    """
    @decorators.NotImplementedWarn
    def isIfaceBind(self):
        return True

    """
    Captura evento cerrar
    """
    @decorators.NotImplementedWarn
    def closeEvent(self, e):
        return True

    """
    Captura evento mostrar
    """
    @decorators.NotImplementedWarn
    def showEvent(self, e):
        return True
    """
    Captura evento ocultar
    """
    @decorators.NotImplementedWarn
    def hideEvent(self, h):
        return True
        

    """
    Captura evento de entrar foco
    """
    @decorators.NotImplementedWarn
    def focusInEvent(self, f):
        return True

    """
    Inicializa componenentes del widget principal

    @param w Widget a inicializar. Si no se establece utiliza
            por defecto el widget principal actual
    """
    @decorators.NotImplementedWarn
    def initMainWidget(self, w = None):
        return True



#endif