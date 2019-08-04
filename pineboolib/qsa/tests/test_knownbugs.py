"""
Tests for known bugs on qsa.
"""

import unittest
from pineboolib.loader.main import init_testing
from pineboolib.application.types import Function


class TestIsLoadedModule(unittest.TestCase):
    """Test qsa.isLoadedModule."""

    @classmethod
    def setUpClass(cls) -> None:
        """Ensure pineboo is initialized for testing."""
        init_testing()

    def test_full(self) -> None:
        """Test bug where sys.isLoadedModule seems to be None."""

        fn_test = Function("module", "return sys.isLoadedModule(module);")
        self.assertEqual(fn_test("random_module"), False)
        self.assertEqual(fn_test("sys"), True)


if __name__ == "__main__":
    unittest.main()
