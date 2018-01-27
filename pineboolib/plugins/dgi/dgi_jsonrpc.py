# # -*- coding: utf-8 -*-

from pineboolib.plugins.dgi.dgi_schema import dgi_schema
from pineboolib.utils import Struct
from pineboolib import decorators

import pineboolib

from PyQt5 import QtCore

from xmljson import yahoo as xml2json
from xml.etree.ElementTree import fromstring
from json import dumps
from lxml import etree

from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple

from jsonrpc import JSONRPCResponseManager, dispatcher



import traceback
import sys






class parser(object):
    
    _mainForm = None
    
    def __init__(self, mainForm):
        self._mainForm = mainForm
    
    @Request.application
    def receive(self, request):
        response = None
        try:
            response = JSONRPCResponseManager.handle(
                request.data, dispatcher)
        except Exception:
            response = "Not Found"
            
        return Response(response.json, mimetype='application/json')



    

    @dispatcher.add_method   
    def mainWindow(*args):
        if not args:
            return "needArguments"
        obj_ = getattr(pineboolib.project.main_window,"json_%s" % args[0],None)
        if obj_:
            return obj_(args)
        else:
            print("No existe mainWindow.json_%s" % args[0])
            return "notFound"

    @dispatcher.add_method   
    def mainForm(*args):
        if not args:
            return "needArguments"
        try:
            obj_ = pineboolib.project._DGI.mainForm()
            return obj_.json_process(args)
        except Exception:
            print(traceback.format_exc())
            return "notFound"

arrayControles = {}




class dgi_jsonrpc(dgi_schema):
    _par = None
    _reject_widgets = []
    _W = {}
    
    def __init__(self):
        # desktopEnabled y mlDefault a True
        super(dgi_jsonrpc, self).__init__()
        self._name = "jsonrpc"
        self._alias = "JSON-RPC"
        self.setUseDesktop(True)
        self.setUseMLDefault(True)
        self.setLocalDesktop(False)
        self.showInitBanner()
        self.loadReferences()
        self._mainForm = None
        self._reject_widgets =["QFrame"]

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
        self._par = parser(self._mainForm)
        self.launchServer()

    def launchServer(self):
        run_simple('localhost', 4000, self._par.receive)
        #print("JSON-RPC:INFO: Listening socket", self._listenSocket)
        #WSGIServer(self._par.query, bindAddress=self._listenSocket).run()
        
    @decorators.NotImplementedWarn
    def child(self, parent, name):
        return self._W[parent._action.name]
    
    @decorators.BetaImplementation
    def loadUI(self, path, widget):
        self._W[widget._action.name] = widget
        """
        Convertir a .json el ui
        """
    

    @decorators.NotImplementedWarn
    def showWidget(self, widget):
        print("Mostrando",widget)    
    
    
    @decorators.NotImplementedWarn
    def createWidget(self, classname, parent):
        """
        Carga un objecto del tipo classname y lo añade a self._W[widget._action.name]
        """
        
        if classname not in self.reject_widgets():
            print("%s acepted !!!!(%s)" % (classname, parent))
            return self._W[widget._action.name].remote_widgets[classname]
        else:
            print("%s rejected !!!!" % classname)
            return parent
    
    def reject_widgets(self):
        return self._reject_widgets

class mainForm(object):

    mainWindow = None
    MainForm = None

    def __init__(self):
        self.mainWindow = json_mainWindow()
        self.MainForm = json_MainForm()
    
    def json_process(self, args):
        try:
            _action = args[0]
        
            if _action == "launch":
                print("Lanzando", args[1])
                return self.runAction(args[1])
        except Exception:
            print(traceback.format_exc())
            return False


    def runAction(self, name):
        try:
            self.mainWindow._actionsConnects[name].run()
            return True
        except Exception:
            print(traceback.format_exc())
            return False


class json_mainWindow():

    areas_ = {}
    modules_ = {}
    _actionsConnects = {}
    _actions = {}
    _toolBarActions = []
    _images = {}


    def __init__(self):
        self.areas_ = {}
        self.modules_ = {}
        self._actionsConnects = {}
        self._actions = {}
        self._toolBarActions = []
        self._images = {}

    def load(self):
        pass
        # Aquí se genera el json con las acciones disponibles

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
        if not module.loaded:
            module.load()
        if not module.loaded:
            print("WARN: Ignorando modulo %r por fallo al cargar" %
                  (module.name))
            return False

        for key in module.mainform.toolbar:
            action = module.mainform.actions[key]
            self._actionsConnects[action.name] = action

    def show(self):
        pass
    
    
    def loadAction(self, action):
        self._actions[action.name] = action
    
    def loadConnection(self, action):
        self._actions[action.name] = action
    
    def loadToolBarsAction(self, name):
        self._toolBarActions.append(name)
    
    def addToJson(self, xml):
        _json = xml2json.data(fromstring(etree.tostring(xml, pretty_print=True)))
        _jsonStr = dumps(_json, sort_keys=True, indent=2)
        return _jsonStr
    
    def json_areas(self, *args):
        return self.areas_
        
    def json_modules(self, args):
        _area = None
        if len(args) > 1:
            _area = args[1]
        
        modulesS = []
            
        for modu in self.modules_.keys():
            if _area:
                if self.modules_[modu].areaid == _area:
                    modulesS.append(self.modules_[modu].name)
                    modulesS.append(self.modules_[modu].description)
                    modulesS.append(self.modules_[modu].areaid)
            else:
                modulesS.append(self.modules_[modu].name)
                modulesS.append(self.modules_[modu].description)
                modulesS.append(self.modules_[modu].areaid)
                    
            
        
        return modulesS
    
    def json_actions(self, args):
        _module = None
        _ret = []
        if len(args) > 1:
            _module = args[1]
        
        include = True
        for ac in self._actions.keys():
            _mod = self._actions[ac].mod
            if _module:
                include = False
                if _mod.name == _module:
                    include = True
            
            
            if include:
                _ret.append(_mod.name)
                _ret.append(self._actions[ac].name)
                _ret.append(self._actions[ac].iconSet)
                _ret.append(self._actions[ac].slot)
        
        return _ret
    
    def json_image(self, name):
        for _ac in self._actions.keys():
            if name[1] == self._actions[_ac].iconSet:
                return str(self._actions[_ac].icon)
        
        
        return False


class json_MainForm(object):
    def setDebugLevel(self, number):
        pass

"""
class parser(object):
    _mainForm = None

    def __init__(self, mainForm):
        self._mainForm = mainForm

    def query(self, environ, start_response):
        _received = environ["QUERY_STRING"]
        start_response('200 OK', [('Content-Type', 'text/html')])
        print("JSON-RPC:INFO: Processing '%s' ..." % _received)
        #if _received == "mainWindow":
        #    return self._mainForm.mainWindow._json
        #elif _received[0:7] == "action:":
        #    try:
        #        _action = _received[7:]
        #        print("Loading action", _action)
        #        self._mainForm.runAction(_action)
        #            
        #            
        #        return "OK!"
        #    except Exception:
        #        print(traceback.format_exc())
        retorno = self.proccess_rpc(_received)
        print("_________>", retorno)
        return retorno
    
    def proccess_rpc(self, json_data):
        return json_data
        
"""

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

    # def __getattr__(self, name):
    #     return DefFun(self, name)

    def controlFormato(self):
        pass

    # def setText(self, texto, b=True):
    #     push(self, texto)
    #
    # def text(self):
    #     return pull(self, "text")

    """
    Especifica un valor máximo para el text (numérico)
    """

    def setMaxValue(self, value):
        self._maxValue = value
