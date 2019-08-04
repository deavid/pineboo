"""
Version number normalization library.
"""
import re
from typing import List
from pineboolib.core.utils import logging

logger = logging.getLogger(__name__)


class VersionNumber:
    """
    Create version objects from string that can be easily be compared together.
    """

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
