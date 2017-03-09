# -*- coding: utf-8 -*-

from pineboolib.fllegacy.FLFormDB import FLFormDB
from pineboolib.fllegacy.FLSqlCursor import FLSqlCursor
from pineboolib import decorators
from pineboolib.utils import DefFun
from PyQt4 import QtCore, QtGui
from pineboolib.utils import filedir

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
    cursor_ = None
    
    eventloop = None
    """
    constructor.
    """


    
    def __init__(self, *args, **kwargs):
        parent = None
        name = None
        action = None
        
        if isinstance(args[0], str):
            #@param actionName Nombre de la acción asociada al formulario
            
            if len(args) == 2:
                parent = args[1]
            
            name = args[0]
             
            
            self.cursor_ = FLSqlCursor(name, True, "default", None, None, self)
            action = self.cursor_.action()
            self.accepted_ = False

        elif isinstance(args[0], FLSqlCursor):
            #@param cursor Objeto FLSqlCursor para asignar a este formulario
            #@param actionName Nombre de la acción asociada al formulario
            
            if len(args) > 2:
                action = args[1]
                name = action.name
                
            if len(args) == 3:
                parent = args[2]
            
            self.cursor_ = args[0]
        
        super(FLFormSearchDB,self).__init__(parent, action)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        
        if not name:
            print("FLFormSearchDB : Nombre de acción vacío")
            return
        
        if not action:
            print("FLFormSearchDB : No existe la acción", name)
            return


        
        self.initForm()
                    
        

  
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
    
    def initForm(self):
        super(FLFormSearchDB, self).initForm()
        
    
    def loadControls(self):
        
        self.bottomToolbar = QtGui.QFrame()
        self.bottomToolbar.setMaximumHeight(64)
        self.bottomToolbar.setMinimumHeight(16)
        self.bottomToolbar.layout = QtGui.QHBoxLayout()
        self.bottomToolbar.setLayout(self.bottomToolbar.layout)
        self.bottomToolbar.layout.setMargin(0)
        self.bottomToolbar.layout.setSpacing(0)
        self.bottomToolbar.layout.addStretch()
        self.bottomToolbar.setFocusPolicy(QtCore.Qt.NoFocus)
        self.layout.addWidget(self.bottomToolbar)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0) ,QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHeightForWidth(True)
        
        pbSize = QtCore.QSize(22,22)

  
                
                
            
        if not self.pushButtonAccept:
            self.pushButtonAccept = QtGui.QToolButton()
            self.pushButtonAccept.clicked.connect(self.accept)
                
        self.pushButtonAccept.setSizePolicy(sizePolicy)
        self.pushButtonAccept.setMaximumSize(pbSize)
        self.pushButtonAccept.setMinimumSize(pbSize)
        self.pushButtonAccept.setIcon(QtGui.QIcon(filedir("icons","gtk-save.png")))
        #pushButtonAccept->setAccel(QKeySequence(Qt::Key_F10)); FIXME
        self.pushButtonAccept.setFocus()
        self.pushButtonAccept.setWhatsThis("Seleccionar registro actual y cerrar formulario (F10)")
        self.pushButtonAccept.setToolTip("Seleccionar registro actual y cerrar formulario (F10)")
        self.pushButtonAccept.setFocusPolicy(QtCore.Qt.NoFocus)
        self.bottomToolbar.layout.addWidget(self.pushButtonAccept)
        self.pushButtonAccept.show()
                
            
        if not self.pushButtonCancel:
            self.pushButtonCancel = QtGui.QToolButton()
            self.pushButtonCancel.clicked.connect(self.reject)
                
        self.pushButtonCancel.setSizePolicy(sizePolicy)
        self.pushButtonCancel.setMaximumSize(pbSize)
        self.pushButtonCancel.setMinimumSize(pbSize)
        self.pushButtonCancel.setIcon(QtGui.QIcon(filedir("icons","gtk-stop.png")))
        self.pushButtonCancel.setFocusPolicy(QtCore.Qt.NoFocus)  
        #pushButtonCancel->setAccel(Esc); FIXME
        self.pushButtonCancel.setWhatsThis("Cerrar formulario sin seleccionar registro (Esc)")
        self.pushButtonCancel.setToolTip("Cerrar formulario sin seleccionar registro (Esc)")
        self.bottomToolbar.layout.addWidget(self.pushButtonCancel)
        self.pushButtonCancel.show()
        
        self.cursor_.setEdition(False)
        self.cursor_.setBrowse(False)
        self.cursor_.recordChoosed.connect(self.accept)                
            
                   
    
    def __getattr__(self, name): 
        return DefFun(self, name)

    
    
    """
    Muestra el formulario y entra en un nuevo bucle de eventos
    para esperar, a seleccionar registro.

    Se espera el nombre de un campo del cursor
    devolviendo el valor de dicho campo si se acepta el formulario
    y un QVariant::Invalid si se cancela.

    @param n Nombre del un campo del cursor del formulario
    @return El valor del campo si se acepta, o QVariant::Invalid si se cancela
    """
    @decorators.BetaImplementation
    def exec_(self, valor):
        if not self.cursor_:
            return None
        
        if not self.cursor_.isLocked():
            self.cursor_.setModeAccess(FLSqlCursor.Edit)
            
        if self.loop or self.inExec_:
            print("FLFormSearchDB::exec(): Se ha detectado una llamada recursiva")
            super(FLFormDB,self).show()
            if self.initFocusWidget_:
                self.initFocusWidget_.setFocus()
            
            return None
        
        self.load() #Extra
        self.inExec_ = True
        self.acceptingRejecting_ = False
        
        super(FLFormDB,self).show()
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
        
        self.accepted_ = False
        self.loop = True
        self.eventloop = QtCore.QEventLoop()      
        self.eventloop.exec_()
        
        #if not self.isClosing_ and not self.acceptingRejecting_:
            #QtCore.QEventLoop().enterLoop() FIXME
        
        self.loop = False
        
        #self.clearWFlags(WShowModal) FIXME
        
        v = None
        if self.accepted_ and valor:
            v = self.cursor_.valueBuffer(valor)
        else:
            v = None
        
        self.inExec_ = False   
        return v
                    

    """
    Aplica un filtro al cursor
    """
    def setFilter(self, f):

        if not self.cursor_:
            return
        previousF = self.cursor_.mainFilter()
        newF = None
        if not previousF:
            newF = f
        elif previousF.contains(f):
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
        if self.focusWidget():
            fdb = self.focusWidget().parentWidget()
            if fdb and fdb.autoComFrame_ and fdb.autoComFrame_.isvisible():
                fdb.autoComFrame_.hide()
                return
        
        if self.cursor_ and self.pushButtonCancel:
            if not self.pushButtonCancel.isEnabled():
                return
            
            self.isClosing_ = True
            self.setCursor(None)
        else:
            self.isClosing_ = True
        
        if self.isShown():
            self.reject()
        
        if self.isHidden():
            self.closed.emit()
            super(FLFormSearchDB, self).closeEvent(e)
            self.deleteLater()
            




    """
    Invoca a la función "init()" del script asociado al formulario
    """
    @QtCore.pyqtSlot()
    def initScript(self):
        return False

    """
    Redefinida por conveniencia
    """
    @QtCore.pyqtSlot()
    def hide(self):
        if self.isHidden():
            return
        
        super(FLFormSearchDB, self).hide()
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
            except:
                pass
        self.acceptingRejecting_ = True
        self.accepted_ = True
        self.hide()
        
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
            except:
                pass
        self.acceptingRejecting_ = True
        self.hide()

    
    """
    Redefinida por conveniencia
    """
    @QtCore.pyqtSlot()
    def show(self):
        self.exec_()





    def accepted(self):
        return self.accepted_
    
    def setMainWidget(self, w=None):
        
        if not self.cursor_:
            return
        
        if w:
            w.hide()
            self.mainWidget_ = w
        
