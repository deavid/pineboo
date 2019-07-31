"""
Tests for application.types module.
"""

import unittest
from pineboolib.loader.main import init_cli
from pineboolib.application.types import Boolean, QString, Function, Object, Array, Date

init_cli()  # FIXME: This should be avoided


class TestBoolean(unittest.TestCase):
    """Test booleans."""

    def test_true(self):
        """Test for true."""
        self.assertEqual(Boolean(1), True)
        self.assertEqual(Boolean("True"), True)
        self.assertEqual(Boolean("Yes"), True)
        self.assertEqual(Boolean(0.8), True)

    def test_false(self):
        """Test for false."""
        self.assertEqual(Boolean(0), False)
        self.assertEqual(Boolean("False"), False)
        self.assertEqual(Boolean("No"), False)


class TestQString(unittest.TestCase):
    """Test QString."""

    def test_basic(self):
        """Basic testing."""
        s = QString("hello world")
        self.assertEqual(s, "hello world")
        self.assertEqual(s.mid(5), s[5:])
        self.assertEqual(s.mid(5, 2), s[5:7])


class TestFunction(unittest.TestCase):
    """Test function. Parses QSA into Python."""

    def test_basic(self):
        """Basic testing."""
        source = "return x + 1"
        fn = Function("x", source)
        self.assertEqual(fn(1), 2)


class TestObject(unittest.TestCase):
    """Test object."""

    def test_basic1(self):
        """Basic testing."""
        o = Object()
        o.prop1 = 1
        o.prop2 = 2
        self.assertEqual(o.prop1, o["prop1"])

    def test_basic2(self):
        """Basic testing."""
        o = Object({"prop1": 1})
        self.assertEqual(o.prop1, o["prop1"])


class TestArray(unittest.TestCase):
    """Test Array class."""

    def test_basic1(self):
        """Basic testing."""
        a = Array()
        a.value = 1
        self.assertEqual(a.value, a["value"])

    def test_basic2(self):
        """Basic testing."""
        test_arr = [0, 1, 2, 3, 4]
        a = Array(test_arr)
        self.assertEqual(a[3], 3)
        self.assertEqual(list(a._dict.values()), test_arr)
        self.assertEqual(len(a), len(test_arr))
        self.assertEqual(a, test_arr)

        test_arr = [3, 4, 2, 1, 0]
        a = Array(test_arr)
        self.assertEqual(list(a._dict.values()), test_arr)
        a.append(10)
        self.assertEqual(a[5], 10)

    def test_repr(self):
        """Test repr method."""
        test_arr = [3, 4, 5, 6, 7]
        a1 = Array(test_arr)
        self.assertEqual(repr(a1), "<Array %r>" % test_arr)

    def test_iter(self):
        """Test iterating arrays."""

        test_arr = [3, 4, 5, 6, 7]
        a1 = Array(test_arr)
        a2 = [x for x in a1]
        self.assertEqual(test_arr, a2)

        test_arr = [8, 7, 6, 4, 2]
        a1 = Array(test_arr)
        a2 = [x for x in a1]
        self.assertEqual(test_arr, a2)


class TestDate(unittest.TestCase):
    """Test Date class."""

    # FIXME: Complete unit tests
    def test_basic1(self):
        """Basic testing."""
        d = Date("2001-02-25")
        self.assertEqual(d.getDay(), 25)
        self.assertEqual(d.getMonth(), 2)
        self.assertEqual(d.getYear(), 2001)


if __name__ == "__main__":
    unittest.main()
