class PNGroupByQuery(object):

    level_: int
    field_: str

    def __init__(self, l: int, f: str) -> None:
        self.level_ = l
        self.field_ = f

    def level(self) -> int:
        return self.level_

    def field(self) -> str:
        return self.field_
