# -*- coding: utf-8 -*-

#Completa Si
import sip


# switch on QVariant in Python3
sip.setapi('QVariant', 2)
sip.setapi('QString', 1)

from PyQt4.QtCore import QtCore, QString, QVariant
from PyQt4.QtGui import QtGui
from PyQt4.Qt import Qt

from pineboolib.fllegacy.FLFormDB import FLFormDB
from pineboolib.fllegacy.FLSqlCursor import FLSqlCursor
from pineboolib.fllegacy.FLUtil import FLUtil
from pineboolib.fllegacy.FLSqlConnections import FLSqlConnections
from pineboolib.fllegacy.aqApp import aqApp






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
    Uso interno
    """
    acceptingRejecting_ = False
    inExec_ = False
    
    """
    Boton Aceptar
    """
    pushButtonAccept = None
    
    """
    Almacena si se ha abierto el formulario con el método FLFormSearchDB::exec()
    """
    loop = None


    def __init__(self,*args, **kwargs):
        if isinstance(args[0],QString):
            super(FLFormSearchDB,self).__init(args[0], args[1],(Qt.WStyle_Customize, Qt.WStyle_Maximize, Qt.WStyle_Title, Qt.WStyle_NormalBorder, Qt.WType_Dialog, Qt.WShowModal, Qt.WStyle_SysMenu))
            self.init1(args[0],args[1])
        else:
            super(FLFormSearchDB,self).__init(args[1], args[2],(Qt.WStyle_Customize, Qt.WStyle_Maximize, Qt.WStyle_Title, Qt.WStyle_NormalBorder, Qt.WType_Dialog, Qt.WShowModal, Qt.WStyle_SysMenu))
            self.init2(args[0],args[1],args[2])
    """
    constructor.

    @param actionName Nombre de la acción asociada al formulario
    """
    def init1(self, actionName, parent = None):
        self.setFocusPolicy(QtGui.QWidget.NoFocus)
        if actionName.isEmpty():
            self.action_ = False
            print(FLUtil.translate("app","FLFormSearchDB : Nombre de acción vacío"))
            return
        else:
            self.action_ = FLSqlConnections.database().manager().action(actionName)
        if not self.action_:
            print(FLUtil.translate("app","FLFormSearchDB : No existe la acción %s" % actionName))
            return
        
        self.cursor_ = FLSqlCursor(self.action_.table(), True,"default", 0, 0, self)
        self.name_ = self.action_.name()
        
        self.initForm()
            

    """ constructor sobrecargado.

    @param cursor Objeto FLSqlCursor para asignar a este formulario
    @param actionName Nombre de la acción asociada al formulario
    """
    def init2(self, cursor,actionName = QString.null, parent = None):
        self.setFocusPolicy(QtGui.QWidget.NoFocus)
        if actionName.isEmpty():
            self.action_ = False
        elif cursor:
            self.action_ = FLSqlConnections.database().manager().action(actionName)
        self.cursor_ = cursor 
        if self.action_:
            self.name_ = self.action_.name()
        else:
            self.name_ = QString.null 

    """
    destructor
    """
    def __del__(self):
        if self.cursor_ and not self.cursor_.aqWasDeleted():
            self.cursor_.restoreEditionFlag(self)
            self.cursor_.restoreBrowseFlag(self)

    """
    Establece el cursor que debe utilizar el formulario.

    @param c Cursor con el que trabajar
    """
    def setCursor(self, c):
        if not c == self.cursor_ and self.cursor_ and self.oldCursorCtxt:
            self.cursor_.setContext(self.oldCursorCtxt)
        
        if not c:
            return
        
        if self.cursor_:
            self.cursor_.recordChoosed.disconnect(self.accept())
            self.cursor_.destroyed.disconnect(self.cursorDestroyed())
        
        if self.cursor_ and not c == self.cursor_:
            self.cursor_.restoreEditionFlag(self)
            self.cursor_.restoreBrowseFlag(self)
        
        self.cursor_ = c
        self.cursor_.setEdition(False, self)
        self.cursor_.setBrowse(False, self)
        self.cursor_.recordChoosed.connect(self.accept())
        self.cursor_.destroyed.connect(self.cursorDestroyed())
        if self.iface and self.cursor_:
            self.oldCursorCtxt = self.cursor_.context()
            self.cursor_.setContext(self.iface)
        
    
    
    """
    Sobrecargado de setMainWidget.

    Aqui toma el nombre de un formulario de la acción asociada y construye el Widget principal, a partir de él.
    """    

    """
    Reimplementado, añade un widget como principal del formulario
    """
    def setMainWidget(self, *args, **kwargs):
        if len(args) == 0:
            super(FLFormSearchDB,self).setMainWidget()
        else:
            self.setMainWidgetFLFormSearhDB(args[0])
    
    def setMainWidgetFLFormSearchDB(self, w):
        if not self.cursor_ or not w:
            return
        if self.showed:
            if self.mainWidget_ and not self.mainWidget_ == w:
                self.initMainWidget(w)
        else:
            w.hide()
        
        if self.layoutButtons:
            del self.layoutButtons
        
        if self.layout:
            del self.layout 
        
        w.setFont(QtGui.qApp.font())
        desk = QtGui.QApplication.desktop.availableGeometry(self)
        geo = w.geometry()
        tooLarge = False
        
        if geo.width() > desk.width() or geo.height() > desk.heigh():
            sv = QtGui.QScrollArea(self)
            #sv->setResizePolicy(QScrollView::AutoOneFit) FIXME
            sv.hide()
            sv.addChild(w)
            self.layout = QtGui.QVBoxLayout(self, 5,5,"vlay" + self.name_)
            self.Layout.add(sv)
            sv.resize(self.size().expand(desk.size()))
            self.layoutButtons = QtGui.QHBoxLayout(self.layout, 3, "hlay" + self.name_)
            self.formReady.connect(sv.show())
            tooLarge = True
        else:
            self.layout = QtGui.QVBoxLayout(self, 2, 3, "vlay" + self.name_)
            self.layout.add(w)
            self.layoutButtons = QtGui.QHBoxLayout(self.layout, 3, "hlay" + self.name_)
            
        
        pbSize = Qt.qsize(22,22)
        """
        QToolButton *wt = QWhatsThis::whatsThisButton(this);
        wt->setIconSet(QPixmap::fromMimeSource("about.png"));
        layoutButtons->addWidget(wt);
        wt->show()
        """
        self.layoutButtons.addItem(QtGui.QSpacerItem(20,20, Qt.QSizePolicy.Expanding, Qt.QSizePolicy.Minimum))
        self.pushButtonAccept = QtGui.QPushButton(self,"pushButtonAccept")
        self.pushButtonAccept.sizePolicy(Qt.QSizePolicy(0,0,0,0, self.pushButtonAccept.sizePolicy().hasHeightForWidth()))
        self.pushButtonAccept.setMinimumSize(pbSize)
        self.pushButtonAccept.setMaximumSize(pbSize)
        ok = QtGui.QIcon(FLUtil.filedir("icons","button_ok.png"))
        self.pushButtonAccept.setIcon(ok)
        self.pushButtonAccept.setFocusPolicy(QtGui.QWidget.NoFocus)
        
        #pushButtonAccept->setAccel(QKeySequence(Qt::Key_F10)); FIXME
        self.pushButtonAccept.setDefault(True)
        #QToolTip::add(pushButtonAccept, tr("Seleccionar registro actual y cerrar formulario (F10)")); FIXME
        #QWhatsThis::add(pushButtonAccept, tr("Seleccionar registro actual y cerrar formulario (F10)")); FIXME
        self.layoutButtons.addWidget(self.pushButtonAccept)
        self.pushButtonAccept.clicked.connect(self.accept())
        
        self.pushButtonCancel = QtGui.QPushButton(self, "pushButtonCancel")
        self.pushButtonCancel.sizePolicy(Qt.QSizePolicy(0,0,0,0, self.pushButtonAccept.sizePolicy().hasHeightForWidth()))
        self.pushButtonCancel.setMinimumSize(pbSize)
        self.pushButtonCancel.setMaximumSize(pbSize)
        cancel = QtGui.QIcon(FLUtil.filedir("icons","button_cancel.png"))
        self.pushButtonAccept.setIcon(cancel)
        self.pushButtonCancel.setFocusPolicy(QtGui.QWidget.NoFocus)
        #pushButtonCancel->setAccel(QKeySequence(tr("Esc"))); #FIXME
        #QToolTip::add(pushButtonCancel, tr("Cerrar formulario sin seleccionar registro (Esc)")); #FIXME
        #QWhatsThis::add(pushButtonCancel, tr("Cerrar formulario sin seleccionar registro (Esc)")); #FIXME
        self.layoutButtons.addItem(QtGui.QSpacerItem(20,20, Qt.QSizePolicy.Fixed, Qt.QSizePolicy.Fixed))
        self.layoutButtons.addWidget(self.pushButtonCancel)
        self.pushButtonCancel.clicked.connect(self.reject())
        
        self.mainWidget_ = w
        self.cursor_.setEdition(False)
        self.cursor_.setBrowse(False)
        self.cursor_.recordChoosed.connect(self.accept())
        
        if not tooLarge:
            mWidth = self.mainWidget_.width()
            mHeight = self.mainWidget_.height()
            actWin = QtGui.qApp.activeWindow()
            if actWin:
                screen = actWin.geometry()
            else:
                screen = QtGui.qApp.mainWidget().geometry()
            p = screen.center() - Qt.QPoint(mWidth / 2, mHeight / 2)
            
            if p.x() + mWidth > desk.width():
                p.setx(desk.width() - mWidth)
            if p.y() + mHeight > desk.height():
                p.sety(desk.height() - mHeight)
            if p.x() < 0:
                p.setx(0)
            if p.y() < 0:
                p.sety(0)
            self.move(p)
            
    """
    Muestra el formulario y entra en un nuevo bucle de eventos
    para esperar, a seleccionar registro.

    Se espera el nombre de un campo del cursor
    devolviendo el valor de dicho campo si se acepta el formulario
    y un QVariant::Invalid si se cancela.

    @param n Nombre del un campo del cursor del formulario
    @return El valor del campo si se acepta, o QVariant::Invalid si se cancela
    """
    def exec(self, n = QString.null):
        if not self.cursor_:
            return QVariant()
        
        if self.loop and self.inExec_:
            print(FLUtil.translate("app","FLFormSearchDB::exec(): Se ha detectado una llamada recursiva"))
            self.QWidget.show()
            if self.initFocusWidget_:
                self.initFocusWidget_.setFocus()
            return QVariant()
        
        self.inExec_ = True
        self.acceptingRejecting_ = False
        
        self.QWidget.show()
        if self.initFocusWidget_:
            self.initFocusWidget_.setFocus()
        
        if self.iface:
            aqApp.call("init", self.QSArgumentList(), self.iface)
        
        #if (!isClosing_ && !aqApp->project()->interpreter()->hadError()) #FIXME
        #    QTimer::singleShot(0, this, SLOT(emitFormReady())); #FIXME
        
        self.accepted_ = False
        self.loop = True
        if not self.isClosing_ and not self.acceptingRejecting_:
            QtGui.QApplication.eventLoop().enterLoop()
        self.loop = False
        
        self.clearWFlags(Qt.WShowModal)
        v = None
        if self.accepted_ and not n.isEmpty():
            v = self.cursor_.valueBuffer(n)
        else:
            v = QVariant()
        
        self.inExec_ = False
        return v
        

    """
    Aplica un filtro al cursor
    """
    def setFilter(self, f):
        if not self.cursor_:
            return
        previousF = QString(self.cursor_.mainFilter())
        newF = QString(None)
        if previousF.isEmpty():
            newF = f
        elif previousF.contains(f):
            return
        else:
            newF = previousF + " AND " + f
        self.cursor_.setMainFilter(newF)
    

    """
    Devuelve el nombre de la clase del formulario en tiempo de ejecución
    """
    def formClassName(self):
        return "FormSearhDB"
        

    """
    Establece el título de la ventana.

    @param text Texto a establecer como título de la ventana
    @author Silix
    """
    def setCaptionWidget(self, text):
        if text.isEmpty():
            return 
        self.setCaption(text)
        

    """
    Nombre interno del formulario
    """
    def geoName(self):
        return QString("formSearch") + self.idMDI_

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
            self.closed()
            self.QWidget.closeEvent(e)
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
        
        self.QWidget.hide()
        if self.loop:
            self.loop = False
            QtGui.QApplication.eventLoop().exitLoop()

    """
    Se activa al pulsar el boton aceptar
    """
    @QtCore.pyqtSlot()
    def accept(self):
        if self.acceptingRejecting_:
            return
        self.frameGeometry()
        if self.cursor_:
            self.cursor_.recordChoosed.disconnect(self.accept())
            self.accepted_ = True
        
        self.acceptingRejecting_ = True
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
            self.cursor_.recordChoosed.disconnect(self.accept())
        self.acceptingRejecting_ = True
        self.hide()

    """
    Redefinida por conveniencia
    """
    @QtCore.pyqtSlot()
    def show(self):
        self.exec()
        




