# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
import os


class FileDialog(object):
    def getOpenFileName(*args):
        obj = QtWidgets.QFileDialog.getOpenFileName(None, *args)
        return obj[0] if obj is not None else None

    def getSaveFileName(filter=None, title="Pineboo"):
        ret = QtWidgets.QFileDialog.getSaveFileName(None, title, os.getenv("HOME"), filter)
        return ret[0] if ret else None

    def getExistingDirectory(basedir=None, title="Pineboo"):
        dir_ = basedir if basedir and os.path.exists(basedir) else "%s/" % os.getenv("HOME")
        ret = QtWidgets.QFileDialog.getExistingDirectory(None, title, dir_, QtWidgets.QFileDialog.ShowDirsOnly)
        return "%s/" % ret if ret else ret
