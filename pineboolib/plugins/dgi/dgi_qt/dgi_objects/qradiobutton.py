# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets

class QRadioButton(QtWidgets.QRadioButton):

    def __ini__(self):
        super(QRadioButton, self).__init__()
        self.setChecked(False)

    def __setattr__(self, name, value):
        if name == "text":
            self.setText(value)
        elif name == "checked":
            self.setChecked(value)
        else:
            super(RadioButton, self).__setattr__(name, value)

    def __getattr__(self, name):
        if name == "checked":
            return self.isChecked()