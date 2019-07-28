# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets  # type: ignore
from pineboolib.core import decorators
from PyQt5 import Qt  # type: ignore
from pineboolib import logging

from typing import Any

logger = logging.getLogger("QGroupBox")


class QGroupBox(QtWidgets.QGroupBox):

    style_str = None
    _line_width = 0
    presset = Qt.pyqtSignal(int)

    def __init__(self, *args, **kwargs) -> None:
        super(QGroupBox, self).__init__(*args, **kwargs)
        from pineboolib.core.settings import config

        self._line_width = 0
        # self._do_style()
        self.setFlat(True)
        if not config.value("ebcomportamiento/spacerLegacy", False):
            self.setSizePolicy(
                QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
            )

    def setLineWidth(self, width: int) -> None:
        self._line_width = width
        self._do_style()

    def setTitle(self, t: str) -> None:
        super().setTitle(t)
        self._do_style()

    def _do_style(self) -> None:
        self.style_str = "QGroupBox { font-weight: bold; background-color: transparent;"
        if self._line_width == 0 and not self.title():
            self.style_str += " border: none;"
        else:
            self.style_str += " border-width: %spx transarent" % self._line_width
        self.style_str += " }"
        self.setStyleSheet(self.style_str)

    @property
    def selectedId(self):
        return 0

    def get_enabled(self) -> Any:
        return self.isEnabled()

    def set_enabled(self, b) -> None:
        self.setDisabled(not b)

    @decorators.NotImplementedWarn
    def setShown(self, b):
        pass

    def __setattr__(self, name: str, value: Any) -> None:
        if name == "title":
            self.setTitle(str(value))
        else:
            super().__setattr__(name, value)

    @decorators.NotImplementedWarn
    def setFrameShadow(self, fs):
        pass

    @decorators.NotImplementedWarn
    def setFrameShape(self, fs):
        pass

    @decorators.NotImplementedWarn
    def newColumn(self):
        pass

    enabled = property(get_enabled, set_enabled)
