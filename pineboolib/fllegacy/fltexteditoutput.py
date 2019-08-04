# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets  # type: ignore
import sys
from typing import Union


class FLTextEditOutput(QtWidgets.QPlainTextEdit):
    oldStdout = None
    oldStderr = None

    def __init__(self, parent) -> None:
        super(FLTextEditOutput, self).__init__(parent)

        self.oldStdout = sys.stdout
        self.oldStderr = sys.stderr
        sys.stdout = self
        sys.stderr = self

    def write(self, txt: Union[bytearray, bytes, str]) -> None:
        txt = str(txt)
        if self.oldStdout:
            self.oldStdout.write(txt)
        self.appendPlainText(txt)

    def close(self) -> bool:
        if self.oldStdout:
            sys.stdout = self.oldStdout
        if self.oldStderr:
            sys.stderr = self.oldStderr
        return super().close()
