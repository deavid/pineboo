# -*- coding: utf-8 -*-
from PyQt5 import QtCore
import logging
import os

logger = logging.getLogger(__name__)



class FLSqlCursor(QtCore.QObject):
    
    parent_cursor = None
    _buffer_changed = None
    _before_commit = None
    _after_commit = None
    _buffer_commited = None
    _inicia_valores_cursor = None
    _buffer_changed_label = None
    _validate_cursor = None
    _validate_transaction = None
    _cursor_accepted = None
    cursor_tree_dict = {}
    show_debug = None
    
    def __init__(self, cursor, stabla):
        super().__init__()
        self.parent_cursor = cursor
        self.parent_cursor.setActivatedBufferChanged(False)
        self.parent_cursor.setActivatedBufferCommited(False) 
        self.cursor_tree_dict = {}    
        self.show_debug = False
        
        
        
        if stabla is not None:
            from pineboolib.pncontrolsfactory import aqApp       
            module_name = aqApp.db().managerModules().idModuleOfFile("%s.mtd" % stabla)
            model_file = "models.%s.%s" % (module_name, stabla)
            if os.path.exists(model_file):
                (self._model, self._buffer_changed, self._before_commit, self._after_commit, self._buffer_commited, self._inicia_valores_cursor, self._buffer_changed_label, self._validate_cursor, self._validate_transaction, self._cursor_accepted) = self.obtener_modelo(stabla)
                #self._stabla = self._model._meta.db_table
    
    
    def buffer_changed_signal(self, scampo):
        if self._buffer_changed is None:
            return True

        return self._buffer_changed(scampo, self.parent_cursor)

    def buffer_commited_signal(self):
        if not self._activatedBufferCommited:
            return True

        if self._buffer_commited is None:
            return True

        try:
            return self._buffer_commited(self.parent_cursor)
        except Exception as exc:
            print("Error inesperado", exc)

    def before_commit_signal(self):
        if not self._activatedCommitActions:
            return True

        if self._before_commit is None:
            return True

        return self._before_commit(self.parent_cursor)

    def after_commit_signal(self):
        if not self._activatedCommitActions:
            return True

        if self._after_commit is None:
            return True

        return self._after_commit(self.parent_cursor)

    def inicia_valores_cursor_signal(self):
        if self._inicia_valores_cursor is None:
            return True

        return self._inicia_valores_cursor(self.parent_cursor)

    def buffer_changed_label_signal(self, scampo):
        if self._buffer_changed_label is None:
            return {}

        import inspect
        expected_args = inspect.getargspec(self._buffer_changed_label)[0]
        if len(expected_args) == 3:
            return self._buffer_changed_label(self._model, scampo, self.parent_cursor)
        else:
            return self._buffer_changed_label(scampo, self.parent_cursor)

    def validate_cursor_signal(self):
        if self._validate_cursor is None:
            return True

        return self._validate_cursor(self.parent_cursor)

    def validate_transaction_signal(self):
        if self._validate_transaction is None:
            return True

        return self._validate_transaction(self.parent_cursor)

    def cursor_accepted_signal(self):
        if self._cursor_accepted is None:
            return True

        return self._cursor_accepted(self.parent_cursor)
    
    def obtener_modelo(self, stabla):
        #logger.warn("****** obtener_modelo %s", stabla, stack_info = True)
        from YBLEGACY.FLAux import FLAux
        return FLAux.obtener_modelo(stabla)
    
    
    def assoc_model(self):
        import pineboolib
        cur_name = self.parent_cursor.curName()
        #logger.warn("Asociando modelo %s a cursor %s", cur_name, self.parent_cursor )
        self.parent_cursor._meta_model = pineboolib.project._DGI.load_meta_model(cur_name)
        
    
    def build_cursor_tree_dict(self, recursive = False): 
        lev = 2
        l = 0
        cur_rel = None
        while True:
            if cur_rel is None:    
                cur_rel = self.parent_cursor.cursorRelation()
            else:
                cur_rel = cur_rel.cursorRelation()
            
            
            
            
            if cur_rel:
                if cur_rel.meta_model() and cur_rel.cursorRelation():
                    if l == lev:
                        if self.show_debug:
                            print("Corte cíclica nivel", lev, self.parent_cursor.curName())
                        recursive = False
                        break
            
                    l += 1
                else:
                    break
            else:
                break
        
        
        from pineboolib.pncontrolsfactory import FLSqlCursor as FLSqlCursor_legacy, FLRelationMetaData
        mtd = self.parent_cursor.metadata()
        fields_list = mtd.fieldList()
        if fields_list:
            for field in fields_list:
                field_relation = field.relationM1()
                if isinstance(field_relation, FLRelationMetaData) and recursive:
                    relation_table_name = field_relation.foreignTable()
                    relation_field_name = field_relation.foreignField()
                    if relation_table_name and relation_field_name:
                        key_ = "%s_%s" % ( relation_table_name, relation_field_name)
                        print("Creando", relation_table_name, relation_field_name,"desde", self.parent_cursor.curName(), field_relation.field())
                        self.cursor_tree_dict[key_] =  FLSqlCursor_legacy(relation_table_name, True, self.parent_cursor.d.db_, self.parent_cursor, field_relation)
    
    def populate_meta_model(self):
        fields_list = self.parent_cursor.metadata().fieldList()
        meta_model = self.parent_cursor.meta_model()
        if meta_model is not None:
            #meta_model._meta = {}
            #setattr(meta_model._meta, "db_table" ,self.parent_cursor.curName())
            
            if fields_list:
                for field in fields_list:
                    field_name = field.name()
                    field_relation = field.relationM1()
                    value = self.parent_cursor.buffer().value(field_name)
                    if field_relation is not None:
                        key_ = "%s_%s" % ( field_relation.foreignTable(), field_relation.foreignField())
                        if key_ in self.cursor_tree_dict.keys():
                            value = self.cursor_tree_dict[key_].meta_model()                            
                    
                    if self.show_debug:
                        print("Populate", self.parent_cursor.curName(),":", field_name, "--->", value)
                    setattr(meta_model, field_name, value)
          
           
    
    
    def getYBschema(self, cursor):
        """Permite obtener definicion de schema de uso interno de YEBOYEBO"""
        import pineboolib
        from pineboolib.pncontrolsfactory import FLSqlCursor
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
            dict[key] = collections.OrderedDict()
            dict[key]['verbose_name'] = field.alias()
            """ FIXME: help_text """
            dict[key]['help_text'] = None
            dict[key]['locked'] = False #FIXME: hay que ver el criterio de locked
            dict[key]['field'] = False
            visible = False if cursor.primaryKey() == key or key == 'desc' else True 
                
            dict[key]['visible'] = visible
            dict[key]['tipo'] = pineboolib.utils.get_tipo_aqnext(field.type())
            
            dict[key]['visiblegrid'] = field.visibleGrid()
            dict[key]['required'] = not field.allowNull()
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
                cursor_rel = FLSqlCursor(table_name)
            
                rel_meta_model = cursor_rel.meta_model()
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
            