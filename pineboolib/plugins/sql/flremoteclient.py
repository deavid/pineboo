import json

# from PyQt5.QtCore import QTime, QDate, QDateTime  # type: ignore
# from PyQt5.Qt import qWarning, QDomDocument, QRegExp  # type: ignore
# from PyQt5.QtWidgets import QMessageBox, QProgressDialog  # type: ignore

from pineboolib.application.utils.check_dependencies import check_dependencies

# from pineboolib.core import decorators
# from pineboolib.fllegacy.flutil import FLUtil
# from pineboolib.fllegacy.flsqlquery import FLSqlQuery
# from pineboolib.fllegacy.flsqlcursor import FLSqlCursor

from pineboolib import logging
from typing import Any, Callable, Dict, List, Union, Optional


logger = logging.getLogger(__name__)


def base_create_dict(
    method: str, fun: str, id: int, arguments: List[Any] = []
) -> Dict[str, Union[str, int, List[Any], Dict[str, Any]]]:
    data = [{"function": fun, "arguments": arguments, "id": id}]
    return {"method": method, "params": data, "jsonrpc": "2.0", "id": id}


class FLREMOTECLIENT(object):

    version_: str
    conn_ = None
    name_: str
    alias_: str
    errorList: List[str]
    lastError_: str
    db_ = None
    mobile_: bool
    pure_python_: bool
    defaultPort_: int

    def __init__(self) -> None:
        self.version_ = "0.6"
        self.conn_ = None
        self.name_ = "REMOTECLIENT"
        self.open_ = False
        self.errorList = []
        self.alias_ = "Pineboo Server"
        self._dbname = None
        self.mobile_ = False
        self.pure_python_ = False
        self.defaultPort_ = 4000
        self.id_ = 0
        self.url: Optional[str] = None
        check_dependencies({"requests": "requests"}, False)

    def useThreads(self) -> bool:
        return False

    def useTimer(self) -> bool:
        return True

    def desktopFile(self) -> bool:
        return False

    def version(self) -> str:
        return self.version_

    def driverName(self) -> str:
        return self.name_

    def isOpen(self) -> bool:
        return self.open_

    def pure_python(self) -> bool:
        return self.pure_python_

    def safe_load(self) -> bool:
        return True

    def mobile(self) -> bool:
        return self.mobile_

    def DBName(self) -> Any:
        return self._dbname

    def create_dict(self, fun, data: Any = []) -> Dict[str, Any]:
        fun = "%s__%s" % (self.id_, fun)
        return base_create_dict("dbdata", fun, self.id_, data)

    def send_to_server(self, js) -> Any:
        import requests

        headers = {"content-type": "application/json"}
        if self.url is None:
            raise Exception("send_to_server. self.url is None")
        req = requests.post(self.url, data=json.dumps(js), headers=headers).json()
        res_ = req["result"] if "result" in req.keys() else None
        # if res_ is None:
        #    print("FAIL %s --> %s\n%s" % (js, self.url, req))

        if res_ == "Desconocido":
            print("%s -> %s\nresult: %s" % (js, self.url, res_))
        return res_

    def connect(self, db_name, db_host, db_port, db_user_name, db_password) -> Any:
        self._dbname = db_name
        self.id_ = db_user_name
        self.url = "http://%s:%s/jsonrpc" % (db_host, db_port)
        dict_ = self.create_dict("hello")
        try:
            ret = self.send_to_server(dict_)
        except Exception as exc:
            print(exc)
            return False

        server_found = False

        if ret[0:7] == "Welcome":
            server_found = True

        if server_found:
            self.conn_ = conn_class(db_name, self)

            if not self.conn_.is_valid():
                return False

        return self.conn_

    def existsTable(self, name) -> bool:  # Siempre True
        return True

    def mismatchedTable(self, *args) -> bool:
        return False

    def __getattr__(self, name) -> Callable:
        return virtual_function(name, self).virtual

    def refreshQuery(self, curname, fields, table, where, cursor, conn) -> None:
        self.send_to_server(
            self.create_dict(
                "refreshQuery",
                {
                    "cursor_id": cursor.id_,
                    "curname": "%s_%s" % (self.id_, curname),
                    "fields": fields,
                    "table": table,
                    "where": where,
                },
            )
        )

    def refreshFetch(
        self, number, curname, table, cursor, fields, where_filter
    ) -> None:
        self.send_to_server(
            self.create_dict(
                "refreshFetch",
                {
                    "cursor_id": cursor.id_,
                    "curname": "%s_%s" % (self.id_, curname),
                    "fields": fields,
                    "table": table,
                    "where_filter": where_filter,
                    "number": number,
                },
            )
        )

    def fetchAll(self, cursor, tablename, where_filter, fields, curname) -> Any:
        return self.send_to_server(
            self.create_dict(
                "fetchAll",
                {
                    "cursor_id": cursor.id_,
                    "tablename": tablename,
                    "where_filter": where_filter,
                    "fields": fields,
                    "curname": "%s_%s" % (self.id_, curname),
                },
            )
        )


