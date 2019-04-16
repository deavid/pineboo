# -*- coding: utf-8 -*-
from pineboolib.fllegacy.flsqlcursor import FLSqlCursor
from pineboolib.fllegacy.flrelationmetadata import FLRelationMetaData
from pineboolib.utils import _dir

import pineboolib
import importlib

import os
import sys

class default_schema(object):
    
    _orm = None
    
    def __init__(self):
        self._orm = orm()

    def __getattr__(self, name):
        ret_ = getattr(self._orm, name, None)
        return ret_
    
    def __getitem__(self, name):
        return getattr(self, name)
    
    def __setitem__(self, name, value):
        setattr(self, name, value)
    
    def __setattr__(self, name, value):
        if hasattr(self._orm, name) and self._orm.table_cursor:
            if name in self._orm.table_cursor.metadata().fieldsNames():
                self._orm.set_value(name, value)
                return

        self.__dict__[name] = value
        
    
    def __del__(self):
        for d in list(self.__dict__.keys()):
            del self.__dict__[d]
        if getattr(self._orm, "table_cursor", None):
            del self._orm.table_cursor
        if getattr(self, "_orm", None):
            del self._orm
        

def load_object(obj_name, *args, **kwargs):
    module_path = "tempdata.cache.%s.objects.%s" % (pineboolib.project.conn.DBName(), obj_name)
    module_path = module_path.lower()
    obj_name = obj_name[0].upper() + obj_name[1:]
    if module_path in sys.modules:
        mod = importlib.reload(sys.modules[module_path])
    else:
        mod = importlib.import_module(module_path)
    
    fun = getattr(mod, obj_name, None)
    if fun is not None:
        ret_ = fun(*args, **kwargs)
    else:
        ret_ = None
    
    return ret_
    


class orm(object):
    
    table_cursor = None
    object_tree_dict = None
    connection = None
    
    def __init__(self):
        self.table_cursor = None
        self.connection = connection_obj
    
    
    def connect_to_table(self, *args, **kwargs):
        if self.table_cursor is not None:
            del self.table_cursor
        
        cursor = None
        if "field_relation" in kwargs:
            name = kwargs["field_relation"]
            cursor = kwargs["cursor"]
            #if hasattr(cursor, "table_cursor"):
            #    cursor = cursor.table_cursor
            
            field = pineboolib.project.conn.manager().metadata(args[0]).field(name)
            if field is not None:
                field_relation = field.relationM1()
                value = cursor.valueBuffer(field.name())   
                if field_relation is not None:
                    relation_table_name = field_relation.foreignTable()
                    relation_field_name = field_relation.foreignField()
                    relation_mtd = FLRelationMetaData(relation_table_name, field_relation.field(), FLRelationMetaData.RELATION_1M, False, False, True)
                    relation_mtd.setField(relation_field_name)
                    new_args = [args[0], True, cursor.conn(), cursor, relation_mtd]
                    #new_args = [args[0], True, cursor.conn(), cursor, field_relation]
        else:
            new_args = args
            
        self.object_tree_dict = {}
        self.table_cursor = FLSqlCursor(*new_args)
        #self.table_cursor.setModeAccess(self.table_cursor.Edit)
        #self.table_cursor.refreshBuffer()
        if cursor:
            cursor.newBuffer.connect(self.table_cursor.select)
            self.table_cursor.select()
            
        
        return True
    
    def select(self, value= None):
        
        
        if self.table_cursor:
            self.table_cursor.select(value)
            self.table_cursor.first()
            self.table_cursor.setModeAccess(self.table_cursor.Edit)
            self.table_cursor.refreshBuffer()
    
    def save(self):
        self.table_cursor.commitBuffer()
    
    def rollback(self):
        self.table_cursor.rollback()
        self.table_cursor.refreshBuffer()
    
    def __getattr__(self, name): 
        #print("buscando name", name)
        ret = None
        if self.table_cursor:
            if name == "pk":
                name = self.table_cursor.primaryKey()            
            
            field = self.table_cursor.metadata().field(name)
            if field is not None:
                if self.table_cursor.relation():
                    if name == self.table_cursor.relation().foreignField():
                        return self.table_cursor.cursorRelation()
                
                field_relation = field.relationM1()
                value = self.table_cursor.valueBuffer(field.name())
                if field_relation is not None:
                    relation_table_name = field_relation.foreignTable()
                    relation_field_name = field_relation.foreignField()
            
                    key_ = "%s_%s" % ( relation_table_name, relation_field_name)
            
                    if key_ not in self.object_tree_dict.keys(): #Si el objeto no está cacheado
                        #rel_mtd = aqApp.db().manager().metadata(relation_table_name)
            
                        relation_mtd = FLRelationMetaData(relation_table_name, field_relation.field(), FLRelationMetaData.RELATION_1M, False, False, True)
                        relation_mtd.setField(relation_field_name)
            
                        if relation_table_name and relation_field_name:
                            obj = load_object(relation_table_name)
                            if obj is not None: #Si hay objeto , monto el orm
                                obj.connect_to_table(relation_table_name, True, self.table_cursor.conn(), self.table_cursor, relation_mtd)
                        else:
                            obj = None
                                
                        self.object_tree_dict[key_] = obj
            
                    rel_object = self.object_tree_dict[key_] #retorna el objeto
                    if rel_object is not None:
                        rel_object.refresh()
            
                    ret = rel_object
            
                else:
                    ret = self.table_cursor.valueBuffer(field.name())
            else:
                ret = getattr(self.table_cursor, name, None)
        
        return ret
    
    def set_value(self, field_name, value):
        #print("seteando", field_name, value)
        self.table_cursor.setValueBuffer(field_name, value)
        pass    
        
    
class connection_class(object):

    def execute(self, sql):
        cursor = pineboolib.project.conn.cursor()
        cursor.execute(sql)   
        return cursor 

connection_obj = connection_class()
    