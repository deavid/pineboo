# # -*- coding: utf-8 -*-
from PyQt5.QtCore import QObject, QVariant


def bind(objectName, propertyName, type):
    """
        Utilidad para crear propiedades de estilo Qt fácilmente.
        Actualmente en desuso. Python tiene su propio sistema de propiedades y funciona bien.
    """

    def getter(self):
        return type(self.findChild(QObject, objectName).property(propertyName).toPyObject())

    def setter(self, value):
        self.findChild(QObject, objectName).setProperty(
            propertyName, QVariant(value))

    return property(getter, setter)
