# -*- coding: utf-8 -*-
from pineboolib.qsa import qsa

sys = qsa.SysType()


class FormInternalObj(qsa.FormDBWidget):
    def _class_init(self):
        pass

    def init(self):
        connect(self.cursor(), u"cursorUpdated()", self, u"actualizarAreas")

    def actualizarAreas(self):
        qsa.sys.updateAreas()


form = None
