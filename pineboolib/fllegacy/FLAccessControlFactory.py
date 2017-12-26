# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets

from pineboolib.flcontrols import ProjectClass
from pineboolib.fllegacy.FLFieldMetaData import FLFieldMetaData
from pineboolib.fllegacy.FLTableMetaData import FLTableMetaData
from pineboolib.fllegacy.FLAccessControl import FLAccessControl
from pineboolib.fllegacy.FLFormDB import FLFormDB
from pineboolib.fllegacy.FLUtil import FLUtil
from pineboolib import decorators
from PyQt5.Qt import qApp

try:
    QString = unicode
except NameError:
    # Python 3
    QString = str

class FLAccessControlFactory(ProjectClass):
    
    def __init__(self):
        super(FLAccessControlFactory, self).__init__()
    
    @decorators.BetaImplementation
    def create(self, type_):
        if type_ == None:
            return False
        
        if type_ == "mainwindow":
            return FLAccessControlMainWindow()
        elif type_ == "form":
            return FLAccessControlForm()
        elif type_ == "table":
            return FLAccessControlTable()
        
        return False
    @decorators.BetaImplementation
    def type(self, obj):
        if not obj:
            print("NO OBJ")
        
        if obj == QtWidgets.QMainWindow:
            return "mainwindow"
        if obj == FLTableMetaData:
            return "table"
        if obj == FLFormDB:
            return "form"
        
        return QString("")
    
        
class FLAccessControlMainWindow(FLAccessControl):

    acosPerms_ = None
    perm_ = None
    
    def __init__(self):
        super(FLAccessControlForm, self).__init__()
    
    """
  Dado un objeto general (tipo QObject) de alto nivel, identifica si existe un controlador que puede controlar
  su acceso devolviendo en tal caso el nombre de tipo asignado.

  @param Objeto de alto nivel del cual se quiere conocer su tipo.
  @return Devuelve el nombre del tipo asociado al objeto de alto nivel dado, si existe controlador de acceso para él,
  en caso contrario devuelve una cadena vacía.
    """
    @decorators.BetaImplementation
    def type(self):
        return "mainwindow"
    
    @decorators.BetaImplementation
    def processObject(self, obj):
        mv = QMainWindow(obj)
        if not mw or not self.acosPerms_:
            return
        
        if not self.perm_.isEmpty():
            l = QtCore.QObjectList(mw.queryList("QAction"))
            ito = QtCore.QObjectListIt(l)
            a = QtCore.QAction
            
            while not ito.current() == 0:
                a = ito.current()
                ++ito
                if self.acosPerm_[a.name()]:
                    continue
                if self.perm_ == "-w" or self.perm_ == "--":
                    a.setVisible(False)
            
            del l
        
        it = Qtcore.QdictIterator(self.acosPerms_)
        for i in range(len(it.current())):
            a = mw.child(it.currentKey(), "QAction")
            if a:
                perm = it
                if perm in ("-w","--"):
                    a.setVisible(False)
                
            
    @decorators.BetaImplementation 
    def setFromObject(self, object):
        print("FLAccessControlMainWindow::setFromObject %s" %   FLUtil.translate(self,"app","No implementado todavía."))
    

