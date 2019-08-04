"""
Tests for utils.version.VersionNumber.
"""
import unittest
from pineboolib.core.utils.version import VersionNumber


class TestVersionNumber(unittest.TestCase):
    """Test VersionNumber class."""

    def test_create(self) -> None:
        """Test create version."""
        version = VersionNumber("1.0.1")
        self.assertEqual(version.is_null, False)
        self.assertEqual(version.raw_text, "1.0.1")

    def test_normalize_complex(self) -> None:
        """Test normalize_complex function."""
        norm_cplx = VersionNumber.normalize_complex
        self.assertEqual(norm_cplx("1.0.0"), [(1, ""), (0, ""), (0, "")])
        self.assertEqual(norm_cplx("1b.0.0-ubuntu0"), [(1, "b"), (0, ""), (0, "-ubuntu0")])

    def test_compare(self) -> None:
        """Test compare versions."""

        self.assertEqual(VersionNumber("1.0.1") == VersionNumber("1.0.1 "), True)
        self.assertEqual(VersionNumber("1.0.1") > VersionNumber("1.0.1 "), False)
        self.assertEqual(VersionNumber("1.0b.1") < VersionNumber("1.0a.1 "), False)
        self.assertEqual(VersionNumber("1.0b.1") != VersionNumber("1.0a.1"), True)
        self.assertEqual(VersionNumber("1.0.1") >= VersionNumber("1.0.1"), True)
        self.assertEqual(VersionNumber("1.0.1") <= VersionNumber("1.0.1"), True)
        self.assertEqual(VersionNumber("1.0.1") > VersionNumber("1.0.1"), False)
        self.assertEqual(VersionNumber("1.0.1") < VersionNumber("1.0.1"), False)

    def test_repr_str(self) -> None:
        """Test repr and str methods."""
        self.assertEqual(str(VersionNumber("v1.0a.1 ")), "1.0a.1")
        self.assertEqual(str(VersionNumber(None)), "")
        self.assertEqual(repr(VersionNumber("v1.0a.1 ")), "<VersionNumber '1.0a.1'>")
        self.assertEqual(repr(VersionNumber(None)), "<VersionNumber None>")


if __name__ == "__main__":
    unittest.main()
