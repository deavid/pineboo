from typing import List, Optional, Union
from .itablemetadata import ITableMetaData


class IFieldMetaData:
    """Abastract class for FieldMetaData.
    """

    def __init__(self, *args, **kwargs) -> None:
        return

    def __len__(self) -> int:
        return 0

    def addRelationMD(self, r) -> None:
        return

    def alias(self) -> str:
        return ""

    def allowNull(self) -> bool:
        return False

    def associatedField(self) -> None:
        return

    def associatedFieldFilterTo(self) -> str:
        return ""

    def associatedFieldName(self) -> Optional[str]:
        return None

    def defaultValue(self) -> Optional[Union[str, bool]]:
        return None

    def editable(self) -> bool:
        return False

    def formatAssignValue(self, fieldName: str, value: int, upper: bool) -> str:
        return ""

    def generated(self) -> bool:
        return False

    def getIndexOptionsList(self, name: str) -> Optional[int]:
        return None

    def hasOptionsList(self) -> bool:
        return False

    def inicializeNewFLFieldMetaData(self, *args, **kwargs) -> None:
        return

    def isCompoundKey(self) -> bool:
        return False

    def isPrimaryKey(self) -> bool:
        return False

    def length(self) -> int:
        return 0

    def metadata(self) -> ITableMetaData:
        return ITableMetaData("", None, None)

    def name(self) -> str:
        return ""

    def optionsList(self) -> List[str]:
        return []

    def outTransaction(self) -> bool:
        return False

    def partDecimal(self) -> int:
        return 0

    def partInteger(self) -> int:
        return 0

    def regExpValidator(self) -> Optional[str]:
        return None

    def relationM1(self) -> None:
        return

    def setAssociatedField(self, r_or_name, f: str) -> None:
        return

    def setEditable(self, ed: bool) -> None:
        return

    def setFullyCalculated(self, c: bool) -> None:
        return

    def setMetadata(self, mtd) -> None:
        return

    def setOptionsList(self, ol: str) -> None:
        return

    def setTrimed(self, t: bool) -> None:
        return

    def setVisible(self, v: bool) -> None:
        return

    def type(self) -> str:
        return ""

    def visible(self) -> bool:
        return False

    def visibleGrid(self) -> bool:
        return False
