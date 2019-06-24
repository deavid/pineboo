# -*- coding: utf-8 -*-
from pineboolib.plugins.dgi.dgi_qt.dgi_objects.flwidget import FLWidget


class FLWorkSpace(FLWidget):
    def __getattr__(self, name):
        return getattr(self.parent(), name)
