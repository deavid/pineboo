"""Test_flfieldDB module."""

import unittest
from pineboolib.loader.main import init_testing


class TestFLFieldDBString(unittest.TestCase):
    """TestFLFieldDBString Class."""

    @classmethod
    def setUpClass(cls) -> None:
        """Ensure pineboo is initialized for testing."""
        init_testing()

    def test_basic(self) -> None:
        """Test string FLFieldDB mode."""

        from pineboolib.qsa import dictmodules
        from pineboolib.application.database import pnsqlcursor

        cursor_1 = pnsqlcursor.PNSqlCursor("flmodules")
        cursor_1.select()
        cursor_1.setModeAccess(cursor_1.Insert)
        cursor_1.refreshBuffer()
        cursor_1.insertRecord(False)

        module_ = dictmodules.from_project("formRecordflmodules")
        self.assertTrue(module_)

        cursor_2 = module_.cursor()
        field = module_.child("fLFieldDB2")
        self.assertNotEqual(field, None)
        field.setValue("hola")

        self.assertEqual(cursor_1.valueBuffer("descripcion"), "hola")
        cursor_2.setValueBuffer("descripcion", "nueva hola.")
        self.assertEqual(field.value(), "nueva hola.")

        # module_.form.close()


if __name__ == "__main__":
    unittest.main()
