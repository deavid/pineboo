"""
Tests for loader.connection.
"""
import unittest
from pineboolib.loader.projectconfig import ProjectConfig
from pineboolib.loader.connection import config_dbconn  # , connect_to_db
from pineboolib.loader.options import parse_options

# from unittest.mock import patch, Mock


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


if __name__ == "__main__":
    unittest.main()
