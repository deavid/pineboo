# -*- coding: utf-8 -*-
import pineboolib
from pineboolib.utils import _path, _dir, filedir
from importlib import machinery

from sqlalchemy import String

import importlib
import traceback
import sys
import os

processed_ = []


def base_model( name ):
    print("Base", name)
    path = _path("%s.mtd" % name, True)
    if path:
        path = "%s_model.py" % path[:-4]
        if os.path.exists(path):
            return machinery.SourceFileLoader( name , path).load_module() if path else None
    
    return None


def load_model( nombre ):
    
    if nombre is None:
        return
    
    from pineboolib import qsa as qsa_dict_modules
    db_name = pineboolib.project.conn.DBName()
    print(2, "load", nombre)
    if nombre in processed_: 
        return
    
    processed_.append(nombre)
    
    nombre_qsa = nombre.replace("_model", "")
    model_name = nombre_qsa[0].upper() + nombre_qsa[1:] 
    
    mod = None
    module_path = "tempdata.cache.%s.models.%s" % (db_name, nombre)
    if not os.path.exists(filedir("..", "tempdata", "cache", db_name, "models", nombre)):
        print("No existe personalizado de", nombre)
        mod = base_model( nombre )
    else:
        if module_path in sys.modules:
            print("Recargando", module_path)
            try:
                mod = importlib.reload(sys.modules[module_path])
            except Exception as exc:
                print("** ***", exc)
                pass 
        else:
            print("Cargando", module_path)
            try:
                mod = importlib.import_module(module_path)
            except Exception as exc:
                print("** *** **", traceback.format_exc())
                pass 
            #models_[nombre] = mod
    
    
    return mod
       
    #if mod is not None:
    #    setattr(qsa_dict_modules,  model_name, mod)
    
    
    

def load_models():
    print(1, "load_models!!")
    db_name = pineboolib.project.conn.DBName()
    #models_ = {}
    for root, dirs, files in os.walk(filedir(".." , "tempdata" , "cache", db_name, "models")):
        for nombre in files:
            if nombre.endswith("pyc"):
                continue
            
            load_model(nombre)
            
            
            
            
Calculated = String       
    
    
    