from typing import List, Any, Generator


class ICursor:
    """Database internal cursor. Follows Python DBAPI for cursors. Do not confuse with FLSqlCuror"""

    description: List
    closed: bool
    connection: Any
    arraysize: int
    itersize: int
    rowcount: int
    rownumber: int
    index: int
    lastrowid: int
    query: str
    statusmessage: str

    def close(self) -> None:
        pass

    def execute(self, query, vars=None) -> None:
        pass

    def executemany(self, query, vars_list) -> None:
        pass

    def callproc(self, procname, *parameters) -> Any:
        pass

    def setinputsizes(self, sizes) -> None:
        pass

    def fetch(self) -> List[List[Any]]:
        return []

    def __iter__(self) -> Generator[List[Any], None, None]:
        yield []

    def fetchone(self) -> List[Any]:
        return []

    def fetchall(self) -> List[Any]:
        return []

    def scroll(value, mode="relative") -> Any:
        pass

    def nextset(self) -> Any:
        pass

    def setoutputsize(size, column=None) -> Any:
        pass
