# # -*- coding: utf-8 -*-

from pineboolib.plugins.dgi.dgi_schema import dgi_schema
from pineboolib import decorators
import pineboolib

from PyQt5 import QtCore


from xmljson import yahoo as xml2json
from xml.etree.ElementTree import fromstring
from json import dumps
from xml import etree




from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple

from jsonrpc import JSONRPCResponseManager, dispatcher

import traceback
import logging
import sys
import inspect

logger = logging.getLogger(__name__)

cursor_dict = {}


class parser_options(object):
    
    def hello(self, *args):
        return "Welcome to pineboo server"
    
    def db_name(self, *args):
        from pineboolib.pncontrolsfactory import aqApp
        return aqApp.db().DBName()
    
    
    def __getattr__(self, name):
        print("** parser_options no contiene", name)
        

parser_server = parser_options()


class parser(object):

    @Request.application
    def receive(self, request):
        response = None
        #print("**", request.data)
        try:
            response = JSONRPCResponseManager.handle(request.data, dispatcher)
        except Exception:
            response = "Not Found"
            
        return Response(response.json, mimetype='application/json')
    

    @dispatcher.add_method
    def dbdata(*args):
        dict_ = args[0]
        from pineboolib.pncontrolsfactory import aqApp
        
        if dict_["function"] == "execute":
            if not dict_["arguments"]["cursor_id"] in cursor_dict.keys():
                cursor_dict[dict_["arguments"]["cursor_id"]] = aqApp.db().driver().conn_.cursor()
            
            #res = []
            try:
                cursor_dict[dict_["arguments"]["cursor_id"]].execute(dict_["arguments"]["sql"])
            #    for data in cursor_dict[dict_["arguments"]["cursor_id"]]:
            #        res.append(data)
                    
            except:
                print("Error %s  %s %s" % (dict_["arguments"]["cursor_id"], dict_["arguments"]["sql"] , dict_["function"]), traceback.format_exc())
            
            return
        
        if dict_["function"] == "fetchone":
            ret = None
            
            try:
                ret = cursor_dict[dict_["arguments"]["cursor_id"]].fetchone()
                #print("2", dict_["arguments"]["cursor_id"], ret)
            except:
                print("Error %s" % dict_["function"], traceback.format_exc())
            return ret
        
        if dict_["function"] == "refreshQuery":
            try:
                fun = getattr(aqApp.db().driver(), dict_["function"])
                if not dict_["arguments"]["cursor_id"] in cursor_dict.keys():
                     cursor_dict[dict_["arguments"]["cursor_id"]] = aqApp.db().driver().conn_.cursor()
                
                fun(dict_["arguments"]["curname"], dict_["arguments"]["fields"], dict_["arguments"]["table"], dict_["arguments"]["where"], cursor_dict[dict_["arguments"]["cursor_id"]], aqApp.db().driver().conn_)
            except:
                print("Error refreshQuery", traceback.format_exc())
            return
        
        if dict_["function"] == "refreshFetch":
            try:
                fun = getattr(aqApp.db().driver(), dict_["function"])
                if not dict_["arguments"]["cursor_id"] in cursor_dict.keys():
                     cursor_dict[dict_["arguments"]["cursor_id"]] = aqApp.db().driver().conn_.cursor()
                     
                fun(dict_["arguments"]["number"], dict_["arguments"]["curname"], dict_["arguments"]["table"], cursor_dict[dict_["arguments"]["cursor_id"]], dict_["arguments"]["fields"], dict_["arguments"]["where_filter"])
            except:
                print("Error refreshFetch", traceback.format_exc())
            return
        
        if dict_["function"] == "fetchAll":
            try:
                fun = getattr(aqApp.db().driver(), dict_["function"])
                if not dict_["arguments"]["cursor_id"] in cursor_dict.keys():
                     cursor_dict[dict_["arguments"]["cursor_id"]] = aqApp.db().driver().conn_.cursor()
                     
                return fun(cursor_dict[dict_["arguments"]["cursor_id"]], dict_["arguments"]["tablename"], dict_["arguments"]["where_filter"], dict_["arguments"]["fields"], dict_["arguments"]["curname"])
            except:
                print("Error fetchAll", traceback.format_exc())
            return
        
        
        
        if dict_["function"] == "close":
            try:
                cursor_dict[dict_["arguments"]["cursor_id"]].close()
                #print("3 close", dict_["arguments"]["cursor_id"])
                return
            except:
                print("Error %s" % dict_["function"], traceback.format_exc())
        
        fun = getattr(aqApp.db().driver(), dict_["function"], None)
            
                
        if fun is None:
            fun = getattr(parser_server, dict_["function"], None)
        
        if fun is not None:
            expected_args = inspect.getargspec(fun)[0]
            args_num = len(expected_args)
            #print("-->", fun, dict_["arguments"][:args_num])
            return fun(*dict_["arguments"][:args_num])
        
        
        return "Desconocido"



class dgi_server(dgi_schema):
    _par = None
    _W = {}
    _WJS = {}

    def __init__(self):
        # desktopEnabled y mlDefault a True
        super().__init__()
        self._name = "server"
        self._alias = "SERVER"
        self._listenSocket = 4000
        self.setUseDesktop(False)
        self.setUseMLDefault(False)
        self.setLocalDesktop(False)
        self.showInitBanner()
        self._mainForm = None
        self._show_object_not_found_warnings = False
        self.qApp = QtCore.QCoreApplication
        #self.parserDGI = parserJson()

    def alternativeMain(self, options):
        app = QtCore.QCoreApplication(sys.argv)
        if options.dgi_parameter:
            self._listenSocket = int(options.dgi_parameter)
        return app

    def exec_(self):
        self._par = parser()
        self.launchServer()

    def launchServer(self):
        #run_simple('localhost', self._listenSocket, self._par.receive, ssl_context="adhoc")
        run_simple('localhost', self._listenSocket, self._par.receive)

    def __getattr__(self, name):
        return super().resolveObject(self._name, name)
    
    def accept_file(self, name):
        #if name.endswith((".ui")):
        #    return False
        return True
