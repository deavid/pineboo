# # -*- coding: utf-8 -*-

from pineboolib.plugins.dgi.dgi_schema import dgi_schema
from pineboolib.utils import Struct
from pineboolib import decorators

import pineboolib

from PyQt5 import QtCore, QtWidgets

from xmljson import yahoo as xml2json
from xml.etree.ElementTree import fromstring
from json import dumps
from lxml import etree

from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple

from jsonrpc import JSONRPCResponseManager, dispatcher

import traceback


class parser(object):
    _mainForm = None
    _queqe = {}

    def __init__(self, mainForm):
        self._mainForm = mainForm

    def addQueqe(self, name, value):
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
        if not args:
            return "needArguments"
        try:
            obj_ = pineboolib.project._DGI.mainForm()
            return obj_.json_process(args)
        except Exception:
            print(traceback.format_exc())
            return "notFound"

    @dispatcher.add_method
    def queqe(*args):
        if len(args) == 1:
            if args[0] == "clean":
                pineboolib.project._DGI._par._queqe = {}
                return True
            else:
                return "notFound"

        ret = pineboolib.project._DGI._par._queqe
        pineboolib.project._DGI._par._queqe = {}
        return ret

    @dispatcher.add_method
    def action(*args):
        arguments = args
        actionName = arguments[0]
        control = arguments[1]
        emite = arguments[2]
        if actionName in pineboolib.project._DGI._WJS.keys():
            ac = pineboolib.project._DGI._W[actionName]

            cr = ac.child(control)
            if cr:
                em = getattr(cr, emite, None)
                if em:
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
        print("*************Cargando UI", path, widget)
        self._WJS[widget._action.name] = self.parserDGI.parse(path)
        self._W[widget._action.name] = widget
        """
        Convertir a .json el ui
        """

    def showWidget(self, widget):
        self._par.addQueqe("showWidget", self._WJS[widget._action.name])

    def loadReferences(self):
        super(dgi_jsonrpc, self).loadReferences()
        self.FLLineEdit = FLLineEdit


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


class FLLineEdit(QtWidgets.QLineEdit):

    _tipo = None
    _partDecimal = 0
    _partInteger = 0
    _maxValue = None
    autoSelect = True
    _name = None
    _longitudMax = None
    _parent = None

    lostFocus = QtCore.pyqtSignal()

    def __init__(self, parent, name=None):
        super(FLLineEdit, self).__init__(parent)
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
        texto = str(super(FLLineEdit, self).text())
        denegarCambio_ = False
        denegarCambioEnteros_ = False
        cambiarComa_ = False
        decimales_ = None
        posComa_ = -1

        if texto == "" or texto is None:
            return
        """
        if self._tipo == "int" or self._tipo == "uint":
            if not texto is None:
                try:
                    float(decimales_)
                except:
                        denegarCambio_ = True

            texto = texto.replace(",",".")
            try:
                posComa_ = texto.index(".")
            except:
                if posComa_ > -1:
                    denegarCambio_ = True

        """
        if self._tipo == "string":
            if len(texto) > int(self._longitudMax):
                denegarCambio_ = True

        if self._tipo == "double":

            texto_old = texto
            if (QtCore.QLocale().decimalPoint() == ","):
                texto = texto.replace(".", ",")
            else:
                texto = texto.replace(",", ".")

            if not texto_old == texto:
                cambiarComa_ = True

            try:
                posComa_ = texto.index(".")
                # print("Coma encontrada en pos", posComa_, denegarCambio_)
            except Exception:
                # print("Coma no encontrada", denegarCambio_)
                pass

            if posComa_ > -1:
                decimales_ = texto[posComa_ + 1:]

                if len(decimales_) > int(self._partDecimal):
                    # print("Parte decimal (%s) se pasa de %s" % (decimales_ , self._partDecimal))
                    denegarCambio_ = True

            enteros_ = texto

            if posComa_ > -1:
                enteros_ = texto[:posComa_]

            # print("enteros ...", enteros_)
            if len(enteros_) > int(self._partInteger):
                # print("Parte entera (%s) se pasa de %s" % (enteros_ , self._partInteger))
                denegarCambioEnteros_ = True

            # print("Decimales =", decimales_ , type(decimales_))
            if decimales_ is not None:
                try:
                    float(decimales_)
                except Exception:
                    # print("Decimal esta mal", decimales_, len(decimales_))
                    if len(decimales_) > 0:
                        denegarCambio_ = True

            # print("Enteros =", enteros_, type(enteros_))
            try:
                float(enteros_)
            except Exception:
                # print("Entero esta mal")
                denegarCambioEnteros_ = True
            # if not decimales_.isdecimal():
                # denegarCambio_ = True

            # if not enteros_.isdecimal():
                # denegarCambioEnteros_ = True

        # print("Procesado final", texto, denegarCambio_)

        if denegarCambio_:
            texto = texto[0:len(texto) - 1]
            super(FLLineEdit, self).setText(texto)

        if denegarCambioEnteros_ and decimales_ is not None:
            texto = "%s%s%s" % (
                enteros_[0:len(enteros_) - 1], QtCore.QLocale().decimalPoint(), decimales_)
            super(FLLineEdit, self).setText(texto)
        elif denegarCambioEnteros_ and decimales_ is None:
            texto = enteros_[0:len(enteros_) - 1]
            super(FLLineEdit, self).setText(texto)

        if cambiarComa_:
            super(FLLineEdit, self).setText(texto)

    def setText(self, texto, b=True):
        if self._maxValue:
            if self._maxValue < int(texto):
                texto = self._maxValue

        texto = str(texto)

        # Miramos si le falta digitos a la parte decimal ...
        if self._tipo == "double" and len(texto) > 0:
            if texto == "0":
                d = 0
                texto = "0."
                while d < self._partDecimal:
                    texto = texto + "0"
                    d = d + 1

            i = None
            l = len(texto) - 1
            try:
                i = texto.index(".")
            except Exception:
                pass

            if i:
                # print("Posicion de . (%s) de %s en %s" % (i, l, texto))
                f = (i + self._partDecimal) - l
                # print("Part Decimal = %s , faltan %s" % (self._partDecimal, f))
                while f > 0:
                    texto = texto + "0"
                    f = f - 1

        super(FLLineEdit, self).setText(texto)
        pineboolib.project._DGI._par.addQueqe(
            "setText_%s" % self._fieldName, texto)
        self.textChanged.emit(texto)

    def text(self):
        texto = str(super(FLLineEdit, self).text())

        if texto is "":
            texto = None

        if texto is None:
            if self._tipo == "string":
                texto = ""

            elif self._tipo == "double":
                d = 0
                texto = "0."
                while d < self._partDecimal:
                    texto = texto + "0"
                    d = d + 1

        return str(texto)
