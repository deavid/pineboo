"""
Tests for loader.main.
"""
import unittest
from unittest.mock import patch
from pineboolib.loader.options import parse_options
from pineboolib.loader import main


class TestMain(unittest.TestCase):
    """Test Main load."""

    @patch("pineboolib.loader.main.sys.exit")
    @patch("pineboolib.loader.main.exec_main")
    @patch("pineboolib.loader.main.parse_options")
    def test_startup(self, mock_parse_options, mock_exec_main, mock_sys_exit) -> None:
        """Test bug where logging tries to get incorrect options."""
        options = parse_options(custom_argv=[])
        mock_parse_options.return_value = options
        main.startup()
        mock_parse_options.assert_called_once()
        mock_exec_main.assert_called_once()
        mock_sys_exit.assert_called_once()


if __name__ == "__main__":
    unittest.main()
