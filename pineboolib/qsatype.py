# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import os
import datetime, weakref

from PyQt4 import QtCore, QtGui

# Cargar toda la API de Qt para que sea visible.
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from pineboolib import qsaglobals
from pineboolib import flcontrols
from pineboolib.fllegacy import FLFormSearchDB as FLFormSearchDB_legacy
from pineboolib.flcontrols import FLTable, QLineEdit
from pineboolib.fllegacy import FLSqlQuery as FLSqlQuery_Legacy
from pineboolib.fllegacy import FLSqlCursor as FLSqlCursor_Legacy
from pineboolib.fllegacy import FLTableDB as FLTableDB_Legacy
from pineboolib.fllegacy import FLUtil as FLUtil_Legacy
from pineboolib.fllegacy import FLReportViewer as FLReportViewer_Legacy

from pineboolib import decorators
import traceback

class StructMyDict(dict):

     def __getattr__(self, name):
         try:
             return self[name]
         except KeyError as e:
             raise AttributeError(e)

     def __setattr__(self, name, value):
         self[name] = value
         
def Function(args, source):
    # Leer código QS embebido en Source
    # asumir que es una funcion anónima, tal que: 
    #  -> function($args) { source }
    # compilar la funcion y devolver el puntero
    qs_source = """
function anon(%s) {
    %s
} """ % (args,source)
    print("Compilando QS en línea: ", qs_source)
    from pineboolib.flparser import flscriptparse
    from pineboolib.flparser import postparse
    from pineboolib.flparser.pytnyzer import write_python_file, string_template
    import io
    prog = flscriptparse.parse(qs_source)
    tree_data = flscriptparse.calctree(prog, alias_mode = 0)
    ast = postparse.post_parse(tree_data)
    tpl = string_template
    
    f1 = io.StringIO()

    write_python_file(f1,ast,tpl)
    pyprog = f1.getvalue()
    print("Resultado: ", pyprog)
    glob = {}
    loc = {}
    exec(pyprog, glob, loc)
    # ... y lo peor es que funciona. W-T-F.
    
    return loc["anon"]

def Object(x=None):
    if x is None: x = {}
    return StructMyDict(x)

#def Array(x=None):
    #try:
        #if x is None: return {}
        #else: return list(x)
    #except TypeError:
        #return [x]
        
class Array(object):
    
    dict_ = None
    key_ = None
    
    def __init__(self, data = None):
        if not data:
            self.dict_ = {}
        else:
            self.dict_ = data
    
    def __setitem__(self, key, value):
        self.dict_[key] = value
        
            
        
    def __getitem__(self, key):
        #print("QSATYPE.DEBUG: Array.getItem() " ,key,  self.dict_[key])
        return self.dict_[key]
    
    def __getattr__(self, k):
        if k == 'length': 
            return len(self.dict_)
            
        

def Boolean(x=False): return bool(x)

def FLSqlQuery(*args):
    #if not args: return None
    query_ = FLSqlQuery_Legacy.FLSqlQuery(*args)
        
        
    return query_

def FLUtil(*args):
    return FLUtil_Legacy.FLUtil(*args)

def AQUtil(*args):
    return FLUtil_Legacy.FLUtil(*args)

def FLSqlCursor(action=None):
    if action is None: return None
    return FLSqlCursor_Legacy.FLSqlCursor(action)

def FLTableDB(*args):
    if not args: return None
    return FLTableDB_Legacy.FLTableDB(*args)

FLListViewItem = QtGui.QListView
QTable = FLTable
Color = QtGui.QColor
QColor = QtGui.QColor
QDateEdit = QtGui.QDateEdit

File = QtCore.QFile

@decorators.NotImplementedWarn
def FLPosPrinter(*args, **kwargs):
    class flposprinter:
        pass
    return flposprinter()

@decorators.BetaImplementation
def FLReportViewer():
    return FLReportViewer_Legacy.FLReportViewer()

@decorators.NotImplementedWarn
def FLDomDocument(*args, **kwargs):
    class fldomdocument:
        pass
    return fldomdocument()

@decorators.NotImplementedWarn
def FLCodBar(*args, **kwargs):
    class flcodbar:
        def nameToType(self, name):
            return name
        def pixmapError(self):
            return QtGui.QPixmap()
        def pixmap(self):
            return QtGui.QPixmap()
        def validBarcode(self):
            return None
    return flcodbar()

def print_stack(maxsize=1):
    for tb in traceback.format_list(traceback.extract_stack())[1:-2][-maxsize:]:
        print(tb.rstrip())

