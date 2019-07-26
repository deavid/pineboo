# -*- coding: utf-8 -*-
from pineboolib import logging
from PyQt5 import QtCore  # type: ignore
from pineboolib.application.metadata.pnrelationmetadata import PNRelationMetaData
from typing import Any

logger = logging.getLogger(__name__)


class DelayedObjectProxyLoader(object):

    """
    Constructor
    """

    cursor_tree_dict = {}
    last_value_buffer = None

    def __init__(self, obj, *args, **kwargs) -> None:
        if "field_object" in kwargs:
            self._field = kwargs["field_object"]
            del kwargs["field_object"]
        self._obj = obj
        self._args = args
        self._kwargs = kwargs
        self.loaded_obj = None
        self.logger = logging.getLogger("FLSQLCURSOR AQNEXT.DelayedObjectProxyLoader")
        self.cursor_tree_dict = {}
        self.last_value_buffer = None

    """
    Carga un objeto nuevo
    @return objeto nuevo o si ya existe , cacheado
    """

    def __load(self):
        from pineboolib.fllegacy.flsqlcursor import FLSqlCursor

        # print("**Carga", self._field.name())
        field_relation = self._field.relationM1()

        value = self._obj.valueBuffer(self._field.name())

        if value == self.last_value_buffer:
            return self.loaded_obj

        self.last_value_buffer = value
        if value in (None, ""):
            self.loaded_obj = None
            return self.loaded_obj

        if isinstance(field_relation, PNRelationMetaData):
            relation_table_name = field_relation.foreignTable()
            relation_field_name = field_relation.foreignField()

            key_ = "%s_%s" % (relation_table_name, relation_field_name)

            if key_ not in self.cursor_tree_dict.keys():
                # rel_mtd = aqApp.db().manager().metadata(relation_table_name)

                relation_mtd = PNRelationMetaData(
                    relation_table_name, field_relation.field(), PNRelationMetaData.RELATION_1M, False, False, True
                )
                relation_mtd.setField(relation_field_name)

                if relation_table_name and relation_field_name:
                    self.cursor_tree_dict[key_] = FLSqlCursor(relation_table_name, True, self._obj.conn(), self._obj, relation_mtd)

            rel_cursor = self.cursor_tree_dict[key_]

            rel_cursor.select()
            loaded_obj = rel_cursor.meta_model()

        else:
            loaded_obj = self._obj.valueBuffer(self._field.name())

        # if loaded_obj is None:
        #    self = None
        self.loaded_obj = loaded_obj
        return loaded_obj

    """
    Retorna una función buscada
    @param name. Nombre del la función buscada
    @return el objecto del XMLAction afectado
    """

    def __getattr__(self, name: str) -> Any:  # Solo se lanza si no existe la propiedad.
        obj_ = self.__load()
        ret = getattr(obj_, name, obj_) if obj_ is not None else None
        return ret

    def __le__(self, other) -> Any:
        obj_ = self.__load()
        return obj_ <= other

    def __lt__(self, other) -> Any:
        obj_ = self.__load()
        return obj_ < other

    def __ne__(self, other) -> Any:
        obj_ = self.__load()
        return obj_ != other

    def __eq__(self, other) -> Any:
        obj_ = self.__load()
        return obj_ == other

    def __gt__(self, other) -> Any:
        obj_ = self.__load()
        return obj_ > other

    def __ge__(self, other) -> Any:
        obj_ = self.__load()
        return obj_ >= other

    def __str__(self):
        obj_ = self.__load()
        return "%s" % obj_

    def resolve_expression(self, *args, **kwargs) -> Any:
        return getattr(self, self._field.name())


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

    show_debug = None

    def __init__(self, cursor, stabla) -> None:
        super().__init__()
        self.parent_cursor = cursor
        # self.parent_cursor.setActivatedBufferChanged(False)
        # self.parent_cursor.setActivatedBufferCommited(False)

        self.show_debug = False

        # if stabla is not None:
        #     from pineboolib.application import project
        #
        #     module_name = project.conn.managerModules().idModuleOfFile("%s.mtd" % stabla)
        #     model_file = "models.%s.%s" % (module_name, stabla)
        #     if os.path.exists(model_file):
        #         (
        #             self._model,
        #             self._buffer_changed,
        #             self._before_commit,
        #             self._after_commit,
        #             self._buffer_commited,
        #             self._inicia_valores_cursor,
        #             self._buffer_changed_label,
        #             self._validate_cursor,
        #             self._validate_transaction,
        #             self._cursor_accepted,
        #         ) = self.obtener_modelo(stabla)
        #         self._stabla = self._model._meta.db_table

    def buffer_changed_signal(self, scampo) -> Any:
        if self._buffer_changed is None:
            return True

        return self._buffer_changed(scampo, self.parent_cursor)

    def buffer_commited_signal(self) -> Any:
        if not self._activatedBufferCommited:
            return True

        if self._buffer_commited is None:
            return True

        try:
            return self._buffer_commited(self.parent_cursor)
        except Exception as exc:
            print("Error inesperado", exc)

    def before_commit_signal(self) -> Any:
        if not self._activatedCommitActions:
            return True

        if self._before_commit is None:
            return True

        return self._before_commit(self.parent_cursor)

    def after_commit_signal(self) -> Any:
        if not self._activatedCommitActions:
            return True

        if self._after_commit is None:
            return True

        return self._after_commit(self.parent_cursor)

    def inicia_valores_cursor_signal(self) -> Any:
        if self._inicia_valores_cursor is None:
            return True

        return self._inicia_valores_cursor(self.parent_cursor)

    def buffer_changed_label_signal(self, scampo) -> Any:
        if self._buffer_changed_label is None:
            return {}

        import inspect

        expected_args = inspect.getargspec(self._buffer_changed_label)[0]
        if len(expected_args) == 3:
            return self._buffer_changed_label(self._model, scampo, self.parent_cursor)
        else:
            return self._buffer_changed_label(scampo, self.parent_cursor)

    def validate_cursor_signal(self) -> Any:
        if self._validate_cursor is None:
            return True

        return self._validate_cursor(self.parent_cursor)

    def validate_transaction_signal(self) -> Any:
        if self._validate_transaction is None:
            return True

        return self._validate_transaction(self.parent_cursor)

    def cursor_accepted_signal(self) -> Any:
        if self._cursor_accepted is None:
            return True

        return self._cursor_accepted(self.parent_cursor)

    # def obtener_modelo(self, stabla):
    #     # logger.warning("****** obtener_modelo %s", stabla, stack_info = True)
    #     from YBLEGACY.FLAux import FLAux
    #
    #     return FLAux.obtener_modelo(stabla)

    def assoc_model(self, module_name=None) -> None:
        from pineboolib.application import project

        cursor = self.parent_cursor
        # mtd = cursor.metadata()
        if module_name is None:
            module_name = cursor.curName()
        model = meta_model(project.DGI.load_meta_model(module_name), cursor)
        if model:
            cursor._meta_model = model
            # setattr(cursor.meta_model(), "_cursor", cursor)

            # Creamos las propiedades , una por carda campo
            # fields_list = mtd.fieldList()

            # for field in fields_list:
            # print("Seteando", field.name())
            #    setattr(model, field.name(), DelayedObjectProxyLoader(cursor, field_object=field))


