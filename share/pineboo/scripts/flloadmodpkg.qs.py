# -*- coding: utf-8 -*-
from pineboolib import qsatype
from pineboolib.qsaglobals import *
from pineboolib.qsatype import *


class FormInternalObj(FormDBWidget):
    def _class_init(self):
        pass

    def main(self):
        sys.loadModules()


form = None