def check_gc_referrers(typename, w_obj, name):
    import threading, time
    def checkfn():
        import gc
        time.sleep(2)
        gc.collect()
        obj = w_obj()
        if not obj: return
        # TODO: Si ves el mensaje a continuación significa que "algo" ha dejado
        # ..... alguna referencia a un formulario (o similar) que impide que se destruya
        # ..... cuando se deja de usar. Causando que los connects no se destruyan tampoco
        # ..... y que se llamen referenciando al código antiguo y fallando.
        print("HINT: Objetos referenciando %r::%r (%r) :" % (typename, obj, name))
        for ref in gc.get_referrers(obj):           
            if isinstance(ref, dict): 
                x = []
                for k,v in ref.items():
                    if v is obj:
                        k = "(**)" + k
                        x.insert(0,k)
                    else:
                        x.append(k)    
                print(" - ", repr(x[:48]))
            else:
                if "<frame" in str(repr(ref)): continue
                print(" - ", repr(ref))

        
    threading.Thread(target = checkfn).start()
    

class FormDBWidget(QtGui.QWidget):

    def __init__(self, action, project, parent = None):
        super(FormDBWidget, self).__init__(parent)
        self._action = action
        self.cursor_ = FLSqlCursor(action.name)
        self._prj = project
        self._class_init()
        
    def __del__(self):
        print("FormDBWidget: Borrando form para accion %r" % self._action.name)
        

    def _class_init(self):
        pass
    
    def closeEvent(self, event):
        can_exit = True
        print("FormDBWidget: closeEvent para accion %r" % self._action.name)
        check_gc_referrers("FormDBWidget:"+self.__class__.__name__, weakref.ref(self), self._action.name)
        if hasattr(self, 'iface'):
            check_gc_referrers("FormDBWidget.iface:"+self.iface.__class__.__name__, weakref.ref(self.iface), self._action.name)
            del self.iface.ctx 
            del self.iface 
        
        if can_exit:
            event.accept() # let the window close
        else:
            event.ignore()
    def child(self, childName):
        try:
            ret = self.findChild(QtGui.QWidget, childName)
        except RuntimeError as rte:
            # FIXME: A veces intentan buscar un control que ya está siendo eliminado.
            # ... por lo que parece, al hacer el close del formulario no se desconectan sus señales.
            print("ERROR: Al buscar el control %r encontramos el error %r" % (childName,rte))
            print_stack(8)
            import gc
            gc.collect()
            print("HINT: Objetos referenciando FormDBWidget::%r (%r) : %r" % (self, self._action.name, gc.get_referrers(self)))
            if hasattr(self, 'iface'):
                print("HINT: Objetos referenciando FormDBWidget.iface::%r : %r" % (self.iface, gc.get_referrers(self.iface)))
            ret = None
        else:
            if ret is None:
                print("WARN: No se encontró el control %r" % childName)
        #else:
        #    print("DEBUG: Encontrado el control %r: %r" % (childName, ret))
        return ret

    def cursor(self):
        cursor = None
        try:
            if self.parentWidget():
                cursor = getattr(self.parentWidget(),"cursor_", None)
            if cursor:
                del self.cursor_
                self.cursor_ = cursor
        except Exception:
            # FIXME: A veces parentWidget existía pero fue eliminado. Da un error
            # ... en principio debería ser seguro omitir el error.
            pass
        return self.cursor_

def FLFormSearchDB(name):
    widget = FLFormSearchDB_legacy.FLFormSearchDB(name)
    widget.setWindowModality(QtCore.Qt.ApplicationModal)
    return widget

class Date(QtCore.QDate):
    pass

class Dialog(QtGui.QDialog):
    _layout = None
    buttonBox = None
    OKButtonText = None
    cancelButtonText = None
    OKButton = None
    cancelButton = None

    def __init__(self, title, f, desc=None):
        #FIXME: f no lo uso , es qt.windowsflg
        super(Dialog, self).__init__()
        self.setWindowTitle(title)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self._layout = QtGui.QVBoxLayout()
        self.setLayout(self._layout)
        self.buttonBox = QtGui.QDialogButtonBox()
        self.OKButton = QtGui.QPushButton("&Aceptar")
        self.cancelButton = QtGui.QPushButton("&Cancelar")
        self.buttonBox.addButton(self.OKButton, QtGui.QDialogButtonBox.AcceptRole)
        self.buttonBox.addButton(self.cancelButton, QtGui.QDialogButtonBox.RejectRole)
        self.OKButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)


    def add(self, _object):
        self._layout.addWidget(_object)

    def exec_(self):
        if (self.OKButtonText):
            self.OKButton.setText(self.OKButtonText)
        if (self.cancelButtonText):
            self.cancelButton.setText(self.cancelButtonText)
        self._layout.addWidget(self.buttonBox)

        return super(Dialog, self).exec_()

class GroupBox(QtGui.QGroupBox):
    def __init__(self):
        super(GroupBox, self).__init__()
        self._layout = QtGui.QHBoxLayout()
        self.setLayout(self._layout)

    def add(self, _object):     
        self._layout.addWidget(_object)

class CheckBox(QtGui.QCheckBox):
    pass

   
    
        