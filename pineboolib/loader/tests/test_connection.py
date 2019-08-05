"""
Tests for loader.connection.
"""
import unittest
from pineboolib.loader.projectconfig import ProjectConfig
from pineboolib.loader.connection import config_dbconn  # , connect_to_db
from pineboolib.loader.options import parse_options
from . import fixture_path

from unittest.mock import patch, Mock


class TestConfigDBConn(unittest.TestCase):
    """Test for config_dbconn function."""

    maxDiff = 200

    def test_connstring(self) -> None:
        """Test to provide a connstring."""
        # format: "user:passwd:driver_alias@host:port/database"
        options = parse_options(["pineboo", "--connect", "user:pass@127.0.0.1:5433/mydb"])
        cfg1 = config_dbconn(options)
        cfg2 = ProjectConfig(
            database="mydb",
            username="user",
            password="pass",
            host="127.0.0.1",
            port=5433,
            type="PostgreSQL (PSYCOPG2)",
        )
        self.assertEqual(cfg1, cfg2)

        options = parse_options(["pineboo", "--connect", "mydb"])
        cfg1 = config_dbconn(options)
        cfg2 = ProjectConfig(
            database="mydb",
            username="postgres",
            password="",
            host="127.0.0.1",
            port=5432,
            type="PostgreSQL (PSYCOPG2)",
        )
        self.assertEqual(cfg1, cfg2)

    def test_project(self) -> None:
        """Test to provide a project template."""
        options = parse_options(["pineboo", "--load", fixture_path("project_test1")])
        cfg1 = config_dbconn(options)
        cfg2 = ProjectConfig(database="mydb", type="SQLite3 (SQLITE3)")
        self.assertEqual(cfg1, cfg2)

    @patch("pineboolib.loader.connection.getpass.getpass")
    def test_project_passwd(self, mock_get_pass: Mock) -> None:
        """Test to provide a project template with password."""
        mock_get_pass.return_value = "myhardtoguesspassword"
        options = parse_options(["pineboo", "--load", fixture_path("project_test2")])
        cfg1 = config_dbconn(options)
        cfg2 = ProjectConfig(
            database="postgres_testdb",
            type="PostgreSQL (PSYCOPG2)",
            host="192.168.1.101",
            port=5432,
            username="postgres",
            password="postgrespassword",
            description="Postgres Test DB",
            project_password="myhardtoguesspassword",
        )
        self.assertEqual(cfg1, cfg2)


if __name__ == "__main__":
    unittest.main()
