# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
import sys

class FLTextEditOutput(QtWidgets.QPlainTextEdit):
    oldStdout = None
    oldStderr = None

    def __init__(self, parent):
        super(FLTextEditOutput, self).__init__(parent)

        self.oldStdout = sys.stdout
        self.oldStderr = sys.stderr
        sys.stdout = self
        sys.stderr = self

    def write(self, txt):
        self.oldStdout.write(txt)
        self.appendPlainText(str(txt))
    
    def close(self):
        sys.stdout = self.oldStdout
        sys.stderr = self.oldStderr
        super().close()