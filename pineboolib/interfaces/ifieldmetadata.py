"""
IFieldMetaData module.
"""
from typing import List, Optional, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from .itablemetadata import ITableMetaData  # noqa: F401
    from pineboolib.application.metadata.pnrelationmetadata import PNRelationMetaData  # noqa: F401


class IFieldMetaData:
    """
    Abastract class for FieldMetaData.
    """

    def __init__(self, *args, **kwargs) -> None:
        """Create new FieldMetaData."""
        return

    def __len__(self) -> int:
        """Get size of field."""
        return 0

    def addRelationMD(self, r) -> None:
        """Add relation M1 or 1M."""
        return

    def alias(self) -> str:
        """Get alias for this field."""
        return ""

    def allowNull(self) -> bool:
        """Determine if this field allos NULLs."""
        return False

    def associatedField(self) -> Optional["ITableMetaData"]:
        """Return associated field."""
        return None

    def associatedFieldFilterTo(self) -> str:
        """Return associated field filter in sql string format."""
        return ""

    def associatedFieldName(self) -> Optional[str]:
        """Return associated field name."""
        return None

    def defaultValue(self) -> Optional[Union[str, bool]]:
        """Return field default value."""
        return None

    def editable(self) -> bool:
        """Get if field is editable."""
        return False

    def formatAssignValue(self, fieldName: str, value: int, upper: bool) -> str:
        """Format a value for this field."""
        return ""

    def generated(self) -> bool:
        """Get if field is computed."""
        return False

    def getIndexOptionsList(self, name: str) -> Optional[int]:
        """Get list of options."""
        return None

    def hasOptionsList(self) -> bool:
        """Return if this field has list of options."""
        return False

    def inicializeFLFieldMetaData(self, other) -> None:
        """Initialize."""
        return

    def inicializeNewFLFieldMetaData(
        self,
        n: str,
        a: str,
        aN: bool,
        isPrimaryKey: bool,
        t: str,
        length_: int = 0,
        c: bool = False,
        v: bool = True,
        ed: bool = True,
        pI: int = 4,
        pD: int = 0,
        iNX: bool = False,
        uNI: bool = False,
        coun: bool = False,
        defValue: Optional[str] = None,
        oT: bool = False,
        rX: Optional[str] = None,
        vG: bool = True,
        gen: bool = True,
        iCK: bool = False,
    ) -> None:
        """Initialize."""
        return

    def isCompoundKey(self) -> bool:
        """Return if this field is part of CK."""
        return False

    def isPrimaryKey(self) -> bool:
        """Return if this field is PK."""
        return False

    def length(self) -> int:
        """Return field size."""
        return 0

    def metadata(self) -> Optional["ITableMetaData"]:
        """Return table metadata for this field."""
        return None

    def name(self) -> str:
        """Get name of this field."""
        return ""

    def optionsList(self) -> List[str]:
        """Get list of options for this field."""
        return []

    def outTransaction(self) -> bool:
        """Return if this field should be updated outside of transaction."""
        return False

    def partDecimal(self) -> int:
        """Return the amount of digits after dot when formatting numbers."""
        return 0

    def partInteger(self) -> int:
        """Return amount of digits before decimal dot."""
        return 0

    def regExpValidator(self) -> Optional[str]:
        """Validate regexp."""
        return None

    def relationM1(self) -> Optional["PNRelationMetaData"]:
        """Return M1 relationship in this field."""
        return None

    def setAssociatedField(self, r_or_name, f: str) -> None:
        """Set new associated field."""
        return

    def setEditable(self, ed: bool) -> None:
        """Set if this field should be editable."""
        return

    def setFullyCalculated(self, c: bool) -> None:
        """Set if this field should be fully calculated."""
        return

    def setMetadata(self, mtd) -> None:
        """Set TableMetadata for this field."""
        return

    def setOptionsList(self, ol: str) -> None:
        """Set option list for this field."""
        return

    def setTrimed(self, t: bool) -> None:
        """Set if this field should be trimed."""
        return

    def setVisible(self, v: bool) -> None:
        """Set if this field should be visible."""
        return

    def type(self) -> str:
        """Return field type."""
        return ""

    def visible(self) -> bool:
        """Get if this field should be visible in UI."""
        return False

    def visibleGrid(self) -> bool:
        """Get if this field should be visible in grids."""
        return False
