# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
import os
        
class FileDialog(object):

    def getOpenFileName(*args):
        obj = QtWidgets.QFileDialog.getOpenFileName(None, *args)
        return obj[0] if obj is not None else None
    
    
    def getSaveFileName(filter=None):
        ret = QtWidgets.QFileDialog.getSaveFileName(None, 'Pineboo', os.getenv('HOME'), 'CSV(*.csv)')
        return ret[0] if ret else None
        

    def getExistingDirectory(basedir=None, caption=None):
        ret = QtWidgets.QFileDialog.getExistingDirectory(None, caption, os.getenv('HOME'), QtWidgets.QFileDialog.ShowDirsOnly)
        return "%s/" % ret if ret else ret