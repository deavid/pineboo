# -*- coding: utf-8 -*-
from pineboolib.core import decorators


class auth(object):
    @decorators.NotImplementedWarn
    def authenticate(**kwargs):
        print("Autenticando", kwargs)
