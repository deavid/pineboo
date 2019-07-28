# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets  # type: ignore
from pineboolib.core import decorators


from typing import Union, Optional, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from pineboolib.plugins.dgi.dgi_qt.dgi_objects.qframe import QFrame  # noqa: F401
    from pineboolib.plugins.dgi.dgi_qt.dgi_objects.qgroupbox import (
        QGroupBox,
    )  # noqa: F401
    from pineboolib.plugins.dgi.dgi_qt.dgi_objects.qwidget import QWidget  # noqa: F401


class QLineEdit(QtWidgets.QLineEdit):

    _parent = None
    WindowOrigin = 0

    def __init__(
        self,
        parent: Optional[Union["QGroupBox", "QWidget", "QFrame"]] = None,
        name: str = None,
    ) -> None:
        super(QLineEdit, self).__init__(parent)
        self._parent = parent
        if name:
            # self.setText(text)
            self.setObjectName(name)
        # if not project.DGI.localDesktop():
        #    project.DGI._par.addQueque("%s_CreateWidget" % self._parent.objectName(), "QLineEdit")

    def getText(self) -> Any:
        return super(QLineEdit, self).text()

    def setText(self, v) -> None:
        if not isinstance(v, str):
            v = str(v)
        super(QLineEdit, self).setText(v)
        # if not project.DGI.localDesktop():
        #    project.DGI._par.addQueque("%s_setText" % self._parent.objectName(), v)

    text = property(getText, setText)  # type: ignore

    @decorators.NotImplementedWarn
    def setBackgroundOrigin(self, bgo):
        pass

    @decorators.NotImplementedWarn
    def setLineWidth(self, w):
        pass

    @decorators.NotImplementedWarn
    def setFrameShape(self, f):
        pass

    @decorators.NotImplementedWarn
    def setFrameShadow(self, f):
        pass
