# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QFileDialog, QApplication  # type: ignore
import os
from typing import Optional, Any


class FileDialog(object):
    @staticmethod
    def getOpenFileName(path: str, *args: Any) -> Optional[str]:
        obj = QFileDialog.getOpenFileName(QApplication.activeWindow(), path, *args)
        return obj[0] if obj is not None else None

    @staticmethod
    def getSaveFileName(filter: str = "*", title: str = "Pineboo") -> Optional[str]:
        ret = QFileDialog.getSaveFileName(
            QApplication.activeWindow(), title, os.getenv("HOME") or ".", filter
        )
        return ret[0] if ret else None

    @staticmethod
    def getExistingDirectory(
        basedir: Optional[str] = None, title: str = "Pineboo"
    ) -> Optional[str]:
        dir_ = (
            basedir
            if basedir and os.path.exists(basedir)
            else "%s/" % os.getenv("HOME")
        )
        ret = QFileDialog.getExistingDirectory(
            QApplication.activeWindow(), title, dir_, QFileDialog.ShowDirsOnly
        )
        return "%s/" % ret if ret else ret
