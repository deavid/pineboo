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
import datetime

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

def normalize_data(data):   
    if isinstance(data, (list, tuple)):
        new_data = []
        for line in data:
            if isinstance(line, (datetime.date, datetime.time)):
                #print("premio!!", type(line), line, type(data))
                new_data.append(line.__str__())
            else:
                #print(type(line), line)
                new_data.append(normalize_data(line))      
        
        data = new_data
                
    return data

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
    def call_function(*args):
        dict_ = args[0]
        func_name = dict_["function"]
        arguments = dict_["arguments"]
        from pineboolib.pncontrolsfactory import aqApp
        return aqApp.call(func_name, arguments)
        
        
    

    @dispatcher.add_method
    def dbdata(*args):
        dict_ = args[0]
        from pineboolib.pncontrolsfactory import aqApp
        list_fun = dict_["function"].split("__")
        fun_name = list_fun[1]
        id_conn = list_fun[0]
        cursor = None
        
        if fun_name == "hello":
            aqApp.db().removeConn("%s_remote_client" % id_conn)
            list_to_delete = []
            for k in list(cursor_dict.keys()):
                if k.startswith(id_conn):
                    cursor_dict[k] = None
                    del cursor_dict[k]
                
        conn = aqApp.db().useConn("%s_remote_client" % id_conn)
        
        

        #print("--->", dict_["function"], dict_["arguments"]["cursor_id"] if "cursor_id" in dict_["arguments"] else None)
        
        if "cursor_id" in dict_["arguments"]:          
            if not "%s_%s" % (id_conn, dict_["arguments"]["cursor_id"]) in cursor_dict.keys():
                cursor_dict["%s_%s" % (id_conn, dict_["arguments"]["cursor_id"])] = conn.cursor()
            
            cursor = cursor_dict["%s_%s" % (id_conn, dict_["arguments"]["cursor_id"])]
            
        
        if fun_name == "execute":           
            try:
                cursor.execute(dict_["arguments"]["sql"])
            #    for data in cursor_dict[dict_["arguments"]["cursor_id"]]:
            #        res.append(data)
                    
            except:
                print("Error %s  %s %s" % (dict_["arguments"]["cursor_id"], dict_["arguments"]["sql"] , fun_name), traceback.format_exc())

        
        elif fun_name == "fetchone":
            ret = None
            
            try:
                ret = cursor.fetchone()
            except:
                print("Error %s" % fun_name, traceback.format_exc())
            return normalize_data(ret)
        
        elif fun_name == "refreshQuery":
            try:
                fun = getattr(conn.driver(), fun_name)
                
                fun(dict_["arguments"]["curname"], dict_["arguments"]["fields"], dict_["arguments"]["table"], dict_["arguments"]["where"], cursor, aqApp.db().driver().conn_)
            except:
                print("Error refreshQuery", traceback.format_exc())

        
        elif fun_name == "refreshFetch":
            try:
                fun = getattr(conn.driver(), fun_name)
                     
                fun(dict_["arguments"]["number"], dict_["arguments"]["curname"], dict_["arguments"]["table"], cursor, dict_["arguments"]["fields"], dict_["arguments"]["where_filter"])
            except:
                print("Error refreshFetch", traceback.format_exc())
        
        elif fun_name == "fetchAll":
            try:
                fun = getattr(conn.driver(), fun_name)
                     
                ret = fun( cursor, dict_["arguments"]["tablename"], dict_["arguments"]["where_filter"], dict_["arguments"]["fields"], dict_["arguments"]["curname"])
                return normalize_data(ret)
            except:
                print("Error fetchAll", traceback.format_exc())

        
        elif fun_name == "fetchall":
            try:
                ret_ =  cursor.fetchall()
                return normalize_data(ret_)
            except:
                print("Error fetchall", traceback.format_exc())
        
        
        elif fun_name == "close":
            try:
                cursor.close()
                #print("3 close", dict_["arguments"]["cursor_id"])
            except:
                print("Error %s" % fun_name, traceback.format_exc())
        
        else:
            
            
            fun = getattr(conn.driver(), fun_name, None)
            
                
            if fun is None:
                fun = getattr(parser_server, fun_name, None)
        
            if fun is not None:
                expected_args = inspect.getargspec(fun)[0]
                args_num = len(expected_args)
                #print("-->", fun, dict_["arguments"][:args_num])
                return normalize_data(fun(*dict_["arguments"][:args_num]))
        
        
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