class meta_model(object):

    _model = None
    _cursor = None
    cursor_tree_dict = {}

    def __init__(self, model, cursor) -> None:
        self._model = model
        self._cursor = cursor
        self.cursor_tree_dict = {}

    def __getattr__(self, name: str) -> Any:
        from pineboolib.fllegacy.flsqlcursor import FLSqlCursor

        # print("Buscando", name)
        ret = None
        if name == "pk":
            name = self._cursor.primaryKey()

        field = self._cursor.metadata().field(name)
        if field is not None:
            field_relation = field.relationM1()
            # value = self._cursor.valueBuffer(field.name())

            if isinstance(field_relation, PNRelationMetaData):
                relation_table_name = field_relation.foreignTable()
                relation_field_name = field_relation.foreignField()

                key_ = "%s_%s" % (relation_table_name, relation_field_name)

                if key_ not in self.cursor_tree_dict.keys():
                    # rel_mtd = aqApp.db().manager().metadata(relation_table_name)

                    relation_mtd = PNRelationMetaData(
                        relation_table_name, field_relation.field(), PNRelationMetaData.RELATION_1M, False, False, True
                    )
                    relation_mtd.setField(relation_field_name)

                    if relation_table_name and relation_field_name:
                        self.cursor_tree_dict[key_] = FLSqlCursor(
                            relation_table_name, True, self._cursor.conn(), self._cursor, relation_mtd
                        )

                rel_cursor = self.cursor_tree_dict[key_]
                rel_cursor.select()

                ret = rel_cursor.meta_model()

            else:
                ret = self._cursor.valueBuffer(field.name())

        else:
            if self._model is not None:
                ret = getattr(self._model, name, None)

                # if ret is None:
                #    logger.warning("No se encuentra %s en el model (%s) del cursor %s" , name, self._model, self._cursor.curName())

        # print("-->", ret, type(ret))
        return ret
