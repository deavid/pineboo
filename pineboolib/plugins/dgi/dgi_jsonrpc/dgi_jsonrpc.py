# # -*- coding: utf-8 -*-
import traceback
from pineboolib import logging
import sys
import re

from xmljson import yahoo as xml2json
from xml.etree.ElementTree import fromstring
from json import dumps
from xml import etree

from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple

from jsonrpc import JSONRPCResponseManager, dispatcher

from pineboolib.plugins.dgi.dgi_schema import dgi_schema
from pineboolib.core import decorators


logger = logging.getLogger(__name__)


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
            response = JSONRPCResponseManager.handle(request.data, dispatcher)
        except Exception:
            response = "Not Found"

        return Response(response.json, mimetype="application/json")

    @dispatcher.add_method
    def mainWindow(*args):
        from pineboolib import project

        if project._DGI._par._queqe:
            return "queqePending"
        if not args:
            return "needArguments"
        obj_ = getattr(project.main_window, "json_%s" % args[0], None)
        if obj_:
            return obj_(args)
        else:
            print("No existe mainWindow.json_%s" % args[0])
            return "notFound"

    @dispatcher.add_method
    def mainForm(*args):
        from pineboolib import project

        if project._DGI._par._queqe:
            return "queqePending"
        if not args:
            return "needArguments"
        try:
            obj_ = project._DGI.mainForm()
            return obj_.json_process(args)
        except Exception:
            print(traceback.format_exc())
            return "notFound"

    @dispatcher.add_method
    def callFunction(*args):
        from pineboolib import project

        if project._DGI._par._queqe:
            return "queqePending"

        fun_ = args[0]
        param_ = None
        # fn = None
        if len(args) > 1:
            param_ = ",".join(args[1:])
        else:
            param_ = [args[0]]

        try:
            project.call(fun_, param_)
        except Exception:
            return "notFound"
        # if param_:
        #    return fn(param_)
        # else:
        #    return fn()

    @dispatcher.add_method
    def queqe(*args):
        from pineboolib import project

        if len(args) == 1:
            if args[0] == "clean":
                project._DGI._par._queqe = {}
                return True
            elif args[0] in project._DGI._par._queqe.keys():
                ret = []
                for q in project._DGI._par._queqe.keys():
                    if q.find(args[0]) > -1:
                        ret.append((q, project._DGI._par._queqe[q]))
                        del project._DGI._par._queqe[q]
            else:
                ret = "Not Found"
        else:
            ret = project._DGI._par._queqe
            project._DGI._par._queqe = {}

        return ret

    @dispatcher.add_method
    def action(*args):
        from pineboolib import project
        from pineboolib import pncontrolsfactory

        if project._DGI._par._queqe:
            return "queqePending"
        arguments = args
        actionName = arguments[0]
        control = arguments[1]
        emite = arguments[2]
        if actionName in project._DGI._WJS.keys():
            ac = project._DGI._W[actionName]

            cr = ac.child(control)
            if cr:
                em = getattr(cr, emite, None)
                if isinstance(cr, pncontrolsfactory.FLFieldDB):
                    if emite == "setText":
                        cr.editor_.setText(arguments[3])
                        return True
                    else:
                        print("Función desconocida", emite)
                        return False

                elif isinstance(cr, pncontrolsfactory.FLTableDB):
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
        super().__init__()
        self._name = "jsonrpc"
        self._alias = "JSON-RPC"
        self.setUseDesktop(True)
        self.setUseMLDefault(True)
        self.setLocalDesktop(False)
        self.showInitBanner()
        self._mainForm = None
        self.parserDGI = parserJson()

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
        run_simple("localhost", 4000, self._par.receive)
        # print("JSON-RPC:INFO: Listening socket", self._listenSocket)
        # WSGIServer(self._par.query, bindAddress=self._listenSocket).run()

    @decorators.BetaImplementation
    def loadUI(self, path, widget):
        self._WJS[widget.__class__.__module__] = self.parserDGI.parse(path)
        self._W[widget.__class__.__module__] = widget

    def showWidget(self, widget):
        self._par.addQueque("%s_showWidget" % widget.__class__.__module__, self._WJS[widget.__class__.__module__])

    def __getattr__(self, name):
        return super().resolveObject(self._name, name)


