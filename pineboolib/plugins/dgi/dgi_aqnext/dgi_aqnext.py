# # -*- coding: utf-8 -*-
import collections
import traceback
import inspect
import os
from typing import List, Dict, Any, Union
from PyQt5 import QtCore  # type: ignore

from pineboolib.core.utils import logging
from pineboolib.plugins.dgi.dgi_schema import dgi_schema
from pineboolib.application.utils import sql_tools
from pineboolib.application import project

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
        self._use_authentication = False  # True La autenticación la realiza pineboolib
        self.showInitBanner()
        self._show_object_not_found_warnings = False
        self.qApp = QtCore.QCoreApplication
        self._alternative_content_cached = False

    def extraProjectInit(self):
        pass

    def setParameter(self, param):
        self._listenSocket = param

    def mainForm(self):
        if not self._mainForm:
            self._mainForm = mainForm()  # FIXME
        return self._mainForm

    def __getattr__(self, name):
        return super().resolveObject(self._name, name)

    def exec_(self):
        from pineboolib.fllegacy.systype import SysType

        qsa_sys = SysType()
        logger.warning("DGI_%s se ha inicializado correctamente" % self._alias)
        if project.conn:
            logger.warning("Driver  DB: %s", project.conn.driverAlias())
            logger.warning("Usuario DB: %s", qsa_sys.nameUser())
            logger.warning("Nombre  DB: %s", qsa_sys.nameBD())

    def processEvents(self):
        return QtCore.QCoreApplication.processEvents()

    def interactiveGUI(self):
        return "Django"

    def authenticate(self, **kwargs):
        # user = kwargs["username"]  # FIXME
        # password = kwargs["password"]
        pass

    def use_authentication(self):
        return self._use_authentication

    def use_model(self):
        return True

    def alternative_content_cached(self):
        return True

    def content_cached(self, tmp_folder, db_name, module_id, file_ext, file_name, sha_key):
        from pineboolib.core.utils.utils_base import filedir

        data_ = None
        if module_id == "sys" and file_name in self.sys_mtds():
            path_ = filedir("./plugins/dgi/dgi_aqnext/system_files/%s/%s.%s" % (file_ext, file_name, file_ext))
            if os.path.exists(path_) and project.conn:
                data_ = project.conn.managerModules().contentFS(path_, False)

        return data_

    def use_alternative_credentials(self):
        return True

    def get_nameuser(self):
        return ""
        # FIXME
        # from YBUTILS.viewREST.cacheController import getUser
        # return str(getUser())

    def sys_mtds(self):
        return ["sis_acl", "sis_user_notifications", "sis_gridfilter"]

    # def interactiveGUI(self):
    # return "Django"

    def __content_cached__old__(self, tmp_dir, db_name, module_id, ext_, name_, sha_key):
        data = None
        utf8_ = False
        if not project.conn:
            raise Exception
        if ext_ == "qs":
            from django.conf import settings  # type: ignore

            folder_ = settings.PROJECT_ROOT
            legacy_path = "%s/legacy/%s/%s.py" % (folder_, module_id, name_)
            print("**** Buscando en path", legacy_path)
            if os.path.exists(legacy_path):
                data = project.conn.managerModules().contentFS(legacy_path, True)
        else:
            if os.path.exists("%s/cache/%s/%s/file.%s/%s" % (tmp_dir, db_name, module_id, ext_, name_)):
                if ext_ == "kut":
                    utf8_ = True
                data = project.conn.managerModules().contentFS(
                    "%s/cache/%s/%s/file.%s/%s/%s.%s" % (tmp_dir, db_name, module_id, ext_, name_, sha_key, ext_), utf8_
                )

        return data

    def alternative_script_path(self, script_name, app=None):
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
        from pineboolib.application.xmlaction import XMLAction
        from pineboolib.application.proxy import DelayedObjectProxyLoader

        action = XMLAction(project=project)
        action.name = module_name
        action.alias = module_name
        action.form = None
        action.table = None
        action.scriptform = module_name

        # Carganmos módulo
        if module_name == script_name:
            # Estamos aquí porque script_name existe en model. Hay que ver si existe el legacy
            if hasattr(qsa_dict_modules, action.name):
                # Lo convertimos en legacy
                legacy = getattr(qsa_dict_modules, action.name)
                setattr(qsa_dict_modules, "%s_legacy" % action.name, legacy)
                delattr(qsa_dict_modules, action.name)  # Borramos el script del arbol

            # Se crea el script
            setattr(qsa_dict_modules, action.name, DelayedObjectProxyLoader(action.load, name="QSA.Module.%s" % app))
            project.actions[action.name] = action
            if prefix == "":
                return

        action_xml = XMLAction(project=project)
        action_xml.name = module_name

        if "%s_legacy" in action_xml.name not in project.actions.keys():
            if action_xml.name in project.actions.keys():
                project.actions["%s_legacy" % action_xml.name] = project.actions[action_xml.name]
                del project.actions[action_xml.name]

        if prefix == "form":
            if hasattr(qsa_dict_modules, "form" + action_xml.name):
                # Cambiamos a legacy el script existente
                legacy = getattr(qsa_dict_modules, action_xml.name)
                setattr(qsa_dict_modules, "form%s_legacy" % action_xml.name, legacy)
                delattr(qsa_dict_modules, action_xml.name)

            action_xml.table = action_xml.name
            action_xml.scriptform = script_name
            project.actions[action_xml.name] = action_xml
            delayed_action = DelayedObjectProxyLoader(action_xml.load, name="QSA.Module.%s.Action.form%s" % (app, action_xml.name))
            # print("Creando", "form" + module_name)
            setattr(qsa_dict_modules, "form" + action_xml.name, delayed_action)

        if prefix == "formRecord":
            if hasattr(qsa_dict_modules, "formRecord" + action_xml.name):
                # Cambiamos a legacy el script existente
                legacy = getattr(qsa_dict_modules, action_xml.name)
                setattr(qsa_dict_modules, "formRecord%s_legacy" % action_xml.name, legacy)
                delattr(qsa_dict_modules, action_xml.name)

            action_xml.table = action_xml.name
            action_xml.scriptformrecord = script_name
            project.actions[action_xml.name] = action_xml
            delayed_action = DelayedObjectProxyLoader(
                action_xml.formRecordWidget, name="QSA.Module.%s.Action.formRecord%s" % (app, action_xml.name)
            )
            setattr(qsa_dict_modules, "formRecord" + action_xml.name, delayed_action)
            # print("Creando **** ", getattr(qsa_dict_modules, "formRecord" + module_name))

    def load_meta_model(self, action_name, opt=None):
        import importlib

        module_name = project.conn.managerModules().idModuleOfFile("%s.mtd" % action_name)
        module = None
        ret_ = None
        model_file = "models.%s.%s" % (module_name, action_name)
        if module_name is not None:
            try:
                module = importlib.import_module(model_file)
            except ImportError:
                logger.warning("DGI: load_meta_model. No se encuentra el model de %s", action_name)
                module = None
                ret_ = None

        if module is not None:
            ret_ = getattr(module, action_name, None)

        return ret_

    def get_master_cursor(self, prefix, template="master"):
        from pineboolib import qsa as qsa_tree

        module_name = prefix

        # logger.warning("Cargando el prefix_master de %s", prefix)

        # if template == "master":
        #    module_name = "form%s" % prefix
        # elif template == "formRecord":
        #    module_name = "formRecord%s" % prefix
        if template in ["master", "formRecord", "newRecord"]:
            module_name = "form%s" % prefix

        cursor = None
        module = getattr(qsa_tree, module_name, None)
        if module is not None:
            cursor = module.widget.cursor()
        else:
            logger.warning("*** DGI.get_master_cursor creando cursor %s sin action asociada ***", prefix)
            from pineboolib.fllegacy.flsqlcursor import FLSqlCursor

            cursor = FLSqlCursor(prefix)

        if cursor is None:
            logger.warning("*** DGI.get_master_cursor no encuentra cursor de %s***", prefix)

        if cursor and not cursor.meta_model():
            # print("**************************", prefix)
            try:
                cursor.assoc_model()  # Asocia el modelo
            except Exception:
                logger.warning("DGI. get_master_cursor: %s", traceback.format_exc())

        # if template == "newRecord":
        #    cursor.setModeAccess(cursor.Insert)
        #    cursor.refreshBuffer()

        return cursor

    def init_cursor(self, cursor, params, template):
        from pineboolib import qsa as qsa_tree

        prefix = cursor.curName()

        if template in ["formRecord", "newRecord"]:
            module_name = "form%s" % prefix

        self.populate_with_params(cursor, params)

        module = getattr(qsa_tree, module_name, None)

        if template == "newRecord":
            if cursor.meta_model():
                fun_mod = getattr(cursor.meta_model(), "iniciaValoresCursor", None)
                if fun_mod is not None:
                    # print("Inicializando cursor model", prefix)
                    fun_mod(cursor)

            fun_qsa = getattr(module.widget, "iniciaValoresCursor", None)
            if fun_qsa is not None:
                # print("Inicializando cursor qsa", prefix)
                fun_qsa(cursor)

    def populate_with_params(self, cursor, params):
        for k in params.keys():
            if k.startswith("p_"):
                cursor.setValueBuffer(k[2:], params[k])
            else:
                print("FIXME:: populate_with_params", k, params[k])

    def cursor2json(self, cursor, template=None):
        ret_: List[Dict[str, Any]] = []
        if not cursor.modeAccess() == cursor.Insert:
            if not cursor.isValid():
                logger.warning("Cursor inválido/vacío en %s", cursor.curName())
                return ret_

            if cursor.first():
                pass

        meta_model = cursor.meta_model()

        # project.init_time()
        size_ = cursor.size()
        pk = cursor.primaryKey()
        fields_list = cursor.metadata().fieldList()
        i = 0
        # date_fields = []

        if cursor.modeAccess() == cursor.Insert:
            size_ = 1
        # logger.warning("***** %s", size_, stack_info = True)
        while i < size_:
            # dict_ = collections.OrderedDict()
            dict_ = {}

            for f in fields_list:
                field_name = f.name() if f.name() != "pk" else pk
                value = cursor.valueBuffer(field_name)
                if f.type() in ["date"]:
                    if hasattr(value, "toString"):
                        value = value.toString()
                    value = value[:10]

                if f.isPrimaryKey():
                    dict_["pk"] = value
                dict_[f.name()] = value

            if meta_model:
                calculateFields = self.get_foreign_fields(meta_model, template)
                for field in calculateFields:
                    if hasattr(meta_model, field["func"]):
                        dict_[field["verbose_name"]] = str(getattr(meta_model, field["func"])(meta_model))

                desc_function = getattr(meta_model, "getDesc", None)
                desc = None
                if desc_function:
                    expected_args = inspect.getargspec(desc_function)[0]
                    new_args = [meta_model]
                    desc = desc_function(*new_args[: len(expected_args)])
                dict_["desc"] = desc
            # for field in calculateFields:
            #     serializer._declared_fields.update(
            #         {field["verbose_name"]: serializers.serializers.ReadOnlyField(label=field["verbose_name"], source=field["func"])}
            #     )

            if cursor.next():
                pass
            i += 1

        # project.show_time("Fin cursor2json %s %s %s" % (cursor.curName(), meta_model, cursor.filter()))
        if len(ret_) == 1:
            # FIXME: Avoid changing the type "automagically", as the caller can get confused.
            return ret_[0]
        else:
            return ret_

    def getYBschema(self, cursor, template=None):
        """Permite obtener definicion de schema de uso interno de YEBOYEBO"""

        mtd = cursor.metadata()

        meta_model = cursor.meta_model()

        dict: Dict = collections.OrderedDict()
        meta: Dict = collections.OrderedDict()

        if mtd is None:
            return dict, meta

        meta["verbose_name"] = mtd.alias()

        dict["desc"] = collections.OrderedDict()
        dict["desc"]["verbose_name"] = "Desc"
        dict["desc"]["help_text"] = None
        dict["desc"]["locked"] = True
        dict["desc"]["field"] = False
        dict["desc"]["visible"] = True
        dict["desc"]["tipo"] = 3
        dict["desc"]["visiblegrid"] = False
        fields_list = mtd.fieldNames()

        fields_list.append("pk")

        for key in fields_list:
            field = mtd.field(key if key != "pk" else mtd.primaryKey())
            if field is None:
                continue
            dict[key] = collections.OrderedDict()
            dict[key]["verbose_name"] = field.alias() if key != "pk" else "Pk"
            """ FIXME: help_text """
            dict[key]["help_text"] = None
            dict[key]["locked"] = True if field.name() == mtd.primaryKey() else False  # FIXME: hay que ver el criterio de locked
            dict[key]["field"] = False

            dict[key]["visible"] = False if key in ["pk", "desc"] else True
            dict[key]["tipo"] = sql_tools.get_tipo_aqnext(field.type())
            if field.type() == "stringlist":
                dict[key]["subtipo"] = 6

            dict[key]["visiblegrid"] = field.visibleGrid()
            if not field.allowNull():
                dict[key]["required"] = True
            if field.type() == "double":
                dict[key]["max_digits"] = field.partInteger()
                dict[key]["decimal_places"] = field.partDecimal()
            if field.hasOptionsList():
                dict[key]["optionslist"] = field.optionsList()
                dict[key]["tipo"] = 5

            # dict[key]['desc'] = cursor.primaryKey()
            relation = field.relationM1()
            if relation is not None:
                table_name = relation.foreignTable()  # Tabla relacionada
                dict[key]["rel"] = table_name
                dict[key]["to_field"] = relation.foreignField()  # Campo relacionado
                desc = None
                # print("Cursor relacionado", table_name)
                # cursor_rel = FLSqlCursor(table_name)

                rel_meta_model = getattr(meta_model, relation.field())
                desc_function = getattr(rel_meta_model, "getDesc", None)
                if desc_function:
                    expected_args = inspect.getargspec(desc_function)[0]
                    new_args = [rel_meta_model]
                    desc = desc_function(*new_args[: len(expected_args)])

                if not desc or desc is None:
                    desc = cursor.db().manager().metadata(table_name).primaryKey()

                dict[key]["desc"] = desc

        if meta_model:
            calculateFields = self.get_foreign_fields(meta_model, template)
            for field in calculateFields:
                dict[field["verbose_name"]] = collections.OrderedDict()
                dict[field["verbose_name"]]["verbose_name"] = field["verbose_name"]
                dict[field["verbose_name"]]["help_text"] = None
                dict[field["verbose_name"]]["locked"] = True
                dict[field["verbose_name"]]["field"] = False
                dict[field["verbose_name"]]["visible"] = True
                dict[field["verbose_name"]]["tipo"] = 3

        return dict, meta

    def get_foreign_fields(self, meta_model, template=None):
        foreign_field_function = getattr(meta_model, "getForeignFields")
        expected_args = inspect.getargspec(foreign_field_function)[0]
        new_args = [meta_model, template]
        return foreign_field_function(*new_args[: len(expected_args)])

    def pagination(self, data_, query):
        return pagination_class(data_, query)  # FIXME

    def get_queryset(self, prefix, params):

        # retorna una lista con objetos del modelo
        cursor_master = self.get_master_cursor(prefix)
        list_objects = []
        where, order_by = sql_tools.resolve_query(prefix, params)
        where_filter = "%s ORDER BY %s" % (where, order_by) if len(order_by) else where

        first_reg, limit_reg = sql_tools.resolve_pagination(params)
        if first_reg:
            where_filter += " OFFSET %s" % first_reg

        if limit_reg:
            where_filter += " LIMIT %s" % limit_reg

        cursor_master.select(where_filter)
        if cursor_master.first():
            while True:
                list_objects.append(cursor_master.meta_model()())

                if not cursor_master.next():
                    break

        return list_objects

    """
    @decorators.NotImplementedWarn
    def paginate_queryset(self, query_set):

        return query_set
    """

    def get_paginated_response(self, data, params, size=None):

        response = paginated_object()
        response.data = {}
        data_list = self._convert_to_ordered_dict(data)
        response.data["data"] = data_list

        # pagination = pagination_class(data_list, params)
        first_reg, limit_reg = sql_tools.resolve_pagination(params)

        response.data["PAG"] = {
            "NO": "%s" % (int(limit_reg) + int(first_reg)) if first_reg else 0,
            "PO": "%s" % (int(first_reg) - int(limit_reg)) if first_reg else 0,
            "COUNT": len(data) if size is None else size,
        }

        return response

    def carga_datos_custom_filter(self, table, usuario):
        from pineboolib.fllegacy.flsqlcursor import FLSqlCursor

        ret: Dict[str, Dict[str, Any]] = {}
        cursor = FLSqlCursor("sis_gridfilter")
        cursor.select(" prefix ='%s' AND usuario ='%s'" % (table, usuario))
        if cursor.first():
            ret[cursor.valueBuffer("descripcion")] = {}
            ret[cursor.valueBuffer("descripcion")]["pk"] = cursor.valueBuffer("id")
            ret[cursor.valueBuffer("descripcion")]["filtro"] = cursor.valueBuffer("filtro").replace('"', "'")
            ret[cursor.valueBuffer("descripcion")]["default"] = cursor.valueBuffer("inicial")
        return ret

    def _convert_to_ordered_dict(self, data: Union[List[Dict[str, Any]], Dict[str, Any]]):
        ret_ = []

        if isinstance(data, list):
            for t in data:
                o = {key: t[key] for key in t.keys()}
                ret_.append(o)
        elif isinstance(data, dict):
            o = {key: data[key] for key in data.keys()}
            ret_.append(o)

        return ret_


class paginated_object(object):
    data: Dict


class pagination_class(object):

    count = None
    _limit = None
    _page = None

    def __init__(self, data_, query={}):
        self.count = len(data_)
        self._limit = 50 if "p_l" not in query.keys() or query["p_l"] == "true" else int(query["p_l"])
        self._page = 0 if "p_c" not in query.keys() or query["p_c"] == "true" else int(query["p_c"])

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


class mainForm(object):
    mainWindow = None
    MainForm = None
