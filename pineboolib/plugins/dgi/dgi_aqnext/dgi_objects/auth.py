# -*- coding: utf-8 -*-
from pineboolib import decorators

class auth(object):
    
    @decorators.NotImplementedWarn
    def authenticate(**kwargs):
        print("Autenticando", kwargs)