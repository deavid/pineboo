"""
Tests for known bugs on qsa.
"""

import unittest
from pineboolib.loader.main import init_testing
from pineboolib.application.types import Function
from pineboolib.application.parsers.qsaparser.postparse import pythonify_string as qs2py


class TestIsLoadedModule(unittest.TestCase):
    """Test qsa.isLoadedModule."""

    @classmethod
    def setUpClass(cls) -> None:
        """Ensure pineboo is initialized for testing."""
        init_testing()

    def test_isloadedmodule(self) -> None:
        """Test bug where sys.isLoadedModule seems to be None."""

        fn_test = Function("module", "return sys.isLoadedModule(module);")
        self.assertEqual(fn_test("random_module"), False)
        self.assertEqual(fn_test("sys"), True)

    def test_mid(self) -> None:
        """Test str.mid(5, 2)."""

        value_1 = 'var cadena:String = "abcdefg";\ncadena.mid(5, 2);'
        self.assertEqual(qs2py(value_1), 'cadena = "abcdefg"\ncadena[5, 2]\n')

        value_2 = 'var cadena:String = "abcdefg";\ncadena.mid(5);'
        self.assertEqual(qs2py(value_2), 'cadena = "abcdefg"\ncadena[0 + 5 :]\n')


if __name__ == "__main__":
    unittest.main()
