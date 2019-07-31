"""
AQBoolFlagState package.

Save cursor states.
"""
from typing import List, Optional

# -*- coding: utf-8 -*-


class AQBoolFlagState(object):
    """AQBollFlagState Class."""

    modifier_: str
    prevValue_: bool


class AQBoolFlagStateList(object):
    """AQBoolFlagStateList Class."""

    data_list_: List[AQBoolFlagState]

    def __init__(self):
        """Initialize the list."""

        self.data_list_ = []

    def append(self, data: AQBoolFlagState) -> None:
        """
        Add a state to the list.

        @param data. Flag state.
        """

        if data is not None:
            self.data_list_.append(data)

    def pushOnTop(self, data: AQBoolFlagState) -> None:
        """
        Add a state to the list first.

        @param data. Flag state.
        """

        self.data_list_.insert(0, data)

    def erase(self, data: AQBoolFlagState) -> None:
        """
        Erase a state to the list first.

        @param data. Flag state.
        """
        self.data_list_.remove(data)

    def find(self, data: str) -> Optional[AQBoolFlagState]:
        """
        Search for a state in the list from a value.

        @param data. Value to search.
        @return Flag state.
        """

        for d in self.data_list_:
            if d.modifier_ == data:
                return d

        return None

    def current(self) -> Optional[AQBoolFlagState]:
        """
        Return the first state of the list.

        @return Flag state.
        """

        if not self.data_list_:
            return None
        return self.data_list_[0]
