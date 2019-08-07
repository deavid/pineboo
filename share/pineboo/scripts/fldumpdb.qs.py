# -*- coding: utf-8 -*-
from pineboolib.qsa import qsa


class FormInternalObj(qsa.FormDBWidget):
    def _class_init(self):
        pass

    def main(self):
        qsa.sys.dumpDatabase()


form = None
