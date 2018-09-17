# -*- coding: utf-8 -*-
from pineboolib import decorators


class AQOdsGenerator_class(object):

    def __init__(self):
        from pineboolib.utils import checkDependencies
        checkDependencies({"odf": "odfpy"})


class AQOdsSpreadSheet(object):

    def __init__(self, generator):

        self.generator_ = generator


class AQOdsSheet(object):
    def __init__(self, spread_sheet, name):
        self.spread_sheet_ = spread_sheet
        self.name_ = name


class AQOdsRow(object):
    def __init__(self, sheet):
        self.sheet_ = sheet
        # soy una nueva linea en una hoja

    @decorators.NotImplementedWarn
    def addBgColor(self, color):
        # Añado color a la linea
        pass

    @decorators.NotImplementedWarn
    def opIn(self, opt):
        # Añade opcion a la linea
        pass

    @decorators.NotImplementedWarn
    def close(self):
        # Termina de editar la linea
        pass

    @decorators.NotImplementedWarn
    def coveredCell(self):
        pass


def AQOdsColor(color):
    return color


AQOdsGenerator = AQOdsGenerator_class()
