"""Test_systype module."""

import unittest
from pineboolib.loader.main import init_testing


class TestFileWrite(unittest.TestCase):
    """TestCompoundKeyPNTableMetaData Class."""

    @classmethod
    def setUpClass(cls) -> None:
        """Ensure pineboo is initialized for testing."""
        init_testing()

    def test_basic(self) -> None:
        """Test FileWrite attributes."""

        from pineboolib.fllegacy import systype
        from pineboolib.application import types
        from pineboolib import application
        import os

        qsa_sys = systype.SysType()
        txt = "avión, cañita"
        path_1 = "%s/test_systype_one_iso_8859-15.txt" % application.project.tmpdir
        path_2 = "%s/test_systype_one_utf-8.txt" % application.project.tmpdir

        if os.path.exists(path_1):
            os.remove(path_1)

        if os.path.exists(path_2):
            os.remove(path_2)

        qsa_sys.fileWriteIso(path_1, txt)
        qsa_sys.fileWriteUtf8(path_2, txt)

        file_1 = types.File(path_1, "ISO-8859-15")
        file_2 = types.File(path_2, "UTF-8")

        result_1 = file_1.read()
        result_2 = file_2.read()

        self.assertEqual(result_1, txt)
        self.assertEqual(result_2, txt)


if __name__ == "__main__":
    unittest.main()
