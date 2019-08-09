"""Test_pnbuffer module."""

import unittest
from pineboolib.loader.main import init_testing
from pineboolib.application.database import pnsqlcursor


class TestPNBuffer(unittest.TestCase):
    """TestPNBuffer Class."""

    @classmethod
    def setUpClass(cls) -> None:
        """Ensure pineboo is initialized for testing."""
        init_testing()

        cursor = pnsqlcursor.PNSqlCursor("fltest")
        cursor.setModeAccess(cursor.Insert)
        cursor.refreshBuffer()
        cursor.setValueBuffer("string_field", "Campo texto 1")
        cursor.setValueBuffer("date_field", "2019-01-01")
        cursor.setValueBuffer("time_field", "01:01:01")
        cursor.setValueBuffer("bool_field", False)
        cursor.setValueBuffer("double_field", 1.01)
        cursor.commitBuffer()
        cursor.setModeAccess(cursor.Insert)
        cursor.refreshBuffer()
        cursor.setValueBuffer("string_field", "Campo texto 2")
        cursor.setValueBuffer("date_field", "2019-02-02")
        cursor.setValueBuffer("time_field", "02:02:02")
        cursor.setValueBuffer("bool_field", True)
        cursor.setValueBuffer("double_field", 2.02)
        cursor.commitBuffer()
        cursor.setModeAccess(cursor.Insert)
        cursor.refreshBuffer()
        cursor.setValueBuffer("string_field", "Campo texto 3")
        cursor.setValueBuffer("date_field", "2019-03-03")
        cursor.setValueBuffer("time_field", "03:03:03")
        cursor.setValueBuffer("bool_field", True)
        cursor.setValueBuffer("double_field", 3.03)
        cursor.commitBuffer()

    def test_basic1(self) -> None:
        """Basic test 1."""

        cursor = pnsqlcursor.PNSqlCursor("fltest")
        cursor.select()
        cursor.first()

        buffer_ = cursor.buffer()

        if buffer_ is None:
            raise Exception("buffer is empty!.")

        self.assertEqual(buffer_.value(2), "2019-01-01")
        self.assertEqual(buffer_.value("date_field"), "2019-01-01")
        self.assertEqual(buffer_.count(), 7)
        buffer_.clear_buffer()
        buffer_.primeUpdate(0)
        buffer_.primeDelete()
        self.assertEqual(buffer_.value(1), None)
        buffer_.primeUpdate(0)
        buffer_.setRow(0)
        self.assertEqual(buffer_.row(), 0)
        self.assertEqual(buffer_.value(1), "Campo texto 1")
        self.assertEqual(buffer_.setNull(1), True)
        self.assertEqual(buffer_.value(1), None)
        time_field_ = buffer_.field("time_field")

        if time_field_ is None:
            raise Exception("time_field_ is empty!.")

        self.assertEqual(time_field_.generated, True)
        buffer_.setGenerated(3, False)
        self.assertEqual(time_field_.generated, False)

    def test_basic2(self) -> None:
        """Basic test 2."""

        cursor = pnsqlcursor.PNSqlCursor("fltest")
        cursor.select()
        cursor.first()

        buffer_ = cursor.buffer()

        if buffer_ is None:
            raise Exception("buffer is empty!.")

        self.assertEqual(buffer_.isNull("string_field"), False)
        self.assertEqual(buffer_.isNull("date_field"), False)
        self.assertEqual(buffer_.isNull("time_field"), False)
        self.assertEqual(buffer_.isNull("bool_field"), False)
        self.assertEqual(buffer_.isNull("double_field"), False)

        self.assertEqual(buffer_.isEmpty(), False)
        buffer_.clearValues()
        self.assertEqual(buffer_.isNull("string_field"), True)
        self.assertEqual(buffer_.isNull("date_field"), True)
        self.assertEqual(buffer_.isNull("time_field"), True)
        self.assertEqual(buffer_.isNull("bool_field"), True)
        self.assertEqual(buffer_.isNull("double_field"), True)
        buffer_.primeUpdate()

        self.assertEqual(buffer_.value("string_field"), "Campo texto 1")
        self.assertEqual(buffer_.value("double_field"), 1.01)
        self.assertEqual(buffer_.value("date_field"), "2019-01-01")
        self.assertEqual(buffer_.value("time_field"), "01:01:01")
        self.assertEqual(buffer_.value("bool_field"), False)

    def test_basic3(self) -> None:
        """Basic test 3."""

        cursor = pnsqlcursor.PNSqlCursor("fltest")
        cursor.select()
        cursor.first()

        buffer_ = cursor.buffer()

        if buffer_ is None:
            raise Exception("buffer is empty!.")

        buffer_.setValue("string_field", "Campo texto 1 mod")
        self.assertEqual(buffer_.modifiedFields(), ["string_field"])
        buffer_.setNoModifiedFields()
        self.assertEqual(buffer_.modifiedFields(), [])
        buffer_.setValue("double_field", 1.02)
        self.assertEqual(buffer_.modifiedFields(), ["double_field"])
        self.assertEqual(buffer_.value("double_field"), 1.02)

    def test_basic4(self) -> None:
        """Basic test 4."""

        cursor = pnsqlcursor.PNSqlCursor("fltest")
        cursor.select()
        cursor.first()

        buffer_ = cursor.buffer()

        if buffer_ is None:
            raise Exception("buffer is empty!.")

        self.assertEqual(buffer_.pK(), "id")
        self.assertEqual(buffer_.indexField("string_field"), 1)

        field_ = buffer_.field("bool_field")

        if field_ is None:
            raise Exception("field_ is empty!.")

        self.assertEqual(field_.name, "bool_field")


if __name__ == "__main__":
    unittest.main()
