#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
"""
Start the application and give control to pineboolib.pnapplication().

Bootstrap. Se encarga de inicializar la aplicación y ceder el control a
pineboolib.pnapplication(); para ello acepta los parámetros necesarios de consola
y configura el programa adecuadamente.
"""


if __name__ == "__main__":
    from pineboolib.loader.main import startup

    startup()
