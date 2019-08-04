"""
Version number normalization library.
"""
import re
from typing import List, Optional, Tuple, Any

from pineboolib.core.utils import logging

SubVersionNumber = int
SubVersionAppendedText = str
SubVersionTuple = Tuple[SubVersionNumber, SubVersionAppendedText]


logger = logging.getLogger(__name__)


class VersionNumber:
    """
    Create version objects from string that can be easily be compared together.
    """

    is_null: bool  # True if no version at all.
    raw_text: str  # Raw version text or empty string if null.
    text: str  # Version text or empty string if null.
    normalized: List[SubVersionTuple]  # Normalized version

    def __init__(self, version_string: Optional[str], default: Optional[str] = None) -> None:
        """
        Create Version object.
        """
        if default is not None and version_string is None:
            version_string = default

        self.is_null = version_string is None

        if version_string is None:
            version_string = ""

        self.raw_text = version_string
        self.text = version_string.strip().lstrip("v")
        self.normalized = [] if self.is_null else self.normalize_complex(version_string)

    def __eq__(self, other_any: Any) -> bool:
        """Compare for equality."""
        other: "VersionNumber" = self.to_version_number(other_any)
        return self.normalized == other.normalized

    def __neq__(self, other_any: Any) -> bool:
        """Compare for unequality."""
        other: "VersionNumber" = self.to_version_number(other_any)
        return self.normalized != other.normalized

    def __gt__(self, other_any: Any) -> bool:
        """Compare for greater than."""
        other: "VersionNumber" = self.to_version_number(other_any)
        return self.normalized > other.normalized

    def __lt__(self, other_any: Any) -> bool:
        """Compare for less than."""
        other: "VersionNumber" = self.to_version_number(other_any)
        return self.normalized < other.normalized

    def __ge__(self, other_any: Any) -> bool:
        """Compare for greater than equal."""
        other: "VersionNumber" = self.to_version_number(other_any)
        return self.normalized >= other.normalized

    def __le__(self, other_any: Any) -> bool:
        """Compare for less than equal."""
        other: "VersionNumber" = self.to_version_number(other_any)
        return self.normalized <= other.normalized

    def __str__(self) -> str:
        """Get string representation of the version."""
        return self.text

    def __repr__(self) -> str:
        """Get python representation of the version."""
        return "<%s %r>" % (str(self.__class__.__name__), None if self.is_null else self.text)

    @classmethod
    def to_version_number(self, other_any: Any) -> "VersionNumber":
        """Convert any input to VersionNumber."""
        other: "VersionNumber"
        if isinstance(other_any, str):
            other = VersionNumber(other_any)
        elif isinstance(other_any, VersionNumber):
            other = other_any
        else:
            raise ValueError("Can't compare VersionNumber with %r" % type(other_any))
        return other

    @classmethod
    def normalize_complex(cls, raw_text: str) -> List[SubVersionTuple]:
        """
        Normalize a complex version as 1.0.5b-ubuntu0 into something that can be used for comparison.
        """
        decomposed_str: List[str] = raw_text.strip().lstrip("v").split(".")
        normalized: List[SubVersionTuple] = []
        subver: str
        for subver in decomposed_str:
            subver = subver.strip()
            subver_appended_part: SubVersionAppendedText = subver.lstrip("0123456789")

            subver_number_part = (
                subver[: -len(subver_appended_part)] if subver_appended_part else subver
            )

            subver_number: SubVersionNumber = int(subver_number_part) if subver_number_part else -1
            normalized.append((subver_number, subver_appended_part))
        return normalized

    @classmethod
    def check(cls, mod_name: str, mod_ver: str, min_ver: str) -> bool:
        """Compare two version numbers and raise a warning if "minver" is not met."""
        if cls.normalize(mod_ver) < cls.normalize(min_ver):
            logger.warning(
                "La version de <%s> es %s. La mínima recomendada es %s.", mod_name, mod_ver, min_ver
            )
            return False
        return True

    @classmethod
    def normalize(cls, v: str) -> List[int]:
        """Normalize version string numbers like 3.10.1 so they can be compared."""
        return [int(x) for x in re.sub(r"(\.0+)*$", "", v).split(".")]
