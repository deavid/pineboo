# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QFileDialog, QApplication
import os


class FileDialog(object):
    def getOpenFileName(*args):
        obj = QFileDialog.getOpenFileName(QApplication.activeModalWidget(), *args)
        return obj[0] if obj is not None else None

    def getSaveFileName(filter=None, title="Pineboo"):
        ret = QFileDialog.getSaveFileName(QApplication.activeModalWidget(), title, os.getenv("HOME"), filter)
        return ret[0] if ret else None

    def getExistingDirectory(basedir=None, title="Pineboo"):
        dir_ = basedir if basedir and os.path.exists(basedir) else "%s/" % os.getenv("HOME")
        ret = QFileDialog.getExistingDirectory(QApplication.activeModalWidget(), title, dir_, QFileDialog.ShowDirsOnly)
        return "%s/" % ret if ret else ret
