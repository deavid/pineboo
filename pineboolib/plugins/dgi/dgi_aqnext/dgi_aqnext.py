# # -*- coding: utf-8 -*-

from pineboolib.plugins.dgi.dgi_schema import dgi_schema
from pineboolib import decorators
import pineboolib


from importlib import import_module
from PyQt5 import QtCore

import traceback
import collections
import inspect
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
    
    def use_model(self):
        return True
    
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
        
    def load_meta_model(self, action_name, opt = None):
        import importlib, os
        import sys as python_sys
        from pineboolib.pncontrolsfactory import aqApp
        module_name = aqApp.db().managerModules().idModuleOfFile("%s.mtd" % action_name)
        module = None
        ret_ = None
        model_file = "models.%s.%s" % (module_name, action_name)
        if module_name is not None:
            try:
                module = importlib.import_module(model_file)     
            except:
                logger.warn("DGI: load_meta_model. No se encuentra el model de %s", action_name)
                module = None
                ret_ = None
                    
        if module is not None:           
            ret_ = getattr(module, action_name, None)
        
        return ret_
    
    def get_master_cursor(self, prefix, template = "master"):
        from pineboolib import qsa as qsa_tree
        import traceback
        
        module_name = prefix
        
        logger.warn("Cargando el prefix_master de %s", prefix)
        
        #if template == "master":        
        #    module_name = "form%s" % prefix
        #elif template == "formRecord":
        #    module_name = "formRecord%s" % prefix
        if template in ["master", "formRecord"]:
            module_name = "form%s" % prefix
            
        script_form_cursor = None
        module = getattr(qsa_tree, module_name, None)
        if module is not None:
            script_form_cursor = module.widget.cursor()
        else:
            logger.warn("*** DGI.get_master_cursor creando cursor %s sin action asociada ***", prefix)
            from pineboolib.pncontrolsfactory import FLSqlCursor
            script_form_cursor = FLSqlCursor(prefix)
            
        if script_form_cursor is None:
            logger.warn("*** DGI.get_master_cursor no encuentra cursor de %s***", prefix)
        
        if script_form_cursor and not script_form_cursor.meta_model():
            #print("**************************", prefix)
            try:
                script_form_cursor.assoc_model() #Asocia el modelo
                script_form_cursor.build_cursor_tree_dict(True)
            except:
                import traceback
        
        return script_form_cursor
    
    
    
    
    
    def cursor2json(self, cursor):
    
        if not cursor.isValid():
            logger.warn("Cursor inválido/vacío en %s", cursor.curName())
            return []
    
        meta_model = cursor.meta_model()
    
        import json, collections
    
        ret_ = None
    
        cursor.first()
        size_ = cursor.size()
        i = 0
        while i < size_:
            #dict_ = collections.OrderedDict()
            dict_ = {}
            pk = cursor.primaryKey()
            fields_list = cursor.metadata().fieldsNames()
            for f in fields_list:
                field_name = f if f != "pk" else pk
                value = cursor.valueBuffer(field_name)
                if cursor.metadata().field(field_name).type() in ["date"]:
                    if hasattr(value, "toString"):
                        value = value.toString()
                    value = value[:10]
            
                if f == pk:
                    dict_["pk"] = value
                dict_[f] = value
        
            if meta_model:
                calculateFields = meta_model.getForeignFields(meta_model, cursor.curName())
                for field in calculateFields:
                    if hasattr(meta_model, field["func"]):
                        dict_[field["verbose_name"]] = getattr(meta_model, field["func"])(meta_model)
            
                desc_function = getattr(meta_model, "getDesc", None)
                desc = None
                if desc_function:
                    expected_args = inspect.getargspec(desc_function)[0]
                    new_args = [meta_model]
                    desc = desc_function(*new_args[:len(expected_args)])
            
                dict_["desc"] = desc
            #for field in calculateFields:
            #        serializer._declared_fields.update({field["verbose_name"]: serializers.serializers.ReadOnlyField(label=field["verbose_name"], source=field["func"])})
        
        
            if size_ == 1:
                ret_ = dict_
                break
            else:
                if ret_ is None:
                    ret_ = []
                ret_.append(dict_)
        
            cursor.next()
            i += 1
        
        return ret_
    
    def getYBschema(self, cursor):
        """Permite obtener definicion de schema de uso interno de YEBOYEBO"""
        import pineboolib
        mtd = cursor.metadata()

        meta_model = cursor.meta_model()
    
        dict = collections.OrderedDict()
        meta = collections.OrderedDict()
        meta["verbose_name"] = mtd.alias()
    
        dict["desc"] = collections.OrderedDict()
        dict["desc"]["verbose_name"] = "Desc"
        dict["desc"]["help_text"] = None
        dict["desc"]["locked"] = True
        dict["desc"]["field"] = False
        dict["desc"]["visible"] = True
        dict["desc"]["tipo"] = 3
        dict["desc"]["visiblegrid"] = False
        fields_list = mtd.fieldsNames()
    
        fields_list.append("pk")
    
        for key in fields_list:
            field = mtd.field(key if key != "pk" else mtd.primaryKey())
            if field is None:
                continue
            dict[key] = collections.OrderedDict()
            dict[key]['verbose_name'] = field.alias() if key != "pk" else "Pk"
            """ FIXME: help_text """
            dict[key]['help_text'] = None
            dict[key]['locked'] = True if field.name() == mtd.primaryKey() else False #FIXME: hay que ver el criterio de locked
            dict[key]['field'] = False
                            
            dict[key]['visible'] = False if key in ['pk','desc'] else True 
            dict[key]['tipo'] = pineboolib.utils.get_tipo_aqnext(field.type())
            if field.type() == "stringlist":
                dict[key]['subtipo'] = 6
            
            dict[key]['visiblegrid'] = field.visibleGrid()
            if not field.allowNull():
                dict[key]['required'] = True
            if field.type() == "double":
                dict[key]['max_digits'] = field.partInteger()
                dict[key]['decimal_places'] = field.partDecimal()
            if field.hasOptionsList():
                dict[key]['optionslist'] = field.optionsList()
                dict[key]['tipo'] = 5
            
        #dict[key]['desc'] = cursor.primaryKey()
            relation = field.relationM1()     
            if relation is not None:
                table_name = relation.foreignTable() #Tabla relacionada
                dict[key]['rel'] = table_name
                dict[key]['to_field'] = relation.field() #Campo relacionado
                desc = None
                #print("Cursor relacionado", table_name)
                #cursor_rel = FLSqlCursor(table_name)
                
                rel_meta_model = getattr(meta_model,relation.foreignField())
                desc_function = getattr(rel_meta_model, "getDesc", None)
                if desc_function:
                    expected_args = inspect.getargspec(desc_function)[0]
                    new_args = [rel_meta_model]
                    desc = desc_function(*new_args[:len(expected_args)])
            
                if not desc or desc is None:
                        desc = cursor.db().manager().metadata(table_name).primaryKey()
                
                dict[key]['desc'] = desc
    
        if meta_model:
            calculateFields = meta_model.getForeignFields(meta_model, cursor.curName())
            for field in calculateFields:
                dict[field["verbose_name"]] = collections.OrderedDict()
                dict[field["verbose_name"]]["verbose_name"] = field["verbose_name"]
                dict[field["verbose_name"]]["help_text"] = None
                dict[field["verbose_name"]]["locked"] = True
                dict[field["verbose_name"]]["field"] = False
                dict[field["verbose_name"]]["visible"] = True
                dict[field["verbose_name"]]["tipo"] = 3
            
        return dict, meta
        
    def pagination(self, cursor, query): 
        limit_ = int(query["p_l"])
        page_ =  0 if isinstance(query["p_c"], bool) else int(query["p_c"])
        return pagination_class(cursor, limit_, page_)

class pagination_class(object):
    
    count = None
    _limit = None
    _page = None
    
    def __init__(self, cursor, limit, page):
        self.count = cursor.size()
        self._limit = limit
        self._page = page
    
    
    def get_next_offset(self):
        ret_ = None
        actual = 0
        i = 0         
        while i < self._page:
            actual += self._limit
            ret_ = actual
            i += 1
            
        
        return ret_
        
    
    def get_previous_offset(self):
        ret_ = None
        i = 0
        while i < self._page: 
            if ret_ is None:
                ret_ = 0
            else:
                ret_ += self._limit
            i += 1
        
        return ret_
        
        
        
    
        
        
        
        
