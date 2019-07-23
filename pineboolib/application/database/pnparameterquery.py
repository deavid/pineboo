from typing import Any
from pineboolib.interfaces.iparameterquery import IParameterQuery


class PNParameterQuery(IParameterQuery):

    name_: str
    alias_: str
    type_: int
    value_: Any

    def __init__(self, n: str, a: str, t: int) -> None:
        self.name_ = n
        self.alias_ = a
        self.type_ = t

    def name(self) -> str:
        return self.name_

    def alias(self) -> str:
        return self.alias_

    def type(self) -> int:
        return self.type_

    def value(self) -> Any:
        return self.value_

    def setValue(self, v: Any) -> None:
        self.value_ = v
