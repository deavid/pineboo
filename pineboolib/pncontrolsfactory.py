# -*- coding: utf-8 -*-
import pineboolib
import logging
logger = logging.getLogger("PNControlsFactory")

"""
Conjunto de controles usados en Pineboo. Estos son cargados desde el DGI seleccionado en el proyecto
"""

"""
Devuelve un objecto a partir de su nombre
@param name, Nombre del objecto a buscar
@return objecto o None si no existe el objeto buscado
"""


def resolveObject(name):
    ret_ = pineboolib.project.resolveDGIObject(name)
    return ret_


QComboBox = resolveObject("QComboBox")
QTable = resolveObject("QTable")
QLayoutWidget = resolveObject("QLayoutWidget")
QTabWidget = resolveObject("QTabWidget")
QGroupBox = resolveObject("QGroupBox")
QListView = resolveObject("QListView")
QPushButton = resolveObject("QPushButton")
QTextEdit = resolveObject("QTextEdit")
QLineEdit = resolveObject("QLineEdit")
QCheckBox = resolveObject("QCheckBox")
FLLineEdit = resolveObject("FLLineEdit")
FLTimeEdit = resolveObject("FLTimeEdit")
FLDateEdit = resolveObject("FLDateEdit")
FLPixmapView = resolveObject("FLPixmapView")
