# -*- coding: utf-8 -*-
from pineboolib.fllegacy.flwidget import FLWidget
from typing import Any


class FLWorkSpace(FLWidget):
    def __getattr__(self, name: str) -> Any:
        return getattr(self.parent(), name)
