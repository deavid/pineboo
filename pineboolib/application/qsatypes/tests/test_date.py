"""Test_systype module."""

import unittest
from pineboolib.loader.main import init_testing


class TestDate(unittest.TestCase):
    """TestDate Class."""

    @classmethod
    def setUpClass(cls) -> None:
        """Ensure pineboo is initialized for testing."""
        init_testing()

    def test_basic(self) -> None:
        """Test Date class."""

        from pineboolib.application.qsatypes import date

        date_ = date.Date("2019-11-03")
        self.assertEqual(date_.toString(), "2019-11-03T00:00:00")
        self.assertEqual(date_.toString("yyyy-MM-dd"), "2019-11-03")
        self.assertEqual(date_.toString("MM:yyyy-dd"), "11:2019-03")
        self.assertEqual(date_.getTime(), 20191103000000)
        self.assertEqual(date_.getYear(), 2019)
        self.assertEqual(date_.getMonth(), 11)
        self.assertEqual(date_.getDay(), 3)
        date_.setDay(26)
        self.assertEqual(date_.toString(), "2019-11-26T00:00:00")
        self.assertEqual(date_.getDay(), 26)
        self.assertEqual(date_.addDays(3).toString("yyyy-MM-dd"), "2019-11-29")
        self.assertEqual(date_.addMonths(-2).toString("yyyy-MM-dd"), "2019-09-26")
        self.assertEqual(date_.addYears(1).toString("yyyy-MM-dd"), "2020-11-26")


if __name__ == "__main__":
    unittest.main()
