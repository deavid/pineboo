from pineboolib.plugins.dgi.dgi_qt.dgi_objects.qdialog import QDialog
from pineboolib.plugins.dgi.dgi_qt.dgi_objects.qpushbutton import QPushButton
from pineboolib.plugins.dgi.dgi_qt.dgi_objects.qtabwidget import QTabWidget
from PyQt5 import QtCore, QtWidgets  # type: ignore
from typing import Any


class Dialog(QDialog):
    _layout: QtWidgets.QVBoxLayout
    buttonBox: QtWidgets.QDialogButtonBox
    okButtonText = "Aceptar"
    cancelButtonText = "Cancelar"
    okButton: QPushButton
    cancelButton: QPushButton
    _tab: QTabWidget

    def __init__(self, title=None, f=None, desc=None) -> None:
        # FIXME: f no lo uso , es qt.windowsflg
        super(Dialog, self).__init__()
        if title:
            self.setWindowTitle(str(title))

        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self._layout = QtWidgets.QVBoxLayout()
        self.setLayout(self._layout)
        self.buttonBox = QtWidgets.QDialogButtonBox()
        self.okButton = QPushButton("&Aceptar")
        self.cancelButton = QPushButton("&Cancelar")
        self.buttonBox.addButton(self.okButton, QtWidgets.QDialogButtonBox.AcceptRole)
        self.buttonBox.addButton(self.cancelButton, QtWidgets.QDialogButtonBox.RejectRole)
        self.okButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)
        self._tab = QTabWidget()
        self._tab.hide()
        self._layout.addWidget(self._tab)

    def add(self, _object) -> None:
        self._layout.addWidget(_object)

    def exec_(self) -> Any:
        if self.okButtonText:
            self.okButton.setText(str(self.okButtonText))
        if self.cancelButtonText:
            self.cancelButton.setText(str(self.cancelButtonText))
        self._layout.addWidget(self.buttonBox)

        return super(Dialog, self).exec_()

    def newTab(self, name) -> None:
        if self._tab.isHidden():
            self._tab.show()
        self._tab.addTab(QtWidgets.QWidget(), str(name))

    def __getattr__(self, name: str) -> Any:
        if name == "caption":
            name = "setWindowTitle"

        return getattr(super(Dialog, self), name)
