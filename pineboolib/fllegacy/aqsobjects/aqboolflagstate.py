from typing import List, Optional

# -*- coding: utf-8 -*-


class AQBoolFlagState(object):
    modifier_: bool
    prevValue_: bool


class AQBoolFlagStateList(object):

    data_list_: List[AQBoolFlagState]

    def __init__(self):
        self.data_list_ = []

    def append(self, data) -> None:
        if data is not None:
            self.data_list_.append(data)

    def pushOnTop(self, data) -> None:
        self.data_list_.insert(0, data)

    def erase(self, data) -> None:
        self.data_list_.remove(data)

    def find(self, data) -> Optional[AQBoolFlagState]:
        for d in self.data_list_:
            if d.modifier_ == data:
                return d

        return None

    def current(self) -> Optional[AQBoolFlagState]:
        if not self.data_list_:
            return None
        return self.data_list_[0]
