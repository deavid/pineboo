# -*- coding: utf-8 -*-
import pineboolib
from pineboolib.utils import _path, _dir, filedir
from importlib import machinery

from sqlalchemy import String, orm, event
from sqlalchemy.orm import relationship

import importlib
import traceback
import sys
import os
import logging

logger = logging.getLogger("PNControlsFactory")

processed_ = []


def base_model( name ):
    #print("Base", name)
    path = _path("%s.mtd" % name, False)
    if path:
        path = "%s_model.py" % path[:-4]
        if os.path.exists(path):
            try:
                return machinery.SourceFileLoader( name , path).load_module() if path else None
            except Exception as exc:
                logger.warning("Error recargando model base:\n%s\n%s", exc, traceback.format_exc())
                pass 
    
    return None


def load_model( nombre ):
    
    if nombre is None:
        return
    
    #if nombre in processed_: 
    #    return None
    
    #processed_.append(nombre)
    
    
    from pineboolib import qsa as qsa_dict_modules
    
    
    nombre_qsa = nombre.replace("_model", "")
    model_name = nombre_qsa[0].upper() + nombre_qsa[1:]
    
    #mod = getattr(qsa_dict_modules, model_name, None)
    #if mod is None:
    #    mod = base_model(nombre)
    #    if mod:
    #        setattr(qsa_dict_modules, model_name, mod)
    
    
    
    db_name = pineboolib.project.conn.DBName()
    
    mod = None
    file_path = filedir("..", "tempdata", "cache", db_name, "models", "%s_model.py" % nombre)
    
    if os.path.exists(file_path):
        module_path = "tempdata.cache.%s.models.%s_model" % (db_name, nombre)
        if module_path in sys.modules:
            #print("Recargando", module_path)
            try:
                mod = importlib.reload(sys.modules[module_path])
            except Exception as exc:
                logger.warning("Error recargando módulo:\n%s\n%s", exc, traceback.format_exc())
                pass 
        else:
            #print("Cargando", module_path)
            try:
                mod = importlib.import_module(module_path)
            except Exception as exc:
                logger.warning("Error cargando módulo:\n%s\n%s", exc, traceback.format_exc())
                pass 
            #models_[nombre] = mod
    
    
    #if mod:
    #    setattr(qsa_dict_modules, model_name, mod)
    
    #print(3, nombre, mod)
    return mod
       
    #if mod is not None:
    #    setattr(qsa_dict_modules,  model_name, mod)
    
    
    

def load_models():
    #print(1, "load_models!!")
    
    db_name = pineboolib.project.conn.DBName()
    tables = pineboolib.project.conn.tables()
    #models_ = {}
    from pineboolib.pncontrolsfactory import aqApp
    from pineboolib import qsa as qsa_dict_modules
    Base = aqApp.db().declarative_base()
    
    setattr(qsa_dict_modules, "Base", aqApp.db().declarative_base())
    setattr(qsa_dict_modules, "session", aqApp.db().session())
    setattr(qsa_dict_modules, "engine", aqApp.db().engine())
    
    for t in tables:
        #print(t, "*")
        try:
            mod = base_model(t)
        except Exception:
            mod = None
        #print(t, mod)
        if mod is not None:
            model_name = "%s%s" % (t[0].upper(), t[1:])
            class_ = getattr(mod, model_name, None)
            if class_ is not None:
                #print("Registrando", model_name)
                setattr(qsa_dict_modules, model_name, class_)
    
    

    
    for root, dirs, files in os.walk(filedir(".." , "tempdata" , "cache", db_name, "models")):
        for nombre in files: #Buscamos los presonalizados
            if nombre.endswith("pyc"):
                continue
            
            nombre = nombre.replace("_model.py", "")
            mod = load_model(nombre)
            if mod is not None:
                model_name = "%s%s" % (nombre[0].upper(), nombre[1:])
                
                class_ = getattr(mod, model_name, None)
                if class_ is not None:
                    #print("Registro 2", model_name)
                    setattr(qsa_dict_modules, model_name, class_)
    
    
    
    
            
Calculated = String    
"""
def before_commit(s):
    for o in s.new:
        o.beforeCommit()
    for o in s.dirty:
        o.beforeCommit()
    for o in s.deleted:
        o.beforeCommit()   
        

def after_commit(s):
    for o in s.new:
        o.afterCommit()
    for o in s.dirty:
        o.afterCommit()
    for o in s.deleted:
        o.afterCommit()   

def after_flush(*args):
    print("****", args)
    
"""