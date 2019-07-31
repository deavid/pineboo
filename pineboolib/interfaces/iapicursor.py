"""
IApiCursor module.
"""
from typing import List, Any, Generator


class IApiCursor:
    """Database internal cursor. Follows Python DBAPI for cursors. Do not confuse with FLSqlCuror."""

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
        """Close cursor."""
        pass

    def execute(self, query, vars=None) -> None:
        """Excecute SQL."""
        pass

    def executemany(self, query, vars_list) -> None:
        """Execute a list of SQL."""
        pass

    def callproc(self, procname, *parameters) -> Any:
        """Call a procedure in DB."""
        pass

    def setinputsizes(self, sizes) -> None:
        """Define input sizes."""
        pass

    def fetch(self) -> List[List[Any]]:
        """Fetch records from last execution."""
        return []

    def __iter__(self) -> Generator[List[Any], None, None]:
        """Fetch in iterator fashion."""
        yield []

    def fetchone(self) -> List[Any]:
        """Fetch one record."""
        return []

    def fetchall(self) -> List[Any]:
        """Fetch remaining records."""
        return []

    def scroll(value, mode="relative") -> Any:
        """Scroll cursor down without fetching."""
        pass

    def nextset(self) -> Any:
        """Get next set of records from DB."""
        pass

    def setoutputsize(size, column=None) -> Any:
        """Define output size."""
        pass