class cursor_class(object):
    driver_: FLREMOTECLIENT
    id_ = None
    data_ = None
    current_ = None
    last_sql = None

    def __init__(self, driver, n) -> None:
        self.driver_ = driver
        self.id_ = n
        self.current_ = None
        self.last_sql = None
        self.description = None

    def __getattr__(self, name) -> None:
        logger.info("cursor_class: cursor(%s).%s !!", self.id_, name)
        logger.trace("Detalle:", stack_info=True)

    def execute(self, sql) -> None:
        self.last_sql = sql
        self.data_ = self.driver_.send_to_server(
            self.driver_.create_dict("execute", {"cursor_id": self.id_, "sql": sql})
        )
        self.current_ = 0

    def close(self) -> None:
        self.driver_.send_to_server(
            self.driver_.create_dict("close", {"cursor_id": self.id_})
        )

    def fetchone(self) -> Any:
        ret_ = self.driver_.send_to_server(
            self.driver_.create_dict("fetchone", {"cursor_id": self.id_})
        )
        # print(self.id_, "**", self.last_sql, ret_)
        return ret_

    def fetchall(self) -> Any:
        ret_ = self.driver_.send_to_server(
            self.driver_.create_dict("fetchall", {"cursor_id": self.id_})
        )
        # print(self.id_, "**", self.last_sql, ret_)
        return ret_

    def __iter__(self) -> "cursor_class":
        return self

    def __next__(self) -> Any:
        ret = self.driver_.send_to_server(
            self.driver_.create_dict("fetchone", {"cursor_id": self.id_})
        )
        if ret is None:
            raise StopIteration
        return ret


class conn_class(object):

    db_name_ = None
    driver_: FLREMOTECLIENT
    list_cursor: List[cursor_class]

    def __init__(self, db_name, driver) -> None:
        self.db_name_ = db_name
        self.driver_ = driver
        self.list_cursor = []

    def is_valid(self) -> Any:
        db_name_server = self.driver_.send_to_server(
            self.driver_.create_dict("db_name")
        )
        return self.db_name_ == db_name_server

    def cursor(self) -> cursor_class:
        cur = cursor_class(self.driver_, len(self.list_cursor))
        self.list_cursor.append(cur)
        return cur


class virtual_function(object):
    name_: str
    driver_: FLREMOTECLIENT

    def __init__(self, name: str, driver: FLREMOTECLIENT) -> None:
        self.name_ = name
        self.driver_ = driver

    def virtual(self, *args) -> Any:
        # return self.driver_.send_to_server(self.driver_.create_dict("%s_%s" % (self.driver_.conn_.user_name_, self.name_), args))
        return self.driver_.send_to_server(self.driver_.create_dict(self.name_, args))
