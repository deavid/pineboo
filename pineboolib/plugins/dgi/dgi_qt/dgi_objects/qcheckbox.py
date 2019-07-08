# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtCore  # type: ignore


class QCheckBox(QtWidgets.QCheckBox):

    _parent = None

    def __init__(self, parent) -> None:
        self._parent = parent
        super().__init__(parent)

    @QtCore.pyqtProperty(int)
    def checked(self):
        return self.isChecked()

    @checked.setter
    def checked(self, b):
        if isinstance(b, str):
            b = b == "true"

        super().setChecked(b)
        # if not project._DGI.localDesktop():
        #    project._DGI._par.addQueque("%s_setChecked" % self._parent.objectName(), b)
