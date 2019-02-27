# # -*- coding: utf-8 -*-

from pineboolib.plugins.dgi.dgi_schema import dgi_schema
from pineboolib import decorators
import pineboolib


from importlib import import_module
from PyQt5 import QtCore

import traceback
import logging
import sys
import os

logger = logging.getLogger(__name__)



class dgi_aqnext(dgi_schema):


    def __init__(self):
        # desktopEnabled y mlDefault a True
        super().__init__()
        self._name = "aqnext"
        self._alias = "AQNEXT"
        self.setUseDesktop(False)
        self.setUseMLDefault(True)
        self.setLocalDesktop(False)
        self._mainForm = None
        self._use_authentication = False # True La autenticación la realiza pineboolib
        self.showInitBanner()
        self._show_object_not_found_warnings = False
        self.qApp = QtCore.QCoreApplication
        self._alternative_content_cached = False
        

    def extraProjectInit(self):
        pass
    
    def create_app(self):
        app = QtCore.QCoreApplication(sys.argv)
        return app

    def setParameter(self, param):
        self._listenSocket = param

    def mainForm(self):
        if not self._mainForm:
            self._mainForm = mainForm()
        return self._mainForm

    def __getattr__(self, name):
        return super().resolveObject(self._name, name)
    
    def exec_(self):
        from pineboolib.pncontrolsfactory import SysType, aqApp
        sys = SysType()
        logger.warn("DGI_%s se ha inicializado correctamente" % self._alias)
        logger.warn("Driver  DB: %s", aqApp.db().driverAlias())
        logger.warn("Usuario DB: %s", sys.nameUser())
        logger.warn("Nombre  DB: %s", sys.nameBD())
    
    def processEvents(self):
        return QtCore.QCoreApplication.processEvents()
    
    

    def authenticate(self, **kwargs):
        user = kwargs["username"]
        password = kwargs["password"]
    
    
    def use_authentication(self):
        return self._use_authentication
    
    #def interactiveGUI(self):       
        #return "Django"
    
    """
    def content_cached(self, tmp_dir, db_name, module_id, ext_, name_, sha_key):
        data = None
        utf8_ = False
        if ext_ == "qs":
            from django.conf import settings
            folder_ = settings.PROJECT_ROOT
            legacy_path = "%s/legacy/%s/%s.py" % (folder_, module_id, name_)
            print("**** Buscando en path", legacy_path)
            if os.path.exists(legacy_path):
                data = pineboolib.project.conn.managerModules().contentFS(legacy_path, True)
        else:
            if os.path.exists("%s/cache/%s/%s/file.%s/%s" % (tmp_dir, db_name, module_id, ext_, name_)):
                if ext_ == "kut":
                    utf8_ = True
                data = pineboolib.project.conn.managerModules().contentFS("%s/cache/%s/%s/file.%s/%s/%s.%s" % (tmp_dir, db_name, module_id, ext_, name_, sha_key, ext_), utf8_)
        
        return data
    """
    def alternative_script_path(self, script_name, app = None):
        from django.conf import settings
        import glob
        
        ret_ = None
        
        folder_ = settings.PROJECT_ROOT
        if app is None:
            app = "**"
        
        
        
        for file_name in glob.iglob("%s/legacy/%s/%s" % (folder_, app, script_name), recursive=True):
            if file_name.endswith(script_name):
                ret_ = file_name
                break
            
        return ret_
    
    def register_script(self, app, module_name, script_name, prefix):

        
        ret_ = self.alternative_script_path("%s.py" % script_name, app)
        if ret_ is None:
            raise ImportError
        
        

        from pineboolib import qsa as qsa_dict_modules
        from pineboolib.pnapplication import DelayedObjectProxyLoader, XMLAction
            
        action = XMLAction()
        action.name = module_name
        action.alias = module_name
        action.form = None
        action.table = None
        action.scriptform = module_name
        
        #Carganmos módulo
        if module_name == script_name:
            #Estamos aquí porque script_name existe en model. Hay que ver si existe el legacy
            if hasattr(qsa_dict_modules, action.name):
                #Lo convertimos en legacy
                legacy = getattr(qsa_dict_modules, action.name)
                setattr(qsa_dict_modules, "%s_legacy" % action.name, legacy)
                delattr(qsa_dict_modules, action.name) #Borramos el script del arbol
            
            #Se crea el script
            setattr(qsa_dict_modules, action.name, DelayedObjectProxyLoader(action.load, name="QSA.Module.%s" % app))
            pineboolib.project.actions[action.name] = action
            if prefix == "":
                return
        
        
        action_xml = XMLAction()
        action_xml.name = module_name
        
        if "%s_legacy" in action_xml.name not in pineboolib.project.actions.keys():
            if action_xml.name in pineboolib.project.actions.keys():
                pineboolib.project.actions["%s_legacy" % action_xml.name] = pineboolib.project.actions[action_xml.name]
                del pineboolib.project.actions[action_xml.name]
            
        
        if prefix == "form":
            if hasattr(qsa_dict_modules, "form" + action_xml.name):
                #Cambiamos a legacy el script existente
                legacy = getattr(qsa_dict_modules, action_xml.name)
                setattr(qsa_dict_modules, "form%s_legacy" % action_xml.name, legacy)
                delattr(qsa_dict_modules, action_xml.name)
                
                
            action_xml.table = action_xml.name
            action_xml.scriptform = script_name 
            pineboolib.project.actions[action_xml.name] = action_xml
            delayed_action = DelayedObjectProxyLoader(action_xml.load, name="QSA.Module.%s.Action.form%s" % (app, action_xml.name))
            #print("Creando", "form" + module_name)
            setattr(qsa_dict_modules, "form" + action_xml.name, delayed_action)

        if prefix == "formRecord":
            if hasattr(qsa_dict_modules, "formRecord" + action_xml.name):
                #Cambiamos a legacy el script existente
                legacy = getattr(qsa_dict_modules, action_xml.name)
                setattr(qsa_dict_modules, "formRecord%s_legacy" % action_xml.name, legacy)
                delattr(qsa_dict_modules, action_xml.name)
                
            action_xml.table = action_xml.name
            action_xml.script = script_name 
            pineboolib.project.actions[action_xml.name] = action_xml
            delayed_action = DelayedObjectProxyLoader(action_xml.formRecordWidget ,name="QSA.Module.%s.Action.formRecord%s" % (app, action_xml.name))
            setattr(qsa_dict_modules, "formRecord" + action_xml.name, delayed_action)
            #print("Creando **** ", getattr(qsa_dict_modules, "formRecord" + module_name))
        
        
