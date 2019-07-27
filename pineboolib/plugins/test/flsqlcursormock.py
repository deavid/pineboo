import traceback
from pineboolib.fllegacy.flsqlcursor import FLSqlCursor


class FLSqlCursorMock:

    maxValue = None

    def __init__(self):
        self.maxValue = 50

    def run(self):
        value = 0
        cursor = FLSqlCursor("paises")

        try:
            cursor.setModeAccess(cursor.Insert)
            cursor.refreshBuffer()
        except Exception:
            print(traceback.format_exc())
        else:
            value = value + 10

        try:
            cursor.setValueBuffer("codpais", "TEST")
            cursor.setValueBuffer("nombre", "test name")
            cursor.setValueBuffer("codiso", "TS")
        except Exception:
            print(traceback.format_exc())
        else:
            value = value + 10

        try:
            cursor.commitBuffer()
        except Exception:
            print(traceback.format_exc())
        else:
            value = value + 10

        try:
            val1 = cursor.valueBuffer("codpais")
        except Exception:
            print(traceback.format_exc())
        else:
            if val1 == "TEST":
                value = value + 10

        try:
            cursor.select("codpais = 'TEST'")
            while cursor.next():
                cursor.setModeAccess(cursor.Del)
                cursor.refreshBuffer()
                cursor.commitBuffer()
        except Exception:
            print(traceback.format_exc())
        else:
            value = value + 10

        return value
