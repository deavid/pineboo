# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets, QtGui  # type: ignore
from PyQt5.QtWidgets import QLabel  # type: ignore
from typing import Any, cast


class FLPixmapView(QtWidgets.QScrollArea):
    frame_ = None
    scrollView = None
    autoScaled_ = None
    path_ = None
    pixmap_ = None
    pixmapView_ = None
    lay_ = None
    gB_ = None
    _parent = None

    def __init__(self, parent) -> None:
        super(FLPixmapView, self).__init__(parent)
        self.autoScaled_ = False
        self.lay_ = QtWidgets.QHBoxLayout(self)
        self.lay_.setContentsMargins(0, 2, 0, 2)
        self.pixmap_ = QtGui.QPixmap()
        self.pixmapView_ = QLabel(self)
        self.lay_.addWidget(self.pixmapView_)
        self.pixmapView_.setAlignment(
            cast(
                QtCore.Qt.AlignmentFlag, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignCenter
            )
        )
        self.pixmapView_.installEventFilter(self)
        self.setStyleSheet(
            "QScrollArea { border: 1px solid darkgray; border-radius: 3px; }"
        )
        self._parent = parent

    def setPixmap(self, pix: QtGui.QPixmap) -> None:
        # if not project.DGI.localDesktop():
        #    project.DGI._par.addQueque("%s_setPixmap" % self._parent.objectName(
        #    ), self._parent.cursor_.valueBuffer(self._parent.fieldName_))
        #    return

        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        self.pixmap_ = pix
        if self.pixmapView_ is not None:
            self.pixmapView_.clear()
            self.pixmapView_.setPixmap(self.pixmap_)
        self.repaint()
        QtWidgets.QApplication.restoreOverrideCursor()

    def eventFilter(self, obj, ev) -> Any:

        if isinstance(obj, QLabel) and isinstance(ev, QtGui.QResizeEvent):
            self.resizeContents()

        return super(FLPixmapView, self).eventFilter(obj, ev)

    def resizeContents(self) -> None:

        if self.pixmap_ is None or self.pixmap_.isNull():
            return

        new_pix = self.pixmap_
        if (
            self.autoScaled_ is not None
            and self.pixmap_ is not None
            and self.pixmapView_ is not None
        ):
            if (
                self.pixmap_.height() > self.pixmapView_.height()
                or self.pixmap_.width() > self.pixmapView_.width()
            ):
                new_pix = self.pixmap_.scaled(
                    self.pixmapView_.size(), QtCore.Qt.KeepAspectRatio
                )

            elif (
                self.pixmap_.height() < self.pixmapView_.pixmap().height()
                or self.pixmap_.width() < self.pixmapView_.pixmap().width()
            ):
                new_pix = self.pixmap_.scaled(
                    self.pixmapView_.size(), QtCore.Qt.KeepAspectRatio
                )

        if self.pixmapView_ is not None:
            self.pixmapView_.clear()
            self.pixmapView_.setPixmap(new_pix)

    def previewUrl(self, url) -> None:
        u = QtCore.QUrl(url)
        if u.isLocalFile():
            path = u.path()

        if not path == self.path_:
            self.path_ = path
            img = QtGui.QImage(self.path_)

            if img is None:
                return

            pix = QtGui.QPixmap()
            QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
            pix.convertFromImage(img)
            QtWidgets.QApplication.restoreOverrideCursor()

            if pix is not None:
                self.setPixmap(pix)

    def clear(self) -> None:
        if self.pixmapView_ is not None:
            self.pixmapView_.clear()

    def pixmap(self) -> Any:
        return self.pixmap_

    def setAutoScaled(self, autoScaled) -> None:
        self.autoScaled_ = autoScaled
