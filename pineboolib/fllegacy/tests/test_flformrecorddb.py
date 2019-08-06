"""Test_flformrecorddb module."""

import unittest
from pineboolib.loader.main import init_testing


class TestFLFormrecordCursor(unittest.TestCase):
    """TestFLFormrecordCursor Class."""

    @classmethod
    def setUpClass(cls) -> None:
        """Ensure pineboo is initialized for testing."""
        init_testing()

    def test_basic(self) -> None:
        """Test flformrecord cursor assignment"""

        from pineboolib.qsa import dictmodules
        from pineboolib.application.database import pnsqlcursor

        cursor_1 = pnsqlcursor.PNSqlCursor("flareas")
        cursor_1.select()
        cursor_1.setModeAccess(cursor_1.Insert)
        cursor_1.refreshBuffer()
        cursor_1.insertRecord(False)

        cursor_3 = pnsqlcursor.PNSqlCursor("flareas")

        module_ = dictmodules.from_project("formRecordflareas")
        self.assertNotEqual(module_, None)
        cursor_2 = module_.cursor()

        self.assertNotEqual(cursor_1, cursor_3)
        self.assertEqual(cursor_1, cursor_2)


if __name__ == "__main__":
    unittest.main()
