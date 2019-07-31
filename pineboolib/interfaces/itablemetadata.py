"""
ITableMetadata module.
"""
from typing import List, Optional, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from pineboolib.application.metadata.pnfieldmetadata import PNFieldMetaData  # noqa


class ITableMetaData:
    """Abstract class for PNTableMetaData."""

    def __init__(self, n: str, a: Optional[str], q: Optional[str]) -> None:
        """Create new tablemetadata."""
        return

    def addFieldMD(self, f) -> None:
        """Add new field to this object."""
        return

    def field(self, fN: str) -> Any:
        """Retrieve field by name."""
        return

    def fieldIsIndex(self, field_name: str) -> int:
        """Get if a field is an index."""
        return -1

    def fieldList(self):
        """Return list of fields."""
        return

    def fieldListOfCompoundKey(self, fN: str) -> Optional[List["PNFieldMetaData"]]:
        """Return list of fields for CK."""
        return []

    def fieldNameToAlias(self, fN: str) -> str:
        """Get alias of field."""
        return ""

    def fieldNames(self) -> List[str]:
        """Get list of field names."""
        return []

    def fieldNamesUnlock(self) -> List[str]:
        """Get field names for unlock fields."""
        return []

    def inCache(self) -> bool:
        """Get if in cache."""
        return False

    def indexFieldObject(self, position: int):
        """Get field by position."""
        return

    def indexPos(self, field_name: str) -> int:
        """Get field position by name."""
        return 0

    def inicializeNewFLTableMetaData(self, n: str, a: str, q: Optional[str]) -> None:
        """Initialize object."""
        return

    def isQuery(self) -> bool:
        """Return true if is a query."""
        return False

    def name(self) -> str:
        """Get table name."""
        return ""

    def primaryKey(self, prefixTable: bool) -> str:
        """Get primary key field."""
        return ""

    def query(self) -> str:
        """Get query string."""
        return ""

    def relation(self, fN: str, fFN: str, fTN: str):
        """Get relation object."""
        return

    def setCompoundKey(self, cK) -> None:
        """Set CK."""
        return

    def setConcurWarn(self, b: bool) -> None:
        """Enable concurrency warning."""
        return

    def setDetectLocks(self, b: bool) -> None:
        """Enable Lock detection."""
        return

    def setFTSFunction(self, ftsfun: str) -> None:
        """Set Full-Text-Search function."""
        return
