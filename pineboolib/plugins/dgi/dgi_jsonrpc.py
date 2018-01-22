# # -*- coding: utf-8 -*-

from pineboolib.plugins.dgi.dgi_schema import dgi_schema
from pineboolib.utils import Struct
from PyQt5 import QtCore

from xmljson import yahoo as xml2json
from xml.etree.ElementTree import fromstring
from json import dumps

from flup.server.fcgi import WSGIServer


import traceback
import sys
#from flup.server.fcgi import WSGIServer

dependences = []

# try:
#    import flup
# except ImportError:
#    print(traceback.format_exc())
#    dependences.append("flup-py3")


if len(dependences) > 0:
    print()
    print("HINT: Dependencias incumplidas:")
    for dep in dependences:
        print("HINT: Instale el paquete %s e intente de nuevo" % dep)
    print()
    sys.exit(32)

arrayControles = {}


class dgi_jsonrpc(dgi_schema):

    _fcgiCall = None
    _fcgiSocket = None
    _par = None

    def __init__(self):
        # desktopEnabled y mlDefault a True
        super(dgi_jsonrpc, self).__init__()
        self._name = "jsonrpc"
        self._alias = "JSON-RPC"
        self.setUseDesktop(True)
        self.setUseMLDefault(True)
        self.setLocalDesktop(False)
        self.showInitBanner()
        self._listenSocket = "/tmp/pineboo-JSONRPC.socket"
        self.loadReferences()
        self._mainForm = None

    def extraProjectInit(self):
        pass
        

    def setParameter(self, param):
        self._listenSocket = param

    def loadReferences(self):
        self.FLLineEdit = FLLineEdit
        self.QPushButton = PushButton
        self.QLineEdit = LineEdit
    
    
    def mainForm(self):
        if not self._mainForm:
            self._mainForm = mainForm()
        return self._mainForm
    
    def exec_(self):
        self._par = parser()
        self.launchServer()
    
    def launchServer(self):
        print("JSON-RPC:INFO: Listening socket", self._listenSocket)
        WSGIServer(self._par.query, bindAddress=self._listenSocket).run()


class mainForm(object):
    
    mainWindow = None
    MainForm = None
    
    def __init__(self):
        self.mainWindow = mainWindow()
        self.MainForm = MainForm()

class mainWindow():
    
    areas_ = {}
    modules_ = {}
    
    def __init__(self):
        self.areas_ = {}
        self.modules_ = {}
    
    def load(self):
        pass
        #Aquí se genera el json con las acciones disponibles
    
    def loadArea(self, area):
        self.areas_[area.idarea] = area.descripcion
    
    def loadModule(self, module):
        if module.areaid not in self.areas_.keys():
            self.loadArea(Struct(idarea=module.areaid,
                                 descripcion=module.areaid))
        
        module_ = Struct()
        module_.areaid = module.areaid
        module_.description = module.description
        module_.name = module.name
          
        self.modules_[module_.name] = module_
        
        self.moduleLoad(module)
    
    def moduleLoad(self, module):
        if module.loaded == False:
            module.load()
        if module.loaded == False:
            print("WARN: Ignorando modulo %r por fallo al cargar" %
                  (module.name))
            return False
    
    def show(self):
        #Preparamos el comando a enviar
        pass
    
    
    
        
        
          

class MainForm(object):
    
    def setDebugLevel(self, number):
        pass    
        


class parser(object):

    def query(self, environ, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])
        print("FCGI:INFO: Processing '%s' ..." % environ["QUERY_STRING"])


class PushButton(object):

    def __getattr__(self, name):
        print("Pushbutton necesita", name)


class LineEdit(object):

    def __getattr__(self, name):
        print("LineEdit necesita", name)


class FLLineEdit(object):

    _tipo = None
    _partDecimal = 0
    _partInteger = 0
    _maxValue = None
    autoSelect = True
    _name = None
    _longitudMax = None
    _parent = None
    _name = None
    lostFocus = QtCore.pyqtSignal()
    parentObj_ = None

    def __init__(self, parent, name=None):
        if self.name:
            self._name = name

        if isinstance(parent.fieldName_, str):
            self._fieldName = parent.fieldName_
            self._tipo = parent.cursor_.metadata().fieldType(self._fieldName)
            self._partDecimal = parent.partDecimal_
            self._partInteger = parent.cursor_.metadata().field(self._fieldName).partInteger()
            self._longitudMax = parent.cursor_.metadata().field(self._fieldName).length()
            # self.textChanged.connect(self.controlFormato)
            self._parent = parent

    def __getattr__(self, name):
        return DefFun(self, name)

    def controlFormato(self):
        pass

    def setText(self, texto, b=True):
        push(self, texto)

    def text(self):
        return pull(self, "text")

    """
    Especifica un valor máximo para el text (numérico)
    """

    def setMaxValue(self, value):
        self._maxValue = value
