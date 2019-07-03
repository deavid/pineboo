import logging

logger = logging.getLogger(__name__)


class sql_inspector(object):

    _table_names = None
    _field_names = None
    _mtd_fields = None
    _sql_list = None
    _invalid_tables = None
    _invalid_fields = None
    _posible_float = None
    _sql = None

    def __init__(self, sql_text):

        self._mtd_fields = {}
        self._posible_float = False
        self._sql = sql_text
        if sql_text.startswith("show"):
            return
        else:
            self._resolve_fields(sql_text)

            # self.table_names()
            # self.field_names()

    def mtd_fields(self):
        return self._mtd_fields

    def table_names(self):
        return self._table_names

    def field_names(self):
        return self._field_names

    def fieldNameToPos(self, name):

        if name in self._field_names:
            return self._field_names.index(name)
        else:
            raise Exception(
                "No se encuentra el campo %s el la query (%s)"
                % (name, self._table_names)
            )

    def field_type_from_position(self, position):
        pass

    def _resolve_fields(self, sql):
        list_sql = sql.split(" ")

        if list_sql[0] == "select":
            index_from = list_sql.index("from")
            fl = list_sql[1:index_from][0]
            if "where" in list_sql:
                index_where = list_sql.index("where")
                tl = list_sql[index_from + 1 : index_where]
            else:
                tl = list_sql[index_from + 1 :]

            fl = fl.replace(" ", "")
            fl = fl.split(",")

            tablas = []
            alias = {}
            jump = 0
            next_is_alias = None
            prev_ = ""
            last_was_table = False
            for t in tl:
                if jump > 0:
                    jump -= 1
                    prev_ = t
                    last_was_table = False
                    continue

                # if next_is_alias:
                #    alias[t] = next_is_alias
                #    next_is_alias = None
                #    prev_ = t
                #    continue

                # elif t in ("inner", "on"):
                #    print("Comprobando")
                #    if prev_ not in tablas:
                #        alias[prev_] = tablas[:-1]

                elif t == "on":
                    jump = 3
                    prev_ = t
                    last_was_table = False

                elif t in ("left", "join", "right"):
                    prev_ = t
                    last_was_table = False
                    continue

                # elif t == "on":
                # jump = 3
                #    prev_ = t
                #    continue
                # elif t == "as":
                #    next_is_alias = True
                #    continue
                else:
                    if last_was_table:
                        alias[t] = prev_
                        last_was_table = False
                    else:
                        tablas.append(t)
                        last_was_table = True
                    prev_ = t

            temp_tl = []
            for t in tablas:
                temp_tl = temp_tl + t.split(",")

            tablas = temp_tl

            fl_finish = []
            for f in fl:
                field_name = f
                if field_name.find(".") > -1:
                    a_ = field_name[0 : field_name.find(".")]
                    f_ = field_name[field_name.find(".") + 1 :]
                    if a_.find("(") > -1:
                        a = a_[a_.find("(") + 1 :]
                    else:
                        a = a_

                    if a in alias.keys():
                        field_name = "%s.%s" % (a_.replace(a, alias[a]), f_)

                fl_finish.append(field_name)

            self._create_mtd_fields(fl_finish, tablas)

            if not self.mtd_fields():
                if len(fl_finish):
                    self._posible_float = True
                else:
                    logger.warn(
                        "La consulta % no se ha procesado correctamente. Campos: %s, Alias: %s, Tablas: %s",
                        sql,
                        fl_finish,
                        alias,
                        tablas,
                    )

    def resolve_empty_value(self, pos):
        if not self.mtd_fields():
            return None

        mtd = self._mtd_fields[self.field_names()[pos]]

        type_ = mtd.type()
        ret_ = None
        if type_ in ("double", "int", "uint", "serial"):
            ret_ = 0
        elif type_ in ("string", "stringlist", "pixmap"):
            ret_ = ""
        elif type_ in ("unlock", "bool"):
            ret_ = False
        elif type_ == "date":
            from pineboolib.application import types

            ret_ = types.Date()
        elif type_ == "time":
            ret_ = "00:00:00"
        elif type_ == "bytearray":
            ret_ = bytearray()

        return ret_

    def resolve_value(self, pos, value, raw=False):

        if not self.mtd_fields():
            if self._posible_float:
                return float(value)
            else:
                return value

        mtd = self._mtd_fields[self.field_names()[pos]]
        type_ = mtd.type()

        ret_ = value
        if type_ in ("string", "stringlist"):
            pass
        elif type_ == "double":
            ret_ = float(ret_)
        elif type_ in ("int", "uint", "serial"):
            ret_ = int(ret_)
        elif type_ == "pixmap":
            from pineboolib import project

            if raw or not project.conn.manager().isSystemTable(mtd.metadata().name()):
                ret_ = project.conn.manager().fetchLargeValue(ret_)
        elif type_ == "date":
            from pineboolib.application import types

            ret_ = types.Date(str(ret_))
        elif type_ == "time":
            ret_ = str(ret_)[:8]
        elif type_ in ("unlock", "bool"):
            pass
        else:
            ret_ = float(ret_)
            print("TIPO DESCONOCIDO", type_, ret_)

        return ret_

    def _create_mtd_fields(self, fields_list, tables_list):
        from pineboolib import project

        _filter = ["sum(", "max(", "distint("]

        self._mtd_fields = {}
        self._invalid_tables = []
        self._table_names = list(tables_list)
        self._field_names = []

        for field_name_org in list(fields_list):
            self._field_names.append(field_name_org)
            field_name = field_name_org
            for table_name in list(tables_list):
                mtd_table = project.conn.manager().metadata(table_name)
                if mtd_table is not None:
                    for fil in _filter:
                        if field_name.startswith(fil):
                            field_name = field_name.replace(fil, "")
                            field_name = field_name[:-1]

                    if field_name.find(".") > -1:
                        if table_name != field_name[0 : field_name.find(".")]:
                            continue
                        else:
                            field_name = field_name[field_name.find(".") + 1 :]
                    mtd_field = mtd_table.field(field_name)
                    if mtd_field is not None:
                        self._mtd_fields[field_name_org] = mtd_field
                    # fields_list.remove(field_name_org)
            else:
                if table_name not in self._invalid_tables:
                    self._invalid_tables.append(table_name)
                    # tables_list.remove(table_name)
