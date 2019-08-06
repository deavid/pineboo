"""Test_sysbasetype module."""

import unittest
from pineboolib.loader.main import init_testing


class TestSysBaseClassGeneral(unittest.TestCase):
    """TestSysBaseClassGeneral Class."""

    @classmethod
    def setUpClass(cls) -> None:
        """Ensure pineboo is initialized for testing."""
        init_testing()

    def test_basic(self) -> None:
        """Test basic functions."""
        import platform
        from pineboolib.application.qsatypes import sysbasetype
        from pineboolib.core.utils.utils_base import filedir
        from pineboolib import application
        import os

        base_type = sysbasetype.SysBaseType()

        self.assertEqual(base_type.nameUser(), None)
        self.assertEqual(base_type.interactiveGUI(), "Pineboo")
        self.assertEqual(base_type.isLoadedModule("sys"), True)
        os_name = "LINUX"
        if platform.system() == "Windows":
            os_name = "WIN32"
        elif platform.system() == "Darwin":
            os_name = "MACX"

        self.assertEqual(base_type.osName(), os_name)
        self.assertEqual(base_type.nameBD(), "")
        self.assertEqual(base_type.installPrefix(), filedir(".."))
        self.assertEqual(base_type.version(), str(application.project.version))
        file_path = "%s/test_sysbasetype.txt" % application.project.tmpdir

        if os.path.exists(file_path):
            os.remove(file_path)

        base_type.write("ISO-8859-15", file_path, "avión, caña")
        self.assertEqual(os.path.exists(file_path), True)
        self.assertEqual(base_type.nameDriver(), "FLsqlite")
        self.assertEqual(base_type.nameHost(), None)

        prueba_conn = application.project.conn.useConn("prueba")
        self.assertEqual(prueba_conn.isOpen(), False)
        self.assertEqual(base_type.addDatabase("prueba"), True)
        self.assertEqual(prueba_conn.isOpen(), True)
        self.assertEqual(base_type.removeDatabase("prueba"), True)
        self.assertNotEqual(base_type.idSession(), None)


if __name__ == "__main__":
    unittest.main()
