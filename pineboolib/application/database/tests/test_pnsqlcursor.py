"""Test_pnsqlcursor module."""

import unittest
from pineboolib.loader.main import init_testing


class TestInsertData(unittest.TestCase):
    """TestInsertData Class."""

    @classmethod
    def setUpClass(cls) -> None:
        """Ensure pineboo is initialized for testing."""
        init_testing()

    def test_basic(self) -> None:
        """Insert data into a database."""
        from pineboolib.application.database import pnsqlcursor

        cursor = pnsqlcursor.PNSqlCursor("flareas")
        cursor.setModeAccess(cursor.Insert)
        cursor.refreshBuffer()
        cursor.setValueBuffer("boqueo", False)
        cursor.setValueBuffer("idarea", "T")
        cursor.setValueBuffer("descripcion", "Área de prueba T")
        self.assertTrue(cursor.commitBuffer())
        mode_access = cursor.modeAccess()
        self.assertEqual(mode_access, cursor.Edit)


class TestEditData(unittest.TestCase):
    """TestEditData Class."""

    @classmethod
    def setUpClass(cls) -> None:
        """Ensure pineboo is initialized for testing."""
        init_testing()

    def test_basic(self) -> None:
        """Edit data from a database."""
        from pineboolib.application.database import pnsqlcursor

        cursor = pnsqlcursor.PNSqlCursor("flareas")
        cursor.select("idarea ='T'")
        first_result = cursor.first()
        self.assertEqual(first_result, True)
        cursor.setModeAccess(cursor.Edit)
        cursor.refreshBuffer()

        value_idarea = cursor.valueBuffer("idarea")
        self.assertEqual(value_idarea, "T")


class TestDeleteData(unittest.TestCase):
    """TestDeletedata Class."""

    @classmethod
    def setUpClass(cls) -> None:
        """Ensure pineboo is initialized for testing."""
        init_testing()

    def test_basic(self) -> None:
        """Delete data from a database."""
        from pineboolib.application.database import pnsqlcursor

        cursor = pnsqlcursor.PNSqlCursor("flareas")
        cursor.select("idarea ='T'")
        first_result = cursor.first()
        self.assertEqual(first_result, True)
        size_1 = cursor.size()
        self.assertEqual(size_1, 1)
        cursor.setModeAccess(cursor.Del)
        cursor.refreshBuffer()

        value_idarea = cursor.valueBuffer("idarea")
        self.assertEqual(value_idarea, "T")
        cursor.commitBuffer()

        size_2 = cursor.size()
        self.assertEqual(size_2, 0)


