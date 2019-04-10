# -*- coding: utf-8 -*-
from pineboolib.fllegacy.flsqlcursor import FLSqlCursor
from pineboolib.utils import _dir

import importlib
import os
import sys

class default_schema(object):
    
    _orm = None
    
    def __init__(self):
        print("Nuevo objeto", object_name)
        self._orm = orm()

    def __getattr__(self, name):
        ret_ = getattr(self._orm, name, None)
        return ret_
        

def load_object(obj_name):
    module_path = "tempdata.cache.%s.objects.%s" % (pineboolib.conn.DBName(), obj_name) 
    
    if module_path in sys.modules:
        mod = importlib.reload(sys.modules[module_path])
    else:
        mod = importlib.import_module(module_path)
    
    print("---->", mod)
    return mod
    


class orm(object):
    
    table_cursor = None
    object_tree_dict = None
    
    def connect_to_table(self, *args):
        if self.table_cursor is not None:
            del self.table_cursor
        
        self.object_tree_dict = {}
        self.table_cursor = FLSqlCursor(*args)
    
    
    def __getattr__(self, name):
        if self.table_cursor:
            #print("Buscando", name)
            ret = None
            if name == "pk":
                name = self.table_cursor.primaryKey()
        
        
            field = self.table_cursor.metadata().field(name)
            if field is not None:
                field_relation = field.relationM1()
                value = self.table_cursor.valueBuffer(field.name())
                       
                if isinstance(field_relation, FLRelationMetaData):
                    relation_table_name = field_relation.foreignTable()
                    relation_field_name = field_relation.foreignField()
            
                    key_ = "%s_%s" % ( relation_table_name, relation_field_name)
            
                    if key_ not  in self.object_tree_dict.keys():
                        rel_mtd = aqApp.db().manager().metadata(relation_table_name)
            
                        relation_mtd = FLRelationMetaData(relation_table_name, field_relation.field(), FLRelationMetaData.RELATION_1M, False, False, True)
                        relation_mtd.setField(relation_field_name)
            
                        if relation_table_name and relation_field_name:
                            #self.object_tree_dict[key_] =  FLSqlCursor(relation_table_name, True, self.table_cursor.conn(), self.table_cursor, relation_mtd)
                            self.object_tree_dict[key_] = load_object(relation_table_name)
                            self.object_tree_dict[key_].connect_to_table(relation_table_name, True, self.table_cursor.conn(), self.table_cursor, relation_mtd)
            
                    rel_object = self.object_tree_dict[key_]
                    
                    rel_object.select()
            
                    ret = rel_object
            
                else:
                    ret = self.table_cursor.valueBuffer(field.name())
                    
            return ret
        
        
    
    
    