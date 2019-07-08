from typing import Any

# -*- coding: utf-8 -*-


class AQBoolFlagState(object):
    modifier_ = None
    prevValue_ = None


class AQBoolFlagStateList(object):

    data_list_ = None

    def __init__(self):
        self.data_list_ = []

    def append(self, data=None) -> None:
        if data is not None:
            self.data_list_.append(data)

    def pushOnTop(self, data) -> None:

        data_list_new = []
        data_list_new.append(data)
        for old_data in self.data_list_:
            data_list_new.append(old_data)

        self.data_list_ = data_list_new

    def erase(self, data) -> None:

        for d in self.data_list_:
            if d == data:
                del d
                break

    def find(self, data) -> Any:
        ret_ = None
        for d in self.data_list_:
            if d.modifier_ == data:
                ret_ = d
                break

        return ret_

    def current(self) -> Any:
        return self.data_list_[0]
