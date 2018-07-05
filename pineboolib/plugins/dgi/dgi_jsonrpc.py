# # -*- coding: utf-8 -*-

from pineboolib.plugins.dgi.dgi_schema import dgi_schema
from pineboolib.utils import Struct
from pineboolib.fllegacy.FLFieldDB import FLFieldDB
from pineboolib.fllegacy.FLTableDB import FLTableDB
from pineboolib import decorators
import pineboolib

from PyQt5 import QtCore, QtWidgets

from xmljson import yahoo as xml2json
from xml.etree.ElementTree import fromstring
from json import dumps
from xml import etree

from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple

from jsonrpc import JSONRPCResponseManager, dispatcher

import traceback


class parser(object):
    _mainForm = None
    _queqe = {}

    def __init__(self, mainForm):
        self._mainForm = mainForm

    def addQueque(self, name, value):
        self._queqe[name] = value

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
        if pineboolib.project._DGI._par._queqe:
            return "queqePending"
        if not args:
            return "needArguments"
        obj_ = getattr(pineboolib.project.main_window,
                       "json_%s" % args[0], None)
        if obj_:
            return obj_(args)
        else:
            print("No existe mainWindow.json_%s" % args[0])
            return "notFound"

    @dispatcher.add_method
    def mainForm(*args):
        if pineboolib.project._DGI._par._queqe:
            return "queqePending"
        if not args:
            return "needArguments"
        try:
            obj_ = pineboolib.project._DGI.mainForm()
            return obj_.json_process(args)
        except Exception:
            print(traceback.format_exc())
            return "notFound"

    @dispatcher.add_method
    def callFunction(*args):
        if pineboolib.project._DGI._par._queqe:
            return "queqePending"

        fun_ = args[0]
        param_ = None
        fn = None
        if len(args) > 1:
            param_ = ",".join(args[1:])
        else:
            param_ = [args[0]]

        try:
            pineboolib.project.call(fun_, param_)
        except Exception:
            return "notFound"
        # if param_:
        #    return fn(param_)
        # else:
        #    return fn()

    @dispatcher.add_method
    def queqe(*args):
        if len(args) == 1:
            if args[0] == "clean":
                pineboolib.project._DGI._par._queqe = {}
                return True
            elif args[0] in pineboolib.project._DGI._par._queqe.keys():
                ret = []
                for q in pineboolib.project._DGI._par._queqe.keys():
                    if q.find(args[0]) > -1:
                        ret.append(q, pineboolib.project._DGI._par._queqe[q])
                        del pineboolib.project._DGI._par._queqe[q]
            else:
                ret = "Not Found"
        else:
            ret = pineboolib.project._DGI._par._queqe
            pineboolib.project._DGI._par._queqe = {}

        return ret

    @dispatcher.add_method
    def action(*args):
        if pineboolib.project._DGI._par._queqe:
            return "queqePending"
        arguments = args
        actionName = arguments[0]
        control = arguments[1]
        emite = arguments[2]
        if actionName in pineboolib.project._DGI._WJS.keys():
            ac = pineboolib.project._DGI._W[actionName]

            cr = ac.child(control)
            if cr:
                em = getattr(cr, emite, None)
                if isinstance(cr, FLFieldDB):
                    if emite == "setText":
                        cr.editor_.setText(arguments[3])
                        return True
                    else:
                        print("Función desconocida", emite)
                        return False

                elif isinstance(cr, FLTableDB):
                    if emite == "data":
                        print("Recoge data!!!")

                elif em:
                    getattr(cr, emite).emit()
                    return True

            return False

        return "notFound"


class dgi_jsonrpc(dgi_schema):
    _par = None
    _W = {}
    _WJS = {}

    def __init__(self):
        # desktopEnabled y mlDefault a True
        super(dgi_jsonrpc, self).__init__()
        self._name = "jsonrpc"
        self._alias = "JSON-RPC"
        self.setUseDesktop(True)
        self.setUseMLDefault(True)
        self.setLocalDesktop(False)
        self.showInitBanner()
        self._mainForm = None

    def extraProjectInit(self):
        pass

    def setParameter(self, param):
        self._listenSocket = param

    def mainForm(self):
        if not self._mainForm:
            self._mainForm = mainForm()
        return self._mainForm

    def exec_(self):
        self._par = parser(self._mainForm)
        self.launchServer()

    def launchServer(self):
        run_simple('localhost', 4000, self._par.receive)
        # print("JSON-RPC:INFO: Listening socket", self._listenSocket)
        # WSGIServer(self._par.query, bindAddress=self._listenSocket).run()

    @decorators.BetaImplementation
    def loadUI(self, path, widget):
        self._WJS[widget.__class__.__module__] = self.parserDGI.parse(path)
        self._W[widget.__class__.__module__] = widget

    def showWidget(self, widget):
        self._par.addQueque(
            "%s_showWidget" % widget.__class__.__module__, self._WJS[widget.__class__.__module__])


class mainForm(QtWidgets.QMainWindow):
    mainWindow = None
    MainForm = None

    def __init__(self):
        super(mainForm, self).__init__()
        self.mainWindow = json_mainWindow()
        self.MainForm = json_MainForm()

    def json_process(self, args):
        try:
            _action = args[0]

            if _action == "launch":
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


class json_mainWindow(QtWidgets.QMainWindow):
    areas_ = {}
    modules_ = {}
    _actionsConnects = {}
    _actions = {}
    _toolBarActions = []
    _images = {}

    def __init__(self):
        super(json_mainWindow, self).__init__()
        self.areas_ = {}
        self.modules_ = {}
        self._actionsConnects = {}
        self._actions = {}
        self._toolBarActions = []
        self._images = {}

    def load(self):
        pass
        # Aquí se genera el json con las acciones disponibles

    def addFormTab(self, f):
        pass

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
        _json = xml2json.data(fromstring(
            etree.tostring(xml, pretty_print=True)))
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
