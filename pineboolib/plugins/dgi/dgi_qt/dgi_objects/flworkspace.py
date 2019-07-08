# -*- coding: utf-8 -*-
from pineboolib.plugins.dgi.dgi_qt.dgi_objects.flwidget import FLWidget
from typing import Any


class FLWorkSpace(FLWidget):
    def __getattr__(self, name: str) -> Any:
        return getattr(self.parent(), name)
