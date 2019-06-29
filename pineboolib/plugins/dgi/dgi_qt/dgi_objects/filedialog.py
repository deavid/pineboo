# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QFileDialog, QApplication
import os
from typing import Any


class FileDialog(object):
    def getOpenFileName(*args) -> Any:
        obj = QFileDialog.getOpenFileName(QApplication.activeWindow(), *args)
        return obj[0] if obj is not None else None

    def getSaveFileName(filter: str = None, title="Pineboo") -> Any:
        ret = QFileDialog.getSaveFileName(QApplication.activeWindow(), title, os.getenv("HOME"), filter)
        return ret[0] if ret else None

    def getExistingDirectory(basedir: str = None, title="Pineboo") -> Any:
        dir_ = basedir if basedir and os.path.exists(basedir) else "%s/" % os.getenv("HOME")
        ret = QFileDialog.getExistingDirectory(QApplication.activeWindow(), title, dir_, QFileDialog.ShowDirsOnly)
        return "%s/" % ret if ret else ret