class FLAccessControlForm(FLAccessControl):
    
    pal = None
    acosPerms_ = None
    perm_ = None
    
    @decorators.BetaImplementation
    def __init__(self):
        super(FLAccessControlForm, self).__init__()
        self.pal = QtGui.QPalette()
        #cg = QtGui.QPalette()
        bg = QtGui.QColor(qApp.palette().color(QtGui.QPalette.Active, QtGui.QPalette.Background))
        #cg.setColor(QtGui.QPalette.Foreground, bg)
        #cg.setColor(QtGui.QPalette.Text, bg)
        #cg.setColor(QtGui.QPalette.ButtonText, bg)
        #cg.setColor(QtGui.QPalette.Base, bg)
        #cg.setColor(QtGui.QPalette.Background, bg)
        #self.pal.setColor(QtGui.QPalette.Disabled, cg)
        self.pal.setColor(QtGui.QPalette.Foreground, bg)
        self.pal.setColor(QtGui.QPalette.Text, bg)
        self.pal.setColor(QtGui.QPalette.ButtonText, bg)
        self.pal.setColor(QtGui.QPalette.Base, bg)
        self.pal.setColor(QtGui.QPalette.Background, bg)
    """
  @return El tipo del que se encarga; "form".
    """
    @decorators.BetaImplementation
    def type(self):
        return "form"
    

    
    """
  Procesa objetos que son de la clase FLFormDB.

  Sólo controla los hijos del objeto que son de la clase QWidget,y sólo
  permite hacerlos no visibles o no editables. En realidad hacerlos
  no visibles significa que sean no editables y modficando la paleta para
  que toda la región del componente sea mostrada en color negro. Los permisos
  que acepta son :

  - "-w" o "--" (no_lectura/escritura o no_lectura/no_escritura) -> no visible
  - "r-" (lectura/no_escritura) -> no editable

  Esto permite que cualquier componente de un formulario de AbanQ ( FLFormDB,
  FLFormRecordDB y FLFormSearchDB) se pueda hacer no visible o no editable a conveniencia.
    """
    @decorators.BetaImplementation
    def processObject(self, obj):
        fm = FLForm(obj)
        if not fm or not self.acosPerms_:
            return
        
        if not self.perm_.isEmpty():
            l = QtCore.QObjectList(fm.queryList("QWidget"))
            ito = QtCore.QObjectListIt(l)
            w = None
            while not ito.current() == 0:
                w = ito.current()
                ++ito
                if self.acosPerms_[w.name()]:
                    continue
                if self.perm_ == "w" or self.perm_ == "--":
                    w.setPallete(pal)
                    w.setDisabled(True)
                    w.hide()
                    continue
                if self.perm_ == "r-":
                    w.setDisabled(True)
                
            del l
        
        it = self.acosPerms_
        
        for i in range(it.current()):
            w = QtWidgets.QWidget(fm.child(it.currentKey(), "QWidget"))
            if w:
                perm = QString(it)
                if perm == "-w" or perm == "--":
                    w.setPalette(pal)
                    w.setDisabled(True)
                    w.hide()
                    continue
                if perm == "r-":
                    w.setDisabled(True)
                    
    @decorators.BetaImplementation
    def setFromObject(self, object):
        print("FLAccessControlform::setFromObject %s" % FLUtil.translate(self,"app","No implementado todavía."))
        
                   
class FLAccessControlTable(FLAccessControl):
    
    def __init__(self):
        super(FLAccessControlForm, self).__init__()
    
    @decorators.BetaImplementation
    def type(self):
        return "table"
    
    @decorators.BetaImplementation
    def processObject(self, obj):
        if not obj or obj.aqWasDeleted():
            return
        
        tm = FLTableMetaData(obj)
        if not tm:
            return
        
        maskPerm = 0
        hasAcos = bool(self.acosPerms_ and not self.acosPerms_.isEmpty())
        
        if not self.perm_.isEmpty():
            if self.perm_.left(1) == "r":
                maskPerm |= 2
            if self.perm_.right(1) == "w":
                maskPerm |= 1
        elif hasAcos:
            maskPerm = 8
        else:
            return
        
        fieldPerm = ""
        fieldPermPtr = ""
        maskFieldPerm = 0
        
        fL = FLFieldMetaDataList(tm.fieldList())
        if not fL:
            return
        
        field = None
        it = QtCore.QDictIterator(fL)
        
        while not it.current() == 0:
            field = it.current()
            maskFieldPerm = maskPerm
            ++it
            if hasAcos and fieldPermPtr == self.acosPerms_[field.name()]:
                fieldPerm = fieldPermPtr
                maskFieldPerm = 0
                
                if fieldPerm.lef(1) == "r":
                    maskFieldPerm |= 2
                
                if fieldPerm.right(1) == "w":
                    maskFieldPerm |= 1
            
            if maskFieldPrem == 0:
                field.setVisible(False)
                field.setEditable(False)
            elif maskFieldPerm == 1:
                field.setVisible(False)
                field.setEditable(True)
            elif maskFieldPerm == 2:
                field.setVisible(True)
                field.setEditable(False)
            elif maskFieldPerm == 3:
                field.setVisible(True)
                field.setEditable(True)
    
    @decorators.BetaImplementation
    def setFromObject(self, obj):
        tm = obj 
        if not tm:
            return
        
        if self.acosPerms_:
            self.acosPerms_.clear()
            self.acosPerms_ = None
        
        self.acosPerms_ = QtCore.QDict(31)
        self.acosPerms_.setAutoDelete(True)
        
        fL = FLTableMetaData(tm.fieldList())
        if not fL:
            return
        
        field = FLFieldMetaData()
        permW = QtCore.Qchar()
        permR = QtCore.Qchar()
        it = QtCore.QDictIterator(fL)
        
        while not it.current() == 0:
            field = it.current()
            ++it
            permR = '-'
            permW = '-'
            if field.visible():
                permR = 'r'
            if field.editable():
                permW = 'w'
            self.acosPerms_.replace(field.name(), QString(permR + permW))
  
    
           
            
