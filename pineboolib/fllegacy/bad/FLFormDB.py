# -*- coding: utf-8 -*-

from pineboolib.fllegacy.FLUtil import FLUtil
from pineboolib import decorators

from PyQt4 import QtGui, QtCore

from pineboolib.fllegacy.FLSqlCursor import FLSqlCursor
from pineboolib.fllegacy.FLSqlConnections import FLSqlConnections
from pineboolib.utils import filedir




class FLFormDB(QtGui.QWidget):
    
    
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

    #ifdef QSDEBUGGER
    """
    Boton Debug Script
    """
    pushButtonDebug = None
    #endif

    """
    Almacena que se aceptado, es decir NO se ha pulsado, botón cancelar
    """
    accepted_ = None

    """
    Interface para scripts
    """
    iface = None
    
    parent_= None
    

    @decorators.BetaImplementation
    def __init__(self, *args, **kwargs):
        if isinstance(args[0],FLSqlCursor):
            QtGui.QWidget.__init__(self, args[2])
            self.inicialize3(args, kwargs)
        elif isinstance(args[0], QtGui.QWidget):
            QtGui.QWidget.__init__(self, args[0])
            self.inicialize1(args,kwargs)
        else:
            QtGui.QWidget.__init__(self, args[1])
            self.inicialize2(args,kwargs)
        
            
        
    """
    constructor
    """
    @decorators.BetaImplementation
    def inicialize1(self, *args, **kwargs):            
        parent = args[0][0]
        name = args[0][1]
        f = args[1]
        
        if parent:
            self.parent_ = parent
        else:
            self.parent_ = QtGui.QWidget(pineboolib.project.mainWidget(), name, f)
        
        self.cursor_ = None
        self.layout = None
        self.mainWidget_ = None
        self.layoutButtons = None
        self.pushButtonCancel = None
        self.showed = False
        self.iface = None
        self.oldCursorCtxt = None
        self.isClosing_ = False
        self.initFocusWidget_ = None
        self.oldFormObj = None
        self.accepted_ = False
        self.loaded = False
        
    
    

    """
    constructor.

    @param actionName Nombre de la acción asociada al formulario
    """
    @decorators.BetaImplementation
    def inicialize2(self,*args, **kwargs):
        actionName = str(args[0][0])
        parent = args[0][1]
        f = args[1]

        if parent:
            self.parent_ = parent
        else:
            self.parent_ = QtGui.QWidget(pineboolib.project.mainWidget(), actionName, f)

        self.layout = None
        self.mainWidget_ = None
        self.layoutButtons = None
        self.pushButtonCancel = None
        self.showed = False
        self.iface = None
        self.oldCursorCtxt = None
        self.isClosing_ = False
        self.initFocusWidget_ = None
        self.oldFormObj = None
        self.accepted_ = False
    
        self.setFocusPolicy(QtGui.QWidget.NoFocus)
    
        if actionName.isEmpty():
            self.action_ = None
            print(FLUtil.translate("sys","FLFormDB : Nombre de acción vacío"))
            return
        else:
            self.action_ = FLSqlConnections.database().manager().action(actionName)
        
        if not self.action_:
            print(FLUtil.translate("sys","FLFormDB : No existe la acción %s" % actionName))
            return
        
        self.cursor_ = FLSqlCursor(self.action_.table(), True, "default", 0, 0, self)
        self.name_ = self.action_.name()
        
        self.initForm()
        
        

    """
    constructor sobrecargado.

    @param cursor Objeto FLSqlCursor para asignar a este formulario
    @param actionName Nombre de la acción asociada al formulario
    """
    @decorators.BetaImplementation
    def inicialize3(self, *args, **kwargs):
        
        cursor = args[0]
        actionName = args[1]
        parent = args[2]
        f = args[3]
        
        self.cursor_ = cursor
        self.layout = None
        self.mainWidget_ = None
        self.layoutButtons = None
        self.pushButtonCancel = None
        self.showed = False
        self.iface = None
        self.oldCursorCtxt = None
        self.isClosing_ = False
        self.initFocusWidget_ = None
        self.oldFormObj = None
        self.accepted_ = False
        


        if parent:
            self.parent_ = QtGui.QWidget(parent)
        else:
            self.parent_ = QtGui.QWidget(pineboolib.project.mainWidget(), actionName, f)
        
        self.setFocusPolicy(QtGui.QWidget.NoFocus)
        
        if actionName.isEmpty():
            self.action_ = None
        elif cursor:
            self.action_ = cursor.db().manager().action(actionName)
        else:
            self.action =  FLSqlConnections.database().manager().action(actionName)
        
        if self.action_:
            self.name_ = self.action_.name()
            
      

    """
    destructor
    """
    @decorators.BetaImplementation
    def __del__(self):
        self.unbindIface()

    """
    Establece el cursor que debe utilizar el formulario.

    @param c Cursor con el que trabajar
    """
    @decorators.BetaImplementation
    def setCursor(self, *c):
        if not c == self.cursor_ and self.cursor_ and self.oldCursorCtxt:
            self.cursor_.setContext(self.oldCursorCtxt)
        
        if not c:
            return
        
        if self.cursor_:
            self.cursor_.destroyed.disconnect(self.cursorDestroyed)
        
        self.cursor_ = c 
        self.cursor_.destroyed.connect(self.cursorDestroyed)
        
        if self.iface and self.cursor_:
            self.oldCursorCtxt = self.cursor_.context()
            self.cursor_.setContext(self.iface)    

    """
    Para obtener el cursor utilizado por el formulario.

    return Objeto FLSqlCursor con el cursor que contiene los registros para ser utilizados
      en el formulario
    """
    @decorators.BetaImplementation
    def cursor(self):
        return self.cursor_

    """
    Para obtener el widget principal del formulario.

    return Objeto QWidget que corresponde con el widget principal del formulario
    """
    @decorators.BetaImplementation
    def mainWidget(self):
        return self.mainWidget_

    """
    Establece el identificador MDI
    """
    @decorators.BetaImplementation
    def setIdMDI(self, _id):
        self.idMDI_ = _id

    """
    Obtiene el identificador MDI
    """
    @decorators.BetaImplementation
    def idMDI(self):
        return self.idMDI_
    
    
    
    @decorators.BetaImplementation
    def setMainWidget(self, *args, **kwarg):
        if isinstance(args[0], QtGui.QWidget):
            self.setMainWidgetQWidget(args[0])
        elif isinstance(args[0], str):
            self.setMainWidgetString(args[0])
        else:
            self.setMainWidgetEmpty()
            

    """
    Establece widget como principal del formulario.

    Este widget contendrá componentes que quieran enlazar con la
    base de datos, por lo que esperan estar contenidos en una clase
    FLFormDB, la cual les proporciona el cursor (registros) a los que enlazar.
    Si ya existiera otro widget como principal, este será borrado.

    Si existe un widget principal establecido con anterioridad será borrado

    @param w Widget principal para el formulario
    """
    @decorators.BetaImplementation
    def setMainWidgetQWidget(self, *w):
        
        if not self.cursor_ and not w:
            return
        
        if self.showed:
            if self.mainWidget_ and not self.mainWidget_ == w:
                self.initMainWidget(w)
            else:
                w.hide()
            
            if self.layout:
                del self.Layout
            
            #w.setFont(qApp.font()) #FIXME
            self.layout = QtGui.QVBoxLayout(self, 2,3,"vlay" + self.name_)
            self.layout.add(w)
            self.layoutButtons = QtGui.QHBoxLayout(self.layout , 3, "hlay" + self.name_)
            
            self.layoutButtons.addItem(QtGui.QSpacerItem())
            self.pushButtonCancel = QtGui.QPushButton(self, "pushButtonCancel")
            #self.pushButtonCancel.set_size(QtGui.QSizePolicy) #FIXME
            self.pushButtonCancel.setMinimumSize(22, 22)
            self.pushButtonCancel.setMaximumSize(22, 22)
            self.pushButtonCancel.setIcon(QtGui.QIcon(filedir("icons","gtk-cancel.png")))
            #pushButtonCancel->setFocusPolicy(QWidget::NoFocus);
            #pushButtonCancel->setAccel(QKeySequence(tr("Esc")));
            #QToolTip::add(pushButtonCancel, tr("Cerrar formulario (Esc)"));
            #QWhatsThis::add(pushButtonCancel, tr("Cerrar formulario (Esc)"));
            self.layoutButtons.addWidget(self.pushButtonCancel)
            self.pushButtonCancel.clicked.connect(self.close)
            self.pushButtonCancel.show()
            self.mainWidget_ = w

    """
    Sobrecargado de setMainWidget.

    Aqui toma el nombre de un formulario de la acción asociada y construye el Widget principal, a partir de él.
    """
    @decorators.BetaImplementation
    def setMainWidgetEmpty(self):
        if not self.action_:
            return
    
        if self.cursor_:
            self.setMainWidgetQWidget(self.cursor_.db().managerModules.createUI(self.action_, self, self))
        else:
            self.setMainWidget(FLSqlConnections.database().managerModules().createUI(self.action_, self, self))

    """
    Sobrecargado de setMainWidget.

    Aqui construye el Widget principal a partir del nombre de un fichero de interfaz .ui.

    @param uiFileName Nombre del fichero de descripción de interfaz, incluyendo la extension .ui, p.e. clientes.ui
    """
    @decorators.BetaImplementation
    def setMainWidgetString(self, uiFileName):
        if self.cursor_:
            self.setMainWidgetQWidget(self.cursor_.db().managerModules.createUI(uiFileName, self, self))
        else:
            self.setMainWidget(FLSqlConnections.database().managerModules().createUI(uiFileName, self, self))
    """
    Obtiene la imagen o captura de pantalla del formulario.
    """
    @decorators.BetaImplementation
    def snapShot(self):
        pix = QtGui.QPixmap.grabWidget(self)
        return QtGui.QImage(pix)
    

    """
    Salva en un fichero con formato PNG la imagen o captura de pantalla del formulario.

    @param pathFile Ruta y nombre del fichero donde guardar la imagen
    """
    @decorators.BetaImplementation
    def saveSnapShot(self, pathFile):
        fi = QtCore.QFile(pathFile)
        if not fi.open(QtCore.QFile.WriteOnly):
            print("FLFormDB : " + FLUtil.translate("sys", "Error I/O al intentar escribir el fichero %s" % pathFile))
            return
        self.snapShot().save(fi, "PNG")
            

    """
    Establece el título de la ventana.

    @param text Texto a establecer como título de la ventana
    @author Silix
    """
    @decorators.BetaImplementation
    def setCaptionWidget(self, text):
        if text.isEmpty():
            return
        
        self.setCaption(text)


    """
    Devuelve si se ha aceptado el formulario
    """
    @decorators.BetaImplementation
    def accepted(self):
        return self.accepted_

    """
    Devuelve el nombre de la clase del formulario en tiempo de ejecución
    """
    @decorators.BetaImplementation
    def formClassName(self):
        return "FormDB"

    """
    Sólo para compatibilizar con FLFormSearchDB. Por defecto sólo llama QWidget::show
    """
    @decorators.BetaImplementation
    def exec_(self):
        QtGui.QWidget.show()
        return QtCore.QVariant()
        
        
    #public slots:

    """
    Cierra el formulario
    """
    @decorators.BetaImplementation
    def close(self):
        if self.isClosing_:
            return True
        self.isClosing_ = True
        self.isClosing_ = QtGui.QWidget.close()

    """
    Invoca a la función "init" del script "masterprocess" asociado al formulario
    """
    @decorators.NotImplementedWarn
    def initScript(self):
        if self.iface:
            #pineboolib.project.call("init", QtCore.QSArgumentList(), self.iface) #FIXME
            return True
        else:
            return False
        

    """
    Se activa al pulsar el boton aceptar
    """
    @decorators.BetaImplementation
    def accept(self):
        return

    """
    Se activa al pulsar el botón cancelar
    """
    @decorators.BetaImplementation
    def reject(self):
        return

    """
    Redefinida por conveniencia
    """
    @decorators.BetaImplementation
    def show(self):
        QtGui.QWidget.show()

    """
    Muestra el formulario sin llamar al script "init".
    Utilizado en documentación para evitar conflictos al capturar los formularios
    """
    @decorators.BetaImplementation
    def showForDocument(self):
        self.showed = True
        self.mainWidget_.show()
        self.resize(self.size().expandedTo(self.mainWidget_.size()))
        QtGui.QWidget.show()

    """
    Maximiza el formulario
    """
    @decorators.BetaImplementation
    def setMaximized(self):
        self.setWindowState(self.windowState() | QtCore.Qt.WindowMaximized)

    """
    Muestra el script asociado al formulario en el Workbench para depurar
    """
    @decorators.BetaImplementation
    def debugScript(self):
        return

    """
    Devuelve el script asociado al formulario
    """
    @decorators.BetaImplementation
    def script(self):
        return

    #private slots:
    @decorators.BetaImplementation
    def callInitScript(self):
        if not self.initScript():
            return
        if not self.isClosing_:
            self.emitFormReady.emit()

    #protected:

    """
    Inicialización
    """
    @decorators.BetaImplementation
    def initForm(self):
        if self.cursor_ and self.cursor_.metadata():
            caption = None
            if self.action_:
                self.cursor_.setAction(self.action_)
                caption = self.action_.caption()
                if not self.action_.description().isEmpty():
                    self.QtGui.QWhatsThis.add(self, self.action_.description())
                self.idMDI_ = self.action_.name()
            
            if caption.isEmpty():
                caption = self.cursor_.metadata().alias()
            self.setCaption(caption)
            
            self.bindIface()
            self.setCursor(self.cursor_)
        
        else:
            self.setCaption(FLUtil.translate("sys" ,"No hay metadatos"))
            
                    

    """
    Nombre interno del formulario
    """
    @decorators.BetaImplementation
    def formName(self):
        return ("form%s" % self.idMDI_)
    
    @decorators.BetaImplementation
    def geoName(self):
        return self.formName()

    """
    Une la interfaz de script al objeto del formulario
    """
    @decorators.BetaImplementation
    def bindIface(self):
        p = pineboolib.project
        
        if not p:
            return
        
        self.setName(self.formName())
        o = p.object(self.name())
        
        if not o == self.iface and self.iface and self.oldFormObj:
            self.iface.setObj(self.oldFormObj)
        self.iface = o
        
        ifc = self.iface
        if not ifc:
            return
        
        if not ifc.obj() == self:
            if self.oldFormObj:
                self.oldFormObj.destroyed.disconnect(self.oldFormObjDestroyed())
            
            self.oldFormObj = ifc.obj()
            if self.oldFormObj:
                self.oldFormObj.destroyed.connect(self.oldFormObjDestroyed())
            ifc.setObj(self) 
        

    """
    Desune la interfaz de script al objeto del formulario
    """
    @decorators.BetaImplementation
    def unbindIface(self):
        ifc = self.iface
        if not ifc:
            return
        
        if ifc.obj() == self:
            ifc.setObj(self.oldFormObj) 

    """
    Indica si la interfaz de script está unida al objeto formulario
    """
    @decorators.BetaImplementation
    def isIfaceBind(self):
        ifc = self.iface
        if not ifc:
            return
        return (ifc.obj() == self)

    """
    Captura evento cerrar
    """
    @decorators.BetaImplementation
    def closeEvent(self, *e):
        self.frameGeometry()
        if self.focusWidget():
            fdb = self.focusWidget().parentWidget()
            if fdb and fdb.autoComFrame_ and fdb.autoComFrame_.isVisible():
                fdb.autoComFrame_.hide()
                return 
            

    """
    Captura evento mostrar
    """
    @decorators.NotImplementedWarn
    def showEvent(self, *e):
        if not self.showed and self.mainWidget_:
            self.showed = True
        
            if self.cursor_ and self.iface:
                #v = pineboolib.project.call("preloadMainFilter", QSArgumentList(), self.iface).variant())
                if v and isinstance(v.type(), str):
                    self.cursor_.setMainFilter(str(v), False)
        
            self.initMainWidget()
            self.callInitScript()
        if not self.isIfaceBind():
            self.bindIface()
    """
    Captura evento ocultar
    """
    @decorators.NotImplementedWarn
    def hideEvent(self, *h):
        return     
    """
    {
  QWidget *pW = parentWidget();
  if (pW && pW->isA("QWorkspaceChild")) {
    QRect geo(pW->x(), pW->y(), pW->width(), pW->height());
    if (isMinimized()) {
      geo.setWidth(1);
      aqApp->saveGeometryForm(geoName(), geo);
    } else if (isMaximized()) {
      geo.setWidth(9999);
      aqApp->saveGeometryForm(geoName(), geo);
    } else
      aqApp->saveGeometryForm(geoName(), geo);
  } else {
    QRect geo(x(), y(), width(), height());
    aqApp->saveGeometryForm(geoName(), geo);
  }
}
    """

    """
    Captura evento de entrar foco
    """
    @decorators.BetaImplementation
    def focusInEvent(self, *f):
        self.focusInEvent(f)
        if self.isIfaceBind():
            self.bindIface()

    """
    Inicializa componenentes del widget principal

    @param w Widget a inicializar. Si no se establece utiliza
            por defecto el widget principal actual
    """
    @decorators.NotImplementedWarn
    def initMainWidget(self, *w):
        return
    """
    
{
  QWidget *mWidget = w ? w : mainWidget_;
  if (mWidget) {
    QObjectList *l = static_cast<QObject *>(mWidget)->queryList("FLTableDB");
    QObjectListIt itt(*l);
    FLTableDB *tdb;
    while ((tdb = static_cast<FLTableDB *>(itt.current())) != 0) {
      ++itt;
      tdb->initCursor();
    }
    delete l;

    l = static_cast<QObject *>(mWidget)->queryList("FLFieldDB");
    QObjectListIt itf(*l);
    FLFieldDB *fdb;
    while ((fdb = static_cast<FLFieldDB *>(itf.current())) != 0) {
      ++itf;
      fdb->initCursor();
      fdb->initEditor();
      if (fdb->aqFirstTabStop == 1)
        initFocusWidget_ = fdb;
    }

    while (mWidget->parentWidget() && mWidget->parentWidget() != this)
      mWidget = mWidget->parentWidget();
    mWidget->show();

    FLAccessControlLists *acl = aqApp->acl();
    if (acl)
      acl->process(this);

    QWidget *pW = parentWidget();
    QRect desk;
    bool parentIsDesktop = true;
    
    if (!(pW && pW->isA("QWorkspaceChild"))) {
        desk = QApplication::desktop()->availableGeometry(this);
        pW = this;
    } else {
        desk = pW->parentWidget()->rect();
        parentIsDesktop = false;
    }

    QRect geo(aqApp->geometryForm(QObject::name()));
    pW->show();
    QSize oSz = mWidget->size();
    mWidget->updateGeometry();
    QSize bSz = mWidget->baseSize();
    QSize SzH = mWidget->sizeHint();
    int border = 5, border_b = 48;
    /*
    qDebug("geo: " + QString::number(geo.width()) + "x"  + QString::number(geo.height()));
    qDebug("oSz: " + QString::number(oSz.width()) + "x"  + QString::number(oSz.height()));
    qDebug("bSz: " + QString::number(bSz.width()) + "x"  + QString::number(bSz.height()));
    qDebug("SzH: " + QString::number(SzH.width()) + "x"  + QString::number(SzH.height()));
    */

    if (geo.width() < 100 || geo.width()>9000) {
        // qDebug(" -- reset Form Size and position -- ");
        geo.setWidth(oSz.width());
        geo.setHeight(oSz.height());
        geo.moveCenter(desk.center());
        
        if (!parentIsDesktop) {
            geo.moveTop(desk.top() + border - geo.top()+1);
        }
    }

    if (geo.width() < SzH.width()) {
        // qDebug(" -- geo width too small -- ");
        geo.setWidth(SzH.width());
    }
    if (geo.height() < SzH.height()) {
        // qDebug(" -- geo height too small -- ");
        geo.setHeight(SzH.height());
    }
    // Exceeds available horizontal area:
    if (geo.width() > desk.width() - border * 2) {
        // qDebug(" -- geo width too big -- ");
        geo.setWidth(desk.width() - border * 2 - 5);
    }
    // Exceeds available vertical area:
    if (geo.height() > desk.height() - border - border_b) {
        // qDebug(" -- geo height too big -- ");
        geo.setHeight(desk.height() - border - border_b - 5);
    }
    if (parentIsDesktop) {
        // Invalid position values, re-center
        if (  geo.right() > 9000
         || geo.left() < 1
         || geo.bottom() > 9000
         || geo.top() < 1 ) {
            // qDebug(" -- geo invalid position -- ");
            geo.moveCenter(desk.center());
        }
    

        if ( geo.top() < desk.top() + border)  {
            // qDebug(" -- geo position too high -- ");
            geo.moveTop(desk.top() + border - geo.top()+1);
        }

        if ( geo.left() < desk.left() + border) {
            // qDebug(" -- geo position too left -- ");
            geo.moveLeft(desk.left() + border - geo.left()+1);
        }

        if ( geo.bottom() > desk.bottom() - border_b ) {
            int diff = geo.bottom() - desk.bottom() - border_b;
            // qDebug(" -- geo position too low -- ");
            geo.moveTop(-diff-1);
        }

        if ( geo.right() > desk.right() - border) {
            int diff = geo.right() - desk.right() - border;
            // qDebug(" -- geo position too right -- ");
            geo.moveLeft(-diff-1);
        }

        // Outside of screen, re-center:
        if (  geo.right() > desk.right() - border  
         || geo.left() < desk.left() + border
         || geo.bottom() > desk.bottom() - border_b
         || geo.top() < desk.top() + border ) {
            // qDebug(" -- geo position out of screen -- ");
            geo.moveCenter(desk.center());
        }
    }
    mWidget->resize(geo.size());

    pW->updateGeometry();
    QSize tSz= pW->size();
    QSize tSzH = pW->sizeHint();
    if (tSz.width() < tSzH.width()) {
        tSz.setWidth(tSzH.width());
    }
    if (tSz.height() < tSzH.height()) {
        tSz.setHeight(tSzH.height());
    }
    pW->resize(tSz.expandedTo(mWidget->size()));
    
    pW->move(geo.topLeft());

    if (!initFocusWidget_) {
      itf.toFirst();
      while ((fdb = static_cast<FLFieldDB *>(itf.current())) != 0) {
        ++itf;
        if (fdb->isEnabled()) {
          initFocusWidget_ = fdb;
          break;
        }
      }
      if (!initFocusWidget_)
        initFocusWidget_ = static_cast<QWidget *>(mWidget->focusWidget());
      if (initFocusWidget_)
        initFocusWidget_->setFocus();
    }

    delete l;

    QWidget *focWid = qApp->focusWidget();
    if (focWid) {
      QWidget *topWidget = focWid->topLevelWidget();
      if (topWidget && !topWidget->inherits("FLFormDB")) {
        QWidget *topWid = focWid->parentWidget();
        while (topWid && !topWid->inherits("FLFormDB"))
          topWid = topWid->parentWidget();
        topWidget = topWid;
      }
      if (topWidget != this)
        setFocus();
    } else setFocus();
    
  }
}

"""
        
    #protected slots:

    """
    Emite señal formulari listo. Ver FLFormDB::formReady()
    """
    
    emitFormReady = QtCore.pyqtSignal()

    """
    Uso interno
    """
    @QtCore.pyqtSlot()
    def oldFormObjDestroyed(self):
        print("oldFormObjDestroyed")
        self.oldFormObj = None
        return None
        
    @QtCore.pyqtSlot(QtCore.QObject)
    def cursorDestroyed(self, *obj):
        print("cursorDestroyed")
        if not obj or not obj == self.cursor_:
            return
        
        self.cursor_ = None
        return None

    #signals:

    """
    Señal emitida cuando se cierra el formulario
    """
    closed = QtCore.pyqtSignal() 

    """
    Señal emitida cuando el formulario ya ha sido inicializado y está listo para usarse
    """
    formReady = QtCore.pyqtSignal()


#endif
