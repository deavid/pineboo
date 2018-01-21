# # -*- coding: utf-8 -*-

from pineboolib.plugins.dgi.dgi_schema import dgi_schema
from pineboolib.utils import Struct
from PyQt5 import QtCore
import traceback, sys
#from flup.server.fcgi import WSGIServer

dependences = []

#try:
#    import flup
#except ImportError:
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

    def __init__(self):
        super(dgi_jsonrpc, self).__init__()  # desktopEnabled y mlDefault a True
        self._name = "jsonrpc"
        self._alias = "JSON-RPC"
        self.setUseDesktop(True)
        self.setUseMLDefault(True)
        self.setLocalDesktop(False)
        self.showInitBanner()
        self._listenSocket = "/tmp/pineboo-JSONRPC.socket"
        self.loadReferences()

    def extraProyectInit(self):
        print("=============================================")
        print("============ EXTRA PROJECT INIT =============")
        print("=============================================")
        print("JSON-RPC:INFO: Listening socket", self._listenSocket)
        par_ = parser()
        #WSGIServer(par_.query, bindAddress=self._fcgiSocket).run()
        print("End load extraProjectInit")

    def setParameter(self, param):
        self._listenSocket = param
    
    def loadReferences(self):
        self.FLLineEdit = FLLineEdit
        self.QPushButton = PushButton
        self.QLineEdit = LineEdit

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
        push(self,texto)
        
    def text(self):
        return pull(self, "text")

    """
    Especifica un valor máximo para el text (numérico)
    """

    def setMaxValue(self, value):
        self._maxValue = value

