"""Test_process module."""

import unittest
from pineboolib.loader.main import init_testing


class TestProcess(unittest.TestCase):
    """TestProcess Class."""

    @classmethod
    def setUpClass(cls) -> None:
        """Ensure pineboo is initialized for testing."""
        init_testing()

    def test_Process(self) -> None:
        """Test Process."""

        from pineboolib.application import process

        proc = process.Process()

        proc.execute("python3 --version")

        salida = None
        if proc.stderr != "":
            salida = proc.stderr
        else:
            salida = proc.stdout

        self.assertTrue(salida.find("Python") > -1)

    def test_ProcessStatic(self) -> None:
        """Test ProcessStatic."""

        from pineboolib.qsa import qsa

        proc = qsa.ProcessStatic

        proc.execute("python3 --version")

        salida = None
        if proc.stderr != "":
            salida = proc.stderr
        else:
            salida = proc.stdout

        self.assertTrue(salida.find("Python") > -1)
