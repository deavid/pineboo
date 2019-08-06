"""
Tests for loader.projectconfig.
"""
import os.path
import unittest
import tempfile
from unittest.mock import Mock, patch
from pineboolib.loader.projectconfig import ProjectConfig, VERSION_1_1, VERSION_1_2
from pineboolib.loader.projectconfig import PasswordMismatchError
from . import fixture_read

# from unittest.mock import patch, Mock


class TestProjectConfig(unittest.TestCase):
    """Test ProjectConfig class."""

    maxDiff = 1000

    def test_basic(self) -> None:
        """Test to create projectConfig class."""
        cfg = ProjectConfig(database="mydb", type="SQLite3 (SQLITE3)")
        self.assertTrue(cfg)
        self.assertEqual(cfg.SAVE_VERSION, VERSION_1_2)

    def test_read_write(self) -> None:
        """Test that we can read a file, save it back, read it again and stays the same."""
        project_test1 = fixture_read("project_test1.xml")
        with tempfile.TemporaryDirectory() as tmpdirname:
            cfg = ProjectConfig(
                database="mydb",
                type="SQLite3 (SQLITE3)",
                filename=os.path.join(tmpdirname, "test.xml"),
            )
            cfg.SAVE_VERSION = VERSION_1_1
            cfg.save_projectxml(False)
            self.assertEqual(open(cfg.filename).read(), project_test1)
            cfg2 = ProjectConfig(load_xml=cfg.filename)
            cfg2.SAVE_VERSION = cfg2.version
            cfg2.save_projectxml(True)
            self.assertEqual(open(cfg2.filename).read(), project_test1)

    @patch("os.urandom")
    def test_read_write2(self, mock_urandom: Mock) -> None:
        """Test we can read and write and stays equal (slightly more complicated)."""
        project_test2 = fixture_read("project_test2.xml")
        project_test3 = fixture_read("project_test3.xml")
        mock_urandom.return_value = b"123456789"
        with tempfile.TemporaryDirectory() as tmpdirname:
            # Verify Version 1.1
            cfg = ProjectConfig(
                database="postgres_testdb",
                description="Postgres Test DB",
                type="PostgreSQL (PSYCOPG2)",
                host="192.168.1.101",
                port=5432,
                username="postgres",
                password="postgrespassword",
                project_password="myhardtoguesspassword",
                filename=os.path.join(tmpdirname, "test.xml"),
            )
            cfg.SAVE_VERSION = VERSION_1_1
            cfg.save_projectxml(False)
            self.assertEqual(open(cfg.filename).read(), project_test2)

            with self.assertRaises(PasswordMismatchError):
                ProjectConfig(load_xml=cfg.filename, project_password="wrongpassword")

            cfg2 = ProjectConfig(load_xml=cfg.filename, project_password="myhardtoguesspassword")
            cfg2.SAVE_VERSION = cfg2.version
            cfg2.save_projectxml(True)
            self.assertEqual(open(cfg2.filename).read(), project_test2)

            # Verify Version 1.2
            cfg2.SAVE_VERSION = VERSION_1_2
            cfg2.save_projectxml(True)
            self.assertEqual(open(cfg2.filename).read(), project_test3)

            with self.assertRaises(PasswordMismatchError):
                ProjectConfig(load_xml=cfg2.filename, project_password="wrongpassword")

            cfg3 = ProjectConfig(load_xml=cfg2.filename, project_password="myhardtoguesspassword")
            cfg3.SAVE_VERSION = VERSION_1_2
            cfg3.save_projectxml(True)
            self.assertEqual(open(cfg3.filename).read(), project_test3)


if __name__ == "__main__":
    unittest.main()
