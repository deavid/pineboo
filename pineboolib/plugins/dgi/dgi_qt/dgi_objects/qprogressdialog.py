# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets

class ProgressDialog(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(ProgressDialog, self).__init__(*args, **kwargs)
        self.title = "Untitled"
        self.step = 0
        self.steps = 100

    def __getattr__(self, name):
        return DefFun(self, name)

    def setup(self, title, steps):
        self.title = title
        self.step = 0
        self.steps = steps
        self.setWindowTitle("%s - %d/%d" % (self.title, self.step, self.steps))
        self.setWindowModality(QtCore.Qt.ApplicationModal)

    def setProgress(self, step):
        self.step = step
        self.setWindowTitle("%s - %d/%d" % (self.title, self.step, self.steps))
        if step > 0:
            self.show()
        self.update()
        QtCore.QCoreApplication.processEvents(
            QtCore.QEventLoop.ExcludeUserInputEvents)