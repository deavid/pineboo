# -*- coding: utf-8 -*-
from PyQt5 import QtCore

class FLSqlCursor(QtCore.QObject):
    
    def __init__(self):
        super().__init__()
    
    def setActivatedCommitActions(self, activated_commitactions):
        self._activatedCommitActions = activated_commitactions

    def setActivatedBufferChanged(self, activated_bufferchanged):
        self._activatedBufferChanged = activated_bufferchanged

    def setActivatedBufferCommited(self, activated_buffercommited):
        self._activatedBufferCommited = activated_buffercommited
        