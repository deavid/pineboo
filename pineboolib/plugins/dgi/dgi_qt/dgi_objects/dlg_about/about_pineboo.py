# -*- coding: utf-8 -*-
"""About_pineboo module."""

from PyQt5 import QtWidgets


class AboutPineboo(QtWidgets.QWidget):
    """AboutPineboo class."""

    ui = None

    def __init__(self) -> None:
        """Inicialize."""

        super().__init__()
        self.load()

    def load(self) -> None:
        """Load widget and show."""

        from pineboolib import application
        from pineboolib.core.utils.utils_base import filedir

        dlg_ = filedir("plugins/dgi/dgi_qt/dgi_objects/dlg_about/about_pineboo.ui")
        version_ = application.project.version
        self.ui = None
        if application.project._DGI:
            self.ui = application.project.DGI.createUI(dlg_, None, self)
        if self.ui is None:
            raise Exception("Error creating UI About Dialog")
        self.ui.lbl_version.setText("Pineboo %s" % str(version_))
        self.ui.btn_close.clicked.connect(self.ui.close)
        self.ui.btn_clipboard.clicked.connect(self.to_clipboard)
        self.ui.show()

        self.ui.lbl_librerias.setText(self.load_components())

    def load_components(self) -> str:
        """Resume libraries loaded."""

        from PyQt5 import QtCore  # type: ignore
        import platform
        from pineboolib.core.utils.check_dependencies import DEPENDENCIES_CHECKED

        components = "Versiones de componentes:\n\n"
        components += "S.O.: %s %s %s\n" % (
            platform.system(),
            platform.release(),
            platform.version(),
        )
        # py_ver = sys.version
        # if py_ver.find("(") > -1:
        #    py_ver = py_ver[:py_ver.find("(")]

        # components += "Python: %s\n" % py_ver

        if "PyQt5.QtCore" not in DEPENDENCIES_CHECKED.keys():
            components += "PyQt5.QtCore: %s\n" % QtCore.QT_VERSION_STR

        for k in DEPENDENCIES_CHECKED.keys():
            components += "%s: %s\n" % (k, DEPENDENCIES_CHECKED[k])

        return components

    def to_clipboard(self) -> None:
        """Copy resume libraries loaded into clipboard."""

        from PyQt5.QtWidgets import QApplication  # type: ignore

        clip_board = QApplication.clipboard()
        clip_board.clear()
        clip_board.setText(self.load_components())
