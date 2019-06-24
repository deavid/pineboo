# -*- coding: utf-8 -*-
from pineboolib.qsa import *
import traceback

sys = SysType()


class FormInternalObj(FormDBWidget):
    def _class_init(self):
        pass

    def main(self):
        sys.dumpDatabase()


form = None