class TestMove(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """Ensure pineboo is initialized for testing."""
        init_testing()

    def test_basic(self) -> None:

        from pineboolib.application.database import pnsqlcursor

        cursor = pnsqlcursor.PNSqlCursor("flareas")
        cursor.setModeAccess(cursor.Insert)
        cursor.refreshBuffer()
        cursor.setValueBuffer("bloqueo", False)
        cursor.setValueBuffer("idarea", "A")
        cursor.setValueBuffer("descripcion", "Área de prueba A")
        self.assertTrue(cursor.commitBuffer())
        cursor.setModeAccess(cursor.Insert)
        cursor.refreshBuffer()
        cursor.setValueBuffer("bloqueo", False)
        cursor.setValueBuffer("idarea", "B")
        cursor.setValueBuffer("descripcion", "Área de prueba B")
        self.assertTrue(cursor.commitBuffer())
        cursor.setModeAccess(cursor.Insert)
        cursor.refreshBuffer()
        cursor.setValueBuffer("bloqueo", False)
        cursor.setValueBuffer("idarea", "C")
        cursor.setValueBuffer("descripcion", "Área de prueba C")
        self.assertTrue(cursor.commitBuffer())
        cursor.setModeAccess(cursor.Insert)
        cursor.refreshBuffer()
        cursor.setValueBuffer("bloqueo", False)
        cursor.setValueBuffer("idarea", "D")
        cursor.setValueBuffer("descripcion", "Área de prueba D")
        self.assertTrue(cursor.commitBuffer())
        cursor.setModeAccess(cursor.Insert)
        cursor.refreshBuffer()
        cursor.setValueBuffer("bloqueo", False)
        cursor.setValueBuffer("idarea", "E")
        cursor.setValueBuffer("descripcion", "Área de prueba E")
        self.assertTrue(cursor.commitBuffer())

        cursor.first()
        self.assertEqual(cursor.valueBuffer("idarea"), "A")
        res_1 = cursor.prev()
        self.assertEqual(res_1, False)
        self.assertEqual(cursor.valueBuffer("idarea"), "A")
        res_2 = cursor.last()
        self.assertEqual(res_2, True)
        self.assertEqual(cursor.valueBuffer("idarea"), "E")
        res_3 = cursor.next()
        self.assertEqual(res_3, False)
        self.assertEqual(cursor.valueBuffer("idarea"), "E")
        res_4 = cursor.prev()
        self.assertEqual(res_4, True)
        self.assertEqual(cursor.valueBuffer("idarea"), "D")
        cursor.prev()
        self.assertEqual(cursor.valueBuffer("idarea"), "C")
        res_5 = cursor.first()
        self.assertEqual(res_5, True)
        self.assertEqual(cursor.valueBuffer("idarea"), "A")
        cursor.next()
        self.assertEqual(cursor.valueBuffer("idarea"), "B")
        res_6 = cursor.next()
        self.assertEqual(res_6, True)
        self.assertEqual(cursor.valueBuffer("idarea"), "C")
        self.assertEqual(cursor.size(), 5)


class TestBuffer(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """Ensure pineboo is initialized for testing."""
        init_testing()

    def test_basic(self) -> None:
        """Test buffers data."""
        from pineboolib.application.database import pnsqlcursor

        cursor = pnsqlcursor.PNSqlCursor("flareas")
        self.assertEqual(cursor.size(), 5)
        cursor.select("1=1 ORDER BY idarea ASC")
        cursor.setModeAccess(cursor.Edit)
        self.assertEqual(cursor.size(), 5)
        self.assertEqual(cursor.first(), True)
        cursor.refreshBuffer()
        buffer_copy = cursor.bufferCopy()
        self.assertEqual(cursor.valueBuffer("idarea"), "A")
        self.assertEqual(cursor.buffer().value("idarea"), "A")
        self.assertEqual(buffer_copy.value("idarea"), "A")
        cursor.next()
        self.assertEqual(cursor.buffer().value("idarea"), "B")
        self.assertEqual(buffer_copy.value("idarea"), "A")


class TestValues(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """Ensure pineboo is initialized for testing."""
        init_testing()

    def test_basic(self) -> None:
        """Test values."""
        from pineboolib.application.database import pnsqlcursor
        from pineboolib.application.qsatypes import date
        from PyQt5 import QtCore

        cursor = pnsqlcursor.PNSqlCursor("flupdates")
        cursor.setModeAccess(cursor.Insert)
        cursor.refreshBuffer()
        date = date.Date()
        cursor.setValueBuffer("fecha", date)
        cursor.setValueBuffer("hora", "00:00:01")
        cursor.setValueBuffer("nombre", "nombre de prueba")
        cursor.setValueBuffer("modulesdef", "module_1\nmodule_2\nmodule_3")
        cursor.setValueBuffer("filesdef", "file_1\nfile_2\nfile_3")
        cursor.setValueBuffer("shaglobal", "1234567890")
        cursor.setValueBuffer("auxtxt", "aux_1\naux_2\naux_3")
        self.assertEqual(cursor.commitBuffer(), True)
        self.assertEqual(str(cursor.valueBuffer("fecha"))[0:8], str(date)[0:8])
        self.assertEqual(cursor.valueBuffer("hora"), "00:00:01")
        self.assertEqual(cursor.valueBuffer("nombre"), "nombre de prueba")


if __name__ == "__main__":
    unittest.main()
