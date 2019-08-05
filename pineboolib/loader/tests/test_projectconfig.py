"""
Tests for loader.projectconfig.
"""
import os.path
import unittest
import tempfile
from pineboolib.loader.projectconfig import ProjectConfig

# from unittest.mock import patch, Mock


class TestProjectConfig(unittest.TestCase):
    """Test ProjectConfig class."""

    maxDiff = 1000

    def test_basic(self) -> None:
        """Test to create projectConfig class."""
        cfg = ProjectConfig(database="mydb", type="SQLite3 (SQLITE3)")
        self.assertTrue(cfg)

    def test_read_write(self) -> None:
        """Test that we can read a file, save it back, read it again and stays the same."""
        project_test1 = fixture("project_test1.xml")
        with tempfile.TemporaryDirectory() as tmpdirname:
            cfg = ProjectConfig(
                database="mydb",
                type="SQLite3 (SQLITE3)",
                filename=os.path.join(tmpdirname, "test.xml"),
            )
            cfg.save_projectxml(False)
            self.assertEqual(open(cfg.filename).read(), project_test1)
            cfg2 = ProjectConfig(load_xml=cfg.filename)
            cfg2.save_projectxml(True)
            self.assertEqual(open(cfg2.filename).read(), project_test1)

    def test_read_write2(self) -> None:
        """Test we can read and write and stays equal (slightly more complicated)."""
        project_test1 = fixture("project_test2.xml")
        with tempfile.TemporaryDirectory() as tmpdirname:
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
            cfg.save_projectxml(False)
            self.assertEqual(open(cfg.filename).read(), project_test1)
            cfg2 = ProjectConfig(load_xml=cfg.filename, project_password="myhardtoguesspassword")
            cfg2.save_projectxml(True)
            self.assertEqual(open(cfg2.filename).read(), project_test1)


def fixture(*path: str) -> str:
    """
    Get fixture path for this test file.
    """
    basedir = os.path.realpath(os.path.dirname(__file__))
    filepath = os.path.join(basedir, "fixtures", *path)
    with open(filepath, "r") as file:
        contents = file.read()
    return contents


if __name__ == "__main__":
    unittest.main()