"""
Exportador UI a JSON
"""


class parserJson:
    def __init__(self):
        # TODO: se puede ampliar con propiedades y objetos de qt4
        self.aPropsForbidden = [
            "images",
            "includehints",
            "layoutdefaults",
            "slots",
            "stdsetdef",
            "stdset",
            "version",
            "spacer",
            "connections",
        ]
        self.aObjsForbidden = [
            "geometry",
            "sizePolicy",
            "margin",
            "spacing",
            "frameShadow",
            "frameShape",
            "maximumSize",
            "minimumSize",
            "font",
            "focusPolicy",
            "iconSet",
            "author",
            "comment",
            "forwards",
            "includes",
            "sizepolicy",
            "horstretch",
            "verstretch",
        ]

    def isInDgi(self, property, type):
        if type == "prop":
            if property in self.aPropsForbidden:
                return False
            else:
                if property in self.aObjsForbidden:
                    return False

        return True

    def manageProperties(self, obj):
        if isinstance(obj, dict):
            for property in list(obj):
                if self.isInDgi(property, "prop"):
                    if property == "name" and not self.isInDgi(obj[property], "obj"):
                        del obj
                        return None
                    else:
                        prop = self.manageProperties(obj[property])
                        if prop:
                            obj[property] = prop
                        else:
                            del obj[property]
                else:
                    del obj[property]
        elif isinstance(obj, list):
            ind = 0
            while ind < len(obj):
                it = self.manageProperties(obj[ind])
                if it:
                    obj[ind] = it
                    ind += 1
                else:
                    del obj[ind]
        return obj

    def parse(self, name):
        inputFile = name
        outputFile = re.search(r"\w+.ui", inputFile)

        if outputFile is None:
            print("Error. El fichero debe tener extension .ui")
            return None

        # ret_out = outputFile

        outputFile = re.sub(".ui", ".dgi", inputFile)

        try:
            ui = open(inputFile, "r")
            xml = ui.read()

        except Exception:
            print("Error. El fichero no existe o no tiene formato XML")
            sys.exit()

        json = xml2json.data(fromstring(xml))
        json = self.manageProperties(json)
        strJson = dumps(json, sort_keys=True, indent=2)

        """
        try:
            dgi = open(outputFile, 'w')
            dgi.write(strJson)
            dgi.close()
        except:
            print("Error. Ha habido un problema durante la escritura del fichero")
            return None
        """
        strJson = strJson.replace("\n", "")
        strJson = " ".join(strJson.split())
        return strJson


"""
FIXME: Estas clases de abajo ,deberian de ser tipo object para poder levantar la aplicación sin entorno gráfico
"""


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


class json_mainWindow(object):
    areas_ = {}
    modules_ = {}
    _actionsConnects = {}
    _actions = {}
    _toolBarActions = []
    _images = {}
    initialized_mods_ = []
    w_ = None

    def __init__(self):
        self.areas_ = {}
        self.modules_ = {}
        self._actionsConnects = {}
        self._actions = {}
        self._toolBarActions = []
        self._images = {}
        self.initialized_mods_ = []
        self.w_ = "hola"

    """
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
    """

    def show(self):
        pass

    def loadAction(self, action):
        self._actions[action.name] = action

    def loadConnection(self, action):
        self._actions[action.name] = action

    def loadToolBarsAction(self, name):
        self._toolBarActions.append(name)

    def addToJson(self, xml):
        _json = xml2json.data(fromstring(etree.ElementTree.tostring(xml)))
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

    def initScript(self):
        self.initModule("sys")

    def initModule(self, module):
        if module not in self.initialized_mods_:
            self.initialized_mods_.append(module)
            from pineboolib import project

            project.call("%s.iface.init" % module, [], None, False)

        mng = project.conn.managerModules()
        mng.setActiveIdModule(module)


class json_MainForm(object):
    def setDebugLevel(self, number):
        pass
