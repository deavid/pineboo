# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog

class FileDialog(QFileDialog):

    def getOpenFileName(*args):
        obj = None
        parent = QtWidgets.QApplication.activeModalWidget()
        if len(args) == 1:
            obj = QFileDialog.getOpenFileName(parent, str(args[0]))
        elif len(args) == 2:
            obj = QFileDialog.getOpenFileName(parent, str(args[0]), str(args[1]))
        elif len(args) == 3:
            obj = QFileDialog.getOpenFileName(parent, str(args[0]), str(args[1]), str(args[2]))
        elif len(args) == 4:
            obj = QFileDialog.getOpenFileName(parent, str(args[0]), str(args[1]), str(args[2]), str(args[3]))

        if obj is None:
            return None

        return obj[0]
    
    
    def getSaveFileName(filter=None):
        parent = QtWidgets.QApplication.activeModalWidget()
        from pineboolib.utils import filedir
        basedir = filedir("..")
        ret = QFileDialog.getSaveFileName(parent,"caption",basedir,filter)
        
        return ret[0] if ret else None


    def getExistingDirectory(basedir=None, caption=None):
        if not basedir:
            from pineboolib.utils import filedir
            basedir = filedir("..")

        parent = QtWidgets.QApplication.activeModalWidget()
        ret = QFileDialog.getExistingDirectory(parent, caption, basedir, QtWidgets.QFileDialog.ShowDirsOnly)
        if ret:
            ret = ret + "/"

        return ret