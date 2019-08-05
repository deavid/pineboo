"""
Test QS Snippets.
"""
import unittest
from pineboolib.application.parsers.qsaparser.postparse import pythonify_string as qs2py
from pineboolib.application.parsers.qsaparser import pytnyzer


class TestParser(unittest.TestCase):
    """Test Parsing QS to PY."""

    @classmethod
    def setUpClass(cls) -> None:
        """Enable strict parsing."""
        pytnyzer.STRICT_MODE = True

    def test_basic(self) -> None:
        """Test basic stuff."""

        self.assertEqual(qs2py("x = 0"), "x = 0\n")

    def test_file_class(self) -> None:
        """Test parsing the file class."""
        self.assertEqual(qs2py('x = File.read("test")'), 'x = qsa.FileStatic.read("test")\n')
        self.assertEqual(
            qs2py('x = File.write("test", "contents")'),
            'x = qsa.FileStatic.write("test", "contents")\n',
        )
        self.assertEqual(qs2py('x = File.remove("test")'), 'x = qsa.FileStatic.remove("test")\n')

        self.assertEqual(qs2py('x = File("test").read()'), 'x = qsa.File("test").read()\n')
        self.assertEqual(
            qs2py('x = File("test").write("contents")'), 'x = qsa.File("test").write("contents")\n'
        )
        self.assertEqual(qs2py('x = File("test").remove()'), 'x = qsa.File("test").remove()\n')


if __name__ == "__main__":
    unittest.main()
