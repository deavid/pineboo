from typing import List, Optional, Union


class IFieldMetaData:
    def __init__(self, *args, **kwargs) -> None:
        pass

    def __len__(self) -> int:
        pass

    def addRelationMD(self, r) -> None:
        pass

    def alias(self) -> str:
        pass

    def allowNull(self) -> bool:
        pass

    def associatedField(self) -> None:
        pass

    def associatedFieldFilterTo(self) -> str:
        pass

    def associatedFieldName(self) -> Optional[str]:
        pass

    def defaultValue(self) -> Optional[Union[str, bool]]:
        pass

    def editable(self) -> bool:
        pass

    def formatAssignValue(self, fieldName: str, value: int, upper: bool) -> str:
        pass

    def generated(self) -> bool:
        pass

    def getIndexOptionsList(self, name: str) -> Optional[int]:
        pass

    def hasOptionsList(self) -> bool:
        pass

    def inicializeNewFLFieldMetaData(self, *args, **kwargs) -> None:
        pass

    def isCompoundKey(self) -> bool:
        pass

    def isPrimaryKey(self) -> bool:
        pass

    def length(self) -> int:
        pass

    def metadata(self) -> None:
        pass

    def name(self) -> str:
        pass

    def optionsList(self) -> List[str]:
        pass

    def outTransaction(self) -> bool:
        pass

    def partDecimal(self) -> int:
        pass

    def partInteger(self) -> int:
        pass

    def regExpValidator(self) -> Optional[str]:
        pass

    def relationM1(self) -> None:
        pass

    def setAssociatedField(self, r_or_name, f: str) -> None:
        pass

    def setEditable(self, ed: bool) -> None:
        pass

    def setFullyCalculated(self, c: bool) -> None:
        pass

    def setMetadata(self, mtd) -> None:
        pass

    def setOptionsList(self, ol: str) -> None:
        pass

    def setTrimed(self, t: bool) -> None:
        pass

    def setVisible(self, v: bool) -> None:
        pass

    def type(self) -> str:
        pass

    def visible(self) -> bool:
        pass

    def visibleGrid(self) -> bool:
        pass
